"""WO-ECP-034 (SPEC-ECP-024 ECP-ENG-001 to ECP-ENG-009): the engine as an import surface and its twins folded.

The package imports the engine and loads nothing by path; each entry module still runs as
`python -m se_harness.engine.<name>`; the layout tables, the lifecycle registry, the
evaluator-evidence validator, the implemented-or-later status set, the body parser and the
artifact-id pattern each have one definition; the engine names its codes from the registry.
"""

from __future__ import annotations

import ast
import re
import subprocess
import sys
import unittest
from pathlib import Path

from se_harness import artifact_layout, cli, evaluator_evidence, front_matter, preflight, provenance, repository_graph, workflow, workflow_contract, workflow_procedures
from se_harness.engine import generate_harness_dashboard, inspect_engineering_artifacts, validate_engineering_artifacts

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
ENGINE = REPOSITORY_ROOT / "se_harness" / "engine"
ENTRY_MODULES = ("validate_engineering_artifacts", "generate_harness_dashboard", "inspect_engineering_artifacts")


def _imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.append(node.module)
    return names


class ImportSurfaceTests(unittest.TestCase):
    def test_the_engine_modules_import_their_siblings_and_the_package_by_name(self) -> None:
        # ECP-ENG-001: no bare sibling import, no path load, no sys.path edit.
        for path in sorted(ENGINE.glob("*.py")):
            with self.subTest(module=path.name):
                source = path.read_text(encoding="utf-8")
                self.assertNotIn("spec_from_file_location", source)
                self.assertNotIn("sys.path.insert", source)
                for name in _imports(path):
                    self.assertFalse(name in ENTRY_MODULES or name == "artifact_layout_registry", f"{path.name} imports {name} bare")
        self.assertFalse((ENGINE / "artifact_layout_registry.py").exists())
        self.assertIn("import surface", (ENGINE / "__init__.py").read_text(encoding="utf-8"))

    def test_the_package_loads_no_engine_module_by_path(self) -> None:
        # ECP-ENG-003: the path loader and the command-line assemblies are gone.
        offenders: list[str] = []
        for path in sorted((REPOSITORY_ROOT / "se_harness").glob("*.py")):
            source = path.read_text(encoding="utf-8")
            if "spec_from_file_location" in source or "_load_validator_module" in source or "_launch_engine" in source:
                offenders.append(path.name)
            if path.name != "installer.py" and "ENGINE_ROOT" in source:
                offenders.append(f"{path.name}: ENGINE_ROOT")
            if re.search(r"validate_engineering_artifacts\.py|generate_harness_dashboard\.py|inspect_engineering_artifacts\.py", source):
                offenders.append(f"{path.name}: script path")
        self.assertEqual([], offenders)
        self.assertIs(repository_graph._validator_module, validate_engineering_artifacts)
        self.assertIs(preflight.validate_engineering_artifacts, validate_engineering_artifacts)
        self.assertIs(cli.validate_engineering_artifacts, validate_engineering_artifacts)
        self.assertIs(provenance.generate_harness_dashboard, generate_harness_dashboard)

    def test_each_entry_module_runs_as_a_module_with_its_arguments(self) -> None:
        # ECP-ENG-002: the module form, its --help, and exit code 0.
        for name in ENTRY_MODULES:
            with self.subTest(module=name):
                completed = subprocess.run(
                    [sys.executable, "-m", f"se_harness.engine.{name}", "--help"],
                    cwd=REPOSITORY_ROOT, capture_output=True, text=True, check=False, timeout=120,
                )
                self.assertEqual(0, completed.returncode, completed.stderr)
                self.assertIn("--root", completed.stdout)


