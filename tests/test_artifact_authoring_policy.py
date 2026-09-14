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
from se_harness.engine import validate_engineering_artifacts
from tests.mutation_guard_support import patch_mutation_authority
from tests.artifact_support import create_base_chain
from tests.fixture_support import standard_repository
from tests.cli_support import invoke

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = REPOSITORY_ROOT / "templates/repository/standard/docs/engineering/templates/REQUIREMENT.template.md"
POLICY = REPOSITORY_ROOT / "templates/repository/standard/docs/engineering/ARTIFACT_AUTHORING.md"


class ArtifactAuthoringPolicyFixture:
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        standard_repository(self.root)
        patch_mutation_authority(self)
        create_base_chain(self.root, operating_contract_status="draft")
        self.requirement = self.root / "docs/engineering/product/requirements/REQ-001.md"

    def set_front_matter(self, **fields: str) -> None:
        text = self.requirement.read_text(encoding="utf-8")
        for name, value in fields.items():
            pattern = re.compile(rf"^{name} = .*$", re.MULTILINE)
            if pattern.search(text):
                text = pattern.sub(lambda _m: f"{name} = {value}", text, count=1)
            else:
                text = text.replace("\n[relations]", f"\n{name} = {value}\n[relations]", 1)
        self.requirement.write_text(text, encoding="utf-8")

    def diagnostics(self) -> tuple[list, list, list]:
        report = validate_engineering_artifacts.validate_repository(self.root)
        mine = lambda items: [item for item in items if item.path.endswith("REQ-001.md")]
        return mine(report.errors), mine(report.warnings), mine(report.advisories)

    # ---------------------------------------------------------------- REQ-AUT-001


