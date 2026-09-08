from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from se_harness import provenance, workflow
from se_harness.engine import validate_engineering_artifacts
from se_harness.workflow_edges import LIFECYCLE_REGISTRY, TRANSITIONS, grants_authority, validate_edge
from se_harness.workflow_contract import (
    IMPLEMENTED_OR_LATER_STATUSES,
    ContractError,
    LifecycleState,
    lifecycle_family,
    load_lifecycle_registry,
)


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_CONTRACT = ROOT / "se_harness/workflow_contract.json"
MANAGED_CONTRACT = ROOT / "templates/repository/standard/docs/engineering/WORKFLOW.json"
VALIDATOR = validate_engineering_artifacts


def row_value(row: object) -> tuple[tuple[str, ...], bool, bool, bool, bool, str]:
    return (
        tuple(row.transitions_to),
        row.grants_authority,
        row.reserves_version,
        row.transitionable,
        row.must_remain_visible,
        row.predecessor_adapter,
    )


class LifecycleStateContractTests(unittest.TestCase):
    def test_one_loader_serves_the_package_and_the_engine(self) -> None:
        # SPEC-ECP-024 ECP-ENG-005: the validator reads the registry through the package loader;
        # its former copy and the hand-written matrix this test carried are gone. The contract
        # file is the one source, byte-identical to the managed template.
        self.assertEqual(RUNTIME_CONTRACT.read_bytes(), MANAGED_CONTRACT.read_bytes())
        self.assertIs(VALIDATOR.load_lifecycle_registry, load_lifecycle_registry)
        self.assertIs(VALIDATOR.LifecycleStatePolicy, LifecycleState)
        runtime = {
            family: {state: row_value(row) for state, row in states.items()}
            for family, states in LIFECYCLE_REGISTRY.items()
        }
        standalone = {
            family: {state: row_value(row) for state, row in states.items()}
            for family, states in VALIDATOR.WORKFLOW_LIFECYCLES.items()
        }
        self.assertEqual(runtime, standalone)
        self.assertEqual(
            {family: {state: set(row.transitions_to) for state, row in states.items()} for family, states in LIFECYCLE_REGISTRY.items()},
            TRANSITIONS,
        )
        self.assertEqual(
            {family: {state: frozenset(row.transitions_to) for state, row in states.items()} for family, states in LIFECYCLE_REGISTRY.items()},
            {family: dict(states) for family, states in VALIDATOR.WORKFLOW_TRANSITIONS.items()},
        )
        source = (ROOT / "se_harness/engine/validate_engineering_artifacts.py").read_text(encoding="utf-8")
        self.assertNotIn("def _load_workflow_lifecycles", source)
        self.assertNotIn("class LifecycleStatePolicy", source)

    def test_the_family_map_and_the_status_set_have_one_definition(self) -> None:
        # ECP-ENG-007: the implemented-or-later states are declared once and checked at load.
        self.assertEqual(frozenset({"implemented", "verified", "released"}), IMPLEMENTED_OR_LATER_STATUSES)
        self.assertIs(VALIDATOR.IMPLEMENTED_OR_LATER_STATUSES, IMPLEMENTED_OR_LATER_STATUSES)
        for state in IMPLEMENTED_OR_LATER_STATUSES:
            self.assertIn(state, LIFECYCLE_REGISTRY["work_order"])
            self.assertTrue(set(LIFECYCLE_REGISTRY["work_order"][state].transitions_to) <= IMPLEMENTED_OR_LATER_STATUSES)
        for artifact_type, family in (
            ("requirement", "definition"), ("adr", "definition"), ("work_order", "work_order"),
            ("verification_record", "verification_record"), ("release_record", "release_record"),
            ("decision", "decision"), ("risk", "risk"), ("unknown", "definition"),
        ):
            self.assertEqual(family, lifecycle_family(artifact_type))
            self.assertEqual(family, VALIDATOR.lifecycle_family(artifact_type))

    def test_registry_is_immutable_and_rejected_rows_are_terminal_history(self) -> None:
        with self.assertRaises(TypeError):
            LIFECYCLE_REGISTRY["definition"] = {}  # type: ignore[index]
        with self.assertRaises(TypeError):
            LIFECYCLE_REGISTRY["release_record"]["ready"] = object()  # type: ignore[index]
        with self.assertRaises(TypeError):
            VALIDATOR.WORKFLOW_LIFECYCLES["definition"] = {}  # type: ignore[index]
        with self.assertRaises(TypeError):
            VALIDATOR.WORKFLOW_LIFECYCLES["release_record"]["ready"] = object()  # type: ignore[index]
        for family in ("verification_record", "release_record"):
            rejected = LIFECYCLE_REGISTRY[family]["rejected"]
            self.assertEqual((), rejected.transitions_to)
            self.assertFalse(rejected.grants_authority)
            self.assertFalse(rejected.reserves_version)
            self.assertFalse(rejected.transitionable)
            self.assertTrue(rejected.must_remain_visible)
            self.assertEqual("required", rejected.predecessor_adapter)

    def test_authority_and_version_consumers_query_registry_semantics(self) -> None:
        artifact_type = {
            "definition": "requirement",
            "work_order": "work_order",
            "verification_record": "verification_record",
            "release_record": "release_record",
            "decision": "decision",
            "risk": "risk",
        }
        for family, states in LIFECYCLE_REGISTRY.items():
            for status, row in states.items():
                self.assertEqual(row.grants_authority, grants_authority(family, status))
                self.assertEqual(row.grants_authority, provenance._grants_authority(family, status))
                self.assertEqual(
                    row.grants_authority,
                    VALIDATOR.grants_authority(artifact_type[family], status),
                )
                if family == "release_record":
                    self.assertEqual(row.reserves_version, provenance._reserves_version(status))
                    self.assertEqual(row.reserves_version, VALIDATOR.reserves_version(status))

    def test_strict_loader_rejects_each_structural_inconsistency(self) -> None:
        source = json.loads(RUNTIME_CONTRACT.read_text(encoding="utf-8"))

        def missing_family(value: dict) -> None:
            value["lifecycles"].pop("definition")

        def missing_field(value: dict) -> None:
            value["lifecycles"]["release_record"]["ready"].pop("grants_authority")

        def unknown_target(value: dict) -> None:
            value["lifecycles"]["definition"]["draft"]["transitions_to"] = ["unknown"]

        def duplicate_target(value: dict) -> None:
            value["lifecycles"]["definition"]["draft"]["transitions_to"] = ["approved", "approved"]

        def inconsistent_transitionable(value: dict) -> None:
            value["lifecycles"]["definition"]["draft"]["transitionable"] = False

        def illegal_reservation(value: dict) -> None:
            value["lifecycles"]["verification_record"]["ready"]["reserves_version"] = True

        def hidden_history(value: dict) -> None:
            value["lifecycles"]["release_record"]["rejected"]["must_remain_visible"] = False

        def wrong_boolean(value: dict) -> None:
            value["lifecycles"]["release_record"]["ready"]["reserves_version"] = 1

        def missing_implemented(value: dict) -> None:
            # ECP-ENG-007: the status set is checked against the registry at load.
            value["lifecycles"]["work_order"].pop("released")
            value["lifecycles"]["work_order"]["implemented"]["transitions_to"] = ["verified"]
            value["lifecycles"]["work_order"]["verified"]["transitions_to"] = []
            value["lifecycles"]["work_order"]["verified"]["transitionable"] = False

        def leaking_implemented(value: dict) -> None:
            value["lifecycles"]["work_order"]["verified"]["transitions_to"] = ["released", "rejected"]

        for name, mutate in (
            ("missing-family", missing_family),
            ("missing-field", missing_field),
            ("unknown-target", unknown_target),
            ("duplicate-target", duplicate_target),
            ("inconsistent-transitionable", inconsistent_transitionable),
            ("illegal-reservation", illegal_reservation),
            ("hidden-history", hidden_history),
            ("wrong-boolean", wrong_boolean),
            ("missing-implemented-or-later", missing_implemented),
            ("leaking-implemented-or-later", leaking_implemented),
        ):
            with self.subTest(case=name), tempfile.TemporaryDirectory() as temporary:
                malformed = copy.deepcopy(source)
                mutate(malformed)
                path = Path(temporary) / "WORKFLOW.json"
                path.write_text(json.dumps(malformed), encoding="utf-8")
                with self.assertRaises(ContractError):
                    load_lifecycle_registry(path)

    def test_loader_rejects_v2_duplicate_keys_and_oversized_contracts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            v2 = root / "v2.json"
            v2.write_text('{"schema":"se-harness-workflow-v2"}', encoding="utf-8")
            with self.assertRaises(ContractError):
                load_lifecycle_registry(v2)

            duplicate = root / "duplicate.json"
            duplicate.write_text(
                RUNTIME_CONTRACT.read_text(encoding="utf-8").replace(
                    '"schema": "se-harness-workflow-v4",',
                    '"schema": "se-harness-workflow-v4",\n  "schema": "se-harness-workflow-v4",',
                    1,
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ContractError, "duplicate JSON key"):
                load_lifecycle_registry(duplicate)

            oversized = root / "oversized.json"
            oversized.write_bytes(b"{" + b" " * 2_000_001 + b"}")
            with self.assertRaisesRegex(ContractError, "exceeds 2 MB"):
                load_lifecycle_registry(oversized)

            non_utf8 = root / "non-utf8.json"
            non_utf8.write_bytes(b"\xff")
            with self.assertRaisesRegex(ContractError, "cannot load machine policy"):
                load_lifecycle_registry(non_utf8)

    def test_the_one_loader_refuses_the_malformed_managed_registries(self) -> None:
        # Formerly a copy of the validator was executed against each of these; the validator
        # now imports the package loader, so the loader's refusal is the engine's (ECP-ENG-005).
        original = MANAGED_CONTRACT.read_text(encoding="utf-8")
        cases = {
            "v3": original.replace("se-harness-workflow-v4", "se-harness-workflow-v3", 1),
            "duplicate": original.replace(
                '"schema": "se-harness-workflow-v4",',
                '"schema": "se-harness-workflow-v4",\n  "schema": "se-harness-workflow-v4",',
                1,
            ),
            "unknown-target": original.replace(
                '"transitions_to": ["approved", "rejected"]',
                '"transitions_to": ["unknown"]',
                1,
            ),
        }
        for name, contract in cases.items():
            with self.subTest(case=name), tempfile.TemporaryDirectory() as temporary:
                path = Path(temporary) / "WORKFLOW.json"
                path.write_text(contract, encoding="utf-8")
                with self.assertRaises(RuntimeError) as raised:
                    load_lifecycle_registry(path)
                self.assertIsInstance(raised.exception, ContractError)

    def test_planner_accepts_exactly_declared_edges(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".engineering-harness.toml").write_text(
                "[revision_provenance]\n"
                "required_for_verified_work = true\n"
                "required_for_release = true\n",
                encoding="utf-8",
            )
            for family, states in LIFECYCLE_REGISTRY.items():
                artifact_type = "requirement" if family == "definition" else family
                universe = set(states)
                for source, row in states.items():
                    artifact = SimpleNamespace(
                        artifact_id="TEST-001",
                        artifact_type=artifact_type,
                        status=source,
                    )
                    for target in universe:
                        reason = "VREC-NEXT-001" if target == "superseded" else "review decision" if target == "rejected" else None
                        if target in row.transitions_to:
                            validate_edge(root, artifact, target, "test-owner", reason)
                        else:
                            with self.assertRaisesRegex(Exception, "is not allowed"):
                                validate_edge(root, artifact, target, "test-owner", reason)

    def test_validator_admits_exactly_the_registry_vocabulary_per_family(self) -> None:
        fixtures = {
            "definition": ("REQ-TST-001", "requirement"),
            "work_order": ("WO-TST-001", "work_order"),
            "verification_record": ("VREC-TST-001", "verification_record"),
            "release_record": ("RLS-TST-001", "release_record"),
        }
        all_states = set().union(*(set(states) for states in LIFECYCLE_REGISTRY.values())) | {"unknown"}
        for family, (artifact_id, artifact_type) in fixtures.items():
            for status in all_states:
                artifact = VALIDATOR.Artifact(
                    path=Path("docs/engineering/test.md"),
                    metadata={
                        "id": artifact_id,
                        "type": artifact_type,
                        "title": "Test",
                        "status": status,
                        "owners": ["test-owner"],
                        "created": "2026-08-23",
                        "updated": "2026-08-23",
                        "relations": {},
                    },
                    body="",
                )
                diagnostics = VALIDATOR.validate_common_metadata([artifact], ROOT)
                status_errors = [item for item in diagnostics if "status" in item.message]
                self.assertEqual(
                    status not in LIFECYCLE_REGISTRY[family],
                    bool(status_errors),
                    f"{family}:{status}: {[item.message for item in diagnostics]}",
                )


if __name__ == "__main__":
    unittest.main()
