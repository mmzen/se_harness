from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from validate_engineering_artifacts import (  # noqa: E402
    Artifact,
    validate_work_order_assurance,
    work_order_assurance_state,
)


MISSING = object()


def artifact(
    *,
    status: str = "draft",
    assurance: object = MISSING,
    artifact_type: str = "work_order",
) -> Artifact:
    metadata: dict[str, object] = {
        "id": "WO-WAC-900" if artifact_type == "work_order" else "REQ-WAC-900",
        "type": artifact_type,
        "title": "Fixture",
        "status": status,
        "owners": ["owner"],
        "created": "2026-08-16",
        "updated": "2026-08-16",
        "relations": {},
    }
    if assurance is not MISSING:
        metadata["assurance"] = assurance
    return Artifact(Path("fixture.md"), metadata, "")


def valid_assurance(value: str = "required") -> dict[str, str]:
    return {
        "commit_bound_verification": value,
        "rationale": "Future decisions rely on the changed trusted state.",
        "decided_by": "quality-owner",
    }


class WorkOrderAssuranceValidationTests(unittest.TestCase):
    def test_valid_contract_is_normalized_without_judging_the_claim(self) -> None:
        state = work_order_assurance_state(
            artifact(
                status="approved",
                assurance={
                    "commit_bound_verification": " required ",
                    "rationale": "  Accountable rationale.  ",
                    "decided_by": " quality-owner ",
                },
            )
        )
        self.assertEqual("valid", state["state"])
        self.assertEqual("required", state["commit_bound_verification"])
        self.assertEqual("Accountable rationale.", state["rationale"])
        self.assertEqual("quality-owner", state["decided_by"])
        self.assertEqual([], state["issues"])

        not_required = work_order_assurance_state(
            artifact(assurance=valid_assurance("not_required"))
        )
        self.assertEqual("valid", not_required["state"])

    def test_actionable_work_requires_a_declaration_but_legacy_completion_does_not(self) -> None:
        required_statuses = {"approved", "in_progress"}
        compatible_statuses = {
            "draft",
            "ready",
            "implemented",
            "verified",
            "released",
            "rejected",
            "superseded",
        }
        for status in sorted(required_statuses | compatible_statuses):
            with self.subTest(status=status):
                errors = validate_work_order_assurance([artifact(status=status)], Path.cwd())
                if status in required_statuses:
                    self.assertEqual(["E019"], [item.code for item in errors])
                    self.assertEqual({"governance"}, {item.plane for item in errors})
                else:
                    self.assertEqual([], errors)

    def test_malformed_present_contract_is_rejected_in_every_lifecycle_state(self) -> None:
        malformed = (
            "required",
            {},
            {
                "commit_bound_verification": "optional",
                "rationale": "",
                "decided_by": "",
                "typo": "ignored",
            },
        )
        for status in ("draft", "implemented", "rejected"):
            for value in malformed:
                with self.subTest(status=status, value=value):
                    errors = validate_work_order_assurance(
                        [artifact(status=status, assurance=value)], Path.cwd()
                    )
                    self.assertTrue(errors)
                    self.assertEqual({"E019"}, {item.code for item in errors})

    def test_assurance_table_is_work_order_only_and_bounded(self) -> None:
        non_work = validate_work_order_assurance(
            [artifact(artifact_type="requirement", assurance=valid_assurance())],
            Path.cwd(),
        )
        self.assertEqual(1, len(non_work))
        self.assertIn("only on work-order", non_work[0].message)

        too_long = valid_assurance()
        too_long["rationale"] = "x" * 2001
        errors = validate_work_order_assurance(
            [artifact(status="approved", assurance=too_long)], Path.cwd()
        )
        self.assertEqual(1, len(errors))
        self.assertIn("exceeds 2000", errors[0].message)


if __name__ == "__main__":
    unittest.main()
