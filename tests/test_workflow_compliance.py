from __future__ import annotations

import contextlib
import io
import json
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


class WorkflowComplianceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        code, _, error = self.invoke("init", str(self.root), "--project-name", "Compliance Fixture")
        self.assertEqual(0, code, error)
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
