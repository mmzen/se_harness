from __future__ import annotations

import contextlib
import errno
import io
import json
import os
import statistics
import tempfile
import time
import tomllib
import unittest
from pathlib import Path
from unittest import mock

from se_harness.cli import main
from se_harness.preflight import _load_validator_module
from se_harness.workflow import apply_transition, focus, plan_transition
from tests.test_revision_provenance import create_base_chain, formal, write


class WorkflowExecutionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        code, _, error = self.invoke("init", str(self.root), "--project-name", "Workflow Fixture")
        self.assertEqual(0, code, error)
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
tag = "v1.0.0"''',
        ).replace('owners = ["owner"]', 'owners = ["release-owner"]')
        write(path, content)
        return path

    def test_focus_projects_only_selected_governing_chain(self) -> None:
        code, output, error = self.invoke("focus", str(self.root), "--artifact", "WO-001", "--json")
        self.assertEqual(0, code, error)
        result = json.loads(output)
        self.assertEqual("completed", result["operation"]["outcome"])
        self.assertEqual(
            ["ADR-001", "ARCH-001", "CAP-001", "INT-001", "REQ-001", "SPEC-001", "VER-001"],
            result["scope"]["governing"],
        )
        self.assertEqual("prepare verification record", result["handoff"]["recommended_next_step"]["action"])

    def test_focus_projects_exact_vrec_scope_without_unrelated_work(self) -> None:
        self.ready_vrec()
        code, output, error = self.invoke(
            "focus", str(self.root), "--artifact", "VREC-001", "--json"
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
        self.assertEqual("assurance decision", result["handoff"]["recommended_next_step"]["action"])

    def test_focus_projects_exact_rls_scope_without_synchronizing_records(self) -> None:
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
            "focus", str(self.root), "--artifact", "RLS-001", "--json"
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

    def test_focus_rejects_a_non_primary_artifact_type(self) -> None:
        code, output, _ = self.invoke(
            "focus", str(self.root), "--artifact", "INT-001", "--json"
        )
        self.assertEqual(1, code)
        result = json.loads(output)
        self.assertEqual("failed", result["operation"]["outcome"])
        self.assertIn("only WO, VREC, or RLS", result["findings"]["scoped_blockers"][0]["message"])

    def test_duplicate_identity_is_a_repository_blocker(self) -> None:
        write(
            self.root / "docs/engineering/duplicate/INT-001.md",
            formal("INT-001", "intent", "approved", {}),
        )
        code, output, _ = self.invoke(
            "focus", str(self.root), "--artifact", "WO-001", "--json"
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
            "focus", str(self.root), "--artifact", "WO-001", "--json"
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
                    "focus", str(self.root), "--artifact", selected, "--json"
                )
                self.assertEqual(1, code)
                self.assertEqual("failed", json.loads(output)["operation"]["outcome"])
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
        self.assertEqual("planned", json.loads(output)["operation"]["outcome"])
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
        self.assertEqual("failed", result["operation"]["outcome"])
        self.assertIn("requires --reason", result["findings"]["scoped_blockers"][0]["message"])

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
        self.assertEqual("planned", json.loads(output)["operation"]["outcome"])
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
                    "focus", str(self.root),
                    "--artifact", scenario["artifact"],
                    "--json",
                )
            self.assertEqual(0, code, error)
            result = json.loads(output)
            self.assertEqual(scenario["expected"]["selection"], result["selection"])
            self.assertEqual(scenario["expected"]["scope"], result["scope"])
            self.assertEqual(scenario["expected"]["state"], result["state"])
            self.assertEqual(scenario["expected"]["handoff"], result["handoff"])
            observed.append(output)
        self.assertEqual(1, len(set(observed)))

    def test_human_output_exposes_the_same_fixture_handoff_semantics(self) -> None:
        fixture_path = Path(__file__).parent / "fixtures/workflow_execution/scenarios.json"
        scenario = json.loads(fixture_path.read_text(encoding="utf-8"))["scenarios"][0]
        json_code, json_output, json_error = self.invoke(
            "focus", str(self.root), "--artifact", scenario["artifact"], "--json"
        )
        human_code, human_output, human_error = self.invoke(
            "focus", str(self.root), "--artifact", scenario["artifact"]
        )
        self.assertEqual(0, json_code, json_error)
        self.assertEqual(0, human_code, human_error)
        handoff = json.loads(json_output)["handoff"]
        for value in handoff["completed"] + handoff["current_lifecycle_state"]:
            self.assertIn(value, human_output)
        for section in (
            "recommended_next_step",
            "human_decision_or_approval_required",
            "command_or_suggested_response",
        ):
            for value in handoff[section].values():
                self.assertIn(value, human_output)

    def test_focus_and_planning_scale_to_one_thousand_artifacts(self) -> None:
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
        for target_count in (100, 500, 1000):
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

            focus_seconds, result = median_runtime(lambda: focus(self.root, "WO-001"))
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
