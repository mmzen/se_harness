from __future__ import annotations

import sys
import tomllib
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
from tests.root_identity_support import evaluator_scripts_dir  # noqa: E402
from tests.root_identity_support import load_evaluator_module
SCRIPTS = evaluator_scripts_dir()
_artifact_layout_registry = load_evaluator_module("artifact_layout_registry")
ARTIFACT_DIRECTORIES = _artifact_layout_registry.ARTIFACT_DIRECTORIES
ARTIFACT_PREFIXES = _artifact_layout_registry.ARTIFACT_PREFIXES
CATALOG_BEGIN = "<!-- artifact-catalog:begin -->"
CATALOG_END = "<!-- artifact-catalog:end -->"
CATALOG_COLUMNS = (
    "Type",
    "Prefix",
    "Objective",
    "Required or applicable when",
    "Valid omission or reuse",
    "Accountable owner",
    "Primary relations",
)


class ArtifactCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.traceability_path = REPOSITORY_ROOT / "docs" / "engineering" / "TRACEABILITY.md"
        cls.traceability = cls.traceability_path.read_text(encoding="utf-8")

    def catalog_block(self) -> str:
        self.assertEqual(1, self.traceability.count(CATALOG_BEGIN))
        self.assertEqual(1, self.traceability.count(CATALOG_END))
        return self.traceability.split(CATALOG_BEGIN, 1)[1].split(CATALOG_END, 1)[0]

    def types_absent_from_root_catalog(self) -> set[str]:
        """Registry types the hash-locked root catalog does not carry yet (declared, not hidden)."""
        present = {row[0].strip("`") for row in self.catalog_rows()}
        # WO-DCM-001 added the decision type and WO-RSK-010 the risk type to the
        # candidate registry; each root gains its row at adoption.
        absent = ({"decision", "risk"} & set(ARTIFACT_DIRECTORIES)) - present
        self.assertLessEqual(absent, {"decision", "risk"})
        return absent

    def catalog_rows(self) -> list[list[str]]:
        rows: list[list[str]] = []
        for line in self.catalog_block().splitlines():
            if not line.startswith("| `"):
                continue
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            rows.append(cells)
        return rows

    def test_catalog_exactly_covers_the_canonical_registry(self) -> None:
        rows = self.catalog_rows()
        parsed = [(row[0].strip("`"), row[1].strip("`")) for row in rows]
        self.assertEqual(len(parsed), len({artifact_type for artifact_type, _ in parsed}))
        # WO-DCM-001 (SPEC-DCM-001): the candidate registry added the decision type; the
        # root catalog is the released root's and gains the row at adoption.
        registry_types = set(ARTIFACT_DIRECTORIES) - self.types_absent_from_root_catalog()
        self.assertEqual(registry_types, {artifact_type for artifact_type, _ in parsed})
        self.assertEqual(
            {artifact_type: prefix for artifact_type, prefix in ARTIFACT_PREFIXES.items() if artifact_type in registry_types},
            {artifact_type: prefix for artifact_type, prefix in parsed},
        )

    def test_every_catalog_entry_defines_the_complete_applicability_contract(self) -> None:
        block = self.catalog_block()
        header = next(line for line in block.splitlines() if line.startswith("| Type |"))
        self.assertEqual(list(CATALOG_COLUMNS), [cell.strip() for cell in header.strip("|").split("|")])
        rows = self.catalog_rows()
        self.assertEqual(len(ARTIFACT_DIRECTORIES) - len(self.types_absent_from_root_catalog()), len(rows))
        for row in rows:
            with self.subTest(artifact_type=row[0]):
                self.assertEqual(len(CATALOG_COLUMNS), len(row))
                self.assertTrue(all(cell and cell != "â€”" for cell in row))
        for non_formal in (
            "evidence",
            "acceptance scenarios",
            "candidate commits",
            "dashboards",
            "tickets",
            "conversations",
        ):
            self.assertIn(non_formal, block.lower())

    def test_router_and_human_notes_point_to_the_authoritative_catalog(self) -> None:
        router = (REPOSITORY_ROOT / "ENGINEERING_HARNESS.md").read_text(encoding="utf-8")
        self.assertIn("Normative chain, artifact applicability, relation types, and coverage", router)
        self.assertIn("`docs/engineering/TRACEABILITY.md`", router)
        link = "../engineering/TRACEABILITY.md#artifact-applicability-catalog"
        for note in ("harness-overview.md", "harness-uml-model.md"):
            content = (REPOSITORY_ROOT / "docs" / "notes" / note).read_text(encoding="utf-8")
            with self.subTest(note=note):
                self.assertIn(link, content)
                self.assertNotIn(CATALOG_BEGIN, content)

    def test_released_policy_copies_match_with_declared_candidate_exceptions(self) -> None:
        released_work_order = (
            REPOSITORY_ROOT / "docs/engineering/templates/WORK_ORDER.template.md"
        ).read_text(encoding="utf-8")
        candidate_work_order = (
            REPOSITORY_ROOT
            / "templates/repository/standard/docs/engineering/templates/WORK_ORDER.template.md"
        ).read_text(encoding="utf-8")
        # WO-KIS-009 removes the optional delegation switch prospectively.
        # All other metadata still matches the installed template.
        released_metadata = tomllib.loads(released_work_order.split("+++", 2)[1])
        released_metadata.pop("delegation", None)
        candidate_metadata = tomllib.loads(candidate_work_order.split("+++", 2)[1])
        self.assertNotIn("delegation", candidate_metadata)
        self.assertEqual(
            released_metadata,
            candidate_metadata,
        )
        self.assertIn("docs/engineering/ARTIFACT_AUTHORING.md", candidate_work_order)
        released_traceability = (
            REPOSITORY_ROOT / "docs/engineering/TRACEABILITY.md"
        ).read_text(encoding="utf-8")
        candidate_traceability = (
            REPOSITORY_ROOT / "templates/repository/standard/docs/engineering/TRACEABILITY.md"
        ).read_text(encoding="utf-8")
        # WO-KIS-001 changes only these two applicability rows. The released root
        # stays untouched; all other rows still compare against the released copy.
        for prefix in ("| `requirement` |", "| `risk` |"):
            previous = next((line for line in released_traceability.splitlines() if line.startswith(prefix)), None)
            current = next(line for line in candidate_traceability.splitlines() if line.startswith(prefix))
            if previous is not None:
                candidate_traceability = candidate_traceability.replace(current, previous)
        # WO-DST-027 (SPEC-DST-028 DST-TPL-001 to DST-TPL-003, DST-TPL-006): the candidate
        # rewrites TRC-008 for the retired relation; a root released before it (0.17.0)
        # carries the compatibility-only reading, declared here; a root released with the
        # rewrite takes the branches below unchanged.
        retired_rule = (
            "`TRC-008` - `ARCH.constrains` is retired. A validator MUST refuse every\n"
            "`constrains` relation with `E016`, whatever the architecture's status; it\n"
            "classifies no historical relation and reports no migration. `ARCH.addresses`\n"
            "and `ARCH.conforms_to` are the only form. Installation and upgrade MUST NOT\n"
            "rewrite repository-owned artifacts.\n"
        )
        compatibility_rule = (
            "`TRC-008` - `ARCH.constrains` is compatibility-only. A validator MAY classify\n"
            "an unambiguous completed historical relation and MUST report the migration. It\n"
            "MUST reject a mixed or ambiguous target set. Installation and upgrade MUST NOT\n"
            "rewrite repository-owned artifacts.\n"
        )
        self.assertIn(retired_rule, candidate_traceability)
        if compatibility_rule in released_traceability:
            candidate_traceability = candidate_traceability.replace(retired_rule, compatibility_rule, 1)
        # WO-DCM-001 (SPEC-DCM-001): the candidate TRACEABILITY.md adds the decision
        # artifact's catalog row, relations TRC-REL-020..022 and rule TRC-015. A root
        # released before them lacks exactly those lines, declared here; a root
        # released with them takes the equality branch.
        if "`TRC-REL-023`" in released_traceability:
            self.assertEqual(released_traceability, candidate_traceability)
        elif "`TRC-REL-020`" in released_traceability:
            # WO-RSK-010 (SPEC-RSK-010): the candidate TRACEABILITY.md adds the risk
            # artifact's catalog row, relations TRC-REL-023..025 and rule TRC-016. A root
            # released before them lacks exactly those lines, declared here; a root
            # released with them takes the equality branch above.
            risk_rows = ("| `TRC-REL-023`", "| `TRC-REL-024`", "| `TRC-REL-025`", "| `risk` | `RISK-` |")
            kept: list[str] = []
            skipping = False
            for line in candidate_traceability.splitlines():
                if line.startswith("`TRC-016`"):
                    skipping = True
                if skipping:
                    if not line.strip():
                        skipping = False
                    continue
                if line.startswith(risk_rows):
                    continue
                kept.append(line)
            self.assertEqual(released_traceability.splitlines(), kept)
            self.assertIn("`TRC-016`", candidate_traceability)
        else:
            decision_rows = ("| `TRC-REL-020`", "| `TRC-REL-021`", "| `TRC-REL-022`", "| `decision` | `DEC-` |")
            kept: list[str] = []
            skipping = False
            for line in candidate_traceability.splitlines():
                if line.startswith("`TRC-015`"):
                    skipping = True
                if skipping:
                    if not line.strip():
                        skipping = False
                    continue
                if line.startswith(decision_rows):
                    continue
                kept.append(line)
            self.assertEqual(released_traceability.splitlines(), kept)
            self.assertIn("`TRC-015`", candidate_traceability)
        self.assertIn("`TRC-001`", released_traceability)
        self.assertIn("`TRC-001`", candidate_traceability)
        self.assertIn("BCP 14", candidate_traceability)
        router = (REPOSITORY_ROOT / "ENGINEERING_HARNESS.md").read_text(encoding="utf-8")
        router_template = (
            REPOSITORY_ROOT / "templates/repository/standard/ENGINEERING_HARNESS.md.tpl"
        ).read_text(encoding="utf-8")
        evaluator_version = tomllib.loads(
            (REPOSITORY_ROOT / ".engineering-harness.toml").read_text(encoding="utf-8")
        )["harness"]["tool_version"]
        candidate_router = router_template.replace("{{PROJECT_NAME}}", "se_harness").replace(
            "{{HARNESS_VERSION}}", evaluator_version
        )
        technical_communication_route = (
            "| Eligible operator and technical-artifact English prose | "
            "`docs/engineering/TECHNICAL_COMMUNICATION.md` |"
        )
        artifact_authoring_route = (
            "| Artifact authoring locations and templates | "
            "`docs/engineering/templates/README.md` |"
        )
        # The released root follows its adopted evaluator, independently of the
        # candidate version (WO-HUP-019).
        self.assertIn("the selected governing chain is invalid or artifact IDs are ambiguous", candidate_router)
        self.assertIn("The installed evaluator owns executable policy", candidate_router)
        self.assertIn("--replace-file PATH", candidate_router)
        self.assertEqual(1, router.count(technical_communication_route))
        self.assertIn(
            f"{technical_communication_route}\n{artifact_authoring_route}",
            router,
        )
        self.assertIn("## Lifecycle handoff", router)
        self.assertNotIn("## Lifecycle restitution", router)
        self.assertIn("The structured\nresult is authoritative", router)
        if tuple(int(part) for part in evaluator_version.split(".")) >= (0, 18, 0):
            self.assertIn("It MUST NOT claim an effect, decision, or authority absent", router)
        else:
            self.assertIn("Model transcription MUST NOT", router)
        self.assertNotIn("harnessctl focus", router)
        self.assertNotIn("harnessctl preflight", router)
        self.assertIn("WORKFLOW.json", router)

    def test_work_order_template_expresses_conditional_architecture(self) -> None:
        template = (
            REPOSITORY_ROOT / "docs/engineering/templates/WORK_ORDER.template.md"
        ).read_text(encoding="utf-8")
        front_matter = template.split("+++", 2)[1]
        self.assertNotIn("architecture =", front_matter)
        self.assertIn(
            "Omit the `architecture` relation only when no active architecture addresses any implemented requirement.",
            template,
        )


if __name__ == "__main__":
    unittest.main()
