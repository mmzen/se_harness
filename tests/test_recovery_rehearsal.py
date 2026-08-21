from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from se_harness.cli import main
from se_harness.recovery_rehearsal import RecoveryRehearsalError, run_recovery_rehearsal


class RecoveryRehearsalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary.name)
        self.repository = self.base / "operational-repository"
        self.repository.mkdir()
        (self.repository / "preserved.txt").write_text("operational bytes\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_rehearsal_is_deterministic_disposable_and_rolls_back_interruption(self) -> None:
        before = (self.repository / "preserved.txt").read_bytes()
        first = run_recovery_rehearsal(
            self.base / "first",
            operational_repository=self.repository,
            candidate_commit="a" * 40,
            target_version="999.0.0",
            environment={},
        )
        second = run_recovery_rehearsal(
            self.base / "second",
            operational_repository=self.repository,
            candidate_commit="a" * 40,
            target_version="999.0.0",
            environment={},
        )
        self.assertEqual(first, second)
        self.assertEqual("pass", first["result"])
        self.assertTrue(first["restoration"]["rollback_exact"])
        self.assertTrue(first["restoration"]["absence_invariants"])
        self.assertTrue(all(value is False for value in first["external_actions"].values()))
        self.assertEqual(
            {"candidate-contamination", "stale-or-mismatched-identity", "conflicting-chains"},
            {item["case"] for item in first["negative_cases"]},
        )
        conflict = next(item for item in first["negative_cases"] if item["case"] == "conflicting-chains")
        self.assertIs(False, conflict["automatic"])
        self.assertEqual(before, (self.repository / "preserved.txt").read_bytes())
        retained = json.loads((self.base / "first" / "rehearsal-report.json").read_bytes())
        self.assertEqual(first, retained)

    def test_rehearsal_rejects_mutable_selection_credentials_and_operational_output(self) -> None:
        cases = (
            ({"candidate_commit": "main", "environment": {}}, "full immutable commit"),
            ({"candidate_commit": "b" * 40, "environment": {"PYPI_API_TOKEN": "secret"}}, "credential signals"),
        )
        for index, (overrides, message) in enumerate(cases):
            with self.subTest(message=message), self.assertRaisesRegex(RecoveryRehearsalError, message):
                run_recovery_rehearsal(
                    self.base / f"rejected-{index}",
                    operational_repository=self.repository,
                    candidate_commit=overrides["candidate_commit"],
                    target_version="999.0.0",
                    environment=overrides["environment"],
                )
        with self.assertRaisesRegex(RecoveryRehearsalError, "outside the operational repository"):
            run_recovery_rehearsal(
                self.repository / "target" / "rehearsal",
                operational_repository=self.repository,
                candidate_commit="b" * 40,
                target_version="999.0.0",
                environment={},
            )
        occupied_file = self.base / "occupied-file"
        occupied_file.write_text("not a directory\n", encoding="utf-8")
        with self.assertRaisesRegex(RecoveryRehearsalError, "absent or empty"):
            run_recovery_rehearsal(
                occupied_file,
                operational_repository=self.repository,
                candidate_commit="b" * 40,
                target_version="999.0.0",
                environment={},
            )

    def test_cli_retains_report_and_converts_boundary_failures(self) -> None:
        output = io.StringIO()
        error = io.StringIO()
        with mock.patch("se_harness.recovery_rehearsal.os.environ", {}), contextlib.redirect_stdout(
            output
        ), contextlib.redirect_stderr(error):
            code = main(
                [
                    "rehearse-recovery",
                    str(self.base / "cli"),
                    "--repository",
                    str(self.repository),
                    "--candidate-commit",
                    "c" * 40,
                ]
            )
        self.assertEqual(0, code, error.getvalue())
        self.assertIn("PASS", output.getvalue())

        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(error):
            code = main(
                [
                    "rehearse-recovery",
                    str(self.base / "rejected-cli"),
                    "--repository",
                    str(self.repository),
                    "--candidate-commit",
                    "main",
                ]
            )
        self.assertEqual(2, code)
        self.assertIn("full immutable commit", error.getvalue())


if __name__ == "__main__":
    unittest.main()
