"""REQ-ECP-011 / SPEC-ECP-006 ECP-DLG-001 to -007, -009, -010: the delegation class.

Every scenario of VER-ECP-015 over a fixture repository with a real Git history:
the work order carries `[delegation] class = "execution"` at the base branch,
the gate is a local file the test controls, and the CLI is driven through
`main()`; the `github-checks` source is exercised against a stub HTTP server.
"""

from __future__ import annotations

import contextlib
import http.server
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock

from se_harness.cli import main
from se_harness.gate_source import DELEGATED_ROLE, DelegationConfiguration, read_gate
from tests.fixture_support import standard_repository
from tests.mutation_guard_support import trusted_mutation_authority
from tests.test_revision_provenance import create_base_chain, write

ASSURANCE_AND_SCOPE = """[assurance]
commit_bound_verification = "required"
rationale = "The executable fixture requires exact-candidate assurance."
decided_by = "engineering-owner"

[execution_scope]
paths = ["src/"]

[relations]"""

READY_RECORD = [
    "+++", 'id = "VREC-001"', 'type = "verification_record"', 'title = "t"', 'status = "ready"',
    'owners = ["assurance-owner"]', 'created = "2026-08-29"', 'updated = "2026-08-29"',
    'commit = "0000000000000000000000000000000000000000"', 'git_object_format = "sha1"',
    'worktree_state = "clean"', 'prepared_at = "2026-08-29T00:00:00Z"', 'prepared_by = "x"',
    'artifact_snapshot_sha256 = "' + "0" * 64 + '"', 'evidence_paths = ["docs/engineering/product/evidence/e.md"]',
    "[relations]", 'verifies_work_order = ["WO-PRD-001"]', 'conforms_to = ["VER-001"]', "+++", "", "# r", "",
]


class DelegationFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        standard_repository(self.root, "Delegation Fixture")
        create_base_chain(self.root, work_order_status="approved", operating_contract_status="draft")
        # Preflight requires a domain-segmented id (WO-XXX-NNN); the base chain writes WO-001.
        original = self.root / "docs/engineering/product/work-orders/WO-001.md"
        self.work_order = self.root / "docs/engineering/product/work-orders/WO-PRD-001.md"
        self.work_order.write_text(original.read_text(encoding="utf-8").replace('id = "WO-001"', 'id = "WO-PRD-001"', 1), encoding="utf-8")
        original.unlink()
        for artifact in (self.root / "docs/engineering/product").rglob("*.md"):
            content = artifact.read_text(encoding="utf-8")
            if "WO-001" in content:
                artifact.write_text(content.replace("WO-001", "WO-PRD-001"), encoding="utf-8")
        text = self.work_order.read_text(encoding="utf-8")
        if "[assurance]" not in text:
            self.work_order.write_text(text.replace("[relations]", ASSURANCE_AND_SCOPE, 1), encoding="utf-8")
        self.environment = mock.patch.dict(os.environ, {"SE_HARNESS_REHEARSAL": "1"})
        self.environment.start()
        self.addCleanup(self.environment.stop)
        guard = mock.patch("se_harness.mutation_guard.require_mutation_authority", side_effect=trusted_mutation_authority)
        guard.start()
        self.addCleanup(guard.stop)

    def git(self, *arguments: str) -> str:
        return subprocess.run(
            ["git", "-C", str(self.root), *arguments], capture_output=True, text=True, check=True,
        ).stdout.strip()

    def declare_class(self, *, at_base: bool = True) -> None:
        text = self.work_order.read_text(encoding="utf-8")
        if "[delegation]" not in text:
            text = text.replace("[relations]", '[delegation]\nclass = "execution"\n\n[relations]', 1)
            self.work_order.write_text(text, encoding="utf-8")
        if at_base:
            self.commit("declare the class")

    def configure(self, source: str = "local-file", **extra: str) -> None:
        # Owner content beside the managed toml, never inside it (the toml is hash-locked).
        lines = [
            "[delegation]", f'gate_source = "{source}"', 'check_name = "validate"',
            'base_ref = "main"', 'local_file = "gate.json"',
        ] + [f'{key} = "{value}"' for key, value in extra.items()]
        (self.root / ".engineering-harness.delegation.toml").write_text("\n".join(lines) + "\n", encoding="utf-8")

    def commit(self, message: str) -> str:
        if not (self.root / ".git").exists():
            self.git("init", "-q", "-b", "main")
            self.git("config", "user.email", "fixture@example.invalid")
            self.git("config", "user.name", "Fixture")
            self.git("config", "core.autocrlf", "false")
        ignore = self.root / ".gitignore"
        # Append to the managed fragment file; never overwrite its se-harness block.
        existing = ignore.read_text(encoding="utf-8") if ignore.exists() else ""
        if "gate.json" not in existing:
            ignore.write_text(existing.rstrip("\n") + "\ngate.json\n.engineering-harness.delegation.toml\n*.log\n", encoding="utf-8")
        self.git("add", "-A")
        self.git("commit", "-q", "--allow-empty", "-m", message)
        return self.git("rev-parse", "HEAD")

    def branch(self, name: str = "wo/001") -> None:
        self.git("checkout", "-q", "-b", name)

    def set_gate(self, conclusion: str | None, *, sha: str | None = None) -> None:
        gate = self.root / "gate.json"
        if conclusion is None:
            gate.unlink(missing_ok=True)
            return
        payload = {"sha": sha or self.git("rev-parse", "HEAD"), "conclusion": conclusion, "check_run_id": "4242"}
        gate.write_text(json.dumps(payload), encoding="utf-8")

    def invoke(self, *arguments: str) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = main(list(arguments))
            except SystemExit as exc:
                code = int(exc.code or 0)
        return code, out.getvalue(), err.getvalue()

    def transition(self, target: str, actor: str = DELEGATED_ROLE, *, apply: bool = True) -> tuple[int, dict, str]:
        arguments = ["transition", str(self.root), "--set", f"WO-PRD-001={target}", "--decision", f"WO-PRD-001={actor}", "--json"]
        if apply:
            arguments.append("--apply")
        code, out, err = self.invoke(*arguments)
        return code, json.loads(out) if out.strip().startswith("{") else {}, err

    def status(self) -> str:
        return re.search(r'(?m)^status = "([a-z_]+)"$', self.work_order.read_text(encoding="utf-8")).group(1)

    def blockers(self, result: dict, err: str) -> str:
        return " ".join(result.get("restitution", {}).get("blocked_by", [])) + err


