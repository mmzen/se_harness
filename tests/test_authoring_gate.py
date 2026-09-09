"""Evidence for REQ-TCM-017 (WO-TCM-011, SPEC-TCM-007): authoring advisories refuse approval of a definition draft.

Each test names the VER-TCM-007 row it serves. Fixture drafts are written with a known number
of advisories; the gate's message is compared with the validator's own diagnostics for the same
fixture; the budgets are read from the validator and asserted unchanged.
"""

from __future__ import annotations

import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from se_harness import codes
from se_harness.engine import validate_engineering_artifacts, validation_authoring
from se_harness.workflow_compliance import authoring_ready
from se_harness import workflow_predicates
from tests.artifact_support import create_base_chain, formal, write
from tests.cli_support import invoke
from tests.fixture_support import standard_repository
from tests.mutation_guard_support import patch_mutation_authority

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
GUIDE = REPOSITORY_ROOT / "templates/repository/standard/docs/engineering/ARTIFACT_AUTHORING.md"
CLOSING = "fix the draft and run the transition again"

CLEAN_STATEMENT = "WHEN a succession is requested, THE SYSTEM SHALL qualify it."
LONG_STATEMENT = (
    "THE SYSTEM SHALL qualify every requested succession between two released evaluator versions "
    "under the managed check before any installation is attempted on the repository root, "
    "recording every refusal with its reason, its time and its actor."
)  # 36 words
REQUIREMENT_BODY = (
    "\n## In plain words\n\nA succession is checked the same way every time.\n\n## Why\n\nA repository owner cannot check each pair by hand.\n\n"
    "## Behavior\n\n| Trigger | Response | On failure |\n| --- | --- | --- |\n| a succession is requested | it is qualified | it is refused |\n\n"
    "## Examples\n\n### Normal\n\n**Given** a pair, **When** requested, **Then** qualified.\n\n### Failure\n\n**Given** a bad pair, **When** requested, **Then** refused.\n"
)
CLEAN_OUTCOME = "A reviewer can tell from a work order's status alone whether it was authorized, finished, verified or released."
LONG_OUTCOME = (
    "A reviewer of any repository can tell from a work order's recorded status alone, without opening any record or "
    "asking anyone, whether the work was authorized, finished, verified, released and published to every consumer."
)  # 40 words
INTENT_BODY = (
    "\n## In plain words\n\nA status should mean one thing.\n\n## Problem\n\nFinished work is still marked approved.\n\n"
    "## Success measures\n\n| Measure | Today | When reached | Observed |\n| --- | --- | --- | --- |\n"
    "| Work orders whose status is not backed by a record | 11 | 0 | Explorer overview, at each release review |\n\n"
    "## Not this\n\n- Deciding whether any record is verified or released.\n"
)
CLEAN_ABILITY = "A repository owner can qualify an exact evaluator succession under the managed check without version-specific workflow logic."
NO_UNDER_ABILITY = "A repository owner can qualify an exact evaluator succession."
CAPABILITY_BODY = (
    "\n## In plain words\n\nMoving from one released version to the next should not need a new workflow each time.\n\n"
    "## Actor and need\n\nA repository owner needs the same controlled CI behavior for every succession.\n\n"
    "## Not decided here\n\n- Which lane runs the succession is a requirement's decision.\n"
)
CONTRACT = "A conforming succession qualifies the exact evaluator pair under the managed check and refuses every other pair."
SHORT_RULES = (
    "**FIX-SUC-001.** The lane MUST read the target evaluator identity from the lock and from nowhere else.\n\n"
    "**FIX-SUC-002.** The lane MUST NOT install an evaluator whose archive digest differs from the lock's.\n"
)
LONG_RULE = (
    "The lane MUST read the target evaluator identity from the committed lock file of the default branch and from no other "
    "source whatsoever, including the environment, the command line, the workflow inputs and any cached artifact of an earlier run.\n"
)
LONG_RULES = f"**FIX-SUC-001.** {LONG_RULE}\n**FIX-SUC-002.** {LONG_RULE}"


