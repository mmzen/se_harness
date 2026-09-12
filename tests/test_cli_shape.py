"""The harnessctl command shape (REQ-ECP-027 / SPEC-ECP-016, ECP-CLI-001 to -008).

Every test drives ``main()``; commands that need an environment have their
collaborator mocked at the module boundary.
"""

from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from se_harness.cli import build_parser, main
from se_harness.codes import MG005, WEX220
from se_harness.release_qualification import failed_qualification
from tests.fixture_support import standard_repository
from tests.mutation_guard_support import patch_mutation_authority
from tests.artifact_support import create_base_chain
from tests.cli_support import invoke

#: ECP-CLI-001: the repository commands take the positional `target`; the
#: non-repository commands take none (WO-ECP-030 retired rehearse-recovery and renumber-artifacts).
REPOSITORY_COMMANDS = {
    "init", "validate", "inspect", "dashboard", "doctor", "preflight", "check", "evidence",
    "pr-body", "transition", "upgrade", "skill-ownership", "scaffold-domain", "create-artifact",
    "release-unit", "capture-verification", "prepare-release", "decide", "raise-risk", "risks",
}
NON_REPOSITORY_COMMANDS = {"select-work-order", "identity"}
REPOSITORY_QUALIFY_ROLES = {"released-root", "complete-candidate", "public-install"}
NON_REPOSITORY_QUALIFY_ROLES = {"candidate-package"}
SCHEMA = "se-harness-command-result-v1"


def _subparsers(parser):
    action = next(a for a in parser._actions if getattr(a, "choices", None) and "preflight" in a.choices)
    return action.choices


def _positionals(subparser) -> list[str]:
    return [a.dest for a in subparser._actions if not a.option_strings and a.dest != "help" and a.dest != "qualification_operation"]


def _options(subparser) -> set[str]:
    return {opt for a in subparser._actions for opt in a.option_strings}


