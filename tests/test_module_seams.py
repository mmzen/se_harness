"""WO-ECP-036 (SPEC-ECP-024 ECP-ENG-017 to ECP-ENG-022): the module seams and the complexity ceiling.

The validator, the generator and the compliance module are split along their
declared seams; the workflow graph names have one public home each; no module
imports a private name across the package; no function reads above complexity 60.
"""

from __future__ import annotations

import ast
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PACKAGE = REPOSITORY_ROOT / "se_harness"
ENGINE = PACKAGE / "engine"

VALIDATOR_SEAMS = (
    "validation_core", "validation_report", "validation_lifecycle", "validation_authoring", "validation_evidence",
    "validation_revision", "validation_architecture", "validation_decisions", "validation_layout",
)
COMPLIANCE_SEAMS = ("workflow_change_set", "workflow_evidence_packet", "workflow_predicates")
GRAPH_NAMES = ("classify_diagnostics", "diagnostic_payload", "project_scope", "artifact_catalog", "validated_repository")
RETIRED_PRIVATE_NAMES = ("_classify", "_diagnostic", "_catalog", "_validation", "_family")


def package_modules() -> list[Path]:
    return sorted(path for path in PACKAGE.rglob("*.py") if "harness_explorer" not in path.parts)


def top_level_definitions(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return [node.name for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))]


def imports_of(path: Path) -> list[ast.ImportFrom | ast.Import]:
    return [node for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))) if isinstance(node, (ast.ImportFrom, ast.Import))]


class SeamTests(unittest.TestCase):
    def test_the_validator_is_split_along_its_eight_seams(self) -> None:
        # ECP-ENG-017: the orchestrator stays in the entry module, every pass lives in a seam.
        for seam in VALIDATOR_SEAMS:
            self.assertTrue((ENGINE / f"{seam}.py").is_file(), seam)
        self.assertEqual(["validate_repository", "build_parser", "main"], top_level_definitions(ENGINE / "validate_engineering_artifacts.py"))

    def test_the_generator_is_split_at_its_two_seams(self) -> None:
        # ECP-ENG-018
        self.assertIn("build_snapshot", top_level_definitions(ENGINE / "dashboard_snapshot.py"))
        self.assertIn("build_dashboard_bundle", top_level_definitions(ENGINE / "dashboard_bundle.py"))
        entry = top_level_definitions(ENGINE / "generate_harness_dashboard.py")
        self.assertNotIn("build_snapshot", entry)
        self.assertNotIn("build_dashboard_bundle", entry)
        self.assertLessEqual(set(entry), {"generate_snapshot", "generate_bundle", "build_parser", "_display_output", "main"})

    def test_the_compliance_module_is_split_and_the_workflow_cycle_is_gone(self) -> None:
        # ECP-ENG-019: three seams, and neither the evaluator nor its seams import the workflow module.
        for seam in COMPLIANCE_SEAMS:
            self.assertTrue((PACKAGE / f"{seam}.py").is_file(), seam)
        offenders: list[str] = []
        for name in ("workflow_compliance", *COMPLIANCE_SEAMS, "repository_graph", "workflow_edges"):
            for node in imports_of(PACKAGE / f"{name}.py"):
                if isinstance(node, ast.ImportFrom) and node.module == "se_harness.workflow":
                    offenders.append(f"{name}:{node.lineno}")
                if isinstance(node, ast.Import) and any(alias.name == "se_harness.workflow" for alias in node.names):
                    offenders.append(f"{name}:{node.lineno}")
        self.assertEqual([], offenders)

    def test_each_workflow_graph_name_has_one_public_home(self) -> None:
        # ECP-ENG-020
        homes: dict[str, list[str]] = {name: [] for name in (*GRAPH_NAMES, "lifecycle_family", *RETIRED_PRIVATE_NAMES)}
        for path in package_modules():
            for name in top_level_definitions(path):
                if name in homes:
                    homes[name].append(path.relative_to(PACKAGE).as_posix())
        for name in GRAPH_NAMES:
            self.assertEqual(["repository_graph.py"], homes[name], name)
        self.assertEqual(["workflow_contract.py"], homes["lifecycle_family"])
        for name in RETIRED_PRIVATE_NAMES:
            self.assertEqual([], homes[name], name)

    def test_no_module_imports_a_private_name_across_the_package(self) -> None:
        # ECP-ENG-021: the imported name is what counts; a private alias of a public name is fine.
        offenders: list[str] = []
        for path in package_modules():
            for node in imports_of(path):
                if not isinstance(node, ast.ImportFrom):
                    continue
                if node.level == 0 and not (node.module or "").startswith("se_harness"):
                    continue
                for alias in node.names:
                    if alias.name.startswith("_") and not alias.name.startswith("__"):
                        offenders.append(f"{path.relative_to(PACKAGE).as_posix()}:{node.lineno} {alias.name}")
        self.assertEqual([], offenders)

    def test_no_function_exceeds_complexity_sixty(self) -> None:
        # ECP-ENG-022, as radon measures it; the reading is part of the work order's evidence and this
        # test repeats it wherever radon is installed.
        try:
            from radon.complexity import cc_visit
        except ImportError:
            self.skipTest("radon is not installed")
        offenders: list[str] = []
        for path in package_modules():
            for block in cc_visit(path.read_text(encoding="utf-8")):
                units = [block, *getattr(block, "methods", [])]
                for unit in units:
                    if unit.complexity > 60:
                        offenders.append(f"{path.relative_to(PACKAGE).as_posix()} {unit.name} {unit.complexity}")
        self.assertEqual([], offenders)


if __name__ == "__main__":
    unittest.main()