def specification_body(rules: str) -> str:
    return (
        "\n## In plain words\n\nMoving from one released version to the next is checked the same way every time.\n\n"
        "## Scope\n\nThe succession check of the managed lane.\n\n## Terms\n\n- **Pair.** The base and target evaluator identities.\n\n"
        f"## Rules\n\n{rules}\n## Failure behaviour\n\n| Trigger | Response | Diagnostic |\n| --- | --- | --- |\n| the digests differ | the lane stops before install | `SUC001` |\n\n"
        "## Examples\n\n**Given** a lock naming 0.15.0, **when** the lane runs, **then** it installs 0.15.0 (FIX-SUC-001).\n\n"
        "## Coverage\n\n| Requirement | Rules |\n| --- | --- |\n| `REQ-001` | FIX-SUC-001, FIX-SUC-002 |\n\n"
        "## Not decided here\n\n- The runner image is the workflow's choice.\n"
    )


class AuthoringGateFixture(unittest.TestCase):
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
        self.product = self.root / "docs/engineering/product"

    # ------------------------------------------------------------------ drafts

    def requirement(self, statement: str, *, status: str = "draft", body: str = REQUIREMENT_BODY) -> Path:
        # an approved requirement needs active specification and verification coverage (E007, E008)
        write(self.product / "specifications/SPEC-001.md", formal("SPEC-001", "specification", "implemented", {"specifies": ["REQ-001", "REQ-002"]}))
        write(self.product / "verification/VER-001.md", formal("VER-001", "verification", "approved", {"verifies": ["REQ-001", "REQ-002"]}))
        return write(self.product / "requirements/REQ-002.md", formal("REQ-002", "requirement", status, {"derives_from": ["CAP-001"]},
                     f'statement = "{statement}"\nverification_method = ["test"]') + body)

    def intent(self, outcome: str) -> Path:
        return write(self.product / "intent/INT-002.md", formal("INT-002", "intent", "draft", {}, f'outcome = "{outcome}"') + INTENT_BODY)

    def capability(self, ability: str) -> Path:
        return write(self.product / "capabilities/CAP-002.md", formal("CAP-002", "capability", "draft", {"derives_from": ["INT-001"]}, f'ability = "{ability}"') + CAPABILITY_BODY)

    def specification(self, rules: str) -> Path:
        return write(self.product / "specifications/SPEC-002.md", formal("SPEC-002", "specification", "draft", {"specifies": ["REQ-001"]},
                     f'contract = "{CONTRACT}"') + specification_body(rules))

    def report(self):
        return validate_engineering_artifacts.validate_repository(self.root)

    def artifact(self, artifact_id: str):
        return next(item for item in self.report().artifacts if item.artifact_id == artifact_id)

    def validator_advisories(self, artifact_id: str) -> list[tuple[str, str]]:
        report = self.report()
        path = self.artifact(artifact_id).path
        return [(item.code, item.message) for item in report.advisories if path.as_posix().endswith(item.path)]

    def transition(self, artifact_id: str, target: str, *, apply: bool = False) -> tuple[int, dict]:
        arguments = ["transition", str(self.root), "--set", f"{artifact_id}={target}", "--decision", f"{artifact_id}=owner", "--json"]
        if apply:
            arguments.append("--apply")
        code, output, error = invoke(*arguments)
        self.assertTrue(output, error)
        return code, json.loads(output)

    @staticmethod
    def predicate(result: dict, predicate_id: str) -> dict | None:
        for gate in result["compliance"]["gates"]:
            for item in gate.get("predicates", []):
                if item["id"] == predicate_id:
                    return item
        return None


