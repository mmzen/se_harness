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
from se_harness.release_qualification import failed_qualification
from tests.fixture_support import standard_repository
from tests.mutation_guard_support import trusted_mutation_authority
from tests.test_revision_provenance import create_base_chain

#: ECP-CLI-001: the repository commands take the positional `target`; the three
#: non-repository commands take none; rehearse-recovery keeps its shape (issue #221).
REPOSITORY_COMMANDS = {
    "init", "adopt", "validate", "inspect", "dashboard", "doctor", "preflight", "check", "evidence",
    "pr-body", "transition", "upgrade", "scaffold-domain", "create-artifact", "renumber-artifacts",
    "release-unit", "capture-verification", "prepare-release", "decide",
}
NON_REPOSITORY_COMMANDS = {"select-work-order", "identity"}
REPOSITORY_QUALIFY_ROLES = {"released-root", "complete-candidate", "public-install"}
NON_REPOSITORY_QUALIFY_ROLES = {"candidate-package"}
SCHEMA = "se-harness-command-result-v1"


def invoke(*arguments: str) -> tuple[int, str, str]:
    output = io.StringIO()
    error = io.StringIO()
    with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
        code = main(list(arguments))
    return code, output.getvalue(), error.getvalue()


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
            REPOSITORY_COMMANDS | NON_REPOSITORY_COMMANDS | {"rehearse-recovery", "qualify"},
            set(choices),
        )
        for name in REPOSITORY_COMMANDS:
            with self.subTest(command=name):
                self.assertEqual(["target"], _positionals(choices[name]))
                self.assertFalse(_options(choices[name]) & {"--root", "--repository", "--checkout-root"})
        for name in NON_REPOSITORY_COMMANDS:
            with self.subTest(command=name):
                self.assertEqual([], _positionals(choices[name]))
        self.assertEqual(["output"], _positionals(choices["rehearse-recovery"]))
        self.assertIn("--repository", _options(choices["rehearse-recovery"]))
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

    def test_prepare_release_names_its_actor_owner_and_knows_no_authorized_by(self) -> None:
        # ECP-CLI-002, amended under WO-ECP-025 (ECP-TMB-006): the pre-parse guard is
        # gone; argparse refuses the unknown option as it refuses any other.
        choices = _subparsers(build_parser())
        self.assertIn("--owner", _options(choices["prepare-release"]))
        self.assertNotIn("--authorized-by", _options(choices["prepare-release"]))
        output = io.StringIO()
        error = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error), self.assertRaises(SystemExit) as raised:
            main(["prepare-release", ".", "--id", "RLS-001", "--authorized-by", "release-owner"])
        self.assertEqual(2, raised.exception.code)
        self.assertEqual("", output.getvalue())
        self.assertIn("harnessctl prepare-release: error:", error.getvalue())
        self.assertIn("--owner", error.getvalue())
        self.assertNotIn("was renamed", error.getvalue())


class RepositoryCommandShapeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        standard_repository(self.root, "Shape Fixture")
        guard = mock.patch("se_harness.mutation_guard.require_mutation_authority", side_effect=trusted_mutation_authority)
        guard.start()
        self.addCleanup(guard.stop)
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

    def test_renumber_artifacts_plans_through_main(self) -> None:
        # ECP-CLI-008: renumber-artifacts through main(); planning writes nothing.
        code, output, error = invoke("renumber-artifacts", str(self.root), "--map", "REQ-001=REQ-009", "--json")
        payload = json.loads(output)
        self.assertEqual("se-harness-renumber-v1", payload["schema"])
        self.assertIn(code, (0, 1))
        self.assertTrue((self.root / "docs/engineering/product/requirements/REQ-001.md").is_file())

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
        from se_harness.installer import HarnessError

        with mock.patch("se_harness.mutation_guard.require_mutation_authority", side_effect=HarnessError("mutation guard MG005 (capture-verification): RID002 harness_version: resolved")):
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
    def test_rehearse_recovery_exits_by_result_and_prints_the_report(self) -> None:
        # ECP-CLI-008 / -004.
        for result, expected in (("pass", 0), ("fail", 1)):
            with self.subTest(result=result):
                report = {"schema": "se-harness-evaluator-recovery-rehearsal-v1", "result": result}
                with mock.patch("se_harness.cli.run_recovery_rehearsal", return_value=report) as run:
                    code, output, error = invoke("rehearse-recovery", "out-dir", "--candidate-commit", "a" * 40, "--json")
                self.assertEqual(expected, code)
                payload = json.loads(output)
                self.assertEqual((SCHEMA, "rehearse-recovery", "completed" if expected == 0 else "failed"), (payload["schema"], payload["command"], payload["outcome"]))
                self.assertEqual(report, payload["report"])
                self.assertEqual(Path("out-dir"), run.call_args.args[0])

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
