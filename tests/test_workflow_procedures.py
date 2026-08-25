from __future__ import annotations

import copy
import inspect
import unittest

from se_harness.workflow_contract import ContractError, load_validated_contracts, validate_contracts
from se_harness.workflow_procedures import ProcedureError, resolve_procedure


class WorkflowProcedureTests(unittest.TestCase):
    def test_standard_start_procedure_has_exact_order_and_argv(self) -> None:
        _, _, _, procedures, _ = load_validated_contracts()
        resolved = resolve_procedure(procedures, "PROC-WO-START", {"artifact_id": "WO-ABC-001"})
        self.assertEqual(
            [
                "STEP-WO-START-FOCUS",
                "STEP-WO-START-PREFLIGHT",
                "STEP-WO-START-RISKS",
                "STEP-WO-START-DECIDE",
                "STEP-WO-START-PREVIEW",
                "STEP-WO-START-APPLY",
                "STEP-WO-START-FINAL-FOCUS",
            ],
            [step["id"] for step in resolved["steps"]],
        )
        self.assertEqual(
            ["harnessctl", "preflight", ".", "--work-order", "WO-ABC-001", "--phase", "start"],
            resolved["steps"][1]["argv"],
        )
        self.assertEqual("decision", resolved["steps"][3]["kind"])
        self.assertEqual("DR-WO-START", resolved["steps"][3]["decision_right"])

    def test_shell_metacharacters_remain_one_inert_text_argument(self) -> None:
        procedure = {
            "id": "PROC-TEST",
            "parameters": [{"name": "value", "type": "text", "cardinality": "one", "source": "test"}],
            "steps": [{
                "id": "STEP-TEST",
                "kind": "command",
                "argv": ["tool", "--value", "{value}"],
                "gate_ids": [],
                "effects": [],
                "non_effects": [],
            }],
        }
        hostile = '$(command); echo "quoted" > output'
        resolved = resolve_procedure({"PROC-TEST": procedure}, "PROC-TEST", {"value": hostile})
        self.assertEqual(["tool", "--value", hostile], resolved["steps"][0]["argv"])

    def test_missing_parameter_blocks_before_command_resolution(self) -> None:
        _, _, _, procedures, _ = load_validated_contracts()
        with self.assertRaisesRegex(ProcedureError, "WEX221"):
            resolve_procedure(procedures, "PROC-WO-START", {})

    def _reference_step(self, **overrides: object) -> dict[str, object]:
        step: dict[str, object] = {
            "id": "STEP-REFERENCE",
            "kind": "reference",
            "gate_ids": [],
            "effects": [],
            "non_effects": [],
        }
        step.update(overrides)
        return step

    def test_reference_step_declaring_action_id_is_rejected_before_resolution(self) -> None:
        workflow, quality, _, _, _ = load_validated_contracts()
        for overrides in (
            {"action_id": "CTX-ACT-REPOSITORY-CHECKS"},
            {"action_id": "CTX-ACT-REPOSITORY-CHECKS", "procedure_id": workflow["procedures"][0]["id"]},
            {"action_id": "not-an-action-identifier"},
        ):
            with self.subTest(overrides=sorted(overrides)):
                mutated = copy.deepcopy(workflow)
                mutated["procedures"][0]["steps"][0] = self._reference_step(**overrides)
                with self.assertRaises(ContractError) as raised:
                    validate_contracts(mutated, quality)
                message = str(raised.exception)
                self.assertIn("action_id", message)
                self.assertIn("withdrawn", message)

    def test_reference_step_without_a_procedure_id_is_rejected(self) -> None:
        workflow, quality, _, _, _ = load_validated_contracts()
        mutated = copy.deepcopy(workflow)
        mutated["procedures"][0]["steps"][0] = self._reference_step()
        with self.assertRaisesRegex(ContractError, "must declare a procedure ID"):
            validate_contracts(mutated, quality)

    def test_resolver_exposes_no_repository_context_argument(self) -> None:
        parameters = inspect.signature(resolve_procedure).parameters
        self.assertEqual(["procedures", "procedure_id", "parameters"], list(parameters))

    def test_unknown_reference_and_cycles_invalidate_policy(self) -> None:
        workflow, quality, _, _, _ = load_validated_contracts()
        mutated = copy.deepcopy(workflow)
        mutated["procedures"][0]["steps"][0] = {
            "id": "STEP-CYCLE",
            "kind": "reference",
            "procedure_id": mutated["procedures"][0]["id"],
            "gate_ids": [],
            "effects": [],
            "non_effects": [],
        }
        with self.assertRaisesRegex(Exception, "cycle"):
            validate_contracts(mutated, quality)


if __name__ == "__main__":
    unittest.main()
