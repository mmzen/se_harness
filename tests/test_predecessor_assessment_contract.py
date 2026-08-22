from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = REPOSITORY_ROOT / ".github" / "workflows" / "predecessor-evaluator-assessment.yml"
MANAGED_WORKFLOW = REPOSITORY_ROOT / ".github" / "workflows" / "engineering-harness.yml"


class PredecessorAssessmentContractTests(unittest.TestCase):
    def test_candidate_owned_workflow_is_read_only_fixed_and_credential_free(self) -> None:
        content = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("permissions:\n  contents: read", content)
        self.assertIn("persist-credentials: false", content)
        self.assertNotIn("continue-on-error", content)
        self.assertNotIn("id-token: write", content)
        self.assertIn("actions/checkout@v4", content)
        self.assertIn("actions/setup-python@v5", content)
        self.assertIn("actions/upload-artifact@v4", content)
        self.assertIn('SE_HARNESS_VERSION: "0.5.0"', content)
        self.assertIn(
            'SE_HARNESS_WHEEL_SHA256: "974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f"',
            content,
        )
        self.assertIn("--candidate-commit \"$GITHUB_SHA\"", content)
        self.assertIn("--release-contract REL-SEH-010", content)
        self.assertIn("--output \"$RUNNER_TEMP/predecessor-assessment.json\"", content)
        self.assertIn("git diff --exit-code", content)
        self.assertIn("git status --porcelain=v1 --untracked-files=all", content)
        for forbidden in ("--omit", "--expected-error", "git push", "harnessctl transition"):
            self.assertNotIn(forbidden, content)

    def test_existing_managed_workflow_remains_byte_identical_to_head(self) -> None:
        committed = subprocess.run(
            [
                "git",
                "-c",
                "safe.directory=*",
                "-C",
                str(REPOSITORY_ROOT),
                "show",
                "HEAD:.github/workflows/engineering-harness.yml",
            ],
            check=True,
            capture_output=True,
        ).stdout
        self.assertEqual(
            committed.decode("utf-8"),
            MANAGED_WORKFLOW.read_text(encoding="utf-8").replace("\r\n", "\n"),
        )

    def test_cli_reports_shared_boundary_failures_as_closed_json(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                "-S",
                str(REPOSITORY_ROOT / "scripts" / "assess_predecessor_evaluator.py"),
                "--repository",
                str(REPOSITORY_ROOT / "missing-assessment-repository"),
                "--candidate-commit",
                "0" * 40,
                "--release-contract",
                "REL-SEH-010",
                "--evaluator-python",
                "missing-python",
                "--evaluator-entry-point",
                "missing-entry-point",
                "--evaluator-wheel",
                "missing-wheel",
                "--json",
            ],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(1, completed.returncode)
        self.assertEqual("", completed.stderr)
        self.assertIn('"passed": false', completed.stdout)
        self.assertIn('"applied": false', completed.stdout)


if __name__ == "__main__":
    unittest.main()
