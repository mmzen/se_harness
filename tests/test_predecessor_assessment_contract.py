from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from se_harness.installer import tracked_content
from se_harness.integrity import canonical_sha256


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = REPOSITORY_ROOT / ".github" / "workflows" / "predecessor-evaluator-assessment.yml"
MANAGED_WORKFLOW = REPOSITORY_ROOT / ".github" / "workflows" / "engineering-harness.yml"


class GovernorTransitionAssessmentContractTests(unittest.TestCase):
    def test_candidate_owned_workflow_is_generic_read_only_and_credential_free(self) -> None:
        content = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("permissions:\n  contents: read", content)
        self.assertIn("fetch-depth: 0", content)
        self.assertIn("persist-credentials: false", content)
        self.assertNotIn("continue-on-error", content)
        self.assertNotIn("id-token: write", content)
        self.assertIn("actions/checkout@v4", content)
        self.assertIn("actions/setup-python@v5", content)
        self.assertIn("actions/upload-artifact@v4", content)
        self.assertEqual(2, content.count("if: always()"))
        self.assertIn("name: Governor Transition Assessment", content)
        self.assertIn("scripts/validate_governor_transition.py plan", content)
        self.assertIn("scripts/validate_governor_transition.py assess", content)
        self.assertIn("qualify released-root \"$GITHUB_WORKSPACE\"", content)
        self.assertIn("target-released-root-qualification.json", content)
        self.assertIn("github.event.pull_request.base.sha || github.event.before", content)
        self.assertIn("refs/remotes/origin/$DEFAULT_BRANCH", content)
        self.assertIn('"se-harness==$TARGET_VERSION"', content)
        self.assertIn("target_archive_sha256", content)
        self.assertIn("git diff --exit-code", content)
        self.assertIn("git status --porcelain=v1 --untracked-files=all", content)
        for forbidden in (
            "0.5.0",
            "0.6.0",
            "RLS-SEH-",
            "validate_predecessor_publication_view.py",
            "--omit",
            "--expected-error",
            "git push",
            "harnessctl transition",
        ):
            self.assertNotIn(forbidden, content)

        download = content.index('"se-harness==$TARGET_VERSION"')
        archive_check = content.index("hashlib.sha256(wheel.read_bytes())")
        install = content.index('python -m venv "$RUNNER_TEMP/target-evaluator"')
        self.assertLess(download, archive_check)
        self.assertLess(archive_check, install)

    def test_existing_managed_workflow_matches_the_selected_released_lock(self) -> None:
        lock = json.loads(
            (REPOSITORY_ROOT / ".engineering-harness.lock").read_text(encoding="utf-8")
        )
        raw = MANAGED_WORKFLOW.read_bytes()
        self.assertEqual(
            lock["files"][".github/workflows/engineering-harness.yml"]["sha256"],
            canonical_sha256(tracked_content("managed", raw)),
        )

    def test_transition_cli_reports_boundary_failures_as_closed_json(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                "-S",
                str(REPOSITORY_ROOT / "scripts" / "validate_governor_transition.py"),
                "plan",
                "--repository",
                str(REPOSITORY_ROOT / "missing-assessment-repository"),
                "--base-revision",
                "a" * 40,
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
        self.assertIn('"passed":false', completed.stdout)
        self.assertIn('"applied":false', completed.stdout)


if __name__ == "__main__":
    unittest.main()