class DelegatedTransitionTests(DelegationFixture):
    def test_green_gate_unlocks_start_and_records_the_gate_evidence(self) -> None:
        # Scenario 1.
        self.configure(); self.declare_class(); self.branch(); self.set_gate("success")
        code, result, err = self.transition("in_progress")
        self.assertEqual(0, code, self.blockers(result, err))
        self.assertEqual("completed", result["operation"]["outcome"])
        self.assertEqual("in_progress", self.status())
        text = self.work_order.read_text(encoding="utf-8")
        self.assertIn(f'decided_by = "{DELEGATED_ROLE}"', text)
        self.assertIn("Delegated DR-WO-START under [delegation] class 'execution'", text)
        self.assertIn("check-run 4242", text)
        self.assertIn(self.git("rev-parse", "HEAD"), text)

    def test_red_or_absent_gate_refuses_without_a_write(self) -> None:
        # Scenario 2 and ECP-DLG-003's other conclusions.
        self.configure(); self.declare_class(); self.branch()
        before = self.work_order.read_bytes()
        for conclusion in ("failure", "neutral", "cancelled", "pending", None):
            with self.subTest(conclusion=conclusion):
                self.set_gate(conclusion)
                code, result, err = self.transition("in_progress")
                self.assertNotEqual(0, code)
                blockers = self.blockers(result, err)
                self.assertIn("WEX-ECP-040", blockers)
                self.assertIn(self.git("rev-parse", "HEAD")[:7], blockers)
                self.assertEqual(before, self.work_order.read_bytes())
        self.set_gate("success", sha="0" * 40)
        code, result, err = self.transition("in_progress")
        self.assertNotEqual(0, code)
        self.assertIn("head not found", self.blockers(result, err))

    def test_the_caller_cannot_assert_the_gate(self) -> None:
        # Scenario 3: no request-side field is consulted; only the configured source decides.
        self.configure(); self.declare_class(); self.branch(); self.set_gate("failure")
        with mock.patch.dict(os.environ, {"GATES_PASSED": "true", "GITHUB_ACTIONS": "true", "GITHUB_TOKEN": "x"}):
            code, result, err = self.transition("in_progress", apply=True)
        self.assertNotEqual(0, code)
        self.assertIn("WEX-ECP-040", self.blockers(result, err))
        self.assertEqual("approved", self.status())

    def test_rights_outside_the_class_are_refused_with_a_green_gate(self) -> None:
        # Scenario 4 and ECP-DLG-007: approve and verify stay human.
        self.configure()
        text = self.work_order.read_text(encoding="utf-8").replace('status = "approved"', 'status = "draft"', 1)
        self.work_order.write_text(text, encoding="utf-8")
        self.declare_class(); self.branch(); self.set_gate("success")
        code, result, err = self.transition("approved")
        self.assertNotEqual(0, code)
        self.assertIn("WEX-ECP-022", self.blockers(result, err))
        self.assertEqual("draft", self.status())
        # DR-VREC-DECIDE with the delegated role: a legal edge, refused by the class.
        write(self.root / "docs/engineering/product/verification-records/VREC-001.md", "\n".join(READY_RECORD))
        write(self.root / "docs/engineering/product/evidence/e.md", "# e\n")
        text = self.work_order.read_text(encoding="utf-8").replace('status = "draft"', 'status = "implemented"', 1)
        self.work_order.write_text(text, encoding="utf-8")
        self.commit("implemented with a ready record"); self.set_gate("success")
        code, out, err = self.invoke(
            "transition", str(self.root), "--set", "VREC-001=verified", "--decision", f"VREC-001={DELEGATED_ROLE}", "--json", "--apply",
        )
        self.assertNotEqual(0, code)
        self.assertIn("WEX-ECP-022", out + err)
        record = (self.root / "docs/engineering/product/verification-records/VREC-001.md").read_text(encoding="utf-8")
        self.assertIn('status = "ready"', record)

    def test_no_class_no_delegation_whatever_the_environment_says(self) -> None:
        # ECP-DLG-006.
        self.configure(); self.commit("base without the class"); self.branch(); self.set_gate("success")
        with mock.patch.dict(os.environ, {"GITHUB_ACTIONS": "true", "GITHUB_TOKEN": "x", "GITHUB_ACTOR": DELEGATED_ROLE}):
            code, result, err = self.transition("in_progress")
        self.assertNotEqual(0, code)
        self.assertIn("WEX-ECP-022", self.blockers(result, err))
        self.assertEqual("approved", self.status())

    def test_a_class_added_on_the_branch_is_not_at_the_base(self) -> None:
        # Security check: the class read for the decision is the base's.
        self.configure(); self.commit("base without the class"); self.branch()
        self.declare_class(at_base=False); self.commit("branch adds the class"); self.set_gate("success")
        code, result, err = self.transition("in_progress")
        self.assertNotEqual(0, code)
        blockers = self.blockers(result, err)
        self.assertIn("WEX-ECP-022", blockers)
        self.assertIn("base", blockers)
        self.assertEqual("approved", self.status())

    def test_delegated_completion_runs_the_handoff_gate_first(self) -> None:
        # ECP-DLG-009: the change set is narrowed by the implementation gate before the CI gate is read.
        self.configure(); self.declare_class(); self.branch(); self.set_gate("success")
        code, result, err = self.transition("in_progress")
        self.assertEqual(0, code, self.blockers(result, err))
        self.commit("started"); self.set_gate("success")
        code, result, err = self.transition("implemented")
        self.assertNotEqual(0, code)
        self.assertNotIn("WEX-ECP-040", self.blockers(result, err))
        self.assertEqual("in_progress", self.status())

    def test_human_route_is_unchanged_on_a_class_bearing_work_order(self) -> None:
        self.configure(); self.declare_class(); self.branch(); self.set_gate("failure")
        code, result, err = self.transition("in_progress", actor="engineering-owner")
        self.assertEqual(0, code, self.blockers(result, err))
        self.assertEqual("in_progress", self.status())
        self.assertNotIn("Delegated", self.work_order.read_text(encoding="utf-8"))


