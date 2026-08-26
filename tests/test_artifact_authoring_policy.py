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
        self.assertEqual("2.0.0", contract.value["version"])
        vectors = json.loads(
            (REPOSITORY_ROOT / "tests/fixtures/agentic_execution/phase4/skills/portable-vectors.json").read_text(
                encoding="utf-8"
            )
        )
        current = vectors["skills"]["harness-draft-change"]["current"]
        self.assertEqual(current["manifest_sha256"], build_skill_manifest(core).sha256)
        self.assertEqual(
            current["contract_sha256"],
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
            ("- Trigger: <the observable condition or event; \"always\" for an invariant>", "- Trigger: a work order is selected"),
            ("- Response: <what the reader can check>", "- Response: the manifest is listed"),
            ("- On failure: <what happens when the response cannot be given>", "- On failure: the command exits 1"),
            ("<What this obligation relies on; not how it is built — that is a specification's job.>", "None."),
        ):
            self.assertIn(placeholder, filled, placeholder)
            filled = filled.replace(placeholder, value)
        # keep the acceptance/<REQ-ID>.feature sentence: it is inside inline code and must not count
        path.write_text(filled.replace("## Open decisions\n\nNone.", "## Open decisions\n\nWhether the manifest is sorted."), encoding="utf-8")
        code, message = approve()
        self.assertEqual(1, code)
        self.assertIn("open decision", message)
        self.assertIn("sorted", message)

        path.write_text(filled, encoding="utf-8")
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
        errors, warnings = self.diagnostics()
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
        # the repository itself is untouched: every requirement still carries the string form
        self.assertEqual([], [f for f in (REPOSITORY_ROOT / "docs/engineering").rglob("requirements/REQ-*.md") if re.search(r"^verification_method = \[", f.read_text(encoding="utf-8"), re.MULTILINE)])