class ParserShapeTests(unittest.TestCase):
    def test_every_subcommand_is_classified_and_takes_target_accordingly(self) -> None:
        choices = _subparsers(build_parser())
        self.assertEqual(
            REPOSITORY_COMMANDS | NON_REPOSITORY_COMMANDS | {"qualify"},
            set(choices),
        )
        for name in REPOSITORY_COMMANDS:
            with self.subTest(command=name):
                self.assertEqual(["target"], _positionals(choices[name]))
                self.assertFalse(_options(choices[name]) & {"--root", "--repository", "--checkout-root"})
                target = next(action for action in choices[name]._actions if action.dest == "target")
                if name == "skill-ownership":
                    self.assertTrue(target.required)
                    self.assertIsNone(target.nargs)
                    self.assertIsNone(target.default)
                else:
                    self.assertEqual("?", target.nargs)
                    self.assertEqual(".", target.default)
        for name in NON_REPOSITORY_COMMANDS:
            with self.subTest(command=name):
                self.assertEqual([], _positionals(choices[name]))
        roles = next(a for a in choices["qualify"]._actions if getattr(a, "choices", None)).choices
        self.assertEqual(REPOSITORY_QUALIFY_ROLES | NON_REPOSITORY_QUALIFY_ROLES, set(roles))
        for name in REPOSITORY_QUALIFY_ROLES:
            with self.subTest(role=name):
                self.assertEqual(["target"], _positionals(roles[name]))
        self.assertEqual([], _positionals(roles["candidate-package"]))

    def test_every_subcommand_accepts_json(self) -> None:
        # ECP-CLI-003.
        choices = _subparsers(build_parser())
        for name, subparser in choices.items():
            if name == "qualify":
                roles = next(a for a in subparser._actions if getattr(a, "choices", None)).choices
                for role, role_parser in roles.items():
                    with self.subTest(command=f"qualify {role}"):
                        self.assertIn("--json", _options(role_parser))
                continue
            with self.subTest(command=name):
                self.assertIn("--json", _options(subparser))

    def test_skill_ownership_requires_explicit_target_and_provider(self) -> None:
        # WO-PLG-020: the sole optional-target exception keeps the exact census.
        ownership = _subparsers(build_parser())["skill-ownership"]
        provider = next(action for action in ownership._actions if action.dest == "provider")
        self.assertTrue(provider.required)
        self.assertEqual({"plugin", "repository"}, set(provider.choices))
        for arguments, diagnostic in (
            (("skill-ownership", "--provider", "repository"), "target"),
            (("skill-ownership", "explicit-repository"), "--provider"),
            (("skill-ownership", "explicit-repository", "--provider", "automatic"), "invalid choice"),
        ):
            with self.subTest(arguments=arguments):
                code, output, error = invoke(*arguments)
                self.assertEqual(2, code)
                self.assertEqual("", output)
                self.assertIn(diagnostic, error)

    def test_skill_ownership_plans_by_default_and_applies_reviewed_selection(self) -> None:
        # Parser/handler selection only; real package authority is covered by OWN01.
        target = Path("explicit-repository")
        binding = Path("explicit-binding.json")
        digest = "a" * 64
        planned = {"schema": SCHEMA, "command": "skill-ownership", "outcome": "planned", "passed": True}
        applied = {**planned, "outcome": "applied"}
        arguments = ("skill-ownership", str(target), "--provider", "plugin",
                     "--binding-input", str(binding), "--json")
        with mock.patch("se_harness.skill_ownership.plan_skill_ownership", return_value=planned) as plan, \
                mock.patch("se_harness.skill_ownership.apply_skill_ownership", return_value=applied) as apply:
            code, output, error = invoke(*arguments)
            self.assertEqual((0, ""), (code, error))
            self.assertEqual(planned, json.loads(output))
            plan.assert_called_once_with(target, provider="plugin", binding_input=binding)
            apply.assert_not_called()
            plan.reset_mock()
            code, output, error = invoke(*arguments, "--apply", "--expected-plan-sha256", digest)
            self.assertEqual((0, ""), (code, error))
            self.assertEqual(applied, json.loads(output))
            plan.assert_not_called()
            apply.assert_called_once_with(target, provider="plugin", binding_input=binding,
                                          expected_plan_sha256=digest)
        for extra, diagnostic in (
            (("--apply",), "invalid SHA-256: reviewed ownership plan"),
            (("--expected-plan-sha256", digest), "--expected-plan-sha256 requires --apply"),
        ):
            with self.subTest(arguments=extra):
                code, output, error = invoke(*arguments, *extra)
                self.assertEqual((1, ""), (code, error))
                result = json.loads(output)
                self.assertEqual((SCHEMA, "skill-ownership", "failed", False),
                                 (result["schema"], result["command"], result["outcome"], result["passed"]))
                self.assertIn(diagnostic, result["error"])

    def test_prepare_release_names_its_actor_owner_and_knows_no_authorized_by(self) -> None:
        # ECP-CLI-002, amended under WO-ECP-025 (ECP-TMB-006): the pre-parse guard is
        # gone; argparse refuses the unknown option as it refuses any other.
        choices = _subparsers(build_parser())
        self.assertIn("--owner", _options(choices["prepare-release"]))
        self.assertNotIn("--authorized-by", _options(choices["prepare-release"]))
        code, output, error = invoke("prepare-release", ".", "--id", "RLS-001", "--authorized-by", "release-owner")
        self.assertEqual(2, code)
        self.assertEqual("", output)
        self.assertIn("harnessctl prepare-release: error:", error)
        self.assertIn("--owner", error)
        self.assertNotIn("was renamed", error)


class RepositoryCommandShapeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        standard_repository(self.root)
        patch_mutation_authority(self)
        create_base_chain(self.root, operating_contract_status="draft")

    def json_of(self, *arguments: str) -> tuple[int, dict, str]:
        code, output, error = invoke(*arguments)
        self.assertTrue(output, f"no stdout; stderr: {error}")
        return code, json.loads(output), error

    def test_doctor_json_lists_every_check(self) -> None:
        code, payload, error = self.json_of("doctor", str(self.root), "--json")
        self.assertEqual(0, code, error)
        self.assertEqual((SCHEMA, "doctor", "completed"), (payload["schema"], payload["command"], payload["outcome"]))
        self.assertTrue(payload["checks"])
        self.assertTrue(all(set(item) == {"name", "passed", "detail"} for item in payload["checks"]))
        self.assertIn("warnings", payload)

    def test_create_artifact_and_scaffold_domain_json(self) -> None:
        # ECP-CLI-008: create-artifact through main().
        code, payload, error = self.json_of("create-artifact", str(self.root), "--domain", "product", "--type", "requirement", "--id", "REQ-777", "--json")
        self.assertEqual(0, code, error)
        self.assertEqual("create-artifact", payload["command"])
        self.assertEqual([{"action": "create", "path": "docs/engineering/product/requirements/REQ-777.md"}], payload["changes"])
        self.assertFalse(payload["dry_run"])
        self.assertNotIn("allocated_id", payload)
        # Allocation needs a Git checkout (ECP-IDA); the fixture has none, so the id is explicit.
        code, payload, error = self.json_of("create-artifact", str(self.root), "--domain", "product", "--type", "requirement", "--id", "REQ-778", "--dry-run", "--json")
        self.assertEqual(0, code, error)
        self.assertTrue(payload["dry_run"])
        self.assertNotIn("allocated_id", payload)
        code, payload, error = self.json_of("scaffold-domain", str(self.root), "--domain", "shape-domain", "--dry-run", "--json")
        self.assertEqual(0, code, error)
        self.assertEqual("scaffold-domain", payload["command"])
        self.assertTrue(payload["changes"])
        self.assertTrue(payload["dry_run"])

    def test_pr_body_and_select_work_order_json(self) -> None:
        work_order = self.root / "docs/engineering/product/work-orders/WO-001.md"
        # The selection rule wants a domain-segmented id; the renderer is mocked, so the body names one.
        body = "Harness-Work-Order: WO-PRD-001" + chr(10) * 2 + "## Summary" + chr(10) * 2 + "- WO-PRD-001" + chr(10)
        with mock.patch("se_harness.github_ci.render_pull_request_body", return_value=body):
            code, payload, error = self.json_of("pr-body", str(self.root), "--artifact", "WO-001", "--json")
        self.assertEqual(0, code, error)
        self.assertEqual("pr-body", payload["command"])
        self.assertIn("Harness-Work-Order: WO-PRD-001", payload["body"])
        event = self.root / "event.json"
        event.write_text(json.dumps({"pull_request": {"body": payload["body"]}}), encoding="utf-8")
        code, payload, error = self.json_of("select-work-order", "--event", str(event), "--json")
        self.assertEqual(0, code, error)
        self.assertEqual({"schema": SCHEMA, "command": "select-work-order", "outcome": "completed", "field": "work-order", "value": "WO-PRD-001"}, payload)
        self.assertTrue(work_order.is_file())

    def test_a_mutation_guard_refusal_is_an_environment_refusal(self) -> None:
        # ECP-CLI-004: the guard fires before any result exists, so the command could not run.
        # WO-ECP-027 (ECP-COR-004, ECP-COR-005): the guard raises its own type and the
        # handler re-raises it by type, never by message prefix.
        from se_harness.mutation_guard import MutationGuardError

        with mock.patch("se_harness.mutation_guard.require_mutation_authority", side_effect=MutationGuardError(MG005, "capture-verification", "RID002 harness_version: resolved")):
            code, output, error = invoke(
                "capture-verification", str(self.root), "--id", "VREC-009", "--work-order", "WO-001",
                "--verification", "VER-001", "--evidence", "README.md", "--json",
            )
        self.assertEqual(2, code)
        self.assertEqual("", output)
        self.assertTrue(error.startswith("harnessctl: mutation guard MG005"), error)

    def test_check_prints_each_code_once(self) -> None:
        # ECP-CLI-006.
        code, payload, error = self.json_of("check", str(self.root), "--artifact", "REQ-001", "--json")
        self.assertEqual(1, code)
        blocker = payload["restitution"]["blocked_by"][0]
        self.assertTrue(blocker.startswith("WEX210: "), blocker)
        self.assertEqual(1, blocker.count("WEX210"))

    def test_checkpoint_check_prints_each_code_once(self) -> None:
        # WO-ECP-027 (ECP-COR-001): the checkpoint path splits the code as the projection does.
        code, payload, error = self.json_of("check", str(self.root), "--artifact", "WO-ZZZ-999", "--checkpoint", "scope", "--json")
        self.assertEqual(1, code, error)
        blocker = payload["restitution"]["blocked_by"][0]
        self.assertEqual("WEX210: unknown artifact ID: WO-ZZZ-999", blocker)
        self.assertEqual(1, blocker.count("WEX210"))

    def test_transition_guard_refusal_exits_2(self) -> None:
        # WO-ECP-027 (ECP-COR-005): transition follows its siblings; the guard is a refusal.
        from se_harness.mutation_guard import MutationGuardError

        with mock.patch("se_harness.cli.plan_transition", side_effect=MutationGuardError(MG005, "transition", "RID002 harness_version: resolved")):
            code, output, error = invoke("transition", str(self.root), "--apply", "--set", "WO-001=verified", "--decision", "WO-001=engineering-owner", "--json")
        self.assertEqual(2, code)
        self.assertEqual("", output)
        self.assertTrue(error.startswith("harnessctl: mutation guard MG005"), error)

    def test_transition_option_syntax_error_is_a_refusal(self) -> None:
        # WO-ECP-027 (ECP-COR-006): a malformed --set is a usage error, not a blocked result.
        code, output, error = invoke("transition", str(self.root), "--set", "WO-001", "--decision", "WO-001=engineering-owner", "--json")
        self.assertEqual(2, code)
        self.assertEqual("", output)
        self.assertTrue(error.startswith("harnessctl: --set must use ID=VALUE"), error)

    def test_result_handlers_convert_the_shared_tuple(self) -> None:
        # WO-ECP-027 (ECP-COR-002, ECP-COR-007): every result-building handler converts the
        # classes _check converts, with the code split once.
        from se_harness.workflow_procedures import ProcedureError

        with mock.patch("se_harness.cli.plan_transition", side_effect=ProcedureError(WEX220, "no procedure binds the transition")):
            code, payload, error = self.json_of("transition", str(self.root), "--set", "WO-001=verified", "--decision", "WO-001=engineering-owner", "--json")
        self.assertEqual(1, code, error)
        self.assertEqual(["WEX220: no procedure binds the transition"], payload["restitution"]["blocked_by"])
        with mock.patch("se_harness.cli.write_evidence_packet", side_effect=ValueError("WEX230: result field missing")):
            code, payload, error = self.json_of("evidence", str(self.root), "--artifact", "WO-001", "--checkpoint", "handoff", "--json")
        self.assertEqual(1, code, error)
        self.assertEqual(["WEX230: result field missing"], payload["restitution"]["blocked_by"])
        with mock.patch("se_harness.cli.capture_verification", side_effect=ProcedureError(WEX220, "no procedure binds the record")):
            code, payload, error = self.json_of(
                "capture-verification", str(self.root), "--id", "VREC-009", "--work-order", "WO-001",
                "--verification", "VER-001", "--evidence", "README.md", "--json",
            )
        self.assertEqual(1, code, error)
        self.assertEqual(["WEX220: no procedure binds the record"], payload["restitution"]["blocked_by"])

    def test_main_refuses_a_procedure_error_that_escapes_a_handler(self) -> None:
        # WO-ECP-027 (ECP-COR-008): no traceback; the refusal line and exit 2.
        from se_harness.workflow_procedures import ProcedureError

        with mock.patch("se_harness.cli.inspect_installation", side_effect=ProcedureError(WEX220, "no procedure binds doctor")):
            code, output, error = invoke("doctor", str(self.root))
        self.assertEqual(2, code)
        self.assertEqual("", output)
        self.assertTrue(error.startswith("harnessctl: WEX220: no procedure binds doctor"), error)  # ECP-PRM-017: the refusal carries its code

    def test_dashboard_json_passes_the_engine_refusal_and_error_through(self) -> None:
        # WO-ECP-027 (ECP-COR-009, ECP-COR-010): engine exit 2 is a refusal, engine exit 1 keeps its
        # standard error; since WO-ECP-034 (ECP-ENG-003) the engine runs in-process.
        import sys

        def refusing(argv):
            print("GenerationError: bad root", file=sys.stderr)
            return 2

        def failing(argv):
            print("dashboard: manifest mismatch", file=sys.stderr)
            return 1

        with mock.patch("se_harness.cli.generate_harness_dashboard.main", side_effect=refusing):
            code, output, error = invoke("dashboard", str(self.root), "--json")
        self.assertEqual(2, code)
        self.assertEqual("", output)
        self.assertIn("GenerationError: bad root", error)
        with mock.patch("se_harness.cli.generate_harness_dashboard.main", side_effect=failing):
            code, payload, error = self.json_of("dashboard", str(self.root), "--json")
        self.assertEqual(1, code, error)
        self.assertEqual("failed", payload["outcome"])
        self.assertIn("manifest mismatch", payload["error"])

    def test_pr_body_unknown_artifact_is_a_failed_result(self) -> None:
        # WO-ECP-027 (ECP-COR-011, ECP-COR-012): exit 1 with the result on stdout, as check and evidence.
        code, payload, error = self.json_of("pr-body", str(self.root), "--artifact", "WO-ZZZ-999", "--json")
        self.assertEqual(1, code, error)
        self.assertEqual(("pr-body", "failed", "WEX-ECP-014"), (payload["command"], payload["outcome"], payload["code"]))
        self.assertIn("WO-ZZZ-999", payload["message"])
        code, output, error = invoke("pr-body", str(self.root), "--artifact", "WO-ZZZ-999")
        self.assertEqual(1, code)
        self.assertEqual("WEX-ECP-014: unknown artifact ID: WO-ZZZ-999\n", output)
        self.assertEqual("", error)

    def test_the_engine_runs_in_process_and_its_exit_code_is_ours(self) -> None:
        # WO-ECP-034 (SPEC-ECP-024 ECP-ENG-003): no engine subprocess exists to time out; the
        # validator runs in-process and the command returns its exit code.
        import subprocess

        with mock.patch("se_harness._process.subprocess.run", side_effect=subprocess.TimeoutExpired(cmd="validate", timeout=1)) as run:
            code, output, error = invoke("validate", str(self.root))
        self.assertEqual(0, code, error)
        self.assertIn("Engineering artifact validation: PASS", output)
        self.assertFalse(run.called)
        with mock.patch("se_harness.cli.validate_engineering_artifacts.main", return_value=1) as main:
            code, output, error = invoke("validate", str(self.root), "--json")
        self.assertEqual(1, code)
        self.assertEqual(["--root", str(self.root.resolve()), "--json"], main.call_args.args[0])

    def test_every_subprocess_launch_in_the_package_carries_a_timeout(self) -> None:
        # WO-ECP-027 (ECP-COR-013 to ECP-COR-015): the inspection VER-ECP-023 names.
        import ast

        repository = Path(__file__).resolve().parents[1]
        unbounded: list[str] = []
        for base in ("se_harness", "repository_tools"):
            for path in sorted((repository / base).rglob("*.py")):
                tree = ast.parse(path.read_text(encoding="utf-8"))
                for node in ast.walk(tree):
                    if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                        continue
                    if not (isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess"):
                        continue
                    if node.func.attr in {"run", "check_output", "check_call", "Popen"} and not any(k.arg == "timeout" for k in node.keywords):
                        unbounded.append(f"{path.relative_to(repository).as_posix()}:{node.lineno}")
        self.assertEqual([], unbounded)

    def test_init_dry_run_json_and_conflict_exit_code(self) -> None:
        fresh = self.root / "fresh"
        fresh.mkdir()
        code, payload, error = self.json_of("init", str(fresh), "--dry-run", "--json")
        self.assertEqual(0, code, error)
        self.assertEqual(("init", "completed", False), (payload["command"], payload["outcome"], payload["written"]))
        self.assertTrue(all(set(item) == {"action", "path"} for item in payload["changes"]))
        (fresh / "AGENTS.md").write_text("owner content without markers\n", encoding="utf-8")
        (fresh / ".github").mkdir()
        (fresh / ".github" / "workflows").mkdir()
        (fresh / ".github" / "workflows" / "engineering-harness.yml").write_text("name: other\n", encoding="utf-8")
        code, output, error = invoke("init", str(fresh), "--json")
        if code == 1:
            payload = json.loads(output)
            self.assertEqual("failed", payload["outcome"])
            self.assertTrue(payload["conflicts"])
            self.assertEqual("", error)


class MockedCommandShapeTests(unittest.TestCase):
    def test_identity_json_is_the_runtime_identity_object(self) -> None:
        # ECP-CLI-008 / -003.
        report = mock.Mock(passed=False)
        report.to_dict.return_value = {"schema": "se-harness-runtime-identity-v3", "passed": False}
        with mock.patch("se_harness.cli.inspect_runtime_identity", return_value=report) as inspect:
            code, output, error = invoke("identity", "--role", "released-evaluator", "--expected-version", "0.11.0", "--expected-root", "x", "--json")
        self.assertEqual(1, code)
        self.assertEqual({"schema": "se-harness-runtime-identity-v3", "passed": False}, json.loads(output))
        self.assertEqual("released-evaluator", inspect.call_args.kwargs["role"])

    def test_qualify_exits_one_on_a_failed_result_and_prints_its_json(self) -> None:
        # ECP-CLI-008 / -004.
        failed = failed_qualification("complete-candidate", code="RQ001", subject="qualification-input", message="stub")
        with mock.patch("se_harness.cli.qualify_complete_candidate", return_value=failed) as qualify:
            code, output, error = invoke("qualify", "complete-candidate", ".", "--candidate-commit", "a" * 40, "--json")
        self.assertEqual(1, code)
        payload = json.loads(output)
        self.assertEqual("se-harness-release-qualification-v1", payload["schema"])
        self.assertEqual("a" * 40, qualify.call_args.kwargs["candidate_commit"])


if __name__ == "__main__":
    unittest.main()
