from __future__ import annotations

import re
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VALUE_PROPOSAL_PATH = REPOSITORY_ROOT / "VALUE_PROPOSAL.md"


class ValueProposalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = VALUE_PROPOSAL_PATH.read_text(encoding="utf-8")

    def test_document_is_an_executive_demo_brief(self) -> None:
        for phrase in (
            "**Target duration:** 10–15 minutes",
            "**Audience:** Executives, engineering leaders",
            "**Technical depth:** 4/10",
            "**Objective:**",
            "Suggested 12-minute flow",
            "Demo preparation checklist",
            "Q&A — likely executive pushback",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.document)

    def test_current_roadmap_and_vision_are_separated(self) -> None:
        for phrase in (
            "**Current — shipped**",
            "**Roadmap — approved or planned, not shipped**",
            "**Vision — intended outcome, not demonstrated**",
            "read-only, single-agent `harness-orient` skill with delegation disabled",
            "Delegated mutation",
            "multi-agent orchestration",
            "Organizational-scale governed delegation",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.document)

        self.assertNotIn("The architecture supports scale", self.document)
        self.assertNotIn("current multi-agent", self.document.lower())

    def test_enforcement_and_security_boundaries_are_explicit(self) -> None:
        for phrase in (
            "caller declaring the complete change set",
            "A process with write access can still modify files",
            "agent-runtime permissions",
            "not a coding agent, agent runtime, sandbox, permission system",
            "standalone security boundary",
            "privileged malicious process",
            "not physical prevention",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.document)

        self.assertNotIn("prevents an agent from modifying", self.document.lower())
        self.assertNotIn("The harness controls the engineering process", self.document)

    def test_demo_uses_the_real_lifecycle_and_authority_boundaries(self) -> None:
        ordered_phrases = (
            "transition from `approved` to `in_progress`",
            "engineering-owner completion decision",
            "implemented work",
            "clean candidate commit",
            "ready VREC",
            "assurance-owner decision",
            "verified VREC",
            "separately selected repository-integration or release path",
        )
        positions = [self.document.index(phrase) for phrase in ordered_phrases]
        self.assertEqual(sorted(positions), positions)
        self.assertIn("Preparing a VREC leaves it `ready`; it does not verify itself.", self.document)
        self.assertIn("changes only the VREC", self.document)
        self.assertIn("The referenced work order is not changed", self.document)

    def test_demo_uses_canonical_restitution_headings(self) -> None:
        sample = self.document.split("An abbreviated, structurally accurate example is:", 1)[1]
        sample = sample.split("```", 2)[1]
        headings = (
            "Outcome",
            "Done",
            "Not done",
            "Blocked by",
            "Current lifecycle state",
            "Decision required",
            "Next",
            "Command or response",
        )
        positions = [sample.index(heading) for heading in headings]
        self.assertEqual(sorted(positions), positions)
        self.assertNotRegex(self.document, r"(?m)^STATUS: BLOCKED$")

    def test_provenance_scale_assurance_and_compliance_claims_are_qualified(self) -> None:
        for phrase in (
            "exact source candidate",
            "Do not call it the “exact executable”",
            "Scale is unproven",
            "not a demonstrated result",
            "not independent assurance",
            "do not define applicable regulation, certify the organization",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.document)

        self.assertNotIn("The exact executable was verified", self.document)
        self.assertNotIn("certifies regulatory compliance", self.document.lower())

    def test_markdown_is_safe_and_complete(self) -> None:
        self.assertEqual(0, self.document.count("```") % 2)
        self.assertNotRegex(self.document, r"(?i)<(?:script|style|iframe)\b")
        for marker in ("PENDING_", "TODO", "FIXME", "\ufffd", "\u00c3", "\u00e2\u20ac"):
            with self.subTest(marker=marker):
                self.assertNotIn(marker, self.document)
        self.assertFalse(re.search(r"(?m)^# (?:TODO|Draft)\b", self.document))


if __name__ == "__main__":
    unittest.main()
