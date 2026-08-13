from __future__ import annotations

import re
import tomllib
import unittest
from pathlib import Path

from se_harness import __version__
from se_harness.cli import build_parser


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
NOTES_ROOT = REPOSITORY_ROOT / "docs" / "notes"

DOCUMENTS = {
    REPOSITORY_ROOT / "README.md": "6/10",
    NOTES_ROOT / "README.md": "4/10",
    NOTES_ROOT / "harness-overview.md": "4/10",
    NOTES_ROOT / "harness-uml-model.md": "6/10",
    NOTES_ROOT / "harness-operational-phasing.md": "6/10",
    NOTES_ROOT / "harness-branching-model.md": "6.5/10",
    NOTES_ROOT / "harness-lineage-example.md": "7/10",
    NOTES_ROOT / "harness-installation-and-upgrades.md": "5/10",
    NOTES_ROOT / "harnessctl-reference.md": "7/10",
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
                self.assertNotIn("> **Target expertise:", content)

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
        self.assertIn("requires every work order's `architecture` relation to be non-empty", model)

    def test_observations_do_not_claim_human_authority(self) -> None:
        overview = self.contents[NOTES_ROOT / "harness-overview.md"]
        model = self.contents[NOTES_ROOT / "harness-uml-model.md"]
        phasing = self.contents[NOTES_ROOT / "harness-operational-phasing.md"]
        self.assertIn("None of these commands approves work", overview)
        self.assertIn("Only an accountable assurance decision", model)
        self.assertIn("ready` is a proposal", phasing)
        self.assertIn("separate human release decision", overview)

    def test_branching_guide_is_one_explicitly_non_authoritative_model(self) -> None:
        branching = self.contents[NOTES_ROOT / "harness-branching-model.md"]
        context = (REPOSITORY_ROOT / "docs" / "engineering" / "REPOSITORY_CONTEXT.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("SE Harness does **not** require this branch model", branching)
        self.assertEqual(2, branching.count("gitGraph"))
        self.assertIn("Example 1: one change from implementation to release", branching)
        self.assertIn("tag points back to **candidate C**", branching)
        self.assertIn("Example 2: continuous integration, delayed release", branching)
        self.assertIn("`main` is the only integration branch for normal development", branching)
        self.assertIn("Harness-Work-Order: WO-FEAT-001", branching)
        self.assertIn("G5: ready VREC-C binds C3", branching)
        self.assertIn("WO-QUAL-030", branching)
        self.assertIn("aggregate VREC re-evaluates the release-bearing work at R", branching)
        self.assertIn("`release/0.3` is not used for new features", branching)
        self.assertIn("v0.3.0` and `release/0.3` are created only after G10", branching)
        self.assertNotIn("feature/<short-description>", context)
        self.assertIn("harness-branching-model.md", context)
        self.assertIn("release/x.y", context)
        self.assertIn("REL-031", branching)
        self.assertIn("VER-FIX-014", branching)
        self.assertIn("WO-QUAL-031", branching)
        self.assertIn("docs/engineering/verification-records/VREC-030.md", branching)
        self.assertIn("W013` advisory, never a validation error", branching)

    def test_refused_verification_paths_are_explained_without_invented_authority(self) -> None:
        phasing = self.contents[NOTES_ROOT / "harness-operational-phasing.md"]
        branching = self.contents[NOTES_ROOT / "harness-branching-model.md"]

        for required in (
            "## When verification is refused",
            "A VREC has no `rejected` status",
            "The work order honestly remains `implemented`",
            "only a proposal and is not release-eligible",
            "an RLS has no `rejected` or `superseded` state",
            "W-REV-004",
            "harness-uml-model.md#important-multiplicities-and-invariants",
            "harness-branching-model.md#when-assurance-refuses-a-candidate",
        ):
            self.assertIn(required, phasing)

        for required in (
            "### When assurance refuses a candidate",
            "does not remove the candidate from `main` or rewrite branch history",
            "a revert is also an append-only commit and becomes its own candidate",
            "harness-operational-phasing.md#when-verification-is-refused",
        ):
            self.assertIn(required, branching)

        self.assertEqual(2, branching.count("gitGraph"))

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
            "dashboard",
            "capture-verification",
            "prepare-release",
        }
        self.assertTrue(documented_commands.issubset(command_action.choices))

        example = self.contents[NOTES_ROOT / "harness-lineage-example.md"]
        for command in documented_commands:
            with self.subTest(command=command):
                self.assertIn(f"harnessctl {command}", example)

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

    def test_development_note_explains_three_self_hosting_planes(self) -> None:
        development = self.contents[NOTES_ROOT / "developing-se-harness.md"]
        for phrase in (
            "Released governor",
            "Candidate source",
            "Candidate package",
            "0.2.2",
            "0.2.1",
            ".self-hosting/governor.toml",
            "does not automatically promote",
            "python -m unittest discover",
            "SELF_HOSTING.md",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, development)

    def test_readme_version_matches_package_metadata(self) -> None:
        project = tomllib.loads(
            (REPOSITORY_ROOT / "pyproject.toml").read_text(encoding="utf-8")
        )["project"]
        readme = self.contents[REPOSITORY_ROOT / "README.md"]
        self.assertEqual(project["version"], __version__)
        self.assertIn(f'se-harness=={project["version"]}', readme)

    def test_markdown_fences_are_balanced(self) -> None:
        for path, content in self.contents.items():
            with self.subTest(path=path.name):
                self.assertEqual(0, content.count("```") % 2)


if __name__ == "__main__":
    unittest.main()
