"""REQ-AUT-009 / SPEC-AUT-004 (WO-AUT-006): the compatibility windows are closed.

AUT-WIN-015 pins the closed windows that the traceability, applicability and
compliance modules do not already cover: the registry and the index, the
dashboard's sets, the contract loader without its v1 hint, and the absence of
every legacy state name from the package.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from se_harness import codes
from se_harness.engine import dashboard_snapshot
from se_harness.workflow_contract import (
    QUALITY_GATES_SCHEMA,
    ContractError,
    load_quality_gate_contract,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = REPOSITORY_ROOT / "se_harness"
INDEX_PAGE = REPOSITORY_ROOT / "docs/notes/diagnostic-codes.md"

#: AUT-WIN-011: the four codes that left with their windows.
RETIRED_CODES = ("W014", "W015", "W019", "W-ECP-002")
#: The codes that stay: the refusals the windows gave way to, and the binding fault code.
KEPT_CODES = ("E014", "E015", "E016", "WEX-ECP-030")
#: AUT-WIN-002, -004, -006, -008, -009: the names of the closed branches.
RETIRED_NAMES = (
    "legacy_missing",
    "legacy_requirement_trace",
    "legacy_specification_trace",
    "legacy_ambiguous",
    "dual_declared",
    "legacy_targets",
    "legacy_adr_covered",
    "legacy_adr_missing",
    "W_ECP_002",
    "RETIRED_QUALITY_GATES_SCHEMAS",
)


def _package_sources() -> list[Path]:
    return sorted(path for path in PACKAGE_ROOT.rglob("*.py") if "__pycache__" not in path.parts)


class RetiredCodeRegistryTests(unittest.TestCase):
    """AUT-WIN-011: the four codes are gone from the registry and the index; the refusals stay."""

    def test_the_retired_codes_left_the_registry_and_the_kept_ones_stayed(self) -> None:
        registered = {value for name, value in vars(codes).items() if name.isupper() and isinstance(value, str)}
        for code in RETIRED_CODES:
            with self.subTest(code=code):
                self.assertNotIn(code, registered)
        for code in KEPT_CODES:
            with self.subTest(code=code):
                self.assertIn(code, registered)

    def test_the_index_page_names_no_retired_code_and_matches_the_source(self) -> None:
        page = INDEX_PAGE.read_text(encoding="utf-8")
        for code in RETIRED_CODES:
            with self.subTest(code=code):
                self.assertNotRegex(page, rf"`{re.escape(code)}`")
        for code in KEPT_CODES:
            with self.subTest(code=code):
                self.assertIn(f"`{code}`", page)
        completed = subprocess.run(
            [sys.executable, "-m", "repository_tools.diagnostic_code_index", "--check"],
            cwd=REPOSITORY_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)

    def test_no_package_module_names_a_closed_branch(self) -> None:
        # The state names, the constant and the code symbol of the closed branches
        # occur nowhere in the package, so no reader of a legacy state survives.
        for path in _package_sources():
            source = path.read_text(encoding="utf-8")
            for name in RETIRED_NAMES:
                with self.subTest(module=path.relative_to(REPOSITORY_ROOT).as_posix(), name=name):
                    self.assertIsNone(re.search(rf"\b{re.escape(name)}\b", source))
            for code in ("W014", "W015", "W019"):
                with self.subTest(module=path.relative_to(REPOSITORY_ROOT).as_posix(), code=code):
                    self.assertNotIn(f'"{code}"', source)


class DashboardSetTests(unittest.TestCase):
    """AUT-WIN-006: the dashboard reads the typed relations and the current assessment states only."""

    def test_the_architecture_relation_set_holds_the_typed_pair_only(self) -> None:
        self.assertEqual(
            frozenset({"addresses", "conforms_to"}),
            dashboard_snapshot.TEMPORAL_REASSESSMENT_RELATIONS["architecture"],
        )

    def test_no_legacy_assessment_state_is_produced(self) -> None:
        source = Path(dashboard_snapshot.__file__).read_text(encoding="utf-8")
        self.assertNotIn("legacy_adr", source)
        self.assertNotIn("constrains", source)


class ContractLoaderTests(unittest.TestCase):
    """AUT-WIN-009, AUT-WIN-010: a retired schema meets the loader's own error; the binding faults keep their code."""

    def test_a_v1_contract_meets_the_loaders_own_schema_error(self) -> None:
        contract_path = Path(load_quality_gate_contract.__globals__["__file__"]).with_name("quality_gates_contract.json")
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        self.assertEqual(QUALITY_GATES_SCHEMA, contract["schema"])
        contract["schema"] = "se-harness-quality-gates-v1"
        with tempfile.TemporaryDirectory() as temporary:
            copy = Path(temporary) / "quality_gates_contract.json"
            copy.write_text(json.dumps(contract), encoding="utf-8")
            with self.assertRaises(ContractError) as raised:
                load_quality_gate_contract(copy)
        message = str(raised.exception)
        self.assertNotIn("retired schema", message)
        self.assertNotIn("WEX-ECP-030", message)
        self.assertIn(f"must use schema {QUALITY_GATES_SCHEMA}", message)

    def test_the_loader_carries_no_retired_schema_set(self) -> None:
        source = Path(load_quality_gate_contract.__globals__["__file__"]).read_text(encoding="utf-8")
        self.assertNotIn("RETIRED_QUALITY_GATES_SCHEMAS", source)
        self.assertNotIn("se-harness-quality-gates-v1", source)
        self.assertIn("WEX_ECP_030", source)


if __name__ == "__main__":
    unittest.main()
