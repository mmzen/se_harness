"""Approval checks content and decisions, without policing writing style (WO-KIS-001)."""

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


class SimpleAuthoringTests(AuthoringGateFixture):
    def test_ordinary_prose_is_approvable_for_all_four_definitions(self) -> None:
        self.requirement("The command returns the reading manifest.")
        self.intent(LONG_OUTCOME)
        self.capability(NO_UNDER_ABILITY)
        self.specification(LONG_RULES)
        for artifact_id in ("REQ-002", "INT-002", "CAP-002", "SPEC-002"):
            with self.subTest(artifact=artifact_id):
                code, result = self.transition(artifact_id, "approved")
                self.assertEqual(0, code, result)

    def test_missing_acceptance_and_unfinished_content_still_refuse(self) -> None:
        self.requirement("The command returns the reading manifest.", body="")
        artifact = self.artifact("REQ-002")
        self.assertEqual("fail", authoring_ready(artifact, self.root)[0])
        self.requirement("The command returns <fill in the result>.")
        code, result = self.transition("REQ-002", "approved")
        self.assertEqual(1, code, result)
        self.assertIn("placeholder", str(result))

    def test_linked_verification_can_supply_the_acceptance_condition(self) -> None:
        self.requirement("The command returns the reading manifest.", body="")
        write(self.product / "verification/VER-001.md", formal("VER-001", "verification", "approved", {"verifies": ["REQ-001", "REQ-002"]}) + "\nRun the command and compare its returned paths with the work order's required inputs.\n")
        code, result = self.transition("REQ-002", "approved")
        self.assertEqual(0, code, result)

    def test_optional_hint_does_not_block_owner_approval(self) -> None:
        path = self.intent(CLEAN_OUTCOME)
        path.write_text(path.read_text(encoding="utf-8").replace(f'outcome = "{CLEAN_OUTCOME}"\n', ''), encoding="utf-8")
        self.assertIn(codes.W_AUT_011, [i.code for i in self.report().advisories])
        code, result = self.transition("INT-002", "approved")
        self.assertEqual(0, code, result)

    def test_duplicate_rule_reference_is_a_hint(self) -> None:
        self.specification(SHORT_RULES + SHORT_RULES)
        self.assertIn(codes.W_AUT_020, [i.code for i in self.report().advisories])
        code, result = self.transition("SPEC-002", "approved")
        self.assertEqual(0, code, result)
