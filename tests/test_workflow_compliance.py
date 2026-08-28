from __future__ import annotations

import contextlib
import io
import json
import subprocess
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

from se_harness.cli import main
from se_harness.preflight import _load_validator_module
from se_harness.workflow_compliance import (
    declared_change_set,
    formal_snapshot_digest,
    normalize_path,
    path_is_admitted,
)
from tests.test_revision_provenance import create_base_chain, formal, write
from tests.fixture_support import standard_repository


class WorkflowComplianceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        standard_repository(self.root, "Compliance Fixture")
        create_base_chain(self.root, work_order_status="in_progress", operating_contract_status="draft")
        work_order = self.root / "docs/engineering/product/work-orders/WO-001.md"
        text = work_order.read_text(encoding="utf-8")
        text = text.replace(
            "[relations]",
            '''[assurance]
commit_bound_verification = "required"
rationale = "The executable fixture requires exact-candidate assurance."
decided_by = "repository-owner"

[execution_scope]
paths = ["src/exact.py", "src/component/", "changes.json"]

[relations]''',
            1,
        )
        work_order.write_text(text, encoding="utf-8")
        (self.root / "src/component").mkdir(parents=True)
        (self.root / "src/exact.py").write_text("exact = True\n", encoding="utf-8")
        (self.root / "src/component/inside.py").write_text("inside = True\n", encoding="utf-8")

    def invoke(self, *arguments: str) -> tuple[int, str, str]:
        output = io.StringIO()
        error = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            code = main(list(arguments))
        return code, output.getvalue(), error.getvalue()

    def check(self, *extra: str) -> tuple[int, dict, str]:
        with (
            mock.patch("se_harness.workflow_compliance._preflight_status", return_value=("pass", "Review preflight is ready.")),
            mock.patch("se_harness.workflow_compliance._review_evidence", return_value=("pass", "Evidence is current.")),
        ):
            code, output, error = self.invoke(
                "check",
                str(self.root),
                "--artifact",
                "WO-001",
                "--checkpoint",
                "handoff",
                *extra,
                "--json",
            )
        return code, json.loads(output), error

    def test_exact_and_component_boundary_scope_matching(self) -> None:
        scope = ("src/exact.py", "src/component/")
        self.assertTrue(path_is_admitted("src/exact.py", scope))
        self.assertTrue(path_is_admitted("src/component/inside.py", scope))
        self.assertFalse(path_is_admitted("src/exact.py.bak", scope))
        self.assertFalse(path_is_admitted("src/component-lookalike/inside.py", scope))

    def test_hostile_and_ambiguous_paths_are_rejected(self) -> None:
        invalid = (
            "../escape.py",
            "/absolute.py",
            "C:/drive.py",
            "src\\alternate.py",
            "src/*.py",
            "src/./dot.py",
            "CON.txt",
            "src/control\n.py",
        )
        for value in invalid:
            with self.subTest(value=value), self.assertRaises(Exception):
                normalize_path(value)
        with self.assertRaisesRegex(Exception, "case-ambiguous"):
            declared_change_set(["src/A.py", "src/a.py"], complete=True)

    def test_candidate_validator_rejects_invalid_work_order_scope(self) -> None:
        work_order = self.root / "docs/engineering/product/work-orders/WO-001.md"
        work_order.write_text(
            work_order.read_text(encoding="utf-8").replace(
                'paths = ["src/exact.py", "src/component/", "changes.json"]',
                'paths = ["../escape.py"]',
            ),
            encoding="utf-8",
        )
        report = _load_validator_module().validate_repository(self.root)
        failures = [item for item in report.errors if item.code == "E020"]
        self.assertEqual(1, len(failures))
        self.assertIn("invalid execution scope path", failures[0].message)

    def test_complete_in_scope_change_set_passes(self) -> None:
        code, result, error = self.check(
            "--changed-path", "src/exact.py",
            "--changed-path", "src/component/inside.py",
            "--changes-complete",
        )
        self.assertEqual(0, code, error)
        self.assertEqual("completed", result["operation"]["outcome"])
        self.assertEqual("pass", result["compliance"]["status"])
        self.assertEqual("selected", result["scope"]["mode"])
        self.assertEqual("PROC-WO-IMPLEMENT", result["procedure"]["id"])
        self.assertEqual("STEP-WO-IMPLEMENT-DECIDE", result["procedure"]["current_step"])

    def test_start_checkpoint_resolves_exact_start_decision(self) -> None:
        work_order = self.root / "docs/engineering/product/work-orders/WO-001.md"
        work_order.write_text(
            work_order.read_text(encoding="utf-8").replace(
                'status = "in_progress"', 'status = "approved"', 1
            ),
            encoding="utf-8",
        )
        with mock.patch(
            "se_harness.workflow_compliance._preflight_status",
            return_value=("pass", "Start preflight is ready."),
        ):
            code, output, error = self.invoke(
                "check", str(self.root), "--artifact", "WO-001", "--checkpoint", "start", "--json"
            )
        self.assertEqual(0, code, error)
        result = json.loads(output)
        self.assertEqual("PROC-WO-START", result["procedure"]["id"])
        self.assertEqual("STEP-WO-START-DECIDE", result["procedure"]["current_step"])
        self.assertEqual("DR-WO-START", result["restitution"]["decision_required"]["decision_right"])
        self.assertEqual(
            {"kind": "response", "value": "Start WO-001 implementation."},
            result["restitution"]["command_or_response"],
        )

    def test_pre_action_requires_selected_procedure(self) -> None:
        code, output, _ = self.invoke(
            "check", str(self.root), "--artifact", "WO-001", "--checkpoint", "pre-action", "--json"
        )
        self.assertEqual(1, code)
        self.assertIn("--procedure is required", output)
        code, output, _ = self.invoke(
            "check", str(self.root), "--artifact", "WO-001", "--checkpoint", "pre-action",
            "--procedure", "PROC-WO-START", "--json",
        )
        self.assertEqual(1, code)
        self.assertIn("not selected by workflow rule", output)

    def test_missing_completeness_is_not_assessable_and_blocks_handoff(self) -> None:
        code, result, _ = self.check("--changed-path", "src/exact.py")
        self.assertEqual(1, code)
        self.assertEqual("blocked", result["operation"]["outcome"])
        statuses = {
            predicate["id"]: predicate["status"]
            for gate in result["compliance"]["gates"]
            for predicate in gate["predicates"]
        }
        self.assertEqual("not_assessable", statuses["QGP-G4I-COMPLETE"])
        self.assertEqual("not_assessable", statuses["QGP-G4I-PATHS"])

    def test_one_out_of_scope_path_fails_without_writes(self) -> None:
        work_order = self.root / "docs/engineering/product/work-orders/WO-001.md"
        before = work_order.read_bytes()
        code, result, _ = self.check(
            "--changed-path", "src/component-lookalike/inside.py",
            "--changes-complete",
        )
        self.assertEqual(1, code)
        self.assertEqual("fail", result["compliance"]["status"])
        self.assertIn("WEX201", json.dumps(result["restitution"]["blocked_by"]))
        self.assertEqual(before, work_order.read_bytes())

    def test_manifest_and_repeated_arguments_have_equivalent_scope(self) -> None:
        manifest = self.root / "changes.json"
        manifest.write_text(
            json.dumps(
                {
                    "schema": "se-harness-change-set-v1",
                    "complete": True,
                    "paths": ["src/exact.py", "src/component/inside.py"],
                }
            ),
            encoding="utf-8",
        )
        argument_code, argument_result, _ = self.check(
            "--changed-path", "src/exact.py",
            "--changed-path", "src/component/inside.py",
            "--changes-complete",
        )
        manifest_code, manifest_result, _ = self.check("--change-manifest", "changes.json")
        self.assertEqual((0, 0), (argument_code, manifest_code))
        self.assertEqual(argument_result["scope"]["changed_paths"], manifest_result["scope"]["changed_paths"])
        self.assertEqual(argument_result["compliance"]["status"], manifest_result["compliance"]["status"])

    def test_manifest_unknown_key_fails_closed(self) -> None:
        (self.root / "changes.json").write_text(
            '{"schema":"se-harness-change-set-v1","complete":true,"paths":[],"extra":1}',
            encoding="utf-8",
        )
        code, output, _ = self.invoke(
            "check", str(self.root), "--artifact", "WO-001", "--checkpoint", "handoff",
            "--change-manifest", "changes.json", "--json",
        )
        self.assertEqual(1, code)
        result = json.loads(output)
        self.assertEqual("blocked", result["operation"]["outcome"])
        self.assertNotIn("extra", result["scope"])

    def test_evidence_freshness_requires_artifact_checkpoint_and_snapshot(self) -> None:
        evidence = self.root / "docs/engineering/product/evidence/WO-001-verification.md"
        evidence.write_text(
            "artifact: WO-001\ncheckpoint: handoff\nformal_snapshot_sha256: " + "0" * 64 + "\n",
            encoding="utf-8",
        )
        with mock.patch(
            "se_harness.workflow_compliance._preflight_status",
            return_value=("pass", "Review preflight is ready."),
        ):
            code, output, _ = self.invoke(
                "check", str(self.root), "--artifact", "WO-001", "--checkpoint", "handoff",
                "--changes-complete", "--json",
            )
        self.assertEqual(1, code)
        stale = json.loads(output)
        statuses = {
            predicate["id"]: predicate["status"]
            for gate in stale["compliance"]["gates"]
            for predicate in gate["predicates"]
        }
        self.assertEqual("not_assessable", statuses["QGP-G4I-EVIDENCE"])

        report = _load_validator_module().validate_repository(self.root)
        digest = formal_snapshot_digest(self.root, report.artifacts)
        evidence.write_text(
            f"artifact: WO-001\ncheckpoint: handoff\nformal_snapshot_sha256: {digest}\n",
            encoding="utf-8",
        )
        with mock.patch(
            "se_harness.workflow_compliance._preflight_status",
            return_value=("pass", "Review preflight is ready."),
        ):
            code, output, error = self.invoke(
                "check", str(self.root), "--artifact", "WO-001", "--checkpoint", "handoff",
                "--changes-complete", "--json",
            )
        self.assertEqual(0, code, error)
        self.assertEqual("pass", json.loads(output)["compliance"]["status"])

    def test_unrelated_diagnostics_are_counted_without_details(self) -> None:
        write(
            self.root / "docs/engineering/unrelated/INT-999.md",
            formal("INT-999", "intent", "draft", {}),
        )
        code, result, _ = self.check("--changes-complete")
        self.assertEqual(0, code)
        self.assertGreaterEqual(result["findings"]["unrelated_count"], 1)
        encoded = json.dumps(result)
        self.assertNotIn("completed legacy architecture", encoded)
        self.assertNotIn("ARCH-001.md", encoded)

    def test_ten_thousand_path_scope_evaluation_is_bounded(self) -> None:
        paths = [f"src/component/{index:05d}.py" for index in range(10_000)]
        started = time.perf_counter()
        admitted = [path for path in paths if path_is_admitted(path, ("src/component/",))]
        duration = time.perf_counter() - started
        self.assertEqual(paths, admitted)
        self.assertLess(duration, 5.0)


