from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from se_harness.installer import _block, tracked_content
from se_harness.integrity import canonical_sha256
from se_harness.workflow_contract import load_validated_contracts
from se_harness.workflow_procedures import resolve_procedure


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROUTER = REPOSITORY_ROOT / "templates" / "repository" / "standard" / "ENGINEERING_HARNESS.md.tpl"
PACKAGED_FRAGMENT = REPOSITORY_ROOT / "templates" / "repository" / "standard" / "AGENTS.md.fragment"
RETIRED_PATH = "docs/engineering/REPOSITORY_CONTEXT.md"
RETIRED_ACTION_PREFIX = "CTX-ACT-"
BASELINE_RULE_IDS = ("HRN-001", "HRN-002", "HRN-003", "HRN-004", "HRN-005", "HRN-006", "HRN-007", "HRN-008")
BASELINE_ROUTING_SUBJECTS = (
    "Lifecycle states, transitions, procedures, next actions, and handoff fields",
    "Roles, accountabilities, delegation, and reserved decisions",
    "Gate criteria, executable predicates, validation planes, pass/fail behavior, and exceptions",
    "Normative chain, artifact applicability, relation types, and coverage",
    "Artifact authoring locations and templates",
    "Repository-specific facts and commands",
)
BASELINE_STOP_CONDITIONS = (
    "managed integrity fails",
    "the formal graph is invalid",
    "no phase-eligible selected work order exists",
    "a required governing artifact or gate is missing",
    "a required check fails",
    "owner instructions conflict with this contract",
    "remediation would exceed the selected work order",
    "the requested action lacks the decision right or explicit authority defined",
)
PACKAGED_FRAGMENT_BLOCK_DIGEST = "864a2c3bafbc3191c778fe20402a2e983b4bece1c11103540164c06c46b4bef5"
# Files permitted to name the retired path, with the reason each is not a live obligation.
PERMITTED_MENTIONS = {
    "AGENTS.md": "owner region of this repository, governed by REQ-IAR-020",
    "docs/engineering/README.md": "this repository's own owner-owned seed",
    "docs/engineering/harness-distribution/README.md": "packet index recording the retirement",
    "docs/engineering/harness-distribution/evidence/WO-DST-021-verification.md": "retained evidence for this retirement",
    "docs/engineering/harness-distribution/evidence/WO-DOC-007-verification.md": "historical evidence",
    "docs/engineering/harness-distribution/evidence/WO-DOC-009-verification.md": "historical evidence",
    "docs/engineering/harness-distribution/evidence/WO-DOC-013-verification.md": "historical evidence",
    "docs/engineering/harness-distribution/requirements/REQ-DST-008.md": "superseded requirement retained as history",
    "docs/engineering/harness-distribution/requirements/REQ-DST-065.md": "the retiring requirement",
    "docs/engineering/harness-distribution/specifications/SPEC-DST-021.md": "the retiring specification",
    "docs/engineering/harness-distribution/work-orders/WO-DOC-007.md": "historical work order",
    "docs/engineering/harness-distribution/work-orders/WO-DOC-009.md": "historical work order",
    "docs/engineering/harness-distribution/work-orders/WO-DST-021.md": "the retiring work order",
    "docs/engineering/instruction-architecture/README.md": "packet index recording the retirement",
    "docs/engineering/instruction-architecture/evidence/WO-DST-021-verification.md": "retained evidence for this retirement",
    "docs/engineering/instruction-architecture/evidence/WO-IAR-012-verification.md": "retained evidence for the owner-region revision",
    "docs/engineering/instruction-architecture/requirements/REQ-IAR-005.md": "superseded requirement retained as history",
    "docs/engineering/instruction-architecture/requirements/REQ-IAR-020.md": "owner-region requirement, ordinary owner content only",
    "docs/engineering/instruction-architecture/requirements/REQ-IAR-021.md": "the routing requirement",
    "docs/engineering/instruction-architecture/specifications/SPEC-IAR-012.md": "owner-region contract, ordinary owner content only",
    "docs/engineering/instruction-architecture/verification/VER-IAR-012.md": "owner-region verification contract",
    "docs/engineering/instruction-architecture/work-orders/WO-IAR-012.md": "owner-region work order",
    "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-001-verification.md": "historical evidence",
    "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-001.md": "historical work order",
    "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-002.md": "approved root-upgrade scope names the owner context path",
    "docs/engineering/release-orchestration/work-orders/WO-RLO-004.md": "approved execution scope names the owner context path",
    "docs/engineering/released-evaluator-boundary/architecture/adr/ADR-REB-010.md": "names this repository's own owner context file as an affected operator path",
    "docs/engineering/released-evaluator-boundary/evidence/WO-REB-005-verification.md": "retained released-0.5 preflight evidence",
    "docs/engineering/released-evaluator-boundary/requirements/REQ-REB-023.md": "names this repository's own owner context file as an affected operator path",
    "docs/engineering/self-hosting-boundary/work-orders/WO-SHB-001.md": "historical work order",
    "docs/engineering/verification-supersession/engineering-README.md": "historical domain note",
    "docs/engineering/work-order-assurance-classification/evidence/WO-WAC-001-verification.md": "historical evidence",
    "docs/engineering/workflow-execution/evidence/WO-WEX-002-verification.md": "historical evidence",
    "docs/engineering/workflow-execution/work-orders/WO-WEX-002.md": "historical work order",
    "docs/notes/developing-se-harness.md": "this repository's own owner content, named as owner content",
    "docs/notes/harness-migration-repository-context-retirement.md": "migration note describing the retirement",
}
HISTORICAL_RECORDS = tuple(
    relative
    for relative, reason in sorted(PERMITTED_MENTIONS.items())
    if reason in {"historical evidence", "historical work order", "historical domain note"}
)
OWNER_REGION_PROBES = (
    "- Test: python -m unittest\n",
    "<!-- CTX-ACT-REPOSITORY-CHECKS -->\n- Repository purpose: TODO[purpose]\n",
    "## Local notes\n\nTODO[unresolved]\n",
    "".join(f"- line {index}\n" for index in range(200)),
)


