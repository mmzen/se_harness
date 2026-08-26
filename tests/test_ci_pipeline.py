"""Evidence for REQ-CIP-001 and REQ-CIP-002 (WO-CIP-001): trigger policy and one build per workflow."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = REPOSITORY_ROOT / ".github/workflows"
TEMPLATE_WORKFLOWS = REPOSITORY_ROOT / "templates/repository/standard/.github/workflows"

CANDIDATE_EVIDENCE_WORKFLOWS = {
    "candidate-evidence": WORKFLOWS / "candidate-evidence.yml",
    "governor-transition": WORKFLOWS / "predecessor-evaluator-assessment.yml",
    "engineering-harness": TEMPLATE_WORKFLOWS / "engineering-harness.yml",
}
PROTECTED_LINES = ("main", '"release/**"', '"candidate/**"')


def _job_blocks(workflow: str) -> dict[str, str]:
    """Split the `jobs:` mapping into {job_id: block text} without a YAML parser."""

    body = workflow.split("\njobs:\n", 1)[1]
    names = [(m.start(), m.group(1)) for m in re.finditer(r"(?m)^  ([a-z][a-z0-9-]*):$", body)]
    blocks = {}
    for index, (start, name) in enumerate(names):
        end = names[index + 1][0] if index + 1 < len(names) else len(body)
        blocks[name] = body[start:end]
    return blocks


class TriggerPolicyTests(unittest.TestCase):
    """REQ-CIP-001 / SPEC-CIP-001 CIP-TRG."""

    def test_each_candidate_evidence_workflow_runs_once_per_commit(self) -> None:
        for name, path in CANDIDATE_EVIDENCE_WORKFLOWS.items():
            with self.subTest(workflow=path.name):
                text = path.read_text(encoding="utf-8")
                head = text.split("\njobs:\n", 1)[0]
                self.assertIn("\non:\n  pull_request:\n  push:\n    branches:\n", head)
                push_block = head.split("  push:\n", 1)[1].split("\nconcurrency:", 1)[0]
                for line in PROTECTED_LINES:
                    self.assertIn(f"      - {line}\n", push_block, line)
                self.assertRegex(head, rf"(?m)^concurrency:\n  group: {name}-\$\{{\{{ github\.ref \}}\}}\n  cancel-in-progress: true$")
                # the header comment names the policy and the note that describes the workflow
                self.assertTrue(text.startswith("# "), "workflow header comment missing")
                self.assertIn("pull requests, and pushes to", text.split("\nname:", 1)[0])

    def test_release_workflows_do_not_cancel_in_progress(self) -> None:
        for filename in ("publish-pypi.yml", "release-candidate-replay.yml", "publish-dashboard-pages.yml"):
            with self.subTest(workflow=filename):
                text = (WORKFLOWS / filename).read_text(encoding="utf-8")
                self.assertIn("cancel-in-progress: false", text)

    def test_root_managed_copy_is_untouched(self) -> None:
        # The root engineering-harness.yml is a hash-locked 0.6.0 copy; WO-CIP-001
        # changes the standard template only. The root keeps the unfiltered
        # triggers until the governor upgrade replaces it.
        root = (WORKFLOWS / "engineering-harness.yml").read_text(encoding="utf-8")
        self.assertIn("\non:\n  pull_request:\n  push:\n\n", root)
        self.assertNotIn("concurrency:", root)


class OneBuildPerWorkflowTests(unittest.TestCase):
    """REQ-CIP-002 / SPEC-CIP-001 CIP-ART."""

    def setUp(self) -> None:
        self.text = CANDIDATE_EVIDENCE_WORKFLOWS["candidate-evidence"].read_text(encoding="utf-8")
        self.jobs = _job_blocks(self.text)

    def test_only_candidate_source_builds_and_every_consumer_verifies_the_handover(self) -> None:
        builders = [name for name, block in self.jobs.items() if "pip wheel" in block or "python -m build" in block]
        self.assertEqual(["candidate-source"], builders)
        source = self.jobs["candidate-source"]
        self.assertIn("sha256sum -- *.whl > SHA256SUMS", source)
        self.assertIn("name: candidate-wheel-non-promotable-${{ github.sha }}", source)
        for consumer, check in (
            ("candidate-package", "sha256sum --check --strict SHA256SUMS"),
            ("governance-migration", "Get-FileHash -Algorithm SHA256 -LiteralPath $wheel.FullName"),
        ):
            with self.subTest(job=consumer):
                block = self.jobs[consumer]
                self.assertIn("name: candidate-wheel-non-promotable-${{ github.sha }}", block)
                self.assertIn(check, block)
                self.assertNotIn("git archive", block)

    def test_integration_package_keeps_its_own_deterministic_double_build(self) -> None:
        # SPEC-IPK-001 rule 1: the integration package applies a local-version
        # overlay and builds twice for byte equality; those bytes are a different
        # distribution from the candidate wheel and are built by the script, not
        # by the workflow. Recorded as a deviation from CIP-ART in WO-CIP-001.
        block = self.jobs["integration-package-build"]
        self.assertIn("build_integration_package.py", block)
        self.assertNotIn("pip wheel", block)

    def test_reconcile_and_retain_only_jobs(self) -> None:
        self.assertNotIn("governance-migration-reconcile", self.jobs)
        migration = self.jobs["governance-migration"]
        self.assertIn("outputs:\n      Linux: ${{ steps.digest.outputs.Linux }}\n      Windows: ${{ steps.digest.outputs.Windows }}", migration)
        build = self.jobs["integration-package-build"]
        self.assertIn("Require one cross-platform migration semantic result", build)
        self.assertIn("MIGRATION_DIGEST_LINUX: ${{ needs.governance-migration.outputs.Linux }}", build)
        # SPEC-IPK-001 rule 5 keeps the retention job downstream of every matrix member
        self.assertIn("integration-package-retain", self.jobs)
        self.assertEqual(
            ["candidate-source", "candidate-package", "governance-migration",
             "integration-package-build", "integration-package-verify", "integration-package-retain"],
            list(self.jobs),
        )

    def test_the_double_rehearsal_per_platform_is_kept(self) -> None:
        # REQ-REB-017's acceptance example runs the rehearsal twice per platform.
        migration = self.jobs["governance-migration"]
        self.assertEqual(2, migration.count("-m se_harness rehearse-migration"))


if __name__ == "__main__":
    unittest.main()