class ArtifactAuthoringPolicyTests(ArtifactAuthoringPolicyFixture, unittest.TestCase):
    def test_policy_is_managed_routed_once_listed_and_printed_by_create_artifact(self) -> None:
        installed = self.root / "docs/engineering/ARTIFACT_AUTHORING.md"
        self.assertTrue(installed.is_file())
        self.assertEqual(POLICY.read_bytes().replace(b"\r\n", b"\n"), installed.read_bytes().replace(b"\r\n", b"\n"))
        lock = json.loads((self.root / ".engineering-harness.lock").read_text(encoding="utf-8"))
        self.assertEqual("seed", lock["files"]["docs/engineering/ARTIFACT_AUTHORING.md"]["mode"])
        router = (self.root / "ENGINEERING_HARNESS.md").read_text(encoding="utf-8")
        self.assertEqual(1, router.count("docs/engineering/ARTIFACT_AUTHORING.md"))
        self.assertIn("| Authoring rules for formal artifacts |", router)
        from se_harness.preflight import POLICY_PATHS, REQUIRED_PATHS

        self.assertIn("docs/engineering/ARTIFACT_AUTHORING.md", REQUIRED_PATHS)
        self.assertIn("docs/engineering/ARTIFACT_AUTHORING.md", POLICY_PATHS)

        code, output, error = invoke(
            "create-artifact", str(self.root), "--domain", "product", "--type", "requirement", "--id", "REQ-002"
        )
        self.assertEqual(0, code, error)
        self.assertIn("authoring checklist for requirement", output)
        self.assertIn("observable behavior", output)
        self.assertIn("acceptance condition", output)
        code, output, error = invoke(
            "create-artifact", str(self.root), "--domain", "product", "--type", "requirement", "--id", "REQ-003", "--quiet"
        )
        self.assertEqual(0, code, error)
        self.assertNotIn("authoring checklist", output)
        code, output, error = invoke(
            "create-artifact", str(self.root), "--domain", "product", "--type", "verification_record", "--id", "VREC-009"
        )
        self.assertEqual(0, code, error)
        self.assertNotIn("authoring checklist", output)
        # the checklist comes from the installed file, not package text
        installed.write_text(installed.read_text(encoding="utf-8").replace("- State the observable behavior", "- ONE OBLIGATION EDITED"), encoding="utf-8")
        code, output, error = invoke(
            "create-artifact", str(self.root), "--domain", "product", "--type", "requirement", "--id", "REQ-004"
        )
        self.assertEqual(0, code, error)
        self.assertIn("ONE OBLIGATION EDITED", output)


    def test_plain_requirement_and_old_shall_form_both_validate(self) -> None:
        for statement in ('"The command returns the reading manifest."', '"THE SYSTEM SHALL return the reading manifest."'):
            with self.subTest(statement=statement):
                self.set_front_matter(status='"draft"', statement=statement)
                errors, _, advisories = self.diagnostics()
                self.assertEqual([], [i for i in errors if i.code.startswith("E-AUT") or i.code == "E005"])
                self.assertEqual([], advisories)
        self.set_front_matter(statement='""')
        self.assertTrue(any("statement" in i.message for i in self.diagnostics()[0]))

    # ---------------------------------------------------------------- REQ-AUT-004 and vocabulary

    def test_vocabulary_and_optional_attributes_are_validated(self) -> None:
        self.set_front_matter(status='"draft"', verification_method='"automated-test"')
        errors, warnings, advisories = self.diagnostics()
        self.assertNotIn("W-AUT-004", {item.code for item in advisories})
        self.assertNotIn("W-AUT-004", {item.code for item in warnings})
        self.assertEqual([], [item for item in errors if item.code.startswith("E-AUT")])
        self.set_front_matter(verification_method='["test", "inspection"]')
        errors, warnings, advisories = self.diagnostics()
        self.assertNotIn("W-AUT-004", {item.code for item in advisories})
        self.assertEqual([], [item for item in errors if item.code.startswith("E-AUT")])
        self.set_front_matter(verification_method='["manual-review"]')
        errors, _, _ = self.diagnostics()
        self.assertIn("E-AUT-001", {item.code for item in errors})
        self.set_front_matter(verification_method='["test", "test"]')
        errors, _, _ = self.diagnostics()
        self.assertIn("E-AUT-001", {item.code for item in errors})
        self.set_front_matter(verification_method='["test"]', priority='"must"', source='"CAP-001"', measure='"under 300 ms at p95"')
        errors, _, _ = self.diagnostics()
        self.assertEqual([], [item for item in errors if item.code.startswith("E-AUT")])
        self.set_front_matter(priority='"high"')
        errors, _, _ = self.diagnostics()
        self.assertTrue(any(item.code == "E-AUT-002" and "priority" in item.message for item in errors))
        self.set_front_matter(priority='"should"', source='"REQ-999"')
        errors, _, _ = self.diagnostics()
        self.assertTrue(any(item.code == "E-AUT-002" and "REQ-999" in item.message for item in errors))
        self.set_front_matter(source='"ISO 29148 section 5.2"', measure='""')
        errors, _, _ = self.diagnostics()
        self.assertTrue(any(item.code == "E-AUT-002" and "measure" in item.message for item in errors))

    # ---------------------------------------------------------------- REQ-AUT-006

    def test_requirement_template_gives_an_acceptance_example(self) -> None:
        text = TEMPLATE.read_text(encoding="utf-8")
        self.assertIn('statement = ', text)
        self.assertIn('verification_method = ["test"]', text)
        self.assertIn("## Examples", text)
        code, output, error = invoke("create-artifact", str(self.root), "--domain", "product", "--type", "requirement", "--id", "REQ-005", "--quiet")
        self.assertEqual(0, code, error + output)
        self.assertTrue((self.root / "docs/engineering/product/requirements/REQ-005.md").is_file())


if __name__ == "__main__":
    unittest.main()


    # ---------------------------------------------------------------- REQ-AUT-007




