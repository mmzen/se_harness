"""WO-ECP-010: the real upgrade rehearsal (REQ-ECP-012, SPEC-ECP-007 ECP-PRD-008; issue #210)."""

from __future__ import annotations

import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
import unittest.mock
from dataclasses import dataclass, field
from contextlib import redirect_stderr
from pathlib import Path

from repository_tools import upgrade_rehearsal
from repository_tools.upgrade_rehearsal import Completed, UpgradeRehearsalError, canonical_sha256, rehearse
from tests.fixture_support import standard_repository
from tests.git_support import git

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PREDECESSOR = Path("/env/predecessor/bin/python")
SUCCESSOR = Path("/env/successor/bin/python")


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
    four_number_summary: bool = False
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
            # WO-AUT-004: a 0.12.0 validator prints a fourth number; an older one does not.
            summary = f"Artifacts: 10 | Errors: {len(errors)} | Warnings: 0"
            if self.four_number_summary:
                summary += " | Advisories: 0"
            body = "\n".join([*self.validate_lines, summary]) + "\n"
            return Completed(1 if errors else 0, body, "")
        raise AssertionError(f"unexpected evaluator invocation: {argv}")


@unittest.skipUnless(shutil.which("git"), "git is unavailable")
class UpgradeRehearsalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        base = Path(self.temporary.name)
        self.repository = base / "repository"
        standard_repository(self.repository)
        lock_path = self.repository / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["evaluator"]["version"] = "0.7.1"
        lock["tool_version"] = "0.7.1"
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        git(self.repository, "init", "-q", "-b", "main")
        git(self.repository, "config", "user.email", "t@example.invalid")
        git(self.repository, "config", "user.name", "t")
        git(self.repository, "config", "commit.gpgsign", "false")
        git(self.repository, "add", "-A")
        git(self.repository, "commit", "-q", "-m", "fixture")
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
        self.assertEqual("", git(self.repository, "status", "--porcelain"))
        # Every evaluator ran with -I from its own environment.
        self.assertTrue(all(argv[1:4] == ["-I", "-m", "se_harness"] for argv in fake.calls if argv[0] != "git"))

    def test_a_four_number_validate_summary_is_read_as_a_summary(self) -> None:
        # WO-AUT-004 (SPEC-AUT-002 AUT-ADV-003): a 0.12.0 successor prints `| Advisories: N`
        # after the warnings; the rehearsal must still find the summary line.
        result = self.run_rehearsal(FakeEvaluators(four_number_summary=True))
        self.assertEqual("pass", result["overall_result"], result["failure"])
        self.assertIn(("successor-validate-after", "pass"), [(step["id"], step["outcome"]) for step in result["steps"]])

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

    def test_timing_preserves_commands_results_and_success_and_failure_verdicts(self) -> None:
        cases = (
            {"validate_lines": ["- [E012] [governance] VREC-X-001: evaluator evidence differs from the standard lock"]},
            {"predecessor_doctor_before": 1},
            {"predecessor_doctor_after": 0},
            {"validate_lines": ["- [E010] invalid record"]},
        )
        for index, knobs in enumerate(cases):
            with self.subTest(knobs=knobs), redirect_stderr(io.StringIO()):
                runs = []
                calls = []
                for enabled in (False, True):
                    fake = FakeEvaluators(**knobs)
                    output = self.output.with_name(f"out-{index}-{enabled}")
                    runs.append(rehearse(self.repository, predecessor_python=PREDECESSOR, successor_python=SUCCESSOR,
                                        output=output, runner=fake, workspace=self.workspace, timings=enabled))
                    calls.append([tuple(re.sub(r"upgrade-rehearsal-[^/\\]+", "upgrade-rehearsal-copy", item)
                                        for item in argv) for argv in fake.calls if argv[:2] != ["git", "rev-parse"]])
                    path_queries = [argv for argv in fake.calls if argv[:2] == ["git", "rev-parse"]]
                    self.assertEqual(1 if enabled else 0, len(path_queries))
                    self.assertEqual(enabled, (output / upgrade_rehearsal.TIMING_NAME).exists())
                    if enabled:
                        timing = json.loads((output / upgrade_rehearsal.TIMING_NAME).read_text())
                        self.assertTrue(timing["complete"])
                        self.assertEqual(runs[-1]["overall_result"], timing["stages"][0]["handover_result"])
                        self.assertEqual([], timing["diagnostic_errors"])
                        self.assertGreaterEqual(timing["unaccounted_seconds"], 0)
                        stages = {stage["id"]: stage for stage in timing["stages"]}
                        self.assertIn("git-add", stages)
                        self.assertIn("git-commit", stages)
                        self.assertIn("scratch-cleanup", stages)
                        self.assertGreater(stages["archive-extraction"]["files"], 0)
                        if "predecessor-doctor-after" in stages:
                            self.assertEqual(fake.predecessor_doctor_after, stages["predecessor-doctor-after"]["exit_code"])
                self.assertEqual(runs[0], runs[1])
                self.assertEqual(calls[0], calls[1])

    def test_default_and_explicit_workspace_report_actual_storage_and_cleanup(self) -> None:
        default = self.workspace / "default temp"
        explicit = self.workspace / "selected temp"
        default.mkdir()
        explicit.mkdir()
        results = []
        for workspace, expected in ((None, default), (explicit, explicit)):
            output = self.output.with_name(expected.name)
            with unittest.mock.patch.object(upgrade_rehearsal.tempfile, "gettempdir", return_value=str(default)), redirect_stderr(io.StringIO()):
                results.append(rehearse(self.repository, predecessor_python=PREDECESSOR, successor_python=SUCCESSOR,
                                       output=output, runner=FakeEvaluators(), workspace=workspace, timings=True))
            timing = json.loads((output / upgrade_rehearsal.TIMING_NAME).read_text())
            storage = timing["storage"]
            self.assertEqual("python-default" if workspace is None else "explicit", storage["selection"])
            self.assertEqual(default.resolve(), Path(storage["python_default_temp"]))
            self.assertEqual(expected.resolve(), Path(storage["workspace_root"]))
            scratch = Path(storage["scratch_directory"])
            copy = Path(storage["repository_directory"])
            self.assertEqual(expected.resolve(), scratch.parent)
            self.assertEqual(scratch / "repository", copy)
            self.assertEqual(copy / ".git", Path(storage["git_directory"]))
            self.assertEqual(copy / ".git/index", Path(storage["index_file"]))
            self.assertEqual(copy / ".git/objects", Path(storage["object_directory"]))
            self.assertEqual({"TMPDIR", "TEMP", "TMP", "RUNNER_TEMP"}, set(storage["temp_environment"]))
            self.assertFalse(scratch.exists())
            self.assertEqual([], list(expected.iterdir()))
        self.assertEqual(results[0], results[1])
        self.assertEqual("", git(self.repository, "status", "--porcelain"))

    def test_invalid_workspace_is_rejected_before_output_or_scratch_writes(self) -> None:
        file = self.workspace / "file"
        file.write_text("retain")
        for workspace in (self.repository, self.repository / "child", self.workspace / "missing", file):
            with self.subTest(workspace=workspace), unittest.mock.patch.object(upgrade_rehearsal, "_scratch") as scratch:
                with self.assertRaisesRegex(UpgradeRehearsalError, "workspace must"):
                    rehearse(self.repository, predecessor_python=PREDECESSOR, successor_python=SUCCESSOR,
                             output=self.output, workspace=workspace)
                scratch.assert_not_called()
                self.assertFalse(self.output.exists())
        with unittest.mock.patch.object(upgrade_rehearsal.tempfile, "gettempdir", return_value=str(self.repository)):
            with self.assertRaisesRegex(UpgradeRehearsalError, "outside the operational repository"):
                rehearse(self.repository, predecessor_python=PREDECESSOR, successor_python=SUCCESSOR, output=self.output)
        self.assertEqual("", git(self.repository, "status", "--porcelain"))
        self.assertEqual("retain", file.read_text())

    def test_git_path_diagnostic_failure_is_incomplete_and_does_not_hide_handover_failure(self) -> None:
        for failed_handover in (False, True):
            fake = FakeEvaluators(predecessor_doctor_before=int(failed_handover))
            output = self.output.with_name(f"path-query-{failed_handover}")
            def runner(argv, cwd):
                if list(argv[:2]) == ["git", "rev-parse"]:
                    return Completed(1, "", "do not retain this raw diagnostic")
                return fake(argv, cwd)
            with redirect_stderr(io.StringIO()):
                if failed_handover:
                    result = rehearse(self.repository, predecessor_python=PREDECESSOR, successor_python=SUCCESSOR,
                                      output=output, runner=runner, workspace=self.workspace, timings=True)
                    self.assertEqual("fail", result["overall_result"])
                else:
                    with self.assertRaisesRegex(UpgradeRehearsalError, "timing diagnostics are incomplete"):
                        rehearse(self.repository, predecessor_python=PREDECESSOR, successor_python=SUCCESSOR,
                                 output=output, runner=runner, workspace=self.workspace, timings=True)
            timing = json.loads((output / upgrade_rehearsal.TIMING_NAME).read_text())
            self.assertFalse(timing["complete"])
            self.assertEqual(["git-storage-paths"], timing["diagnostic_errors"])
            self.assertNotIn("do not retain", json.dumps(timing))
            self.assertEqual([], list(self.workspace.iterdir()))

    def test_cli_passes_the_explicit_workspace_without_changing_omitted_default(self) -> None:
        for extra, expected in (([], None), (["--workspace", str(self.workspace)], self.workspace)):
            with unittest.mock.patch.object(upgrade_rehearsal, "rehearse", return_value={"overall_result": "pass"}) as operation, unittest.mock.patch("builtins.print"):
                self.assertEqual(0, upgrade_rehearsal.main([
                    "--repository", str(self.repository), "--predecessor-python", str(PREDECESSOR),
                    "--successor-python", str(SUCCESSOR), "--output", str(self.output), "--json", *extra,
                ]))
            self.assertEqual(expected, operation.call_args.kwargs["workspace"])

    def test_partial_timing_retains_export_failure_without_masking_it(self) -> None:
        with unittest.mock.patch.object(upgrade_rehearsal.subprocess, "run", return_value=subprocess.CompletedProcess([], 1, b"", b"export refused")), redirect_stderr(io.StringIO()):
            with self.assertRaisesRegex(UpgradeRehearsalError, "export refused"):
                rehearse(self.repository, predecessor_python=PREDECESSOR, successor_python=SUCCESSOR,
                         output=self.output, runner=FakeEvaluators(), workspace=self.workspace, timings=True)
        timing = json.loads((self.output / upgrade_rehearsal.TIMING_NAME).read_text())
        self.assertFalse(timing["complete"])
        self.assertEqual([("replay", "error"), ("git-archive", "error"), ("scratch-cleanup", "finished")],
                         [(item["id"], item["status"]) for item in timing["stages"]])
        self.assertFalse((self.output / upgrade_rehearsal.RESULT_NAME).exists())

    def test_cleanup_failure_remains_an_error_and_is_measured(self) -> None:
        original = tempfile.TemporaryDirectory.cleanup

        def fail_after_cleanup(directory):
            original(directory)
            raise OSError("cleanup refused")

        with unittest.mock.patch.object(tempfile.TemporaryDirectory, "cleanup", fail_after_cleanup), redirect_stderr(io.StringIO()):
            with self.assertRaisesRegex(OSError, "cleanup refused"):
                rehearse(self.repository, predecessor_python=PREDECESSOR, successor_python=SUCCESSOR,
                         output=self.output, runner=FakeEvaluators(), workspace=self.workspace, timings=True)
        timing = json.loads((self.output / upgrade_rehearsal.TIMING_NAME).read_text())
        self.assertFalse(timing["complete"])
        self.assertEqual("scratch-cleanup", timing["stages"][-1]["id"])
        self.assertEqual("error", timing["stages"][-1]["status"])

    def test_unwritable_timing_cannot_hide_export_failure_or_claim_complete_success(self) -> None:
        with unittest.mock.patch.object(Path, "replace", side_effect=PermissionError("timing denied")), redirect_stderr(io.StringIO()):
            with unittest.mock.patch.object(upgrade_rehearsal.subprocess, "run", side_effect=RuntimeError("original failure")):
                with self.assertRaisesRegex(RuntimeError, "original failure"):
                    rehearse(self.repository, predecessor_python=PREDECESSOR, successor_python=SUCCESSOR,
                             output=self.output, runner=FakeEvaluators(), workspace=self.workspace, timings=True)
            with self.assertRaisesRegex(UpgradeRehearsalError, "timing diagnostics are incomplete"):
                rehearse(self.repository, predecessor_python=PREDECESSOR, successor_python=SUCCESSOR,
                         output=self.output.with_name("other-out"), runner=FakeEvaluators(), workspace=self.workspace, timings=True)

    def test_timing_cannot_write_into_the_operational_repository(self) -> None:
        with self.assertRaisesRegex(UpgradeRehearsalError, "outside the operational repository"):
            rehearse(self.repository, predecessor_python=PREDECESSOR, successor_python=SUCCESSOR,
                     output=self.repository / "diagnostic", runner=FakeEvaluators(), timings=True)
        self.assertFalse((self.repository / "diagnostic").exists())


