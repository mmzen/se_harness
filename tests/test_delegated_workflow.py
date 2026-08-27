from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
import subprocess
import tempfile
import unittest
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from se_harness.cli import main
from se_harness.delegated_authority import DelegatedAuthorityError
from se_harness.delegated_workflow import (
    CompletionProof,
    DelegatedWorkflowError,
    EffectProof,
    LifecycleProof,
    PHASE4_OPERATIONS,
    PROHIBITED_ACTIONS,
    candidate_commit_stop,
    delegated_change_bundle_apply,
    delegated_vrec_prepare,
    delegated_work_order_complete,
    delegated_work_order_start,
    phase4_delegation_policy,
    phase4_operation_catalog,
    refuse_prohibited_action,
)
from se_harness.repository_state import (
    EvaluatorIdentity,
    RepositoryObservationError,
    observe_repository,
    observe_stable_repository,
)
from se_harness.runtime_state import RuntimeStateError, RuntimeStateStore
from se_harness.workflow_contract import (
    ContractError,
    load_validated_contracts,
    validate_contracts,
)
from tests.mutation_guard_support import trusted_mutation_authority
from tests.test_revision_provenance import create_base_chain, formal


EVALUATOR = EvaluatorIdentity(
    package="se-harness",
    version="0.6.0",
    payload_sha256="1" * 64,
    launcher_sha256="2" * 64,
)
PASS_GATE = {
    "id": "QG-G4-CANDIDATE-READY",
    "status": "pass",
    "predicates": [],
}
EVIDENCE = {
    "kind": "verification",
    "path": "docs/evidence.json",
    "sha256": "3" * 64,
}
MODEL_CASES = (
    Path(__file__).resolve().parent
    / "fixtures/agentic_execution/phase4/workflow/model-cases.json"
)


