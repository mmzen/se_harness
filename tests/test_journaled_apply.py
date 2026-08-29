"""The retained journaled apply: the fault matrix of the Phase 4 broker, re-pointed.

ADR-ECP-002 keeps one property of `se_harness/effect_broker.py`: a multi-file
write that completes as a whole or restores every pre-image, and stops for a
human when it cannot prove which. These are the broker's fault-matrix cases
(`tests/test_effect_broker.py` before WO-ECP-006) over `journaled_apply`.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from se_harness.journaled_apply import (
    ACTIVE_JOURNAL,
    HUMAN_RECOVERY_STOP,
    JournaledApplyError,
    Target,
    apply_journaled,
    read_journal,
    recover_journaled,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class JournaledApplyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.target = self.base / "target"
        self.journal = self.base / "journal"
        self._reset()

    def _reset(self) -> None:
        import shutil

        for path in (self.target, self.journal):
            if path.exists():
                shutil.rmtree(path)
        self.target.mkdir()
        (self.target / "files").mkdir()
        (self.target / "files/delete.txt").write_bytes(b"delete")
        (self.target / "files/replace.txt").write_bytes(b"before")

    def _targets(self) -> list[Target]:
        return [
            Target("files/delete.txt", b"delete", None),
            Target("files/nested/create.txt", None, b"created"),
            Target("files/replace.txt", b"before", b"after"),
        ]

    def _manifest(self) -> dict[str, str]:
        return {
            path.relative_to(self.target).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(self.target.rglob("*"))
            if path.is_file()
        }

    def _apply(self, **overrides):
        values = {"journal_directory": self.journal, "transaction_id": "7" * 32}
        values.update(overrides)
        return apply_journaled(self.target, self._targets(), **values)

    def test_create_replace_delete_commit_as_a_whole(self) -> None:
        result = self._apply()
        self.assertEqual("committed", result.outcome)
        self.assertEqual(
            {"files/nested/create.txt": hashlib.sha256(b"created").hexdigest(), "files/replace.txt": hashlib.sha256(b"after").hexdigest()},
            self._manifest(),
        )
        self.assertIsNone(read_journal(self.journal))
        self.assertTrue(result.journal_path.exists())
        self.assertEqual("committed", json.loads(result.journal_path.read_bytes())["state"])
        self.assertFalse(list(self.target.rglob("*.part")))

    def test_stale_target_aborts_before_the_journal_is_written(self) -> None:
        # ECP-JNL-005: the bytes planned against must be the bytes on disk.
        (self.target / "files/replace.txt").write_bytes(b"changed")
        before = self._manifest()
        with self.assertRaisesRegex(JournaledApplyError, "JNL007"):
            self._apply()
        self.assertEqual(before, self._manifest())
        self.assertFalse((self.journal / ACTIVE_JOURNAL).exists())
        self.assertFalse((self.journal / ("7" * 32)).exists())

    def test_injected_apply_failure_restores_exact_prior_state(self) -> None:
        before = self._manifest()

        def fail(stage: str) -> None:
            if stage.startswith("after-apply:"):
                raise OSError("injected apply fault")

        with self.assertRaisesRegex(JournaledApplyError, "prior state was restored"):
            self._apply(fault=fail)
        self.assertEqual(before, self._manifest())
        self.assertIsNone(read_journal(self.journal))
        self.assertFalse((self.target / "files/nested").exists())

    def test_every_in_process_fault_stage_restores_prior_state(self) -> None:
        stages = (
            "before-journal",
            "after-journal-prepared",
            "after-parent:files/nested",
            "after-temp:files/nested/create.txt",
            "after-temp:files/replace.txt",
            "after-apply:files/delete.txt",
            "after-apply:files/nested/create.txt",
            "after-apply:files/replace.txt",
            "before-commit",
        )
        for index, selected in enumerate(stages, start=1):
            with self.subTest(stage=selected):
                self._reset()
                before = self._manifest()

                def fail(stage: str, selected: str = selected) -> None:
                    if stage == selected:
                        raise OSError(f"injected fault at {selected}")

                with self.assertRaisesRegex(JournaledApplyError, "JNL010"):
                    self._apply(fault=fail, transaction_id=f"{index:032x}")
                self.assertEqual(before, self._manifest())
                self.assertIsNone(read_journal(self.journal))
                self.assertFalse(list(self.target.rglob("*.part")))

    def test_post_commit_fault_requires_recovery_then_keeps_the_result(self) -> None:
        def fail(stage: str) -> None:
            if stage == "after-journal-commit":
                raise OSError("injected post-commit finalization fault")

        with self.assertRaisesRegex(JournaledApplyError, "JNL013"):
            self._apply(fault=fail)
        self.assertEqual("committed", read_journal(self.journal)["state"])
        recovered = recover_journaled(self.target, journal_directory=self.journal)
        self.assertEqual("recovered-result", recovered.outcome)
        self.assertEqual(b"after", (self.target / "files/replace.txt").read_bytes())
        self.assertIsNone(read_journal(self.journal))

    def test_interruption_leaves_journal_and_restart_recovers_prior(self) -> None:
        before = self._manifest()

        def interrupt(stage: str) -> None:
            if stage.startswith("after-apply:"):
                raise SystemExit("simulated process termination")

        with self.assertRaises(SystemExit):
            self._apply(fault=interrupt)
        self.assertIsNotNone(read_journal(self.journal))
        recovered = recover_journaled(self.target, journal_directory=self.journal)
        self.assertEqual("recovered-prior", recovered.outcome)
        self.assertEqual(before, self._manifest())
        self.assertIsNone(read_journal(self.journal))

    def test_interruption_at_each_durable_stage_recovers_prior(self) -> None:
        stages = (
            "after-journal-prepared",
            "after-apply:files/delete.txt",
            "after-apply:files/nested/create.txt",
            "after-apply:files/replace.txt",
            "before-commit",
        )
        for index, selected in enumerate(stages, start=16):
            with self.subTest(stage=selected):
                self._reset()
                before = self._manifest()

                def interrupt(stage: str, selected: str = selected) -> None:
                    if stage == selected:
                        raise SystemExit(f"simulated termination at {selected}")

                with self.assertRaises(SystemExit):
                    self._apply(fault=interrupt, transaction_id=f"{index:032x}")
                self.assertIsNotNone(read_journal(self.journal))
                recovered = recover_journaled(self.target, journal_directory=self.journal)
                self.assertEqual("recovered-prior", recovered.outcome)
                self.assertEqual(before, self._manifest())
                self.assertIsNone(read_journal(self.journal))

    def test_process_exit_leaves_a_journal_a_new_process_recovers(self) -> None:
        before = self._manifest()
        script = """
