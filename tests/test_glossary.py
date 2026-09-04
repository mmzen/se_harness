"""Evidence for REQ-TCM-007 (WO-TCM-006): the repository-owned glossary and its drift report."""

from __future__ import annotations

import contextlib
import importlib.util
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
TEMPLATE_ROOT = REPOSITORY_ROOT / "templates/repository/standard"
SEED = TEMPLATE_ROOT / "GLOSSARY.md.seed"
INSPECT = TEMPLATE_ROOT / "scripts/inspect_engineering_artifacts.py"


_INSPECT_MODULE = None


def load_inspect():
    """The candidate inspection script, loaded by path once so its exception classes stay identical."""
    global _INSPECT_MODULE
    if _INSPECT_MODULE is None:
        import sys

        scripts = str(TEMPLATE_ROOT / "scripts")
        if scripts not in sys.path:
            sys.path.insert(0, scripts)
        spec = importlib.util.spec_from_file_location("candidate_inspect", INSPECT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _INSPECT_MODULE = module
    return _INSPECT_MODULE


class GlossaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        code, _, error = self.invoke("init", str(self.root), "--project-name", "Ledger Service")
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
        self.glossary = self.root / "GLOSSARY.md"

    def invoke(self, *arguments: str) -> tuple[int, str, str]:
        output = io.StringIO()
        error = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            code = main(list(arguments))
        return code, output.getvalue(), error.getvalue()

    def write_corpus(self, *, ledger: int = 80, tally: int = 10, checkpoint: int = 80) -> None:
        body = "\n## Why\n\n" + " ".join(["The ledger keeps every posting."] * ledger) + "\n\n" + " ".join(["A tally is kept."] * tally) + "\n\n" + " ".join(["The checkpoint gate holds."] * checkpoint) + "\n"
        write(
            self.root / "docs/engineering/product/requirements/REQ-002.md",
            formal("REQ-002", "requirement", "draft", {"derives_from": ["CAP-001"]},
                   'statement = "WHEN a posting arrives, THE LEDGER SHALL record it."\nverification_method = ["test"]') + body,
        )

    def report(self, threshold: int = 50) -> dict:
        module = load_inspect()
        validation = _load_validator_module().validate_repository(self.root)
        return module.build_vocabulary_report(self.root, validation, threshold)

    # ---------------------------------------------------------------- TCM-RFR-007: the seed

    def test_init_seeds_an_empty_repository_owned_glossary(self) -> None:
        self.assertTrue(self.glossary.is_file())
        text = self.glossary.read_text(encoding="utf-8")
        self.assertIn("# Glossary for Ledger Service", text)
        self.assertIn("## Terms", text)
        terms_section = text.split("## Terms", 1)[1].split("## ", 1)[0]
        self.assertEqual("", terms_section.strip())
        self.assertNotIn("**", terms_section)
        lock = json.loads((self.root / ".engineering-harness.lock").read_text(encoding="utf-8"))
        self.assertEqual({"mode": "seed", "state": "present"}, lock["files"]["GLOSSARY.md"])
        self.assertNotIn("sha256", lock["files"]["GLOSSARY.md"])

    def test_an_edited_glossary_survives_upgrade_and_doctor_untouched(self) -> None:
        edited = self.glossary.read_text(encoding="utf-8").replace("## Terms\n", "## Terms\n\n**Posting.** One movement of value on the ledger.\n")
        self.glossary.write_text(edited, encoding="utf-8")
        before = self.glossary.read_bytes()
        code, output, error = self.invoke("upgrade", str(self.root), "--apply")
        self.assertEqual(0, code, error + output)
        self.assertEqual(before, self.glossary.read_bytes())
        code, output, error = self.invoke("doctor", str(self.root))
        self.assertEqual(0, code, error + output)
        self.assertNotIn("glossary.md: FAIL", output)

    def test_adopt_seeds_the_glossary_and_keeps_an_existing_one(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary)
            (target / "README.md").write_text("# existing\n", encoding="utf-8")
            (target / "GLOSSARY.md").write_text("# Ours\n\n## Terms\n\n**Posting.** Ours.\n", encoding="utf-8")
            code, output, error = self.invoke("adopt", str(target), "--project-name", "Adopted")
            self.assertEqual(0, code, error + output)
            self.assertEqual("# Ours\n\n## Terms\n\n**Posting.** Ours.\n", (target / "GLOSSARY.md").read_text(encoding="utf-8"))

    # ---------------------------------------------------------------- TCM-RFR-008: the report

    def test_the_report_names_frequent_project_terms_and_stale_entries_only(self) -> None:
        self.write_corpus()
        self.glossary.write_text(
            self.glossary.read_text(encoding="utf-8").replace("## Terms\n", "## Terms\n\n**Vault.** Where postings rest at night.\n\n**Tally.** A running count.\n"),
            encoding="utf-8",
        )
        report = self.report()
        undefined = {item["term"]: item["count"] for item in report["undefined_frequent_terms"]}
        self.assertIn("ledger", undefined)
        self.assertGreaterEqual(undefined["ledger"], 80)
        self.assertNotIn("tally", undefined)
        self.assertNotIn("checkpoint", undefined)
        self.assertNotIn("gate", undefined)
        self.assertEqual([{"term": "Vault"}], report["stale_entries"])
        self.assertEqual(2, report["entry_count"])
        self.assertTrue(report["present"])
        self.assertEqual([], report["notes"])
        self.assertEqual(report, self.report())

    def test_the_threshold_is_bounded_and_the_default_is_fifty(self) -> None:
        module = load_inspect()
        self.assertEqual(50, module.VOCABULARY_DEFAULT_THRESHOLD)
        self.write_corpus(ledger=40)
        self.assertEqual([], [item["term"] for item in self.report(50)["undefined_frequent_terms"] if item["term"] == "ledger"])
        self.assertIn("ledger", [item["term"] for item in self.report(30)["undefined_frequent_terms"]])
        with self.assertRaises(module.InspectionError):
            self.report(20)

    def test_a_missing_glossary_is_one_note_not_an_error(self) -> None:
        self.glossary.unlink()
        report = self.report()
        self.assertFalse(report["present"])
        self.assertEqual(1, len(report["notes"]))
        self.assertIn("GLOSSARY.md is absent", report["notes"][0])
        self.assertEqual(0, report["entry_count"])

    def test_inspect_carries_the_vocabulary_section_in_json_and_text(self) -> None:
        self.write_corpus()
        code, output, error = self.invoke("inspect", str(self.root), "--json")
        self.assertEqual(0, code, error)
        report = json.loads(output)
        self.assertEqual("derived", report["vocabulary"]["authority"])
        self.assertIn("ledger", [item["term"] for item in report["vocabulary"]["undefined_frequent_terms"]])
        code, output, error = self.invoke("inspect", str(self.root), "--vocabulary-threshold", "30")
        self.assertEqual(0, code, error)
        self.assertIn("Vocabulary (derived, informational):", output)
        self.assertIn("ledger (", output)
        code, output, error = self.invoke("inspect", str(self.root), "--vocabulary-threshold", "5")
        self.assertEqual(2, code)
        self.assertIn("vocabulary threshold must be between 30 and 100", error)

    # ---------------------------------------------------------------- TCM-RFR-010: the boundary

    def test_no_glossary_term_ships_with_the_distribution(self) -> None:
        seed = SEED.read_text(encoding="utf-8")
        terms_section = seed.split("## Terms", 1)[1].split("## ", 1)[0]
        self.assertEqual("", terms_section.strip())
        entry = re.compile(r"^\*\*[^*]+\*\*", re.M)
        for path in sorted(TEMPLATE_ROOT.rglob("*")):
            if not path.is_file() or path.suffix not in {".md", ".seed", ".tpl", ".json", ".py"}:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            with self.subTest(path=path.relative_to(TEMPLATE_ROOT).as_posix()):
                if "## Terms" in text:
                    section = text.split("## Terms", 1)[1].split("\n## ", 1)[0]
                    self.assertEqual([], entry.findall(section))
        this_glossary = (REPOSITORY_ROOT / "GLOSSARY.md").read_text(encoding="utf-8")
        heads = [match.group(0) for match in re.finditer(r"^\*\*[^*]+\*\*", this_glossary, re.M)]
        self.assertGreaterEqual(len(heads), 30)
        for path in sorted(TEMPLATE_ROOT.rglob("*.md")) + sorted(TEMPLATE_ROOT.rglob("*.seed")):
            text = path.read_text(encoding="utf-8", errors="replace")
            for head in heads:
                self.assertNotIn(head, text, f"{path.name} carries the glossary entry {head}")

    def test_the_seed_is_packaged_explicitly_at_the_template_root(self) -> None:
        # The template root is packaged as an explicit file list, so a seed there
        # needs its own data-files line or the wheel omits it while the checkout works.
        pyproject = (REPOSITORY_ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('"templates/repository/standard/GLOSSARY.md.seed"', pyproject)

    def test_this_repository_glossary_defines_the_terms_the_assessment_named(self) -> None:
        text = (REPOSITORY_ROOT / "GLOSSARY.md").read_text(encoding="utf-8")
        for term in ("**Candidate.**", "**Digest.**", "**Canonical.**", "**Deterministic.**", "**Schema.**", "**Accountable role.**", "**Dashboard snapshot.**", "**Provenance.**", "**Predicate.**"):
            self.assertIn(term, text)
        self.assertIn("Two vocabularies meet in a requirement.", text)
        self.assertIn("## Upkeep", text)


if __name__ == "__main__":
    unittest.main()
