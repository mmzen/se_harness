"""Evidence for REQ-CIP-001, REQ-CIP-002 (WO-CIP-001) and REQ-CIP-006 (WO-CIP-003)."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
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


class PredecessorDerivationTests(unittest.TestCase):
    """REQ-CIP-006 / SPEC-CIP-001 CIP-PRE."""

    REPOSITORY_OWNED = (WORKFLOWS / "candidate-evidence.yml", WORKFLOWS / "predecessor-evaluator-assessment.yml")

    def test_facts_come_from_the_lock_and_the_legacy_table(self) -> None:
        from repository_tools.predecessor_facts import LEGACY_ACCEPTANCE_CONTRACT_SHA256, derive

        lock = json.loads((REPOSITORY_ROOT / ".engineering-harness.lock").read_bytes())["evaluator"]
        facts = derive(REPOSITORY_ROOT)
        self.assertEqual(lock["version"], facts.version)
        self.assertEqual(lock["archive_name"], facts.wheel)
        self.assertEqual(lock["archive_sha256"], facts.wheel_sha256)
        self.assertEqual(lock["payload_sha256"], facts.payload_sha256)
        self.assertEqual(LEGACY_ACCEPTANCE_CONTRACT_SHA256[facts.version], facts.acceptance_contract_sha256)
        self.assertEqual(f"tests/fixtures/governance_migration/candidate-{facts.version}-to-{facts.candidate_version}.json", facts.scenario)
        self.assertTrue((REPOSITORY_ROOT / facts.scenario).is_file())
        lines = facts.github_output_lines().splitlines()
        self.assertIn(f"wheel_sha256={facts.wheel_sha256}", lines)
        self.assertIn(f"scenario={facts.scenario}", lines)

    def test_no_predecessor_literal_remains_in_the_repository_owned_workflows(self) -> None:
        for path in self.REPOSITORY_OWNED:
            with self.subTest(workflow=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertIsNone(re.search(r"[0-9a-f]{64}", text.replace("actions/", "")), "a digest literal remains")
                # version literals: the pinned build tools are not evaluator facts
                versions = {m.group(0) for m in re.finditer(r"\b\d+\.\d+\.\d+(?:\.post\d+)?\b", text)}
                self.assertEqual(set(), {v for v in versions if v in {"0.6.0", "0.7.0"}}, versions)

    def test_workflow_derives_once_and_consumers_take_the_outputs(self) -> None:
        text = (WORKFLOWS / "candidate-evidence.yml").read_text(encoding="utf-8")
        jobs = _job_blocks(text)
        self.assertEqual(1, text.count("repository_tools.predecessor_facts derive"))
        self.assertIn("repository_tools.predecessor_facts derive", jobs["candidate-source"])
        for output in ("predecessor_version", "predecessor_wheel_sha256", "migration_scenario"):
            self.assertIn(f"{output}: ${{{{ steps.predecessor.outputs.", jobs["candidate-source"])
        self.assertIn("needs.candidate-source.outputs.predecessor_acceptance_contract_sha256", jobs["candidate-package"])
        self.assertIn("needs.candidate-source.outputs.migration_scenario_sha256", jobs["governance-migration"])
        self.assertIn("throw 'predecessor facts were not derived by candidate-source'", jobs["governance-migration"])

    def _copy_repository_declarations(self, root: Path) -> None:
        for relative in (".engineering-harness.toml", ".engineering-harness.lock", "pyproject.toml"):
            shutil.copy(REPOSITORY_ROOT / relative, root / relative)
        (root / "tests/fixtures/governance_migration").mkdir(parents=True)
        for scenario in (REPOSITORY_ROOT / "tests/fixtures/governance_migration").glob("*.json"):
            shutil.copy(scenario, root / "tests/fixtures/governance_migration" / scenario.name)

    def test_version_bump_without_a_scenario_fails_closed_naming_the_path(self) -> None:
        from repository_tools.predecessor_facts import PredecessorFactsError, derive

        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            self._copy_repository_declarations(root)
            pyproject = root / "pyproject.toml"
            pyproject.write_text(pyproject.read_text(encoding="utf-8").replace('version = "0.7.0"', 'version = "0.8.0"', 1), encoding="utf-8")
            with self.assertRaises(PredecessorFactsError) as caught:
                derive(root)
            self.assertIn("PRE009", str(caught.exception))
            self.assertIn("tests/fixtures/governance_migration/candidate-0.6.0-to-0.8.0.json", str(caught.exception))
            completed = subprocess.run(
                [sys.executable, "-m", "repository_tools.predecessor_facts", "derive", "--repository", str(root)],
                capture_output=True, text=True, cwd=REPOSITORY_ROOT,
            )
            self.assertEqual(2, completed.returncode)
            self.assertIn("PRE009", completed.stderr)

    def test_disagreeing_root_declarations_fail_closed(self) -> None:
        from repository_tools.predecessor_facts import PredecessorFactsError, derive

        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            self._copy_repository_declarations(root)
            toml = root / ".engineering-harness.toml"
            toml.write_text(toml.read_text(encoding="utf-8").replace('tool_version = "0.6.0"', 'tool_version = "0.5.0"'), encoding="utf-8")
            with self.assertRaises(PredecessorFactsError) as caught:
                derive(root)
            self.assertIn("PRE007", str(caught.exception))

    def test_module_is_standard_library_only_and_its_writer_equals_the_contract_module(self) -> None:
        # repository_tools may not widen its pinned import crossing into se_harness
        # (tests/test_interpreter_safety.py); the writer is restated and proven equal.
        from repository_tools import predecessor_facts
        from se_harness import governance_migration_contract as contract

        source = (REPOSITORY_ROOT / "repository_tools/predecessor_facts.py").read_text(encoding="utf-8")
        self.assertNotIn("se_harness", [line.split()[1] for line in source.splitlines() if line.startswith(("import ", "from "))])
        for scenario in (REPOSITORY_ROOT / "tests/fixtures/governance_migration").glob("*.json"):
            with self.subTest(scenario=scenario.name):
                loaded, raw = predecessor_facts.load_scenario(scenario)
                self.assertEqual(contract.canonical_json(loaded), predecessor_facts.canonical_json(loaded))
                self.assertEqual(raw, predecessor_facts.canonical_json(loaded))
                self.assertEqual(contract.sha256_bytes(raw), predecessor_facts.sha256_bytes(raw))
                contract.load_migration_scenario(scenario, contract.load_migration_contract())

    def test_writer_reproduces_the_committed_scenario_and_writes_the_next_pair(self) -> None:
        from repository_tools.predecessor_facts import derive, write_scenario
        from se_harness.governance_migration_contract import load_migration_contract, load_migration_scenario

        facts = derive(REPOSITORY_ROOT)
        committed = REPOSITORY_ROOT / facts.scenario
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            self._copy_repository_declarations(root)
            destination, raw = write_scenario(root, template=committed, predecessor=None, successor=None, output=root / "same.json")
            self.assertEqual(committed.read_bytes(), raw, "the writer must reproduce the committed pair byte for byte")
            destination, raw = write_scenario(root, template=committed, predecessor=None, successor="0.8.0", output=None)
            self.assertEqual(root / "tests/fixtures/governance_migration/candidate-0.6.0-to-0.8.0.json", destination)
            scenario, _ = load_migration_scenario(destination, load_migration_contract())
            self.assertEqual({"predecessor": "0.6.0", "successor": "0.8.0"}, scenario["versions"])
            self.assertEqual("0.8.0", scenario["fixture"]["replacement_proposal"]["version"])
            self.assertEqual(facts.wheel_sha256, scenario["runtime_expectations"]["predecessor"]["archive_sha256"])
            pyproject = root / "pyproject.toml"
            pyproject.write_text(pyproject.read_text(encoding="utf-8").replace('version = "0.7.0"', 'version = "0.8.0"', 1), encoding="utf-8")
            self.assertEqual("tests/fixtures/governance_migration/candidate-0.6.0-to-0.8.0.json", derive(root).scenario)


if __name__ == "__main__":
    unittest.main()