import sys
from pathlib import Path
from se_harness.journaled_apply import Target, apply_journaled
target, journal = Path(sys.argv[1]), Path(sys.argv[2])
def interrupt(stage):
    if stage == "after-apply:files/delete.txt":
        raise SystemExit(3)
apply_journaled(target, [
    Target("files/delete.txt", b"delete", None),
    Target("files/nested/create.txt", None, b"created"),
    Target("files/replace.txt", b"before", b"after"),
], journal_directory=journal, transaction_id="8" * 32, fault=interrupt)
"""
        completed = subprocess.run(
            [sys.executable, "-c", script, str(self.target), str(self.journal)],
            cwd=REPOSITORY_ROOT, capture_output=True, text=True,
        )
        self.assertEqual(3, completed.returncode, completed.stderr)
        self.assertEqual("applying", read_journal(self.journal)["state"])
        recovered = recover_journaled(self.target, journal_directory=self.journal)
        self.assertEqual("recovered-prior", recovered.outcome)
        self.assertEqual(before, self._manifest())

    def test_corrupt_backup_stops_for_human_recovery_and_blocks_further_writes(self) -> None:
        def interrupt(stage: str) -> None:
            if stage == "after-apply:files/delete.txt":
                raise SystemExit("simulated process termination")

        with self.assertRaises(SystemExit):
            self._apply(fault=interrupt)
        backup = self.journal / ("7" * 32) / "backups" / hashlib.sha256(b"delete").hexdigest()
        self.assertTrue(backup.exists())
        backup.write_bytes(b"corrupt")
        with self.assertRaisesRegex(JournaledApplyError, "WEX-ECP-041"):
            recover_journaled(self.target, journal_directory=self.journal)
        journal = read_journal(self.journal)
        self.assertEqual(HUMAN_RECOVERY_STOP, journal["state"])
        self.assertEqual(["files/delete.txt", "files/nested/create.txt", "files/replace.txt"], journal["uncertain_paths"])
        # ECP-JNL-003: nothing writes until the journal is resolved.
        with self.assertRaisesRegex(JournaledApplyError, "WEX-ECP-042"):
            apply_journaled(
                self.target, [Target("files/replace.txt", b"before", b"other")],
                journal_directory=self.journal, transaction_id="9" * 32,
            )
        with self.assertRaisesRegex(JournaledApplyError, "WEX-ECP-041"):
            recover_journaled(self.target, journal_directory=self.journal)

    def test_interruption_after_journal_commit_recovers_the_result(self) -> None:
        def interrupt(stage: str) -> None:
            if stage == "after-journal-commit":
                raise SystemExit("simulated post-commit termination")

        with self.assertRaises(SystemExit):
            self._apply(fault=interrupt)
        recovered = recover_journaled(self.target, journal_directory=self.journal)
        self.assertEqual("recovered-result", recovered.outcome)
        self.assertEqual("committed", json.loads(recovered.journal_path.read_bytes())["state"])
        self.assertEqual(b"after", (self.target / "files/replace.txt").read_bytes())

    def test_checksum_mismatched_journal_blocks_recovery(self) -> None:
        def interrupt(stage: str) -> None:
            if stage == "after-journal-prepared":
                raise SystemExit("simulated process termination")

        with self.assertRaises(SystemExit):
            self._apply(fault=interrupt)
        path = self.journal / ACTIVE_JOURNAL
        value = json.loads(path.read_bytes())
        value["entries"][0]["path"] = "files/other.txt"
        path.write_bytes(json.dumps(value).encode("utf-8"))
        with self.assertRaisesRegex(JournaledApplyError, "JNL005"):
            recover_journaled(self.target, journal_directory=self.journal)

    @unittest.skipUnless(sys.platform == "win32", "a held-open destination refuses replacement on Windows only")
    def test_locked_destination_rolls_back_prior_entries_on_windows(self) -> None:
        before = self._manifest()
        handle = (self.target / "files/replace.txt").open("rb")
        try:
            with self.assertRaisesRegex(JournaledApplyError, "JNL010"):
                self._apply()
            self.assertEqual(before, self._manifest())
            self.assertEqual(b"before", (self.target / "files/replace.txt").read_bytes())
            self.assertIsNone(read_journal(self.journal))
        finally:
            handle.close()

    def test_paths_are_untrusted_and_a_link_is_refused(self) -> None:
        for path in ("../escape.txt", "/abs.txt", "files\\win.txt", "files/./x.txt", ""):
            with self.subTest(path=path), self.assertRaisesRegex(JournaledApplyError, "JNL001"):
                apply_journaled(self.target, [Target(path, None, b"x")], journal_directory=self.journal)
        with self.assertRaisesRegex(JournaledApplyError, "JNL001"):
            apply_journaled(
                self.target, [Target("files/a.txt", None, b"x"), Target("files/A.txt", None, b"y")],
                journal_directory=self.journal,
            )
        self.assertIsNone(read_journal(self.journal))


if __name__ == "__main__":
    unittest.main()
