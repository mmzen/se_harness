from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import se_harness.renumber as renumber
from se_harness.cli import main
from se_harness.renumber import RenumberError, normalize_mappings


class ArtifactRenumberingTests(unittest.TestCase):
    def setUp(self) -> None:
        if shutil.which("git") is None:
            self.skipTest("Git is required")
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "repository"
        self.assertEqual(0, self.invoke("init", str(self.root), "--project-name", "Renumber Sample")[0])
        self._write_fixture()
        self._git("init")
        self._git("config", "user.email", "renumber@example.invalid")
        self._git("config", "user.name", "Renumber Test")
        self._git("add", "-A")
        self._git("commit", "-m", "baseline")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def invoke(self, *arguments: str) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = main(list(arguments))
        return code, stdout.getvalue(), stderr.getvalue()

    def _git(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        completed = subprocess.run(
            [shutil.which("git") or "git", *arguments],
            cwd=self.root,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        return completed

    def _write_fixture(self) -> None:
        intent = self.root / "docs/engineering/simulation/intent/INT-SIM-001.md"
        capability = self.root / "docs/engineering/simulation/capabilities/CAP-SIM-001.md"
        evidence = self.root / "docs/engineering/simulation/evidence/INT-SIM-001-output.txt"
        binary = self.root / "assets/INT-SIM-001.bin"
        notes = self.root / "notes/references.md"
        for path in (intent, capability, evidence, binary, notes):
            path.parent.mkdir(parents=True, exist_ok=True)
        intent.write_text(
            '''+++
id = "INT-SIM-001"
type = "intent"
title = "Simulate a renumbering"
status = "draft"
owners = ["product-owner"]
created = "2026-08-20"
updated = "2026-08-20"

[relations]
+++

# Intent

The current hard reference is INT-SIM-001.
''',
            encoding="utf-8",
        )
        capability.write_text(
            '''+++
id = "CAP-SIM-001"
type = "capability"
title = "Exercise a simulated capability"
status = "draft"
owners = ["product-owner"]
created = "2026-08-20"
updated = "2026-08-20"

[relations]
derives_from = ["INT-SIM-001"]
+++

# Capability
''',
            encoding="utf-8",
        )
        evidence.write_bytes(b"captured INT-SIM-001\r\n")
        binary.write_bytes(b"\x00captured INT-SIM-001\xff")
        notes.write_bytes(
            b"\xef\xbb\xbfline one\r\nmanual INT-SIM-001\r"
            b"lookalike XINT-SIM-001Y must not match\n"
        )

    def _commit_all(self, message: str) -> None:
        self._git("add", "-A")
        self._git("commit", "-m", message)

    def test_plan_is_read_only_and_apply_changes_only_structured_fields_and_paths(self) -> None:
        original_intent = (
            self.root / "docs/engineering/simulation/intent/INT-SIM-001.md"
        ).read_bytes()
        original_evidence = (
            self.root / "docs/engineering/simulation/evidence/INT-SIM-001-output.txt"
        ).read_bytes()
        original_binary = (self.root / "assets/INT-SIM-001.bin").read_bytes()

        code, output, error = self.invoke(
            "renumber-artifacts",
            str(self.root),
            "--map",
            "INT-SIM-001=INT-SIM-002",
            "--json",
        )
        self.assertEqual(0, code, error)
        plan = json.loads(output)
        self.assertEqual("plan", plan["mode"])
        self.assertFalse(plan["applied"])
        self.assertTrue(plan["manual_action_required"])
        self.assertFalse(plan["repository_repair_complete"])
        self.assertEqual(2, len(plan["manual_references"]))
        self.assertEqual(1, len(plan["preserved_evidence_references"]))
        self.assertEqual(1, len(plan["unsupported_references"]))
        self.assertEqual("2", str(plan["manual_references"][1]["line"]))
        self.assertEqual("", self._git("status", "--porcelain", "--untracked-files=all").stdout)
        self.assertTrue((self.root / "docs/engineering/simulation/intent/INT-SIM-001.md").is_file())

        code, output, error = self.invoke(
            "renumber-artifacts",
            str(self.root),
            "--map",
            "INT-SIM-001=INT-SIM-002",
            "--json",
            "--apply",
        )
        self.assertEqual(0, code, error)
        result = json.loads(output)
        self.assertTrue(result["applied"])
        self.assertTrue(result["manual_action_required"])
        self.assertFalse(result["repository_repair_complete"])

        new_intent = self.root / "docs/engineering/simulation/intent/INT-SIM-002.md"
        self.assertTrue(new_intent.is_file())
        self.assertFalse((self.root / "docs/engineering/simulation/intent/INT-SIM-001.md").exists())
        expected_intent = original_intent.replace(
            b'id = "INT-SIM-001"', b'id = "INT-SIM-002"'
        )
        self.assertEqual(expected_intent, new_intent.read_bytes())
        self.assertIn(b"hard reference is INT-SIM-001", new_intent.read_bytes())

        capability = (
            self.root / "docs/engineering/simulation/capabilities/CAP-SIM-001.md"
        ).read_bytes()
        self.assertIn(b'derives_from = ["INT-SIM-002"]', capability)
        self.assertNotIn(b'derives_from = ["INT-SIM-001"]', capability)

        new_evidence = self.root / "docs/engineering/simulation/evidence/INT-SIM-002-output.txt"
        new_binary = self.root / "assets/INT-SIM-002.bin"
        self.assertEqual(original_evidence, new_evidence.read_bytes())
        self.assertEqual(original_binary, new_binary.read_bytes())
        manual_paths = {item["resulting_path"] for item in result["manual_references"]}
        self.assertIn("docs/engineering/simulation/intent/INT-SIM-002.md", manual_paths)

    def test_human_output_makes_incomplete_manual_repair_explicit(self) -> None:
        code, output, error = self.invoke(
            "renumber-artifacts",
            str(self.root),
            "--map",
            "INT-SIM-001=INT-SIM-002",
        )
        self.assertEqual(0, code, error)
        self.assertIn("MANUAL ACTION REQUIRED", output)
        self.assertIn("PRESERVED EVIDENCE REFERENCES", output)
        self.assertIn("UNSUPPORTED REFERENCES", output)
        self.assertIn("REPOSITORY REPAIR COMPLETE: no", output)
        self.assertIn("No files were written", output)

    def test_multi_map_plan_is_order_independent_and_repairs_cross_relations(self) -> None:
        first = [
            "--map", "CAP-SIM-001=CAP-SIM-002",
            "--map", "INT-SIM-001=INT-SIM-002",
        ]
        second = [
            "--map", "INT-SIM-001=INT-SIM-002",
            "--map", "CAP-SIM-001=CAP-SIM-002",
        ]
        code, first_output, error = self.invoke(
            "renumber-artifacts", str(self.root), *first, "--json"
        )
        self.assertEqual(0, code, error)
        code, second_output, error = self.invoke(
            "renumber-artifacts", str(self.root), *second, "--json"
        )
        self.assertEqual(0, code, error)
        self.assertEqual(json.loads(first_output), json.loads(second_output))

        code, _, error = self.invoke(
            "renumber-artifacts", str(self.root), *first, "--apply"
        )
        self.assertEqual(0, code, error)
        capability = self.root / "docs/engineering/simulation/capabilities/CAP-SIM-002.md"
        self.assertTrue(capability.is_file())
        content = capability.read_text(encoding="utf-8")
        self.assertIn('id = "CAP-SIM-002"', content)
        self.assertIn('derives_from = ["INT-SIM-002"]', content)

    def test_structured_edit_preserves_utf8_bom_and_crlf_bytes(self) -> None:
        intent = self.root / "docs/engineering/simulation/intent/INT-SIM-001.md"
        original_text = intent.read_text(encoding="utf-8")
        intent.write_bytes(b"\xef\xbb\xbf" + original_text.replace("\n", "\r\n").encode("utf-8"))
        self._commit_all("use bom and crlf")
        code, _, error = self.invoke(
            "renumber-artifacts",
            str(self.root),
            "--map",
            "INT-SIM-001=INT-SIM-002",
            "--apply",
        )
        self.assertEqual(0, code, error)
        result = (
            self.root / "docs/engineering/simulation/intent/INT-SIM-002.md"
        ).read_bytes()
        self.assertTrue(result.startswith(b"\xef\xbb\xbf"))
        self.assertNotIn(b"\n", result.replace(b"\r\n", b""))
        self.assertEqual(
            b"\xef\xbb\xbf"
            + original_text.replace('id = "INT-SIM-001"', 'id = "INT-SIM-002"')
            .replace("\n", "\r\n")
            .encode("utf-8"),
            result,
        )

    def test_ineligible_lifecycle_and_existing_destination_block_the_plan(self) -> None:
        intent = self.root / "docs/engineering/simulation/intent/INT-SIM-001.md"
        intent.write_text(
            intent.read_text(encoding="utf-8").replace('status = "draft"', 'status = "ready"'),
            encoding="utf-8",
        )
        self._commit_all("make intent ready")
        code, output, _ = self.invoke(
            "renumber-artifacts", str(self.root), "--map", "INT-SIM-001=INT-SIM-002", "--json"
        )
        self.assertEqual(1, code)
        self.assertIn("lifecycle is not eligible", output)

        intent.write_text(
            intent.read_text(encoding="utf-8").replace('status = "ready"', 'status = "draft"'),
            encoding="utf-8",
        )
        collision = self.root / "docs/engineering/simulation/evidence/INT-SIM-002-output.txt"
        collision.write_text("pre-existing destination\n", encoding="utf-8")
        self._commit_all("add destination collision")
        code, output, _ = self.invoke(
            "renumber-artifacts", str(self.root), "--map", "INT-SIM-001=INT-SIM-002", "--json"
        )
        self.assertEqual(1, code)
        self.assertIn("multiple paths map to one destination", output)

    def test_dirty_repository_and_invalid_maps_fail_without_writing(self) -> None:
        before = self._git("status", "--porcelain", "--untracked-files=all").stdout
        code, output, error = self.invoke(
            "renumber-artifacts",
            str(self.root),
            "--map",
            "INT-SIM-001=CAP-SIM-002",
            "--json",
        )
        self.assertEqual(1, code)
        self.assertEqual("blocked", json.loads(output)["mode"])
        self.assertIn("type-compatible", output)
        self.assertEqual(before, self._git("status", "--porcelain", "--untracked-files=all").stdout)

        (self.root / "dirty.txt").write_text("dirty\n", encoding="utf-8")
        code, output, error = self.invoke(
            "renumber-artifacts",
            str(self.root),
            "--map",
            "INT-SIM-001=INT-SIM-002",
            "--json",
            "--apply",
        )
        self.assertEqual(1, code)
        self.assertIn("clean Git worktree", output)
        self.assertFalse((self.root / "docs/engineering/simulation/intent/INT-SIM-002.md").exists())

    def test_postcondition_failure_restores_original_repository(self) -> None:
        before = {
            path.relative_to(self.root).as_posix(): path.read_bytes()
            for path in self.root.rglob("*")
            if path.is_file() and ".git" not in path.parts
        }
        injected = RenumberError("TEST", "postcondition", "injected failure")
        with mock.patch("se_harness.renumber._postconditions", side_effect=injected):
            code, _, error = self.invoke(
                "renumber-artifacts",
                str(self.root),
                "--map",
                "INT-SIM-001=INT-SIM-002",
                "--apply",
            )
        self.assertEqual(1, code)
        self.assertIn("injected failure", error)
        self.assertIn("rollback restored the original repository", error)
        after = {
            path.relative_to(self.root).as_posix(): path.read_bytes()
            for path in self.root.rglob("*")
            if path.is_file() and ".git" not in path.parts
        }
        self.assertEqual(before, after)
        self.assertEqual("", self._git("status", "--porcelain", "--untracked-files=all").stdout)
        self.assertEqual([], list(self.root.glob(".harness-renumber-recovery-*")))

    def test_commit_bound_record_reference_blocks_all_writes(self) -> None:
        report = renumber._validator_report(self.root)
        record = self.root / "docs/engineering/verification-records/VREC-SIM-001.md"
        record.parent.mkdir(parents=True, exist_ok=True)
        record.write_text(
            '''+++
id = "VREC-SIM-001"
type = "verification_record"
title = "Captured reference"
status = "ready"
owners = ["quality-owner"]
created = "2026-08-20"
updated = "2026-08-20"

[relations]
verifies_work_order = ["INT-SIM-001"]
+++

# Captured record
''',
            encoding="utf-8",
        )
        self._commit_all("add mocked commit-bound record")
        report["artifacts"].append(
            {
                "id": "VREC-SIM-001",
                "type": "verification_record",
                "status": "ready",
                "path": "docs/engineering/verification-records/VREC-SIM-001.md",
            }
        )
        with mock.patch("se_harness.renumber._validator_report", return_value=report):
            code, output, error = self.invoke(
                "renumber-artifacts",
                str(self.root),
                "--map",
                "INT-SIM-001=INT-SIM-002",
                "--json",
                "--apply",
            )
        self.assertEqual(1, code, error)
        self.assertIn("commit-bound verification or release provenance", output)
        self.assertFalse((self.root / "docs/engineering/simulation/intent/INT-SIM-002.md").exists())
        self.assertEqual("", self._git("status", "--porcelain", "--untracked-files=all").stdout)

    def test_affected_hard_link_and_ignored_destination_are_rejected(self) -> None:
        source = self.root / "notes/references.md"
        linked = self.root / "notes/INT-SIM-001-hardlink.md"
        try:
            os.link(source, linked)
        except OSError as exc:
            self.skipTest(f"hard links are unavailable: {exc}")
        self._commit_all("add affected hard link")
        code, output, _ = self.invoke(
            "renumber-artifacts", str(self.root), "--map", "INT-SIM-001=INT-SIM-002", "--json"
        )
        self.assertEqual(1, code)
        self.assertIn("hard-linked files are unsupported", output)

        linked.unlink()
        ignored = self.root / ".gitignore"
        with ignored.open("a", encoding="utf-8") as handle:
            handle.write("\n*INT-SIM-002*\n")
        self._commit_all("ignore mapped destinations")
        code, output, _ = self.invoke(
            "renumber-artifacts", str(self.root), "--map", "INT-SIM-001=INT-SIM-002", "--json"
        )
        self.assertEqual(1, code)
        self.assertIn("hidden by Git ignore rules", output)

    def test_unfinished_recovery_state_is_reported_before_any_new_plan(self) -> None:
        recovery = self.root / ".harness-renumber-recovery-interrupted"
        recovery.mkdir()
        (recovery / "manifest.json").write_text("{}\n", encoding="utf-8")
        code, output, _ = self.invoke(
            "renumber-artifacts", str(self.root), "--map", "INT-SIM-001=INT-SIM-002", "--json"
        )
        self.assertEqual(1, code)
        blocker = json.loads(output)["blockers"][0]
        self.assertEqual("REN007", blocker["code"])
        self.assertIn("recovery state requires inspection", blocker["message"])

    def test_capacity_fixture_reports_250_evidence_files_and_500_occurrences(self) -> None:
        capacity = self.root / "docs/engineering/simulation/evidence/capacity"
        capacity.mkdir(parents=True)
        for index in range(250):
            (capacity / f"capture-{index:03d}.txt").write_text(
                "INT-SIM-001 then INT-SIM-001\n",
                encoding="utf-8",
            )
        self._commit_all("add capacity evidence")
        code, output, error = self.invoke(
            "renumber-artifacts",
            str(self.root),
            "--map",
            "INT-SIM-001=INT-SIM-002",
            "--json",
        )
        self.assertEqual(0, code, error)
        plan = json.loads(output)
        preserved = sum(
            item["occurrences"] for item in plan["preserved_evidence_references"]
        )
        self.assertEqual(501, preserved)
        self.assertEqual(251, len(plan["preserved_evidence_references"]))

    def test_mapping_normalization_rejects_duplicates_chains_and_cycles(self) -> None:
        self.assertEqual(
            ("INT-A-001", "INT-A-002"),
            (normalize_mappings(["INT-A-001=INT-A-002"])[0].old,
             normalize_mappings(["INT-A-001=INT-A-002"])[0].new),
        )
        for mappings in (
            ["INT-A-001=INT-A-002", "INT-A-001=INT-A-003"],
            ["INT-A-001=INT-A-003", "INT-A-002=INT-A-003"],
            ["INT-A-001=INT-A-002", "INT-A-002=INT-A-003"],
            ["INT-A-001=INT-A-002", "INT-A-002=INT-A-001"],
            ["INT-A-001=INT-X-INT-A-001-002"],
        ):
            with self.subTest(mappings=mappings), self.assertRaises(RenumberError):
                normalize_mappings(mappings)


if __name__ == "__main__":
    unittest.main()