class ContextRoutingRetirementTests(unittest.TestCase):
    def router_text(self) -> str:
        return TEMPLATE_ROUTER.read_text(encoding="utf-8")

    def test_router_routes_repository_facts_to_the_owner_region_only(self) -> None:
        router = self.router_text()
        self.assertIn("owner-controlled region\nof `AGENTS.md`", router)
        self.assertIn("| Repository-specific facts and commands | the owner-controlled region of `AGENTS.md` |", router)
        self.assertNotIn("REPOSITORY_CONTEXT", router)
        self.assertNotIn("repository context", router.lower())
        self.assertNotIn(RETIRED_ACTION_PREFIX, router)

    def test_router_stop_conditions_retain_the_baseline_without_repository_context(self) -> None:
        section = self.router_text().split("## Stop conditions", 1)[1]
        for condition in BASELINE_STOP_CONDITIONS:
            with self.subTest(condition=condition):
                self.assertIn(condition, section)
        for withdrawn in ("REPOSITORY_CONTEXT", "repository context", "context is incomplete", "context is missing"):
            with self.subTest(withdrawn=withdrawn):
                self.assertNotIn(withdrawn, section.lower() if withdrawn.islower() else section)

    def test_router_rule_identifiers_keep_their_recorded_order(self) -> None:
        found = re.findall(r"HRN-\d{3}", self.router_text())
        self.assertEqual(list(BASELINE_RULE_IDS), found)
        self.assertEqual(len(set(found)), len(found))

    def test_routing_table_gives_every_subject_exactly_one_owner(self) -> None:
        rows = [
            line
            for line in self.router_text().split("| Subject | Normative owner |", 1)[1].splitlines()
            if line.startswith("|") and not line.startswith("| ---")
        ]
        subjects: list[str] = []
        for row in rows:
            cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
            self.assertEqual(2, len(cells), row)
            subject, owner = cells
            self.assertTrue(owner, row)
            subjects.append(subject)
        self.assertEqual(list(BASELINE_ROUTING_SUBJECTS), subjects)

    def test_packaged_fragment_block_matches_the_recorded_baseline(self) -> None:
        block = _block(PACKAGED_FRAGMENT.read_bytes(), Path("AGENTS.md"))
        self.assertEqual(PACKAGED_FRAGMENT_BLOCK_DIGEST, canonical_sha256(block))
        text = block.decode("utf-8")
        self.assertEqual(1, text.count("ENGINEERING_HARNESS.md"))
        self.assertNotIn("REPOSITORY_CONTEXT", text)

    def test_fragment_digests_equal_their_lock_entries(self) -> None:
        lock = json.loads((REPOSITORY_ROOT / ".engineering-harness.lock").read_text(encoding="utf-8"))
        fragments = {path: entry for path, entry in lock["files"].items() if entry.get("mode") == "fragment"}
        self.assertTrue(fragments)
        for path, entry in sorted(fragments.items()):
            with self.subTest(path=path):
                content = (REPOSITORY_ROOT / path).read_bytes()
                self.assertEqual(entry["sha256"], canonical_sha256(tracked_content("fragment", content)))

    def test_owner_region_content_changes_no_digest_or_diagnostic(self) -> None:
        agents = (REPOSITORY_ROOT / "AGENTS.md").read_bytes()
        baseline = canonical_sha256(tracked_content("fragment", agents))
        head, marker, tail = agents.decode("utf-8").partition("<!-- se-harness:begin -->")
        self.assertTrue(marker)
        for probe in OWNER_REGION_PROBES:
            with self.subTest(probe=probe[:32]):
                mutated = (head + probe + marker + tail).encode("utf-8")
                self.assertEqual(baseline, canonical_sha256(tracked_content("fragment", mutated)))

    def test_resolved_procedures_are_deterministic_and_free_of_the_action_form(self) -> None:
        _, _, _, procedures, _ = load_validated_contracts()
        self.assertTrue(procedures)
        parameters = {
            "artifact_id": "WO-ABC-001",
            "work_order_id": "WO-ABC-001",
            "target": ".",
            "version": "0.0.0",
        }
        for procedure_id in sorted(procedures):
            with self.subTest(procedure=procedure_id):
                try:
                    first = resolve_procedure(procedures, procedure_id, parameters)
                except Exception as error:  # a parameter this corpus does not supply
                    self.assertIn("WEX221", str(error))
                    continue
                second = resolve_procedure(procedures, procedure_id, parameters)
                rendered = json.dumps(first, sort_keys=True)
                self.assertEqual(rendered, json.dumps(second, sort_keys=True))
                self.assertNotIn(RETIRED_ACTION_PREFIX, rendered)
                self.assertNotIn("action_id", rendered)
                for step in first["steps"]:
                    if step.get("kind") == "reference":
                        self.assertEqual({"id", "kind", "procedure_id"}, set(step) & {"id", "kind", "procedure_id", "action_id"})

    def test_no_product_code_path_reads_the_retired_path(self) -> None:
        for source in sorted((REPOSITORY_ROOT / "se_harness").glob("*.py")):
            with self.subTest(module=source.name):
                text = source.read_text(encoding="utf-8")
                self.assertNotIn("REPOSITORY_CONTEXT", text)
                self.assertNotIn(RETIRED_ACTION_PREFIX, text)
                self.assertNotIn("repository_commands", text)
                self.assertNotIn("repository_context", text)

    def test_only_recorded_files_name_the_retired_path(self) -> None:
        found: dict[str, str] = {}
        for path in sorted(REPOSITORY_ROOT.rglob("*.md")):
            relative = path.relative_to(REPOSITORY_ROOT).as_posix()
            if relative.startswith(("target/", "tests/", "templates/")) or ".venv" in relative:
                continue
            if "REPOSITORY_CONTEXT" in path.read_text(encoding="utf-8"):
                found[relative] = "present"
        self.assertEqual(sorted(PERMITTED_MENTIONS), sorted(found))

    def test_historical_records_still_describe_the_retired_obligation(self) -> None:
        self.assertEqual(12, len(HISTORICAL_RECORDS))
        for relative in HISTORICAL_RECORDS:
            with self.subTest(record=relative):
                path = REPOSITORY_ROOT / relative
                self.assertTrue(path.is_file())
                self.assertIn("REPOSITORY_CONTEXT", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
