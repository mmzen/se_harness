from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from se_harness.cli import main
from se_harness.preflight import _load_validator_module
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
        self.assertEqual(
            [
                "completed",
                "current_lifecycle_state",
                "recommended_next_step",
                "human_decision_or_approval_required",
                "command_or_suggested_response",
                "alternative_next_steps",
            ],
            contract["handoff_fields"],
        )
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
                ("change-bundle-apply", None, "in_progress", "in_progress"),
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
                self.assertEqual(set(contract["handoff_fields"]), set(rule["handoff"]))
                self.assertIsInstance(rule["selector"]["artifact_types"], list)
                self.assertIsInstance(rule["selector"]["statuses"], list)
                self.assertIsInstance(rule["gate_ids"], list)
                self.assertRegex(rule["procedure_id"], r"^PROC-[A-Z0-9-]+$")
                self.assertIsInstance(rule["alternative_procedure_ids"], list)
                self.assertRegex(rule["decision_right"], r"^DR-[A-Z0-9-]+$")
                self.assertIsInstance(rule["effects"], list)
                self.assertIsInstance(rule["non_effects"], list)
                self.assertEqual(
                    {"action", "detail"},
                    set(rule["handoff"]["recommended_next_step"]),
                )
        failure = contract["failure"]
        self.assertEqual("WFL-FAIL-REMEDIATE", failure["id"])
        self.assertEqual(set(contract["handoff_fields"]), set(failure["handoff"]))
        self.assertEqual(["failed"], failure["selector"]["outcomes"])
        self.assertRegex(failure["procedure_id"], r"^PROC-[A-Z0-9-]+$")
        workflow, quality, rules, procedures, gates = load_validated_contracts()
        self.assertEqual(contract, workflow)
        self.assertEqual(load_quality_gate_contract(), quality)
        self.assertEqual(set(identifiers), set(rules))
        self.assertGreaterEqual(len(procedures), len(rules))
        self.assertGreaterEqual(len(gates), 10)

    def test_every_contract_reference_resolves_to_one_normative_owner(self) -> None:
        workflow = (ENGINEERING_ROOT / "WORKFLOW.md").read_text(encoding="utf-8")
        gates = (ENGINEERING_ROOT / "QUALITY_GATES.md").read_text(encoding="utf-8")
        rights = (ENGINEERING_ROOT / "DECISION_RIGHTS.md").read_text(encoding="utf-8")
        for rule in WORKFLOW_CONTRACT["recommendations"]:
            with self.subTest(rule=rule["id"]):
                self.assertEqual(1, workflow.count(f"`{rule['id']}`"))
                self.assertEqual(1, rights.count(f"`{rule['decision_right']}`"))
                self.assertGreaterEqual(workflow.count(f"`{rule['procedure_id']}`"), 1)
                for gate_id in rule["gate_ids"]:
                    self.assertGreaterEqual(gates.count(f"`{gate_id}`"), 1)
        failure = WORKFLOW_CONTRACT["failure"]
        self.assertEqual(1, workflow.count(f"`{failure['id']}`"))
        self.assertEqual(1, rights.count(f"`{failure['decision_right']}`"))

        _, _, _, procedures, quality_gates = load_validated_contracts()
        for procedure_id, procedure in procedures.items():
            self.assertGreaterEqual(workflow.count(f"`{procedure_id}`"), 1)
            for step in procedure["steps"]:
                self.assertGreaterEqual(workflow.count(f"`{step['id']}`"), 1)
        for gate_id, gate in quality_gates.items():
            self.assertGreaterEqual(gates.count(f"`{gate_id}`"), 1)
            for predicate in gate["predicates"]:
                self.assertGreaterEqual(gates.count(f"`{predicate['id']}`"), 1)

    def test_runtime_and_repository_validator_use_the_same_transitions(self) -> None:
        validator = _load_validator_module()
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
            standard_repository(target, "Contract Fixture")
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
        paths = (
            STANDARD_ROOT / "ENGINEERING_HARNESS.md.tpl",
            ENGINEERING_ROOT / "DECISION_RIGHTS.md",
            ENGINEERING_ROOT / "WORKFLOW.md",
            ENGINEERING_ROOT / "QUALITY_GATES.md",
            ENGINEERING_ROOT / "TRACEABILITY.md",
        )
        forbidden = ("etc.", "as appropriate", "where possible", "when possible", "best effort")
        for path in paths:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertIn("BCP 14", text)
                self.assertIn("RFC 2119", text)
                self.assertIn("RFC 8174", text)
                self.assertTrue(any(prefix in text for prefix in ("HRN-", "DR-", "WFL-", "QG-", "TRC-")))
                self.assertTrue(text.isascii())
                for phrase in forbidden:
                    self.assertNotIn(phrase, text.lower())

    def test_handoff_policy_separates_structured_authority_from_presentation(self) -> None:
        router = (STANDARD_ROOT / "ENGINEERING_HARNESS.md.tpl").read_text(encoding="utf-8")
        workflow = (ENGINEERING_ROOT / "WORKFLOW.md").read_text(encoding="utf-8")
        agents = (STANDARD_ROOT / "AGENTS.md.fragment").read_text(encoding="utf-8")
        claude = (STANDARD_ROOT / "CLAUDE.md.fragment").read_text(encoding="utf-8")

        self.assertIn("The structured\nresult is authoritative", router)
        self.assertIn("SHOULD summarize the result clearly", router)
        self.assertIn("MAY adapt wording and structure", router)
        self.assertIn("deterministic human renderer directly", router)
        self.assertIn("Model transcription MUST NOT", router)

        for phrase in (
            "structured result is authoritative",
            "observed effects from incomplete expected effects",
            "every exact blocker and every material non-effect",
            "exactly one current typed procedure step",
            "command argument values and boundaries",
            "workflow-declared complete alternatives",
            "direct renderer's existing headings",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, workflow)

        self.assertIn("schema-2 structured result as\nauthoritative", agents)
        self.assertIn("authoritative schema-2 result", claude)
        for text in (router, workflow, agents, claude):
            self.assertNotIn("block verbatim", text)
            self.assertNotIn("restitution verbatim", text)


if __name__ == "__main__":
    unittest.main()