class AuthoringAdvisoriesFunctionTests(AuthoringGateFixture):
    """VER-TCM-007 row 'function' (TCM-RFB-001, TCM-RFB-002, TCM-RFB-006)."""

    def test_a_clean_draft_returns_no_advisory(self) -> None:
        self.requirement(CLEAN_STATEMENT)
        self.assertEqual([], validate_engineering_artifacts.authoring_advisories(self.artifact("REQ-002"), self.root))

    def test_an_over_budget_draft_returns_exactly_the_validators_diagnostics(self) -> None:
        self.requirement(LONG_STATEMENT)
        found = [(i.code, i.message) for i in validate_engineering_artifacts.authoring_advisories(self.artifact("REQ-002"), self.root)]
        self.assertEqual(self.validator_advisories("REQ-002"), found)
        self.assertEqual([codes.W_AUT_003], [code for code, _ in found])
        self.assertRegex(found[0][1], r"statement is 3[0-9] words; the budget is 30")

    def test_an_approved_body_is_read_as_a_draft(self) -> None:
        self.requirement(LONG_STATEMENT, status="approved")
        approved = self.artifact("REQ-002")
        self.assertEqual([], self.validator_advisories("REQ-002"))  # AUT-ADV-002: validate is silent on an approved artifact
        found = [(i.code, i.message) for i in validate_engineering_artifacts.authoring_advisories(approved, self.root)]
        self.assertEqual([codes.W_AUT_003], [code for code, _ in found])

    def test_the_other_types_return_none_without_reading_the_passes(self) -> None:
        for artifact_id in ("ARCH-001", "ADR-001", "VER-001", "WO-001", "REL-001", "OPS-001"):
            with self.subTest(artifact=artifact_id), mock.patch.object(validation_authoring, "validate_authoring", side_effect=AssertionError("read")):
                self.assertEqual([], validate_engineering_artifacts.authoring_advisories(self.artifact(artifact_id), self.root))

    def test_the_entry_module_and_the_seam_expose_one_function(self) -> None:
        self.assertIs(validate_engineering_artifacts.authoring_advisories, validation_authoring.authoring_advisories)


