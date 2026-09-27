"""Content conformance against the reviewed instruction contract, SPEC-IAR-014.

These checks cover the candidate prose split. They do not qualify installer
migration, evaluator discovery results or native host event delivery.
"""
from pathlib import Path
import hashlib
import json
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates/repository/standard"
COLLECTION = TEMPLATES / "docs/engineering/harness"
ACCEPTANCE = ROOT / "docs/engineering/instruction-architecture/acceptance/progressive-discovery"
SOURCE = ROOT / "docs/engineering/instruction-architecture/proposals/progressive-discovery/instruction-review-source.md"


def anchor(heading: str) -> str:
    return re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")


def document(path: str) -> Path:
    return TEMPLATES / (path + ".tpl" if path == "ENGINEERING_HARNESS.md" else path)


class ProgressiveInstructionContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entry = TEMPLATES / "ENGINEERING_HARNESS.md.tpl"
        cls.paths = [cls.entry, *sorted(COLLECTION.rglob("*.md"))]
        cls.texts = {p: p.read_text(encoding="utf-8") for p in cls.paths}
        cls.mapping = json.loads((ACCEPTANCE / "source-map.json").read_text(encoding="utf-8"))

    def test_review_source_is_the_accepted_input(self):
        self.assertEqual("9811b1770fa81e20f19890cb45de6d991aa463cf60a4338b39251d9d4c978a28",
                         hashlib.sha256(SOURCE.read_bytes()).hexdigest())

    def test_all_source_headings_and_main_steps_have_valid_destinations(self):
        expected = [(n, line) for n, line in enumerate(SOURCE.read_text(encoding="utf-8").splitlines(), 1)
                    if line.startswith("#")]
        self.assertEqual(58, len(expected))
        self.assertEqual(expected, [(row["line"], row["heading"]) for row in self.mapping["headings"]])
        for row in self.mapping["headings"]:
            self.assertTrue(row["allocations"], row)
            for allocation in row["allocations"]:
                self.assertTrue(document(allocation["destination"]).is_file(), allocation)
                self.assertIn(allocation["disposition"], {"moved", "retained", "corrected by recorded review", "deferred"})
        self.assertEqual(31, len(self.mapping["steps"]))
        self.assertEqual(31, len({row["destination"] for row in self.mapping["steps"]}))
        for row in self.mapping["steps"]:
            name, _, selected = row["destination"].partition("#")
            text = document(name).read_text(encoding="utf-8")
            headings = list(re.finditer(r"^#{1,3} (.+)$", text, re.M))
            match = next((m for m in headings if anchor(m[1]) == selected), None)
            self.assertIsNotNone(match, row)
            end = next((m.start() for m in headings if m.start() > match.start()), len(text))
            step = text[match.end():end]
            for label in ("Inputs", "Output", "Actions", "Harness command", "Completion", "Later use"):
                self.assertIn("**" + label, step, (row, label))
            self.assertLess(step.index("**Inputs"), step.index("**Output"))
            self.assertLess(step.index("**Output"), step.index("**Actions"))

    def test_every_markdown_file_and_heading_link_resolves_inside_the_template(self):
        for path, text in self.texts.items():
            for target in re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", text):
                if "://" in target:
                    continue
                name, _, selected = target.partition("#")
                destination = (path.parent / name).resolve() if name else path
                if destination.name == "ENGINEERING_HARNESS.md":
                    destination = destination.with_suffix(".md.tpl")
                with self.subTest(source=path.name, target=target):
                    self.assertTrue(destination.is_relative_to(TEMPLATES.resolve()))
                    self.assertTrue(destination.is_file())
                    if selected:
                        found = {anchor(m[1]) for m in re.finditer(r"^#{1,6} (.+)$", destination.read_text(encoding="utf-8"), re.M)}
                        self.assertIn(selected, found)

    def test_original_command_operands_are_preserved(self):
        original = set(re.findall(r"^harnessctl .+$", SOURCE.read_text(encoding="utf-8"), re.M))
        current = set(re.findall(r"^harnessctl .+$", "\n".join(self.texts.values()), re.M))
        self.assertTrue(original)
        self.assertEqual(set(), original - current)

    def test_entry_preserves_nine_invariants_and_conditional_reading(self):
        text = self.texts[self.entry]
        self.assertEqual([f"HRN-{n:03d}" for n in range(1, 10)], re.findall(r"^### (HRN-\d{3})", text, re.M))
        for phrase in ("BCP 14", "## Goals", "only source of truth", "before a work",
                       "granted", "temporary storage outside", "A link alone", "## After compaction"):
            self.assertIn(phrase, text)
        self.assertIn("no harness instructions", text)
        self.assertNotIn("OPERATING_CARD.md", text)
        self.assertNotIn("<!-- se-harness:begin -->", text)

    def test_actions_have_entry_and_continuation_conditions(self):
        names = ("CONTINUE", "DEFINE_CHANGE", "DRAFT_DEFINITIONS", "AMEND_DEFINITIONS",
                 "RISKS_AND_DECISIONS", "DRAFT_WORK_ORDERS", "AUTHORIZE_WORK", "EXECUTE_WORK",
                 "VERIFY_OUTCOME", "DELIVER_RESULT", "RELEASE", "PULL_REQUEST", "RECORD_STATE",
                 "RESULTS", "EXCEPTIONS", "SETUP", "UPGRADE", "SKILL_PROVIDER")
        for name in names:
            text = (COLLECTION / (name + ".md")).read_text(encoding="utf-8")
            for title in ("Read this when", "Before this action", "Procedure", "Read next when"):
                self.assertIn("## " + title, text, name)

    def test_no_review_markers_or_stale_lifecycle_links_ship(self):
        self.assertEqual(26, len(self.paths))
        for path, text in self.texts.items():
            self.assertNotRegex(text, r"XXX|voluntarily empty|\]\(#lifecycle-meaning\)|<!-- Implementation needed", path)

    def test_reserved_decisions_and_unsupported_capabilities_are_explicit(self):
        rights = (COLLECTION / "AUTHORITY.md").read_text(encoding="utf-8")
        self.assertIn("Approval, verification acceptance, and release decisions MUST be made by an", rights)
        self.assertIn("authorized human", rights)
        self.assertIn("recorded decision", rights)
        self.assertIn("preserve the accepted version", (COLLECTION / "AMEND_DEFINITIONS.md").read_text(encoding="utf-8"))
        exceptions = (COLLECTION / "EXCEPTIONS.md").read_text(encoding="utf-8")
        self.assertIn("No exception command is available", exceptions)
        self.assertIn("Lifecycle rules and required gates remain fixed", exceptions)

    def test_pr_preparation_does_not_require_release_preparation(self):
        text = (COLLECTION / "PULL_REQUEST.md").read_text(encoding="utf-8")
        self.assertNotIn("RELEASE.md", text)
        self.assertNotIn("harnessctl prepare-release", text)
        self.assertIn("No RLS is created", text)


if __name__ == "__main__":
    unittest.main()
