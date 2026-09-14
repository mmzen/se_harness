from __future__ import annotations

import ast
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
from se_harness.installer import ENGINE_ROOT  # noqa: E402
from tests.root_identity_support import root_copy  # noqa: E402
from tests.root_identity_support import load_evaluator_module
from tests.artifact_support import formal, write
SCRIPTS = REPOSITORY_ROOT / "scripts"
_validate_engineering_artifacts = load_evaluator_module("validate_engineering_artifacts")
TAXONOMY_VERSION = _validate_engineering_artifacts.TAXONOMY_VERSION
VALIDATION_PLANES = _validate_engineering_artifacts.VALIDATION_PLANES
Diagnostic = _validate_engineering_artifacts.Diagnostic
ValidationReport = _validate_engineering_artifacts.ValidationReport
render_human = _validate_engineering_artifacts.render_human
validate_repository = _validate_engineering_artifacts.validate_repository


class ValidationTaxonomyTests(unittest.TestCase):
    def test_every_diagnostic_emission_declares_a_plane(self) -> None:
        # WO-HUP-017 (SPEC-HUP-017 HUP-ADP-016): the root copy when the lock names it, else the engine copy.
        # WO-ECP-036 (SPEC-ECP-024 ECP-ENG-017): the validator is split along its seams, so every
        # engine module is read, the entry file and the validation_* seams alike.
        root_source = root_copy("scripts/validate_engineering_artifacts.py")
        sources = [root_source] if root_source is not None else sorted(ENGINE_ROOT.glob("*.py"))
        missing: list[str] = []
        for path in sources:
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
                    continue
                if node.func.id in {"add_error", "_add_error"} and not any(
                    keyword.arg == "plane" for keyword in node.keywords
                ):
                    missing.append(f"{path.name}:{node.lineno}")
                if (
                    node.func.id == "Diagnostic"
                    and len(node.args) < 4
                    and not any(keyword.arg == "plane" for keyword in node.keywords)
                ):
                    missing.append(f"{path.name}:{node.lineno}")
        self.assertEqual([], missing)

    def test_policy_and_operator_reference_document_the_machine_vocabulary(self) -> None:
        guide = (REPOSITORY_ROOT / "templates/repository/standard/docs/engineering/QUALITY_GATES.md").read_text(encoding="utf-8")
        reference = (REPOSITORY_ROOT / "docs/notes/harnessctl-reference.md").read_text(encoding="utf-8")
        for plane in VALIDATION_PLANES:
            self.assertIn(f"`{plane}`", guide)
            self.assertIn(f"`{plane}`", reference)

    def test_vocabulary_and_diagnostic_construction_are_closed(self) -> None:
        self.assertEqual(
            ("structure", "governance", "policy", "maintenance"),
            VALIDATION_PLANES,
        )
        self.assertEqual("se-harness-validation-taxonomy-v1", TAXONOMY_VERSION)
        for plane in VALIDATION_PLANES:
            self.assertEqual(plane, Diagnostic("artifact.md", "E001", "message", plane).plane)
        with self.assertRaises(ValueError):
            Diagnostic("artifact.md", "E001", "message", "other")

    def test_json_and_human_reports_add_planes_without_a_score(self) -> None:
        report = ValidationReport(
            artifacts=[],
            errors=[Diagnostic("broken.md", "E001", "broken", "structure")],
            warnings=[Diagnostic("legacy.md", "W013", "legacy", "maintenance")],
        )
        payload = report.to_dict(Path.cwd())
        self.assertEqual(TAXONOMY_VERSION, payload["taxonomy"])
        self.assertEqual(
            {
                "structure": {"errors": 1, "warnings": 0},
                "governance": {"errors": 0, "warnings": 0},
                "policy": {"errors": 0, "warnings": 0},
                "maintenance": {"errors": 0, "warnings": 1},
            },
            payload["plane_counts"],
        )
        self.assertEqual("structure", payload["errors"][0]["plane"])
        self.assertEqual("maintenance", payload["warnings"][0]["plane"])
        rendered = render_human(report)
        self.assertIn("Planes:", rendered)
        self.assertIn("[E001] [structure] broken.md: broken", rendered)
        self.assertIn("[W013] [maintenance] legacy.md: legacy", rendered)
        self.assertNotIn("score", rendered.lower())

    def test_current_rule_authority_selects_the_expected_plane(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)

            structure_root = root / "structure"
            write(
                structure_root / "docs/engineering/sample/intent/INT-TAX-001.md",
                '''+++
id = "INT-TAX-001"
type = "intent"
status = "approved"
owners = ["owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
+++
''',
            )
            structure = validate_repository(structure_root)
            self.assertTrue(structure.errors)
            self.assertEqual({"structure"}, {item.plane for item in structure.errors})

            governance_root = root / "governance"
            base = governance_root / "docs/engineering/sample"
            write(base / "intent/INT-TAX-001.md", formal("INT-TAX-001", "intent", "approved", {}))
            write(
                base / "capabilities/CAP-TAX-001.md",
                formal("CAP-TAX-001", "capability", "approved", {"derives_from": ["INT-TAX-001"]}),
            )
            write(
                base / "requirements/REQ-TAX-001.md",
                formal(
                    "REQ-TAX-001",
                    "requirement",
                    "approved",
                    {"derives_from": ["CAP-TAX-001"]},
                    extra='statement = "THE SYSTEM SHALL classify findings."\nverification_method = "test"',
                ),
            )
            governance = validate_repository(governance_root)
            coverage = [item for item in governance.errors if item.code in {"E007", "E008"}]
            self.assertEqual(2, len(coverage))
            self.assertEqual({"governance"}, {item.plane for item in coverage})

            policy_root = root / "policy"
            base = policy_root / "docs/engineering/sample"
            write(
                policy_root / ".engineering-harness.toml",
                "[revision_provenance]\nrequired_for_verified_work = true\nrequired_for_release = false",
            )
            write(base / "intent/INT-TAX-001.md", formal("INT-TAX-001", "intent", "approved", {}))
            write(
                base / "capabilities/CAP-TAX-001.md",
                formal("CAP-TAX-001", "capability", "approved", {"derives_from": ["INT-TAX-001"]}),
            )
            write(
                base / "requirements/REQ-TAX-001.md",
                formal(
                    "REQ-TAX-001",
                    "requirement",
                    "implemented",
                    {"derives_from": ["CAP-TAX-001"]},
                    extra='statement = "THE SYSTEM SHALL classify findings."\nverification_method = "test"',
                ),
            )
            write(
                base / "specifications/SPEC-TAX-001.md",
                formal("SPEC-TAX-001", "specification", "implemented", {"specifies": ["REQ-TAX-001"]}),
            )
            write(
                base / "verification/VER-TAX-001.md",
                formal("VER-TAX-001", "verification", "approved", {"verifies": ["REQ-TAX-001"]}),
            )
            write(
                base / "work-orders/WO-TAX-001.md",
                formal(
                    "WO-TAX-001",
                    "work_order",
                    "verified",
                    {
                        "implements": ["REQ-TAX-001"],
                        "specifications": ["SPEC-TAX-001"],
                        "verification": ["VER-TAX-001"],
                    },
                ),
            )
            policy = validate_repository(policy_root)
            configured = [
                item
                for item in policy.errors
                if item.code == "E010" and "requires coverage" in item.message
            ]
            self.assertEqual(1, len(configured))
            self.assertEqual("policy", configured[0].plane)

            maintenance_root = root / "maintenance"
            write(
                maintenance_root / "docs/engineering/sample/INT-TAX-001.md",
                formal("INT-TAX-001", "intent", "approved", {}),
            )
            maintenance = validate_repository(maintenance_root)
            placement = [item for item in maintenance.warnings if item.code == "W013"]
            self.assertEqual(1, len(placement))
            self.assertEqual("maintenance", placement[0].plane)


if __name__ == "__main__":
    unittest.main()
