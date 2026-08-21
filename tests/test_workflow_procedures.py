from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from se_harness.workflow_contract import load_validated_contracts, validate_contracts
from se_harness.workflow_procedures import ProcedureError, context_actions, resolve_procedure


class WorkflowProcedureTests(unittest.TestCase):
    def test_standard_start_procedure_has_exact_order_and_argv(self) -> None:
        _, _, _, procedures, _ = load_validated_contracts()
        resolved = resolve_procedure(procedures, "PROC-WO-START", {"artifact_id": "WO-ABC-001"})
        self.assertEqual(
            [
                "STEP-WO-START-FOCUS",
                "STEP-WO-START-PREFLIGHT",
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
        self.assertEqual("decision", resolved["steps"][2]["kind"])
        self.assertEqual("DR-WO-START", resolved["steps"][2]["decision_right"])

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

    def test_context_action_markers_must_match_and_cannot_nest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "REPOSITORY_CONTEXT.md"
            path.write_text(
                "<!-- se-harness:action CTX-ACT-CHECK begin -->\nRun tests.\n"
                "<!-- se-harness:action CTX-ACT-CHECK end -->\n",
                encoding="utf-8",
            )
            self.assertEqual(("Run tests.",), context_actions(path)["CTX-ACT-CHECK"])
            path.write_text(
                "<!-- se-harness:action CTX-ACT-A begin -->\n"
                "<!-- se-harness:action CTX-ACT-B begin -->\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ProcedureError, "nested"):
                context_actions(path)

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
