"""WO-ECP-033 (SPEC-ECP-023 ECP-PRM-016 to ECP-PRM-023): the code registry and the contract tables.

Every diagnostic code the package raises is named once in `se_harness/codes.py`
and no module spells one; every coded refusal carries `code` and `message`; the
index reads the registry through the parser; and the four declarative contract
sections drive the gate, the guard, the result validator, the aggregator and the
two digest writers at run time, refusing a missing or malformed section with one
code.
"""

from __future__ import annotations

import ast
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from se_harness import cli, codes, gate_source, github_ci, interpreter_safety, mutation_guard, provenance, workflow, workflow_contract, workflow_procedures, workflow_result
from se_harness.hash_bound import LOCK_RELATIVE, declared_digest
from se_harness.integrity import canonical_sha256, raw_sha256
from se_harness.workflow_compliance import _aggregate

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT))
from repository_tools.diagnostic_code_index import PREFIXES, _CODE, registry, scan  # noqa: E402

#: The registry itself and the standard-library-only loader (SPEC-REB-015 rule 2) spell codes.
EXEMPT_MODULES = {"codes.py", "interpreter_safety.py"}


def _registry_codes() -> dict[str, str]:
    return {name: value for name, value in vars(codes).items() if name.isupper() and isinstance(value, str)}


def _docstring_ids(tree: ast.Module) -> set[int]:
    found: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and node.body:
            first = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
                found.add(id(first.value))
    return found


class RegistryTests(unittest.TestCase):
    def test_every_name_is_its_code(self) -> None:
        entries = _registry_codes()
        self.assertGreater(len(entries), 100)
        for name, value in entries.items():
            with self.subTest(name=name):
                self.assertEqual(name, value.replace("-", "_"))
                self.assertIsNotNone(_CODE.fullmatch(value))
                self.assertIn(_CODE.fullmatch(value).group(1), PREFIXES)

    def test_no_package_module_spells_a_diagnostic_code(self) -> None:
        offenders: list[str] = []
        for path in sorted((REPOSITORY_ROOT / "se_harness").rglob("*.py")):  # the engine included (ECP-ENG-009)
            if path.name in EXEMPT_MODULES:
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"))
            docstrings = _docstring_ids(tree)
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in docstrings:
                    for match in _CODE.finditer(node.value):
                        if match.group(1) in PREFIXES:
                            offenders.append(f"{path.name}:{node.lineno}: {match.group(0)}")
        self.assertEqual([], offenders)

    def test_the_loader_codes_are_named_in_the_registry(self) -> None:
        source = (REPOSITORY_ROOT / "se_harness" / "interpreter_safety.py").read_text(encoding="utf-8")
        spelled = {match.group(0) for match in _CODE.finditer(source) if match.group(1) == "EPS"}
        self.assertTrue(spelled)
        self.assertTrue(spelled <= set(_registry_codes().values()))

    def test_the_record_refusal_tables_name_the_composed_codes(self) -> None:
        self.assertEqual({"state": "WEX301", "provenance": "WEX302", "evidence": "WEX303", "inputs": "WEX304"}, codes.VERIFICATION_RECORD_REFUSALS)
        self.assertEqual({"state": "WEX401", "provenance": "WEX402", "evidence": "WEX403", "inputs": "WEX404"}, codes.RELEASE_RECORD_REFUSALS)
        self.assertEqual(set(codes.VERIFICATION_RECORD_REFUSALS), {cls.cause for cls in (provenance.StateRefusal, provenance.ProvenanceRefusal, provenance.EvidenceRefusal, provenance.InputRefusal)})


