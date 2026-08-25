"""Evidence for REQ-AUT-001, REQ-AUT-002, REQ-AUT-004, and REQ-AUT-006 (WO-AUT-001)."""

from __future__ import annotations

import contextlib
import io
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from se_harness.cli import main
from se_harness.preflight import _load_validator_module
from tests.mutation_guard_support import trusted_mutation_authority
from tests.test_revision_provenance import create_base_chain

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = REPOSITORY_ROOT / "templates/repository/standard/docs/engineering/templates/REQUIREMENT.template.md"
POLICY = REPOSITORY_ROOT / "templates/repository/standard/docs/engineering/ARTIFACT_AUTHORING.md"


class ArtifactAuthoringPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        code, _, error = self.invoke("init", str(self.root), "--project-name", "Authoring Fixture")
        self.assertEqual(0, code, error)
        guard = mock.patch(
            "se_harness.mutation_guard.require_mutation_authority",
            side_effect=trusted_mutation_authority,
        )
        guard.start()
        self.addCleanup(guard.stop)
        create_base_chain(self.root, operating_contract_status="draft")
        self.requirement = self.root / "docs/engineering/product/requirements/REQ-001.md"

    def invoke(self, *arguments: str) -> tuple[int, str, str]:
        output = io.StringIO()
        error = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            code = main(list(arguments))
        return code, output.getvalue(), error.getvalue()

    def set_front_matter(self, **fields: str) -> None:
        text = self.requirement.read_text(encoding="utf-8")
        for name, value in fields.items():
            pattern = re.compile(rf"^{name} = .*$", re.MULTILINE)
            if pattern.search(text):
                text = pattern.sub(lambda _m: f"{name} = {value}", text, count=1)
            else:
                text = text.replace("\n[relations]", f"\n{name} = {value}\n[relations]", 1)
        self.requirement.write_text(text, encoding="utf-8")

    def diagnostics(self) -> tuple[list, list]:
        report = _load_validator_module().validate_repository(self.root)
        mine = lambda items: [item for item in items if item.path.endswith("REQ-001.md")]
        return mine(report.errors), mine(report.warnings)

    # ---------------------------------------------------------------- REQ-AUT-001

    def test_policy_is_managed_routed_once_listed_and_printed_by_create_artifact(self) -> None:
        installed = self.root / "docs/engineering/ARTIFACT_AUTHORING.md"
        self.assertTrue(installed.is_file())
        self.assertEqual(POLICY.read_bytes().replace(b"\r\n", b"\n"), installed.read_bytes().replace(b"\r\n", b"\n"))
        lock = json.loads((self.root / ".engineering-harness.lock").read_text(encoding="utf-8"))
        self.assertEqual("managed", lock["files"]["docs/engineering/ARTIFACT_AUTHORING.md"]["mode"])
        router = (self.root / "ENGINEERING_HARNESS.md").read_text(encoding="utf-8")
        self.assertEqual(1, router.count("docs/engineering/ARTIFACT_AUTHORING.md"))
        self.assertIn("| Authoring rules for formal artifacts |", router)
        from se_harness.preflight import POLICY_PATHS, REQUIRED_PATHS

        self.assertIn("docs/engineering/ARTIFACT_AUTHORING.md", REQUIRED_PATHS)
        self.assertIn("docs/engineering/ARTIFACT_AUTHORING.md", POLICY_PATHS)

        code, output, error = self.invoke(
            "create-artifact", str(self.root), "--domain", "product", "--type", "requirement", "--id", "REQ-002"
        )
        self.assertEqual(0, code, error)
        self.assertIn("authoring checklist for requirement", output)
        self.assertIn("One obligation", output)
        self.assertIn("five shapes", output)
        code, output, error = self.invoke(
            "create-artifact", str(self.root), "--domain", "product", "--type", "requirement", "--id", "REQ-003", "--quiet"
        )
        self.assertEqual(0, code, error)
        self.assertNotIn("authoring checklist", output)
        code, output, error = self.invoke(
            "create-artifact", str(self.root), "--domain", "product", "--type", "verification_record", "--id", "VREC-009"
        )
        self.assertEqual(0, code, error)
        self.assertNotIn("authoring checklist", output)
        # the checklist comes from the installed file, not package text
        installed.write_text(installed.read_text(encoding="utf-8").replace("- One obligation:", "- ONE OBLIGATION EDITED:"), encoding="utf-8")
        code, output, error = self.invoke(
            "create-artifact", str(self.root), "--domain", "product", "--type", "requirement", "--id", "REQ-004"
        )
        self.assertEqual(0, code, error)
        self.assertIn("ONE OBLIGATION EDITED", output)

    def test_draft_change_skill_applies_the_policy_and_its_vector_is_current(self) -> None:
        import hashlib

        from se_harness.skill_contract import build_skill_manifest, canonical_json_bytes, load_skill_contract

        core = REPOSITORY_ROOT / "templates/repository/standard/.agents/skills/harness-draft-change"
        text = (core / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("ARTIFACT_AUTHORING.md", text)
        self.assertIn("checklist is the review standard", text)
        contract = load_skill_contract(core / "skill-contract.json")
        self.assertEqual("1.0.2", contract.value["version"])
        vectors = json.loads((REPOSITORY_ROOT / "tests/fixtures/agentic_execution/phase3/portable_vectors.json").read_text(encoding="utf-8"))
        self.assertEqual(vectors["skills"]["harness-draft-change"]["manifest_sha256"], build_skill_manifest(core).sha256)
        self.assertEqual(
            vectors["skills"]["harness-draft-change"]["contract_sha256"],
            hashlib.sha256(canonical_json_bytes(contract.value)).hexdigest(),
        )
        policy = POLICY.read_text(encoding="utf-8")
        for heading in ("## requirement", "## specification", "## adr", "## verification", "## work_order", "## risk"):
            self.assertIn(heading, policy)
        self.assertNotIn("W-AUT-002", text)  # the skill does not restate the policy

    # ---------------------------------------------------------------- REQ-AUT-002

    def test_five_shapes_validate_clean_and_defects_are_signalled(self) -> None:
        clean = (
            '"THE SYSTEM SHALL refuse a lifecycle decision while the evaluator is unreachable."',
            '"WHEN a work order is selected, THE SYSTEM SHALL list its reading manifest."',
            '"WHILE the evaluator is unreachable, THE SYSTEM SHALL refuse a lifecycle decision."',
            '"IF a managed file is customized, THEN THE SYSTEM SHALL refuse the upgrade."',
            '"WHERE a risk section is configured, THE SYSTEM SHALL raise at its level."',
            '"THE Harness Explorer SHALL render the register."',
        )
        for statement in clean:
            with self.subTest(statement=statement):
                self.set_front_matter(statement=statement)
                errors, warnings = self.diagnostics()
                self.assertEqual([], [item for item in errors if item.code.startswith("E-AUT") or item.code == "E005"])
                self.assertEqual([], [item.code for item in warnings if item.code.startswith("W-AUT-00") and item.code != "W-AUT-004"])
        cases = {
            '"The system should list the manifest and SHALL do so quickly."': {"W-AUT-001"},
            '"WHEN X, THE SYSTEM SHALL do A, and SHALL do B."': {"W-AUT-002"},
            '"IF a file is customized, THE SYSTEM SHALL refuse."': {"W-AUT-001"},
            '"WHEN ' + "x" * 300 + ', THE SYSTEM SHALL respond."': {"W-AUT-003"},
        }
        for statement, expected in cases.items():
            with self.subTest(statement=statement[:40]):
                self.set_front_matter(statement=statement)
                _, warnings = self.diagnostics()
                self.assertEqual(expected, {item.code for item in warnings if item.code in {"W-AUT-001", "W-AUT-002", "W-AUT-003"}})
        self.set_front_matter(statement='"The system must respond."')
        errors, _ = self.diagnostics()
        self.assertIn("E005", {item.code for item in errors})

    # ---------------------------------------------------------------- REQ-AUT-004 and vocabulary

    def test_vocabulary_and_optional_attributes_are_validated(self) -> None:
        self.set_front_matter(verification_method='"automated-test"')
        errors, warnings = self.diagnostics()
        self.assertIn("W-AUT-004", {item.code for item in warnings})
        self.assertEqual([], [item for item in errors if item.code.startswith("E-AUT")])
        self.set_front_matter(verification_method='["test", "inspection"]')
        errors, warnings = self.diagnostics()
        self.assertNotIn("W-AUT-004", {item.code for item in warnings})
        self.assertEqual([], [item for item in errors if item.code.startswith("E-AUT")])
        self.set_front_matter(verification_method='["manual-review"]')
        errors, _ = self.diagnostics()
        self.assertIn("E-AUT-001", {item.code for item in errors})
        self.set_front_matter(verification_method='["test", "test"]')
        errors, _ = self.diagnostics()
        self.assertIn("E-AUT-001", {item.code for item in errors})
        self.set_front_matter(verification_method='["test"]', priority='"must"', source='"CAP-001"', measure='"under 300 ms at p95"')
        errors, _ = self.diagnostics()
        self.assertEqual([], [item for item in errors if item.code.startswith("E-AUT")])
        self.set_front_matter(priority='"high"')
        errors, _ = self.diagnostics()
        self.assertTrue(any(item.code == "E-AUT-002" and "priority" in item.message for item in errors))
        self.set_front_matter(priority='"should"', source='"REQ-999"')
        errors, _ = self.diagnostics()
        self.assertTrue(any(item.code == "E-AUT-002" and "REQ-999" in item.message for item in errors))
        self.set_front_matter(source='"ISO 29148 section 5.2"', measure='""')
        errors, _ = self.diagnostics()
        self.assertTrue(any(item.code == "E-AUT-002" and "measure" in item.message for item in errors))

    # ---------------------------------------------------------------- REQ-AUT-006

    def test_template_carries_six_headings_five_shapes_and_the_acceptance_link(self) -> None:
        text = TEMPLATE.read_text(encoding="utf-8")
        self.assertLess(len(text.encode("utf-8")), 2500)
        headings = re.findall(r"^## .*$", text, flags=re.MULTILINE)
        self.assertEqual(
            ["## Rationale", "## Behavior", "## Assumptions and dependencies", "## Acceptance examples", "## Open decisions"],
            headings,
        )
        for shape in ("THE SYSTEM SHALL", "WHEN <event>", "WHILE <state>", "IF <unwanted condition>, THEN", "WHERE <feature"):
            self.assertIn(shape, text)
        self.assertIn('verification_method = ["test"]', text)
        self.assertIn("acceptance/<REQ-ID>.feature", text)
        for field in ("priority = ", "source = ", "measure = "):
            self.assertIn(field, text)
        code, output, error = self.invoke(
            "create-artifact", str(self.root), "--domain", "product", "--type", "requirement", "--id", "REQ-005", "--quiet"
        )
        self.assertEqual(0, code, error)
        report = _load_validator_module().validate_repository(self.root)
        mine = [item for item in report.errors if item.path.endswith("REQ-005.md")]
        # an unfilled draft is structurally valid apart from its relation placeholder
        self.assertTrue(all("CAP-xxx" in item.message or item.code == "E006" for item in mine), mine)


if __name__ == "__main__":
    unittest.main()
