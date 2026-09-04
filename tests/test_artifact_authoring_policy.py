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
from tests.fixture_support import standard_repository

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = REPOSITORY_ROOT / "templates/repository/standard/docs/engineering/templates/REQUIREMENT.template.md"
POLICY = REPOSITORY_ROOT / "templates/repository/standard/docs/engineering/ARTIFACT_AUTHORING.md"


class ArtifactAuthoringPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        standard_repository(self.root, "Authoring Fixture")
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

    def diagnostics(self) -> tuple[list, list, list]:
        report = _load_validator_module().validate_repository(self.root)
        mine = lambda items: [item for item in items if item.path.endswith("REQ-001.md")]
        return mine(report.errors), mine(report.warnings), mine(report.advisories)

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


    def test_five_shapes_validate_clean_and_defects_are_signalled(self) -> None:
        clean = (
            '"THE SYSTEM SHALL refuse a lifecycle decision while the evaluator is unreachable."',
            '"WHEN a work order is selected, THE SYSTEM SHALL list its reading manifest."',
            '"WHILE the evaluator is unreachable, THE SYSTEM SHALL refuse a lifecycle decision."',
            '"IF a managed file is customized, THEN THE SYSTEM SHALL refuse the upgrade."',
            '"WHERE a risk section is configured, THE SYSTEM SHALL raise at its level."',
            '"THE Harness Explorer SHALL render the register."',
        )
        self.set_front_matter(status='"draft"')
        for statement in clean:
            with self.subTest(statement=statement):
                self.set_front_matter(statement=statement)
                errors, warnings, advisories = self.diagnostics()
                self.assertEqual([], [item for item in errors if item.code.startswith("E-AUT") or item.code == "E005"])
                self.assertEqual([], [item.code for item in advisories if item.code not in {"W-AUT-004", "W-AUT-009"}])
                self.assertEqual([], [item.code for item in warnings if item.code.startswith("W-AUT-")])
        cases = {
            '"The system should list the manifest and SHALL do so quickly."': {"W-AUT-001"},
            '"WHEN X, THE SYSTEM SHALL do A, and SHALL do B."': {"W-AUT-002"},
            '"IF a file is customized, THE SYSTEM SHALL refuse."': {"W-AUT-001"},
            '"WHEN ' + "x " * 32 + ', THE SYSTEM SHALL respond."': {"W-AUT-003"},
            '"WHEN a requirement is validated, THE SYSTEM SHALL count its words."': {"W-AUT-010"},
        }
        for statement, expected in cases.items():
            with self.subTest(statement=statement[:40]):
                self.set_front_matter(statement=statement)
                _, warnings, advisories = self.diagnostics()
                self.assertEqual(expected, {item.code for item in advisories if item.code in {"W-AUT-001", "W-AUT-002", "W-AUT-003", "W-AUT-010"}})
                self.assertEqual([], [item.code for item in warnings if item.code.startswith("W-AUT-")])
        self.set_front_matter(statement='"The system must respond."')
        errors, _, _ = self.diagnostics()
        self.assertIn("E005", {item.code for item in errors})

    # ---------------------------------------------------------------- REQ-AUT-004 and vocabulary

    def test_vocabulary_and_optional_attributes_are_validated(self) -> None:
        self.set_front_matter(status='"draft"', verification_method='"automated-test"')
        errors, warnings, advisories = self.diagnostics()
        self.assertIn("W-AUT-004", {item.code for item in advisories})
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

    def test_template_carries_the_reader_first_shape_and_five_shapes(self) -> None:
        # WO-TCM-005 (SPEC-TCM-003 TCM-RFR-001): four sections, no Open decisions,
        # the glossary pointer names a file the repository writes.
        text = TEMPLATE.read_text(encoding="utf-8")
        self.assertLess(len(text.encode("utf-8")), 2500)
        headings = re.findall(r"^## .*$", text, flags=re.MULTILINE)
        self.assertEqual(["## In plain words", "## Why", "## Behavior", "## Examples"], headings)
        self.assertEqual(["### Normal", "### Failure"], re.findall(r"^### .*$", text, flags=re.MULTILINE))
        for shape in ("THE SYSTEM SHALL", "WHEN <event>", "WHILE <state>", "IF <unwanted condition>, THEN", "WHERE <feature"):
            self.assertIn(shape, text)
        self.assertIn('verification_method = ["test"]', text)
        self.assertIn("| Trigger | Response | On failure |", text)
        self.assertIn("`GLOSSARY.md` at the repository", text)
        self.assertNotIn("Open decisions", text)
        self.assertNotIn("acceptance/", text)
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


    # ---------------------------------------------------------------- REQ-AUT-007

    def test_advisories_are_raised_only_on_drafts(self) -> None:
        # AUT-ADV-002: the same faults on an approved requirement raise nothing.
        faulty = '"The system should list the manifest and SHALL do A, and SHALL do B ' + "x " * 30 + '."'
        self.set_front_matter(status='"draft"', statement=faulty, verification_method='"automated-test"')
        _, warnings, advisories = self.diagnostics()
        # W-AUT-009: the fixture body is a stub without an In plain words section (WO-TCM-005)
        self.assertEqual({"W-AUT-001", "W-AUT-002", "W-AUT-003", "W-AUT-004", "W-AUT-009"}, {item.code for item in advisories})
        self.assertEqual([], [item.code for item in warnings if item.code.startswith("W-AUT-")])
        self.set_front_matter(status='"approved"')
        _, warnings, advisories = self.diagnostics()
        self.assertEqual([], advisories)
        self.assertEqual([], [item.code for item in warnings if item.code.startswith("W-AUT-")])

    def test_advisories_are_reported_apart_in_the_summary_the_listing_and_the_json(self) -> None:
        # AUT-ADV-001, -003, -004, -005.
        module = _load_validator_module()
        self.set_front_matter(status='"draft"', statement='"WHEN X, THE SYSTEM SHALL do A, and SHALL do B."')
        report = module.validate_repository(self.root)
        mine = [item for item in report.advisories if item.path.endswith("REQ-001.md")]
        self.assertEqual(["W-AUT-002"], [item.code for item in mine])
        self.assertEqual([], [item for item in report.warnings if item.code.startswith("W-AUT-")])
        payload = report.to_dict(self.root)
        self.assertEqual(len(report.advisories), payload["advisory_count"])
        self.assertEqual(len(report.warnings), payload["warning_count"])
        self.assertEqual([item["code"] for item in payload["advisories"]], [item.code for item in sorted(report.advisories)])
        self.assertEqual(
            sum(counts["warnings"] for counts in payload["plane_counts"].values()), payload["warning_count"]
        )
        quiet = module.render_human(report)
        loud = module.render_human(report, show_advisories=True)
        summary = f"Artifacts: {len(report.artifacts)} | Errors: {len(report.errors)} | Warnings: {len(report.warnings)} | Advisories: {len(report.advisories)}"
        self.assertIn(summary, quiet)
        self.assertNotIn("\nAdvisories:\n", quiet)
        self.assertNotIn("[W-AUT-002]", quiet)
        self.assertIn("\nAdvisories:\n", loud)
        self.assertIn("[W-AUT-002] [maintenance]", loud)
        self.assertIn("Planes:", quiet)
        code, output, error = self.invoke("validate", str(self.root))
        self.assertIn(summary, output)
        self.assertNotIn("Advisories:\n", output)
        code, output, error = self.invoke("validate", str(self.root), "--advisories")
        self.assertIn("\nAdvisories:\n", output)
        self.assertIn("[W-AUT-002]", output)
        code, output, error = self.invoke("validate", str(self.root), "--json")
        self.assertEqual(payload["advisory_count"], json.loads(output)["advisory_count"])