class ApprovalPredicateTests(ArtifactAuthoringPolicyFixture, unittest.TestCase):
    """Evidence for REQ-AUT-005 (WO-AUT-002); REQ-AUT-003's migration ran under WO-AUT-005."""

    def test_definition_gates_carry_the_authoring_predicate(self) -> None:
        from se_harness.workflow_contract import load_validated_contracts

        _, _, _, _, gates = load_validated_contracts()
        self.assertIn("QGP-G1-AUTHORING", [p["id"] for p in gates["QG-G1-DEFINITION"]["predicates"]])
        self.assertIn("QGP-G2-AUTHORING", [p["id"] for p in gates["QG-G2-ARCHITECTURE"]["predicates"]])

    def test_approval_is_refused_while_a_placeholder_or_an_open_decision_remains(self) -> None:
        code, _, error = invoke(
            "create-artifact", str(self.root), "--domain", "product", "--type", "requirement", "--id", "REQ-002", "--quiet"
        )
        self.assertEqual(0, code, error)
        path = self.root / "docs/engineering/product/requirements/REQ-002.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace('derives_from = ["CAP-xxx"]', 'derives_from = ["CAP-001"]')
        text = text.replace('source = "<stakeholder, standard clause, incident, or artifact ID>"', 'source = "CAP-001"')
        text = text.replace('measure = "<value and unit, for a quality requirement>"', 'measure = "n/a"')
        path.write_text(text, encoding="utf-8")
        for relative, relation in (("specifications/SPEC-001.md", "specifies"), ("verification/VER-001.md", "verifies")):
            covering = self.root / "docs/engineering/product" / relative
            covering.write_text(
                covering.read_text(encoding="utf-8").replace(f'{relation} = ["REQ-001"]', f'{relation} = ["REQ-001", "REQ-002"]'),
                encoding="utf-8",
            )

        def approve() -> tuple[int, str]:
            code, output, error = invoke(
                "transition", str(self.root), "--set", "REQ-002=approved", "--decision", "REQ-002=requirements-steward", "--apply"
            )
            return code, output + error

        code, message = approve()
        self.assertEqual(1, code)
        self.assertIn("QGP-G1-AUTHORING", message)
        self.assertIn("<Observable obligation>", message)
        self.assertIn('status = "draft"', path.read_text(encoding="utf-8"))

        filled = path.read_text(encoding="utf-8")
        for placeholder, value in (
            ('title = "<Observable obligation>"', 'title = "List the manifest"'),
            ('owners = ["<product/domain owner>"]', 'owners = ["product-owner"]'),
            ('statement = "<The observable behavior the system provides.>"', 'statement = "WHEN a work order is selected, THE SYSTEM SHALL list its reading manifest."'),
            ("# Requirement: <title>", "# Requirement: List the manifest"),
            ("<the observable condition or event; \"always\" for an invariant>", "a work order is selected"),
            ("<what the reader can check>", "the manifest is listed"),
            ("<what happens when the response cannot be given>", "the command exits 1"),
        ):
            self.assertIn(placeholder, filled, placeholder)
            filled = filled.replace(placeholder, value)
        # the two guidance paragraphs are placeholders too: replace them whole
        filled = re.sub(r"<One or two sentences a newcomer understands\..*?>", "The command lists what to read.", filled, flags=re.S)
        filled = re.sub(r"<Why the obligation exists\..*?>", "A reader needs the list before the work.", filled, flags=re.S)
        self.assertNotIn("<", filled.split("+++", 2)[2].replace("<REQ", ""))
        # WO-TCM-005: the template carries no Open decisions section; a legacy one with
        # prose is still refused (E-DCM-004), and its absence is not.
        path.write_text(filled + "\n## Open decisions\n\nWhether the manifest is sorted.\n", encoding="utf-8")
        code, message = approve()
        self.assertEqual(1, code)
        self.assertIn("open decision", message)
        self.assertIn("sorted", message)

        path.write_text(filled, encoding="utf-8")
        self.assertNotIn("Open decisions", filled)
        code, message = approve()
        self.assertEqual(0, code, message)
        self.assertIn('status = "approved"', path.read_text(encoding="utf-8"))


