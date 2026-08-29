from __future__ import annotations

import contextlib
import errno
import re
import io
import json
import sys
import os
import statistics
import tempfile
import time
import tomllib
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from se_harness.cli import main
from se_harness.preflight import _load_validator_module
from se_harness.workflow import PreconditionError, apply_transition, plan_transition, project_selected
from se_harness.workflow_compliance import check_workflow
from tests.mutation_guard_support import trusted_mutation_authority
from tests.test_revision_provenance import create_base_chain, formal, write
from tests.fixture_support import standard_repository


def scale_sizes() -> tuple[int, ...]:
    """REQ-TST-002: the 1,000-artifact size runs only under SE_HARNESS_TEST_SCALE=full."""

    return (100, 500, 1000) if os.environ.get("SE_HARNESS_TEST_SCALE") == "full" else (100, 500)



class WorkflowExecutionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        standard_repository(self.root, "Workflow Fixture")
        lock_path = self.root / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["evaluator"]["archive_name"] = (
            f"se_harness-{lock['tool_version'].replace('-', '_')}-py3-none-any.whl"
        )
        lock["evaluator"]["archive_sha256"] = "a" * 64
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        guard = mock.patch(
            "se_harness.mutation_guard.require_mutation_authority",
            side_effect=trusted_mutation_authority,
        )
        guard.start()
        self.addCleanup(guard.stop)
        create_base_chain(self.root, operating_contract_status="draft")

    def invoke(self, *arguments: str) -> tuple[int, str, str]:
        output = io.StringIO()
        error = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            code = main(list(arguments))
        return code, output.getvalue(), error.getvalue()

    def ready_vrec(self, record_id: str = "VREC-001") -> Path:
        path = self.root / f"docs/engineering/product/verification-records/{record_id}.md"
        content = formal(
            record_id,
            "verification_record",
            "ready",
            {"verifies_work_order": ["WO-001"], "conforms_to": ["VER-001"]},
            f'''commit = "{'a' * 40}"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-20T10:00:00Z"
prepared_by = "quality-owner"
artifact_snapshot_sha256 = "{'b' * 64}"
evidence_paths = ["docs/engineering/product/evidence/WO-001-verification.md"]''',
        ).replace('owners = ["owner"]', 'owners = ["quality-owner"]')
        write(path, content)
        return path

    def ready_rls(self) -> Path:
        path = self.root / "docs/engineering/product/releases/RLS-001.md"
        evaluator_evidence = "docs/engineering/product/evidence/RLS-001-evaluator.json"
        authority = trusted_mutation_authority(
            self.root,
            operation="prepare-release",
            require_archive=True,
        )
        evidence_path = self.root / evaluator_evidence
        evidence_path.parent.mkdir(parents=True, exist_ok=True)
        evidence_path.write_bytes(authority.evidence_bytes)
        content = formal(
            "RLS-001",
            "release_record",
            "ready",
            {
                "satisfies": ["REL-001"],
                "includes_verification": ["VREC-001"],
                "releases_work": ["WO-001"],
            },
            f'''version = "1.0.0"
commit = "{'a' * 40}"
git_object_format = "sha1"
prepared_at = "2026-08-20T11:00:00Z"
prepared_by = "release-owner"
evaluator_evidence_path = "{evaluator_evidence}"
evaluator_evidence_sha256 = "{authority.evidence_sha256}"
tag = "v1.0.0"''',
        ).replace('owners = ["owner"]', 'owners = ["release-owner"]')
        write(path, content)
        return path

    def in_progress_work_order(self) -> Path:
        path = self.root / "docs/engineering/product/work-orders/WO-001.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace('status = "implemented"', 'status = "in_progress"', 1)
        text = text.replace(
            "[relations]",
            '''[assurance]
commit_bound_verification = "required"
rationale = "The workflow change affects persistent governance state and requires exact-candidate assurance."
decided_by = "repository-owner"

[execution_scope]
paths = ["src/"]

[relations]''',
            1,
        )
        path.write_text(text, encoding="utf-8")
        return path

    def bind_handoff_evidence(self, work_order_id: str = "WO-001") -> Path:
        """Retain evidence bound to the handoff checkpoint at the current formal snapshot."""

        from se_harness.workflow import _validation
        from se_harness.workflow_compliance import formal_snapshot_digest

        _, report = _validation(self.root)
        snapshot = formal_snapshot_digest(self.root, report.artifacts)
        path = self.root / f"docs/engineering/product/evidence/{work_order_id}-verification.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        existing = path.read_text(encoding="utf-8") if path.exists() else f"# {work_order_id} evidence\n"
        path.write_text(
            existing + f"\nartifact: {work_order_id}\ncheckpoint: handoff\nformal_snapshot_sha256: {snapshot}\n",
            encoding="utf-8",
        )
        return path

    def test_check_projects_only_selected_governing_chain(self) -> None:
        code, output, error = self.invoke("check", str(self.root), "--artifact", "WO-001", "--json")
        self.assertEqual(0, code, error)
        result = json.loads(output)
        self.assertEqual("completed", result["operation"]["outcome"])
        self.assertEqual(
            ["ADR-001", "ARCH-001", "CAP-001", "INT-001", "REQ-001", "SPEC-001", "VER-001"],
            result["scope"]["governing"],
        )
        self.assertEqual("PROC-WO-PREPARE-VREC", result["restitution"]["next"]["procedure_id"])

    def test_check_emits_schema_two_only_and_refuses_the_retired_option(self) -> None:
        # WO-ECP-005 (REQ-ECP-010, ECP-KRN-001/-002): one result schema; the former
        # --result-schema option is an argument error with either value.
        code, output, error = self.invoke("check", str(self.root), "--artifact", "WO-001", "--json")
        self.assertEqual(0, code, error)
        result = json.loads(output)
        self.assertEqual("se-harness-workflow-result-v2", result["schema"])
        self.assertEqual("selected", result["scope"]["mode"])
        self.assertRegex(result["result_sha256"], r"^[0-9a-f]{64}$")
        self.assertNotIn("WEX-ADS-002", error)

        for value in ("1", "2"):
            with self.subTest(value=value):
                error = io.StringIO()
                with contextlib.redirect_stderr(error), self.assertRaises(SystemExit) as raised:
                    main(["check", str(self.root), "--artifact", "WO-001", "--result-schema", value, "--json"])
                self.assertEqual(2, raised.exception.code)
                self.assertIn("unrecognized arguments: --result-schema", error.getvalue())

        code, human, error = self.invoke("check", str(self.root), "--artifact", "WO-001")
        self.assertEqual(0, code, error)
        self.assertTrue(human.startswith("Outcome\n"))
        self.assertNotIn("Workflow focus", human)

    def test_check_implemented_work_with_ready_vrec_recommends_assurance(self) -> None:
        self.ready_vrec()
        code, output, error = self.invoke(
            "check", str(self.root), "--artifact", "WO-001", "--json"
        )
        self.assertEqual(0, code, error)
        result = json.loads(output)
        self.assertEqual(["VREC-001"], result["scope"]["dependencies"])
        self.assertEqual("PROC-FOCUS-RELATED", result["restitution"]["next"]["procedure_id"])
        self.assertEqual(
            {"kind": "command", "argv": ["harnessctl", "check", ".", "--artifact", "VREC-001"]},
            result["restitution"]["command_or_response"],
        )
        self.assertIn(
            "WO-001 is implemented; VREC-001 is ready.",
            result["restitution"]["current_lifecycle_state"],
        )
        self.assertNotIn("PROC-WO-PREPARE-VREC", json.dumps(result["restitution"]))

    def test_check_implemented_work_with_verified_vrec_recommends_delivery(self) -> None:
        self.ready_vrec()
        code, _, error = self.invoke(
            "transition", str(self.root),
            "--set", "VREC-001=verified",
            "--decision", "VREC-001=quality-owner",
            "--apply",
        )
        self.assertEqual(0, code, error)
        code, output, error = self.invoke(
            "check", str(self.root), "--artifact", "WO-001", "--json"
        )
        self.assertEqual(0, code, error)
        result = json.loads(output)
        self.assertEqual("PROC-DELIVERY-SELECT", result["restitution"]["next"]["procedure_id"])
        self.assertIn(
            "WO-001 is implemented; VREC-001 is verified.",
            result["restitution"]["current_lifecycle_state"],
        )

    def test_human_handoff_emits_alternatives_only_when_declared(self) -> None:
        code, output, error = self.invoke(
            "check", str(self.root), "--artifact", "WO-001"
        )
        self.assertEqual(0, code, error)
        self.assertNotIn("Alternatives", output)

        self.ready_vrec()
        code, output, error = self.invoke(
            "check", str(self.root), "--artifact", "VREC-001"
        )
        self.assertEqual(0, code, error)
        self.assertIn("Alternatives", output)
        self.assertIn("PROC-VREC-REJECT", output)

    def test_check_projects_exact_vrec_scope_without_unrelated_work(self) -> None:
        self.ready_vrec()
        code, output, error = self.invoke(
            "check", str(self.root), "--artifact", "VREC-001", "--json"
        )
        self.assertEqual(0, code, error)
        result = json.loads(output)
        self.assertEqual(
            [
                "ADR-001", "ARCH-001", "CAP-001", "INT-001", "REQ-001",
                "SPEC-001", "VER-001", "WO-001",
            ],
            result["scope"]["governing"],
        )
        self.assertEqual([], result["scope"]["dependencies"])
        self.assertEqual("PROC-VREC-DECIDE", result["restitution"]["next"]["procedure_id"])

    def test_check_projects_exact_rls_scope_without_synchronizing_records(self) -> None:
        vrec = self.ready_vrec()
        code, _, error = self.invoke(
            "transition", str(self.root),
            "--set", "VREC-001=verified",
            "--decision", "VREC-001=quality-owner",
            "--apply",
        )
        self.assertEqual(0, code, error)
        release = self.ready_rls()
        vrec_before = vrec.read_bytes()
        release_before = release.read_bytes()
        code, output, error = self.invoke(
            "check", str(self.root), "--artifact", "RLS-001", "--json"
        )
        self.assertEqual(0, code, error)
        result = json.loads(output)
        self.assertEqual(
            [
                "ADR-001", "ARCH-001", "CAP-001", "INT-001", "REL-001",
                "REQ-001", "SPEC-001", "VER-001", "VREC-001", "WO-001",
            ],
            result["scope"]["governing"],
        )
        self.assertEqual([], result["scope"]["dependencies"])
        self.assertEqual(vrec_before, vrec.read_bytes())
        self.assertEqual(release_before, release.read_bytes())

    def test_check_rejects_a_non_primary_artifact_type(self) -> None:
        code, output, _ = self.invoke(
            "check", str(self.root), "--artifact", "INT-001", "--json"
        )
        self.assertEqual(1, code)
        result = json.loads(output)
        self.assertEqual("blocked", result["operation"]["outcome"])
        self.assertIn("only WO, VREC, or RLS", result["findings"]["scoped_blockers"][0]["message"])
        self.assertEqual("PROC-REMEDIATE", result["restitution"]["next"]["procedure_id"])

    def test_work_order_completion_ignores_only_candidate_distribution_drift(self) -> None:
        path = self.in_progress_work_order()
        distribution_only = SimpleNamespace(
            ready=False,
            diagnostics=[SimpleNamespace(
                code="I001",
                path="distribution:ENGINEERING_HARNESS.md",
                message="differs from distribution template",
            )],
        )
        self.bind_handoff_evidence()
        with mock.patch("se_harness.workflow_compliance.run_preflight", return_value=distribution_only):
            plan = plan_transition(
                self.root,
                {"WO-001": "implemented"},
                {"WO-001": "engineering-owner"},
                {},
            )
        self.assertEqual("completed", plan.result["operation"]["outcome"], plan.result["restitution"]["blocked_by"])
        self.assertIn("no files were written", plan.result["restitution"]["done"][0])
        self.assertEqual("transition", plan.result["compliance"]["checkpoint"])
        self.assertEqual("pass", plan.result["compliance"]["status"])
        self.assertEqual('status = "in_progress"', next(
            line for line in path.read_text(encoding="utf-8").splitlines()
            if line.startswith("status =")
        ))

    def test_work_order_completion_keeps_managed_installation_drift_blocking(self) -> None:
        self.in_progress_work_order()
        managed_failure = SimpleNamespace(
            ready=False,
            diagnostics=[SimpleNamespace(
                code="I001",
                path="managed:ENGINEERING_HARNESS.md",
                message="managed file changed",
            )],
        )
        self.bind_handoff_evidence()
        work_order = self.root / "docs/engineering/product/work-orders/WO-001.md"
        before = work_order.read_bytes()
        with mock.patch("se_harness.workflow_compliance.run_preflight", return_value=managed_failure):
            plan = plan_transition(
                self.root,
                {"WO-001": "implemented"},
                {"WO-001": "engineering-owner"},
                {},
            )
            with self.assertRaises(PreconditionError) as raised:
                plan_transition(
                    self.root,
                    {"WO-001": "implemented"},
                    {"WO-001": "engineering-owner"},
                    {},
                    apply=True,
                )
        # ECP-KRN-004/-008: the plan is blocked, rendered under Blocked by with the
        # refusing predicate's own identifier; an apply fails closed the same way.
        self.assertEqual("blocked", plan.result["operation"]["outcome"])
        self.assertEqual((), plan.writes)
        self.assertEqual(["QGP-G4I-PREFLIGHT: managed file changed"], plan.result["restitution"]["blocked_by"])
        self.assertEqual("QGP-G4I-PREFLIGHT", raised.exception.predicate_id)
        self.assertEqual(before, work_order.read_bytes())

    def test_duplicate_identity_is_a_repository_blocker(self) -> None:
        write(
            self.root / "docs/engineering/duplicate/INT-001.md",
            formal("INT-001", "intent", "approved", {}),
        )
        code, output, _ = self.invoke(
            "check", str(self.root), "--artifact", "WO-001", "--json"
        )
        self.assertEqual(1, code)
        result = json.loads(output)
        self.assertEqual([], result["findings"]["scoped_blockers"])
        self.assertEqual(1, len(result["findings"]["repository_blockers"]))

    def test_case_insensitive_identity_collision_is_a_repository_blocker(self) -> None:
        write(
            self.root / "docs/engineering/collision/wo-001.md",
            formal("wo-001", "work_order", "draft", {}),
        )
        code, output, _ = self.invoke(
            "check", str(self.root), "--artifact", "WO-001", "--json"
        )
        self.assertEqual(1, code)
        result = json.loads(output)
        self.assertEqual([], result["findings"]["scoped_blockers"])
        self.assertIn(
            "not unique under case-insensitive comparison",
            result["findings"]["repository_blockers"][0]["message"],
        )

    def test_path_shaped_and_reserved_artifact_inputs_never_select_a_file(self) -> None:
        path = self.root / "docs/engineering/product/work-orders/WO-001.md"
        before = path.read_bytes()
        for selected in (
            "../WO-001",
            "docs/engineering/product/work-orders/WO-001.md",
            "C:\\outside\\WO-001",
            "CON",
        ):
            with self.subTest(selected=selected):
                code, output, _ = self.invoke(
                    "check", str(self.root), "--artifact", selected, "--json"
                )
                self.assertEqual(1, code)
                self.assertEqual("blocked", json.loads(output)["operation"]["outcome"])
                self.assertEqual(before, path.read_bytes())

    def test_transition_plan_is_read_only_and_apply_changes_only_selected_vrec(self) -> None:
        path = self.ready_vrec()
        before = path.read_bytes()
        work_order = self.root / "docs/engineering/product/work-orders/WO-001.md"
        work_before = work_order.read_bytes()

        arguments = (
            "transition", str(self.root),
            "--set", "VREC-001=verified",
            "--decision", "VREC-001=assurance-owner",
            "--json",
        )
        code, output, error = self.invoke(*arguments)
        self.assertEqual(0, code, error)
        planned = json.loads(output)
        self.assertEqual("se-harness-workflow-result-v2", planned["schema"])
        self.assertEqual("completed", planned["operation"]["outcome"])
        self.assertEqual(["Planned 1 explicit lifecycle transition(s); no files were written."], planned["restitution"]["done"])
        self.assertEqual("PROC-DELIVERY-SELECT", planned["restitution"]["next"]["procedure_id"])
        self.assertEqual(before, path.read_bytes())

        code, output, error = self.invoke(*arguments, "--apply")
        self.assertEqual(0, code, error)
        result = json.loads(output)
        self.assertEqual("completed", result["operation"]["outcome"])
        text = path.read_text(encoding="utf-8")
        self.assertIn('status = "verified"', text)
        self.assertIn('verified_by = "assurance-owner"', text)
        self.assertIn("[[lifecycle_events]]", text)
        self.assertEqual(work_before, work_order.read_bytes())
        self.assertTrue(_load_validator_module().validate_repository(self.root).valid)

    def test_ready_prepared_vrec_can_be_superseded_without_verification_decision_fields(self) -> None:
        source = self.ready_vrec()
        successor = self.ready_vrec("VREC-002")
        code, _, error = self.invoke(
            "transition", str(self.root),
            "--set", "VREC-002=verified",
            "--decision", "VREC-002=quality-owner",
            "--apply",
        )
        self.assertEqual(0, code, error)
        self.assertIn('status = "verified"', successor.read_text(encoding="utf-8"))

        before = source.read_text(encoding="utf-8")
        code, output, error = self.invoke(
            "transition", str(self.root),
            "--set", "VREC-001=superseded",
            "--decision", "VREC-001=quality-owner",
            "--reason", "VREC-001=VREC-002",
            "--apply", "--json",
        )
        self.assertEqual(0, code, error or output)
        self.assertEqual("completed", json.loads(output)["operation"]["outcome"])
        updated = source.read_text(encoding="utf-8")
        self.assertIn('status = "superseded"', updated)
        self.assertIn('prepared_at = "2026-08-20T10:00:00Z"', updated)
        self.assertIn('prepared_by = "quality-owner"', updated)
        self.assertNotIn("verified_at =", updated)
        self.assertNotIn("verified_by =", updated)
        self.assertIn('supersession_authorized_by = "quality-owner"', updated)
        self.assertIn('superseded_by = ["VREC-002"]', updated)
        self.assertIn('reason = "VREC-002"', updated)
        self.assertNotEqual(before, updated)
        self.assertTrue(_load_validator_module().validate_repository(self.root).valid)

    def test_transition_uses_the_same_checkpoint_before_plan_and_apply(self) -> None:
        self.ready_vrec()
        with mock.patch(
            "se_harness.workflow_compliance.ensure_governed_checkpoint"
        ) as checkpoint:
            plan_transition(
                self.root,
                {"VREC-001": "verified"},
                {"VREC-001": "assurance-owner"},
                {},
                apply=True,
            )
        self.assertEqual(2, checkpoint.call_count)

    def test_mutually_dependent_definition_packet_is_validated_and_applied_together(self) -> None:
        base = self.root / "docs/engineering/packet"
        write(base / "intent/INT-PKT-001.md", formal("INT-PKT-001", "intent", "draft", {}))
        write(base / "capabilities/CAP-PKT-001.md", formal("CAP-PKT-001", "capability", "draft", {"derives_from": ["INT-PKT-001"]}))
        write(base / "requirements/REQ-PKT-001.md", formal(
            "REQ-PKT-001", "requirement", "draft", {"derives_from": ["CAP-PKT-001"]},
            'statement = "THE SYSTEM SHALL execute a packet."\nverification_method = "automated-test"',
        ))
        write(base / "specifications/SPEC-PKT-001.md", formal("SPEC-PKT-001", "specification", "draft", {"specifies": ["REQ-PKT-001"]}))
        write(base / "verification/VER-PKT-001.md", formal("VER-PKT-001", "verification", "draft", {"verifies": ["REQ-PKT-001"]}))
        ids = ["INT-PKT-001", "CAP-PKT-001", "REQ-PKT-001", "SPEC-PKT-001", "VER-PKT-001"]
        arguments = ["transition", str(self.root)]
        for artifact_id in ids:
            arguments.extend(["--set", f"{artifact_id}=approved"])
        for artifact_id in ids:
            arguments.extend(["--decision", f"{artifact_id}=definition-owner"])
        arguments.extend(["--apply", "--json"])
        code, output, error = self.invoke(*arguments)
        self.assertEqual(0, code, error)
        self.assertEqual(sorted(ids), json.loads(output)["selection"]["artifacts"])
        for path in base.rglob("*.md"):
            self.assertIn('status = "approved"', path.read_text(encoding="utf-8"))

    def test_rejection_requires_non_empty_reason(self) -> None:
        self.ready_vrec()
        code, output, _ = self.invoke(
            "transition", str(self.root),
            "--set", "VREC-001=rejected",
            "--decision", "VREC-001=assurance-owner",
            "--json",
        )
        self.assertEqual(1, code)
        result = json.loads(output)
        self.assertEqual("blocked", result["operation"]["outcome"])
        self.assertIn("requires --reason", result["findings"]["scoped_blockers"][0]["message"])
        self.assertIn("requires --reason", result["restitution"]["blocked_by"][0])

    def test_atomic_packet_rolls_back_when_second_replace_fails(self) -> None:
        first = self.root / "docs/engineering/product/intent/INT-001.md"
        second = self.root / "docs/engineering/product/capabilities/CAP-001.md"
        originals = {first: first.read_bytes(), second: second.read_bytes()}
        plan = plan_transition(
            self.root,
            {"INT-001": "implemented", "CAP-001": "implemented"},
            {"INT-001": "owner", "CAP-001": "owner"},
            {},
        )
        import se_harness.workflow as workflow

        real_replace = workflow._replace
        calls = 0

        def fail_second(staged: Path, target: Path) -> None:
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("injected replacement failure")
            real_replace(staged, target)

        with mock.patch.object(workflow, "_replace", side_effect=fail_second):
            with self.assertRaisesRegex(Exception, "restored"):
                apply_transition(plan)
        self.assertEqual(originals[first], first.read_bytes())
        self.assertEqual(originals[second], second.read_bytes())
        self.assertEqual([], list(self.root.rglob("*.wex-*")))

    def test_interrupted_staging_leaves_no_write_or_temporary_file(self) -> None:
        path = self.root / "docs/engineering/product/intent/INT-001.md"
        original = path.read_bytes()
        plan = plan_transition(
            self.root,
            {"INT-001": "implemented"},
            {"INT-001": "product-owner"},
            {},
        )
        import se_harness.workflow as workflow

        with mock.patch.object(workflow.os, "fsync", side_effect=OSError("interrupted write")):
            with self.assertRaisesRegex(Exception, "restored"):
                apply_transition(plan)
        self.assertEqual(original, path.read_bytes())
        self.assertEqual([], list(self.root.rglob("*.wex-*")))

    def test_full_disk_staging_failure_leaves_no_write_or_temporary_file(self) -> None:
        path = self.root / "docs/engineering/product/intent/INT-001.md"
        original = path.read_bytes()
        plan = plan_transition(
            self.root,
            {"INT-001": "implemented"},
            {"INT-001": "product-owner"},
            {},
        )
        import se_harness.workflow as workflow

        failure = OSError(errno.ENOSPC, "injected full disk")
        with mock.patch.object(workflow.os, "fsync", side_effect=failure):
            with self.assertRaisesRegex(Exception, "restored"):
                apply_transition(plan)
        self.assertEqual(original, path.read_bytes())
        self.assertEqual([], list(self.root.rglob("*.wex-*")))

    def test_denied_first_replacement_leaves_no_write_or_temporary_file(self) -> None:
        path = self.root / "docs/engineering/product/intent/INT-001.md"
        original = path.read_bytes()
        plan = plan_transition(
            self.root,
            {"INT-001": "implemented"},
            {"INT-001": "product-owner"},
            {},
        )
        import se_harness.workflow as workflow

        with mock.patch.object(workflow, "_replace", side_effect=PermissionError("denied")):
            with self.assertRaisesRegex(Exception, "restored"):
                apply_transition(plan)
        self.assertEqual(original, path.read_bytes())
        self.assertEqual([], list(self.root.rglob("*.wex-*")))

    def test_unprovable_rollback_escalates_and_cleans_temporary_files(self) -> None:
        first = self.root / "docs/engineering/product/intent/INT-001.md"
        second = self.root / "docs/engineering/product/capabilities/CAP-001.md"
        plan = plan_transition(
            self.root,
            {"INT-001": "implemented", "CAP-001": "implemented"},
            {"INT-001": "owner", "CAP-001": "owner"},
            {},
        )
        import se_harness.workflow as workflow

        real_replace = workflow._replace
        calls = 0

        def fail_apply_and_rollback(staged: Path, target: Path) -> None:
            nonlocal calls
            calls += 1
            if calls in {2, 3}:
                raise OSError("injected persistent replacement failure")
            real_replace(staged, target)

        with mock.patch.object(workflow, "_replace", side_effect=fail_apply_and_rollback):
            with self.assertRaisesRegex(Exception, "rollback could not prove restoration"):
                apply_transition(plan)
        self.assertNotEqual(plan.writes[0].original, plan.writes[0].path.read_bytes())
        self.assertEqual(plan.writes[1].original, plan.writes[1].path.read_bytes())
        self.assertEqual([], list(self.root.rglob("*.wex-*")))

    def test_new_ready_record_cannot_contain_decision_timestamp(self) -> None:
        path = self.ready_vrec()
        text = path.read_text(encoding="utf-8")
        path.write_text(text.replace(
            'prepared_by = "quality-owner"',
            'prepared_by = "quality-owner"\nverified_at = "2026-08-20T10:00:00Z"',
        ), encoding="utf-8")
        report = _load_validator_module().validate_repository(self.root)
        self.assertTrue(any("must omit decision field 'verified_at'" in item.message for item in report.errors))

    def test_transition_preserves_bom_crlf_and_body_bytes(self) -> None:
        path = self.ready_vrec()
        original_text = path.read_text(encoding="utf-8")
        path.write_bytes(b"\xef\xbb\xbf" + original_text.replace("\n", "\r\n").encode("utf-8"))
        original = path.read_bytes()
        delimiter = b"+++\r\n"
        body = original.split(delimiter, 2)[2]
        code, _, error = self.invoke(
            "transition", str(self.root),
            "--set", "VREC-001=verified",
            "--decision", "VREC-001=assurance-owner",
            "--apply",
        )
        self.assertEqual(0, code, error)
        updated = path.read_bytes()
        self.assertTrue(updated.startswith(b"\xef\xbb\xbf+++\r\n"))
        self.assertNotIn(b"\n", updated.replace(b"\r\n", b""))
        self.assertEqual(body, updated.split(delimiter, 2)[2])

    def test_release_transition_changes_only_selected_rls(self) -> None:
        vrec = self.ready_vrec()
        code, _, error = self.invoke(
            "transition", str(self.root),
            "--set", "VREC-001=verified",
            "--decision", "VREC-001=quality-owner",
            "--apply",
        )
        self.assertEqual(0, code, error)
        release = self.ready_rls()
        vrec_before = vrec.read_bytes()
        work = self.root / "docs/engineering/product/work-orders/WO-001.md"
        work_before = work.read_bytes()
        code, output, error = self.invoke(
            "transition", str(self.root),
            "--set", "RLS-001=released",
            "--decision", "RLS-001=release-owner",
            "--apply", "--json",
        )
        self.assertEqual(0, code, error)
        self.assertEqual("completed", json.loads(output)["operation"]["outcome"])
        release_text = release.read_text(encoding="utf-8")
        self.assertIn('status = "released"', release_text)
        self.assertIn('authorized_by = "release-owner"', release_text)
        self.assertEqual(vrec_before, vrec.read_bytes())
        self.assertEqual(work_before, work.read_bytes())

    def test_repeated_plans_have_byte_identical_json_and_no_timestamp(self) -> None:
        arguments = (
            "transition", str(self.root),
            "--set", "INT-001=implemented",
            "--decision", "INT-001=product-owner",
            "--json",
        )
        first = self.invoke(*arguments)
        second = self.invoke(*arguments)
        self.assertEqual(0, first[0], first[2])
        self.assertEqual(first[1], second[1])
        self.assertNotIn("9999-12-31", first[1])

    def test_plan_after_existing_lifecycle_event_remains_read_only(self) -> None:
        path = self.root / "docs/engineering/product/intent/INT-001.md"
        code, _, error = self.invoke(
            "transition", str(self.root),
            "--set", "INT-001=implemented",
            "--decision", "INT-001=product-owner",
            "--apply",
        )
        self.assertEqual(0, code, error)
        implemented = path.read_bytes()
        # Implemented is terminal; use a newly activated definition to exercise
        # a second edge without changing the plan's read-only property.
        target = self.root / "docs/engineering/product/intent/INT-002.md"
        write(target, formal("INT-002", "intent", "draft", {}))
        code, _, error = self.invoke(
            "transition", str(self.root),
            "--set", "INT-002=approved",
            "--decision", "INT-002=product-owner",
            "--apply",
        )
        self.assertEqual(0, code, error)
        approved = target.read_bytes()
        code, output, error = self.invoke(
            "transition", str(self.root),
            "--set", "INT-002=implemented",
            "--decision", "INT-002=product-owner",
            "--json",
        )
        self.assertEqual(0, code, error)
        planned = json.loads(output)
        self.assertEqual("completed", planned["operation"]["outcome"])
        self.assertEqual(["Planned 1 explicit lifecycle transition(s); no files were written."], planned["restitution"]["done"])
        self.assertEqual(approved, target.read_bytes())
        self.assertEqual(implemented, path.read_bytes())

    def test_stale_input_invalidates_plan_without_overwrite(self) -> None:
        path = self.root / "docs/engineering/product/intent/INT-001.md"
        plan = plan_transition(
            self.root,
            {"INT-001": "implemented"},
            {"INT-001": "product-owner"},
            {},
        )
        path.write_bytes(path.read_bytes() + b"\nconcurrent owner note\n")
        changed = path.read_bytes()
        with self.assertRaisesRegex(Exception, "stale transition plan"):
            apply_transition(plan)
        self.assertEqual(changed, path.read_bytes())

    def test_stale_unselected_graph_input_invalidates_plan_without_overwrite(self) -> None:
        selected = self.root / "docs/engineering/product/intent/INT-001.md"
        dependency = self.root / "docs/engineering/product/capabilities/CAP-001.md"
        selected_before = selected.read_bytes()
        plan = plan_transition(
            self.root,
            {"INT-001": "implemented"},
            {"INT-001": "product-owner"},
            {},
        )
        dependency.write_bytes(dependency.read_bytes() + b"\nconcurrent owner note\n")
        changed = dependency.read_bytes()
        with self.assertRaisesRegex(Exception, "stale transition plan"):
            apply_transition(plan)
        self.assertEqual(selected_before, selected.read_bytes())
        self.assertEqual(changed, dependency.read_bytes())

    def test_change_during_packet_apply_rolls_back_earlier_replacements(self) -> None:
        plan = plan_transition(
            self.root,
            {"INT-001": "implemented", "CAP-001": "implemented"},
            {"INT-001": "owner", "CAP-001": "owner"},
            {},
        )
        first, second = plan.writes
        concurrent = second.original + b"\nconcurrent owner note\n"
        import se_harness.workflow as workflow

        real_replace = workflow._replace
        calls = 0

        def edit_second_after_first_check(staged: Path, target: Path) -> None:
            nonlocal calls
            calls += 1
            if calls == 1:
                second.path.write_bytes(concurrent)
            real_replace(staged, target)

        with mock.patch.object(workflow, "_replace", side_effect=edit_second_after_first_check):
            with self.assertRaisesRegex(Exception, "restored"):
                apply_transition(plan)
        self.assertEqual(first.original, first.path.read_bytes())
        self.assertEqual(concurrent, second.path.read_bytes())
        self.assertEqual([], list(self.root.rglob("*.wex-*")))

    def test_control_characters_in_actor_are_rejected_as_data(self) -> None:
        path = self.ready_vrec()
        before = path.read_bytes()
        code, output, _ = self.invoke(
            "transition", str(self.root),
            "--set", "VREC-001=verified",
            "--decision", "VREC-001=assurance\nowner",
            "--json",
        )
        self.assertEqual(1, code)
        self.assertIn("single-line text", output)
        self.assertEqual(before, path.read_bytes())

    def test_hostile_actor_and_reason_are_encoded_as_toml_data(self) -> None:
        path = self.ready_vrec()
        actor = 'assurance-owner "{json}" $() ; #'
        reason = '"] # {format} [table] $HOME $(command) ;'
        code, _, error = self.invoke(
            "transition", str(self.root),
            "--set", "VREC-001=rejected",
            "--decision", f"VREC-001={actor}",
            "--reason", f"VREC-001={reason}",
            "--apply",
        )
        self.assertEqual(0, code, error)
        document = path.read_text(encoding="utf-8")
        front_matter = document.split("+++", 2)[1]
        metadata = tomllib.loads(front_matter)
        self.assertEqual(actor, metadata["rejected_by"])
        self.assertEqual(reason, metadata["rejection_reason"])
        self.assertEqual(actor, metadata["lifecycle_events"][-1]["decided_by"])
        self.assertEqual(reason, metadata["lifecycle_events"][-1]["reason"])

    def test_symlinked_artifact_is_rejected_without_touching_target(self) -> None:
        path = self.root / "docs/engineering/product/intent/INT-001.md"
        original = path.read_bytes()
        outside = Path(self.temporary.name + "-outside.md")
        self.addCleanup(outside.unlink, missing_ok=True)
        outside.write_bytes(original)
        path.unlink()
        try:
            path.symlink_to(outside)
        except OSError as exc:
            self.skipTest(f"file symlinks unavailable: {exc}")
        code, output, _ = self.invoke(
            "transition", str(self.root),
            "--set", "INT-001=implemented",
            "--decision", "INT-001=product-owner",
            "--apply", "--json",
        )
        self.assertEqual(1, code)
        self.assertIn("refusing to replace a symlink", output)
        self.assertEqual(original, outside.read_bytes())

    def test_agent_host_marker_does_not_change_canonical_result(self) -> None:
        fixture_path = Path(__file__).parent / "fixtures/workflow_execution/scenarios.json"
        scenario = json.loads(fixture_path.read_text(encoding="utf-8"))["scenarios"][0]
        observed: list[str] = []
        for agent_host in scenario["agent_hosts"]:
            with mock.patch.dict(os.environ, {"SE_HARNESS_AGENT_HOST": agent_host}):
                code, output, error = self.invoke(
                    "check", str(self.root),
                    "--artifact", scenario["artifact"],
                    "--json",
                )
            self.assertEqual(0, code, error)
            result = json.loads(output)
            self.assertEqual(scenario["expected"]["selection"], result["selection"])
            self.assertEqual(scenario["expected"]["scope"], result["scope"])
            self.assertEqual(scenario["expected"]["state"], result["state"])
            for key, expected in scenario["expected"]["restitution"].items():
                self.assertEqual(expected, result["restitution"][key], key)
            observed.append(output)
        self.assertEqual(1, len(set(observed)))

    def test_human_output_exposes_the_same_fixture_handoff_semantics(self) -> None:
        fixture_path = Path(__file__).parent / "fixtures/workflow_execution/scenarios.json"
        scenario = json.loads(fixture_path.read_text(encoding="utf-8"))["scenarios"][0]
        json_code, json_output, json_error = self.invoke(
            "check", str(self.root), "--artifact", scenario["artifact"], "--json"
        )
        human_code, human_output, human_error = self.invoke(
            "check", str(self.root), "--artifact", scenario["artifact"]
        )
        self.assertEqual(0, json_code, json_error)
        self.assertEqual(0, human_code, human_error)
        restitution = json.loads(json_output)["restitution"]
        for value in restitution["done"] + restitution["current_lifecycle_state"]:
            self.assertIn(value, human_output)
        self.assertIn(restitution["next"]["action"], human_output)
        self.assertIn(restitution["next"]["procedure_id"], human_output)
        self.assertIn(restitution["command_or_response"]["value"], human_output)

    def test_projection_and_planning_scale_to_one_thousand_artifacts(self) -> None:
        validator = _load_validator_module()
        measurements: list[tuple[int, float, float, float]] = []

        def median_runtime(operation: object) -> tuple[float, object]:
            durations: list[float] = []
            value: object = None
            for _ in range(3):
                started = time.perf_counter()
                value = operation()  # type: ignore[operator]
                durations.append(time.perf_counter() - started)
            return statistics.median(durations), value

        next_id = 1
        for target_count in scale_sizes():
            if target_count == 1000 and os.environ.get("SE_HARNESS_TEST_SCALE") != "full":
                with self.subTest(target_count=target_count):
                    self.skipTest("the 1,000-artifact size runs with SE_HARNESS_TEST_SCALE=full")
                continue
            report = validator.validate_repository(self.root)
            additions = target_count - len(report.artifacts)
            self.assertGreaterEqual(additions, 0)
            for _ in range(additions):
                artifact_id = f"INT-SCL-{next_id:03d}"
                write(
                    self.root / f"docs/engineering/scale/intent/{artifact_id}.md",
                    formal(artifact_id, "intent", "draft", {}),
                )
                next_id += 1
            report = validator.validate_repository(self.root)
            self.assertEqual(target_count, len(report.artifacts))

            validation_seconds, validated = median_runtime(
                lambda: validator.validate_repository(self.root)
            )
            self.assertTrue(validated.valid)

            focus_seconds, result = median_runtime(lambda: project_selected(self.root, "WO-001"))
            self.assertEqual("completed", result["operation"]["outcome"])

            plan_seconds, _ = median_runtime(
                lambda: plan_transition(
                    self.root,
                    {"INT-001": "implemented"},
                    {"INT-001": "product-owner"},
                    {},
                )
            )
            measurements.append(
                (target_count, validation_seconds, focus_seconds, plan_seconds)
            )
            for duration in (validation_seconds, focus_seconds, plan_seconds):
                self.assertLess(duration, 30.0)

        for count, validation_seconds, focus_seconds, plan_seconds in measurements:
            print(
                f"WEX_SCALE artifacts={count} validation={validation_seconds:.6f}s "
                f"focus={focus_seconds:.6f}s plan={plan_seconds:.6f}s"
            )


