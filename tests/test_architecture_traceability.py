from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from se_harness.cli import main
from tests.mutation_guard_support import patch_mutation_authority


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
from tests.root_identity_support import evaluator_scripts_dir  # noqa: E402
SCRIPTS = evaluator_scripts_dir()
from tests.root_identity_support import load_evaluator_module
_generate_harness_dashboard = load_evaluator_module("generate_harness_dashboard")
generate_snapshot = _generate_harness_dashboard.generate_snapshot
_validate_engineering_artifacts = load_evaluator_module("validate_engineering_artifacts")
validate_repository = _validate_engineering_artifacts.validate_repository
from tests.fixture_support import standard_repository
from tests.cli_support import invoke
import functools
from tests.artifact_support import formal, write
complete_formal = functools.partial(formal, complete=True)


ASSESSMENT = {
    "outcome": "adr_required",
    "triggers": ["public-interface-or-protocol"],
    "rationale": "The architecture selects a public metadata contract.",
    "assessed_by": "technical-owner",
}


class ArchitectureTraceabilityTests(unittest.TestCase):
    def setUp(self) -> None:
        patch_mutation_authority(self)
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "repository"
        standard_repository(self.root)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def build_chain(
        self,
        *,
        architecture_relations: dict[str, list[str]] | None = None,
        architecture_status: str = "approved",
        selected_architectures: list[str] | None = None,
        selected_specifications: list[str] | None = None,
        second_architecture: bool = False,
        second_specification: bool = False,
        omit_architecture_relation: bool = False,
    ) -> None:
        base = "docs/engineering/product"
        write(self.root / f"{base}/intent/INT-TRC-001.md", complete_formal("INT-TRC-001", "intent", "approved", {}))
        write(self.root / 
            f"{base}/capabilities/CAP-TRC-001.md",
            complete_formal("CAP-TRC-001", "capability", "approved", {"derives_from": ["INT-TRC-001"]}),
        )
        requirements = ["REQ-TRC-001", "REQ-TRC-002"]
        for requirement in requirements:
            write(self.root / 
                f"{base}/requirements/{requirement}.md",
                complete_formal(requirement, "requirement", "approved", {"derives_from": ["CAP-TRC-001"]}),
            )
        write(self.root / 
            f"{base}/specifications/SPEC-TRC-001.md",
            complete_formal("SPEC-TRC-001", "specification", "approved", {"specifies": requirements}),
        )
        if second_specification:
            write(self.root / 
                f"{base}/specifications/SPEC-TRC-002.md",
                complete_formal("SPEC-TRC-002", "specification", "approved", {"specifies": ["REQ-TRC-001"]}),
            )
        relations = architecture_relations or {
            "addresses": ["REQ-TRC-001"],
            "conforms_to": ["SPEC-TRC-001"],
        }
        write(self.root / 
            f"{base}/architecture/ARCH-TRC-001.md",
            complete_formal("ARCH-TRC-001", "architecture", architecture_status, relations, assessment=ASSESSMENT),
        )
        write(self.root / 
            f"{base}/architecture/adr/ADR-TRC-001.md",
            complete_formal("ADR-TRC-001", "adr", "approved", {"decides": ["ARCH-TRC-001"]}),
        )
        if second_architecture:
            write(self.root / 
                f"{base}/architecture/ARCH-TRC-002.md",
                complete_formal(
                    "ARCH-TRC-002",
                    "architecture",
                    "approved",
                    {"addresses": ["REQ-TRC-002"], "conforms_to": ["SPEC-TRC-001"]},
                    assessment=ASSESSMENT,
                ),
            )
            write(self.root / 
                f"{base}/architecture/adr/ADR-TRC-002.md",
                complete_formal("ADR-TRC-002", "adr", "approved", {"decides": ["ARCH-TRC-002"]}),
            )
        write(self.root / 
            f"{base}/verification/VER-TRC-001.md",
            complete_formal("VER-TRC-001", "verification", "approved", {"verifies": requirements}),
        )
        architecture_selection = (
            ["ARCH-TRC-001", "ADR-TRC-001"]
            if selected_architectures is None
            else selected_architectures
        )
        specification_selection = selected_specifications or ["SPEC-TRC-001"]
        work_order_relations = {
            "implements": requirements,
            "specifications": specification_selection,
            "verification": ["VER-TRC-001"],
        }
        if not omit_architecture_relation:
            work_order_relations["architecture"] = architecture_selection
        write(self.root / 
            f"{base}/work-orders/WO-TRC-001.md",
            complete_formal(
                "WO-TRC-001",
                "work_order",
                "approved",
                work_order_relations,
            ),
        )

    def preflight(self, *, json_output: bool = False) -> tuple[int, str, str]:
        arguments = ["preflight", str(self.root), "--work-order", "WO-TRC-001"]
        if json_output:
            arguments.append("--json")
        return invoke(*arguments)

    def test_validator_enforces_typed_targets_and_triangle(self) -> None:
        self.build_chain(second_specification=True)
        self.assertTrue(validate_repository(self.root).valid)
        architecture = self.root / "docs/engineering/product/architecture/ARCH-TRC-001.md"
        valid = architecture.read_text(encoding="utf-8")

        invalid_variants = {
            "missing typed relations": complete_formal(
                "ARCH-TRC-001",
                "architecture",
                "approved",
                {"constrains": ["REQ-TRC-001"]},
                assessment=ASSESSMENT,
            ),
            "addresses specification": valid.replace(
                'addresses = ["REQ-TRC-001"]', 'addresses = ["SPEC-TRC-001"]'
            ),
            "conforms to requirement": valid.replace(
                'conforms_to = ["SPEC-TRC-001"]', 'conforms_to = ["REQ-TRC-001"]'
            ),
            "incoherent triangle": valid.replace(
                'conforms_to = ["SPEC-TRC-001"]', 'conforms_to = ["SPEC-TRC-002"]'
            ).replace('addresses = ["REQ-TRC-001"]', 'addresses = ["REQ-TRC-002"]'),
            "duplicate driver": valid.replace(
                'addresses = ["REQ-TRC-001"]',
                'addresses = ["REQ-TRC-001", "REQ-TRC-001"]',
            ),
            "non-array driver": valid.replace(
                'addresses = ["REQ-TRC-001"]', 'addresses = "REQ-TRC-001"'
            ),
            "unknown injection-shaped driver": valid.replace(
                'addresses = ["REQ-TRC-001"]', 'addresses = ["REQ-TRC-999;echo-pwned"]'
            ),
        }
        for label, content in invalid_variants.items():
            with self.subTest(label=label):
                architecture.write_text(content, encoding="utf-8")
                codes = {item.code for item in validate_repository(self.root).errors}
                self.assertTrue({"E011", "E016"}.intersection(codes), codes)
        architecture.write_text(valid, encoding="utf-8")

    def test_legacy_classifier_is_status_and_target_type_bounded(self) -> None:
        self.build_chain(
            architecture_relations={"constrains": ["REQ-TRC-001"]},
            architecture_status="approved",
        )
        architecture = self.root / "docs/engineering/product/architecture/ARCH-TRC-001.md"
        self.assertIn("E016", {item.code for item in validate_repository(self.root).errors})

        content = architecture.read_text(encoding="utf-8").replace('status = "approved"', 'status = "implemented"')
        architecture.write_text(content, encoding="utf-8")
        report = validate_repository(self.root)
        self.assertTrue(report.valid)
        self.assertIn("W015", {item.code for item in report.warnings})

        architecture.write_text(
            content.replace('constrains = ["REQ-TRC-001"]', 'constrains = ["SPEC-TRC-001"]'),
            encoding="utf-8",
        )
        report = validate_repository(self.root)
        self.assertTrue(report.valid)
        self.assertIn("W015", {item.code for item in report.warnings})

        architecture.write_text(
            content.replace(
                'constrains = ["REQ-TRC-001"]',
                'constrains = ["REQ-TRC-001", "SPEC-TRC-001"]',
            ),
            encoding="utf-8",
        )
        self.assertIn("E016", {item.code for item in validate_repository(self.root).errors})

    def test_dual_declared_bootstrap_must_be_consistent(self) -> None:
        self.build_chain(
            architecture_relations={
                "constrains": ["REQ-TRC-001"],
                "addresses": ["REQ-TRC-001"],
                "conforms_to": ["SPEC-TRC-001"],
            }
        )
        report = validate_repository(self.root)
        self.assertTrue(report.valid)
        self.assertIn("W015", {item.code for item in report.warnings})

        architecture = self.root / "docs/engineering/product/architecture/ARCH-TRC-001.md"
        architecture.write_text(
            architecture.read_text(encoding="utf-8").replace(
                'constrains = ["REQ-TRC-001"]', 'constrains = ["REQ-TRC-002"]'
            ),
            encoding="utf-8",
        )
        self.assertIn("E016", {item.code for item in validate_repository(self.root).errors})

    def test_routine_requirement_does_not_need_nominal_architecture_coverage(self) -> None:
        self.build_chain()
        code, output, error = self.preflight()
        self.assertEqual(0, code, error)
        self.assertIn("Harness preflight: PASS", output)

        first = self.preflight(json_output=True)
        second = self.preflight(json_output=True)
        self.assertEqual(0, first[0], first[2])
        self.assertEqual(first[1], second[1])
        self.assertTrue(json.loads(first[1])["ready"])

    def test_work_order_may_omit_architecture_when_none_is_active(self) -> None:
        self.build_chain(architecture_status="draft", omit_architecture_relation=True)
        self.assertTrue(validate_repository(self.root).valid)
        code, output, error = self.preflight()
        self.assertEqual(0, code, error)
        self.assertIn("Harness preflight: PASS", output)
        self.assertNotIn("[W014]", output)

    def test_present_empty_work_order_architecture_relation_is_invalid(self) -> None:
        self.build_chain(selected_architectures=[])
        report = validate_repository(self.root)
        self.assertFalse(report.valid)
        self.assertTrue(
            any(
                item.code == "E005"
                and "architecture" in item.message
                and "non-empty array" in item.message
                for item in report.errors
            ),
            report.errors,
        )

    def test_preflight_rejects_omitted_applicable_architecture(self) -> None:
        self.build_chain(omit_architecture_relation=True)
        self.assertTrue(validate_repository(self.root).valid)
        code, output, _ = self.preflight()
        self.assertEqual(1, code)
        self.assertIn("[W022]", output)
        self.assertIn("ARCH-TRC-001", output)

    def test_preflight_requires_every_applicable_architecture(self) -> None:
        self.build_chain(second_architecture=True)
        code, output, _ = self.preflight()
        self.assertEqual(1, code)
        self.assertIn("[W022]", output)
        self.assertIn("ARCH-TRC-002", output)

    def test_preflight_rejects_selected_architecture_unrelated_to_selected_specification(self) -> None:
        self.build_chain(
            second_specification=True,
            architecture_relations={
                "addresses": ["REQ-TRC-001"],
                "conforms_to": ["SPEC-TRC-002"],
            },
            selected_specifications=["SPEC-TRC-001"],
        )
        code, output, _ = self.preflight()
        self.assertEqual(1, code)
        self.assertIn("[W021]", output)
        self.assertIn("ARCH-TRC-001", output)

    def test_explorer_distinguishes_declared_and_derived_traceability(self) -> None:
        self.build_chain()
        snapshot, report, _ = generate_snapshot(self.root)
        self.assertTrue(report.valid)
        architecture = next(item for item in snapshot["artifacts"] if item["id"] == "ARCH-TRC-001")
        traceability = architecture["architecture_traceability"]
        self.assertEqual("typed", traceability["state"])
        self.assertEqual(["REQ-TRC-001"], traceability["addresses"])
        self.assertEqual(["SPEC-TRC-001"], traceability["conforms_to"])
        self.assertEqual(["REQ-TRC-001", "REQ-TRC-002"], traceability["transitive_requirements"])
        derived = [
            relation
            for relation in snapshot["relations"]
            if relation["source"] == "ARCH-TRC-001"
            and relation["relation"] == "conforms_transitively_to_requirement"
        ]
        self.assertEqual(2, len(derived))
        self.assertTrue(all(item["authority"] == "derived" for item in derived))

    def test_managed_authoring_guidance_uses_typed_relations(self) -> None:
        expectations = {
            "docs/engineering/templates/ARCHITECTURE.template.md": (
                'addresses = ["REQ-xxx"]',
                'conforms_to = ["SPEC-xxx"]',
            ),
            "docs/engineering/templates/WORK_ORDER.template.md": (
                "architecturally significant requirement",
                "selected specifications",
            ),
            "docs/engineering/TRACEABILITY.md": (
                "`ARCH.addresses -> REQ`",
                "`ARCH.conforms_to -> SPEC`",
            ),
            "docs/engineering/QUALITY_GATES.md": (
                "architecturally significant requirement drivers",
            ),
        }
        for relative, phrases in expectations.items():
            with self.subTest(path=relative):
                content = (self.root / relative).read_text(encoding="utf-8")
                for phrase in phrases:
                    self.assertIn(phrase, content)

    def test_upgrade_does_not_rewrite_repository_owned_legacy_architecture(self) -> None:
        path = write(self.root / 
            "docs/engineering/product/architecture/ARCH-OWNER-001.md",
            "repository-owner legacy architecture bytes\r\n",
        )
        before = path.read_bytes()
        first = invoke("upgrade", str(self.root), "--apply")
        second = invoke("upgrade", str(self.root), "--apply")
        self.assertEqual(0, first[0], first[2])
        self.assertEqual(0, second[0], second[2])
        self.assertEqual(before, path.read_bytes())


if __name__ == "__main__":
    unittest.main()
