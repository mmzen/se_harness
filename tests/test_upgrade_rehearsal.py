"""WO-ECP-010: the real upgrade rehearsal (REQ-ECP-012, SPEC-ECP-007 ECP-PRD-008; issue #210)."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from dataclasses import dataclass, field
from pathlib import Path

from repository_tools import upgrade_rehearsal
from repository_tools.upgrade_rehearsal import Completed, UpgradeRehearsalError, canonical_sha256, rehearse
from tests.fixture_support import standard_repository

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PREDECESSOR = Path("/env/predecessor/bin/python")
SUCCESSOR = Path("/env/successor/bin/python")


def _git(root: Path, *arguments: str) -> None:
    subprocess.run(["git", *arguments], cwd=root, check=True, capture_output=True)


@dataclass
class FakeEvaluators:
    """Answer the evaluator invocations the rehearsal makes; run git for real.

    The successor's `upgrade --apply` rewrites the throwaway lock and retains the
    transaction evidence the way the installer does; every other answer is a
    knob so each assertion of the rehearsal can be exercised in isolation.
    """

    predecessor_version: str = "0.7.1"
    successor_version: str = "0.8.0"
    successor_payload: str = "b" * 64
    predecessor_doctor_before: int = 0
    predecessor_doctor_after: int = 1
    successor_doctor_after: int = 0
    validate_lines: list[str] = field(default_factory=list)
    lock_schema: int = 3
    lock_version: str | None = None
    lock_payload: str | None = None
    calls: list[list[str]] = field(default_factory=list)
    upgraded: bool = False

    def __call__(self, argv, cwd) -> Completed:
        argv = [str(item) for item in argv]
        self.calls.append(argv)
        if argv[0] == "git":
            completed = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, check=False)
            return Completed(completed.returncode, completed.stdout, completed.stderr)
        python = Path(argv[0])
        version = self.predecessor_version if python == PREDECESSOR else self.successor_version
        command = argv[4]
        if command == "--version":
            return Completed(0, version + "\n", "")
        copy = Path(argv[5])
        if command == "doctor":
            if python == PREDECESSOR:
                code = self.predecessor_doctor_after if self.upgraded else self.predecessor_doctor_before
            else:
                code = self.successor_doctor_after
            return Completed(code, "PASS lock\n" if code == 0 else "FAIL managed:x: changed\n", "")
        if command == "upgrade" and "--apply" not in argv:
            return Completed(0, "summary: 1 files, 0 unchanged\n", "")
        if command == "upgrade":
            self.upgraded = True
            lock_path = copy / ".engineering-harness.lock"
            lock = json.loads(lock_path.read_text(encoding="utf-8"))
            lock["schema"] = self.lock_schema
            lock["tool_version"] = self.lock_version or self.successor_version
            lock["evaluator"] = {
                "version": self.lock_version or self.successor_version,
                "payload_sha256": self.lock_payload or self.successor_payload,
                "archive_name": None,
                "archive_sha256": None,
            }
            lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
            evidence = copy / argv[argv.index("--evidence-output") + 1]
            evidence.parent.mkdir(parents=True, exist_ok=True)
            evidence.write_text(json.dumps({"target": {"version": self.successor_version, "payload_sha256": self.successor_payload}}), encoding="utf-8")
            return Completed(0, "upgraded managed files\n", "")
        if command == "validate":
            errors = [line for line in self.validate_lines if line.startswith("- [E")]
            body = "\n".join([*self.validate_lines, f"Artifacts: 10 | Errors: {len(errors)} | Warnings: 0"]) + "\n"
            return Completed(1 if errors else 0, body, "")
        raise AssertionError(f"unexpected evaluator invocation: {argv}")


@unittest.skipUnless(shutil.which("git"), "git is unavailable")
class UpgradeRehearsalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        base = Path(self.temporary.name)
        self.repository = base / "repository"
        standard_repository(self.repository, "Rehearsal Fixture")
        lock_path = self.repository / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["evaluator"]["version"] = "0.7.1"
        lock["tool_version"] = "0.7.1"
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        _git(self.repository, "init", "-q", "-b", "main")
        _git(self.repository, "config", "user.email", "t@example.invalid")
        _git(self.repository, "config", "user.name", "t")
        _git(self.repository, "config", "commit.gpgsign", "false")
        _git(self.repository, "add", "-A")
        _git(self.repository, "commit", "-q", "-m", "fixture")
        self.output = base / "out"
        self.workspace = base / "work"
        self.workspace.mkdir()

    def run_rehearsal(self, fake: FakeEvaluators) -> dict:
        return rehearse(
            self.repository, predecessor_python=PREDECESSOR, successor_python=SUCCESSOR,
            output=self.output, runner=fake, workspace=self.workspace,
        )

    def test_the_real_handover_passes_and_binds_the_resulting_lock(self) -> None:
        fake = FakeEvaluators(validate_lines=["- [E012] [governance] docs/engineering/x/verification-records/VREC-X-001.md: evaluator evidence differs from the standard lock"])
        result = self.run_rehearsal(fake)
        self.assertEqual("pass", result["overall_result"], result["failure"])
        self.assertEqual([("predecessor-doctor-before", "pass"), ("successor-upgrade-plan", "pass"), ("successor-upgrade-apply", "pass"),
                          ("successor-doctor-after", "pass"), ("successor-validate-after", "pass"), ("predecessor-doctor-after", "pass")],
                         [(step["id"], step["outcome"]) for step in result["steps"]])
        self.assertEqual(3, result["lock"]["schema"])
        self.assertEqual({"version": "0.8.0", "payload_sha256": "b" * 64}, result["lock"]["evaluator"])
        self.assertEqual(result["lock"]["canonical_sha256"], result["semantic_sha256"])
        self.assertEqual(1, len(result["tolerated_diagnostics"]))
        written = json.loads((self.output / "upgrade-rehearsal-result.json").read_text(encoding="utf-8"))
        self.assertEqual(result, written)
        # The operational repository is untouched: its lock still names the predecessor.
        self.assertEqual("0.7.1", json.loads((self.repository / ".engineering-harness.lock").read_text(encoding="utf-8"))["evaluator"]["version"])
        self.assertEqual("", subprocess.run(["git", "status", "--porcelain"], cwd=self.repository, capture_output=True, text=True).stdout)
        # Every evaluator ran with -I from its own environment.
        self.assertTrue(all(argv[1:4] == ["-I", "-m", "se_harness"] for argv in fake.calls if argv[0] != "git"))

    def test_the_predecessor_must_own_the_root_before_the_upgrade(self) -> None:
        result = self.run_rehearsal(FakeEvaluators(predecessor_doctor_before=1))
        self.assertEqual("fail", result["overall_result"])
        self.assertTrue(result["failure"].startswith("predecessor-doctor-before"), result["failure"])
        self.assertEqual(["predecessor-doctor-before"], [step["id"] for step in result["steps"]])

    def test_the_predecessor_must_stop_owning_the_root_after_the_upgrade(self) -> None:
        result = self.run_rehearsal(FakeEvaluators(predecessor_doctor_after=0))
        self.assertEqual("fail", result["overall_result"])
        self.assertTrue(result["failure"].startswith("predecessor-doctor-after: expected failure"), result["failure"])

    def test_the_successor_doctor_must_pass_after_the_upgrade(self) -> None:
        result = self.run_rehearsal(FakeEvaluators(successor_doctor_after=1))
        self.assertTrue(result["failure"].startswith("successor-doctor-after"), result["failure"])

    def test_only_e012_on_a_ready_record_is_tolerated(self) -> None:
        result = self.run_rehearsal(FakeEvaluators(validate_lines=["- [E010] [governance] docs/engineering/x/work-orders/WO-X-001.md: verified work order requires coverage"]))
        self.assertEqual("fail", result["overall_result"])
        self.assertIn("beyond E012", result["failure"])
        self.assertIn("E010", result["failure"])

    def test_the_lock_must_end_at_schema_three_naming_the_successor(self) -> None:
        for knob, expected in (
            ({"lock_schema": 2}, "schema 2"),
            ({"lock_version": "0.7.1"}, "not the successor 0.8.0"),
            ({"lock_payload": "c" * 64}, "installed-payload digest"),
        ):
            with self.subTest(knob=knob):
                shutil.rmtree(self.output, ignore_errors=True)
                result = self.run_rehearsal(FakeEvaluators(**knob))
                self.assertEqual("fail", result["overall_result"])
                self.assertIn(expected, result["failure"])

    def test_same_version_is_no_handover(self) -> None:
        result = self.run_rehearsal(FakeEvaluators(successor_version="0.7.1"))
        self.assertIn("no handover to rehearse", result["failure"])

    def test_the_exported_lock_must_belong_to_the_predecessor(self) -> None:
        result = self.run_rehearsal(FakeEvaluators(predecessor_version="0.6.0", successor_version="0.8.0"))
        self.assertIn("not the predecessor 0.6.0", result["failure"])

    def test_the_output_must_lie_outside_the_repository_and_be_empty(self) -> None:
        with self.assertRaisesRegex(UpgradeRehearsalError, "outside the operational repository"):
            rehearse(self.repository, predecessor_python=PREDECESSOR, successor_python=SUCCESSOR, output=self.repository / "out", runner=FakeEvaluators())
        self.output.mkdir()
        (self.output / "stale").write_text("x", encoding="utf-8")
        with self.assertRaisesRegex(UpgradeRehearsalError, "not empty"):
            rehearse(self.repository, predecessor_python=PREDECESSOR, successor_python=SUCCESSOR, output=self.output, runner=FakeEvaluators())

    def test_the_export_is_the_committed_tree_not_the_working_tree(self) -> None:
        (self.repository / "docs/engineering/README.md").write_text("uncommitted\n", encoding="utf-8")
        seen: list[bytes] = []

        class Peek(FakeEvaluators):
            def __call__(self, argv, cwd):
                if argv[4:5] == ["doctor"] and Path(argv[0]) == PREDECESSOR and not seen:
                    seen.append((Path(argv[5]) / "docs/engineering/README.md").read_bytes())
                return super().__call__(argv, cwd)

        self.run_rehearsal(Peek())
        self.assertNotEqual(b"uncommitted\n", seen[0])

    def test_canonical_digest_ignores_newline_form(self) -> None:
        self.assertEqual(canonical_sha256(b'{"a": 1}\n'), canonical_sha256(b'{"a": 1}\r\n'))
        self.assertEqual(hashlib.sha256(b'{"a": 1}\n').hexdigest(), canonical_sha256(b'{"a": 1}\r\n'))

    def test_credential_variables_never_reach_the_evaluators(self) -> None:
        with unittest.mock.patch.dict(os.environ, {"GITHUB_TOKEN": "x", "PYTHONPATH": "/elsewhere", "AWS_SECRET_ACCESS_KEY": "y"}):
            environment = upgrade_rehearsal._environment()
        for name in ("GITHUB_TOKEN", "PYTHONPATH", "AWS_SECRET_ACCESS_KEY"):
            self.assertNotIn(name, environment)
        self.assertEqual("1", environment["PYTHONNOUSERSITE"])


class RetiredSurfaceTests(unittest.TestCase):
    """Issue #210 acceptance criteria 2 and 3, and the reserved names."""

    #: The stage machine's files, retained dead until the root evaluator advances
    #: past 0.7.1, whose hash-bound class requires a tracked file per pattern
    #: (WO-ECP-010 evidence, section 6). The follow-up that deletes them removes
    #: this set and the exemption below.
    RETAINED_UNTIL_ROOT_ADVANCES = (
        "se_harness/governance_migration.py",
        "se_harness/governance_migration_contract.py",
        "se_harness/governance_migration_contract.json",
        "tests/fixtures/governance_migration/synthetic-n-minus-1-to-n.json",
    )

    def test_no_json_under_se_harness_embeds_a_digest_of_a_python_module(self) -> None:
        digests = {hashlib.sha256(path.read_bytes()).hexdigest() for path in (REPOSITORY_ROOT / "se_harness").rglob("*.py")}
        exempt = {Path(item).name for item in self.RETAINED_UNTIL_ROOT_ADVANCES if item.endswith(".json")}
        for path in sorted((REPOSITORY_ROOT / "se_harness").glob("*.json")):
            if path.name in exempt:
                continue
            with self.subTest(contract=path.name):
                values = re.findall(r"[0-9a-f]{64}", path.read_text(encoding="utf-8"))
                self.assertEqual([], [value for value in values if value in digests])

    def test_the_stage_machine_is_retired_dead_and_its_names_are_reserved(self) -> None:
        for relative in ("tests/test_governance_migration.py", "repository_tools/predecessor_facts.py",
                         "tests/fixtures/governance_migration/candidate-0.7.1-to-0.8.0.json"):
            self.assertFalse((REPOSITORY_ROOT / relative).exists(), relative)
        for relative in self.RETAINED_UNTIL_ROOT_ADVANCES:
            self.assertTrue((REPOSITORY_ROOT / relative).exists(), relative)
        retained = {Path(item).name for item in self.RETAINED_UNTIL_ROOT_ADVANCES}
        for relative in sorted((REPOSITORY_ROOT / "se_harness").rglob("*.py")):
            if relative.name in retained:
                continue
            text = relative.read_text(encoding="utf-8")
            self.assertNotIn("rehearse-migration", text, relative.name)
            self.assertNotIn("governance_migration", text, relative.name)
            self.assertIsNone(re.search(r"\bMIG[0-9]{3}\b", text), relative.name)
        surface = (REPOSITORY_ROOT / "scripts/check_portable_release_surface.py").read_text(encoding="utf-8")
        self.assertIn('b"rehearse-migration"', surface)
        self.assertIn("RETIRED_MIGRATION_MEMBERS", surface)
        workflows = " ".join(path.read_text(encoding="utf-8") for path in (REPOSITORY_ROOT / ".github/workflows").glob("*.yml"))
        self.assertNotIn("rehearse-migration", workflows)

    def test_the_retained_owner_rules_say_why_they_stay(self) -> None:
        attributes = (REPOSITORY_ROOT / ".gitattributes").read_text(encoding="utf-8")
        owner = attributes.split("# se-harness:end\n", 1)[1]
        self.assertIn("se_harness/governance_migration*.py text eol=lf", owner)
        self.assertIn("WO-ECP-010", owner)

    def test_the_lane_runs_the_rehearsal_twice_per_platform_and_compares_across(self) -> None:
        workflow = (REPOSITORY_ROOT / ".github/workflows/candidate-evidence.yml").read_text(encoding="utf-8")
        self.assertEqual(2, workflow.count("python -m repository_tools.upgrade_rehearsal --repository ."))
        self.assertIn("windows-latest", workflow)
        self.assertIn("if ($firstResult.semantic_sha256 -ne $secondResult.semantic_sha256)", workflow)
        self.assertIn("cross-platform semantic mismatch", workflow)
        self.assertNotIn("rehearse-migration", workflow)
        self.assertNotIn("scenario", workflow.lower())