if __name__ == "__main__":
    unittest.main()


class GitDerivedChangeSetTests(WorkflowComplianceTests):
    """REQ-ECP-002 / ECP-CHG-001 to -007: the change set read from Git, not typed."""

    def git(self, *arguments: str) -> str:
        completed = subprocess.run(
            ["git", "-C", str(self.root), *arguments], capture_output=True, text=True, check=True,
        )
        return completed.stdout

    def commit_base(self) -> str:
        self.git("init", "-q")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "user.name", "Fixture")
        self.git("config", "core.autocrlf", "false")
        (self.root / ".gitignore").write_text("*.log\n", encoding="utf-8")
        (self.root / "src/component/renamed_from.py").write_text("old = True\n", encoding="utf-8")
        (self.root / "src/component/deleted.py").write_text("gone = True\n", encoding="utf-8")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "base")
        return self.git("rev-parse", "HEAD").strip()

    def check_from_git(self, base: str) -> tuple[int, dict, str]:
        return self.check("--from-git", base, "--json")

    def test_from_git_derives_modified_deleted_renamed_and_untracked_paths_and_ignores_ignored(self) -> None:
        base = self.commit_base()
        (self.root / "src/exact.py").write_text("exact = False\n", encoding="utf-8")
        (self.root / "src/component/deleted.py").unlink()
        (self.root / "src/component/renamed_from.py").rename(self.root / "src/component/renamed_to.py")
        (self.root / "src/component/new.py").write_text("new = True\n", encoding="utf-8")
        (self.root / "src/component/noise.log").write_text("ignored\n", encoding="utf-8")
        code, result, error = self.check_from_git(base)
        self.assertEqual(0, code, error)
        self.assertEqual(
            [
                "src/component/deleted.py",
                "src/component/new.py",
                "src/component/renamed_from.py",
                "src/component/renamed_to.py",
                "src/exact.py",
            ],
            result["scope"]["changed_paths"],
        )
        self.assertTrue(result["scope"]["change_set_complete"])
        self.assertEqual("git", result["compliance"]["change_set_source"])
        self.assertEqual("completed", result["operation"]["outcome"])

    def test_from_git_change_set_is_scope_checked_and_binds_the_digest(self) -> None:
        base = self.commit_base()
        (self.root / "README-outside.md").write_text("outside\n", encoding="utf-8")
        code, result, error = self.check_from_git(base)
        self.assertEqual(1, code, error)
        self.assertIn("README-outside.md", result["scope"]["changed_paths"])
        self.assertTrue(any("WEX201" in item and "README-outside.md" in item for item in result["restitution"]["blocked_by"]))
        from se_harness.workflow_result import restitution_digest

        self.assertEqual(restitution_digest(result), result["result_sha256"])

    def test_the_selected_work_orders_own_file_is_admitted_by_construction(self) -> None:
        # ECP-CHG-007: lifecycle transitions write the work order; a Git diff always carries it.
        base = self.commit_base()
        work_order = self.root / "docs/engineering/product/work-orders/WO-001.md"
        work_order.write_text(work_order.read_text(encoding="utf-8") + "\n<!-- transitioned -->\n", encoding="utf-8")
        code, result, error = self.check_from_git(base)
        self.assertEqual(0, code, error)
        self.assertIn("docs/engineering/product/work-orders/WO-001.md", result["scope"]["changed_paths"])
        self.assertNotIn("docs/engineering/product/work-orders/WO-001.md", result["scope"]["declared_paths"])
        (self.root / "docs/engineering/product/work-orders/WO-002.md").write_text("+++\nid = \"WO-002\"\n+++\n", encoding="utf-8")
        code, result, error = self.check_from_git(base)
        self.assertEqual(1, code, error)
        self.assertTrue(any("WO-002.md" in item for item in result["restitution"]["blocked_by"]))

    def test_from_git_is_exclusive_with_typed_paths_and_fails_closed_on_a_bad_base(self) -> None:
        base = self.commit_base()
        code, output, error = self.invoke(
            "check", str(self.root), "--artifact", "WO-001", "--checkpoint", "handoff",
            "--from-git", base, "--changed-path", "src/exact.py", "--changes-complete",
        )
        self.assertEqual(2, code)
        self.assertIn("WEX-ECP-002", error)
        code, result, error = self.check_from_git("no-such-ref")
        self.assertEqual(1, code, error)
        self.assertEqual("blocked", result["operation"]["outcome"])
        self.assertTrue(result["restitution"]["blocked_by"][0].startswith("WEX-ECP-003"))
        self.assertIn("no-such-ref", result["restitution"]["blocked_by"][0])
        self.assertEqual(
            ["harnessctl", "next", ".", "--artifact", "WO-001"],
            result["restitution"]["command_or_response"]["argv"],
        )
        for gate in result["compliance"]["gates"]:
            for predicate in gate["predicates"]:
                self.assertNotEqual("pass", predicate["status"])

    def test_from_git_outside_a_checkout_blocks_with_wex_ecp_003(self) -> None:
        code, result, error = self.check_from_git("HEAD")
        self.assertEqual(1, code, error)
        self.assertTrue(result["restitution"]["blocked_by"][0].startswith("WEX-ECP-003"))
        self.assertIn("not a Git checkout", result["restitution"]["blocked_by"][0])