class RestitutionOverlayTests(DelegationFixture):
    def check(self) -> dict:
        code, out, err = self.invoke("check", str(self.root), "--artifact", "WO-PRD-001", "--json")
        return json.loads(out)

    def test_check_tells_the_actor_the_start_is_delegated_when_the_gate_is_green(self) -> None:
        # ECP-DLG-010.
        self.configure(); self.declare_class(); self.branch(); self.set_gate("success")
        result = self.check()
        decision = result["restitution"]["decision_required"]
        self.assertEqual(DELEGATED_ROLE, decision["role"])
        self.assertEqual("DR-WO-START", decision["decision_right"])
        self.assertEqual("success", decision["delegation"]["gate"])
        command = result["restitution"]["command_or_response"]
        self.assertEqual("command", command["kind"])
        self.assertEqual(
            ["harnessctl", "transition", ".", "--set", "WO-PRD-001=in_progress", "--decision", f"WO-PRD-001={DELEGATED_ROLE}", "--apply"],
            command["argv"],
        )

    def test_check_tells_the_actor_to_wait_when_the_gate_is_not_green(self) -> None:
        self.configure(); self.declare_class(); self.branch()
        for conclusion in ("pending", "failure"):
            with self.subTest(conclusion=conclusion):
                self.set_gate(conclusion)
                result = self.check()
                decision = result["restitution"]["decision_required"]
                self.assertEqual(DELEGATED_ROLE, decision["role"])
                self.assertEqual("not passing", decision["delegation"]["gate"])
                command = result["restitution"]["command_or_response"]
                self.assertEqual("response", command["kind"])
                self.assertIn(conclusion, command["value"])
                self.assertIn("validate", command["value"])

    def test_check_names_the_human_without_the_class_or_with_it_only_on_the_branch(self) -> None:
        self.configure(); self.commit("base"); self.branch(); self.set_gate("success")
        restitution = self.check()["restitution"]
        self.assertIsNone(restitution["decision_required"])
        self.assertNotIn(DELEGATED_ROLE, json.dumps(restitution))
        self.declare_class(at_base=False); self.commit("branch adds the class"); self.set_gate("success")
        restitution = self.check()["restitution"]
        self.assertIsNone(restitution["decision_required"])
        self.assertNotIn(DELEGATED_ROLE, json.dumps(restitution))


class DelegatedPreparationTests(DelegationFixture):
    def test_delegated_vrec_prepare_needs_the_class_and_a_green_gate(self) -> None:
        self.configure(); self.declare_class(); self.branch(); self.set_gate("success")
        code, result, err = self.transition("in_progress")
        self.assertEqual(0, code, self.blockers(result, err))
        text = self.work_order.read_text(encoding="utf-8").replace('status = "in_progress"', 'status = "implemented"', 1)
        # The events must agree with the status the test forces.
        event = "\n".join([
            "[[lifecycle_events]]", 'from = "in_progress"', 'to = "implemented"',
            'decided_at = "2099-01-01T00:00:00Z"', 'decided_by = "engineering-owner"', 'reason = "fixture"', "+++",
        ])
        head, _, tail = text.partition("\n+++\n")
        self.work_order.write_text(head + "\n\n" + event + "\n" + tail, encoding="utf-8")
        write(self.root / "docs/engineering/product/evidence/WO-PRD-001/WO-PRD-001-handoff.md", "# evidence\n")
        self.commit("implemented"); self.set_gate("failure")
        arguments = [
            "capture-verification", str(self.root), "--id", "VREC-777", "--work-order", "WO-PRD-001", "--verification", "VER-001",
            "--evidence", "docs/engineering/product/evidence/WO-PRD-001/WO-PRD-001-handoff.md", "--owner", DELEGATED_ROLE,
        ]
        code, out, err = self.invoke(*arguments)
        self.assertNotEqual(0, code)
        self.assertIn("WEX-ECP-040", out + err)
        self.assertFalse((self.root / "docs/engineering/product/verification-records/VREC-777.md").exists())
        self.set_gate("success")
        code, out, err = self.invoke(*arguments)
        self.assertEqual(0, code, out + err)
        record = (self.root / "docs/engineering/product/verification-records/VREC-777.md").read_text(encoding="utf-8")
        self.assertIn(f'prepared_by = "{DELEGATED_ROLE}"', record)
        self.assertIn("Delegated DR-VREC-PREPARE", record)
        self.assertIn("check-run 4242", record)