class CorpusMigrationTests(unittest.TestCase):
    """Evidence for REQ-AUT-008 (WO-AUT-005): SPEC-AUT-003 AUT-MIG-009 over this corpus."""

    ENGINEERING = REPOSITORY_ROOT / "docs/engineering"
    EXCLUDED = {"templates", "evidence"}
    TRIGGERS = frozenset(
        {
            "system-boundary",
            "responsibility-or-dependency-direction",
            "public-interface-or-protocol",
            "data-ownership-or-persistence",
            "security-privacy-or-trust-boundary",
            "deployment-or-operating-model",
            "concurrency-consistency-reliability-or-failure-strategy",
            "technology-framework-vendor-or-external-service",
            "material-performance-scalability-or-cost-tradeoff",
            "cross-cutting-policy",
            "difficult-to-reverse",
            "material-alternatives",
        }
    )
    COMPLETED = frozenset({"implemented", "verified", "released"})
    METHODS = frozenset({"test", "analysis", "inspection", "demonstration"})

    def artifacts(self, artifact_type: str) -> list[tuple[str, dict]]:
        from se_harness import front_matter

        found = []
        for path in sorted(self.ENGINEERING.rglob("*.md")):
            if self.EXCLUDED & set(path.relative_to(self.ENGINEERING).parts):
                continue
            metadata = front_matter.read_or_none(path)
            if metadata is None or metadata.get("type") != artifact_type:
                continue
            found.append((path.relative_to(REPOSITORY_ROOT).as_posix(), metadata))
        self.assertNotEqual([], found, artifact_type)
        return found

    def test_no_architecture_carries_the_legacy_relation(self) -> None:
        legacy = [
            path
            for path, metadata in self.artifacts("architecture")
            if "constrains" in (metadata.get("relations") or {})
        ]
        self.assertEqual([], legacy, "AUT-MIG-001: constrains is retired")

    def test_every_completed_architecture_carries_a_valid_assessment(self) -> None:
        for path, metadata in self.artifacts("architecture"):
            if metadata.get("status") not in self.COMPLETED:
                continue
            with self.subTest(path=path):
                assessment = metadata.get("decision_assessment")
                self.assertIsInstance(assessment, dict, "AUT-MIG-003: an assessment is required")
                self.assertIn(assessment.get("outcome"), {"adr_required", "no_significant_decision"})
                triggers = assessment.get("triggers")
                self.assertIsInstance(triggers, list)
                if assessment["outcome"] == "adr_required":
                    self.assertNotEqual([], triggers)
                self.assertEqual([], [t for t in triggers if t not in self.TRIGGERS])
                self.assertTrue((assessment.get("rationale") or "").strip())
                self.assertTrue((assessment.get("assessed_by") or "").strip())

    def test_no_requirement_holds_a_string_verification_method(self) -> None:
        for path, metadata in self.artifacts("requirement"):
            with self.subTest(path=path):
                method = metadata.get("verification_method")
                self.assertIsInstance(method, list, "AUT-MIG-007: the vocabulary form is an array")
                self.assertNotEqual([], method)
                self.assertEqual([], [item for item in method if item not in self.METHODS])

    def test_the_one_shot_migration_left_the_repository(self) -> None:
        # AUT-MIG-007: the script, its test and its note paragraph are gone. The
        # name is assembled so that this assertion is not its own counterexample.
        script = "migrate_" + "verification_methods"
        self.assertFalse((REPOSITORY_ROOT / "scripts" / f"{script}.py").exists())
        for path in sorted((REPOSITORY_ROOT / "tests").glob("test_*.py")):
            self.assertNotIn(script, path.read_text(encoding="utf-8"), path.name)
        note = (REPOSITORY_ROOT / "docs/notes/artifact-authoring.md").read_text(encoding="utf-8")
        self.assertNotIn(script, note)
        specification = (
            REPOSITORY_ROOT / "docs/engineering/artifact-authoring/specifications/SPEC-AUT-001.md"
        ).read_text(encoding="utf-8")
        self.assertIn("WO-AUT-005", specification, "AUT-MIG-008: the amendment record")
