from __future__ import annotations

import json
import unittest

from se_harness.workflow_result import build_result, render_human, render_json


class WorkflowRestitutionTests(unittest.TestCase):
    def result(self, *, blocked: bool = False) -> dict:
        outcome = "blocked" if blocked else "completed"
        return build_result(
            operation="check",
            outcome=outcome,
            primary="WO-001",
            artifacts=["WO-001"],
            governing=["REQ-001"],
            dependencies=[],
            declared_paths=["src/"],
            changed_paths=["src/main.py"],
            change_set_complete=True,
            compliance={
                "checkpoint": "handoff",
                "workflow_rule_id": "WFL-WO-IMPLEMENT",
                "procedure_id": "PROC-WO-IMPLEMENT",
                "status": "fail" if blocked else "pass",
                "gates": [],
            },
            procedure={"id": "PROC-WO-IMPLEMENT", "current_step": "STEP-NEXT", "steps": []},
            restitution={
                "outcome": outcome,
                "done": ["Evaluated handoff compliance for WO-001."],
                "not_done": ["Implementation evidence remains incomplete."] if blocked else [],
                "blocked_by": ["QGP-EVIDENCE: Evidence is missing."] if blocked else [],
                "current_lifecycle_state": ["WO-001 is in_progress."],
                "decision_required": None,
                "next": {
                    "procedure_id": "PROC-WO-IMPLEMENT",
                    "step_id": "STEP-NEXT",
                    "action": "Run the bound command",
                },
                "command_or_response": {
                    "kind": "command",
                    "argv": ["harnessctl", "check", ".", "--artifact", "WO-001"],
                },
                "alternatives": [],
            },
        )

    def test_success_headings_are_exact_and_ordered(self) -> None:
        human = render_human(self.result())
        headings = [
            "Outcome", "Done", "Not done", "Current lifecycle state",
            "Decision required", "Next", "Command or response",
        ]
        positions = [human.index(heading) for heading in headings]
        self.assertEqual(sorted(positions), positions)
        self.assertNotIn("Blocked by\n", human)
        self.assertNotIn("Background", human)
        self.assertIn("Not done\nNone.", human)

    def test_blocked_output_has_exact_blocker_and_no_extra_sections(self) -> None:
        human = render_human(self.result(blocked=True))
        self.assertIn("Blocked by\n- QGP-EVIDENCE: Evidence is missing.", human)
        self.assertLess(human.index("Not done"), human.index("Blocked by"))
        self.assertLess(human.index("Blocked by"), human.index("Current lifecycle state"))
        self.assertFalse(human.startswith("Here"))

    def test_json_and_human_derive_from_one_semantic_result(self) -> None:
        result = self.result()
        decoded = json.loads(render_json(result))
        self.assertEqual(result, decoded)
        human = render_human(decoded)
        for value in decoded["restitution"]["done"] + decoded["restitution"]["current_lifecycle_state"]:
            self.assertIn(value, human)
        for argument in decoded["restitution"]["command_or_response"]["argv"]:
            self.assertIn(argument, human)

    def test_restitution_rejects_completed_result_with_blocker(self) -> None:
        result = self.result()
        result["restitution"]["blocked_by"] = ["unexpected"]
        with self.assertRaisesRegex(ValueError, "WEX230"):
            render_human(result)


if __name__ == "__main__":
    unittest.main()
