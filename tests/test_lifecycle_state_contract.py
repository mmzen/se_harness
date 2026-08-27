from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from se_harness import provenance, workflow
from se_harness.preflight import _load_validator_module
from se_harness.workflow import LIFECYCLE_REGISTRY, TRANSITIONS, _validate_edge
from se_harness.workflow_contract import ContractError, load_lifecycle_registry


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_CONTRACT = ROOT / "se_harness/workflow_contract.json"
MANAGED_CONTRACT = ROOT / "templates/repository/standard/docs/engineering/WORKFLOW.json"
VALIDATOR = _load_validator_module()


EXPECTED = {
    "definition": {
        "draft": (("approved", "rejected"), False, False, True, True, "none"),
        "ready": ((), False, False, False, True, "none"),
        "approved": (("implemented", "rejected"), True, False, True, True, "none"),
        "in_progress": ((), True, False, False, True, "none"),
        "implemented": ((), True, False, False, True, "none"),
        "verified": ((), True, False, False, True, "none"),
        "released": ((), True, False, False, True, "none"),
        "superseded": ((), False, False, False, True, "none"),
        "rejected": ((), False, False, False, True, "none"),
    },
    "work_order": {
        "draft": (("approved", "rejected"), False, False, True, True, "none"),
        "ready": ((), False, False, False, True, "none"),
        "approved": (("in_progress", "rejected"), True, False, True, True, "none"),
        "in_progress": (("implemented", "rejected"), True, False, True, True, "none"),
        "implemented": (("verified", "released"), True, False, True, True, "none"),
        "verified": (("released",), True, False, True, True, "none"),
        "released": ((), True, False, False, True, "none"),
        "superseded": ((), False, False, False, True, "none"),
        "rejected": ((), False, False, False, True, "none"),
    },
    "verification_record": {
        "ready": (("verified", "rejected", "superseded"), False, False, True, True, "none"),
        "verified": ((), True, False, False, True, "none"),
        "released": ((), True, False, False, True, "none"),
        "superseded": ((), False, False, False, True, "none"),
        "rejected": ((), False, False, False, True, "required"),
    },
    "release_record": {
        "ready": (("released", "rejected"), False, True, True, True, "none"),
        "released": ((), True, True, False, True, "none"),
        "rejected": ((), False, False, False, True, "required"),
    },
    "risk": {
        "identified": (("raised", "accepted", "withdrawn"), False, False, True, True, "none"),
        "raised": (("accepted", "avoided", "mitigating", "withdrawn"), False, False, True, True, "none"),
        "mitigating": (("mitigated",), False, False, True, True, "none"),
        "accepted": ((), False, False, False, True, "none"),
        "avoided": ((), False, False, False, True, "none"),
        "mitigated": ((), False, False, False, True, "none"),
        "withdrawn": ((), False, False, False, True, "none"),
    },
}


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
    def test_exact_matrix_is_shared_by_package_and_standalone_consumers(self) -> None:
        self.assertEqual(RUNTIME_CONTRACT.read_bytes(), MANAGED_CONTRACT.read_bytes())
        runtime = {
            family: {state: row_value(row) for state, row in states.items()}
            for family, states in LIFECYCLE_REGISTRY.items()
        }
        standalone = {
            family: {state: row_value(row) for state, row in states.items()}
            for family, states in VALIDATOR.WORKFLOW_LIFECYCLES.items()
        }
        self.assertEqual(EXPECTED, runtime)
        self.assertEqual(EXPECTED, standalone)
        self.assertEqual(
            {
                family: {state: set(values[0]) for state, values in states.items()}
                for family, states in EXPECTED.items()
            },
            TRANSITIONS,
        )

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
            "risk": "risk",
        }
        for family, states in LIFECYCLE_REGISTRY.items():
            for status, row in states.items():
                self.assertEqual(row.grants_authority, workflow._grants_authority(family, status))
                self.assertEqual(row.grants_authority, provenance._grants_authority(family, status))
                self.assertEqual(
                    row.grants_authority,
                    VALIDATOR._grants_authority(artifact_type[family], status),
                )
                if family == "release_record":
                    self.assertEqual(row.reserves_version, provenance._reserves_version(status))
                    self.assertEqual(row.reserves_version, VALIDATOR._reserves_version(status))

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

        for name, mutate in (
            ("missing-family", missing_family),
            ("missing-field", missing_field),
            ("unknown-target", unknown_target),
            ("duplicate-target", duplicate_target),
            ("inconsistent-transitionable", inconsistent_transitionable),
            ("illegal-reservation", illegal_reservation),
            ("hidden-history", hidden_history),
            ("wrong-boolean", wrong_boolean),
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

    def test_standalone_validator_rejects_invalid_managed_registry_before_import(self) -> None:
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
        for index, (name, contract) in enumerate(cases.items()):
            with self.subTest(case=name), tempfile.TemporaryDirectory() as temporary:
                standard = Path(temporary) / "standard"
                scripts = standard / "scripts"
                engineering = standard / "docs/engineering"
                scripts.mkdir(parents=True)
                engineering.mkdir(parents=True)
                shutil.copy2(
                    ROOT / "templates/repository/standard/scripts/artifact_layout_registry.py",
                    scripts / "artifact_layout_registry.py",
                )
                validator_path = scripts / "validate_engineering_artifacts.py"
                shutil.copy2(
                    ROOT / "templates/repository/standard/scripts/validate_engineering_artifacts.py",
                    validator_path,
                )
                (engineering / "WORKFLOW.json").write_text(contract, encoding="utf-8")
                module_name = f"_invalid_lifecycle_validator_{index}"
                spec = importlib.util.spec_from_file_location(module_name, validator_path)
                self.assertIsNotNone(spec)
                self.assertIsNotNone(spec.loader)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                try:
                    with self.assertRaises(RuntimeError):
                        spec.loader.exec_module(module)
                finally:
                    sys.modules.pop(module_name, None)

    def test_planner_accepts_exactly_declared_edges(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".engineering-harness.toml").write_text(
                "[revision_provenance]\n"
                "required_for_verified_work = true\n"
                "required_for_release = true\n",
                encoding="utf-8",
            )
            risk_reasons = {
                "accepted": "accepted: residual tolerated",
                "avoided": "avoided_by ADR-TST-001",
                "mitigating": "mitigated_by WO-TST-001",
                "mitigated": "residual 1x1 accepted",
                "withdrawn": "duplicate of RISK-TST-002",
            }
            for family, states in LIFECYCLE_REGISTRY.items():
                artifact_type = "requirement" if family == "definition" else family
                universe = set(states)
                for source, row in states.items():
                    artifact = SimpleNamespace(
                        artifact_id="TEST-001",
                        artifact_type=artifact_type,
                        status=source,
                        metadata={"risk": {"stage": "implementation", "acceptance_level": 1}, "relations": {}},
                        relations={},
                    )
                    actor = "engineering-owner" if family == "risk" else "test-owner"
                    for target in universe:
                        if family == "risk":
                            reason = risk_reasons.get(target)
                        else:
                            reason = "VREC-NEXT-001" if target == "superseded" else "review decision" if target == "rejected" else None
                        if target in row.transitions_to:
                            _validate_edge(root, artifact, target, actor, reason)
                        else:
                            with self.assertRaisesRegex(Exception, "is not allowed"):
                                _validate_edge(root, artifact, target, actor, reason)

    def test_validator_admits_exactly_the_registry_vocabulary_per_family(self) -> None:
        fixtures = {
            "definition": ("REQ-TST-001", "requirement"),
            "work_order": ("WO-TST-001", "work_order"),
            "verification_record": ("VREC-TST-001", "verification_record"),
            "release_record": ("RLS-TST-001", "release_record"),
        }
        all_states = set().union(*(set(states) for states in EXPECTED.values())) | {"unknown"}
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
                    status not in EXPECTED[family],
                    bool(status_errors),
                    f"{family}:{status}: {[item.message for item in diagnostics]}",
                )


if __name__ == "__main__":
    unittest.main()