def _git(root: Path, *arguments: str) -> None:
    subprocess.run(
        ["git", "-C", str(root), *arguments],
        check=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _gate(identifier: str) -> dict[str, object]:
    return {"id": identifier, "status": "pass", "predicates": []}


class DelegatedWorkflowContractTests(unittest.TestCase):
    def test_retained_model_fixture_matches_closed_runtime_catalogs(self) -> None:
        fixture = json.loads(MODEL_CASES.read_text(encoding="utf-8"))
        self.assertEqual("se-harness-phase4-workflow-fixtures-v1", fixture["schema"])
        self.assertEqual(
            [
                {
                    "id": item["id"],
                    "decision_right": item["decision_right"],
                    "current_status": item["current_status"],
                    "result_status": item["result_status"],
                }
                for item in phase4_operation_catalog()
            ],
            fixture["advancing_operations"],
        )
        self.assertEqual(sorted(PROHIBITED_ACTIONS), fixture["prohibited_actions"])
        self.assertEqual(
            [
                "altered-receipt-link",
                "direct-unreceipted-write",
                "failed-gate",
                "missing-effect-receipt",
            ],
            fixture["completion_rejections"],
        )

    def test_closed_catalog_maps_exactly_four_operations(self) -> None:
        catalog = phase4_operation_catalog()
        self.assertEqual(PHASE4_OPERATIONS, tuple(item["id"] for item in catalog))
        self.assertEqual(
            (
                ("DR-WO-START", "approved", "in_progress"),
                (None, "in_progress", "in_progress"),
                ("DR-WO-COMPLETE", "in_progress", "implemented"),
                ("DR-VREC-PREPARE", "implemented", "implemented"),
            ),
            tuple(
                (item["decision_right"], item["current_status"], item["result_status"])
                for item in catalog
            ),
        )

    def test_policy_activates_only_three_rights_and_one_logical_writer(self) -> None:
        policy = phase4_delegation_policy()
        self.assertEqual(
            {"DR-WO-START", "DR-WO-COMPLETE", "DR-VREC-PREPARE"},
            set(policy.decision_right_delegators),
        )
        self.assertEqual(set(PHASE4_OPERATIONS), set(policy.operations))
        self.assertEqual({"implementation-worker"}, set(policy.delegates))
        self.assertEqual({"implementer"}, set(policy.execution_profiles))

    def test_operation_right_state_model_has_only_four_advancing_rows(self) -> None:
        catalog = phase4_operation_catalog()
        statuses = ("draft", "approved", "in_progress", "implemented", "verified", "released")
        rights = (None, "DR-WO-START", "DR-WO-COMPLETE", "DR-VREC-PREPARE", "DR-RLS-PREPARE")
        actual = {
            (item["id"], item["decision_right"], item["current_status"])
            for item in catalog
        }
        admitted = {
            (operation, right, status)
            for operation in PHASE4_OPERATIONS
            for right in rights
            for status in statuses
            if (operation, right, status) in actual
        }
        self.assertEqual(actual, admitted)
        self.assertNotIn(("delegated-vrec-prepare", "DR-RLS-PREPARE", "implemented"), admitted)

    def test_contract_rejects_catalog_widening_reordering_right_gate_and_procedure_change(self) -> None:
        workflow, quality, _, _, _ = load_validated_contracts()
        cases = []
        widened = copy.deepcopy(workflow)
        widened["agentic_operations"].append(copy.deepcopy(widened["agentic_operations"][0]))
        cases.append(widened)
        reordered = copy.deepcopy(workflow)
        reordered["agentic_operations"][0], reordered["agentic_operations"][1] = (
            reordered["agentic_operations"][1],
            reordered["agentic_operations"][0],
        )
        cases.append(reordered)
        changed_right = copy.deepcopy(workflow)
        changed_right["agentic_operations"][3]["decision_right"] = "DR-RLS-PREPARE"
        cases.append(changed_right)
        changed_gate = copy.deepcopy(workflow)
        changed_gate["agentic_operations"][0]["gate_ids"] = ["QG-G4-CANDIDATE-READY"]
        cases.append(changed_gate)
        changed_procedure = copy.deepcopy(workflow)
        changed_procedure["agentic_operations"][0]["procedure_id"] = "PROC-WO-IMPLEMENT"
        cases.append(changed_procedure)
        for candidate in cases:
            with self.subTest(candidate=candidate["agentic_operations"]), self.assertRaises(ContractError):
                validate_contracts(candidate, quality)

    def test_candidate_commit_stop_is_lossless_and_has_one_zero_effect_next_action(self) -> None:
        stop = candidate_commit_stop(
            work_order_id="WO-TST-001",
            repository="fixture-repository",
            evaluator=EVALUATOR,
            declared_paths=("docs/",),
            changed_paths=("docs/change.txt",),
            gates=(PASS_GATE,),
            evidence=(EVIDENCE,),
            residual_uncertainty=("Real-world actor identity is not authenticated.",),
        )
        packet = stop.decision_packet.value
        self.assertEqual("DR-EXTERNAL-ACTION", packet["decision"]["kind"])
        self.assertEqual("repository-owner", packet["decision"]["required_accountable_role"])
        self.assertEqual(None, packet["identity"]["candidate_commit"])
        self.assertEqual(
            {"kind": "response", "value": "Authorize creating the exact candidate commit for WO-TST-001."},
            packet["handoff"]["command_or_suggested_response"],
        )
        self.assertIn("does not stage, commit, branch, push, merge, or verify", packet["effect"]["non_effects"][0])
        self.assertEqual(stop.workflow_result["state"]["before"], stop.workflow_result["state"]["after"])

    def test_candidate_commit_stop_rejects_failed_preparation_gate(self) -> None:
        with self.assertRaisesRegex(DelegatedWorkflowError, "AEXFLW006"):
            candidate_commit_stop(
                work_order_id="WO-TST-001",
                repository="fixture-repository",
                evaluator=EVALUATOR,
                declared_paths=("docs/",),
                changed_paths=("docs/change.txt",),
                gates=({"id": "QG-G4-CANDIDATE-READY", "status": "fail", "predicates": []},),
                evidence=(EVIDENCE,),
                residual_uncertainty=(),
            )

    def test_every_prohibited_action_returns_zero_effect_and_one_action_specific_response(self) -> None:
        for action in sorted(PROHIBITED_ACTIONS):
            with self.subTest(action=action):
                stop = refuse_prohibited_action(
                    action,
                    work_order_id="WO-TST-001",
                    repository="fixture-repository",
                    evaluator=EVALUATOR,
                    evidence=(EVIDENCE,),
                )
                result = stop.workflow_result
                self.assertEqual(result["state"]["before"], result["state"]["after"])
                self.assertEqual([], result["mutation"]["writes"])
                response = stop.decision_packet.value["handoff"]["command_or_suggested_response"]
                self.assertEqual("response", response["kind"])
                self.assertIn(action, response["value"])
                self.assertEqual([], stop.decision_packet.value["decision"]["alternatives"])

    def test_cli_catalog_is_machine_readable_and_matches_python_api(self) -> None:
        output = io.StringIO()
        error = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            code = main(["delegated-workflow", "catalog", "--json"])
        self.assertEqual(0, code, error.getvalue())
        self.assertEqual(
            [dict(item) for item in phase4_operation_catalog()],
            json.loads(output.getvalue()),
        )


class DelegatedWorkflowIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.root = self.base / "repository"
        self.root.mkdir()
        output = io.StringIO()
        error = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            code = main(["init", str(self.root), "--project-name", "Delegated Workflow Fixture"])
        self.assertEqual(0, code, error.getvalue())
        create_base_chain(self.root, work_order_status="approved", operating_contract_status="draft")
        work_order = self.root / "docs/engineering/product/work-orders/WO-001.md"
        work_order.write_text(
            formal(
                "WO-001",
                "work_order",
                "approved",
                {
                    "implements": ["REQ-001"],
                    "specifications": ["SPEC-001"],
                    "architecture": ["ARCH-001", "ADR-001"],
                    "verification": ["VER-001"],
                },
                '''[assurance]
commit_bound_verification = "required"
rationale = "Delegated effects and lifecycle transitions require exact-candidate assurance."
decided_by = "repository-owner"

[execution_scope]
paths = [
  "docs/engineering/product/evidence/",
  "docs/engineering/product/verification-records/",
  "docs/engineering/product/work-orders/WO-001.md",
  "src/",
]

[agentic_delegation]
schema = "se-harness-agentic-delegation-v1"
delegated_by = "engineering-owner"
delegate = "implementation-worker"
decision_rights = ["DR-VREC-PREPARE", "DR-WO-COMPLETE", "DR-WO-START"]
operations = [
  "change-bundle-apply",
  "delegated-vrec-prepare",
  "delegated-work-order-complete",
  "delegated-work-order-start",
]
execution_profiles = ["implementer"]
paths = [
  "docs/engineering/product/evidence/",
  "docs/engineering/product/verification-records/",
  "docs/engineering/product/work-orders/WO-001.md",
  "src/",
]
required_evidence = [
  { kind = "verification", path = "docs/engineering/product/evidence/WO-001-verification.md" },
]
valid_until = "2030-01-01T00:00:00Z"
max_retry = 1
max_parallel_writers = 1
child_delegation = false
stop_before = ["accountable-decision-required", "action-time-authorization-required"]''',
            ),
            encoding="utf-8",
            newline="\n",
        )
        _git(self.root, "init")
        _git(self.root, "config", "user.email", "tests@example.invalid")
        _git(self.root, "config", "user.name", "Test Operator")
        _git(self.root, "add", ".")
        _git(self.root, "commit", "-m", "delegated fixture")
        self.runtime_store = RuntimeStateStore(self.base / "runtime", self.root)
        self.open_session = None
        self.addCleanup(self._close_open_session)
        self.evaluator = EvaluatorIdentity("se-harness", "0.7.0", "4" * 64, "5" * 64)
        self.now = lambda: datetime(2026, 8, 25, 10, 0, tzinfo=UTC)
        authority = mock.patch(
            "se_harness.mutation_guard.require_mutation_authority",
            side_effect=trusted_mutation_authority,
        )
        authority.start()
        self.addCleanup(authority.stop)
        preflight = mock.patch(
            "se_harness.workflow.run_preflight",
            return_value=SimpleNamespace(ready=True, diagnostics=[]),
        )
        preflight.start()
        self.addCleanup(preflight.stop)

    def _close_open_session(self) -> None:
        if self.open_session is not None:
            try:
                self.runtime_store.close_session(self.open_session)
            except Exception:
                pass
            self.open_session = None

    def test_start_denials_have_zero_lifecycle_effect(self) -> None:
        work_order = self.root / "docs/engineering/product/work-orders/WO-001.md"
        before = work_order.read_bytes()
        failed_gate = {"id": "QG-G3-WORK-AUTHORIZATION", "status": "fail", "predicates": []}
        with self.assertRaisesRegex(DelegatedWorkflowError, "AEXFLW006"):
            delegated_work_order_start(
                self.root,
                work_order_id="WO-001",
                delegate="implementation-worker",
                execution_profile="implementer",
                gates=(failed_gate,),
                evaluator=self.evaluator,
                runtime_store=self.runtime_store,
                now=self.now,
                authority_guard=trusted_mutation_authority,
            )
        self.assertEqual(before, work_order.read_bytes())

        with self.assertRaisesRegex(DelegatedAuthorityError, "AEXAUTH004"):
            delegated_work_order_start(
                self.root,
                work_order_id="WO-001",
                delegate="foreign-worker",
                execution_profile="implementer",
                gates=(_gate("QG-G3-WORK-AUTHORIZATION"),),
                evaluator=self.evaluator,
                runtime_store=self.runtime_store,
                now=self.now,
                authority_guard=trusted_mutation_authority,
            )
        self.assertEqual(before, work_order.read_bytes())

        self.root.joinpath("unexplained.txt").write_text("dirty\n", encoding="utf-8")
        with self.assertRaisesRegex(DelegatedAuthorityError, "AEXAUTH015"):
            delegated_work_order_start(
                self.root,
                work_order_id="WO-001",
                delegate="implementation-worker",
                execution_profile="implementer",
                gates=(_gate("QG-G3-WORK-AUTHORIZATION"),),
                evaluator=self.evaluator,
                runtime_store=self.runtime_store,
                now=self.now,
                authority_guard=trusted_mutation_authority,
            )
        self.assertEqual(before, work_order.read_bytes())

    def test_unproven_post_transition_state_sets_recovery_block(self) -> None:
        calls = 0

        def failing_after_transition(*args, **kwargs):
            nonlocal calls
            calls += 1
            if calls == 1:
                return observe_stable_repository(*args, **kwargs)
            raise RepositoryObservationError("AEXOBS004", "injected post-transition failure")

        with self.assertRaisesRegex(RepositoryObservationError, "AEXOBS004"):
            delegated_work_order_start(
                self.root,
                work_order_id="WO-001",
                delegate="implementation-worker",
                execution_profile="implementer",
                gates=(_gate("QG-G3-WORK-AUTHORIZATION"),),
                evaluator=self.evaluator,
                runtime_store=self.runtime_store,
                now=self.now,
                observer=failing_after_transition,
                authority_guard=trusted_mutation_authority,
            )
        live = observe_repository(
            self.root,
            work_order_id="WO-001",
            evaluator=self.evaluator,
        )
        self.assertEqual("in_progress", live.value["governance"]["work_order_status"])
        with self.assertRaisesRegex(RuntimeStateError, "AEXRT006"):
            self.runtime_store.start_session(
                live.value["repository"],
                "implementation-worker",
                started_at="2026-08-25T10:01:00Z",
            )

    def _run_to_completion(self, *, proof_mutator=None, before_completion=None):
        start = delegated_work_order_start(
            self.root,
            work_order_id="WO-001",
            delegate="implementation-worker",
            execution_profile="implementer",
            gates=(_gate("QG-G3-WORK-AUTHORIZATION"),),
            evaluator=self.evaluator,
            runtime_store=self.runtime_store,
            now=self.now,
            authority_guard=trusted_mutation_authority,
        )
        self.assertIsNotNone(start.session)
        self.open_session = start.session
        baseline = self.base / "baseline"
        proposed = self.base / "proposed"
        baseline.mkdir()
        proposed.joinpath("src").mkdir(parents=True)
        proposed.joinpath("src/value.txt").write_text(
            "phase-4\n", encoding="utf-8", newline="\n"
        )
        evidence_path = "docs/engineering/product/evidence/WO-001-verification.md"
        evidence = {
            "kind": "verification",
            "path": evidence_path,
            "sha256": hashlib.sha256((self.root / evidence_path).read_bytes()).hexdigest(),
        }
        effect = delegated_change_bundle_apply(
            self.root,
            work_order_id="WO-001",
            delegate="implementation-worker",
            execution_profile="implementer",
            requested_paths=("src/value.txt",),
            baseline_workspace=baseline,
            proposed_workspace=proposed,
            object_store=self.base / "objects",
            intended_deletions=(),
            previous_receipt_sha256=start.receipt.sha256,
            gates=(_gate("QG-G4-IMPLEMENTATION-EVIDENCE"),),
            evidence=(evidence,),
            deviations=(),
            evaluator=self.evaluator,
            runtime_store=self.runtime_store,
            session=start.session,
            now=self.now,
            authority_guard=trusted_mutation_authority,
        )
        test_result = {
            "id": "unit-tests",
            "status": "passed",
            "exit_code": 0,
            "arguments_sha256": "6" * 64,
            "output_sha256": "7" * 64,
            "evidence_path": evidence_path,
        }
        proof = CompletionProof(
            start=LifecycleProof(
                start.receipt,
                start.envelope,
                start.before_observation,
                start.after_observation,
            ),
            effects=(
                EffectProof(
                    effect.result.receipt,
                    effect.before_observation,
                    effect.after_observation,
                ),
            ),
            changed_paths=("src/value.txt",),
            tests=(test_result,),
            gates=(_gate("QG-G4-IMPLEMENTATION-EVIDENCE"),),
            evidence=(evidence,),
            deviations=(),
            residual_uncertainty=(
                "The fixture does not authenticate the real-world actor.",
            ),
        )
        if before_completion is not None:
            before_completion()
        if proof_mutator is not None:
            proof = proof_mutator(proof)
        completion = delegated_work_order_complete(
            self.root,
            work_order_id="WO-001",
            delegate="implementation-worker",
            execution_profile="implementer",
            proof=proof,
            evaluator=self.evaluator,
            runtime_store=self.runtime_store,
            session=start.session,
            now=self.now,
            authority_guard=trusted_mutation_authority,
        )
        self.open_session = None
        return start, effect, completion

    def test_completion_rejects_missing_effect_receipt(self) -> None:
        with self.assertRaisesRegex(DelegatedWorkflowError, "AEXFLW004"):
            self._run_to_completion(
                proof_mutator=lambda proof: replace(proof, effects=()),
            )

    def test_completion_rejects_altered_receipt_link(self) -> None:
        def alter(proof):
            receipt = copy.deepcopy(proof.effects[0].receipt.value)
            receipt["state"]["previous_receipt_sha256"] = "f" * 64
            effect = proof.effects[0]
            return replace(
                proof,
                effects=(EffectProof(receipt, effect.before_observation, effect.after_observation),),
            )

        with self.assertRaisesRegex(DelegatedWorkflowError, "AEXFLW004"):
            self._run_to_completion(proof_mutator=alter)

    def test_completion_rejects_failed_gate(self) -> None:
        failed = {"id": "QG-G4-IMPLEMENTATION-EVIDENCE", "status": "fail", "predicates": []}
        with self.assertRaisesRegex(DelegatedWorkflowError, "AEXFLW006"):
            self._run_to_completion(
                proof_mutator=lambda proof: replace(proof, gates=(failed,)),
            )

    def test_completion_rejects_direct_unreceipted_write(self) -> None:
        def direct_write() -> None:
            self.root.joinpath("src/direct.txt").write_text("unreceipted\n", encoding="utf-8")

        with self.assertRaisesRegex(DelegatedWorkflowError, "AEXFLW004"):
            self._run_to_completion(before_completion=direct_write)

    def test_sequential_start_effect_completion_and_git_stop(self) -> None:
        start, effect, completion = self._run_to_completion()
        self.assertEqual(
            "approved", start.before_observation.value["governance"]["work_order_status"]
        )
        self.assertEqual(
            "in_progress", effect.before_observation.value["governance"]["work_order_status"]
        )
        self.assertEqual(
            "implemented", completion.after_observation.value["governance"]["work_order_status"]
        )
        self.assertEqual(
            ["docs/engineering/product/work-orders/WO-001.md", "src/value.txt"],
            completion.receipt.value["effects"]["changed_paths"],
        )
        stop = delegated_vrec_prepare(
            self.root,
            work_order_id="WO-001",
            record_id="VREC-001",
            verification_ids=("VER-001",),
            evidence_paths=("docs/engineering/product/evidence/WO-001-verification.md",),
            owner="quality-owner",
            output="docs/engineering/product/verification-records/VREC-001.md",
            domain="product",
            delegate="implementation-worker",
            execution_profile="implementer",
            gates=(_gate("QG-G4-CANDIDATE-READY"),),
            completion_proof=LifecycleProof(
                completion.receipt,
                completion.envelope,
                completion.before_observation,
                completion.after_observation,
            ),
            evaluator=self.evaluator,
            runtime_store=self.runtime_store,
            now=self.now,
            authority_guard=trusted_mutation_authority,
        )
        self.assertEqual("candidate commit is required", stop.reason)
        self.assertEqual([], stop.workflow_result["mutation"]["writes"])

    def test_altered_completion_observation_is_rejected_before_vrec_effect(self) -> None:
        _, _, completion = self._run_to_completion()
        altered = copy.deepcopy(completion.after_observation.value)
        altered["filesystem"]["regular_file_manifest_sha256"] = "f" * 64
        with self.assertRaisesRegex(DelegatedWorkflowError, "AEXFLW004"):
            delegated_vrec_prepare(
                self.root,
                work_order_id="WO-001",
                record_id="VREC-001",
                verification_ids=("VER-001",),
                evidence_paths=("docs/engineering/product/evidence/WO-001-verification.md",),
                owner="quality-owner",
                output="docs/engineering/product/verification-records/VREC-001.md",
                domain="product",
                delegate="implementation-worker",
                execution_profile="implementer",
                gates=(_gate("QG-G4-CANDIDATE-READY"),),
                completion_proof=LifecycleProof(
                    completion.receipt,
                    completion.envelope,
                    completion.before_observation,
                    altered,
                ),
                evaluator=self.evaluator,
                runtime_store=self.runtime_store,
                now=self.now,
                authority_guard=trusted_mutation_authority,
            )
        self.assertFalse(
            (self.root / "docs/engineering/product/verification-records/VREC-001.md").exists()
        )

    def test_separately_committed_candidate_prepares_undecided_ready_vrec(self) -> None:
        _, _, completion = self._run_to_completion()
        _git(self.root, "add", ".")
        _git(self.root, "commit", "-m", "candidate")
        result = delegated_vrec_prepare(
            self.root,
            work_order_id="WO-001",
            record_id="VREC-001",
            verification_ids=("VER-001",),
            evidence_paths=("docs/engineering/product/evidence/WO-001-verification.md",),
            owner="quality-owner",
            output="docs/engineering/product/verification-records/VREC-001.md",
            domain="product",
            delegate="implementation-worker",
            execution_profile="implementer",
            gates=(_gate("QG-G4-CANDIDATE-READY"),),
            completion_proof=LifecycleProof(
                completion.receipt,
                completion.envelope,
                completion.before_observation,
                completion.after_observation,
            ),
            evaluator=self.evaluator,
            runtime_store=self.runtime_store,
            now=self.now,
            authority_guard=trusted_mutation_authority,
        )
        record = result.record_path.read_text(encoding="utf-8")
        self.assertIn('status = "ready"', record)
        self.assertIn('prepared_by = "quality-owner"', record)
        self.assertNotIn("verified_at", record)
        self.assertNotIn("verified_by", record)
        self.assertEqual("DR-VREC-DECIDE", result.decision_packet.value["decision"]["kind"])
        self.assertEqual(
            [
                "docs/engineering/product/evidence/VREC-001-evaluator.json",
                "docs/engineering/product/verification-records/VREC-001.md",
            ],
            result.receipt.value["effects"]["changed_paths"],
        )


if __name__ == "__main__":
    unittest.main()
