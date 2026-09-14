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



    def test_renderer_explains_a_blocked_result(self) -> None:
        human = render_human(self.result(blocked=True))
        self.assertIn("Evidence is missing", human)
        self.assertIn("WO-001", human)

    def test_direct_renderer_and_json_derive_from_one_semantic_result(self) -> None:
        result = self.result()
        decoded = json.loads(render_json(result))
        self.assertEqual(result, decoded)
        human = render_human(decoded)
        for value in decoded["restitution"]["done"] + decoded["restitution"]["current_lifecycle_state"]:
            self.assertIn(value, human)
        for argument in decoded["restitution"]["command_or_response"]["argv"]:
            self.assertIn(argument, human)

    def test_wording_changes_do_not_change_machine_identity(self) -> None:
        from copy import deepcopy
        from se_harness.workflow_result import restitution_digest
        result = self.result()
        result["candidate"] = {"commit": "a" * 40, "git_object_format": "sha1"}
        result["state"]["after"] = [{"id": "WO-001", "status": "implemented"}]
        result["restitution"]["decision_required"] = {"decision_right": "DR-WO-COMPLETE", "role": "engineering-owner",
            "artifact": "WO-001", "decision": "whether implementation is complete", "outcomes": ["implemented", "continue"]}
        baseline = restitution_digest(result)
        wording = deepcopy(result)
        wording["restitution"]["done"] = ["Checks passed. Now review the evidence."]
        wording["restitution"]["next"]["action"] = "Review this next"
        wording["restitution"]["current_lifecycle_state"] = ["The work is implemented."]
        wording["restitution"]["decision_required"]["decision"] = "whether the work is done"
        self.assertNotEqual(render_human(result), render_human(wording))
        self.assertEqual(baseline, restitution_digest(wording))
        for change in ("candidate", "state", "argv"):
            with self.subTest(change=change):
                changed = deepcopy(result)
                if change == "candidate":
                    changed["candidate"]["commit"] = "b" * 40
                elif change == "state":
                    changed["state"]["after"][0]["status"] = "verified"
                else:
                    changed["restitution"]["command_or_response"]["argv"].append("--apply")
                self.assertNotEqual(baseline, restitution_digest(changed))

    def test_retained_schema_two_digest_still_uses_its_original_format(self) -> None:
        import hashlib
        from se_harness.workflow_result import canonical_block_bytes, restitution_digest
        result = self.result()
        result.pop("digest_format")
        self.assertEqual(hashlib.sha256(canonical_block_bytes(result)).hexdigest(), restitution_digest(result))

    def test_direct_renderer_rejects_completed_result_with_blocker(self) -> None:
        result = self.result()
        result["restitution"]["blocked_by"] = ["unexpected"]
        with self.assertRaisesRegex(ValueError, "WEX230"):
            render_human(result)


if __name__ == "__main__":
    unittest.main()