class ApprovalPredicateAndMigrationTests(ArtifactAuthoringPolicyTests):
    """Evidence for REQ-AUT-003 (built, not applied here) and REQ-AUT-005 (WO-AUT-002)."""

    def test_definition_gates_carry_the_authoring_predicate(self) -> None:
        from se_harness.workflow_contract import load_validated_contracts

        _, _, _, _, gates = load_validated_contracts()
        self.assertIn("QGP-G1-AUTHORING", [p["id"] for p in gates["QG-G1-DEFINITION"]["predicates"]])
        self.assertIn("QGP-G2-AUTHORING", [p["id"] for p in gates["QG-G2-ARCHITECTURE"]["predicates"]])

    def test_approval_is_refused_while_a_placeholder_or_an_open_decision_remains(self) -> None:
        code, _, error = self.invoke(
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
            code, output, error = self.invoke(
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
            ('statement = "WHEN <event>, THE SYSTEM SHALL <observable response>."', 'statement = "WHEN a work order is selected, THE SYSTEM SHALL list its reading manifest."'),
            ("# Requirement: <title>", "# Requirement: List the manifest"),
            ("<the observable condition or event; \"always\" for an invariant>", "a work order is selected"),
            ("<what the reader can check>", "the manifest is listed"),
            ("<what happens when the response cannot be given>", "the command exits 1"),
        ):
            self.assertIn(placeholder, filled, placeholder)
            filled = filled.replace(placeholder, value)
        # the two guidance paragraphs are placeholders too: replace them whole
        filled = re.sub(r"<One or two sentences a newcomer understands\..*?>", "The command lists what to read.", filled, flags=re.S)
        filled = re.sub(r"<At most five sentences\..*?>", "A reader needs the list before the work.", filled, flags=re.S)
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

    def test_migration_maps_strings_keeps_originals_and_is_idempotent(self) -> None:
        import importlib.util
        import subprocess
        import sys

        script = REPOSITORY_ROOT / "scripts/migrate_verification_methods.py"
        spec = importlib.util.spec_from_file_location("migrate_verification_methods", script)
        module = importlib.util.module_from_spec(spec)
        sys.dont_write_bytecode = True
        try:
            spec.loader.exec_module(module)
        finally:
            sys.dont_write_bytecode = False
        self.assertEqual(["test"], module.map_value("automated-test"))
        self.assertEqual(["test", "inspection"], module.map_value("automated-test-and-manual-review"))
        self.assertEqual(["analysis"], module.map_value("hosted-exact-recipe-replay"))
        self.assertEqual(["demonstration"], module.map_value("inspection-and-end-to-end")[1:])
        self.assertEqual([], module.map_value("automated-active-surface-invariant"))

        self.set_front_matter(verification_method='"automated-test-and-manual-review"')
        before = self.requirement.read_text(encoding="utf-8")
        completed = subprocess.run(
            [sys.executable, str(script), "--root", str(self.root)], capture_output=True, text=True, check=True
        )
        self.assertEqual(before, self.requirement.read_text(encoding="utf-8"), "dry run must not write")
        report = json.loads(completed.stdout)
        entry = report["files"]["docs/engineering/product/requirements/REQ-001.md"]
        self.assertEqual({"state": "mapped", "original": "automated-test-and-manual-review", "mapped": ["test", "inspection"]}, entry)

        subprocess.run([sys.executable, str(script), "--root", str(self.root), "--apply"], capture_output=True, text=True, check=True)
        after = self.requirement.read_text(encoding="utf-8")
        self.assertIn('verification_method = ["test", "inspection"]', after)
        self.assertIn('verification_notes = "automated-test-and-manual-review"', after)
        errors, warnings, advisories = self.diagnostics()
        self.assertEqual([], [item for item in errors if item.code.startswith("E-AUT")])
        self.assertNotIn("W-AUT-004", {item.code for item in warnings})
        subprocess.run([sys.executable, str(script), "--root", str(self.root), "--apply"], capture_output=True, text=True, check=True)
        self.assertEqual(after, self.requirement.read_text(encoding="utf-8"), "second run must be a no-op")

        self.requirement.write_text("+++\nid = \"REQ-001\"\nverification_method = \"x\"\n", encoding="utf-8")
        completed = subprocess.run([sys.executable, str(script), "--root", str(self.root)], capture_output=True, text=True)
        self.assertEqual(2, completed.returncode)
        self.assertIn("refusing", completed.stderr)

    def test_repository_dry_run_report_is_retained_and_matches_a_fresh_run(self) -> None:
        import subprocess
        import sys

        retained = REPOSITORY_ROOT / "docs/engineering/artifact-authoring/evidence/WO-AUT-002/verification-method-mapping.json"
        self.assertTrue(retained.is_file())
        report = json.loads(retained.read_text(encoding="utf-8"))
        self.assertFalse(report["applied"])
        self.assertEqual(0, report["counts"]["skipped"])
        completed = subprocess.run(
            [sys.executable, str(REPOSITORY_ROOT / "scripts/migrate_verification_methods.py"), "--root", str(REPOSITORY_ROOT)],
            capture_output=True, text=True, check=True,
        )
        fresh = json.loads(completed.stdout)
        # WO-CIP-004: the retained report is a dry run at one commit; later requirements may
        # extend the fresh report, but every retained observation must remain stable.
        retained_paths = set(report["files"])
        fresh_paths = set(fresh["files"])
        self.assertLessEqual(retained_paths, fresh_paths)
        self.assertEqual(
            report["files"],
            {path: fresh["files"][path] for path in retained_paths},
            "retained historical observations must remain stable",
        )
        added = fresh_paths - retained_paths
        expected_counts = dict(report["counts"])
        for path in added:
            state = fresh["files"][path]["state"]
            expected_counts[state] += 1
        self.assertEqual(expected_counts, fresh["counts"])
        # WO-AUT-003: the migration was built and not applied, so every requirement the
        # retained dry run observed still carries its original string form. Requirements
        # drafted after the report follow REQ-AUT-003 and carry the array form; they are
        # exactly the ones the retained report does not list.
        array_form = re.compile(r"^verification_method = \[", re.MULTILINE)
        for path in sorted(retained_paths):
            with self.subTest(path=path):
                self.assertIsNone(array_form.search((REPOSITORY_ROOT / path).read_text(encoding="utf-8")))
        array_requirements = sorted(
            f.relative_to(REPOSITORY_ROOT).as_posix()
            for f in (REPOSITORY_ROOT / "docs/engineering").rglob("requirements/REQ-*.md")
            if array_form.search(f.read_text(encoding="utf-8"))
        )
        self.assertEqual([], [path for path in array_requirements if path in retained_paths])
        self.assertEqual(set(array_requirements), {path for path in added if fresh["files"][path]["state"] == "skipped"})
