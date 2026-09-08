from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

from se_harness.cli import main


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


SIGNIFICANT_ASSESSMENT = {
    "outcome": "adr_required",
    "triggers": ["system-boundary", "data-ownership-or-persistence"],
    "rationale": "The design selects system boundaries and durable data ownership.",
    "assessed_by": "technical-owner",
}
NO_DECISION_ASSESSMENT = {
    "outcome": "no_significant_decision",
    "triggers": [],
    "rationale": "The work applies the existing architecture without changing a material trade-off.",
    "assessed_by": "technical-owner",
}


class AdrApplicabilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "repository"
        standard_repository(self.root)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def build_chain(
        self,
        *,
        assessment: dict[str, object] | None = SIGNIFICANT_ASSESSMENT,
        architecture_status: str = "approved",
        selected_adrs: list[str] | None = None,
        second_architecture: bool = False,
        shared_adr: bool = False,
    ) -> None:
        base = "docs/engineering/product"
        write(self.root / f"{base}/intent/INT-ADR-001.md", complete_formal("INT-ADR-001", "intent", "approved", {}))
        write(self.root / 
            f"{base}/capabilities/CAP-ADR-001.md",
            complete_formal("CAP-ADR-001", "capability", "approved", {"derives_from": ["INT-ADR-001"]}),
        )
        requirements = ["REQ-ADR-001"]
        write(self.root / 
            f"{base}/requirements/REQ-ADR-001.md",
            complete_formal("REQ-ADR-001", "requirement", "approved", {"derives_from": ["CAP-ADR-001"]}),
        )
        write(self.root / 
            f"{base}/specifications/SPEC-ADR-001.md",
            complete_formal("SPEC-ADR-001", "specification", "approved", {"specifies": requirements}),
        )
        write(self.root / 
            f"{base}/verification/VER-ADR-001.md",
            complete_formal("VER-ADR-001", "verification", "approved", {"verifies": requirements}),
        )
        architecture_ids = ["ARCH-ADR-001"]
        write(self.root / 
            f"{base}/architecture/ARCH-ADR-001.md",
            complete_formal(
                "ARCH-ADR-001",
                "architecture",
                architecture_status,
                {"addresses": requirements, "conforms_to": ["SPEC-ADR-001"]},
                assessment=assessment,
            ),
        )
        if second_architecture:
            architecture_ids.append("ARCH-ADR-002")
            write(self.root / 
                f"{base}/architecture/ARCH-ADR-002.md",
                complete_formal(
                    "ARCH-ADR-002",
                    "architecture",
                    architecture_status,
                    {"addresses": requirements, "conforms_to": ["SPEC-ADR-001"]},
                    assessment=assessment,
                ),
            )
        decided = architecture_ids if shared_adr else ["ARCH-ADR-001"]
        write(self.root / 
            f"{base}/architecture/adr/ADR-ADR-001.md",
            complete_formal("ADR-ADR-001", "adr", "approved", {"decides": decided}),
        )
        if second_architecture:
            write(self.root / 
                f"{base}/architecture/adr/ADR-ADR-002.md",
                complete_formal("ADR-ADR-002", "adr", "approved", {"decides": ["ARCH-ADR-002"]}),
            )
        selected = selected_adrs if selected_adrs is not None else ["ADR-ADR-001"]
        write(self.root / 
            f"{base}/work-orders/WO-ADR-001.md",
            complete_formal(
                "WO-ADR-001",
                "work_order",
                "approved",
                {
                    "implements": requirements,
                    "specifications": ["SPEC-ADR-001"],
                    "architecture": [*architecture_ids, *selected],
                    "verification": ["VER-ADR-001"],
                },
            ),
        )

    def preflight(self, *, json_output: bool = False) -> tuple[int, str, str]:
        arguments = ["preflight", str(self.root), "--work-order", "WO-ADR-001"]
        if json_output:
            arguments.append("--json")
        return invoke(*arguments)

    def test_validator_enforces_assessment_shape_and_controlled_values(self) -> None:
        self.build_chain()
        report = validate_repository(self.root)
        self.assertNotIn("E014", {item.code for item in report.errors})
        architecture = self.root / "docs/engineering/product/architecture/ARCH-ADR-001.md"
        valid = architecture.read_text(encoding="utf-8")

        invalid_variants = {
            "missing": complete_formal(
                "ARCH-ADR-001",
                "architecture",
                "approved",
                {"addresses": ["REQ-ADR-001"], "conforms_to": ["SPEC-ADR-001"]},
            ),
            "unknown outcome": valid.replace('outcome = "adr_required"', 'outcome = "agent_choice"'),
            "unknown trigger": valid.replace("system-boundary", "shell;echo-pwned"),
            "duplicate trigger": valid.replace(
                'triggers = ["system-boundary", "data-ownership-or-persistence"]',
                'triggers = ["system-boundary", "system-boundary"]',
            ),
            "empty rationale": valid.replace(
                'rationale = "The design selects system boundaries and durable data ownership."',
                'rationale = ""',
            ),
            "empty assessor": valid.replace('assessed_by = "technical-owner"', 'assessed_by = ""'),
            "required without trigger": valid.replace(
                'triggers = ["system-boundary", "data-ownership-or-persistence"]', "triggers = []"
            ),
            "no decision with trigger": valid.replace(
                'outcome = "adr_required"', 'outcome = "no_significant_decision"'
            ),
            "oversized rationale": valid.replace(
                'rationale = "The design selects system boundaries and durable data ownership."',
                f'rationale = "{"x" * 2001}"',
            ),
        }
        for label, content in invalid_variants.items():
            with self.subTest(label=label):
                architecture.write_text(content, encoding="utf-8")
                self.assertIn("E014", {item.code for item in validate_repository(self.root).errors})

        architecture.write_text(valid, encoding="utf-8")
        requirement = self.root / "docs/engineering/product/requirements/REQ-ADR-001.md"
        requirement.write_text(
            requirement.read_text(encoding="utf-8").replace(
                "+++\n\n# requirement",
                "\n[decision_assessment]\noutcome = \"no_significant_decision\"\ntriggers = []\n"
                "rationale = \"not applicable\"\nassessed_by = \"technical-owner\"\n+++\n\n# requirement",
            ),
            encoding="utf-8",
        )
        self.assertIn("E014", {item.code for item in validate_repository(self.root).errors})

    def test_preflight_requires_related_adr_for_each_significant_architecture(self) -> None:
        self.build_chain(second_architecture=True, shared_adr=False, selected_adrs=["ADR-ADR-001"])
        code, output, _ = self.preflight()
        self.assertEqual(1, code)
        self.assertIn("[W018]", output)
        self.assertIn("ARCH-ADR-002", output)

        adr = self.root / "docs/engineering/product/architecture/adr/ADR-ADR-001.md"
        adr.write_text(
            adr.read_text(encoding="utf-8").replace(
                'decides = ["ARCH-ADR-001"]',
                'decides = ["ARCH-ADR-001", "ARCH-ADR-002"]',
            ),
            encoding="utf-8",
        )
        code, output, error = self.preflight()
        self.assertEqual(0, code, error)
        self.assertIn("Harness preflight: PASS", output)

    def test_no_significant_decision_passes_without_ceremonial_adr(self) -> None:
        self.build_chain(assessment=NO_DECISION_ASSESSMENT, selected_adrs=[])
        code, output, error = self.preflight()
        self.assertEqual(0, code, error)
        self.assertIn("Harness preflight: PASS", output)

        code, output, error = self.preflight(json_output=True)
        self.assertEqual(0, code, error)
        report = json.loads(output)
        self.assertTrue(report["ready"])
        self.assertEqual([], report["diagnostics"])

    def test_unrelated_selected_adr_cannot_satisfy_significant_architecture(self) -> None:
        self.build_chain(second_architecture=True, selected_adrs=["ADR-ADR-002"])
        work_order = self.root / "docs/engineering/product/work-orders/WO-ADR-001.md"
        work_order.write_text(
            work_order.read_text(encoding="utf-8").replace(
                'architecture = ["ARCH-ADR-001", "ARCH-ADR-002", "ADR-ADR-002"]',
                'architecture = ["ARCH-ADR-001", "ADR-ADR-002"]',
            ),
            encoding="utf-8",
        )
        code, output, _ = self.preflight()
        self.assertEqual(1, code)
        self.assertIn("[W017]", output)
        self.assertIn("[W018]", output)
        self.assertIn("ARCH-ADR-001", output)

    def test_completed_legacy_architecture_requires_existing_selected_adr(self) -> None:
        self.build_chain(assessment=None, architecture_status="implemented")
        report = validate_repository(self.root)
        self.assertTrue(report.valid)
        self.assertIn("W014", {item.code for item in report.warnings})
        self.assertEqual(0, self.preflight()[0])

        work_order = self.root / "docs/engineering/product/work-orders/WO-ADR-001.md"
        work_order.write_text(
            work_order.read_text(encoding="utf-8").replace(
                'architecture = ["ARCH-ADR-001", "ADR-ADR-001"]',
                'architecture = ["ARCH-ADR-001"]',
            ),
            encoding="utf-8",
        )
        code, output, _ = self.preflight()
        self.assertEqual(1, code)
        self.assertIn("[W019]", output)

    def test_ongoing_architecture_cannot_use_legacy_exception(self) -> None:
        for status in ("draft", "approved", "in_progress"):
            with self.subTest(status=status):
                root = self.root
                self.build_chain(assessment=None, architecture_status=status)
                report = validate_repository(root)
                self.assertIn("E014", {item.code for item in report.errors})

    def test_managed_authoring_guidance_is_distributed(self) -> None:
        expectations = {
            "docs/engineering/templates/ARCHITECTURE.template.md": (
                "[decision_assessment]",
                "Initial software design normally activates one or more triggers",
            ),
            "docs/engineering/templates/ADR.template.md": (
                "one coherent significant decision",
                "do not create ceremonial ADRs",
            ),
            "docs/engineering/templates/WORK_ORDER.template.md": (
                "every applicable architecture plus every required deciding ADR",
            ),
            "docs/engineering/WORKFLOW.md": (
                "decision applicability",
                "no one-ADR-per-requirement rule exists",
            ),
            "docs/engineering/DECISION_RIGHTS.md": (
                "MUST NOT approve its own architecture decision assessment",
            ),
            "docs/engineering/QUALITY_GATES.md": (
                "each `adr_required` architecture has active deciding ADR coverage",
            ),
            "docs/engineering/TRACEABILITY.md": (
                "`ADR.decides -> ARCH` establishes coverage",
            ),
        }
        for relative, phrases in expectations.items():
            with self.subTest(path=relative):
                content = (self.root / relative).read_text(encoding="utf-8")
                for phrase in phrases:
                    self.assertIn(phrase, content)

    def test_explorer_exposes_assessment_state_and_coverage_anomaly(self) -> None:
        self.build_chain()
        snapshot, report, _ = generate_snapshot(self.root)
        self.assertTrue(report.valid)
        architecture = next(item for item in snapshot["artifacts"] if item["id"] == "ARCH-ADR-001")
        self.assertEqual("adr_required_covered", architecture["decision_assessment"]["state"])
        self.assertEqual(["ADR-ADR-001"], architecture["decision_assessment"]["deciding_adrs"])

        adr = self.root / "docs/engineering/product/architecture/adr/ADR-ADR-001.md"
        adr.write_text(
            adr.read_text(encoding="utf-8").replace(
                'decides = ["ARCH-ADR-001"]', 'decides = ["ARCH-ADR-002"]'
            ),
            encoding="utf-8",
        )
        snapshot, report, _ = generate_snapshot(self.root)
        self.assertFalse(report.valid)
        architecture = next(item for item in snapshot["artifacts"] if item["id"] == "ARCH-ADR-001")
        self.assertEqual("adr_required_missing", architecture["decision_assessment"]["state"])
        self.assertIn("E015", {item["rule"] for item in snapshot["findings"]})


if __name__ == "__main__":
    unittest.main()