if __name__ == "__main__":
    unittest.main()


class AgentDirectiveSurfaceTests(WorkflowExecutionTests):
    """Evidence for REQ-ADS-001, REQ-ADS-002, REQ-ADS-003, REQ-ADS-004, and REQ-ADS-005."""

    EVALUATED = ["harnessctl", "check", ".", "--artifact", "{artifact_id}", "--checkpoint"]

    def test_every_gated_command_step_declares_one_distinct_corrective_per_predicate(self) -> None:
        from se_harness.workflow_contract import load_validated_contracts

        workflow, _, _, procedures, gates = load_validated_contracts()
        gated = 0
        for procedure_id, procedure in procedures.items():
            for step in procedure["steps"]:
                if step["kind"] != "command" or not step["gate_ids"]:
                    self.assertNotIn("corrective", step)
                    continue
                gated += 1
                expected = {p["id"] for gate_id in step["gate_ids"] for p in gates[gate_id]["predicates"]}
                self.assertEqual(expected, set(step["corrective"]), (procedure_id, step["id"]))
                for predicate_id, form in step["corrective"].items():
                    with self.subTest(step=step["id"], predicate=predicate_id):
                        self.assertIn(form["kind"], {"command", "escalation", "response"})
                        if form["kind"] == "command":
                            self.assertNotEqual(step["argv"], form["argv"])
                            if form["argv"][1] == "check":
                                self.assertGreater(len(form["argv"]), len(self.EVALUATED) + 1)
                        elif form["kind"] == "escalation":
                            self.assertRegex(form["decision_right"], r"^DR-")
        self.assertGreaterEqual(gated, 5)

    def test_contract_without_corrective_forms_fails_to_load_with_wex_ads_001(self) -> None:
        from se_harness.workflow_contract import (
            ContractError,
            load_quality_gate_contract,
            load_workflow_contract,
            validate_contracts,
        )

        workflow = json.loads(json.dumps(load_workflow_contract()))
        quality = load_quality_gate_contract()
        for procedure in workflow["procedures"]:
            for step in procedure["steps"]:
                if step["id"] == "STEP-WO-IMPLEMENT-CHECK":
                    del step["corrective"]
        with self.assertRaises(ContractError) as missing:
            validate_contracts(workflow, quality)
        self.assertIn("WEX-ADS-001", str(missing.exception))

        workflow = json.loads(json.dumps(load_workflow_contract()))
        for procedure in workflow["procedures"]:
            for step in procedure["steps"]:
                if step["id"] == "STEP-WO-IMPLEMENT-CHECK":
                    step["corrective"]["QGP-G4I-COMPLETE"] = {"kind": "command", "argv": list(step["argv"])}
        with self.assertRaises(ContractError) as loop:
            validate_contracts(workflow, quality)
        self.assertIn("repeats the evaluated command", str(loop.exception))

    def test_blocked_handoff_check_never_renders_its_own_command_as_the_retry(self) -> None:
        self.in_progress_work_order()
        code, output, error = self.invoke(
            "check", str(self.root), "--artifact", "WO-001", "--checkpoint", "handoff", "--json"
        )
        self.assertEqual(1, code, error)
        result = json.loads(output)
        self.assertEqual("blocked", result["operation"]["outcome"])
        command = result["restitution"]["command_or_response"]
        evaluated = ["harnessctl", "check", ".", "--artifact", "WO-001", "--checkpoint", "handoff"]
        self.assertNotEqual(evaluated, command.get("argv"))
        self.assertEqual("command", command["kind"])
        # WO-ECP-001: the completeness corrective names the Git-derived form.
        self.assertEqual(evaluated + ["--from-git", "<base>"], command["argv"])
        self.assertIn("QGP-G4I-COMPLETE", result["restitution"]["next"]["action"])

        code, output, error = self.invoke(
            "check", str(self.root), "--artifact", "WO-001", "--checkpoint", "handoff",
            "--changed-path", "src/main.py", "--changes-complete", "--json",
        )
        self.assertEqual(1, code, error)
        result = json.loads(output)
        command = result["restitution"]["command_or_response"]
        self.assertNotEqual(evaluated, command.get("argv"))
        self.assertNotEqual(evaluated + ["--changed-path", "src/main.py", "--changes-complete"], command.get("argv"))
        failing = [
            predicate["id"]
            for gate in result["compliance"]["gates"]
            for predicate in gate["predicates"]
            if predicate["status"] != "pass"
        ]
        self.assertIn(failing[0], result["restitution"]["next"]["action"])

    def test_projection_and_handoff_check_resolve_the_same_next_step_for_one_state(self) -> None:
        self.in_progress_work_order()
        code, focus_output, error = self.invoke("check", str(self.root), "--artifact", "WO-001", "--json")
        self.assertEqual(0, code, error)
        code, check_output, error = self.invoke(
            "check", str(self.root), "--artifact", "WO-001", "--checkpoint", "handoff", "--json"
        )
        self.assertEqual(1, code, error)
        focus_next = json.loads(focus_output)["restitution"]["next"]
        check_next = json.loads(check_output)["restitution"]["next"]
        self.assertEqual(focus_next["procedure_id"], check_next["procedure_id"])
        self.assertEqual(focus_next["step_id"], check_next["step_id"])
        human = self.invoke("check", str(self.root), "--artifact", "WO-001")[1]
        self.assertTrue(human.startswith("Outcome\n"))

    def test_result_digest_binds_the_canonical_block_bytes(self) -> None:
        import hashlib

        from se_harness.workflow_result import canonical_block_bytes, render_human

        code, output, error = self.invoke("check", str(self.root), "--artifact", "WO-001", "--json")
        self.assertEqual(0, code, error)
        result = json.loads(output)
        digest = result["result_sha256"]
        self.assertRegex(digest, r"^[0-9a-f]{64}$")
        block = canonical_block_bytes(result)
        self.assertEqual(hashlib.sha256(block).hexdigest(), digest)
        self.assertNotIn(b"\r", block)
        self.assertTrue(block.endswith(b"\n") and not block.endswith(b"\n\n"))
        self.assertEqual(block.decode("utf-8").rstrip("\n") + "\n", render_human(result))
        human = self.invoke("check", str(self.root), "--artifact", "WO-001")[1]
        self.assertEqual(digest, hashlib.sha256(human.replace("\r\n", "\n").encode("utf-8")).hexdigest())

    def test_operating_card_template_equals_its_contract_rendering_and_stays_bounded(self) -> None:
        from se_harness.workflow_contract import (
            OPERATING_CARD_LIMIT,
            load_quality_gate_contract,
            load_workflow_contract,
            render_operating_card,
        )

        template = Path(__file__).resolve().parents[1] / "templates/repository/standard/docs/engineering/OPERATING_CARD.md"
        rendered = render_operating_card()
        self.assertEqual(rendered, template.read_bytes().replace(b"\r\n", b"\n"))
        self.assertLessEqual(len(rendered), OPERATING_CARD_LIMIT)
        self.assertEqual([b"## Stop when", b"## Traps"], re.findall(rb"^## .*$", rendered, flags=re.MULTILINE))
        self.assertNotIn(b"| Class |", rendered)
        mutated = json.loads(json.dumps(load_workflow_contract()))
        mutated["restitution_fields"].append("extra")
        with self.assertRaises(Exception):
            render_operating_card(mutated, load_quality_gate_contract())

        installed = self.root / "docs/engineering/OPERATING_CARD.md"
        self.assertTrue(installed.is_file())
        lock = json.loads((self.root / ".engineering-harness.lock").read_text(encoding="utf-8"))
        self.assertEqual("managed", lock["files"]["docs/engineering/OPERATING_CARD.md"]["mode"])
        code, output, error = self.invoke(
            "preflight", str(self.root), "--work-order", "WO-001", "--phase", "review", "--json"
        )
        manifest = json.loads(output)["reading_manifest"]
        self.assertEqual(["ENGINEERING_HARNESS.md", "docs/engineering/OPERATING_CARD.md", "AGENTS.md"], manifest[:3])
        self.assertNotIn("docs/engineering/WORKFLOW.md", manifest)

    def test_carriage_return_trailer_is_named_with_its_offset(self) -> None:
        from se_harness.github_ci import (
            SelectionError,
            carriage_return_trailer_offsets,
            select_restitution_digest,
            select_work_order,
        )

        body = "Summary\r\n\r\nHarness-Work-Order: WO-EX-001\r\n"
        self.assertEqual([len("Summary\r\n\r\nHarness-Work-Order: WO-EX-001")], carriage_return_trailer_offsets(body))
        with self.assertRaises(SelectionError) as raised:
            select_work_order(body)
        self.assertIn("W-ADS-001", str(raised.exception))
        self.assertIn("byte offset", str(raised.exception))
        self.assertEqual("WO-EX-001", select_work_order(body.replace("\r\n", "\n")))
        self.assertEqual("", select_restitution_digest("Harness-Work-Order: WO-EX-001\n"))
        digest = "0" * 64
        self.assertEqual(digest, select_restitution_digest(f"Harness-Restitution: {digest}\n"))
        with self.assertRaises(SelectionError):
            select_restitution_digest(f"Harness-Restitution: {digest}\nHarness-Restitution: {digest}\n")

        event = self.root / "event.json"
        event.write_text(
            json.dumps({"pull_request": {"body": f"Harness-Work-Order: WO-EX-001\nHarness-Restitution: {digest}\n"}}),
            encoding="utf-8",
        )
        code, output, error = self.invoke("select-work-order", "--event", str(event), "--field", "restitution-digest")
        self.assertEqual(0, code, error)
        self.assertEqual(digest, output.strip())
        event.write_text(json.dumps({"pull_request": {"body": "Harness-Work-Order: WO-EX-001\n"}}), encoding="utf-8")
        code, output, _ = self.invoke("select-work-order", "--event", str(event), "--field", "restitution-digest")
        self.assertEqual(0, code)
        self.assertEqual("", output.strip())

    def test_handoff_check_reports_a_carriage_return_trailer_from_a_body_file(self) -> None:
        self.in_progress_work_order()
        body = self.root / "body.md"
        body.write_bytes(b"Harness-Work-Order: WO-EX-001\r\n")
        code, output, error = self.invoke(
            "check", str(self.root), "--artifact", "WO-001", "--checkpoint", "handoff",
            "--pull-request-body", str(body), "--json",
        )
        self.assertEqual(1, code, error)
        blockers = json.loads(output)["restitution"]["blocked_by"]
        self.assertTrue(any(item.startswith("W-ADS-001:") for item in blockers), blockers)

    def test_orphaned_ready_record_blocks_review_preflight_and_handoff(self) -> None:
        import shutil
        import subprocess

        if shutil.which("git") is None:
            self.skipTest("git is unavailable")
        from se_harness.preflight import orphaned_ready_records

        def git(*arguments: str) -> str:
            completed = subprocess.run(
                ["git", "-C", str(self.root), *arguments],
                capture_output=True, text=True, check=True,
                env={
                    **os.environ,
                    "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid",
                    "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.invalid",
                },
            )
            return completed.stdout.strip()

        git("init", "-q", "-b", "main")
        git("add", "-A")
        git("commit", "-q", "-m", "base")
        git("checkout", "-q", "-b", "feature")
        (self.root / "feature.txt").write_text("x\n", encoding="utf-8")
        git("add", "-A")
        git("commit", "-q", "-m", "feature")
        orphan = git("rev-parse", "HEAD")
        git("checkout", "-q", "main")
        reachable = git("rev-parse", "HEAD")

        validator = _load_validator_module()

        def artifacts() -> list:
            return list(validator.validate_repository(self.root).artifacts)

        path = self.ready_vrec()
        path.write_text(path.read_text(encoding="utf-8").replace("a" * 40, orphan, 1), encoding="utf-8")
        messages = orphaned_ready_records(self.root, artifacts(), "WO-001")
        self.assertEqual(1, len(messages), messages)
        self.assertIn("VREC-001", messages[0])
        self.assertIn(orphan, messages[0])
        self.assertIn("verify, reject, or a successor", messages[0])
        self.assertEqual([], orphaned_ready_records(self.root, artifacts(), "WO-999"))

        path.write_text(path.read_text(encoding="utf-8").replace(orphan, reachable, 1), encoding="utf-8")
        self.assertEqual([], orphaned_ready_records(self.root, artifacts(), "WO-001"))

        path.write_text(path.read_text(encoding="utf-8").replace(reachable, "f" * 40, 1), encoding="utf-8")
        self.assertEqual([], orphaned_ready_records(self.root, artifacts(), "WO-001"), "unknown object is not assessable")

        path.write_text(path.read_text(encoding="utf-8").replace("f" * 40, orphan, 1), encoding="utf-8")
        self.in_progress_work_order()
        code, output, error = self.invoke(
            "check", str(self.root), "--artifact", "WO-001", "--checkpoint", "handoff", "--json"
        )
        self.assertEqual(1, code, error)
        blockers = json.loads(output)["restitution"]["blocked_by"]
        self.assertTrue(any(item.startswith("W-ADS-002:") for item in blockers), blockers)
        self.assertTrue(any(orphan in item for item in blockers), blockers)

    def test_projection_digest_equals_the_released_evaluator_golden(self) -> None:
        """Issue #212 criterion 3: an unchanged repository keeps its result_sha256.

        The constant was read from the exact public se-harness 0.7.1 evaluator's
        `focus --json` on this fixture before WO-ECP-005 removed schema 1
        (d22f5e48…) and reproduced by the candidate until 2026-08-28, when
        WO-ECP-003 widened the canonical block with the change set and every
        predicate status (ECP-DIG-001): every result_sha256 changes at that
        upgrade by specification, and the pin moves to the widened block. The
        criterion holds within one block definition. On 2026-08-29 WO-ECP-019
        folded the execution context into the projection (ECP-CTX-003): the
        block gains the Context section and the pin moves again, from
        b8ccd288… to the value below.
        """

        code, output, error = self.invoke("check", str(self.root), "--artifact", "WO-001", "--json")
        self.assertEqual(0, code, error)
        self.assertEqual(
            "c307910acec83b544f8c43748355db3a3e70276195f9c02c46b0c8017435bd69",
            json.loads(output)["result_sha256"],
        )

    def test_every_workflow_command_refuses_the_retired_result_schema_option(self) -> None:
        for command in (
            ["check", str(self.root), "--artifact", "WO-001"],
            ["transition", str(self.root), "--set", "WO-001=verified", "--decision", "WO-001=x"],
            ["capture-verification", str(self.root), "--id", "VREC-009", "--work-order", "WO-001", "--verification", "VER-001", "--evidence", "x"],
            ["prepare-release", str(self.root), "--id", "RLS-009", "--release-contract", "REL-001", "--verification-record", "VREC-001", "--work-order", "WO-001", "--version", "1.0.0", "--authorized-by", "release-owner"],
        ):
            with self.subTest(command=command[0]):
                error = io.StringIO()
                with contextlib.redirect_stderr(error), self.assertRaises(SystemExit) as raised:
                    main([*command, "--result-schema", "2"])
                self.assertEqual(2, raised.exception.code)
                self.assertIn("unrecognized arguments: --result-schema", error.getvalue())

    def test_transition_and_projection_agree_on_the_next_step_for_the_resulting_state(self) -> None:
        # ECP-KRN-003: one selector. The plan's next step for the target state equals
        # focus's next step once that state exists.
        self.ready_vrec()
        code, plan_output, error = self.invoke(
            "transition", str(self.root), "--set", "VREC-001=verified",
            "--decision", "VREC-001=assurance-owner", "--json",
        )
        self.assertEqual(0, code, error)
        code, _, error = self.invoke(
            "transition", str(self.root), "--set", "VREC-001=verified",
            "--decision", "VREC-001=assurance-owner", "--apply",
        )
        self.assertEqual(0, code, error)
        code, focus_output, error = self.invoke("check", str(self.root), "--artifact", "VREC-001", "--json")
        self.assertEqual(0, code, error)
        plan_next = json.loads(plan_output)["restitution"]["next"]
        focus_next = json.loads(focus_output)["restitution"]["next"]
        self.assertEqual(focus_next, plan_next)
        self.assertEqual(
            json.loads(plan_output)["restitution"]["current_lifecycle_state"],
            json.loads(focus_output)["restitution"]["current_lifecycle_state"],
        )



