"""Evidence for REQ-RSK-001 through REQ-RSK-006: the governed risk artifact."""

from __future__ import annotations

import contextlib
import io
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from se_harness.cli import main
from se_harness.preflight import _load_validator_module
from tests.mutation_guard_support import trusted_mutation_authority
from tests.test_revision_provenance import create_base_chain, formal, write


class RiskManagementTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        code, _, error = self.invoke("init", str(self.root), "--project-name", "Risk Fixture")
        self.assertEqual(0, code, error)
        lock_path = self.root / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["evaluator"]["archive_name"] = f"se_harness-{lock['tool_version'].replace('-', '_')}-py3-none-any.whl"
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

    def in_progress_work_order(self) -> Path:
        path = self.root / "docs/engineering/product/work-orders/WO-001.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace('status = "implemented"', 'status = "in_progress"', 1)
        text = text.replace(
            "[relations]",
            '[assurance]\ncommit_bound_verification = "required"\n'
            'rationale = "Risk fixture."\ndecided_by = "repository-owner"\n\n'
            '[execution_scope]\npaths = ["src/"]\n\n[relations]',
            1,
        )
        path.write_text(text, encoding="utf-8")
        return path

    def raise_risk(self, risk_id: str = "RISK-PRD-001", *, likelihood: int = 4, impact: int = 3, stage: str = "implementation", threatens: str = "WO-001", extra: tuple[str, ...] = ()) -> dict:
        code, output, error = self.invoke(
            "raise-risk", str(self.root), "--domain", "product", "--id", risk_id,
            "--title", "A stacked pull request orphans the ready record",
            "--stage", stage, "--category", "process",
            "--likelihood", str(likelihood), "--impact", str(impact),
            "--threatens", threatens, *extra, "--json",
        )
        self.assertEqual(0, code, error + output)
        return json.loads(output)

    def risk_path(self, risk_id: str = "RISK-PRD-001") -> Path:
        return self.root / f"docs/engineering/product/risks/{risk_id}.md"

    def validate(self) -> list:
        validator = _load_validator_module()
        return validator.validate_repository(self.root).errors

    # ---------------------------------------------------------------- REQ-RSK-001 / 002 / 006

    def test_raise_risk_computes_score_and_raises_at_the_default_level(self) -> None:
        result = self.raise_risk()
        self.assertEqual("completed", result["operation"]["outcome"])
        self.assertIn("Raised RISK-PRD-001 (score 12, acceptance level 1)", result["restitution"]["done"][0])
        self.assertEqual("STEP-RISK-DISPOSE", result["restitution"]["next"]["step_id"])
        self.assertEqual("DR-RISK-DISPOSE", result["restitution"]["decision_required"]["decision_right"])
        text = self.risk_path().read_text(encoding="utf-8")
        self.assertIn('status = "raised"', text)
        self.assertIn("score = 12", text)
        self.assertIn("acceptance_level = 1", text)
        self.assertIn('decided_by = "harnessctl"', text)
        self.assertIn('threatens = ["WO-001"]', text)
        self.assertEqual([], [item for item in self.validate() if "RISK" in item.path or "RSK" in item.code])

    def test_configured_level_keeps_a_low_risk_identified_and_copies_the_level(self) -> None:
        policy = self.root / ".engineering-harness.toml"
        policy.write_text(policy.read_text(encoding="utf-8").replace("acceptance_level = 1", "acceptance_level = 6"), encoding="utf-8")
        result = self.raise_risk(likelihood=1, impact=2)
        self.assertIn("Identified RISK-PRD-001 (score 2, acceptance level 6)", result["restitution"]["done"][0])
        self.assertEqual("STEP-FOCUS-SELECTED", result["restitution"]["next"]["step_id"])
        text = self.risk_path().read_text(encoding="utf-8")
        self.assertIn('status = "identified"', text)
        self.assertIn("acceptance_level = 6", text)
        self.assertNotIn("[[lifecycle_events]]", text)
        self.assertEqual([], [item for item in self.validate() if item.code.startswith("E-RSK")])
        # a later policy change does not reclassify the stored risk
        policy.write_text(policy.read_text(encoding="utf-8").replace("acceptance_level = 6", "acceptance_level = 1"), encoding="utf-8")
        self.assertEqual([], [item for item in self.validate() if item.code.startswith("E-RSK")])

    def test_validator_rejects_score_stage_and_stale_status_defects(self) -> None:
        self.raise_risk()
        path = self.risk_path()
        original = path.read_text(encoding="utf-8")
        path.write_text(original.replace("score = 12", "score = 11"), encoding="utf-8")
        self.assertTrue(any(item.code == "E-RSK-001" and "differs" in item.message for item in self.validate()))
        path.write_text(original.replace('stage = "implementation"', 'stage = "release"'), encoding="utf-8")
        self.assertTrue(any(item.code == "E-RSK-002" for item in self.validate()))
        stale = original.replace('status = "raised"', 'status = "identified"')
        stale = stale.split("[[lifecycle_events]]")[0].rstrip() + "\n+++\n" + original.split("+++", 2)[2]
        path.write_text(stale, encoding="utf-8")
        self.assertTrue(any(item.code == "E-RSK-003" for item in self.validate()))
        path.write_text(original, encoding="utf-8")
        policy = self.root / ".engineering-harness.toml"
        policy.write_text(policy.read_text(encoding="utf-8").replace("acceptance_level = 1", "acceptance_level = 40"), encoding="utf-8")
        self.assertTrue(any(item.code == "E-RSK-007" for item in self.validate()))

    def test_raise_risk_refuses_unknown_targets_and_bad_inputs(self) -> None:
        code, output, _ = self.invoke(
            "raise-risk", str(self.root), "--domain", "product", "--id", "RISK-PRD-009", "--title", "x",
            "--stage", "implementation", "--category", "process", "--likelihood", "3", "--impact", "3",
            "--threatens", "WO-999", "--json",
        )
        self.assertEqual(2, code)
        self.assertIn("does not exist", json.loads(output)["restitution"]["blocked_by"][0])
        code, output, _ = self.invoke(
            "raise-risk", str(self.root), "--domain", "product", "--id", "RISK-PRD-009", "--title", "x",
            "--stage", "implementation", "--category", "process", "--likelihood", "9", "--impact", "3",
            "--threatens", "WO-001", "--json",
        )
        self.assertEqual(2, code)
        self.assertFalse(self.risk_path("RISK-PRD-009").exists())

    # ---------------------------------------------------------------- REQ-RSK-004 / 006 (gates, scope exception)

    def test_raised_risk_blocks_handoff_until_disposed_and_its_file_is_admitted_in_scope(self) -> None:
        self.in_progress_work_order()
        self.raise_risk()
        evidence = self.root / "docs/engineering/product/evidence/WO-001/WO-001-verification.md"
        evidence.parent.mkdir(parents=True, exist_ok=True)
        risk_relative = "docs/engineering/product/risks/RISK-PRD-001.md"

        def check() -> dict:
            code, output, error = self.invoke(
                "check", str(self.root), "--artifact", "WO-001", "--checkpoint", "handoff",
                "--changed-path", "src/main.py", "--changed-path", risk_relative,
                "--changes-complete", "--json",
            )
            self.assertIn(code, (0, 1), error)
            return json.loads(output)

        result = check()
        predicates = {p["id"]: p for gate in result["compliance"]["gates"] for p in gate["predicates"]}
        self.assertEqual("pass", predicates["QGP-G4I-PATHS"]["status"], predicates["QGP-G4I-PATHS"])
        self.assertEqual("fail", predicates["QGP-G4I-RISK"]["status"])
        self.assertIn("RISK-PRD-001 (raised, score 12 at level 1)", predicates["QGP-G4I-RISK"]["message"])
        self.assertIn("engineering-owner", predicates["QGP-G4I-RISK"]["message"])
        self.assertTrue(any(item.startswith("QGP-G4I-RISK:") for item in result["restitution"]["blocked_by"]))

        code, _, error = self.invoke(
            "transition", str(self.root), "--set", "RISK-PRD-001=mitigating",
            "--decision", "RISK-PRD-001=engineering-owner",
            "--reason", "RISK-PRD-001=mitigated_by WO-001: add the orphan diagnostic", "--apply",
        )
        self.assertEqual(0, code, error)
        text = self.risk_path().read_text(encoding="utf-8")
        self.assertIn('status = "mitigating"', text)
        self.assertIn('mitigated_by = ["WO-001"]', text)
        result = check()
        predicates = {p["id"]: p for gate in result["compliance"]["gates"] for p in gate["predicates"]}
        self.assertEqual("pass", predicates["QGP-G4I-RISK"]["status"])
        # a disposed risk file is no longer admitted by the exception
        self.assertEqual("fail", predicates["QGP-G4I-PATHS"]["status"])

    def test_disposition_is_refused_for_the_wrong_role_or_without_the_required_fields(self) -> None:
        self.raise_risk()
        base = ["transition", str(self.root), "--set", "RISK-PRD-001=accepted"]
        code, output, error = self.invoke(*base, "--decision", "RISK-PRD-001=release-owner", "--reason", "RISK-PRD-001=fine", "--apply")
        self.assertEqual(1, code)
        self.assertIn("engineering-owner", output + error)
        self.assertIn("DR-RISK-DISPOSE", output + error)
        code, output, error = self.invoke(*base, "--decision", "RISK-PRD-001=engineering-owner", "--apply")
        self.assertEqual(1, code)
        self.assertIn("requires --reason", output + error)
        code, output, error = self.invoke(
            "transition", str(self.root), "--set", "RISK-PRD-001=avoided",
            "--decision", "RISK-PRD-001=engineering-owner", "--reason", "RISK-PRD-001=we changed the plan", "--apply",
        )
        self.assertEqual(1, code)
        self.assertIn("avoided_by ADR-", output + error)
        code, output, error = self.invoke(
            "transition", str(self.root), "--set", "RISK-PRD-001=mitigating",
            "--decision", "RISK-PRD-001=engineering-owner", "--reason", "RISK-PRD-001=someone will fix it", "--apply",
        )
        self.assertEqual(1, code)
        self.assertIn("mitigated_by", output + error)
        self.assertIn('status = "raised"', self.risk_path().read_text(encoding="utf-8"))
        code, _, error = self.invoke(*base, "--decision", "RISK-PRD-001=engineering-owner", "--reason", "RISK-PRD-001=residual accepted: the diagnostic lands next release", "--apply")
        self.assertEqual(0, code, error)
        self.assertIn('status = "accepted"', self.risk_path().read_text(encoding="utf-8"))

    def test_mitigated_requires_verified_coverage_and_a_recorded_residual(self) -> None:
        self.raise_risk()
        code, _, error = self.invoke(
            "transition", str(self.root), "--set", "RISK-PRD-001=mitigating",
            "--decision", "RISK-PRD-001=engineering-owner", "--reason", "RISK-PRD-001=mitigated_by WO-001", "--apply",
        )
        self.assertEqual(0, code, error)
        code, output, error = self.invoke(
            "transition", str(self.root), "--set", "RISK-PRD-001=mitigated",
            "--decision", "RISK-PRD-001=engineering-owner", "--reason", "RISK-PRD-001=residual 1x2 accepted for now", "--apply",
        )
        self.assertEqual(1, code)
        self.assertIn("not covered by a verified record", output + error)
        write(
            self.root / "docs/engineering/product/verification-records/VREC-001.md",
            formal(
                "VREC-001", "verification_record", "verified",
                {"verifies_work_order": ["WO-001"], "conforms_to": ["VER-001"]},
                f'commit = "{"a" * 40}"\ngit_object_format = "sha1"\nworktree_state = "clean"\n'
                'prepared_at = "2026-08-20T10:00:00Z"\nprepared_by = "quality-owner"\n'
                f'artifact_snapshot_sha256 = "{"b" * 64}"\n'
                'evidence_paths = ["docs/engineering/product/evidence/WO-001-verification.md"]\n'
                'verified_at = "2026-08-21T10:00:00Z"\nverified_by = "quality-owner"',
            ).replace('owners = ["owner"]', 'owners = ["quality-owner"]'),
        )
        code, output, error = self.invoke(
            "transition", str(self.root), "--set", "RISK-PRD-001=mitigated",
            "--decision", "RISK-PRD-001=engineering-owner", "--reason", "RISK-PRD-001=residual 2x3 remains", "--apply",
        )
        self.assertEqual(1, code)
        self.assertIn("residual is accepted", output + error)
        code, _, error = self.invoke(
            "transition", str(self.root), "--set", "RISK-PRD-001=mitigated",
            "--decision", "RISK-PRD-001=engineering-owner", "--reason", "RISK-PRD-001=residual 2x3 accepted by the engineering owner", "--apply",
        )
        self.assertEqual(0, code, error)
        text = self.risk_path().read_text(encoding="utf-8")
        self.assertIn('status = "mitigated"', text)
        self.assertIn('residual_likelihood = "2"', text)
        self.assertIn('residual_impact = "3"', text)
        self.assertEqual([], [item for item in self.validate() if item.code.startswith("E-RSK")])

    # ---------------------------------------------------------------- REQ-RSK-005 (release) and surfaces

    def test_prepare_release_refuses_undisposed_risks(self) -> None:
        from se_harness.installer import HarnessError
        from se_harness.provenance import prepare_release

        self.raise_risk()
        with self.assertRaises(HarnessError) as raised:
            prepare_release(
                self.root, record_id="RLS-PRD-001", release_contract_id="REL-001",
                verification_record_ids=["VREC-001"], work_order_ids=["WO-001"],
                version="1.0.0", authorized_by="release-owner", tag=None, output=None,
            )
        message = str(raised.exception)
        self.assertTrue("RISK-PRD-001" in message or "artifact" in message, message)

    def test_risks_command_focus_inspect_and_dashboard_surface_the_register(self) -> None:
        self.raise_risk()
        code, output, error = self.invoke("risks", str(self.root), "--artifact", "WO-001", "--json")
        self.assertEqual(0, code, error)
        register = json.loads(output)
        self.assertEqual("se-harness-risk-register-v1", register["schema"])
        self.assertEqual(["RISK-PRD-001"], [row["id"] for row in register["risks"]])
        self.assertEqual("engineering-owner", register["risks"][0]["disposing_role"])
        code, output, error = self.invoke("focus", str(self.root), "--artifact", "RISK-PRD-001", "--json")
        self.assertEqual(0, code, error)
        focus = json.loads(output)
        self.assertEqual("WFL-RISK-RAISED", focus["compliance"]["workflow_rule_id"])
        self.assertEqual("STEP-RISK-DISPOSE", focus["restitution"]["next"]["step_id"])
        self.assertIn("WO-001", focus["scope"]["governing"])
        code, output, error = self.invoke("inspect", str(self.root), "--json")
        self.assertEqual(0, code, error)
        queue = json.loads(output)["queues"]["decision_required"]
        self.assertIn(("RISK-PRD-001", "dispose-risk"), [(item["id"], item["action"]) for item in queue])
        code, output, error = self.invoke("dashboard", str(self.root))
        self.assertEqual(0, code, error + output)
        manifest = json.loads((self.root / "target/harness-dashboard/dashboard-manifest.json").read_text(encoding="utf-8"))
        self.assertTrue(manifest["repository"]["valid"], manifest["repository"])
        catalog = "".join(
            path.read_text(encoding="utf-8")
            for path in (self.root / "target/harness-dashboard/data/artifacts").rglob("*")
            if path.is_file()
        )
        self.assertIn("RISK-PRD-001", catalog)