class CodedErrorTests(unittest.TestCase):
    def test_the_base_carries_code_and_message_and_renders_the_wire_form(self) -> None:
        error = codes.CodedError(codes.WEX210, "the reason")
        self.assertEqual(("WEX210", "the reason", "WEX210: the reason"), (error.code, error.message, str(error)))
        self.assertIsInstance(error, workflow.HarnessError)

    def test_every_coded_refusal_class_exposes_the_two_attributes(self) -> None:
        cases = [
            (gate_source.DelegationError(codes.WEX_ECP_040, "gate"), "WEX-ECP-040", "gate", "WEX-ECP-040: gate"),
            (workflow_procedures.ProcedureError(codes.WEX221, "parameter"), "WEX221", "parameter", "WEX221: parameter"),
            (workflow_contract.ContractRefusal(codes.WEX_ECP_031, "section"), "WEX-ECP-031", "section", "WEX-ECP-031: section"),
            (workflow_result.RestitutionError(codes.WEX230, "field"), "WEX230", "field", "WEX230: field"),
            (github_ci.SelectionRefusal(codes.WEX_ECP_014, "selection"), "WEX-ECP-014", "selection", "WEX-ECP-014: selection"),
            (mutation_guard.MutationGuardError(codes.MG005, "transition-apply", "resolved"), "MG005", "resolved", "mutation guard MG005 (transition-apply): resolved"),
            (workflow.PreconditionError("QGP-G4I-PATHS", "outside"), "QGP-G4I-PATHS", "outside", "outside"),
            (interpreter_safety.InterpreterSafetyRefusal("EPS004", "python", "not a file"), "EPS004", "python: not a file", "EPS004 python: not a file"),
        ]
        for error, code, message, text in cases:
            with self.subTest(cls=type(error).__name__):
                self.assertEqual((code, message, text), (error.code, error.message, str(error)))
        self.assertIsInstance(cases[0][0], codes.CodedError)
        self.assertIsInstance(cases[2][0], workflow_contract.ContractError)
        self.assertIsInstance(cases[3][0], ValueError)
        self.assertIsInstance(cases[4][0], github_ci.SelectionError)
        self.assertEqual("QGP-G4I-PATHS", cases[6][0].predicate_id)

    def test_the_cli_reads_the_attributes_and_keeps_one_split_for_bare_text(self) -> None:
        self.assertEqual(("WEX210", "x: y"), cli._split_code(codes.CodedError(codes.WEX210, "x: y"), codes.WEX201))
        self.assertEqual(("WEX-ECP-014", "z"), cli._split_code(RuntimeError("WEX-ECP-014: z"), codes.WEX210))
        self.assertEqual(("WEX210", "plain"), cli._split_code(RuntimeError("plain"), codes.WEX210))
        self.assertEqual(("WEX304", "bad input"), cli._record_code(provenance.InputRefusal("bad input"), codes.VERIFICATION_RECORD_REFUSALS))
        self.assertEqual(("WEX401", "state"), cli._record_code(provenance.StateRefusal("state"), codes.RELEASE_RECORD_REFUSALS))
        self.assertEqual(("WEX-ECP-022", "human"), cli._record_code(provenance.StateRefusal("WEX-ECP-022: human"), codes.RELEASE_RECORD_REFUSALS))


class IndexTests(unittest.TestCase):
    def test_the_index_reads_the_registry_through_the_parser_and_attributes_raise_sites(self) -> None:
        names = registry(REPOSITORY_ROOT)
        self.assertEqual(_registry_codes(), names)
        indexed = scan(REPOSITORY_ROOT)
        self.assertTrue(any("check --checkpoint accepts only" in message for message in indexed["WEX"]["WEX210"]))
        self.assertTrue(any(message.startswith("W-ADS-001: the Harness-Work-Order line") for message in indexed["W-ADS"]["W-ADS-001"]))
        self.assertIn("WEX-ECP-031", indexed["WEX-ECP"])
        self.assertIn("WEX301", indexed["WEX"])

    def test_a_checkout_without_the_registry_still_indexes_its_literals(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "se_harness").mkdir()
            (root / "se_harness" / "module.py").write_text('raise RuntimeError("WEX210: spelled")\n', encoding="utf-8")
            self.assertEqual({}, registry(root))
            self.assertEqual({"WEX210: spelled"}, scan(root)["WEX"]["WEX210"])


def _workflow_copy() -> dict:
    return json.loads(json.dumps(workflow_contract.load_workflow_contract()))


def _gates_copy() -> dict:
    return json.loads(json.dumps(workflow_contract.load_quality_gate_contract()))