class TimingClockTests(unittest.TestCase):
    def test_nested_measurements_use_monotonic_intervals_and_flush_progress(self) -> None:
        with tempfile.TemporaryDirectory() as directory, unittest.mock.patch("builtins.print") as progress:
            timing = upgrade_rehearsal.RehearsalTiming(Path(directory), clock=iter([10., 12., 17., 22.]).__next__)
            with timing.measure("replay"):
                with timing.measure("git-archive"):
                    partial = json.loads((Path(directory) / upgrade_rehearsal.TIMING_NAME).read_text())
                    self.assertFalse(partial["complete"])
                    self.assertEqual("running", partial["stages"][-1]["status"])
            self.assertEqual([(None, 12.), ("replay", 5.)],
                             [(item["parent"], item["elapsed_seconds"]) for item in timing.data["stages"]])
            self.assertEqual(4, progress.call_count)
            self.assertTrue(all(call.kwargs["flush"] for call in progress.call_args_list))

    def test_interruption_is_not_suppressed_or_reported_as_finished(self) -> None:
        with tempfile.TemporaryDirectory() as directory, redirect_stderr(io.StringIO()):
            timing = upgrade_rehearsal.RehearsalTiming(Path(directory), clock=iter([3., 8.]).__next__)
            with self.assertRaises(KeyboardInterrupt):
                with timing.measure("replay"):
                    raise KeyboardInterrupt()
            saved = json.loads((Path(directory) / upgrade_rehearsal.TIMING_NAME).read_text())
            self.assertFalse(saved["complete"])
            self.assertEqual("KeyboardInterrupt", saved["stages"][0]["error_type"])
            self.assertEqual(5., saved["stages"][0]["elapsed_seconds"])

    def test_timing_identity_is_allowlisted(self) -> None:
        with tempfile.TemporaryDirectory() as directory, unittest.mock.patch.dict(os.environ, {"GITHUB_TOKEN": "secret", "GITHUB_SHA": "tested", "REHEARSAL_HEAD_SHA": "head"}):
            timing = upgrade_rehearsal.RehearsalTiming(Path(directory))
            self.assertEqual("tested", timing.data["identity"]["GITHUB_SHA"])
            self.assertEqual("head", timing.data["identity"]["REHEARSAL_HEAD_SHA"])
            self.assertNotIn("secret", json.dumps(timing.data))