class TwinTests(unittest.TestCase):
    def test_the_layout_tables_have_one_definition(self) -> None:
        # ECP-ENG-004
        self.assertIs(validate_engineering_artifacts.ARTIFACT_DIRECTORIES, artifact_layout.ARTIFACT_DIRECTORIES)
        self.assertIs(validate_engineering_artifacts.ARTIFACT_PREFIXES, artifact_layout.ARTIFACT_PREFIXES)
        self.assertIs(validate_engineering_artifacts.canonical_artifact_relative_path, artifact_layout.canonical_artifact_relative_path)

    def test_the_lifecycle_registry_has_one_loader(self) -> None:
        # ECP-ENG-005
        self.assertIs(validate_engineering_artifacts.load_lifecycle_registry, workflow_contract.load_lifecycle_registry)
        self.assertEqual(workflow.LIFECYCLE_REGISTRY, validate_engineering_artifacts.WORKFLOW_LIFECYCLES)
        self.assertIs(validate_engineering_artifacts.lifecycle_family, workflow_contract.lifecycle_family)
        test_source = (REPOSITORY_ROOT / "tests" / "test_lifecycle_state_contract.py").read_text(encoding="utf-8")
        self.assertNotIn("EXPECTED = {", test_source)

    def test_one_evidence_validator_serves_the_engine_with_its_own_messages(self) -> None:
        # ECP-ENG-006: every reason the validator can raise has an engine message; the engine's
        # stricter checks (an isolated interpreter, an archive for a release) are its parameters.
        self.assertEqual(set(evaluator_evidence.EVIDENCE_REASONS), set(validate_engineering_artifacts.EVIDENCE_MESSAGES))
        self.assertIs(validate_engineering_artifacts.validate_evaluator_evidence, evaluator_evidence.validate_evaluator_evidence)
        valid = {
            "schema": evaluator_evidence.EVIDENCE_SCHEMA,
            "role": "released-evaluator",
            "evaluator": {
                "version": "0.16.0", "payload_manifest": "se-harness-installed-payload-v1",
                "payload_sha256": "0" * 64, "archive_name": None, "archive_sha256": None,
            },
            "origins": {label: "<evaluator-root>/x" for label in sorted(evaluator_evidence.ORIGIN_FIELDS)},
            "environment": {
                "isolated_python": True, "user_site_enabled": False, "pythonpath_present": False,
                "entry_point_resolved": True, "checkout_excluded": True,
            },
            "diagnostics": [],
        }
        evaluator_evidence.validate_evaluator_evidence(valid, require_isolated_python=True)
        cases = {
            "field_set": lambda v: v.pop("diagnostics"),
            "role": lambda v: v.__setitem__("role", "candidate"),
            "payload_manifest": lambda v: v["evaluator"].__setitem__("payload_manifest", "x"),
            "archive_required": lambda v: None,
            "origin": lambda v: v["origins"].__setitem__("module", "../x"),
            "isolated_python": lambda v: v["environment"].__setitem__("isolated_python", False),
            "diagnostics": lambda v: v.__setitem__("diagnostics", ["one"]),
            "lock": lambda v: None,
        }
        for reason, mutate in cases.items():
            with self.subTest(reason=reason):
                copy = {key: (dict(value) if isinstance(value, dict) else value) for key, value in valid.items()}
                mutate(copy)
                with self.assertRaises(evaluator_evidence.EvaluatorEvidenceError) as raised:
                    evaluator_evidence.validate_evaluator_evidence(
                        copy,
                        require_isolated_python=True,
                        require_archive=reason == "archive_required",
                        expected_evaluator={"version": "0.15.0"} if reason == "lock" else None,
                    )
                self.assertEqual(reason, raised.exception.reason)
                self.assertIn(reason, validate_engineering_artifacts.EVIDENCE_MESSAGES)
        # the package's own readers keep their defaults: an isolated interpreter is not demanded
        relaxed = {key: (dict(value) if isinstance(value, dict) else value) for key, value in valid.items()}
        relaxed["environment"]["isolated_python"] = False
        evaluator_evidence.validate_evaluator_evidence(relaxed)

    def test_the_status_set_the_body_parser_and_the_id_pattern_have_one_home(self) -> None:
        # ECP-ENG-007, ECP-ENG-008
        one = workflow_contract.IMPLEMENTED_OR_LATER_STATUSES
        self.assertIs(one, validate_engineering_artifacts.IMPLEMENTED_OR_LATER_STATUSES)
        self.assertIs(one, generate_harness_dashboard.IMPLEMENTED_OR_LATER_STATUSES)
        self.assertEqual(preflight.START_STATUSES | one, preflight.REVIEW_STATUSES)
        self.assertIs(one, provenance.IMPLEMENTED_OR_LATER_STATUSES)
        self.assertIs(validate_engineering_artifacts.body_sections, front_matter.body_sections)
        self.assertEqual({"A": "one\n \n", "B": "\n"}, front_matter.body_sections("intro\r\n## A\r\none\r\n```\r\n## not a heading\r\n```\r\n## B\r\n"))
        self.assertIs(generate_harness_dashboard.specification_rules, validate_engineering_artifacts.specification_rules)
        self.assertIs(generate_harness_dashboard.coverage_rows, validate_engineering_artifacts.coverage_rows)
        for module in (validate_engineering_artifacts, provenance, workflow_procedures):
            self.assertIs(artifact_layout.ID_PATTERN, module.ID_PATTERN)
        self.assertIs(provenance.evidence_work_order_keys, validate_engineering_artifacts.evidence_work_order_keys)
        offenders: list[str] = []
        for path in sorted((REPOSITORY_ROOT / "se_harness").rglob("*.py")):
            source = path.read_text(encoding="utf-8")
            if '{"implemented", "verified", "released"}' in source and path.name != "workflow_contract.py":
                offenders.append(f"{path.name}: status set")
            if 're.compile(r"^[A-Z][A-Z0-9-]*-\\d{3}$")' in source and path.name != "artifact_layout.py":
                offenders.append(f"{path.name}: id pattern")
            if "def _body_sections" in source or "def _sections(" in source:
                offenders.append(f"{path.name}: body parser")
        self.assertEqual([], offenders)


class EngineCodeTests(unittest.TestCase):
    def test_the_engine_spells_no_code_and_the_index_attributes_it_by_name(self) -> None:
        # ECP-ENG-009
        sys.path.insert(0, str(REPOSITORY_ROOT))
        from repository_tools.diagnostic_code_index import PREFIXES, _CODE, registry, scan

        names = registry(REPOSITORY_ROOT)
        for path in sorted(ENGINE.glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    for match in _CODE.finditer(node.value):
                        if match.group(1) in PREFIXES:
                            self.fail(f"{path.name}:{node.lineno} spells {match.group(0)}")
        self.assertIn("E012", names.values())
        self.assertIn("W_HEX_001", names)
        indexed = scan(REPOSITORY_ROOT)
        self.assertTrue(any("evidence path does not identify an existing file" in message for message in indexed["E"]["E012"]))
        self.assertTrue(any(message.startswith("W-REB-003: ") for message in indexed["W-REB"]["W-REB-003"]))
        self.assertIn("I-REV-001", indexed["I-REV"])


if __name__ == "__main__":
    unittest.main()
