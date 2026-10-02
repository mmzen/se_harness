from __future__ import annotations

import hashlib
import json
import tomllib
import unittest
from pathlib import Path

from tests.root_identity_support import load_evaluator_module

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
_registry = load_evaluator_module("artifact_layout_registry")
ARTIFACT_DIRECTORIES = _registry.ARTIFACT_DIRECTORIES
ARTIFACT_PREFIXES = _registry.ARTIFACT_PREFIXES
# Source tests inspect product assets. Adopted resource identity is checked by
# the released evaluator, separately from candidate-source tests.
STANDARD_ROOT = REPOSITORY_ROOT / "templates/repository/standard"
LEGACY_ROOT = REPOSITORY_ROOT / "tests/fixtures/progressive-discovery/released-0.18.0"


class ArtifactCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.guide = (STANDARD_ROOT / "docs/engineering/harness/ARTIFACTS.md").read_text(encoding="utf-8")
        cls.types = cls.guide.split("## Artifact types", 1)[1].split("## Artifact locations", 1)[0]

    def catalog_rows(self) -> list[list[str]]:
        return [[cell.strip() for cell in line.strip("|").split("|")]
                for line in self.types.splitlines() if line.startswith("| `")]

    def test_catalog_exactly_covers_the_canonical_registry(self) -> None:
        rows = self.catalog_rows()
        types = [row[0].strip("`") for row in rows]
        self.assertEqual(len(types), len(set(types)))
        self.assertEqual(set(ARTIFACT_DIRECTORIES), set(types))
        self.assertEqual(ARTIFACT_PREFIXES,
                         {row[0].strip("`"): row[1].strip("`") for row in rows})

    def test_each_type_explains_its_purpose_and_applicability(self) -> None:
        header = next(line for line in self.types.splitlines() if line.startswith("| Type"))
        self.assertEqual(["Type", "ID prefix", "Purpose", "When needed"],
                         [cell.strip() for cell in header.strip("|").split("|")])
        for row in self.catalog_rows():
            with self.subTest(artifact=row[0]):
                self.assertEqual(4, len(row))
                self.assertTrue(all(cell and cell != "—" for cell in row))
        for non_formal in ("evidence", "acceptance scenarios", "commits", "dashboards", "tickets", "conversations"):
            self.assertIn(non_formal, self.types.lower())
        self.assertIn("Reuse an existing active artifact", self.types)

    def test_router_and_human_notes_reach_the_current_catalog(self) -> None:
        router = (STANDARD_ROOT / "ENGINEERING_HARNESS.md.tpl").read_text(encoding="utf-8")
        define = (STANDARD_ROOT / "docs/engineering/harness/DEFINE_CHANGE.md").read_text(encoding="utf-8")
        self.assertIn("docs/engineering/harness/DEFINE_CHANGE.md", router)
        self.assertIn("ARTIFACTS.md", define)
        for note in ("harness-overview.md", "harness-uml-model.md"):
            content = (REPOSITORY_ROOT / "docs/notes" / note).read_text(encoding="utf-8")
            with self.subTest(note=note):
                self.assertIn("docs/engineering/harness/ARTIFACTS.md", content)
                self.assertIn("`artifact-types`", content)
                self.assertNotIn("<!-- artifact-catalog:begin -->", content)

    def test_legacy_catalog_remains_bound_to_its_released_fixture(self) -> None:
        # History is a fixed release input, not the expected content of the
        # successor's compatibility pointer (IAR-DIS-013, WO-HUP-021).
        content = (LEGACY_ROOT / "TRACEABILITY.md").read_text(encoding="utf-8")
        provenance = json.loads((LEGACY_ROOT / "provenance.json").read_text(encoding="utf-8"))
        self.assertEqual(provenance["editable_guides"]["docs/engineering/TRACEABILITY.md"],
                         hashlib.sha256(content.encode("utf-8")).hexdigest())
        self.assertIn("<!-- artifact-catalog:begin -->", content)
        self.assertIn("`TRC-001`", content)
        self.assertIn("`TRC-015`", content)
        self.assertIn("`TRC-016`", content)

    def test_current_routes_resolve_without_retired_pointers(self) -> None:
        for name in ("OPERATING_CARD.md", "DECISION_RIGHTS.md", "QUALITY_GATES.md",
                     "WORKFLOW.md", "TRACEABILITY.md", "TECHNICAL_COMMUNICATION.md"):
            with self.subTest(retired=name):
                self.assertFalse((REPOSITORY_ROOT / "docs/engineering" / name).exists())
        guides = STANDARD_ROOT / "docs/engineering/harness"
        for source, destination, heading in (
            ("DEFINE_CHANGE.md", "ARTIFACTS.md", "## Artifact types"),
            ("DEFINE_CHANGE.md", "DEFINITION_LINKS.md", "## Links between definitions"),
            ("DRAFT_WORK_ORDERS.md", "WORK_AND_EVIDENCE.md", "## Links from work orders (WO)"),
        ):
            with self.subTest(destination=destination):
                self.assertIn(destination, (guides / source).read_text(encoding="utf-8"))
                self.assertIn(heading, (guides / destination).read_text(encoding="utf-8"))
        router = (STANDARD_ROOT / "ENGINEERING_HARNESS.md.tpl").read_text(encoding="utf-8")
        self.assertIn("MUST be the only source of truth", router)
        self.assertIn("docs/engineering/harness/CONTINUE.md", router)
        self.assertIn("docs/engineering/harness/COMMUNICATION.md", router)
        results = (STANDARD_ROOT / "docs/engineering/harness/RESULTS.md").read_text(encoding="utf-8")
        self.assertIn("The result controls the reported scope", results)
        self.assertIn("Do not invent an effect, authority", results)
        self.assertIn("Machine WORKFLOW.json and QUALITY_GATES.json are evaluator inputs", router)

    def test_work_order_template_expresses_conditional_architecture(self) -> None:
        relative = "docs/engineering/templates/WORK_ORDER.template.md"
        template = (STANDARD_ROOT / relative).read_text(encoding="utf-8")
        metadata = tomllib.loads(template.split("+++", 2)[1])
        self.assertNotIn("architecture", metadata["relations"])
        self.assertNotIn("delegation", metadata)
        self.assertIn("<actual human who confirmed the assurance classification>", template)
        self.assertIn("docs/engineering/harness/AUTHORITY.md#authority-from-work-approval", template)
        self.assertIn("Omit the `architecture` relation only when no active architecture addresses any implemented requirement.", template)
        self.assertIn("docs/engineering/ARTIFACT_AUTHORING.md", template)


if __name__ == "__main__":
    unittest.main()