class AuthoringGateRefusalTests(AuthoringGateFixture):
    """VER-TCM-007 rows 'refusal', 'order', 'other types and targets' (TCM-RFB-003 to TCM-RFB-006, TCM-RFB-010, TCM-RFB-012)."""

    def assert_refused(self, artifact_id: str, predicate_id: str, expected_codes: list[str]) -> None:
        path = self.artifact(artifact_id).path
        before = path.read_bytes()
        for apply in (False, True):
            with self.subTest(apply=apply):
                code, result = self.transition(artifact_id, "approved", apply=apply)
                self.assertEqual(1, code)
                self.assertEqual("blocked", result["operation"]["outcome"])
                blockers = [item for item in result["restitution"]["blocked_by"] if item.startswith(f"{predicate_id}: ")]
                self.assertEqual(1, len(blockers), result["restitution"])
                message = blockers[0].split(": ", 1)[1]
                if not apply:
                    # the preview carries the gate table; the applied refusal carries the blocker alone
                    predicate = self.predicate(result, predicate_id)
                    self.assertIsNotNone(predicate, result["compliance"])
                    self.assertEqual("fail", predicate["status"], predicate)
                    self.assertEqual(message, predicate["message"])
                self.assertTrue(message.endswith(CLOSING), message)
                listed = re.findall(r"W-AUT-\d{3}", message)
                self.assertEqual(expected_codes, listed, message)
                self.assertEqual([c for c, _ in self.validator_advisories(artifact_id)], listed)
        self.assertEqual(before, path.read_bytes())  # TCM-RFB-010: nothing written
        self.assertIn('status = "draft"', path.read_text(encoding="utf-8"))

    def test_a_requirement_draft_with_a_35_word_statement_is_refused(self) -> None:
        self.requirement(LONG_STATEMENT)
        self.assert_refused("REQ-002", "QGP-G1-AUTHORING", [codes.W_AUT_003])

    def test_an_intent_draft_with_a_40_word_outcome_is_refused(self) -> None:
        self.intent(LONG_OUTCOME)
        self.assert_refused("INT-002", "QGP-G1-AUTHORING", [codes.W_AUT_011])

    def test_a_capability_draft_without_under_is_refused(self) -> None:
        self.capability(NO_UNDER_ABILITY)
        self.assert_refused("CAP-002", "QGP-G1-AUTHORING", [codes.W_AUT_016])

    def test_a_specification_draft_with_two_long_rules_is_refused_naming_each(self) -> None:
        self.specification(LONG_RULES)
        self.assert_refused("SPEC-002", "QGP-G2-AUTHORING", [codes.W_AUT_021, codes.W_AUT_021])

    def test_a_clean_draft_passes_the_authoring_predicate(self) -> None:
        self.requirement(CLEAN_STATEMENT)
        self.intent(CLEAN_OUTCOME)
        self.capability(CLEAN_ABILITY)
        self.specification(SHORT_RULES)
        for artifact_id, predicate_id in (("REQ-002", "QGP-G1-AUTHORING"), ("INT-002", "QGP-G1-AUTHORING"), ("CAP-002", "QGP-G1-AUTHORING"), ("SPEC-002", "QGP-G2-AUTHORING")):
            with self.subTest(artifact=artifact_id):
                _, result = self.transition(artifact_id, "approved")
                predicate = self.predicate(result, predicate_id)
                self.assertEqual("pass", predicate["status"], predicate)
                self.assertIn("no authoring advisory", predicate["message"])

    def test_the_placeholder_failure_is_reported_before_the_advisory(self) -> None:
        # TCM-RFB-003
        self.requirement(LONG_STATEMENT, body=REQUIREMENT_BODY + "\n## Notes\n\n<Describe the notes here>\n")
        status, message = authoring_ready(self.artifact("REQ-002"), self.root)
        self.assertEqual("fail", status)
        self.assertIn("template placeholder", message)
        self.assertNotIn("W-AUT", message)

    def test_other_types_pass_without_reading_the_validator(self) -> None:
        # TCM-RFB-006
        write(self.product / "verification/VER-002.md", formal("VER-002", "verification", "draft", {"verifies": ["REQ-001"]}) + "\n## Cases\n\n- One.\n")
        write(self.product / "architecture/ARCH-002.md", formal("ARCH-002", "architecture", "draft", {"addresses": ["REQ-001"]}) + "\n## Shape\n\nOne.\n")
        write(self.product / "architecture/adr/ADR-002.md", formal("ADR-002", "adr", "draft", {"decides": ["ARCH-002"]}) + "\n## Decision\n\nOne.\n")
        for artifact_id in ("VER-002", "ARCH-002", "ADR-002"):
            with self.subTest(artifact=artifact_id), mock.patch.object(validate_engineering_artifacts, "authoring_advisories", side_effect=AssertionError("read")):
                status, message = authoring_ready(self.artifact(artifact_id), self.root)
                self.assertEqual("pass", status, message)

    def test_a_placeholder_in_a_verification_draft_is_refused_without_reading_an_advisory(self) -> None:
        write(self.product / "verification/VER-002.md", formal("VER-002", "verification", "draft", {"verifies": ["REQ-001"]}) + "\n## Cases\n\n<List the cases>\n")
        with mock.patch.object(validate_engineering_artifacts, "authoring_advisories", side_effect=AssertionError("read")):
            status, message = authoring_ready(self.artifact("VER-002"), self.root)
        self.assertEqual("fail", status)
        self.assertIn("template placeholder", message)

    def test_an_implementation_transition_reads_no_advisory(self) -> None:
        # TCM-RFB-012: no authoring predicate is bound to a target other than approved
        self.requirement(LONG_STATEMENT, status="approved")
        with mock.patch.object(validate_engineering_artifacts, "authoring_advisories", side_effect=AssertionError("read")):
            code, output, error = invoke("check", str(self.root), "--artifact", "REQ-002", "--checkpoint", "transition", "--target", "implemented", "--json")
        result = json.loads(output)
        self.assertIsNone(self.predicate(result, "QGP-G1-AUTHORING"), result["compliance"])
        self.assertIsNone(self.predicate(result, "QGP-G2-AUTHORING"), result["compliance"])

    def test_an_unreadable_validator_is_not_assessable(self) -> None:
        self.requirement(CLEAN_STATEMENT)
        with mock.patch.object(validate_engineering_artifacts, "authoring_advisories", side_effect=RuntimeError("cannot load")):
            status, message = authoring_ready(self.artifact("REQ-002"), self.root)
        self.assertEqual("not_assessable", status)
        self.assertIn("cannot load", message)