class ContractTableTests(unittest.TestCase):
    def test_the_delegated_operations_are_the_contract_section(self) -> None:
        section = workflow_contract.load_workflow_contract()["agentic_operations"]
        operations = workflow_contract.delegated_operations()
        self.assertEqual([item["id"] for item in section], [operation.id for operation in operations])
        self.assertEqual({item["decision_right"]: item["mutation_operation"] for item in section}, dict(gate_source.DELEGATED_RIGHTS))
        self.assertEqual(
            {("work_order", item["current_status"], item["result_status"]): item["decision_right"] for item in section if item["current_status"] != item["result_status"]},
            dict(gate_source.DELEGATED_TRANSITIONS),
        )
        self.assertTrue({item["mutation_operation"] for item in section} <= mutation_guard.PUBLIC_MUTATION_OPERATIONS)
        self.assertEqual("DR-VREC-PREPARE", gate_source.delegated_operation("DR-VREC-PREPARE").decision_right)
        self.assertIsNone(gate_source.delegated_operation("DR-VREC-PREPARE").transition)

    def test_the_restitution_fields_and_the_aggregation_are_the_contract_sections(self) -> None:
        self.assertEqual(tuple(workflow_contract.load_workflow_contract()["restitution_fields"]), workflow_contract.restitution_fields())
        self.assertEqual(tuple(workflow_contract.load_quality_gate_contract()["aggregation"]), workflow_contract.aggregation_order())
        self.assertEqual("fail", _aggregate(["pass", "fail", "not_assessable"]))
        self.assertEqual("not_assessable", _aggregate(["pass", "not_assessable"]))
        self.assertEqual("pass", _aggregate([]))
        with mock.patch("se_harness.workflow_compliance.aggregation_order", return_value=("pass", "not_assessable", "fail")):
            self.assertEqual("pass", _aggregate(["fail", "pass"]))
            self.assertEqual("fail", _aggregate([]))

    def test_a_missing_or_malformed_section_refuses_with_one_code(self) -> None:
        # ECP-PRM-023: four throwaway contracts, one code.
        missing = _workflow_copy()
        del missing["agentic_operations"]
        malformed_entry = _workflow_copy()
        del malformed_entry["agentic_operations"][0]["gate_ids"]
        repeated_right = _workflow_copy()
        repeated_right["agentic_operations"][1]["decision_right"] = repeated_right["agentic_operations"][0]["decision_right"]
        no_outcome = _workflow_copy()
        no_outcome["restitution_fields"].remove("outcome")
        short_order = _gates_copy()
        short_order["aggregation"] = ["fail", "pass"]
        for label, call in (
            ("missing section", lambda: workflow_contract.delegated_operations_of(missing)),
            ("malformed entry", lambda: workflow_contract.delegated_operations_of(malformed_entry)),
            ("repeated right", lambda: workflow_contract.delegated_operations_of(repeated_right)),
            ("no outcome", lambda: workflow_contract.restitution_fields_of(no_outcome)),
            ("short order", lambda: workflow_contract.aggregation_of(short_order)),
            ("validated together", lambda: workflow_contract.validate_contracts(malformed_entry, workflow_contract.load_quality_gate_contract())),
        ):
            with self.subTest(label=label):
                with self.assertRaises(workflow_contract.ContractRefusal) as raised:
                    call()
                self.assertEqual("WEX-ECP-031", raised.exception.code)
        # an edge the lifecycle lacks is refused with the same code
        wrong_edge = _workflow_copy()
        wrong_edge["agentic_operations"][0]["result_status"] = "implemented"
        with self.assertRaisesRegex(workflow_contract.ContractError, "WEX-ECP-031"):
            workflow_contract.validate_contracts(wrong_edge, workflow_contract.load_quality_gate_contract())

    def test_the_result_validator_reads_the_contract_field_set(self) -> None:
        restitution = {field: [] for field in workflow_contract.restitution_fields()}
        restitution.update(outcome="completed", decision_required=None, next={"procedure_id": "P", "step_id": "S", "action": "a"}, command_or_response={"kind": "response", "value": "ok"})
        workflow_result._validate_restitution(restitution, "completed")
        del restitution["alternatives"]
        with self.assertRaisesRegex(ValueError, "WEX230"):
            workflow_result._validate_restitution(restitution, "completed")

    def test_the_two_writers_hash_through_the_declared_digest(self) -> None:
        content = b'{"a": 1}\n'
        for relative in ("docs/engineering/evidence/VREC-X-001-evaluator.json", "docs/engineering/some-domain/evidence/RLS-X-001-evaluator.json"):
            with self.subTest(relative=relative):
                self.assertEqual(raw_sha256(content), declared_digest(relative, content))
        self.assertEqual(canonical_sha256(b"{\r\n}\r\n"), declared_digest(LOCK_RELATIVE, b"{\r\n}\r\n"))
        self.assertEqual(raw_sha256(content), provenance._evidence_digest("docs/engineering/evidence/VREC-X-001-evaluator.json", content))
        with self.assertRaises(provenance.EvidenceRefusal):
            provenance._evidence_digest("README.md", content)
        provenance_source = (REPOSITORY_ROOT / "se_harness" / "provenance.py").read_text(encoding="utf-8")
        installer_source = (REPOSITORY_ROOT / "se_harness" / "installer.py").read_text(encoding="utf-8")
        self.assertNotIn("{authority.evidence_sha256}", provenance_source)
        self.assertEqual(2, provenance_source.count("evidence_sha256 = _evidence_digest(evaluator_evidence_path, authority.evidence_bytes)"))
        self.assertIn("declared_digest(LOCK_NAME, lock_file.read_bytes())", installer_source)
        self.assertNotIn("raw_sha256(lock_file", installer_source)

    def test_no_package_module_keeps_a_copy_of_the_tables(self) -> None:
        offenders: list[str] = []
        table_literals = re.compile(r'"delegated-(?:work-order-start|work-order-complete|vrec-prepare)"|\["fail", "not_assessable", "pass"\]|"outcome",\s*"done",\s*"not_done"')
        for path in sorted((REPOSITORY_ROOT / "se_harness").glob("*.py")):
            source = path.read_text(encoding="utf-8")
            if table_literals.search(source):
                offenders.append(path.name)
        self.assertEqual([], offenders)


if __name__ == "__main__":
    unittest.main()