class EvidencePacketTests(GitDerivedChangeSetTests):
    """REQ-ECP-003 / ECP-EVD-001 to -007 and the retained handoff result (ECP-PRB-002 amended)."""

    PACKET = "docs/engineering/product/evidence/WO-001/WO-001-handoff.md"

    def check_real(self, *extra: str) -> tuple[int, dict, str]:
        # The evidence predicate is the subject here: only review preflight is stubbed.
        with mock.patch("se_harness.workflow_compliance._preflight_status", return_value=("pass", "Review preflight is ready.")):
            code, output, error = self.invoke("check", str(self.root), "--artifact", "WO-001", "--checkpoint", "handoff", *extra)
        return code, json.loads(output), error

    def evidence(self, *extra: str) -> tuple[int, dict, str]:
        code, output, error = self.invoke(
            "evidence", str(self.root), "--artifact", "WO-001", "--checkpoint", "handoff", "--json", *extra
        )
        return code, json.loads(output), error

    def test_evidence_writes_a_packet_with_a_machine_header_and_rebinds_only_the_header(self) -> None:
        from se_harness.workflow_compliance import parse_evidence_header

        code, result, error = self.evidence("--rebound-at", "2026-08-28T20:00:00Z")
        self.assertEqual(0, code, error)
        self.assertEqual("evidence", result["operation"]["kind"])
        self.assertEqual([{"id": "WO-001", "path": self.PACKET, "fields": ["artifact", "checkpoint", "formal_snapshot_sha256", "rebound_at"]}], result["mutation"]["writes"])
        packet = self.root / self.PACKET
        data = packet.read_bytes()
        self.assertTrue(data.startswith(b"```toml\nartifact = \"WO-001\"\ncheckpoint = \"handoff\"\n"))
        self.assertNotIn(b"\r", data)
        header, body = parse_evidence_header(data)
        self.assertEqual("2026-08-28T20:00:00Z", header["rebound_at"])
        self.assertIn(b"Retained by `harnessctl evidence`; body content is owner-authored.", body)
        owner_body = body + "\nOwner paragraph with \u00e9 and a trailing space \n".encode("utf-8")
        packet.write_bytes(data[: len(data) - len(body)] + owner_body)
        # move the formal snapshot, then rebind: the header changes, the body does not
        work_order = self.root / "docs/engineering/product/work-orders/WO-001.md"
        work_order.write_text(work_order.read_text(encoding="utf-8") + "\n<!-- moved -->\n", encoding="utf-8")
        code, result, error = self.evidence("--rebound-at", "2026-08-28T20:05:00Z")
        self.assertEqual(0, code, error)
        header_after, body_after = parse_evidence_header(packet.read_bytes())
        self.assertEqual(owner_body, body_after)
        self.assertNotEqual(header["formal_snapshot_sha256"], header_after["formal_snapshot_sha256"])
        self.assertEqual("2026-08-28T20:05:00Z", header_after["rebound_at"])
        self.assertIn("Rebound", result["restitution"]["done"][0])

    def test_evidence_refuses_a_tampered_or_foreign_packet_and_writes_nothing(self) -> None:
        self.evidence("--rebound-at", "2026-08-28T20:00:00Z")
        packet = self.root / self.PACKET
        original = packet.read_bytes()
        for tampered, needle in (
            (b"# no header\n" + original, "no evidence packet header"),
            (original.replace(b'artifact = "WO-001"', b'artifact = "WO-009"', 1), "is the packet of WO-009"),
            (b"```toml\nartifact = \n```\n", "not valid TOML"),
            (b"```toml\nartifact = \"WO-001\"\ncheckpoint = \"handoff\"\nextra = 1\n```\n", "must carry exactly"),
        ):
            with self.subTest(needle=needle):
                packet.write_bytes(tampered)
                code, result, error = self.evidence()
                self.assertEqual(1, code, error)
                self.assertTrue(result["restitution"]["blocked_by"][0].startswith("WEX-ECP-010"), result["restitution"]["blocked_by"])
                self.assertIn(needle, result["restitution"]["blocked_by"][0])
                self.assertEqual(tampered, packet.read_bytes())
                self.assertEqual([], result["mutation"]["writes"])

    def test_evidence_refuses_a_converting_attribute_and_a_different_selected_work_order(self) -> None:
        self.commit_base()
        (self.root / ".gitattributes").write_text("*.md text eol=crlf\n", encoding="utf-8")
        code, result, error = self.evidence()
        self.assertEqual(1, code, error)
        self.assertTrue(result["restitution"]["blocked_by"][0].startswith("WEX-ECP-011"))
        self.assertFalse((self.root / self.PACKET).exists())
        (self.root / ".gitattributes").write_text("*.md text eol=lf\n", encoding="utf-8")
        self.assertEqual(0, self.evidence()[0])
        second = self.root / "docs/engineering/product/work-orders/WO-002.md"
        second.write_text(
            (self.root / "docs/engineering/product/work-orders/WO-001.md").read_text(encoding="utf-8").replace("WO-001", "WO-002").replace('status = "in_progress"', 'status = "approved"'),
            encoding="utf-8",
        )
        (self.root / "docs/engineering/product/work-orders/WO-001.md").write_text(
            (self.root / "docs/engineering/product/work-orders/WO-001.md").read_text(encoding="utf-8").replace('status = "in_progress"', 'status = "approved"', 1),
            encoding="utf-8",
        )
        second.write_text(second.read_text(encoding="utf-8").replace('status = "approved"', 'status = "in_progress"', 1), encoding="utf-8")
        code, output, error = self.invoke("evidence", str(self.root), "--artifact", "WO-001", "--checkpoint", "handoff", "--json")
        self.assertEqual(1, code, error)
        self.assertIn("WEX-ECP-012: the working tree selects WO-002", json.loads(output)["restitution"]["blocked_by"][0])

    def test_the_predicate_reads_the_header_never_substrings_and_keeps_the_grace_for_legacy_packets(self) -> None:
        from se_harness.workflow_compliance import formal_snapshot_digest

        self.evidence("--rebound-at", "2026-08-28T20:00:00Z")
        code, result, error = self.check_real("--changes-complete", "--json")
        self.assertEqual(0, code, error)
        self.assertNotIn("W-ECP-002", json.dumps(result))
        packet = self.root / self.PACKET
        data = packet.read_bytes()
        # a substring copy of the binding inside the body proves nothing once a header exists
        report = _load_validator_module().validate_repository(self.root)
        digest = formal_snapshot_digest(self.root, report.artifacts)
        packet.write_bytes(data.replace(digest.encode("utf-8"), b"0" * 64, 1) + f"\nartifact: WO-001\ncheckpoint: handoff\nformal_snapshot_sha256: {digest}\n".encode("utf-8"))
        code, result, error = self.check_real("--changes-complete", "--json")
        self.assertEqual(1, code, error)
        statuses = {p["id"]: p["status"] for g in result["compliance"]["gates"] for p in g["predicates"]}
        self.assertEqual("not_assessable", statuses["QGP-G4I-EVIDENCE"])
        # a legacy packet with no header still passes for one release, named by W-ECP-002
        packet.write_text(f"# legacy\n\nartifact: WO-001\ncheckpoint: handoff\nformal_snapshot_sha256: {digest}\n", encoding="utf-8")
        code, result, error = self.check_real("--changes-complete", "--json")
        self.assertEqual(0, code, error)
        messages = [p["message"] for g in result["compliance"]["gates"] for p in g["predicates"] if p["id"] == "QGP-G4I-EVIDENCE"]
        self.assertIn("W-ECP-002", messages[0])
        self.assertIn("harnessctl evidence . --artifact WO-001 --checkpoint handoff", messages[0])

    def check_from_git_real(self, base: str) -> tuple[int, dict, str]:
        return self.check_real("--from-git", base, "--json")

    def test_a_completed_git_derived_handoff_retains_its_result_in_the_packet_directory(self) -> None:
        base = self.commit_base()
        self.evidence("--rebound-at", "2026-08-28T20:00:00Z")
        (self.root / "src/exact.py").write_text("exact = False\n", encoding="utf-8")
        code, result, error = self.check_from_git_real(base)
        self.assertEqual(0, code, error)
        retained = self.root / "docs/engineering/product/evidence/WO-001/handoff.json"
        self.assertEqual([{"id": "WO-001", "path": "docs/engineering/product/evidence/WO-001/handoff.json", "fields": ["result_sha256"]}], result["mutation"]["writes"])
        stored = json.loads(retained.read_text(encoding="utf-8"))
        self.assertEqual(result["result_sha256"], stored["result_sha256"])
        self.assertNotIn(b"\r", retained.read_bytes())
        # the retained file is harness-written: the next Git-derived check admits it by construction
        code, result, error = self.check_from_git_real(base)
        self.assertEqual(0, code, error)
        self.assertIn("docs/engineering/product/evidence/WO-001/handoff.json", result["scope"]["changed_paths"])
        # a blocked handoff retains nothing
        (self.root / "outside.md").write_text("x\n", encoding="utf-8")
        before = retained.read_bytes()
        code, result, error = self.check_from_git_real(base)
        self.assertEqual(1, code, error)
        self.assertEqual([], result["mutation"]["writes"])
        self.assertEqual(before, retained.read_bytes())

