"""Evidence for REQ-TCM-012 and REQ-TCM-013 (WO-TCM-008): the reader-first capability shape."""

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
from tests.mutation_guard_support import patch_mutation_authority
from tests.artifact_support import create_base_chain, formal, write
from tests.cli_support import invoke
from tests.fixture_support import standard_repository

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = REPOSITORY_ROOT / "templates/repository/standard/docs/engineering/templates"
GUIDE = REPOSITORY_ROOT / "templates/repository/standard/docs/engineering/ARTIFACT_AUTHORING.md"
EXPLORER_TEMPLATE = REPOSITORY_ROOT / "se_harness/engine/harness_explorer/index.template.html"

ABILITY = "A repository owner can qualify an exact evaluator succession under the managed check without version-specific workflow logic."
PLAIN = "Moving from one released version to the next should not need a new workflow each time."
NEED = "A repository owner needs the same controlled CI behavior for every succession. They do not want to teach the workflow each version pair."
NOT_DECIDED = "- Which lane runs the succession is a requirement's decision.\n- How identities are compared is the specification's."


def reader_first_body(*, plain: str = PLAIN, need: str = NEED, extra: str = "") -> str:
    return f"\n## In plain words\n\n{plain}\n\n## Actor and need\n\n{need}\n\n## Not decided here\n\n{NOT_DECIDED}\n{extra}"


class ReaderFirstCapabilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        standard_repository(self.root)
        lock_path = self.root / ".engineering-harness.lock"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["evaluator"]["archive_name"] = f"se_harness-{lock['tool_version'].replace('-', '_')}-py3-none-any.whl"
        lock["evaluator"]["archive_sha256"] = "a" * 64
        lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        patch_mutation_authority(self)
        create_base_chain(self.root, operating_contract_status="draft")
        self.path = self.root / "docs/engineering/product/capabilities/CAP-002.md"

    def write_capability(self, *, status: str = "draft", ability: str | None = ABILITY, body: str | None = None) -> None:
        front = "" if ability is None else f'ability = "{ability}"'
        write(self.path, formal("CAP-002", "capability", status, {"derives_from": ["INT-001"]}, front) + (reader_first_body() if body is None else body))

    def write_deriving_requirements(self, ids: tuple[str, ...]) -> None:
        for identifier in ids:
            write(
                self.root / f"docs/engineering/product/requirements/{identifier}.md",
                formal(identifier, "requirement", "draft", {"derives_from": ["CAP-002"]},
                       'statement = "WHEN a succession is requested, THE SYSTEM SHALL qualify it."\nverification_method = ["test"]'),
            )

    def report(self):
        return validate_engineering_artifacts.validate_repository(self.root)

    def advisories(self, path_suffix: str = "CAP-002.md") -> dict[str, list[str]]:
        report = self.report()
        self.assertEqual([], [f"{i.code}: {i.message}" for i in report.errors if i.path.endswith(path_suffix)])
        found: dict[str, list[str]] = {}
        for item in report.advisories:
            if item.path.endswith(path_suffix):
                found.setdefault(item.code, []).append(item.message)
        return found

    # ---------------------------------------------------------------- REQ-TCM-012: template, field, checklist

    def test_the_capability_template_is_reader_first_with_an_ability_field(self) -> None:
        text = (TEMPLATES / "CAPABILITY.template.md").read_text(encoding="utf-8")
        self.assertEqual(["## In plain words", "## Actor and need", "## Not decided here"], re.findall(r"^## .*$", text, flags=re.MULTILINE))
        self.assertIsNotNone(re.search(r'^ability = "', text, flags=re.MULTILINE))
        self.assertIn("`GLOSSARY.md` at the repository", text)
        code, output, error = invoke("create-artifact", str(self.root), "--domain", "product", "--type", "capability", "--id", "CAP-003", "--quiet")
        self.assertEqual(0, code, error + output)
        created = (self.root / "docs/engineering/product/capabilities/CAP-003.md").read_text(encoding="utf-8")
        self.assertIn("## Not decided here", created)
        self.assertIn('ability = "', created)

    def test_the_ability_field_is_accepted_optional_and_refused_when_empty(self) -> None:
        self.write_capability(status="approved")
        self.assertEqual([], [f"{i.code}: {i.message}" for i in self.report().errors])
        self.write_capability(status="approved", ability=None, body="\n## Capability statement\n\n`An owner can do it.`\n")
        self.assertEqual([], [f"{i.code}: {i.message}" for i in self.report().errors])
        self.write_capability(status="approved", ability="")
        errors = [f"{i.code}: {i.message}" for i in self.report().errors if i.path.endswith("CAP-002.md")]
        self.assertEqual(1, len(errors), errors)
        self.assertIn("E-AUT-002", errors[0])
        self.assertIn("ability", errors[0])


    # ---------------------------------------------------------------- REQ-TCM-012: advisories

    def test_a_reader_first_draft_within_every_budget_raises_no_advisory(self) -> None:
        self.write_capability()
        self.assertEqual({}, self.advisories())


    def test_no_capability_advisory_fires_on_an_approved_capability_or_another_type(self) -> None:
        self.write_capability(status="approved", ability="An owner qualifies it.", body="\n## Outcomes\n\n" + " ".join(["word"] * 200) + ".\n\n## Candidate requirements\n\n- `REQ-001`\n")
        self.assertEqual({}, self.advisories())
        # an intent draft and a requirement draft over the capability constants raise none of the capability codes
        write(self.root / "docs/engineering/product/intent/INT-002.md",
              formal("INT-002", "intent", "draft", {}, 'outcome = "An owner can see the outcome after delivery."') + "\n## In plain words\n\nShort.\n\n## Problem\n\n" + " ".join(["word"] * 180) + ".\n\n## Candidate requirements\n\n- `REQ-001`\n")
        found = self.advisories("INT-002.md")
        self.assertFalse({"W-AUT-016", "W-AUT-017", "W-AUT-018"} & set(found), found)
        self.assertNotIn("W-AUT-005", found)  # 180 words are within the intent budget of 200

    def test_this_repository_corpus_raises_no_capability_advisory(self) -> None:
        report = validate_engineering_artifacts.validate_repository(REPOSITORY_ROOT)
        capability_paths = {str(p) for p in (REPOSITORY_ROOT / "docs/engineering").glob("*/capabilities/CAP-*.md")}
        found = [f"{i.path}: {i.code}" for i in report.advisories if any(i.path.replace("/", "\\") in path or i.path in path for path in capability_paths)]
        self.assertEqual([], found)

    # ---------------------------------------------------------------- REQ-TCM-013: the graph and the Explorer

    def bundle_detail(self, artifact_id: str) -> dict:
        code, output, error = invoke("dashboard", str(self.root))
        self.assertEqual(0, code, error + output)
        for p in (self.root / "target/harness-dashboard/data/artifacts").rglob("*"):
            if p.is_file():
                detail = json.loads(p.read_text(encoding="utf-8"))
                if detail.get("artifact", {}).get("id") == artifact_id:
                    return detail["artifact"]
        self.fail(f"no detail for {artifact_id}")

    def test_derived_requirements_are_read_from_the_graph_never_from_a_list(self) -> None:
        self.write_capability(status="approved", body=reader_first_body(extra="\n## Candidate requirements\n\n- `REQ-002`\n- `REQ-003`\n"))
        self.write_deriving_requirements(("REQ-002", "REQ-003", "REQ-004", "REQ-005", "REQ-006"))
        artifact = self.bundle_detail("CAP-002")
        self.assertEqual(["REQ-002", "REQ-003", "REQ-004", "REQ-005", "REQ-006"], artifact["derived_requirements"])
        self.assertEqual(ABILITY, artifact["ability"])
        self.assertEqual(PLAIN, artifact["plain_words"])
        self.write_capability(status="approved")
        for identifier in ("REQ-002", "REQ-003", "REQ-004", "REQ-005", "REQ-006"):
            (self.root / f"docs/engineering/product/requirements/{identifier}.md").unlink()
        artifact = self.bundle_detail("CAP-002")
        self.assertEqual([], artifact["derived_requirements"])
        self.write_capability(status="approved", ability=None, body="\n## Capability statement\n\n`An owner can do it.`\n")
        artifact = self.bundle_detail("CAP-002")
        self.assertNotIn("ability", artifact)
        self.assertNotIn("plain_words", artifact)

    def test_the_explorer_places_the_ability_the_plain_words_and_the_derives_list_before_the_events(self) -> None:
        # the built template embeds the views as JSON strings, so markers are the
        # mustache names, which survive the escaping
        template = EXPLORER_TEMPLATE.read_text(encoding="utf-8")
        ability = template.index("{{ability}}")
        derives = template.index("{{derives}}")
        events = template.index("{{events}}")
        self.assertLess(ability, derives)
        self.assertLess(derives, events)
        self.assertIn("{{plainWords}}", template[ability:derives])
        self.assertIn("{{c.ability}}", template)
        self.assertIn("derived_requirements", template)


if __name__ == "__main__":
    unittest.main()
