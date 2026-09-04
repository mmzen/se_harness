"""Evidence for REQ-TCM-009, REQ-TCM-010 and REQ-TCM-011 (WO-TCM-007): the reader-first intent shape."""

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
CORPUS = REPOSITORY_ROOT / "docs/engineering"

OUTCOME = "A reviewer can tell from a work order's status alone whether it was authorized, finished, verified or released."
PLAIN = "A status should mean one thing. Today a reviewer has to open the records to learn what was done."
PROBLEM = "Finished work is still marked approved. Decisions are marked verified without a record. A reviewer cannot trust the status."
MEASURES = (
    "| Measure | Today | When reached | Observed |\n| --- | --- | --- | --- |\n"
    "| Work orders whose status is not backed by a record | 11 | 0 | Explorer overview, at each release review |\n"
    "| Reviewer questions about a status | not measured | 0 per release | pull-request threads, counted per release |"
)
NOT_THIS = "- Deciding whether any record is verified or released."


def reader_first_body(*, plain: str = PLAIN, problem: str = PROBLEM, measures: str | None = MEASURES, extra: str = "") -> str:
    parts = [f"\n## In plain words\n\n{plain}\n\n## Problem\n\n{problem}\n"]
    if measures is not None:
        parts.append(f"\n## Success measures\n\n{measures}\n")
    parts.append(f"\n## Not this\n\n{NOT_THIS}\n{extra}")
    return "".join(parts)


class ReaderFirstIntentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        code, _, error = self.invoke("init", str(self.root), "--project-name", "Intent Fixture")
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
        self.path = self.root / "docs/engineering/product/intent/INT-002.md"

    def invoke(self, *arguments: str) -> tuple[int, str, str]:
        output = io.StringIO()
        error = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            code = main(list(arguments))
        return code, output.getvalue(), error.getvalue()

    def write_intent(self, *, status: str = "draft", outcome: str | None = OUTCOME, body: str | None = None, extra_front_matter: str = "") -> None:
        front = "" if outcome is None else f'outcome = "{outcome}"'
        text = formal("INT-002", "intent", status, {}, front + ("\n" + extra_front_matter if extra_front_matter else ""))
        write(self.path, text + (reader_first_body() if body is None else body))

    def report(self):
        return _load_validator_module().validate_repository(self.root)

    def advisories(self) -> dict[str, list[str]]:
        report = self.report()
        self.assertEqual([], [f"{i.code}: {i.message}" for i in report.errors if i.path.endswith("INT-002.md")])
        found: dict[str, list[str]] = {}
        for item in report.advisories:
            if item.path.endswith("INT-002.md"):
                found.setdefault(item.code, []).append(item.message)
        return found

    # ---------------------------------------------------------------- REQ-TCM-009: template and field

    def test_the_intent_template_is_reader_first_with_an_outcome_field(self) -> None:
        text = (TEMPLATES / "INTENT.template.md").read_text(encoding="utf-8")
        self.assertEqual(["## In plain words", "## Problem", "## Success measures", "## Not this"], re.findall(r"^## .*$", text, flags=re.MULTILINE))
        self.assertIsNotNone(re.search(r'^outcome = "', text, flags=re.MULTILINE))
        self.assertIn("| Measure | Today | When reached | Observed |", text)
        self.assertIn("`GLOSSARY.md` at the repository", text)
        for retired in ("Desired outcomes", "Actors and stakeholders", "Principles and immutable constraints", "Risks and assumptions", "Non-goals", "Open decisions"):
            self.assertNotIn(f"## {retired}", text)
        code, output, error = self.invoke("create-artifact", str(self.root), "--domain", "product", "--type", "intent", "--id", "INT-003", "--quiet")
        self.assertEqual(0, code, error + output)
        created = (self.root / "docs/engineering/product/intent/INT-003.md").read_text(encoding="utf-8")
        self.assertIn("## Success measures", created)
        self.assertIn('outcome = "', created)

    def test_the_outcome_field_is_accepted_optional_and_refused_when_empty(self) -> None:
        self.write_intent(status="approved")
        self.assertEqual([], [f"{i.code}: {i.message}" for i in self.report().errors])
        self.write_intent(status="approved", outcome=None, body="\n## Problem\n\nA legacy intent.\n")
        self.assertEqual([], [f"{i.code}: {i.message}" for i in self.report().errors])
        self.write_intent(status="approved", outcome="")
        errors = [f"{i.code}: {i.message}" for i in self.report().errors if i.path.endswith("INT-002.md")]
        self.assertEqual(1, len(errors), errors)
        self.assertIn("E-AUT-002: outcome must be a non-empty string", errors[0])

    # ---------------------------------------------------------------- REQ-TCM-009: advisories

    def test_a_reader_first_draft_within_every_budget_raises_no_advisory(self) -> None:
        self.write_intent()
        self.assertEqual({}, self.advisories())

    def test_each_budget_raises_exactly_its_advisory_with_the_measured_value(self) -> None:
        self.write_intent(outcome=None)
        found = self.advisories()
        self.assertEqual({"W-AUT-011"}, set(found))
        self.assertIn("no outcome", found["W-AUT-011"][0])

        self.write_intent(outcome=" ".join(f"word{i}" for i in range(31)) + ".")
        found = self.advisories()
        self.assertEqual({"W-AUT-011"}, set(found))
        self.assertIn("31 words; the budget is 30", found["W-AUT-011"][0])

        self.write_intent(outcome="An operator can run `harnessctl check` without reading the code.")
        found = self.advisories()
        self.assertEqual({"W-AUT-011"}, set(found))
        self.assertIn("names no solution", found["W-AUT-011"][0])

        self.write_intent(body=reader_first_body(extra="\n## More\n\n" + " ".join(["word"] * 210) + ".\n"))
        found = self.advisories()
        self.assertEqual({"W-AUT-005", "W-AUT-007"}, set(found))
        self.assertIn("the budget is 200", found["W-AUT-005"][0])

        self.write_intent(body=reader_first_body(problem=" ".join(["Short sentence here."] * 6)))
        found = self.advisories()
        self.assertEqual({"W-AUT-012"}, set(found))
        self.assertIn("6 sentences", found["W-AUT-012"][0])

        self.write_intent(body=reader_first_body(problem="This one sentence " + " ".join(["keeps"] * 24) + " going."))
        self.assertEqual({"W-AUT-007"}, set(self.advisories()))

        self.write_intent(body=reader_first_body(problem="It cites `a`, `b` and `c` in one breath."))
        found = self.advisories()
        self.assertEqual({"W-AUT-008"}, set(found))
        self.assertIn("3 code identifiers; the budget is 2", found["W-AUT-008"][0])

        self.write_intent(body=reader_first_body(problem="The review found it at `se_harness/workflow.py:606` and `scripts/check.py`."))
        found = self.advisories()
        self.assertEqual({"W-AUT-015"}, set(found))
        self.assertIn("2 repository paths or source line ranges", found["W-AUT-015"][0])

        self.write_intent(body=reader_first_body(plain="One. Two. Three."))
        found = self.advisories()
        self.assertEqual({"W-AUT-009"}, set(found))
        self.assertIn("3 sentences", found["W-AUT-009"][0])

        self.write_intent(body="\n## Problem\n\n" + PROBLEM + "\n\n## Success measures\n\n" + MEASURES + "\n")
        found = self.advisories()
        self.assertEqual({"W-AUT-009"}, set(found))
        self.assertIn("no In plain words section", found["W-AUT-009"][0])

    def test_no_shape_advisory_fires_on_an_approved_intent_or_on_a_requirement(self) -> None:
        self.write_intent(status="approved", outcome=None, body="\n## Problem\n\n" + " ".join(["word"] * 300) + ".\n")
        self.assertEqual({}, self.advisories())
        requirement = self.root / "docs/engineering/product/requirements/REQ-002.md"
        for relative, relation in (("specifications/SPEC-001.md", "specifies"), ("verification/VER-001.md", "verifies")):
            covering = self.root / "docs/engineering/product" / relative
            covering.write_text(
                covering.read_text(encoding="utf-8").replace(f'{relation} = ["REQ-001"]', f'{relation} = ["REQ-001", "REQ-002"]'),
                encoding="utf-8",
            )
        # a requirement draft over the intent constants (two identifiers, 200 words) but within its own
        body = (
            "\n## In plain words\n\nThe command lists what to read.\n\n## Why\n\nIt cites `a`, `b` and `c`. "
            + " ".join(["word"] * 40) + ".\n\n## Behavior\n\n| Trigger | Response | On failure |\n| --- | --- | --- |\n| a | b | c |\n\n## Examples\n\n"
            + " ".join(["word"] * 180) + ".\n"
        )
        write(
            requirement,
            formal("REQ-002", "requirement", "draft", {"derives_from": ["CAP-001"]},
                   'statement = "WHEN a work order is selected, THE SYSTEM SHALL list its reading manifest."\nverification_method = ["test"]\npriority = "must"\nsource = "CAP-001"')
            + body,
        )
        self.write_intent()
        report = self.report()
        requirement_codes = {item.code for item in report.advisories if item.path.endswith("REQ-002.md")}
        self.assertEqual(set(), requirement_codes & {"W-AUT-011", "W-AUT-012", "W-AUT-013", "W-AUT-014", "W-AUT-015"})
        self.assertNotIn("W-AUT-005", requirement_codes)
        self.assertNotIn("W-AUT-008", requirement_codes)

    def test_the_corpus_of_approved_intents_raises_nothing(self) -> None:
        report = _load_validator_module().validate_repository(REPOSITORY_ROOT)
        intents = sorted(CORPUS.glob("*/intent/INT-*.md"))
        self.assertGreaterEqual(len(intents), 33)
        self.assertEqual([], [f"{i.path}: {i.code}" for i in report.advisories if "/intent/" in i.path.replace("\\", "/")])
        self.assertEqual([], [f"{i.path}: {i.code}" for i in report.errors if "/intent/" in i.path.replace("\\", "/")])

    def test_validation_still_passes_with_advisories(self) -> None:
        self.write_intent(outcome=None)
        code, _, _ = self.invoke("validate", str(self.root), "--advisories")
        self.assertEqual(0, code)
        report = self.report()
        self.assertEqual([], [f"{i.code}: {i.message}" for i in report.errors])
        self.assertIn("W-AUT-011", {item.code for item in report.advisories if item.path.endswith("INT-002.md")})
        self.assertEqual([], [item.code for item in report.warnings if item.code.startswith("W-AUT-")])

    def test_the_authoring_checklist_names_the_shape_and_when_a_new_intent_is_warranted(self) -> None:
        guide = (REPOSITORY_ROOT / "templates/repository/standard/docs/engineering/ARTIFACT_AUTHORING.md").read_text(encoding="utf-8")
        section = guide.split("## intent", 1)[1].split("## capability", 1)[0]
        for code in ("W-AUT-011", "W-AUT-012", "W-AUT-013", "W-AUT-014", "W-AUT-015", "W-AUT-005", "W-AUT-007", "W-AUT-008", "W-AUT-009"):
            self.assertIn(code, section)
        self.assertIn("`In plain words`, `Problem`, `Success measures`, `Not this`", section)
        self.assertIn("years later, whether the outcome was reached", section)
        self.assertIn("A new intent is warranted", section)
        self.assertIn("capability under the existing", section)

    # ---------------------------------------------------------------- REQ-TCM-010: success measures

    def test_an_acceptance_check_in_the_table_is_reported_once_per_row(self) -> None:
        measures = (
            "| Measure | Today | When reached | Observed |\n| --- | --- | --- | --- |\n"
            "| Refusals per quarter | not measured | 0 | Explorer overview, quarterly |\n"
            "| Validator blocks violations | 0 | 0 | every CI run |\n"
            "| Files rewritten | 0 | 0 | implementation review |\n"
            "| Cases passing | partial | 100% | every regression run |\n"
            "| Records broken | 0 | 0 | packet verification |\n"
        )
        self.write_intent(body=reader_first_body(measures=measures))
        found = self.advisories()
        self.assertEqual({"W-AUT-013"}, set(found))
        self.assertEqual(4, len(found["W-AUT-013"]))
        messages = " || ".join(found["W-AUT-013"])
        for expected in (
            "'Validator blocks violations' is observed by CI",
            "'Files rewritten' is observed by implementation review",
            "'Cases passing' is observed by regression run",
            "'Records broken' is observed by verification",
        ):
            self.assertIn(expected, messages)
        self.assertNotIn("Refusals per quarter", messages)
        self.assertIn("belongs in the verification contract", found["W-AUT-013"][0])

    def test_an_empty_or_malformed_table_is_one_advisory(self) -> None:
        self.write_intent(body=reader_first_body(measures="| Measure | Today | When reached | Observed |\n| --- | --- | --- | --- |"))
        found = self.advisories()
        self.assertEqual({"W-AUT-014"}, set(found))
        self.assertEqual(1, len(found["W-AUT-014"]))
        self.write_intent(body=reader_first_body(measures="| Measure | Today |\n| --- | --- |\n| broken | row |"))
        found = self.advisories()
        self.assertEqual({"W-AUT-014"}, set(found))

    def test_an_honest_baseline_and_a_zero_target_raise_nothing(self) -> None:
        self.write_intent()
        self.assertEqual({}, self.advisories())

    # ---------------------------------------------------------------- REQ-TCM-011: Explorer

    def detail(self, artifact_id: str) -> dict:
        return next(
            json.loads(p.read_text(encoding="utf-8"))
            for p in (self.root / "target/harness-dashboard/data/artifacts").rglob("*")
            if p.is_file() and f'"{artifact_id}"' in p.read_text(encoding="utf-8")
        )

    def readiness_g0(self) -> dict:
        bundle_dir = self.root / "target/harness-dashboard/data"
        for p in bundle_dir.rglob("*"):
            if p.is_file() and "intent_quality" in p.read_text(encoding="utf-8"):
                data = json.loads(p.read_text(encoding="utf-8"))
                readiness = data.get("readiness") or data.get("bundle", {}).get("readiness") or []
                for entry in readiness:
                    if entry.get("work_order") == "WO-001" or entry.get("id") == "WO-001":
                        gates = entry.get("gates", [])
                        return next(g for g in gates if g.get("gate") == "G0")
                for entry in readiness:
                    gates = entry.get("gates", [])
                    g0 = next((g for g in gates if g.get("gate") == "G0"), None)
                    if g0:
                        return g0
        raise AssertionError("no G0 gate in the bundle")

    def test_the_explorer_projects_the_outcome_and_plain_words_of_an_intent(self) -> None:
        self.write_intent(status="approved")
        code, output, error = self.invoke("dashboard", str(self.root))
        self.assertEqual(0, code, error + output)
        detail = self.detail("INT-002")["artifact"]
        self.assertEqual(OUTCOME, detail["outcome"])
        self.assertEqual(PLAIN, detail["plain_words"])
        self.assertEqual(2, detail["success_measure_rows"])
        legacy = self.detail("INT-001")["artifact"]
        self.assertNotIn("outcome", legacy)
        self.assertNotIn("plain_words", legacy)
        requirement = self.detail("REQ-001")["artifact"]
        self.assertNotIn("outcome", requirement)
        template = (REPOSITORY_ROOT / "templates/repository/standard/scripts/harness_explorer/index.template.html").read_text(encoding="utf-8")
        self.assertIn("{{outcome}}", template)
        self.assertIn("{{c.outcome}}", template)
        # the record panel: outcome, then plain words, both before the decision trail
        self.assertLess(template.index("{{outcome}}"), template.rindex("{{plainWords}}"))
        self.assertLess(template.rindex("{{plainWords}}"), template.index("Decision trail"))
        # the requirement ordering of WO-TCM-005 is untouched
        self.assertLess(template.index("{{statementNodes}}"), template.index("{{plainWords}}"))

    def test_the_g0_intent_quality_condition_is_derived_from_outcome_and_a_measure_row(self) -> None:
        # the base chain's WO-001 reaches INT-001 only; make INT-001 the measured intent
        intent = self.root / "docs/engineering/product/intent/INT-001.md"
        write(intent, formal("INT-001", "intent", "approved", {}, f'outcome = "{OUTCOME}"') + reader_first_body())
        code, output, error = self.invoke("dashboard", str(self.root))
        self.assertEqual(0, code, error + output)
        g0 = self.readiness_g0()
        quality = next(c for c in g0["conditions"] if c["id"] == "intent_quality")
        self.assertEqual("satisfied", quality["state"])
        self.assertIn("INT-001", quality["evidence"])
        # outcome without a measure row
        write(intent, formal("INT-001", "intent", "approved", {}, f'outcome = "{OUTCOME}"') + reader_first_body(measures=None))
        code, output, error = self.invoke("dashboard", str(self.root))
        self.assertEqual(0, code, error + output)
        quality = next(c for c in self.readiness_g0()["conditions"] if c["id"] == "intent_quality")
        self.assertEqual("not_assessable", quality["state"])
        # a legacy intent
        write(intent, formal("INT-001", "intent", "approved", {}))
        code, output, error = self.invoke("dashboard", str(self.root))
        self.assertEqual(0, code, error + output)
        g0 = self.readiness_g0()
        quality = next(c for c in g0["conditions"] if c["id"] == "intent_quality")
        self.assertEqual("not_assessable", quality["state"])
        chain = next(c for c in g0["conditions"] if c["id"] == "intent_chain")
        self.assertEqual("satisfied", chain["state"])


if __name__ == "__main__":
    unittest.main()
