from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from se_harness.engine import validate_engineering_artifacts
from se_harness.workflow_contract import load_quality_gate_contract, load_validated_contracts
from se_harness.workflow import LIFECYCLE_REGISTRY, TRANSITIONS, WORKFLOW_CONTRACT
from tests.fixture_support import standard_repository


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
STANDARD_ROOT = REPOSITORY_ROOT / "templates" / "repository" / "standard"
ENGINEERING_ROOT = STANDARD_ROOT / "docs" / "engineering"
RUNTIME_CONTRACT = REPOSITORY_ROOT / "se_harness" / "workflow_contract.json"
INSTALLED_CONTRACT = ENGINEERING_ROOT / "WORKFLOW.json"
RUNTIME_GATES = REPOSITORY_ROOT / "se_harness" / "quality_gates_contract.json"
INSTALLED_GATES = ENGINEERING_ROOT / "QUALITY_GATES.json"


class WorkflowDocumentationContractTests(unittest.TestCase):
    def test_integrity_policy_keeps_default_schema_and_bounded_plugin_exception(self) -> None:
        # Machine lock semantics remain unchanged; current routes need no pointer.
        from se_harness.integrity import LOCK_SCHEMA
        self.assertEqual(3,LOCK_SCHEMA)
        self.assertFalse((ENGINEERING_ROOT/'WORKFLOW.md').exists())
        workflow=(ENGINEERING_ROOT/'harness/CONTINUE.md').read_text(encoding='utf-8')
        self.assertIn('RECORD_STATE.md#',workflow)

    def test_runtime_and_installed_contracts_are_byte_identical(self) -> None:
        self.assertEqual(RUNTIME_CONTRACT.read_bytes(), INSTALLED_CONTRACT.read_bytes())
        self.assertEqual(RUNTIME_GATES.read_bytes(), INSTALLED_GATES.read_bytes())
        self.assertEqual(
            WORKFLOW_CONTRACT,
            json.loads(INSTALLED_CONTRACT.read_text(encoding="utf-8")),
        )

    def test_contract_is_closed_ordered_and_complete(self) -> None:
        contract = WORKFLOW_CONTRACT
        self.assertEqual("se-harness-workflow-v4", contract["schema"])
        self.assertEqual("BCP 14", contract["normative_language"])
        self.assertNotIn("handoff_fields", contract)
        self.assertEqual(
            [
                "outcome", "done", "not_done", "blocked_by",
                "current_lifecycle_state", "decision_required", "next",
                "command_or_response", "alternatives",
            ],
            contract["restitution_fields"],
        )
        self.assertEqual(
            [
                ("delegated-work-order-start", "DR-WO-START", "approved", "in_progress"),
                ("delegated-work-order-complete", "DR-WO-COMPLETE", "in_progress", "implemented"),
                ("delegated-vrec-prepare", "DR-VREC-PREPARE", "implemented", "implemented"),
            ],
            [
                (item["id"], item["decision_right"], item["current_status"], item["result_status"])
                for item in contract["agentic_operations"]
            ],
        )
        recommendations = contract["recommendations"]
        identifiers = [rule["id"] for rule in recommendations]
        self.assertEqual(len(identifiers), len(set(identifiers)))
        self.assertEqual("WFL-DEFAULT-REVIEW", identifiers[-1])
        for rule in recommendations:
            with self.subTest(rule=rule["id"]):
                self.assertRegex(rule["id"], r"^WFL-[A-Z0-9-]+$")
                self.assertNotIn("handoff", rule)
                self.assertEqual({"done", "current_lifecycle_state"}, set(rule["restitution"]))
                self.assertIsInstance(rule["selector"]["artifact_types"], list)
                self.assertIsInstance(rule["selector"]["statuses"], list)
                self.assertIsInstance(rule["gate_ids"], list)
                self.assertRegex(rule["procedure_id"], r"^PROC-[A-Z0-9-]+$")
                self.assertIsInstance(rule["alternative_procedure_ids"], list)
                self.assertRegex(rule["decision_right"], r"^DR-[A-Z0-9-]+$")
                self.assertIsInstance(rule["effects"], list)
                self.assertIsInstance(rule["non_effects"], list)
                for field in ("done", "current_lifecycle_state"):
                    self.assertIsInstance(rule["restitution"][field], list)
        failure = contract["failure"]
        self.assertEqual("WFL-FAIL-REMEDIATE", failure["id"])
        self.assertEqual({"done", "current_lifecycle_state"}, set(failure["restitution"]))
        self.assertEqual(["failed"], failure["selector"]["outcomes"])
        self.assertRegex(failure["procedure_id"], r"^PROC-[A-Z0-9-]+$")
        workflow, quality, rules, procedures, gates = load_validated_contracts()
        self.assertEqual(contract, workflow)
        self.assertEqual(load_quality_gate_contract(), quality)
        self.assertEqual(set(identifiers), set(rules))
        self.assertGreaterEqual(len(procedures), len(rules))
        self.assertGreaterEqual(len(gates), 10)

    def test_every_contract_reference_resolves_to_one_normative_owner(self) -> None:
        from se_harness.instruction_discovery import load_catalog,validate_coverage
        _,_,_,procedures,_=load_validated_contracts()
        validate_coverage(procedures)
        guide=(ENGINEERING_ROOT/'harness/CONTINUE.md').read_text(encoding='utf-8')
        rights=(ENGINEERING_ROOT/'harness/AUTHORITY.md').read_text(encoding='utf-8')
        for rule in WORKFLOW_CONTRACT['recommendations']:
            self.assertEqual(1,rights.count(f"`{rule['decision_right']}`"))
            self.assertIn(rule['procedure_id'],load_catalog()['procedures'])
        for pid,procedure in procedures.items():
            self.assertEqual(1,guide.count(f'`{pid}`'))
            for step in procedure['steps']:
                self.assertEqual(1,guide.count(f"`{step['id']}`"))

    def test_runtime_and_repository_validator_use_the_same_transitions(self) -> None:
        validator = validate_engineering_artifacts
        self.assertEqual(TRANSITIONS, validator.WORKFLOW_TRANSITIONS)
        for family, states in LIFECYCLE_REGISTRY.items():
            self.assertEqual(set(states), set(validator.WORKFLOW_LIFECYCLES[family]))
            for state, row in states.items():
                standalone = validator.WORKFLOW_LIFECYCLES[family][state]
                self.assertEqual(row.transitions_to, standalone.transitions_to)
                self.assertEqual(row.grants_authority, standalone.grants_authority)
                self.assertEqual(row.reserves_version, standalone.reserves_version)
                self.assertEqual(row.transitionable, standalone.transitionable)
                self.assertEqual(row.must_remain_visible, standalone.must_remain_visible)
                self.assertEqual(row.predecessor_adapter, standalone.predecessor_adapter)

    def test_fresh_install_contains_managed_machine_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary)
            standard_repository(target)
            installed = target / "docs" / "engineering" / "WORKFLOW.json"
            expected_workflow = INSTALLED_CONTRACT.read_text(encoding="utf-8").encode("utf-8")
            expected_gates = INSTALLED_GATES.read_text(encoding="utf-8").encode("utf-8")
            self.assertEqual(expected_workflow, installed.read_bytes())
            self.assertEqual(
                expected_gates,
                (target / "docs" / "engineering" / "QUALITY_GATES.json").read_bytes(),
            )
            lock = json.loads((target / ".engineering-harness.lock").read_text(encoding="utf-8"))
            self.assertEqual("managed", lock["files"]["docs/engineering/WORKFLOW.json"]["mode"])
            self.assertEqual("managed", lock["files"]["docs/engineering/QUALITY_GATES.json"]["mode"])

    def test_core_documents_declare_bcp14_and_stable_rules(self) -> None:
        root=(STANDARD_ROOT/'ENGINEERING_HARNESS.md.tpl').read_text(encoding='utf-8')
        for phrase in ('BCP 14','RFC 2119','RFC 8174'):
            self.assertIn(phrase,root)
        for i in range(1,10):self.assertIn(f'HRN-{i:03d}',root)
        for name in ('DECISION_RIGHTS.md','WORKFLOW.md','QUALITY_GATES.md','TRACEABILITY.md','TECHNICAL_COMMUNICATION.md'):
            self.assertFalse((ENGINEERING_ROOT/name).exists())




if __name__ == "__main__":
    unittest.main()
