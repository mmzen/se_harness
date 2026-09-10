"""REQ-DST-076, REQ-DST-077 / SPEC-DST-028 (WO-DST-027): the retired relation in the
managed traceability policy, the completion decider in the managed work-order template,
and the UML note that follows them.

DST-TPL-007 pins DST-TPL-001 to DST-TPL-005 on the standard templates under
templates/repository/standard/. Parity with the released root is
test_artifact_catalog's (DST-TPL-006).
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tests.cli_support import invoke
from tests.mutation_guard_support import patch_mutation_authority

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
STANDARD = REPOSITORY_ROOT / "templates/repository/standard/docs/engineering"
TRACEABILITY = STANDARD / "TRACEABILITY.md"
WORK_ORDER = STANDARD / "templates/WORK_ORDER.template.md"
UML_NOTE = REPOSITORY_ROOT / "docs/notes/harness-uml-model.md"


def _paragraph(text: str, opening: str) -> str:
    """The paragraph that opens with ``opening``, joined into one line."""

    start = text.index(opening)
    end = text.find("\n\n", start)
    return " ".join(text[start : end if end != -1 else None].split())


def _section(text: str, heading: str) -> str:
    marker = f"## {heading}\n"
    start = text.index(marker) + len(marker)
    end = text.find("\n## ", start)
    return text[start : end if end != -1 else None]


class RetiredRelationRuleTests(unittest.TestCase):
    """DST-TPL-001 to DST-TPL-003 on the standard TRACEABILITY.md."""

    def setUp(self) -> None:
        self.text = TRACEABILITY.read_text(encoding="utf-8")
        self.rule = _paragraph(self.text, "`TRC-008`")

    def test_the_rule_names_the_relation_retired_and_refused(self) -> None:
        # DST-TPL-001.
        self.assertIn("`ARCH.constrains` is retired", self.rule)
        self.assertIn("A validator MUST refuse every `constrains` relation with `E016`", self.rule)
        self.assertIn("whatever the architecture's status", self.rule)

    def test_the_rule_names_the_typed_pair_and_promises_no_migration(self) -> None:
        # DST-TPL-002.
        self.assertIn("`ARCH.addresses` and `ARCH.conforms_to` are the only form", self.rule)
        for stale in ("compatibility-only", "MAY classify", "report the migration"):
            with self.subTest(phrase=stale):
                self.assertNotIn(stale, self.text)

    def test_the_rule_keeps_its_installation_sentence_and_its_neighbours(self) -> None:
        # DST-TPL-003: the last sentence stays; the neighbouring rules are each defined once.
        self.assertTrue(
            self.rule.endswith("Installation and upgrade MUST NOT rewrite repository-owned artifacts."),
            self.rule,
        )
        for identifier in ("`TRC-007`", "`TRC-008`", "`TRC-009`"):
            with self.subTest(rule=identifier):
                self.assertEqual(1, self.text.count(f"\n{identifier} - "))


class CompletionDeciderGuidanceTests(unittest.TestCase):
    """DST-TPL-004 on the standard WORK_ORDER.template.md."""

    def setUp(self) -> None:
        self.text = WORK_ORDER.read_text(encoding="utf-8")
        self.section = " ".join(_section(self.text, "Completion report format").split())

    def test_the_heading_carries_guidance_naming_both_deciders(self) -> None:
        self.assertTrue(self.section, "the Completion report format heading has nothing under it")
        self.assertIn("engineering owner", self.section)
        self.assertIn("`delegated-executor`", self.section)
        self.assertIn('`[delegation] class = "execution"`', self.section)
        self.assertIn("`success`", self.section)

    def test_the_guidance_gives_completion_to_no_single_decider(self) -> None:
        self.assertNotIn("the completion decision is the engineering owner's", self.text)


class UmlNoteTests(unittest.TestCase):
    """DST-TPL-005 on docs/notes/harness-uml-model.md."""

    def test_the_note_says_the_relation_is_retired_and_refused(self) -> None:
        text = UML_NOTE.read_text(encoding="utf-8")
        sentence = _paragraph(text, "The compatibility-era `constrains` relation")
        self.assertIn("is retired", sentence)
        self.assertIn("refuses", sentence)
        self.assertIn("`E016`", sentence)
        self.assertNotIn("may still carry", text)


class DraftedWorkOrderTests(unittest.TestCase):
    """VER-DST-028 scenario B: a work order drafted from the candidate template carries the
    completion guidance and no sentence giving the decision to the engineering owner."""

    def test_a_drafted_work_order_carries_the_guidance_and_no_copied_sentence(self) -> None:
        patch_mutation_authority(self)
        with tempfile.TemporaryDirectory() as scratch:
            target = Path(scratch) / "target"
            code, _, error = invoke("init", str(target), "--project-name", "Scenario B")
            self.assertEqual(0, code, error)
            code, _, error = invoke("scaffold-domain", str(target), "--domain", "scratch-domain")
            self.assertEqual(0, code, error)
            code, _, error = invoke(
                "create-artifact", str(target), "--domain", "scratch-domain",
                "--type", "work_order", "--id", "WO-SCR-001", "--quiet",
            )
            self.assertEqual(0, code, error)
            drafted = next((target / "docs/engineering/scratch-domain").rglob("WO-SCR-001.md"))
            text = drafted.read_text(encoding="utf-8")
        section = " ".join(_section(text, "Completion report format").split())
        self.assertIn("engineering owner", section)
        self.assertIn("`delegated-executor`", section)
        self.assertNotIn("the completion decision is the engineering owner's", text)


if __name__ == "__main__":
    unittest.main()
