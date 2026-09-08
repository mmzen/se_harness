from __future__ import annotations

import json
import re
import tomllib
import unittest
from pathlib import Path

from se_harness import __version__
from se_harness.cli import build_parser


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
NOTES_ROOT = REPOSITORY_ROOT / "docs" / "notes"

DOCUMENTS = {
    NOTES_ROOT / "README.md": "4/10",
    NOTES_ROOT / "harness-overview.md": "4/10",
    NOTES_ROOT / "harness-uml-model.md": "6/10",
    NOTES_ROOT / "harness-operational-phasing.md": "6/10",
    NOTES_ROOT / "harness-branching-model.md": "6.5/10",
    NOTES_ROOT / "harness-lineage-example.md": "7/10",
    NOTES_ROOT / "harness-installation-and-upgrades.md": "5/10",
    NOTES_ROOT / "harnessctl-reference.md": "7/10",
    NOTES_ROOT / "harnessctl-check.md": "6/10",
    NOTES_ROOT / "developing-se-harness.md": "8/10",
}


class ProgressiveDocumentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contents = {
            path: path.read_text(encoding="utf-8") for path in DOCUMENTS
        }

    def test_required_documents_have_exact_expertise_labels(self) -> None:
        for path, score in DOCUMENTS.items():
            with self.subTest(path=path.name, score=score):
                self.assertTrue(path.is_file())
                content = self.contents[path]
                self.assertIn(f"<!-- Target expertise: {score}.", content)
                self.assertIn("knowledge expected from the reader", content)

    def test_expertise_metadata_is_not_visible_rendered_content(self) -> None:
        for path, content in self.contents.items():
            rendered_source = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)
            with self.subTest(path=path.name):
                self.assertNotIn("Target expertise", rendered_source)
                self.assertNotRegex(rendered_source, r"\b\d+(?:\.\d+)?/10\b")

    def test_notes_index_links_the_progressive_path(self) -> None:
        index = self.contents[NOTES_ROOT / "README.md"]
        ordered_targets = (
            "harness-overview.md",
            "harness-uml-model.md",
            "harness-operational-phasing.md",
            "harness-branching-model.md",
            "harness-lineage-example.md",
        )
        positions = [index.index(target) for target in ordered_targets]
        self.assertEqual(sorted(positions), positions)

    def test_all_local_note_links_resolve(self) -> None:
        for source, content in self.contents.items():
            for raw_target in re.findall(r"\[[^]]+\]\(([^)]+)\)", content):
                if re.match(r"(?:https?://|mailto:|#)", raw_target):
                    continue
                target = raw_target.split("#", 1)[0]
                resolved = (source.parent / target).resolve()
                with self.subTest(source=source.name, target=raw_target):
                    self.assertTrue(resolved.is_file(), f"missing link from {source}: {raw_target}")

    def test_notes_are_current_and_not_consumer_specific(self) -> None:
        combined = "\n".join(
            content for path, content in self.contents.items() if path.parent == NOTES_ROOT
        )
        for obsolete in (
            "Mokiterions",
            "SE Harness 0.2.1",
            "validator wins",
            "INT-MOK-",
            "REQ-MOK-",
            "cargo fmt",
        ):
            with self.subTest(obsolete=obsolete):
                self.assertNotIn(obsolete, combined)
        for marker in ("\ufffd", "\u00c3", "\u00e2\u20ac"):
            with self.subTest(marker=marker):
                self.assertNotIn(marker, combined)

    def test_model_and_example_use_current_relation_terms(self) -> None:
        model = self.contents[NOTES_ROOT / "harness-uml-model.md"]
        example = self.contents[NOTES_ROOT / "harness-lineage-example.md"]
        for term in (
            "addresses",
            "conforms_to",
            "decides",
            "implements",
            "specifications",
            "architecture",
            "verification",
            "verifies_work_order",
            "includes_verification",
            "releases_work",
        ):
            with self.subTest(term=term):
                self.assertIn(term, model + example)
        self.assertIn("decision_assessment", model)
        self.assertIn("adr_required", model)
        self.assertIn("no_significant_decision", model)
        self.assertNotIn("ARCH.constrains", model + example)
        self.assertIn("omits its `architecture` relation", model)
        self.assertNotIn("Current limitation", model)
        self.assertIn(
            "../engineering/TRACEABILITY.md#artifact-applicability-catalog",
            model,
        )

    def test_active_public_command_contract_uses_six_commands(self) -> None:
        distribution = REPOSITORY_ROOT / "docs" / "engineering" / "harness-distribution"
        requirement = (distribution / "requirements" / "REQ-DST-025.md").read_text(encoding="utf-8")
        specification = (distribution / "specifications" / "SPEC-DST-007.md").read_text(encoding="utf-8")
        verification = (distribution / "verification" / "VER-DST-007.md").read_text(encoding="utf-8")

        self.assertIn("six ordinary human-facing subcommands", requirement)
        self.assertIn("harnessctl inspect", specification)
        self.assertIn("six allowed routine harness subcommands", verification)
        for obsolete in ("five ordinary human-facing subcommands", "five allowed routine harness subcommands"):
            with self.subTest(obsolete=obsolete):
                self.assertNotIn(obsolete, requirement + specification + verification)

    # SPEC-TST-002 TST-HYG-013: the four checks below replace sentence pins on the notes with
    # structural ones. A heading exists, a command parses, a link and its anchor resolve.
    AUTHORITY_SECTIONS = {
        "harness-overview.md": ("## What remains under human or repository control", "## What the tools can and cannot do"),
        "harness-uml-model.md": ("## Important multiplicities and invariants", "## Authority is outside cardinality"),
        "harness-operational-phasing.md": ("## When verification is refused", "## Formal gates versus Explorer readiness"),
        "harness-branching-model.md": (
            "## Policy boundary",
            "## Example 1: one change from implementation to release",
            "## Example 2: continuous integration, delayed release, and supported maintenance",
            "### When assurance refuses a candidate",
            "## What can vary in another repository",
        ),
    }

    def test_authority_notes_keep_their_boundary_sections(self) -> None:
        for note, headings in self.AUTHORITY_SECTIONS.items():
            content = self.contents[NOTES_ROOT / note]
            for heading in headings:
                with self.subTest(note=note, heading=heading):
                    self.assertIn(f"\n{heading}\n", content)
        self.assertEqual(2, self.contents[NOTES_ROOT / "harness-branching-model.md"].count("gitGraph"))

    def test_every_command_a_note_names_exists_in_the_current_cli(self) -> None:
        parser = build_parser()
        command_action = next(action for action in parser._actions if getattr(action, "choices", None) and "preflight" in action.choices)
        subcommands = set(command_action.choices)
        for path, content in self.contents.items():
            spans = re.findall(r"`([^`\n]*)`", content) + re.findall(r"```[^\n]*\n(.*?)```", content, flags=re.DOTALL)
            named = {match for span in spans for match in re.findall(r"harnessctl ([a-z][a-z-]+)", span)}
            for command in sorted(named):
                with self.subTest(note=path.name, command=command):
                    self.assertIn(command, subcommands)

    def test_every_local_anchor_in_a_note_resolves_to_a_heading(self) -> None:
        def slug(heading: str) -> str:
            text = heading.lstrip("#").strip().lower().replace("`", "")
            text = re.sub(r"[^a-z0-9 _-]", "", text)
            return text.replace(" ", "-")

        for source, content in self.contents.items():
            for raw_target in re.findall(r"\[[^]]+\]\(([^)]+)\)", content):
                if re.match(r"(?:https?://|mailto:)", raw_target) or "#" not in raw_target:
                    continue
                target, anchor = raw_target.split("#", 1)
                resolved = (source.parent / target).resolve() if target else source
                if not resolved.is_file():
                    continue  # the link test reports a missing file
                headings = {slug(line) for line in resolved.read_text(encoding="utf-8").splitlines() if line.startswith("#")}
                with self.subTest(source=source.name, anchor=raw_target):
                    self.assertIn(anchor, headings)

    def test_example_commands_exist_in_current_cli(self) -> None:
        parser = build_parser()
        command_action = next(
            action
            for action in parser._actions
            if getattr(action, "choices", None) and "preflight" in action.choices
        )
        documented_commands = {
            "doctor",
            "preflight",
            "validate",
            "inspect",
            "dashboard",
            "capture-verification",
            "prepare-release",
        }
        self.assertTrue(documented_commands.issubset(command_action.choices))

        example = self.contents[NOTES_ROOT / "harness-lineage-example.md"]
        for command in documented_commands:
            with self.subTest(command=command):
                self.assertIn(f"harnessctl {command}", example)

    def test_check_note_is_indexed_linked_and_names_only_contract_identifiers(self) -> None:
        # SPEC-ECP-008 ECP-HST-005 (WO-ECP-012): the check reference derives its tables from
        # the installed contracts, so every identifier it names must exist there.
        note = self.contents[NOTES_ROOT / "harnessctl-check.md"]
        self.assertIn("harnessctl-check.md", self.contents[NOTES_ROOT / "README.md"])
        self.assertIn("harnessctl-check.md", self.contents[NOTES_ROOT / "harnessctl-reference.md"])
        for heading in (
            "## What the command does",
            "## The five checkpoints",
            "## How the artifact's state selects the rule",
            "## Gates and predicates by checkpoint",
            "## Supplying the change set",
            "## Outcomes and what `Blocked by` names",
            "## Refusal codes",
            "## One work order, from approved to implemented",
        ):
            with self.subTest(heading=heading):
                self.assertIn(heading, note)
        standard = REPOSITORY_ROOT / "templates" / "repository" / "standard" / "docs" / "engineering"
        workflow = json.loads((standard / "WORKFLOW.json").read_text(encoding="utf-8"))
        gates = json.loads((standard / "QUALITY_GATES.json").read_text(encoding="utf-8"))
        known = {rule["id"] for rule in workflow["recommendations"]}
        known |= {procedure["id"] for procedure in workflow["procedures"]}
        known |= {gate["id"] for gate in gates["gates"]}
        known |= {predicate["id"] for gate in gates["gates"] for predicate in gate["predicates"]}
        known |= {check for binding in gates["transition_bindings"] for check in binding.get("structural", [])}
        known |= {"QG-STRUCTURAL"}
        named = set(re.findall(r"`((?:WFL|PROC|QG|QGP|QGS)-[A-Z0-9-]+)`", note))
        self.assertTrue(named, "the note names no contract identifier")
        self.assertEqual(set(), named - known, sorted(named - known))
        for rule in workflow["recommendations"]:
            with self.subTest(rule=rule["id"]):
                self.assertIn(f"`{rule['id']}`", note)
        for gate in gates["gates"]:
            with self.subTest(gate=gate["id"]):
                self.assertIn(f"`{gate['id']}`", note)

    def test_command_reference_exactly_covers_current_cli(self) -> None:
        parser = build_parser()
        command_action = next(
            action
            for action in parser._actions
            if getattr(action, "choices", None) and "preflight" in action.choices
        )
        reference = self.contents[NOTES_ROOT / "harnessctl-reference.md"]
        table_commands = set(
            re.findall(r"(?m)^\| `([a-z][a-z-]+)` \|", reference)
        )
        self.assertEqual(set(command_action.choices), table_commands)
        for command in command_action.choices:
            with self.subTest(command=command):
                self.assertIn(f"harnessctl {command}", reference)

    def test_installation_note_separates_package_and_repository_upgrade(self) -> None:
        installation = self.contents[NOTES_ROOT / "harness-installation-and-upgrades.md"]
        upgrade = installation.split("## Upgrade an existing installation\n", 1)[1]
        commands = (
            "python -m pip install --upgrade se-harness",
            "harnessctl upgrade C:\\path\\to\\repository",
            "harnessctl upgrade C:\\path\\to\\repository --apply",
            "harnessctl doctor C:\\path\\to\\repository",
        )
        positions = [upgrade.index(command) for command in commands]
        self.assertEqual(sorted(positions), positions)
        self.assertIn("does **not** silently rewrite", installation)
        self.assertIn("read-only plan", installation)
        self.assertIn("explicitly owner-authorized transactional mutation", installation)

    def test_development_note_explains_standard_evaluator_and_candidate_planes(self) -> None:
        development = self.contents[NOTES_ROOT / "developing-se-harness.md"]
        evaluator_version = tomllib.loads(
            (REPOSITORY_ROOT / ".engineering-harness.toml").read_text(encoding="utf-8")
        )["harness"]["tool_version"]
        for phrase in (
            "Released evaluator",
            "Candidate source",
            "Candidate package",
            __version__,
            evaluator_version,
            ".engineering-harness.toml",
            "Candidate success never changes",
            "python -m unittest discover",
            "SELF_HOSTING.md",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, development)

    def test_candidate_version_matches_package_metadata(self) -> None:
        project = tomllib.loads(
            (REPOSITORY_ROOT / "pyproject.toml").read_text(encoding="utf-8")
        )["project"]
        self.assertEqual(project["version"], __version__)

    def test_markdown_fences_are_balanced(self) -> None:
        for path, content in self.contents.items():
            with self.subTest(path=path.name):
                self.assertEqual(0, content.count("```") % 2)


if __name__ == "__main__":
    unittest.main()