class ValidationAndBudgetsUnchangedTests(AuthoringGateFixture):
    """VER-TCM-007 rows 'validation unchanged', 'budgets unchanged', 'one module', 'checklist' (TCM-RFB-007 to TCM-RFB-009, TCM-RFB-011)."""

    def test_validate_keeps_passing_with_advisories_listed_apart(self) -> None:
        self.requirement(LONG_STATEMENT)
        self.intent(LONG_OUTCOME)
        self.capability(NO_UNDER_ABILITY)
        self.specification(LONG_RULES)
        code, output, error = invoke("validate", str(self.root), "--json", "--advisories")
        self.assertEqual(0, code, error)
        report = json.loads(output)
        self.assertEqual(0, report["error_count"] if "error_count" in report else len(report["errors"]))
        self.assertGreaterEqual(report["advisory_count"], 5)
        self.assertEqual(report["advisory_count"], len(report["advisories"]))

    def test_the_budgets_and_codes_of_the_four_families_are_unchanged(self) -> None:
        expected = {
            "AUTHORING_STATEMENT_LIMIT": 30, "AUTHORING_BODY_LIMIT": 250, "AUTHORING_WHY_WORD_LIMIT": 120, "AUTHORING_WHY_SENTENCE_LIMIT": 5,
            "AUTHORING_SENTENCE_LIMIT": 25, "AUTHORING_CODE_IDENTIFIER_LIMIT": 3, "AUTHORING_PLAIN_WORDS_SENTENCE_LIMIT": 2,
            "INTENT_OUTCOME_LIMIT": 30, "INTENT_BODY_LIMIT": 200, "INTENT_PROBLEM_WORD_LIMIT": 120, "INTENT_PROBLEM_SENTENCE_LIMIT": 5, "INTENT_CODE_IDENTIFIER_LIMIT": 2,
            "CAPABILITY_ABILITY_LIMIT": 30, "CAPABILITY_BODY_LIMIT": 150, "CAPABILITY_NEED_WORD_LIMIT": 60, "CAPABILITY_NEED_SENTENCE_LIMIT": 3, "CAPABILITY_CODE_IDENTIFIER_LIMIT": 2,
            "SPECIFICATION_CONTRACT_LIMIT": 30, "SPECIFICATION_RULE_LIMIT": 30, "SPECIFICATION_PROSE_LIMIT": 300,
        }
        self.assertEqual(expected, {name: getattr(validation_authoring, name) for name in expected})
        self.assertEqual([f"W-AUT-{index:03d}" for index in range(1, 24)], [getattr(codes, f"W_AUT_{index:03d}") for index in range(1, 24)])

    def test_the_gate_reads_the_validator_module_and_holds_no_budget(self) -> None:
        # TCM-RFB-007
        source = (REPOSITORY_ROOT / "se_harness/workflow_predicates.py").read_text(encoding="utf-8")
        self.assertIn("validate_engineering_artifacts.authoring_advisories(", source)
        for path in sorted((REPOSITORY_ROOT / "se_harness").glob("*.py")):
            with self.subTest(module=path.name):
                self.assertNotRegex(path.read_text(encoding="utf-8"), r"^(AUTHORING|INTENT|CAPABILITY|SPECIFICATION)_[A-Z_]*LIMIT = ", "a budget constant outside the validator")
        self.assertIs(workflow_predicates.validate_engineering_artifacts, validate_engineering_artifacts)

    def test_the_four_definition_checklists_state_the_gate(self) -> None:
        # TCM-RFB-011
        text = GUIDE.read_text(encoding="utf-8")
        for kind, predicate in (("requirement", "QGP-G1-AUTHORING"), ("intent", "QGP-G1-AUTHORING"), ("capability", "QGP-G1-AUTHORING"), ("specification", "QGP-G2-AUTHORING")):
            with self.subTest(kind=kind):
                section = text.split(f"\n## {kind}\n", 1)[1].split("\n## ", 1)[0]
                self.assertIn("A draft that still draws an advisory is not approved until it is fixed", section)
                self.assertIn(predicate, section)


class CorpusTests(unittest.TestCase):
    """VER-TCM-007 row 'corpus': the packet's own definitions are clean under the gate they built."""

    def test_the_packet_definitions_draw_no_advisory_as_drafts(self) -> None:
        report = validate_engineering_artifacts.validate_repository(REPOSITORY_ROOT)
        for artifact_id in ("REQ-TCM-017", "SPEC-TCM-007"):
            with self.subTest(artifact=artifact_id):
                artifact = next(item for item in report.artifacts if item.artifact_id == artifact_id)
                self.assertEqual([], [(i.code, i.message) for i in validate_engineering_artifacts.authoring_advisories(artifact, REPOSITORY_ROOT)])


if __name__ == "__main__":
    unittest.main()
