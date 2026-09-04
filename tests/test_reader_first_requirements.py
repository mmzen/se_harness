"""Evidence for REQ-TCM-006 and REQ-TCM-008 (WO-TCM-005): the reader-first requirement shape."""

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
from tests.test_revision_provenance import create_base_chain, formal, write

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = REPOSITORY_ROOT / "templates/repository/standard/docs/engineering/templates"

PLAIN = "The command lists what to read before the work starts."
WHY = "A reader needs the list before the work. It is short by design."
BEHAVIOR = "| Trigger | Response | On failure |\n| --- | --- | --- |\n| a work order is selected | the manifest is listed | the command exits 1 |"
EXAMPLES = "### Normal\n\n**Given** a work order, **When** it is selected, **Then** the manifest is listed.\n\n### Failure\n\n**Given** no work order, **When** selection runs, **Then** the command exits 1."


def reader_first_body(*, plain: str = PLAIN, why: str = WHY, extra: str = "") -> str:
    return (
        f"\n## In plain words\n\n{plain}\n\n## Why\n\n{why}\n\n## Behavior\n\n{BEHAVIOR}\n\n## Examples\n\n{EXAMPLES}\n{extra}"
    )


class ReaderFirstRequirementTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        code, _, error = self.invoke("init", str(self.root), "--project-name", "Reader Fixture")
        self.assertEqual(0, code, error)
        lock_path = self.root / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["evaluator"]["archive_name"] = f"se_harness-{lock['tool_version'].replace('-', '_')}-py3-none-any.whl"
        lock["evaluator"]["archive_sha256"] = "a" * 64
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        guard = mock.patch(
            "se_harness.mutation_guard.require_mutation_authority",
            side_effect=trusted_mutation_authority,
        )
        guard.start()
        self.addCleanup(guard.stop)
        create_base_chain(self.root, operating_contract_status="draft")
        self.path = self.root / "docs/engineering/product/requirements/REQ-002.md"
        for relative, relation in (("specifications/SPEC-001.md", "specifies"), ("verification/VER-001.md", "verifies")):
            covering = self.root / "docs/engineering/product" / relative
            covering.write_text(
                covering.read_text(encoding="utf-8").replace(f'{relation} = ["REQ-001"]', f'{relation} = ["REQ-001", "REQ-002"]'),
                encoding="utf-8",
            )

    def invoke(self, *arguments: str) -> tuple[int, str, str]:
        output = io.StringIO()
        error = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            code = main(list(arguments))
        return code, output.getvalue(), error.getvalue()

    def write_requirement(self, *, status: str = "draft", statement: str = "WHEN a work order is selected, THE SYSTEM SHALL list its reading manifest.", body: str | None = None) -> None:
        text = formal(
            "REQ-002", "requirement", status, {"derives_from": ["CAP-001"]},
            f'statement = "{statement}"\nverification_method = ["test"]\npriority = "must"\nsource = "CAP-001"',
        )
        write(self.path, text + (reader_first_body() if body is None else body))

    def advisories(self) -> dict[str, str]:
        report = _load_validator_module().validate_repository(self.root)
        self.assertEqual([], [f"{i.code}: {i.message}" for i in report.errors if i.path.endswith("REQ-002.md")])
        return {item.code: item.message for item in report.advisories if item.path.endswith("REQ-002.md")}

    # ---------------------------------------------------------------- REQ-TCM-006: template

    def test_every_definition_template_has_no_open_decisions_and_the_requirement_template_is_reader_first(self) -> None:
        for template in sorted(TEMPLATES.glob("*.template.md")):
            with self.subTest(template=template.name):
                self.assertNotIn("## Open decisions", template.read_text(encoding="utf-8"))
        text = (TEMPLATES / "REQUIREMENT.template.md").read_text(encoding="utf-8")
        self.assertEqual(["## In plain words", "## Why", "## Behavior", "## Examples"], re.findall(r"^## .*$", text, flags=re.MULTILINE))
        self.assertIn("`GLOSSARY.md` at the repository", text)
        self.assertIn("which this repository writes", text)
        code, output, error = self.invoke("create-artifact", str(self.root), "--domain", "product", "--type", "requirement", "--id", "REQ-003", "--quiet")
        self.assertEqual(0, code, error + output)
        created = (self.root / "docs/engineering/product/requirements/REQ-003.md").read_text(encoding="utf-8")
        self.assertIn("## In plain words", created)
        self.assertNotIn("## Open decisions", created)

    # ---------------------------------------------------------------- REQ-TCM-006: advisories

    def test_a_reader_first_draft_within_every_budget_raises_no_advisory(self) -> None:
        self.write_requirement()
        self.assertEqual({}, self.advisories())

    def test_each_budget_raises_exactly_its_advisory_with_the_measured_value(self) -> None:
        long_statement = "WHEN " + " ".join(f"word{i}" for i in range(30)) + ", THE SYSTEM SHALL respond."
        self.write_requirement(statement=long_statement)
        found = self.advisories()
        self.assertEqual({"W-AUT-003"}, set(found))
        self.assertIn("35 words; the budget is 30", found["W-AUT-003"])

        long_body = reader_first_body(extra="\n## More\n\n" + " ".join(["word"] * 260) + ".\n")
        self.write_requirement(body=long_body)
        found = self.advisories()
        self.assertEqual({"W-AUT-005", "W-AUT-007"}, set(found))
        self.assertIn("the budget is 250", found["W-AUT-005"])

        self.write_requirement(body=reader_first_body(why=" ".join(["Short sentence here."] * 6)))
        found = self.advisories()
        self.assertEqual({"W-AUT-006"}, set(found))
        self.assertIn("6 sentences", found["W-AUT-006"])

        self.write_requirement(body=reader_first_body(why="This one sentence " + " ".join(["keeps"] * 24) + " going."))
        self.assertEqual({"W-AUT-007"}, set(self.advisories()))

        self.write_requirement(body=reader_first_body(why="It cites `a`, `b`, `c` and `d` in one breath."))
        found = self.advisories()
        self.assertEqual({"W-AUT-008"}, set(found))
        self.assertIn("4 code identifiers", found["W-AUT-008"])

        self.write_requirement(body=reader_first_body(plain="One. Two. Three."))
        found = self.advisories()
        self.assertEqual({"W-AUT-009"}, set(found))
        self.assertIn("3 sentences", found["W-AUT-009"])

        self.write_requirement(body="\n## Why\n\n" + WHY + "\n\n## Behavior\n\n" + BEHAVIOR + "\n")
        found = self.advisories()
        self.assertEqual({"W-AUT-009"}, set(found))
        self.assertIn("no In plain words section", found["W-AUT-009"])

        self.write_requirement(statement="WHEN a requirement is validated, THE SYSTEM SHALL count its words.")
        self.assertEqual({"W-AUT-010"}, set(self.advisories()))

    def test_no_shape_advisory_fires_on_an_approved_requirement(self) -> None:
        long_statement = "WHEN " + " ".join(f"word{i}" for i in range(30)) + ", THE SYSTEM SHALL respond."
        self.write_requirement(status="approved", statement=long_statement, body="\n## Why\n\n" + " ".join(["word"] * 300) + ".\n")
        self.assertEqual({}, self.advisories())

    def test_a_named_component_is_an_accepted_opener(self) -> None:
        for statement in ("THE VALIDATOR SHALL count the words of a draft statement.", "WHEN a draft is validated by hand, THE INSTALLER SHALL write nothing."):
            with self.subTest(statement=statement):
                self.write_requirement(statement=statement)
                self.assertNotIn("W-AUT-001", self.advisories())

    def test_validation_still_passes_with_advisories(self) -> None:
        self.write_requirement(statement="WHEN " + " ".join(f"w{i}" for i in range(40)) + ", THE SYSTEM SHALL respond.")
        code, _, _ = self.invoke("validate", str(self.root), "--advisories")
        self.assertEqual(0, code)
        report = _load_validator_module().validate_repository(self.root)
        self.assertEqual([], [f"{i.code}: {i.message}" for i in report.errors])
        self.assertIn("W-AUT-003", {item.code for item in report.advisories if item.path.endswith("REQ-002.md")})
        self.assertEqual([], [item.code for item in report.warnings if item.code.startswith("W-AUT-")])

    # ---------------------------------------------------------------- REQ-TCM-006: Explorer

    def test_the_explorer_projects_plain_words_beneath_the_statement(self) -> None:
        self.write_requirement()
        code, output, error = self.invoke("dashboard", str(self.root))
        self.assertEqual(0, code, error + output)
        detail = next(
            json.loads(p.read_text(encoding="utf-8"))
            for p in (self.root / "target/harness-dashboard/data/artifacts").rglob("*")
            if p.is_file() and '"REQ-002"' in p.read_text(encoding="utf-8")
        )
        self.assertEqual(PLAIN, detail["artifact"]["plain_words"])
        self.write_requirement(body="\n## Why\n\n" + WHY + "\n")
        code, output, error = self.invoke("dashboard", str(self.root))
        self.assertEqual(0, code, error + output)
        detail = next(
            json.loads(p.read_text(encoding="utf-8"))
            for p in (self.root / "target/harness-dashboard/data/artifacts").rglob("*")
            if p.is_file() and '"REQ-002"' in p.read_text(encoding="utf-8")
        )
        self.assertNotIn("plain_words", detail["artifact"])
        template = (REPOSITORY_ROOT / "templates/repository/standard/scripts/harness_explorer/index.template.html").read_text(encoding="utf-8")
        self.assertIn("plainWords", template)
        self.assertLess(template.index("{{statementNodes}}"), template.index("{{plainWords}}"))

    # ---------------------------------------------------------------- REQ-TCM-008: the gate

    def approve(self) -> tuple[int, str]:
        code, output, error = self.invoke(
            "transition", str(self.root), "--set", "REQ-002=approved", "--decision", "REQ-002=owner", "--reason", "REQ-002=ready", "--apply",
        )
        return code, output + error

    def test_approval_needs_no_open_decisions_section_and_reads_the_graph(self) -> None:
        self.write_requirement()
        code, message = self.approve()
        self.assertEqual(0, code, message)
        self.assertIn('status = "approved"', self.path.read_text(encoding="utf-8"))

    def test_an_open_decision_blocks_approval_through_the_decision_predicate_only(self) -> None:
        self.write_requirement()
        write(
            self.root / "docs/engineering/product/decisions/DEC-001.md",
            formal(
                "DEC-001", "decision", "open", {"concerns": ["REQ-002"], "blocks": ["REQ-002"]},
                'kind = "question"\nquestion = "Is the manifest sorted?"\nraised_by = "coding-agent"\nrecommendation = "yes"\n\n'
                '[[options]]\nid = "yes"\nlabel = "Sort it."\n\n[[options]]\nid = "no"\nlabel = "Leave it."',
            ),
        )
        code, message = self.approve()
        self.assertEqual(1, code)
        self.assertIn("QGP-G1-DECISION", message)
        self.assertIn("DEC-001", message)
        self.assertIn("harnessctl decide", message)
        self.assertNotIn("Open decisions", message)
        self.assertIn('status = "draft"', self.path.read_text(encoding="utf-8"))

    def test_a_legacy_section_with_prose_is_still_refused(self) -> None:
        self.write_requirement(body=reader_first_body(extra="\n## Open decisions\n\nWhether the manifest is sorted.\n"))
        code, message = self.approve()
        self.assertEqual(1, code)
        self.assertIn("E-DCM-004", message)
        self.write_requirement(body=reader_first_body(extra="\n## Open decisions\n\nNone.\n"))
        code, message = self.approve()
        self.assertEqual(0, code, message)

    def test_spec_dcm_001_carries_the_rule_11_amendment(self) -> None:
        spec = (REPOSITORY_ROOT / "docs/engineering/decision-management/specifications/SPEC-DCM-001.md").read_text(encoding="utf-8")
        record = spec.split("## Amendment record", 1)[1]
        self.assertIn("WO-TCM-005", record)
        self.assertIn("legacy rule", record)
        self.assertIn("TCM-RFR-006", record)


if __name__ == "__main__":
    unittest.main()