class ValidatorAndSourceTests(DelegationFixture):
    def validate(self) -> subprocess.CompletedProcess[str]:
        # `validate` runs the managed script as a subprocess, so its output is read from one.
        return subprocess.run(
            [sys.executable, "-m", "se_harness", "validate", str(self.root), "--json"],
            capture_output=True, text=True, check=False,
        )

    def test_validator_refuses_any_other_delegation_table(self) -> None:
        # ECP-DLG-001.
        self.configure()
        cases = {
            "second key": '[delegation]\nclass = "execution"\nscope = "all"\n',
            "other value": '[delegation]\nclass = "full"\n',
        }
        for label, table in cases.items():
            with self.subTest(case=label):
                text = re.sub(r"\[delegation\]\n(?:.*\n)*?\n", "", self.work_order.read_text(encoding="utf-8"))
                self.work_order.write_text(text.replace("[relations]", table + "\n[relations]", 1), encoding="utf-8")
                completed = self.validate()
                self.assertNotEqual(0, completed.returncode)
                self.assertIn("E-ECP-001", completed.stdout + completed.stderr)
        requirement = self.root / "docs/engineering/product/requirements/REQ-001.md"
        text = requirement.read_text(encoding="utf-8").replace("[relations]", '[delegation]\nclass = "execution"\n\n[relations]', 1)
        requirement.write_text(text, encoding="utf-8")
        completed = self.validate()
        self.assertNotEqual(0, completed.returncode)
        self.assertIn("E-ECP-001", completed.stdout + completed.stderr)

    def test_github_checks_source_reads_the_documented_endpoint(self) -> None:
        # ECP-DLG-004 against a stub server; the request shape and the filter are what the test pins.
        seen: list[tuple[str, str | None]] = []
        answers = {"conclusion": "success"}

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self) -> None:  # noqa: N802
                seen.append((self.path, self.headers.get("Authorization")))
                body = json.dumps({"check_runs": [{"id": 99, "name": "validate", "conclusion": answers["conclusion"]}]}).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *_args: object) -> None:
                return

        server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.shutdown)
        configuration = DelegationConfiguration("github-checks", "validate", "owner/name", "main", None)
        sha = "a" * 40
        with mock.patch("se_harness.gate_source.GITHUB_API", f"http://127.0.0.1:{server.server_port}"):
            with mock.patch.dict(os.environ, {"GITHUB_TOKEN": "token-x"}):
                reading = read_gate(self.root, configuration, sha)
            self.assertTrue(reading.passing)
            self.assertEqual("99", reading.check_run_id)
            self.assertEqual((f"/repos/owner/name/commits/{sha}/check-runs?check_name=validate", "Bearer token-x"), seen[-1])
            with mock.patch.dict(os.environ, {}, clear=False):
                os.environ.pop("GITHUB_TOKEN", None)
                read_gate(self.root, configuration, sha)
            self.assertIsNone(seen[-1][1])
            answers["conclusion"] = "failure"
            self.assertFalse(read_gate(self.root, configuration, sha).passing)

    def test_local_file_outside_a_rehearsal_warns(self) -> None:
        self.configure(); self.declare_class(); self.branch(); self.set_gate("success")
        self.environment.stop()
        try:
            code, result, err = self.transition("in_progress")
        finally:
            self.environment.start()
        self.assertEqual(0, code, self.blockers(result, err))
        self.assertIn("W-ECP-005", err)


if __name__ == "__main__":
    unittest.main()