class RetiredSurfaceTests(unittest.TestCase):
    """Issue #210 acceptance criteria 2 and 3, and the reserved names."""

    #: The stage machine's files, deleted by WO-ECP-011 once the 0.8.0 root
    #: (WO-HUP-008) no longer required a tracked file per pattern.
    DELETED_WITH_THE_ROOT_ADVANCE = (
        "se_harness/governance_migration.py",
        "se_harness/governance_migration_contract.py",
        "se_harness/governance_migration_contract.json",
        "tests/fixtures/governance_migration/synthetic-n-minus-1-to-n.json",
    )

    def test_no_json_under_se_harness_embeds_a_digest_of_a_python_module(self) -> None:
        digests = {hashlib.sha256(path.read_bytes()).hexdigest() for path in (REPOSITORY_ROOT / "se_harness").rglob("*.py")}
        for path in sorted((REPOSITORY_ROOT / "se_harness").glob("*.json")):
            with self.subTest(contract=path.name):
                values = re.findall(r"[0-9a-f]{64}", path.read_text(encoding="utf-8"))
                self.assertEqual([], [value for value in values if value in digests])

    def test_the_stage_machine_is_retired_dead_and_its_names_are_reserved(self) -> None:
        for relative in ("tests/test_governance_migration.py", "repository_tools/predecessor_facts.py",
                         "tests/fixtures/governance_migration/candidate-0.7.1-to-0.8.0.json"):
            self.assertFalse((REPOSITORY_ROOT / relative).exists(), relative)
        for relative in self.DELETED_WITH_THE_ROOT_ADVANCE:
            self.assertFalse((REPOSITORY_ROOT / relative).exists(), relative)
        self.assertFalse((REPOSITORY_ROOT / "tests/fixtures/governance_migration").exists())
        for relative in sorted((REPOSITORY_ROOT / "se_harness").rglob("*.py")):
            text = relative.read_text(encoding="utf-8")
            self.assertNotIn("rehearse-migration", text, relative.name)
            self.assertNotIn("governance_migration", text, relative.name)
            self.assertIsNone(re.search(r"\bMIG[0-9]{3}\b", text), relative.name)
        surface = (REPOSITORY_ROOT / "scripts/check_portable_release_surface.py").read_text(encoding="utf-8")
        self.assertIn('b"rehearse-migration"', surface)
        self.assertIn("RETIRED_MIGRATION_MEMBERS", surface)
        workflows = " ".join(path.read_text(encoding="utf-8") for path in (REPOSITORY_ROOT / ".github/workflows").glob("*.yml"))
        self.assertNotIn("rehearse-migration", workflows)

    def test_the_owner_rules_and_the_retired_members_are_gone_or_forbidden(self) -> None:
        attributes = (REPOSITORY_ROOT / ".gitattributes").read_text(encoding="utf-8")
        self.assertNotIn("governance_migration", attributes)
        surface = (REPOSITORY_ROOT / "scripts/check_portable_release_surface.py").read_text(encoding="utf-8")
        self.assertIn("FORBIDDEN_MEMBERS = FORBIDDEN_MEMBERS | RETIRED_MIGRATION_MEMBERS", surface)
        self.assertIn("FORBIDDEN_ACTIVE_PATHS = FORBIDDEN_ACTIVE_PATHS | RETIRED_MIGRATION_MEMBERS", surface)

    def test_the_lane_runs_the_rehearsal_twice_per_platform_and_compares_across(self) -> None:
        workflow = (REPOSITORY_ROOT / ".github/workflows/candidate-evidence.yml").read_text(encoding="utf-8")
        self.assertEqual(2, workflow.count("python -m repository_tools.upgrade_rehearsal --repository ."))
        self.assertIn("windows-latest", workflow)
        self.assertIn("if ($firstResult.semantic_sha256 -ne $secondResult.semantic_sha256)", workflow)
        self.assertIn("cross-platform semantic mismatch", workflow)
        self.assertNotIn("rehearse-migration", workflow)
        self.assertNotIn("scenario", workflow.lower())


class RunnerTimeoutTests(unittest.TestCase):
    """WO-ECP-027 (ECP-COR-015): the rehearsal runner is bounded; a timeout is a failed Completed."""

    def test_a_timeout_becomes_a_failed_completed(self) -> None:
        with unittest.mock.patch(
            "repository_tools.upgrade_rehearsal.subprocess.run",
            side_effect=subprocess.TimeoutExpired(cmd="evaluator", timeout=600),
        ) as run:
            completed = upgrade_rehearsal.run(["evaluator", "doctor", "."], Path("."))
        self.assertEqual(124, completed.exit_code)
        self.assertIn("timed out", completed.stderr)
        self.assertEqual(600, run.call_args.kwargs.get("timeout"))