class ExecutionContextTests(WorkflowExecutionTests):
    """REQ-ECP-001 / ECP-NXT-001 to -008: one call returns the complete context."""

    def context_result(self, *arguments: str) -> tuple[int, dict, str]:
        code, output, error = self.invoke("check", str(self.root), *arguments, "--json")
        return code, json.loads(output), error

    def test_check_selects_the_single_in_progress_work_order_and_carries_the_context(self) -> None:
        # ECP-CTX-001 / ECP-CTX-002: the projection is the execution context.
        self.in_progress_work_order()
        code, result, error = self.context_result()
        self.assertEqual(0, code, error)
        self.assertEqual({"kind": "check", "outcome": "completed"}, result["operation"])
        self.assertEqual("WO-001", result["selection"]["primary"])
        context = result["context"]
        self.assertEqual(
            ["reading_manifest", "governing", "declared_paths", "state", "next", "decision_required"],
            list(context),
        )
        self.assertEqual({"status": "in_progress", "family": "work_order"}, context["state"])
        self.assertEqual(["src/"], context["declared_paths"])
        self.assertEqual(result["scope"]["governing"], context["governing"])
        explicit = json.loads(self.invoke("check", str(self.root), "--artifact", "WO-001", "--json")[1])
        self.assertEqual(explicit, result)
        check = json.loads(self.invoke("check", str(self.root), "--artifact", "WO-001", "--checkpoint", "handoff", "--json")[1])
        self.assertEqual(result["restitution"]["command_or_response"]["argv"], context["next"]["argv"])
        self.assertEqual(
            (check["restitution"]["next"]["procedure_id"], check["restitution"]["next"]["step_id"]),
            (context["next"]["procedure_id"], context["next"]["step_id"]),
        )
        self.assertNotIn("context", check)
        from se_harness.workflow_result import restitution_digest

        self.assertEqual(restitution_digest(result), result["result_sha256"])
        human = self.invoke("check", str(self.root))[1]
        self.assertIn("\nContext\n", human)
        self.assertLess(human.index("Command or response"), human.index("\nContext\n"))

    def test_next_is_a_byte_identical_alias_that_announces_its_removal(self) -> None:
        # ECP-CTX-004: same bytes, same digest, one notice on standard error.
        self.in_progress_work_order()
        for arguments in ((), ("--artifact", "WO-001")):
            with self.subTest(arguments=arguments):
                check_code, check_output, check_error = self.invoke("check", str(self.root), *arguments, "--json")
                next_code, next_output, next_error = self.invoke("next", str(self.root), *arguments, "--json")
                self.assertEqual((0, 0), (check_code, next_code), check_error + next_error)
                self.assertEqual(check_output, next_output)
                self.assertEqual("check", json.loads(next_output)["operation"]["kind"])
                self.assertEqual("", check_error)
                self.assertEqual(1, next_error.count("\n"))
                self.assertIn("harnessctl check", next_error)
        self.assertEqual(self.invoke("check", str(self.root))[1], self.invoke("next", str(self.root))[1])

    def test_check_with_a_checkpoint_still_requires_an_artifact(self) -> None:
        self.in_progress_work_order()
        code, output, error = self.invoke("check", str(self.root), "--checkpoint", "start", "--json")
        self.assertEqual(2, code)
        self.assertEqual("", output)
        self.assertIn("WEX210: --artifact is required with --checkpoint", error)

    def test_check_reading_manifest_equals_preflight_for_the_implied_phase(self) -> None:
        from se_harness.preflight import run_preflight

        self.in_progress_work_order()
        _, result, _ = self.context_result("--artifact", "WO-001")
        expected = list(run_preflight(self.root, work_order_id="WO-001", phase="start").reading_manifest)
        self.assertEqual(expected, result["context"]["reading_manifest"])
        self.assertTrue(expected)
        work_order = self.root / "docs/engineering/product/work-orders/WO-001.md"
        work_order.write_text(work_order.read_text(encoding="utf-8").replace('status = "in_progress"', 'status = "implemented"', 1), encoding="utf-8")
        _, result, _ = self.context_result("--artifact", "WO-001")
        expected = list(run_preflight(self.root, work_order_id="WO-001", phase="review").reading_manifest)
        self.assertEqual(expected, result["context"]["reading_manifest"])
        self.assertEqual("implemented", result["context"]["state"]["status"])

    def test_check_without_an_artifact_blocks_unless_exactly_one_work_order_is_in_progress(self) -> None:
        code, result, error = self.context_result()
        self.assertEqual(1, code, error)
        self.assertEqual("blocked", result["operation"]["outcome"])
        self.assertEqual("check", result["operation"]["kind"])
        self.assertTrue(result["restitution"]["blocked_by"][0].startswith("WEX-ECP-001: 0 work orders"))
        self.in_progress_work_order()
        second = self.root / "docs/engineering/product/work-orders/WO-002.md"
        second.write_text(
            (self.root / "docs/engineering/product/work-orders/WO-001.md").read_text(encoding="utf-8").replace("WO-001", "WO-002"),
            encoding="utf-8",
        )
        code, result, error = self.context_result()
        self.assertEqual(1, code, error)
        self.assertTrue(result["restitution"]["blocked_by"][0].startswith("WEX-ECP-001: 2 work orders"))
        self.assertIn("WO-001, WO-002", result["restitution"]["blocked_by"][0])

    def test_check_projects_a_verification_record_and_a_release_record_with_their_context(self) -> None:
        self.ready_vrec()
        code, result, error = self.context_result("--artifact", "VREC-001")
        self.assertEqual(0, code, error)
        self.assertEqual({"status": "ready", "family": "verification_record"}, result["context"]["state"])
        self.assertEqual([], result["context"]["declared_paths"])
        self.assertIsNotNone(result["context"]["decision_required"])
        self.assertEqual([], result["context"]["next"]["argv"])
        self.assertTrue(result["context"]["reading_manifest"])
        code, result, error = self.context_result("--artifact", "REQ-001")
        self.assertEqual(1, code, error)
        self.assertIn("check accepts only WO, VREC, or RLS", result["restitution"]["blocked_by"][0])

    def test_the_projection_writes_nothing(self) -> None:
        self.in_progress_work_order()
        before = {path: path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        code, result, error = self.context_result()
        self.assertEqual(0, code, error)
        self.assertEqual([], result["mutation"]["writes"])
        after = {path: path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        self.assertEqual(before, after)

    def test_a_failed_check_names_the_projection_as_the_retry_never_the_evaluated_command(self) -> None:
        # ECP-NXT-008 as ECP-CTX-005 restates it: the WEX210 corrective is the projection
        # under `check`, not "rerun the same command".
        code, output, error = self.invoke("check", str(self.root), "--artifact", "WO-404", "--checkpoint", "start", "--json")
        self.assertEqual(1, code, error)
        result = json.loads(output)
        self.assertEqual(
            {"kind": "command", "argv": ["harnessctl", "check", ".", "--artifact", "WO-404"]},
            result["restitution"]["command_or_response"],
        )
        self.assertNotIn("rerun the same command", json.dumps(result))
        self.assertNotIn('"next", "."', json.dumps(result))

    def test_nothing_names_next_as_the_command_but_the_alias_row_and_the_notes(self) -> None:
        # ECP-CTX-007: the template and the reference name check; the reference keeps one
        # row for the alias while it exists, and no accept-candidate row or synopsis.
        workflow_md = (REPOSITORY_ROOT / "templates/repository/standard/docs/engineering/WORKFLOW.md").read_text(encoding="utf-8")
        self.assertNotIn("harnessctl next", workflow_md)
        self.assertIn("`harnessctl check . --artifact WO-...`", workflow_md)
        reference = (REPOSITORY_ROOT / "docs/notes/harnessctl-reference.md").read_text(encoding="utf-8")
        self.assertEqual(1, reference.count("| `next` |"))
        self.assertIn("alias", reference[reference.index("| `next` |"):reference.index("| `next` |") + 200])
        self.assertNotIn("harnessctl next [", reference)
        self.assertEqual(0, reference.count("| `accept-candidate` |"))
        self.assertNotIn("harnessctl accept-candidate", reference)
        note = (REPOSITORY_ROOT / "docs/notes/harnessctl-check.md").read_text(encoding="utf-8")
        self.assertNotIn("harnessctl next", note)
        roles = (REPOSITORY_ROOT / "docs/notes/release-qualification-roles.md").read_text(encoding="utf-8")
        self.assertIn("removed after 0.11.0", roles)
        help_output = io.StringIO()
        with contextlib.redirect_stdout(help_output), self.assertRaises(SystemExit):
            main(["--help"])
        self.assertNotIn("accept-candidate", help_output.getvalue())


class PullRequestBodyTests(unittest.TestCase):
    """REQ-ECP-005 / ECP-PRB-001 to -005 (its own fixture: the parent's tests are not re-run here)."""

    def invoke(self, *arguments: str) -> tuple[int, str, str]:
        output = io.StringIO()
        error = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            code = main(list(arguments))
        return code, output.getvalue(), error.getvalue()

    def setUp(self) -> None:
        # The CI selector accepts only TYPE-DOMAIN-NNN identifiers; the fixture chain
        # is renamed WO-001 -> WO-PRD-001 so the generated body can round-trip.
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        standard_repository(self.root, "Body Fixture")
        create_base_chain(self.root, operating_contract_status="draft")
        for path in (self.root / "docs/engineering/product").rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            if "WO-001" in text:
                path.write_text(text.replace("WO-001", "WO-PRD-001"), encoding="utf-8")
        work_order = self.root / "docs/engineering/product/work-orders/WO-001.md"
        work_order.rename(work_order.with_name("WO-PRD-001.md"))

    def in_progress_work_order(self) -> Path:
        path = self.root / "docs/engineering/product/work-orders/WO-PRD-001.md"
        text = path.read_text(encoding="utf-8").replace('status = "implemented"', 'status = "in_progress"', 1)
        text = text.replace(
            "[relations]",
            '[assurance]\ncommit_bound_verification = "required"\nrationale = "fixture"\ndecided_by = "repository-owner"\n\n[execution_scope]\npaths = ["src/"]\n\n[relations]',
            1,
        )
        path.write_text(text, encoding="utf-8")
        return path

    def body(self, artifact_id: str = "WO-PRD-001") -> tuple[int, bytes, str]:
        from types import SimpleNamespace

        buffer = io.BytesIO()
        error = io.StringIO()
        stdout = SimpleNamespace(buffer=buffer, flush=lambda: None, write=lambda text: buffer.write(text.encode("utf-8")))
        with mock.patch("sys.stdout", new=stdout), contextlib.redirect_stderr(error):
            code = main(["pr-body", str(self.root), "--artifact", artifact_id])
        return code, buffer.getvalue(), error.getvalue()

    def test_body_round_trips_through_the_selector_with_lf_only_and_the_retained_digest(self) -> None:
        from se_harness.github_ci import carriage_return_trailer_offsets, select_restitution_digest, select_work_order

        self.in_progress_work_order()
        code, raw, error = self.body()
        self.assertEqual(0, code, error)
        self.assertNotIn(b"\r", raw)
        self.assertTrue(raw.endswith(b"\n") and not raw.endswith(b"\n\n"))
        text = raw.decode("utf-8")
        self.assertEqual("Harness-Work-Order: WO-PRD-001", text.splitlines()[0])
        self.assertEqual("WO-PRD-001", select_work_order(text))
        self.assertEqual("", select_restitution_digest(text))
        self.assertEqual([], carriage_return_trailer_offsets(text))
        self.assertIn("## Summary\n", text)
        self.assertIn("## Verification\n", text)
        self.assertIn("- No retained evidence under the packet directory yet.", text)
        packet_dir = self.root / "docs/engineering/product/evidence/WO-PRD-001"
        packet_dir.mkdir(parents=True)
        (packet_dir / "WO-PRD-001-handoff.md").write_text("```toml\n```\n", encoding="utf-8")
        (packet_dir / "handoff.json").write_text(json.dumps({"schema": "se-harness-workflow-result-v2", "result_sha256": "a" * 64}), encoding="utf-8")
        code, raw, error = self.body()
        self.assertEqual(0, code, error)
        text = raw.decode("utf-8")
        self.assertEqual("a" * 64, select_restitution_digest(text))
        self.assertEqual(["Harness-Work-Order: WO-PRD-001", "Harness-Restitution: " + "a" * 64], text.splitlines()[:2])
        self.assertIn("- docs/engineering/product/evidence/WO-PRD-001/WO-PRD-001-handoff.md", text)
        self.assertIn("- docs/engineering/product/evidence/WO-PRD-001/handoff.json", text)
        self.assertTrue(text.startswith("Harness-Work-Order: WO-PRD-001\nHarness-Restitution: " + "a" * 64 + "\n\n## Summary\n\n- WO-PRD-001: "))
        (packet_dir / "handoff.json").write_text(json.dumps({"schema": "other", "result_sha256": "b" * 64}), encoding="utf-8")
        self.assertEqual("", select_restitution_digest(self.body()[1].decode("utf-8")))

    def test_pr_body_refuses_a_draft_work_order_and_a_non_work_order(self) -> None:
        code, raw, error = self.body("WO-PRD-001")
        self.assertEqual(0, code, error)  # the fixture work order is implemented
        work_order = self.root / "docs/engineering/product/work-orders/WO-PRD-001.md"
        work_order.write_text(work_order.read_text(encoding="utf-8").replace('status = "implemented"', 'status = "draft"', 1), encoding="utf-8")
        code, raw, error = self.body("WO-PRD-001")
        self.assertEqual(2, code)
        self.assertIn("WEX-ECP-014", error)
        self.assertEqual(b"", raw)
        code, raw, error = self.body("REQ-001")
        self.assertEqual(2, code)
        self.assertIn("WEX-ECP-014", error)



class DigestCoverageTests(WorkflowExecutionTests):
    """REQ-ECP-007 / ECP-DIG-001 to -004: the digest binds the change set and the gates."""

    def test_the_block_carries_the_change_set_and_every_predicate_status(self) -> None:
        from se_harness.workflow_result import canonical_block_bytes

        self.in_progress_work_order()
        (self.root / "src").mkdir(exist_ok=True)
        (self.root / "src/main.py").write_text("x = 1\n", encoding="utf-8")
        code, output, error = self.invoke(
            "check", str(self.root), "--artifact", "WO-001", "--checkpoint", "handoff",
            "--changed-path", "src/main.py", "--changed-path", "src/a.py", "--changes-complete", "--json",
        )
        result = json.loads(output)
        block = canonical_block_bytes(result).decode("utf-8")
        self.assertIn("\nChange set\n- src/a.py\n- src/main.py\ncomplete: true\n", block)
        gates = block.split("\nGates\n", 1)[1].split("\n\n", 1)[0].splitlines()
        expected = [f"{p['id']}: {p['status']}" for g in result["compliance"]["gates"] for p in g["predicates"]]
        self.assertEqual(expected, gates)
        self.assertIn("QGP-G4I-PATHS: ", "\n".join(gates))
        self.assertLess(block.index("Command or response"), block.index("\nChange set\n"))
        self.assertLess(block.index("\nChange set\n"), block.index("\nGates\n"))
        for command in (("check", "--artifact", "WO-001"), ("next", "--artifact", "WO-001")):
            with self.subTest(command=command[0]):
                human = self.invoke(command[0], str(self.root), *command[1:])[1]
                self.assertIn("\nChange set\nNone.\ncomplete: false\n", human)
                self.assertIn("\nGates\n", human)
        human = self.invoke("check", str(self.root), "--artifact", "WO-001", "--checkpoint", "handoff", "--changed-path", "src/main.py", "--changed-path", "src/a.py", "--changes-complete")[1]
        self.assertEqual(block, human.replace("\r\n", "\n"))

    def test_one_changed_path_one_completeness_flip_or_one_predicate_status_changes_the_digest(self) -> None:
        import copy

        from se_harness.workflow_result import canonical_block_bytes, restitution_digest

        self.in_progress_work_order()
        code, output, error = self.invoke(
            "check", str(self.root), "--artifact", "WO-001", "--checkpoint", "handoff",
            "--changed-path", "src/main.py", "--changes-complete", "--json",
        )
        base = json.loads(output)
        self.assertEqual(restitution_digest(base), base["result_sha256"])
        path_edit = copy.deepcopy(base)
        path_edit["scope"]["changed_paths"] = ["src/other.py"]
        complete_edit = copy.deepcopy(base)
        complete_edit["scope"]["change_set_complete"] = not base["scope"]["change_set_complete"]
        status_edit = copy.deepcopy(base)
        predicate = status_edit["compliance"]["gates"][0]["predicates"][0]
        predicate["status"] = "fail" if predicate["status"] != "fail" else "pass"
        digests = {restitution_digest(item) for item in (base, path_edit, complete_edit, status_edit)}
        self.assertEqual(4, len(digests))
        # identical inputs share one digest whether the block is rendered LF or CRLF
        crlf = canonical_block_bytes(base).decode("utf-8").replace("\n", "\r\n").replace("\r\n", "\n")
        self.assertEqual(base["result_sha256"], __import__("hashlib").sha256(crlf.encode("utf-8")).hexdigest())


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class OnePreconditionEngineTests(WorkflowExecutionTests):
    """WO-ECP-009: `transition` evaluates the contract's gates through the evaluator `check` uses."""

    READY_PREFLIGHT = SimpleNamespace(ready=True, diagnostics=[])

    def gates_of(self, result: dict) -> list[tuple[str, str, str]]:
        return [
            (gate["id"], predicate["id"], predicate["status"])
            for gate in result["compliance"]["gates"]
            for predicate in gate["predicates"]
        ]

    def test_transition_plan_and_transition_check_agree_for_every_primary_state(self) -> None:
        # ECP-KRN-007 conformance: identical compliance.gates for the same artifact,
        # target and snapshot, from the planning path and the public preview.
        self.ready_vrec()
        cases = [("VREC-001", "verified", "assurance-owner")]
        work_order = self.root / "docs/engineering/product/work-orders/WO-001.md"
        text = work_order.read_text(encoding="utf-8")
        work_order.write_text(text.replace('status = "implemented"', 'status = "approved"', 1).replace(
            "[relations]",
            '[assurance]\ncommit_bound_verification = "required"\nrationale = "fixture"\ndecided_by = "repository-owner"\n\n[execution_scope]\npaths = ["src/"]\n\n[relations]',
            1,
        ), encoding="utf-8")
        cases.append(("WO-001", "in_progress", "engineering-owner"))
        with mock.patch("se_harness.workflow_compliance.run_preflight", return_value=self.READY_PREFLIGHT):
            for artifact_id, target, actor in cases:
                with self.subTest(artifact=artifact_id, target=target):
                    plan = plan_transition(self.root, {artifact_id: target}, {artifact_id: actor}, {})
                    preview = check_workflow(self.root, artifact_id=artifact_id, checkpoint="transition", target=target)
                    self.assertEqual(self.gates_of(preview), self.gates_of(plan.result))
                    self.assertEqual("transition", plan.result["compliance"]["checkpoint"])
                    self.assertEqual("transition", preview["compliance"]["checkpoint"])
                    self.assertEqual(plan.result["restitution"]["outcome"], preview["restitution"]["outcome"])
                    self.assertTrue(any(gate == "QG-STRUCTURAL" for gate, _, _ in self.gates_of(plan.result)))

    def test_handoff_check_evaluates_a_superset_of_the_transition_to_implemented(self) -> None:
        # Predicate-level checkpoints: the change-set predicates stay at handoff, every
        # predicate transition evaluates is evaluated identically by handoff.
        self.in_progress_work_order()
        self.bind_handoff_evidence()
        with mock.patch("se_harness.workflow_compliance.run_preflight", return_value=self.READY_PREFLIGHT):
            plan = plan_transition(self.root, {"WO-001": "implemented"}, {"WO-001": "engineering-owner"}, {})
            handoff = check_workflow(self.root, artifact_id="WO-001", checkpoint="handoff", changed_paths=["src/a.py"], changes_complete=True)
        transition_predicates = {(p, s) for g, p, s in self.gates_of(plan.result) if g != "QG-STRUCTURAL"}
        handoff_predicates = {(p, s) for _, p, s in self.gates_of(handoff)}
        self.assertTrue(transition_predicates.issubset(handoff_predicates), transition_predicates - handoff_predicates)
        transition_ids = {p for p, _ in transition_predicates}
        self.assertNotIn("QGP-G4I-COMPLETE", transition_ids)
        self.assertNotIn("QGP-G4I-PATHS", transition_ids)
        self.assertIn("QGP-G4I-COMPLETE", {p for p, _ in handoff_predicates})
        self.assertEqual("completed", plan.result["operation"]["outcome"], plan.result["restitution"]["blocked_by"])

    def test_a_predicate_added_to_the_contract_moves_transition_without_code_change(self) -> None:
        # VER-ECP-005 scenario 2: bind one more predicate to the edge in a copy of the
        # contract; the transition blocks naming it.
        from se_harness import workflow_contract

        self.in_progress_work_order()
        self.bind_handoff_evidence()
        contract = json.loads((REPOSITORY_ROOT / "se_harness/quality_gates_contract.json").read_text(encoding="utf-8"))
        for binding in contract["transition_bindings"]:
            if binding["family"] == "work_order" and binding["target"] == "implemented":
                binding["predicates"].append("QGP-G4I-COMPLETE")
        for gate in contract["gates"]:
            for predicate in gate["predicates"]:
                if predicate["id"] == "QGP-G4I-COMPLETE":
                    predicate["checkpoints"] = ["pre-action", "transition", "handoff"]
        mutated = self.root / "mutated-gates.json"
        mutated.write_text(json.dumps(contract), encoding="utf-8")
        original = workflow_contract.load_quality_gate_contract
        with mock.patch.object(workflow_contract, "load_quality_gate_contract", lambda path=None: original(mutated)), \
                mock.patch("se_harness.workflow_compliance.run_preflight", return_value=self.READY_PREFLIGHT):
            plan = plan_transition(self.root, {"WO-001": "implemented"}, {"WO-001": "engineering-owner"}, {})
        self.assertEqual("blocked", plan.result["operation"]["outcome"])
        self.assertTrue(any(item.startswith("QGP-G4I-COMPLETE:") for item in plan.result["restitution"]["blocked_by"]), plan.result["restitution"]["blocked_by"])

    def test_a_retired_gate_contract_is_refused_with_wex_ecp_030(self) -> None:
        from se_harness.workflow_contract import ContractError, load_quality_gate_contract

        contract = json.loads((REPOSITORY_ROOT / "se_harness/quality_gates_contract.json").read_text(encoding="utf-8"))
        contract["schema"] = "se-harness-quality-gates-v1"
        contract.pop("transition_bindings")
        older = self.root / "older-gates.json"
        older.write_text(json.dumps(contract), encoding="utf-8")
        with self.assertRaisesRegex(ContractError, "WEX-ECP-030"):
            load_quality_gate_contract(older)

    def test_an_unbound_lifecycle_edge_fails_contract_loading(self) -> None:
        from se_harness.workflow_contract import ContractError, load_quality_gate_contract, load_workflow_contract, validate_contracts

        contract = json.loads((REPOSITORY_ROOT / "se_harness/quality_gates_contract.json").read_text(encoding="utf-8"))
        contract["transition_bindings"] = [
            item for item in contract["transition_bindings"]
            if not (item["family"] == "verification_record" and item["target"] == "superseded")
        ]
        with self.assertRaisesRegex(ContractError, "WEX-ECP-030.*verification_record:ready -> superseded"):
            validate_contracts(load_workflow_contract(), contract)

    def test_refusals_carry_the_refusing_check_not_a_blanket_code(self) -> None:
        # ECP-KRN-008: an illegal edge is QGS-EDGE, and the CLI labels it so.
        code, output, error = self.invoke(
            "transition", str(self.root), "--set", "WO-001=approved", "--decision", "WO-001=x", "--json"
        )
        self.assertEqual(1, code, error)
        result = json.loads(output)
        self.assertEqual("blocked", result["operation"]["outcome"])
        self.assertEqual("QGS-EDGE", result["findings"]["scoped_blockers"][0]["code"])
        self.assertIn("implemented -> approved is not allowed", result["restitution"]["blocked_by"][0])

    def test_the_transition_preview_requires_and_limits_target(self) -> None:
        code, output, _ = self.invoke("check", str(self.root), "--artifact", "WO-001", "--checkpoint", "transition", "--json")
        self.assertEqual(1, code)
        self.assertIn("--target is required", json.loads(output)["restitution"]["blocked_by"][0])
        code, output, _ = self.invoke(
            "check", str(self.root), "--artifact", "WO-001", "--checkpoint", "handoff", "--target", "verified", "--json"
        )
        self.assertEqual(1, code)
        self.assertIn("applies only to the transition checkpoint", json.loads(output)["restitution"]["blocked_by"][0])
        code, output, error = self.invoke(
            "check", str(self.root), "--artifact", "WO-001", "--checkpoint", "transition", "--target", "verified", "--json"
        )
        self.assertEqual(1, code, error)
        result = json.loads(output)
        self.assertIn("QGS-VREC-COVERAGE: work order WO-001 has no direct eligible verification record", result["restitution"]["blocked_by"])
        self.assertEqual([], [w for w in result["mutation"]["writes"]])



class CheckProjectionTests(unittest.TestCase):
    """REQ-ECP-022 / SPEC-ECP-011 ECP-ONE-001 to -003 and REQ-ECP-024 / SPEC-ECP-013: check without a checkpoint is the projection; focus is gone."""

    STATES = ("approved", "in_progress", "implemented", "verified")

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        standard_repository(self.root, "Projection Fixture")
        create_base_chain(self.root, work_order_status="in_progress", operating_contract_status="draft")

    def run_cli(self, *argv: str) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = main(list(argv))
            except SystemExit as exc:
                code = int(exc.code or 0)
        return code, out.getvalue(), err.getvalue()

    def set_state(self, status: str) -> None:
        import re

        work_order = self.root / "docs/engineering/product/work-orders/WO-001.md"
        text = work_order.read_text(encoding="utf-8")
        work_order.write_text(re.sub(r'(?m)^status = "[a-z_]+"$', f'status = "{status}"', text, count=1), encoding="utf-8")

    def test_every_state_projects_with_no_gate_and_no_write(self) -> None:
        for status in self.STATES:
            with self.subTest(status=status):
                self.set_state(status)
                code, check_json, _ = self.run_cli("check", str(self.root), "--artifact", "WO-001", "--json")
                check = json.loads(check_json)
                self.assertEqual("check", check["operation"]["kind"])
                self.assertEqual([], check["compliance"].get("gates", []))
                self.assertEqual([], check["mutation"]["writes"])
                self.assertEqual("WO-001", check["selection"]["primary"])

    def test_focus_is_refused_with_its_replacement_named(self) -> None:
        # ECP-RMV-001/-002: no subcommand, and a loud refusal naming check.
        _, help_text, _ = self.run_cli("--help")
        self.assertNotIn("focus", help_text)
        code, out, err = self.run_cli("focus", str(self.root), "--artifact", "WO-001", "--json")
        self.assertEqual(2, code)
        self.assertEqual("", out)
        self.assertIn("harnessctl check --artifact WO-001", err)
        self.assertIn("focus was removed", err)
        code, out, err = self.run_cli("focus")
        self.assertEqual((2, ""), (code, out))
        self.assertIn("harnessctl check --artifact ID", err)

    def test_the_projection_accepts_records_and_the_background_switch(self) -> None:
        self.set_state("implemented")
        write(
            self.root / "docs/engineering/product/verification-records/VREC-001.md",
            "\n".join([
                "+++", 'id = "VREC-001"', 'type = "verification_record"', 'title = "t"', 'status = "ready"',
                'owners = ["assurance-owner"]', 'created = "2026-08-29"', 'updated = "2026-08-29"',
                'commit = "0000000000000000000000000000000000000000"', 'git_object_format = "sha1"',
                'worktree_state = "clean"', 'prepared_at = "2026-08-29T00:00:00Z"', 'prepared_by = "x"',
                'artifact_snapshot_sha256 = "' + "0" * 64 + '"', 'evidence_paths = ["docs/engineering/product/evidence/e.md"]',
                "[relations]", 'verifies_work_order = ["WO-001"]', 'conforms_to = ["VER-001"]', "+++", "", "# r", "",
            ]),
        )
        write(self.root / "docs/engineering/product/evidence/e.md", "# e\n")
        _, out, _ = self.run_cli("check", str(self.root), "--artifact", "VREC-001", "--json")
        self.assertEqual("PROC-VREC-DECIDE", json.loads(out)["restitution"]["next"]["procedure_id"])
        _, plain, _ = self.run_cli("check", str(self.root), "--artifact", "WO-001", "--json")
        _, expanded, _ = self.run_cli("check", str(self.root), "--artifact", "WO-001", "--json", "--include-background")
        self.assertEqual(json.loads(plain)["findings"]["unrelated_count"], json.loads(expanded)["findings"]["unrelated_count"])

    def test_the_projection_refuses_what_check_refuses(self) -> None:
        code, out, _ = self.run_cli("check", str(self.root), "--artifact", "INT-001", "--json")
        self.assertEqual(1, code)
        self.assertIn("WEX210: check accepts only WO, VREC, or RLS artifacts", json.loads(out)["restitution"]["blocked_by"][0])
        for option in (("--from-git", "HEAD"), ("--target", "implemented"), ("--procedure", "PROC-WO-IMPLEMENT"), ("--changes-complete",)):
            with self.subTest(option=option[0]):
                code, out, err = self.run_cli("check", str(self.root), "--artifact", "WO-001", *option)
                self.assertNotEqual(0, code)
                self.assertIn(f"WEX210: {option[0]} requires --checkpoint", out + err)

    def test_nothing_names_focus_but_the_note_that_records_its_removal(self) -> None:
        contract = json.loads((REPOSITORY_ROOT / "se_harness/workflow_contract.json").read_text(encoding="utf-8"))
        offenders = [
            (procedure["id"], step["id"])
            for procedure in contract["procedures"]
            for step in procedure.get("steps", [])
            if "focus" in step.get("argv", [])
        ]
        self.assertEqual([], offenders)
        renamed = {"STEP-WO-START-FOCUS", "STEP-WO-START-FINAL-FOCUS", "STEP-FOCUS-SELECTED", "STEP-FOCUS-RELATED", "STEP-REMEDIATE-FOCUS"}
        present = {step["id"] for procedure in contract["procedures"] for step in procedure.get("steps", [])}
        self.assertTrue(renamed <= present, renamed - present)
        workflow_md = (REPOSITORY_ROOT / "templates/repository/standard/docs/engineering/WORKFLOW.md").read_text(encoding="utf-8")
        self.assertIn("`WFL-003` - `harnessctl check` and `harnessctl transition` MUST select the first", workflow_md)
        self.assertNotIn("harnessctl focus", workflow_md)
        reference = (REPOSITORY_ROOT / "docs/notes/harnessctl-reference.md").read_text(encoding="utf-8")
        self.assertEqual(0, reference.count("| `focus` |"))
        self.assertNotIn("harnessctl focus", reference)
        note = (REPOSITORY_ROOT / "docs/notes/harnessctl-check.md").read_text(encoding="utf-8")
        self.assertEqual(1, note.count("`focus`"))
        self.assertIn("removed", note[note.index("`focus`") - 200:note.index("`focus`") + 200])
        # ECP-RMV-004 (the ECP-ONE-007 rule deferred at WO-ECP-015): the shipped orientation
        # core invokes check.
        orient = (REPOSITORY_ROOT / "templates/repository/standard/.agents/skills/harness-orient/scripts/orient.py").read_text(encoding="utf-8")
        self.assertIn('["check", str(target), "--artifact", artifact, "--json"]', orient)
        self.assertNotIn('["focus"', orient)
