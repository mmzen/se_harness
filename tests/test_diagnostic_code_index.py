"""Evidence for REQ-TCM-005 (WO-TCM-003): the diagnostic-code index cannot drift."""

from __future__ import annotations

import unittest
from pathlib import Path

from repository_tools.diagnostic_code_index import (
    NOTE_RELATIVE,
    PREFIXES,
    generate,
    main,
    scan,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

#: TCM-DCI-005: one known code per emitting component, taken from the modules
#: the assessment named, never from the generator's output.
KNOWN_CODES = (
    "A001",
    "I001",
    "E012",
    "W013",
    "W-AUT-002",
    "WEX210",
    "WEX-ECP-030",
    "WEX301",
    "WEX404",
    "MG001",
    "RID018",
    "EPS001",
    "JNL001",
    "PRE001",
    "REN010",
    "RR001",
    "PV001",
)
NOT_DIAGNOSTICS = ("WO-ECP-010", "SPEC-ECP-006", "ECP-DLG-001", "SHA256")


class DiagnosticCodeIndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rendered = generate(REPOSITORY_ROOT)
        cls.committed = (
            (REPOSITORY_ROOT / NOTE_RELATIVE)
            .read_bytes()
            .decode("utf-8")
            .replace("\r\n", "\n")
        )

    def test_the_committed_page_equals_the_regeneration(self) -> None:
        self.assertEqual(self.rendered, self.committed)

    def test_the_check_mode_reports_the_verdict(self) -> None:
        self.assertEqual(0, main(["--check", "--repository", str(REPOSITORY_ROOT)]))

    def test_every_registered_prefix_matches_at_least_one_code(self) -> None:
        codes = scan(REPOSITORY_ROOT)
        for prefix in PREFIXES:
            with self.subTest(prefix=prefix):
                self.assertTrue(codes[prefix], f"registered prefix {prefix} matches no code")

    def test_known_diagnostic_codes_are_indexed(self) -> None:
        for code in KNOWN_CODES:
            with self.subTest(code=code):
                self.assertIn(f"| `{code}` |", self.committed)

    def test_artifact_and_rule_identifiers_are_not_indexed(self) -> None:
        for identifier in NOT_DIAGNOSTICS:
            with self.subTest(identifier=identifier):
                self.assertNotIn(f"| `{identifier}` |", self.committed)

    def test_the_page_carries_the_standard_shape(self) -> None:
        for marker in (
            "GENERATED FILE (WO-TCM-003)",
            "python -m repository_tools.diagnostic_code_index --write",
            "<!-- Target expertise: 5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->",
            "## Summary",
            "## How to read a code",
            "## Codes",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.committed)

    def test_the_page_is_linked_from_the_notes(self) -> None:
        index = (REPOSITORY_ROOT / "docs/notes/README.md").read_text(encoding="utf-8")
        self.assertIn("(diagnostic-codes.md)", index)
        check_note = (REPOSITORY_ROOT / "docs/notes/harnessctl-check.md").read_text(encoding="utf-8")
        self.assertIn("diagnostic-codes.md", check_note)

    def test_two_regenerations_are_identical(self) -> None:
        self.assertEqual(self.rendered, generate(REPOSITORY_ROOT))


if __name__ == "__main__":
    unittest.main()
