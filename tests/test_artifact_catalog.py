from __future__ import annotations

import re
import sys
import tomllib
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
# The candidate registry lives in the standard template; the root copy is the released
# evaluator's and may lag it (WO-RSK-001).
SCRIPTS = REPOSITORY_ROOT / "templates/repository/standard/scripts"
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
        cls.traceability_path = REPOSITORY_ROOT / "templates" / "repository" / "standard" / "docs" / "engineering" / "TRACEABILITY.md"
        cls.traceability = cls.traceability_path.read_text(encoding="utf-8")

    def catalog_block(self) -> str:
        self.assertEqual(1, self.traceability.count(CATALOG_BEGIN))
        self.assertEqual(1, self.traceability.count(CATALOG_END))
        return self.traceability.split(CATALOG_BEGIN, 1)[1].split(CATALOG_END, 1)[0]

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
        self.assertEqual(set(ARTIFACT_DIRECTORIES), {artifact_type for artifact_type, _ in parsed})
        self.assertEqual(
            ARTIFACT_PREFIXES,
            {artifact_type: prefix for artifact_type, prefix in parsed},
        )

    def test_every_catalog_entry_defines_the_complete_applicability_contract(self) -> None:
        block = self.catalog_block()
        header = next(line for line in block.splitlines() if line.startswith("| Type |"))
        self.assertEqual(list(CATALOG_COLUMNS), [cell.strip() for cell in header.strip("|").split("|")])
        rows = self.catalog_rows()
        self.assertEqual(len(ARTIFACT_DIRECTORIES), len(rows))
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
        expected_candidate_work_order = released_work_order.replace(
            "[relations]\n", delegation_block + "[relations]\n", 1
        )
        expected_candidate_work_order = expected_candidate_work_order.replace(
            "Add `architecture = ",
            delegation_guidance + "Add `architecture = ",
            1,
        )
        self.assertNotEqual(released_work_order, candidate_work_order)
        self.assertNotIn("[agentic_delegation]", released_work_order)
        self.assertEqual(candidate_work_order, expected_candidate_work_order)
        self.assertIn("[execution_scope]", released_work_order)
        self.assertIn("[execution_scope]", candidate_work_order)
        self.assertIn("component-prefix", candidate_work_order)
        released_traceability = (
            REPOSITORY_ROOT / "docs/engineering/TRACEABILITY.md"
        ).read_text(encoding="utf-8")
        candidate_traceability = (
            REPOSITORY_ROOT / "templates/repository/standard/docs/engineering/TRACEABILITY.md"
        ).read_text(encoding="utf-8")
        risk_type_row = (
            "| `risk` | `RISK-` | Records one thing that could go wrong at a declared stage, its likelihood, impact, "
            "computed score, the acceptance level in force, and its disposition. | It applies whenever an actor "
            "identifies a risk; a score at or above the acceptance level raises it and blocks the threatened stage "
            "until the stage owner disposes it. | Omit while no risk is identified; an empty register passes every "
            "gate and never implies that no risk exists. | Owner of the threatened stage (`DR-RISK-DISPOSE`). | "
            "`RISK.threatens -> *`; `RISK.mitigated_by -> WO, REQ, VER, OPS`; `RISK.avoided_by -> ADR`; "
            "`RLS.lists_risks -> RISK` |\n"
        )
        risk_relation_rows = (
            "| `TRC-REL-020` | `threatens` | `RISK -> INT, CAP, REQ, SPEC, ARCH, ADR, VER, WO, VREC, REL, RLS, OPS` | "
            "A risk names at least one artifact of its declared stage; the stage and the target types match. |\n"
            "| `TRC-REL-021` | `mitigated_by` | `RISK -> WO, REQ, VER, OPS` | A mitigating or mitigated risk names at "
            "least one governed mitigation. |\n"
            "| `TRC-REL-022` | `avoided_by` | `RISK -> ADR` | An avoided risk names exactly one decision record that "
            "removes its cause. |\n"
            "| `TRC-REL-023` | `lists_risks` | `RLS -> RISK` | A release record names every accepted or mitigated risk "
            "threatening its released work; it is derived at preparation. |\n"
        )
        operating_row_end = released_traceability.index("| `OPS.assures -> REQ` |\n") + len("| `OPS.assures -> REQ` |\n")
        expected_candidate_traceability = (
            released_traceability[:operating_row_end] + risk_type_row + released_traceability[operating_row_end:]
        )
        relation_row_end = expected_candidate_traceability.index("continuing assurance. |\n") + len("continuing assurance. |\n")
        expected_candidate_traceability = (
            expected_candidate_traceability[:relation_row_end] + risk_relation_rows + expected_candidate_traceability[relation_row_end:]
        )
        self.assertNotIn("`TRC-REL-020`", released_traceability)
        self.assertEqual(expected_candidate_traceability, candidate_traceability)
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
        self.assertNotIn(technical_communication_route, router)
        self.assertEqual(1, candidate_router.count(technical_communication_route))
        self.assertIn(
            f"{technical_communication_route}\n{artifact_authoring_route}",
            candidate_router,
        )
        self.assertNotEqual(router, candidate_router)
        self.assertIn("## Lifecycle restitution", router)
        self.assertNotIn("## Lifecycle handoff", router)
        self.assertIn("## Lifecycle handoff", candidate_router)
        self.assertIn("The structured\nresult is authoritative", candidate_router)
        self.assertIn("Model transcription MUST NOT", candidate_router)
        self.assertIn("harnessctl focus", router)
        self.assertNotIn("harnessctl focus", candidate_router)
        self.assertNotIn("harnessctl preflight", router)
        self.assertNotIn("harnessctl preflight", candidate_router)
        self.assertIn("WORKFLOW.json", candidate_router)

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