if __name__ == "__main__":
    unittest.main()


class RiskDeviationClosureTests(unittest.TestCase):
    """Evidence for REQ-RSK-007 / SPEC-RSK-002: guard operation, doctor check, skill integration, amendments."""

    def test_raise_risk_is_a_registered_guard_operation_and_uses_it(self) -> None:
        from se_harness import mutation_guard
        from se_harness.artifact_layout import create_risk

        self.assertIn("raise-risk", mutation_guard.PUBLIC_MUTATION_OPERATIONS)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.assertEqual(0, main(["init", str(root), "--project-name", "Guard Fixture"]))
            create_base_chain(root, operating_contract_status="draft")
            seen: list[str] = []

            def fake(repository, *, operation, **_):
                seen.append(operation)
                return trusted_mutation_authority(repository, operation=operation)

            with mock.patch("se_harness.mutation_guard.require_mutation_authority", side_effect=fake):
                create_risk(
                    root, domain="product", artifact_id="RISK-PRD-001", title="t", stage="implementation",
                    category="process", likelihood=2, impact=2, threatens=["WO-001"], cause="c", effect="e",
                    raised_by="test", acceptance_level=1, now="2026-08-25T00:00:00Z", dry_run=False,
                )
            self.assertEqual(["raise-risk"], seen)

    def test_doctor_reports_c_rsk_001_only_for_an_invalid_risk_section(self) -> None:
        from se_harness.preflight import inspect_installation, risk_policy_check

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.assertEqual(0, main(["init", str(root), "--project-name", "Doctor Fixture"]))
            check = risk_policy_check(root)
            self.assertTrue(check.passed, check)
            self.assertIn("acceptance level 1", check.detail)
            self.assertIn("risk-policy", [item.name for item in inspect_installation(root)])
            policy = root / ".engineering-harness.toml"
            original = policy.read_text(encoding="utf-8")
            policy.write_text(original.replace("acceptance_level = 1", "acceptance_level = 40"), encoding="utf-8")
            check = risk_policy_check(root)
            self.assertFalse(check.passed)
            self.assertIn("C-RSK-001", check.detail)
            self.assertIn("40", check.detail)
            failing = [item for item in inspect_installation(root) if item.name == "risk-policy"]
            self.assertEqual(1, len(failing))
            self.assertFalse(failing[0].passed)
            policy.write_text(original.replace("[risk]\n", "[risk]\nunexpected = 1\n"), encoding="utf-8")
            self.assertFalse(risk_policy_check(root).passed)
            policy.write_text(original.split("[risk]")[0], encoding="utf-8")
            self.assertTrue(risk_policy_check(root).passed)

    def test_skill_contracts_require_the_risk_operations_and_permit_risk_raise(self) -> None:
        from se_harness.skill_contract import load_skill_contract

        skills = Path(__file__).resolve().parents[1] / "templates/repository/standard/.agents/skills"
        draft = load_skill_contract(skills / "harness-draft-change/skill-contract.json").value
        execute = load_skill_contract(skills / "harness-execute-work-order/skill-contract.json").value
        prepare = load_skill_contract(skills / "harness-prepare-assurance/skill-contract.json").value
        self.assertIn("raise-risk", draft["evaluator"]["required_operations"])
        self.assertIn("raise-risk", execute["evaluator"]["required_operations"])
        self.assertIn("risks", prepare["evaluator"]["required_operations"])
        self.assertIn("risk-raise", draft["effects"]["permitted"])
        self.assertIn("risk-raise", execute["effects"]["permitted"])
        self.assertNotIn("risk-raise", prepare["effects"]["permitted"])
        for value in (draft, execute, prepare):
            self.assertEqual("1.0.2", value["version"])
            self.assertEqual([], value["effects"]["lifecycle_transitions"])
        for name in ("harness-draft-change", "harness-execute-work-order", "harness-prepare-assurance"):
            text = (skills / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("never", text)
            self.assertIn("disposes a risk", text)

    def test_helpers_admit_risk_raise_only_for_new_risk_paths(self) -> None:
        import types

        skills = Path(__file__).resolve().parents[1] / "templates/repository/standard/.agents/skills"

        def load(name: str, path: Path):
            # exec the source directly: importing would write __pycache__ into the portable core,
            # and every file under a core is bound by its manifest digest
            module = types.ModuleType(name)
            module.__file__ = str(path)
            exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"), module.__dict__)
            return module

        scope = load("rsk_check_scope", skills / "harness-execute-work-order/scripts/check_scope.py")
        guard = load("rsk_guard", skills / "harness-draft-change/scripts/guard.py")
        risk_path = "docs/engineering/product/risks/RISK-PRD-001.md"
        base = {
            "explicit_skill": "harness-execute-work-order", "work_order": "WO-PRD-001", "state": "in_progress",
            "execution_scope": ["src/"],
        }
        expected = {"work_order": "WO-PRD-001", "state": "in_progress", "scope_sha256": scope.scope_digest(("src/",))}
        admitted = scope.admit_work_order_effect(
            {**base, "effect_class": "risk-raise", "planned_paths": [risk_path]},
            recheck=lambda: expected, effect=lambda planned: planned,
        )
        self.assertEqual((risk_path,), admitted)
        with self.assertRaisesRegex(Exception, "AEXEXE011"):
            scope.admit_work_order_effect(
                {**base, "effect_class": "risk-raise", "planned_paths": [risk_path, "src/main.py"]},
                recheck=lambda: expected, effect=lambda planned: planned,
            )
        with self.assertRaisesRegex(Exception, "AEXEXE009"):
            scope.admit_work_order_effect(
                {**base, "effect_class": "implementation-write", "planned_paths": [risk_path]},
                recheck=lambda: expected, effect=lambda planned: planned,
            )
        draft_base = {"explicit_skill": "harness-draft-change", "allowed_paths": [risk_path], "revisions": {}}
        admitted = guard.admit_draft_effect(
            {**draft_base, "effect_class": "risk-raise", "planned_paths": [risk_path]},
            recheck=lambda: {"allowed_paths": [risk_path], "revisions": {}}, effect=lambda planned: planned,
        )
        self.assertEqual((risk_path,), admitted)
        with self.assertRaisesRegex(Exception, "AEXDRF013"):
            guard.admit_draft_effect(
                {"explicit_skill": "harness-draft-change", "effect_class": "risk-raise",
                 "planned_paths": ["docs/notes/x.md"], "allowed_paths": ["docs/notes/x.md"], "revisions": {}},
                recheck=lambda: {"allowed_paths": ["docs/notes/x.md"], "revisions": {}},
                effect=lambda planned: planned,
            )

    def test_amendments_are_the_shipped_behaviour(self) -> None:
        from se_harness.workflow_contract import load_validated_contracts

        _, _, _, procedures, _ = load_validated_contracts()
        with_step = {pid for pid, proc in procedures.items() if any(s["id"].endswith("-RISKS") for s in proc["steps"])}
        self.assertEqual({"PROC-WO-START", "PROC-WO-IMPLEMENT"}, with_step)
        template = Path(__file__).resolve().parents[1] / "templates/repository/standard/docs/engineering/templates/RISK.template.md"
        self.assertNotIn("residual_likelihood =", template.read_text(encoding="utf-8").split("[risk]")[1].split("[relations]")[0])
