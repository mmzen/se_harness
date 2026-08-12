from __future__ import annotations

import contextlib
import io
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

from se_harness.cli import main


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPOSITORY_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from generate_harness_dashboard import generate_snapshot  # noqa: E402
from validate_engineering_artifacts import validate_repository  # noqa: E402


ASSESSMENT = {
    "outcome": "adr_required",
    "triggers": ["public-interface-or-protocol"],
    "rationale": "The architecture selects a public metadata contract.",
    "assessed_by": "technical-owner",
}


def _array(values: list[str]) -> str:
    return json.dumps(values, ensure_ascii=False)


def formal(
    artifact_id: str,
    artifact_type: str,
    status: str,
    relations: dict[str, list[str]],
    *,
    assessment: dict[str, object] | None = None,
) -> str:
    lines = [
        "+++",
        f'id = "{artifact_id}"',
        f'type = "{artifact_type}"',
        f'title = "{artifact_id} title"',
        f'status = "{status}"',
        'owners = ["technical-owner"]',
        'created = "2026-08-12"',
        'updated = "2026-08-12"',
    ]
    if artifact_type == "requirement":
        lines.extend(
            [
                'statement = "WHEN selected, THE SYSTEM SHALL behave deterministically."',
                'verification_method = "automated-test"',
            ]
        )
    lines.extend(["", "[relations]"])
    lines.extend(f"{name} = {_array(values)}" for name, values in relations.items())
    if assessment is not None:
        lines.extend(
            [
                "",
                "[decision_assessment]",
                f'outcome = {json.dumps(assessment["outcome"])}',
                f'triggers = {_array(assessment["triggers"])}',
                f'rationale = {json.dumps(assessment["rationale"])}',
                f'assessed_by = {json.dumps(assessment["assessed_by"])}',
            ]
        )
    lines.extend(["+++", "", f"# {artifact_type}: {artifact_id}", ""])
    return "\n".join(lines)


class ArchitectureTraceabilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "repository"
        self.assertEqual(0, self.invoke("init", str(self.root), "--project-name", "Trace Sample")[0])
        context = self.root / "docs" / "engineering" / "REPOSITORY_CONTEXT.md"
        content = re.sub(r"TODO\[[A-Za-z0-9-]+\]", "confirmed", context.read_text(encoding="utf-8"))
        context.write_text(content, encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def invoke(self, *arguments: str) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = main(list(arguments))
        return code, stdout.getvalue(), stderr.getvalue()

    def write(self, relative: str, content: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def build_chain(
        self,
        *,
        architecture_relations: dict[str, list[str]] | None = None,
        architecture_status: str = "approved",
        selected_architectures: list[str] | None = None,
        selected_specifications: list[str] | None = None,
        second_architecture: bool = False,
        second_specification: bool = False,
    ) -> None:
        base = "docs/engineering/product"
        self.write(f"{base}/intent/INT-TRC-001.md", formal("INT-TRC-001", "intent", "approved", {}))
        self.write(
            f"{base}/capabilities/CAP-TRC-001.md",
            formal("CAP-TRC-001", "capability", "approved", {"derives_from": ["INT-TRC-001"]}),
        )
        requirements = ["REQ-TRC-001", "REQ-TRC-002"]
        for requirement in requirements:
            self.write(
                f"{base}/requirements/{requirement}.md",
                formal(requirement, "requirement", "approved", {"derives_from": ["CAP-TRC-001"]}),
            )
        self.write(
            f"{base}/specifications/SPEC-TRC-001.md",
            formal("SPEC-TRC-001", "specification", "approved", {"specifies": requirements}),
        )
        if second_specification:
            self.write(
                f"{base}/specifications/SPEC-TRC-002.md",
                formal("SPEC-TRC-002", "specification", "approved", {"specifies": ["REQ-TRC-001"]}),
            )
        relations = architecture_relations or {
            "addresses": ["REQ-TRC-001"],
            "conforms_to": ["SPEC-TRC-001"],
        }
        self.write(
            f"{base}/architecture/ARCH-TRC-001.md",
            formal("ARCH-TRC-001", "architecture", architecture_status, relations, assessment=ASSESSMENT),
        )
        self.write(
            f"{base}/architecture/adr/ADR-TRC-001.md",
            formal("ADR-TRC-001", "adr", "approved", {"decides": ["ARCH-TRC-001"]}),
        )
        if second_architecture:
            self.write(
                f"{base}/architecture/ARCH-TRC-002.md",
                formal(
                    "ARCH-TRC-002",
                    "architecture",
                    "approved",
                    {"addresses": ["REQ-TRC-002"], "conforms_to": ["SPEC-TRC-001"]},
                    assessment=ASSESSMENT,
                ),
            )
            self.write(
                f"{base}/architecture/adr/ADR-TRC-002.md",
                formal("ADR-TRC-002", "adr", "approved", {"decides": ["ARCH-TRC-002"]}),
            )
        self.write(
            f"{base}/verification/VER-TRC-001.md",
            formal("VER-TRC-001", "verification", "approved", {"verifies": requirements}),
        )
        architecture_selection = selected_architectures or ["ARCH-TRC-001", "ADR-TRC-001"]
        specification_selection = selected_specifications or ["SPEC-TRC-001"]
        self.write(
            f"{base}/work-orders/WO-TRC-001.md",
            formal(
                "WO-TRC-001",
                "work_order",
                "approved",
                {
                    "implements": requirements,
                    "specifications": specification_selection,
                    "architecture": architecture_selection,
                    "verification": ["VER-TRC-001"],
                },
            ),
        )

    def preflight(self, *, json_output: bool = False) -> tuple[int, str, str]:
        arguments = ["preflight", str(self.root), "--work-order", "WO-TRC-001"]
        if json_output:
            arguments.append("--json")
        return self.invoke(*arguments)

    def test_validator_enforces_typed_targets_and_triangle(self) -> None:
        self.build_chain(second_specification=True)
        self.assertTrue(validate_repository(self.root).valid)
        architecture = self.root / "docs/engineering/product/architecture/ARCH-TRC-001.md"
        valid = architecture.read_text(encoding="utf-8")

        invalid_variants = {
            "missing typed relations": formal(
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
        path = self.write(
            "docs/engineering/product/architecture/ARCH-OWNER-001.md",
            "repository-owner legacy architecture bytes\r\n",
        )
        before = path.read_bytes()
        first = self.invoke("upgrade", str(self.root), "--apply")
        second = self.invoke("upgrade", str(self.root), "--apply")
        self.assertEqual(0, first[0], first[2])
        self.assertEqual(0, second[0], second[2])
        self.assertEqual(before, path.read_bytes())


if __name__ == "__main__":
    unittest.main()
