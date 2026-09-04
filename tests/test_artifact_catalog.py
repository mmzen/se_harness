from __future__ import annotations

import re
import sys
import tomllib
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPOSITORY_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from artifact_layout_registry import ARTIFACT_DIRECTORIES, ARTIFACT_PREFIXES  # noqa: E402
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
        absent = ({"decision"} & set(ARTIFACT_DIRECTORIES)) - present
        self.assertLessEqual(absent, {"decision"})
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
                self.assertTrue(all(cell and cell != "—" for cell in row))
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
        delegation_block = '''# Optional. Delete this entire table when no agentic delegation is intended.
[agentic_delegation]
schema = "se-harness-agentic-delegation-v1"
delegated_by = "<accountable-role>"
delegate = "<logical-worker>"
decision_rights = ["DR-WO-START"]
operations = ["<closed-evaluator-operation>"]
execution_profiles = ["<approved-logical-profile>"]
paths = ["<path-within-execution-scope>"]
required_evidence = [
  { kind = "verification", path = "<retained-evidence-path>" },
]
valid_until = "YYYY-MM-DDTHH:MM:SSZ"
max_retry = 0
max_parallel_writers = 1
child_delegation = false
stop_before = [
  "accountable-decision-required",
  "action-time-authorization-required",
]

'''
        delegation_guidance = '''The optional agentic_delegation table records a maximum delegation; it does not
start work or grant standing authority. Delete the table when delegation is not
intended. When retained, replace every placeholder, keep every delegated and
evidence path within execution_scope.paths, use only managed decision rights,
evaluator operations, logical profiles, and roles, and set a bounded UTC
expiry. The exact released evaluator still derives a narrower, short-lived
envelope from fresh live state for each request.

'''
        # The released root (0.10.0) carries the delegation table WO-AEX-005 added;
        # WO-ECP-006 (SPEC-ECP-006 ECP-DLG-008) removed the table and its guidance
        # from the candidate template. The declared candidate exception is exactly
        # those two blocks; a root released with the removal takes the equality branch.
        self.assertIn("[execution_scope]", released_work_order)
        if delegation_block in released_work_order:
            self.assertIn(delegation_guidance, released_work_order)
            self.assertEqual(
                released_work_order.replace(delegation_block, "").replace(delegation_guidance, ""),
                candidate_work_order,
            )
        else:
            # WO-ECP-018 (SPEC-ECP-006 ECP-DLG-001): the candidate template adds the optional
            # `[delegation]` table and one paragraph; a root released with them takes equality.
            class_table = (
                "# Optional. Delete this table unless the accountable owner delegates the three\n"
                "# mechanical decisions of this work order to a non-human actor.\n"
                "[delegation]\n"
                'class = "execution"\n\n'
            )
            paragraph_start = "The optional `[delegation]` table with `class = "
            if class_table in candidate_work_order and class_table not in released_work_order:
                stripped = candidate_work_order.replace(class_table, "", 1)
                start = stripped.index(paragraph_start)
                end = stripped.index("\n\n", start) + 2
                stripped = stripped[:start] + stripped[end:]
                self.assertEqual(released_work_order, stripped)
            else:
                self.assertEqual(released_work_order, candidate_work_order)
        self.assertNotIn("agentic_delegation", candidate_work_order)
        self.assertIn("[execution_scope]", released_work_order)
        self.assertIn("[execution_scope]", candidate_work_order)
        self.assertIn("component-prefix", candidate_work_order)
        released_traceability = (
            REPOSITORY_ROOT / "docs/engineering/TRACEABILITY.md"
        ).read_text(encoding="utf-8")
        candidate_traceability = (
            REPOSITORY_ROOT / "templates/repository/standard/docs/engineering/TRACEABILITY.md"
        ).read_text(encoding="utf-8")
        # WO-DCM-001 (SPEC-DCM-001): the candidate TRACEABILITY.md adds the decision
        # artifact's catalog row, relations TRC-REL-020..022 and rule TRC-015. A root
        # released before them lacks exactly those lines, declared here; a root
        # released with them takes the equality branch.
        if "`TRC-REL-020`" in released_traceability:
            self.assertEqual(released_traceability, candidate_traceability)
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
        # The released root router is exact public 0.7.0 (WO-HUP-006): it equals
        # the candidate template rendered for this repository and its evaluator.
        self.assertEqual(router, candidate_router)
        self.assertEqual(1, router.count(technical_communication_route))
        self.assertIn(
            f"{technical_communication_route}\n{artifact_authoring_route}",
            router,
        )
        self.assertIn("## Lifecycle handoff", router)
        self.assertNotIn("## Lifecycle restitution", router)
        self.assertIn("The structured\nresult is authoritative", router)
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
