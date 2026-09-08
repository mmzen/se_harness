"""Evidence for REQ-TCM-014, REQ-TCM-015 and REQ-TCM-016 (WO-TCM-009): the reader-first specification shape."""

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
from tests.mutation_guard_support import trusted_mutation_authority
from tests.test_revision_provenance import create_base_chain, formal, write

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = REPOSITORY_ROOT / "templates/repository/standard/docs/engineering/templates"
GUIDE = REPOSITORY_ROOT / "templates/repository/standard/docs/engineering/ARTIFACT_AUTHORING.md"
EXPLORER_TEMPLATE = REPOSITORY_ROOT / "se_harness/engine/harness_explorer/index.template.html"

CONTRACT = "A conforming succession qualifies the exact evaluator pair under the managed check and refuses every other pair."
PLAIN = "Moving from one released version to the next is checked the same way every time."
SCOPE = "The succession check of the managed lane. The workflow shape is `SPEC-001`'s."
RULES = (
    "**FIX-SUC-001.** The lane MUST read the target evaluator identity from the lock and from nowhere else.\n"
    "\n"
    "**FIX-SUC-002.** The lane MUST NOT install an evaluator whose archive digest differs from the lock's.\n"
    "\n"
    "**FIX-SUC-003.** The lane refuses a succession whose base lock is not the committed lock of `main`.\n"
)
FAILURE = "| Trigger | Response | Diagnostic |\n| --- | --- | --- |\n| the digests differ | the lane stops before install | `SUC001` |\n"
EXAMPLES = "**Given** a lock naming 0.15.0, **when** the lane runs, **then** it installs 0.15.0 (FIX-SUC-001).\n"
COVERAGE = "| Requirement | Rules |\n| --- | --- |\n| `REQ-001` | FIX-SUC-001, FIX-SUC-002 |\n| `REQ-002` | FIX-SUC-003 |\n"
NOT_DECIDED = "- The runner image is the workflow's choice.\n"


def reader_first_body(*, plain: str = PLAIN, scope: str = SCOPE, rules: str = RULES, coverage: str | None = COVERAGE, extra: str = "",
                      rules_heading: str = "Rules") -> str:
    body = (
        f"\n## In plain words\n\n{plain}\n\n## Scope\n\n{scope}\n\n## Terms\n\n- **Pair.** The base and target evaluator identities.\n\n"
        f"## {rules_heading}\n\n{rules}\n## Failure behaviour\n\n{FAILURE}\n## Examples\n\n{EXAMPLES}\n"
    )
    if coverage is not None:
        body += f"## Coverage\n\n{coverage}\n"
    body += f"## Not decided here\n\n{NOT_DECIDED}{extra}"
    return body


class ReaderFirstSpecificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        code, _, error = self.invoke("init", str(self.root), "--project-name", "Specification Fixture")
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
        self.path = self.root / "docs/engineering/product/specifications/SPEC-002.md"
        write(
            self.root / "docs/engineering/product/requirements/REQ-002.md",
            formal("REQ-002", "requirement", "draft", {"derives_from": ["CAP-001"]},
                   'statement = "WHEN a succession is requested, THE SYSTEM SHALL qualify it."\nverification_method = ["test"]'),
        )

    def invoke(self, *arguments: str) -> tuple[int, str, str]:
        output = io.StringIO()
        error = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            code = main(list(arguments))
        return code, output.getvalue(), error.getvalue()

    def write_specification(self, *, status: str = "draft", contract: str | None = CONTRACT, body: str | None = None,
                            specifies: tuple[str, ...] = ("REQ-001", "REQ-002")) -> None:
        front = "" if contract is None else f'contract = "{contract}"'
        write(self.path, formal("SPEC-002", "specification", status, {"specifies": list(specifies)}, front) + (reader_first_body() if body is None else body))

    def report(self):
        return validate_engineering_artifacts.validate_repository(self.root)

    def errors(self, path_suffix: str = "SPEC-002.md") -> list[str]:
        return [f"{i.code}: {i.message}" for i in self.report().errors if i.path.endswith(path_suffix)]

    def advisories(self, path_suffix: str = "SPEC-002.md") -> dict[str, list[str]]:
        report = self.report()
        self.assertEqual([], [f"{i.code}: {i.message}" for i in report.errors if i.path.endswith(path_suffix)])
        found: dict[str, list[str]] = {}
        for item in report.advisories:
            if item.path.endswith(path_suffix):
                found.setdefault(item.code, []).append(item.message)
        return found

    # ---------------------------------------------------------------- REQ-TCM-014: template, field, checklist

    def test_the_specification_template_is_reader_first_with_a_contract_field(self) -> None:
        text = (TEMPLATES / "SPECIFICATION.template.md").read_text(encoding="utf-8")
        self.assertEqual(
            ["## In plain words", "## Scope", "## Terms", "## Rules", "## Failure behaviour", "## Examples", "## Coverage", "## Not decided here"],
            re.findall(r"^## .*$", text, flags=re.MULTILINE),
        )
        self.assertIsNotNone(re.search(r'^contract = "', text, flags=re.MULTILINE))
        self.assertIn("`GLOSSARY.md` at the repository", text)
        for retired in ("Actors and external systems", "Inputs", "Outputs", "State model", "Behavioral rules", "Data and interface contracts",
                        "Security and privacy properties", "Performance and capacity", "Observability", "Compatibility and migration",
                        "Explicitly unspecified decisions", "Open decisions"):
            self.assertNotIn(f"## {retired}", text)
        self.assertNotIn("Number rules", text)
        code, output, error = self.invoke("create-artifact", str(self.root), "--domain", "product", "--type", "specification", "--id", "SPEC-003", "--quiet")
        self.assertEqual(0, code, error + output)
        created = (self.root / "docs/engineering/product/specifications/SPEC-003.md").read_text(encoding="utf-8")
        self.assertIn("## Coverage", created)
        self.assertIn('contract = "', created)

    def test_the_contract_field_is_accepted_optional_and_refused_when_empty(self) -> None:
        self.write_specification(status="approved")
        self.assertEqual([], self.errors())
        self.write_specification(status="approved", contract=None, body="\n## Behavioral rules\n\n1. The lane reads the lock.\n")
        self.assertEqual([], self.errors())
        self.write_specification(status="approved", contract="")
        errors = self.errors()
        self.assertEqual(1, len(errors), errors)
        self.assertIn("E-AUT-002", errors[0])
        self.assertIn("contract", errors[0])

    def test_the_checklist_matches_the_shape(self) -> None:
        section = GUIDE.read_text(encoding="utf-8").split("\n## specification", 1)[1].split("\n## architecture", 1)[0]
        for token in ("`contract`", "W-AUT-019", "W-AUT-020", "W-AUT-021", "W-AUT-022", "W-AUT-023", "W-AUT-005", "W-AUT-007", "W-AUT-009",
                      "E-DCM-005", "no W-AUT-008", "`In plain words`", "`Scope`", "`Terms`", "`Rules`", "`Failure behaviour`", "`Examples`",
                      "`Coverage`", "`Not decided here`", "<PREFIX>-<AREA>-NNN", "MUST, MUST NOT, SHALL, SHALL NOT, MAY or refuses",
                      "never moves", "former number"):
            self.assertIn(token, section, token)
        self.assertNotIn("Number rules", section)
        self.assertNotIn("Rules are numbered", section)
        # TCM-RFS-003: the nine optional sections, each with a sentence on when it earns its place
        for optional in ("`Actors and external systems`", "`Inputs`", "`Outputs`", "`State model`", "`Data and interface contracts`",
                         "`Security and privacy properties`", "`Performance and capacity`", "`Observability`", "`Compatibility and migration`"):
            self.assertIn(optional, section, optional)
        self.assertIn("earn", section)

    # ---------------------------------------------------------------- REQ-TCM-014: advisories

    def test_a_reader_first_draft_within_every_budget_raises_no_advisory(self) -> None:
        self.write_specification()
        self.assertEqual({}, self.advisories())

    def test_the_contract_advisory_fires_for_each_departure(self) -> None:
        self.write_specification(contract=None)
        found = self.advisories()
        self.assertEqual({"W-AUT-019"}, set(found))
        self.assertIn("no contract", found["W-AUT-019"][0])

        self.write_specification(contract="A conforming lane " + " ".join(["really"] * 30) + " qualifies.")
        found = self.advisories()
        self.assertEqual(["W-AUT-019"], list(found))
        self.assertIn("34 words; the budget is 30", found["W-AUT-019"][0])

        self.write_specification(contract="A lane qualifies the pair. It refuses the rest.")
        found = self.advisories()
        self.assertIn("2 sentences; the budget is one", found["W-AUT-019"][0])

        self.write_specification(contract="A lane runs `harnessctl upgrade` and refuses the rest.")
        found = self.advisories()
        self.assertIn("1 code identifiers", found["W-AUT-019"][0])

    def test_rule_identity_and_shape_fire_exactly_for_their_cases(self) -> None:
        # a paragraph without an identifier
        self.write_specification(body=reader_first_body(rules=RULES + "\nThe lane also logs the pair it qualified.\n"))
        found = self.advisories()
        self.assertEqual({"W-AUT-020"}, set(found))
        self.assertEqual(1, len(found["W-AUT-020"]))
        self.assertIn("no identifier", found["W-AUT-020"][0])
        # a duplicate identifier
        self.write_specification(body=reader_first_body(rules=RULES + "\n**FIX-SUC-002.** The lane MUST log the pair.\n"))
        found = self.advisories()
        self.assertEqual({"W-AUT-020"}, set(found))
        self.assertIn("FIX-SUC-002 is defined twice", found["W-AUT-020"][0])
        # a 40-word rule
        long_rule = "**FIX-SUC-004.** The lane MUST " + " ".join(["really"] * 36) + " stop.\n"
        self.write_specification(body=reader_first_body(rules=RULES + "\n" + long_rule))
        found = self.advisories()
        self.assertEqual({"W-AUT-021"}, set(found))
        self.assertIn("FIX-SUC-004 is 40 words; the budget is 30", found["W-AUT-021"][0])
        # a two-sentence rule
        self.write_specification(body=reader_first_body(rules=RULES + "\n**FIX-SUC-004.** The lane MUST stop. It MUST say why.\n"))
        found = self.advisories()
        self.assertEqual({"W-AUT-021"}, set(found))
        self.assertIn("2 sentences", found["W-AUT-021"][0])
        # a rule without a keyword
        self.write_specification(body=reader_first_body(rules=RULES + "\n**FIX-SUC-004.** The lane logs the pair it qualified.\n"))
        found = self.advisories()
        self.assertEqual({"W-AUT-021"}, set(found))
        self.assertIn("no MUST", found["W-AUT-021"][0])
        # an identifier with a parenthesised short name, as SPEC-TCM-005 writes them, is an identifier
        self.write_specification(body=reader_first_body(rules=RULES + "\n**FIX-SUC-004 (logging).** The lane MUST log the pair.\n"))
        self.assertEqual({}, self.advisories())

    def test_legacy_shape_and_budgets_fire_with_specification_constants(self) -> None:
        # a draft copy of SPEC-PYP-001: twelve numbered rules under Behavioral rules, no contract, no coverage
        corpus = (REPOSITORY_ROOT / "docs/engineering/pypi-publication/specifications/SPEC-PYP-001.md").read_text(encoding="utf-8")
        body = corpus.split("+++", 2)[2]
        self.write_specification(contract=None, body=body, specifies=("REQ-001",))
        found = self.advisories()
        self.assertEqual(12, len(found["W-AUT-020"]))
        self.assertEqual(1, len(found["W-AUT-023"]))
        self.assertIn("Behavioral rules", found["W-AUT-023"][0])
        self.assertEqual(1, len(found["W-AUT-022"]))
        self.assertIn("no Coverage table", found["W-AUT-022"][0])
        self.assertIn("W-AUT-019", found)
        self.assertNotIn("W-AUT-008", found)
        # 400 words of prose outside the rules
        self.write_specification(body=reader_first_body(extra="\n## Observability\n\n" + " ".join(["word"] * 400) + ".\n"))
        found = self.advisories()
        self.assertEqual({"W-AUT-005", "W-AUT-007"}, set(found))
        self.assertIn("the budget is 300", found["W-AUT-005"][0])
        # a 30-word sentence in Scope
        self.write_specification(body=reader_first_body(scope="This one sentence " + " ".join(["keeps"] * 27) + " going."))
        self.assertEqual({"W-AUT-007"}, set(self.advisories()))
        # a long sentence inside a rule is the rule's advisory, not W-AUT-007
        self.write_specification(body=reader_first_body(rules=RULES + "\n**FIX-SUC-004.** The lane MUST " + " ".join(["really"] * 30) + " stop.\n"))
        self.assertEqual({"W-AUT-021"}, set(self.advisories()))
        # no In plain words
        self.write_specification(body=reader_first_body().replace("## In plain words\n\n" + PLAIN + "\n\n", ""))
        found = self.advisories()
        self.assertEqual({"W-AUT-009"}, set(found))
        # forty code identifiers draw nothing: TCM-RFS-013
        self.write_specification(body=reader_first_body(extra="\n## Observability\n\n" + " ".join(f"`id{i}`" for i in range(40)) + ".\n"))
        self.assertEqual({}, self.advisories())

    def test_no_specification_advisory_fires_on_an_approved_specification_or_another_type(self) -> None:
        self.write_specification(status="approved", contract=None, body="\n## Behavioral rules\n\n1. The lane reads the lock.\n\n## Observability\n\n" + " ".join(["word"] * 400) + ".\n")
        self.assertEqual({}, self.advisories())
        # a requirement draft with 40 code identifiers keeps its own budget (three), not the specification's
        write(self.root / "docs/engineering/product/requirements/REQ-003.md",
              formal("REQ-003", "requirement", "draft", {"derives_from": ["CAP-001"]},
                     'statement = "WHEN a succession is requested, THE SYSTEM SHALL qualify it."\nverification_method = ["test"]')
              + "\n## In plain words\n\nShort.\n\n## Why\n\nIt cites " + " ".join(f"`id{i}`" for i in range(40)) + ".\n")
        found = self.advisories("REQ-003.md")
        self.assertIn("W-AUT-008", found)
        self.assertFalse({"W-AUT-019", "W-AUT-020", "W-AUT-021", "W-AUT-022", "W-AUT-023"} & set(found), found)

    def test_this_repository_corpus_raises_no_specification_advisory(self) -> None:
        report = validate_engineering_artifacts.validate_repository(REPOSITORY_ROOT)
        specification_paths = {str(p) for p in (REPOSITORY_ROOT / "docs/engineering").glob("*/specifications/SPEC-*.md")}
        found = [f"{i.path}: {i.code}" for i in report.advisories if any(i.path.replace("/", "\\") in path or i.path in path for path in specification_paths)]
        self.assertEqual([], found)
        self.assertEqual([], [f"{i.path}: {i.code}" for i in report.errors])

    # ---------------------------------------------------------------- REQ-TCM-015: coverage

    def test_the_coverage_table_is_checked_against_specifies_and_the_rules(self) -> None:
        self.write_specification(body=reader_first_body(coverage="| Requirement | Rules |\n| --- | --- |\n| `REQ-001` | FIX-SUC-001 |\n"))
        found = self.advisories()
        self.assertEqual({"W-AUT-022"}, set(found))
        self.assertEqual(1, len(found["W-AUT-022"]))
        self.assertIn("no row for REQ-002", found["W-AUT-022"][0])
        self.write_specification(body=reader_first_body(coverage=COVERAGE.replace("FIX-SUC-003", "FIX-SUC-009")))
        found = self.advisories()
        self.assertEqual({"W-AUT-022"}, set(found))
        self.assertIn("names FIX-SUC-009, which the rules section does not define", found["W-AUT-022"][0])
        self.write_specification(body=reader_first_body(coverage=None))
        found = self.advisories()
        self.assertEqual({"W-AUT-022"}, set(found))
        self.assertIn("no Coverage table", found["W-AUT-022"][0])
        self.write_specification()
        self.assertEqual({}, self.advisories())

    def bundle_detail(self, artifact_id: str) -> dict:
        code, output, error = self.invoke("dashboard", str(self.root))
        self.assertEqual(0, code, error + output)
        for p in (self.root / "target/harness-dashboard/data/artifacts").rglob("*"):
            if p.is_file():
                detail = json.loads(p.read_text(encoding="utf-8"))
                if detail.get("artifact", {}).get("id") == artifact_id:
                    return detail["artifact"]
        self.fail(f"no detail for {artifact_id}")

    def test_rules_coverage_and_covered_by_are_projected_from_the_same_table(self) -> None:
        self.write_specification(status="approved")
        artifact = self.bundle_detail("SPEC-002")
        self.assertEqual(CONTRACT, artifact["contract"])
        self.assertEqual(PLAIN, artifact["plain_words"])
        self.assertEqual(["FIX-SUC-001", "FIX-SUC-002", "FIX-SUC-003"], [rule["id"] for rule in artifact["rules"]])
        self.assertTrue(artifact["rules"][0]["text"].startswith("The lane MUST read the target evaluator identity"))
        self.assertEqual(
            [{"requirement": "REQ-001", "rules": ["FIX-SUC-001", "FIX-SUC-002"]}, {"requirement": "REQ-002", "rules": ["FIX-SUC-003"]}],
            artifact["coverage"],
        )
        requirement = self.bundle_detail("REQ-002")
        self.assertEqual([{"specification": "SPEC-002", "rule": "FIX-SUC-003"}], requirement["covered_by"])
        # a requirement covered by no rule projects an empty list; a legacy specification projects no contract and no rules
        self.write_specification(status="approved", contract=None, body="\n## Behavioral rules\n\n1. The lane reads the lock.\n")
        self.assertEqual([], self.bundle_detail("REQ-002")["covered_by"])
        legacy = self.bundle_detail("SPEC-002")
        self.assertNotIn("contract", legacy)
        self.assertEqual([], legacy["rules"])
        self.assertEqual([], legacy["coverage"])

    def test_the_explorer_places_the_contract_the_rules_and_the_coverage_before_the_events(self) -> None:
        template = EXPLORER_TEMPLATE.read_text(encoding="utf-8")
        contract = template.index("{{contract}}")
        rules = template.index("{{r.text}}")
        coverage = template.index("{{c.rules}}")
        events = template.index("{{events}}")
        self.assertLess(contract, rules)
        self.assertLess(rules, coverage)
        self.assertLess(coverage, events)
        self.assertIn("{{plainWords}}", template[contract:rules])
        self.assertIn('id=\\"{{r.id}}\\"', template)  # TCM-RFS-018: the rule anchor
        covered_by = template.index("{{cb.label}}")
        self.assertLess(covered_by, events)  # TCM-RFS-019
        self.assertIn("{{againstHref}}", template)  # TCM-RFS-022
        self.assertIn("covered_by", template)

    # ---------------------------------------------------------------- REQ-TCM-016: the deviation anchor

    def write_deviation(self, against: str) -> None:
        write(
            self.root / "docs/engineering/product/decisions/DEC-001.md",
            formal("DEC-001", "decision", "open", {"concerns": ["SPEC-002"], "blocks": ["SPEC-002"]},
                   'kind = "deviation"\nquestion = "Can the lane read the lock?"\nraised_by = "engineering-owner"\nrecommendation = "stop"\n'
                   f'against = "{against}"\nobserved = "The lock is unreadable on this runner."\n\n'
                   '[[options]]\nid = "accept"\nlabel = "Accept it."\n\n[[options]]\nid = "stop"\nlabel = "Stop."\n')
            + "\n## Question\n\nCan it?\n",
        )

    def test_a_deviation_names_a_rule_that_exists(self) -> None:
        self.write_specification(status="approved")
        self.write_deviation("SPEC-002#FIX-SUC-002")
        self.assertEqual([], self.errors("DEC-001.md"))
        self.write_deviation("SPEC-002#rule-7")
        errors = self.errors("DEC-001.md")
        self.assertEqual(1, len(errors), errors)
        self.assertIn("E-DCM-005", errors[0])
        self.assertIn("SPEC-002#rule-7", errors[0])
        self.write_deviation("SPEC-002#TCM-RFS-009")
        errors = self.errors("DEC-001.md")
        self.assertEqual(1, len(errors), errors)
        self.assertIn("E-DCM-005", errors[0])
        # a legacy numbered specification defines no identifier, so no fragment can name one
        self.write_specification(status="approved", contract=None, body="\n## Behavioral rules\n\n1. The lane reads the lock.\n")
        self.write_deviation("SPEC-002#rule-1")
        self.assertIn("E-DCM-005", self.errors("DEC-001.md")[0])

    def test_the_decision_specification_names_the_check(self) -> None:
        text = (REPOSITORY_ROOT / "docs/engineering/decision-management/specifications/SPEC-DCM-001.md").read_text(encoding="utf-8")
        rule = text.split("3. **Deviation fields.**", 1)[1].split("\n4. ", 1)[0]
        self.assertIn("SPEC-TCM-006#TCM-RFS-009", rule)
        self.assertIn("E-DCM-005", rule)
        self.assertIn("TCM-RFS-020", rule)
        self.assertNotIn("rule-7", rule)
        self.assertIn("WO-TCM-009", text.split("## Amendment record", 1)[1])


if __name__ == "__main__":
    unittest.main()
