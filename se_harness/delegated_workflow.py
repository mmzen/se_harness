"""Delegated Phase 4 workflow coordination under exact evaluator authority.

The coordinator composes the existing observer, delegation resolver, nonce
ledger, effect broker, lifecycle engine, provenance preparation, receipt
validator, and decision-packet projector.  It owns no authority schema and
performs no Git, network, credential, release, or external action.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import tomllib
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence

from se_harness import mutation_guard
from se_harness.agent_contract import (
    AUTONOMY_ENVELOPE_V2_SCHEMA,
    PACKET_CONTEXT_SCHEMA,
    REPOSITORY_OBSERVATION_SCHEMA,
    ContractDocument,
    canonical_json_bytes,
    project_decision_packet,
    validate_portable_path,
    validate_contract,
    validate_execution_receipt,
)
from se_harness.delegated_authority import (
    AuthorityRequest,
    DelegationPolicy,
    EnvelopeDerivation,
    ResolvedDelegation,
    admit_fresh_envelope,
    derive_autonomy_envelope_v2,
    resolve_delegation,
)
from se_harness.change_bundle import BundleConstruction, construct_change_bundle
from se_harness.effect_broker import (
    EffectReceipt,
    EffectResult,
    apply_change_bundle,
    validate_effect_receipt,
)
from se_harness.installer import HarnessError, ensure_target
from se_harness.provenance import capture_verification, git_identity, require_clean_worktree
from se_harness.repository_state import (
    EvaluatorIdentity,
    StableRepositoryObservation,
    observe_repository,
    observe_stable_repository,
)
from se_harness.runtime_state import RuntimeSession, RuntimeStateStore
from se_harness.workflow import plan_transition
from se_harness.workflow_compliance import focus_schema2
from se_harness.workflow_contract import load_validated_contracts
from se_harness.workflow_result import build_result


START_OPERATION = "delegated-work-order-start"
EFFECT_OPERATION = "change-bundle-apply"
COMPLETE_OPERATION = "delegated-work-order-complete"
PREPARE_OPERATION = "delegated-vrec-prepare"
PHASE4_OPERATIONS = (
    START_OPERATION,
    EFFECT_OPERATION,
    COMPLETE_OPERATION,
    PREPARE_OPERATION,
)
PROHIBITED_ACTIONS = frozenset(
    {
        "approval",
        "assurance-decision",
        "child-agent",
        "child-delegation",
        "credential",
        "deploy",
        "external-action",
        "git",
        "merge",
        "network",
        "parallel-writer",
        "publish",
        "release",
    }
)


class DelegatedWorkflowError(RuntimeError):
    """A stable, bounded delegated-workflow diagnostic."""

    def __init__(self, code: str, message: str) -> None:
        text = "".join(character if character >= " " else "?" for character in str(message))[:512]
        super().__init__(f"{code}: {text or 'delegated workflow rejected'}")
        self.code = code
        self.message = text


@dataclass(frozen=True)
class EffectProof:
    """One effect receipt plus the exact before/after observer documents it binds."""

    receipt: EffectReceipt | Mapping[str, Any]
    before_observation: ContractDocument
    after_observation: ContractDocument


@dataclass(frozen=True)
class LifecycleProof:
    """One lifecycle receipt and the exact authority/state documents it binds."""

    receipt: ContractDocument | Mapping[str, Any]
    envelope: ContractDocument | Mapping[str, Any]
    before_observation: ContractDocument | Mapping[str, Any]
    after_observation: ContractDocument | Mapping[str, Any]


@dataclass(frozen=True)
class CompletionProof:
    """Positive, explicit inputs required before delegated completion."""

    start: LifecycleProof
    effects: tuple[EffectProof, ...]
    changed_paths: tuple[str, ...]
    tests: tuple[Mapping[str, Any], ...]
    gates: tuple[Mapping[str, Any], ...]
    evidence: tuple[Mapping[str, str], ...]
    deviations: tuple[Mapping[str, Any], ...]
    residual_uncertainty: tuple[str, ...]


@dataclass(frozen=True)
class DelegatedLifecycleResult:
    operation: str
    workflow_result: Mapping[str, Any]
    receipt: ContractDocument
    envelope: ContractDocument
    before_observation: ContractDocument
    after_observation: ContractDocument
    session: RuntimeSession | None


@dataclass(frozen=True)
class DelegatedEffectResult:
    operation: str
    result: EffectResult
    bundle: BundleConstruction
    envelope: ContractDocument
    before_observation: ContractDocument
    after_observation: ContractDocument


@dataclass(frozen=True)
class DelegatedPreparationResult:
    operation: str
    workflow_result: Mapping[str, Any]
    receipt: ContractDocument
    decision_packet: ContractDocument
    record_path: Path


@dataclass(frozen=True)
class DelegatedStop:
    operation: str
    reason: str
    workflow_result: Mapping[str, Any]
    decision_packet: ContractDocument


Observer = Callable[..., StableRepositoryObservation]
AuthorityGuard = Callable[..., Any]


def _error(code: str, message: str) -> None:
    raise DelegatedWorkflowError(code, message)


def phase4_operation_catalog() -> tuple[Mapping[str, Any], ...]:
    """Return the validated, closed workflow-v4 operation catalog."""

    workflow, _, _, _, _ = load_validated_contracts()
    operations = tuple(dict(item) for item in workflow["agentic_operations"])
    if tuple(item["id"] for item in operations) != PHASE4_OPERATIONS:
        _error("AEXFLW001", "managed Phase 4 operation catalog differs from the closed catalog")
    return operations


def phase4_delegation_policy() -> DelegationPolicy:
    """Build the closed evaluator policy used to resolve formal declarations."""

    operations = phase4_operation_catalog()
    return DelegationPolicy(
        decision_right_delegators={
            "DR-WO-START": frozenset({"engineering-owner"}),
            "DR-WO-COMPLETE": frozenset({"engineering-owner"}),
            "DR-VREC-PREPARE": frozenset({"engineering-owner"}),
        },
        operations=frozenset(item["id"] for item in operations),
        execution_profiles=frozenset({"implementer"}),
        delegates=frozenset({"implementation-worker"}),
        operation_statuses={
            item["id"]: frozenset({item["current_status"]}) for item in operations
        },
    )


def _work_order(root: Path, work_order_id: str) -> tuple[Path, str, bytes]:
    candidates = sorted(
        (
            path
            for path in (root / "docs" / "engineering").rglob(f"{work_order_id}.md")
            if path.is_file()
        ),
        key=lambda item: item.as_posix(),
    )
    if len(candidates) != 1:
        _error("AEXFLW002", "selected work order is missing or ambiguous")
    path = candidates[0]
    try:
        raw = path.read_bytes()
    except OSError as exc:
        _error("AEXFLW002", f"cannot read selected work order: {exc}")
    return path, path.relative_to(root).as_posix(), raw


def _front_matter(raw: bytes) -> Mapping[str, Any]:
    try:
        text = raw.decode("utf-8")
        closing = text.index("\n+++\n", 4)
        value = tomllib.loads(text[4:closing])
    except (UnicodeError, ValueError, tomllib.TOMLDecodeError) as exc:
        _error("AEXFLW002", f"cannot parse work-order metadata: {exc}")
    if not isinstance(value, Mapping):
        _error("AEXFLW002", "work-order metadata is not an object")
    return value


def _required_evidence(delegation: ResolvedDelegation) -> tuple[tuple[str, str], ...]:
    return tuple(
        (item["kind"], item["path"])
        for item in delegation.document.value["required_evidence"]
    )


def _gates_pass(gates: Sequence[Mapping[str, Any]], required: Sequence[str]) -> bool:
    by_id: dict[str, Mapping[str, Any]] = {}
    for gate in gates:
        identifier = gate.get("id")
        if not isinstance(identifier, str) or identifier in by_id:
            _error("AEXFLW006", "gate results contain a missing or duplicate identity")
        if gate.get("status") != "pass":
            return False
        predicates = gate.get("predicates", [])
        if not isinstance(predicates, list) or any(
            not isinstance(item, Mapping) or item.get("status") != "pass"
            for item in predicates
        ):
            return False
        by_id[identifier] = gate
    return bool(required) and set(required).issubset(by_id)


def _operation(operation: str) -> Mapping[str, Any]:
    matches = [item for item in phase4_operation_catalog() if item["id"] == operation]
    if len(matches) != 1:
        _error("AEXFLW001", f"operation is not activated: {operation}")
    return matches[0]


def _changed_paths(root: Path) -> tuple[str, ...]:
    commands = (
        ("git", "diff", "--name-only", "-z", "HEAD", "--"),
        ("git", "ls-files", "--others", "--exclude-standard", "-z"),
    )
    observed: set[str] = set()
    for command in commands:
        try:
            result = subprocess.run(
                command,
                cwd=root,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
                shell=False,
            )
        except OSError as exc:
            _error("AEXFLW003", f"cannot inspect Git changed paths: {exc}")
        if result.returncode != 0 or len(result.stdout) > 67_108_864:
            _error("AEXFLW003", "Git changed-path inspection failed or exceeded its bound")
        for raw in result.stdout.split(b"\0"):
            if not raw:
                continue
            try:
                observed.add(validate_portable_path(raw.decode("utf-8")))
            except (UnicodeError, ValueError) as exc:
                _error("AEXFLW003", f"Git returned an invalid changed path: {exc}")
    return tuple(sorted(observed, key=lambda item: item.encode("utf-8")))


def _observation_core(document: ContractDocument) -> bytes:
    value = dict(document.value)
    value.pop("previous_receipt_sha256", None)
    return canonical_json_bytes(value)


def _ensure_same_live_state(left: ContractDocument, right: ContractDocument, label: str) -> None:
    if _observation_core(left) != _observation_core(right):
        _error("AEXFLW004", f"repository-state discontinuity at {label}")


def _ensure_same_candidate_content(
    historical: ContractDocument,
    current: ContractDocument,
    label: str,
) -> None:
    """Allow only the Git identity change introduced by an exact clean commit."""

    left = historical.value
    right = current.value
    for key in ("repository", "evaluator", "governance", "filesystem"):
        if left[key] != right[key]:
            _error("AEXFLW004", f"candidate content discontinuity at {label}: {key}")


def _guard_evaluator(guarded: Any, evaluator: EvaluatorIdentity) -> None:
    """Cross-check caller-supplied observer identity with the proven runtime."""

    identity = getattr(guarded, "identity", None)
    if identity is None:
        return
    guarded_version = getattr(identity, "harness_version", None)
    guarded_payload = getattr(identity, "evaluator_payload_sha256", None)
    guarded_launcher = getattr(identity, "python_binary_sha256", None)
    if (
        evaluator.package != "se-harness"
        or (guarded_version is not None and guarded_version != evaluator.version)
        or (guarded_payload is not None and guarded_payload != evaluator.payload_sha256)
        or (guarded_launcher is not None and guarded_launcher != evaluator.launcher_sha256)
    ):
        _error("AEXFLW005", "mutation guard and supplied evaluator identities differ")


def _authorize(
    root: Path,
    *,
    operation: str,
    work_order_id: str,
    delegate: str,
    execution_profile: str,
    paths: tuple[str, ...],
    gates: Sequence[Mapping[str, Any]],
    evaluator: EvaluatorIdentity,
    previous_receipt_sha256: str | None,
    retry_ordinal: int,
    observer: Observer,
    authority_guard: AuthorityGuard,
    now: Callable[[], datetime],
) -> tuple[ResolvedDelegation, StableRepositoryObservation, EnvelopeDerivation, str]:
    row = _operation(operation)
    guarded = authority_guard(root, operation=operation)
    _guard_evaluator(guarded, evaluator)
    _, work_order_path, raw = _work_order(root, work_order_id)
    delegation = resolve_delegation(raw, phase4_delegation_policy())
    required = tuple(row["gate_ids"])
    if not _gates_pass(gates, required):
        _error("AEXFLW006", "required current gates did not all pass")
    stable = observer(
        root,
        work_order_id=work_order_id,
        evaluator=evaluator,
        previous_receipt_sha256=previous_receipt_sha256,
    )
    required_evidence = _required_evidence(delegation)
    authorization_paths = tuple(
        sorted(
            {*paths, *(path for _, path in required_evidence)},
            key=lambda item: item.encode("utf-8"),
        )
    )
    request = AuthorityRequest(
        operation=operation,
        decision_right=row["decision_right"],
        delegate=delegate,
        execution_profile=execution_profile,
        paths=authorization_paths,
        required_evidence=required_evidence,
        retry_ordinal=retry_ordinal,
    )
    derivation = derive_autonomy_envelope_v2(
        stable_observation=stable,
        delegation=delegation,
        policy=phase4_delegation_policy(),
        request=request,
        issued_at=now().astimezone(UTC),
        gates_passed=True,
    )
    return delegation, stable, derivation, work_order_path


def _close_failed_session(
    runtime_store: RuntimeStateStore,
    session: RuntimeSession,
    *,
    nonce: str,
    recovery_required: bool,
) -> None:
    """Retain a consumed terminal result and block after an unproven mutation."""

    try:
        if recovery_required:
            runtime_store.mark_recovery_required(
                session,
                "delegated workflow could not prove canonical state after mutation",
            )
            runtime_store.record_terminal(
                session,
                nonce=nonce,
                outcome="recovery-required",
            )
        else:
            runtime_store.record_terminal(
                session,
                nonce=nonce,
                outcome="failed-consumed",
            )
    except Exception:
        pass
    try:
        runtime_store.close_session(session)
    except Exception:
        pass


def _evaluator_receipt_identity(evaluator: EvaluatorIdentity) -> Mapping[str, str]:
    return {
        "identity": evaluator.package,
        "version": evaluator.version,
        "payload_sha256": evaluator.payload_sha256,
    }


def _operation_entry(
    operation: str,
    arguments: Mapping[str, Any],
    output_sha256: str,
    evidence_path: str,
) -> Mapping[str, Any]:
    return {
        "id": operation,
        "status": "passed",
        "exit_code": 0,
        "arguments_sha256": hashlib.sha256(canonical_json_bytes(arguments)).hexdigest(),
        "output_sha256": output_sha256,
        "evidence_path": evidence_path,
    }


def _lifecycle_receipt(
    *,
    operation: str,
    work_order_id: str,
    repository_id: str,
    envelope: ContractDocument,
    execution_profile: str,
    before_sha256: str,
    after_sha256: str,
    changed_paths: Iterable[str],
    evidence: Sequence[Mapping[str, str]],
    gates: Sequence[Mapping[str, Any]],
    deviations: Sequence[Mapping[str, Any]],
    residual_uncertainty: Sequence[str],
    evaluator: EvaluatorIdentity,
    arguments: Mapping[str, Any],
    additional_operations: Sequence[Mapping[str, Any]] = (),
) -> ContractDocument:
    retained = [dict(item) for item in evidence]
    if not retained:
        _error("AEXFLW007", "lifecycle receipt requires retained evidence")
    operation_rows = [
        _operation_entry(
            operation,
            arguments,
            after_sha256,
            retained[0]["path"],
        ),
        *[dict(item) for item in additional_operations],
    ]
    receipt = {
        "schema": "se-harness-execution-receipt-v1",
        "selection": {
            "repository": repository_id,
            "artifact": work_order_id,
            "autonomy_envelope_sha256": envelope.sha256,
        },
        "execution": {
            "profiles": [execution_profile],
            "skills": [],
            "operations": operation_rows,
            "worker_results": [],
        },
        "effects": {
            "changed_paths": list(changed_paths),
            "evidence": retained,
            "state_before": [{"kind": "repository-state", "sha256": before_sha256}],
            "state_after": [{"kind": "repository-state", "sha256": after_sha256}],
        },
        "validation": {
            "evaluator": _evaluator_receipt_identity(evaluator),
            "gates": [dict(item) for item in gates],
            "outcome": "completed",
            "deviations": [dict(item) for item in deviations],
            "residual_uncertainty": list(residual_uncertainty),
        },
    }
    return validate_execution_receipt(receipt)


def _transition_result(
    *,
    operation: str,
    work_order_id: str,
    before_status: str,
    after_status: str,
    declared_paths: Iterable[str],
    changed_paths: Iterable[str],
    gates: Sequence[Mapping[str, Any]],
    next_procedure: str,
    next_step: str,
    next_action: str,
    decision_required: Mapping[str, Any] | None,
    command_or_response: Mapping[str, Any],
) -> Mapping[str, Any]:
    step = _managed_step(next_procedure, next_step, work_order_id)
    return build_result(
        operation=operation,
        outcome="completed",
        primary=work_order_id,
        artifacts=[work_order_id],
        governing=[],
        dependencies=[],
        declared_paths=declared_paths,
        changed_paths=changed_paths,
        change_set_complete=True,
        compliance={
            "checkpoint": "handoff",
            "workflow_rule_id": "WFL-WO-IMPLEMENT" if after_status == "implemented" else "WFL-WO-START",
            "procedure_id": next_procedure,
            "status": "pass",
            "gates": [dict(item) for item in gates],
        },
        procedure={
            "id": next_procedure,
            "current_step": next_step,
            "steps": [step],
        },
        restitution={
            "outcome": "completed",
            "done": [f"{operation} changed {work_order_id} from {before_status} to {after_status}."],
            "not_done": [],
            "blocked_by": [],
            "current_lifecycle_state": [f"{work_order_id} is {after_status}."],
            "decision_required": None if decision_required is None else dict(decision_required),
            "next": {
                "procedure_id": next_procedure,
                "step_id": next_step,
                "action": next_action,
            },
            "command_or_response": dict(command_or_response),
            "alternatives": [],
        },
        before=[{"id": work_order_id, "status": before_status}],
        after=[{"id": work_order_id, "status": after_status}],
        writes=[{"id": work_order_id, "fields": ["status", "updated", "lifecycle_events"]}],
    )


def _managed_step(procedure_id: str, step_id: str, artifact_id: str) -> Mapping[str, Any]:
    workflow, _, _, _, _ = load_validated_contracts()
    procedures = [item for item in workflow["procedures"] if item["id"] == procedure_id]
    if len(procedures) != 1:
        _error("AEXFLW011", f"managed procedure is missing or ambiguous: {procedure_id}")
    steps = [item for item in procedures[0]["steps"] if item["id"] == step_id]
    if len(steps) != 1:
        _error("AEXFLW011", f"managed procedure step is missing or ambiguous: {step_id}")
    return _format_artifact(steps[0], artifact_id)


def _packet_context(
    *,
    repository: str,
    candidate_commit: str | None,
    evaluator: EvaluatorIdentity,
    evidence: Sequence[Mapping[str, str]],
    residual_uncertainty: Sequence[str],
    preview: Mapping[str, Any] | None = None,
    alternatives: Sequence[Mapping[str, Any]] = (),
) -> Mapping[str, Any]:
    return {
        "schema": PACKET_CONTEXT_SCHEMA,
        "repository": repository,
        "candidate_commit": candidate_commit,
        "evaluator_payload_sha256": evaluator.payload_sha256,
        "evidence": [dict(item) for item in evidence],
        "assumptions": ["The exact released evaluator supplied the current repository observation."],
        "residual_uncertainty": list(residual_uncertainty),
        "preview": dict(
            preview
            or {
                "kind": "none",
                "artifact": None,
                "from_status": None,
                "to_status": None,
                "action": None,
                "target": None,
            }
        ),
        "alternatives": [dict(item) for item in alternatives],
        "safe_to_defer": True,
    }


def _format_artifact(value: Any, artifact_id: str) -> Any:
    if isinstance(value, str):
        return value.replace("{artifact_id}", artifact_id)
    if isinstance(value, list):
        return [_format_artifact(item, artifact_id) for item in value]
    if isinstance(value, Mapping):
        return {key: _format_artifact(item, artifact_id) for key, item in value.items()}
    return value


def _packet_alternatives(workflow_result: Mapping[str, Any]) -> tuple[Mapping[str, Any], ...]:
    """Expand schema-2 alternative summaries from authoritative procedures."""

    summaries = workflow_result["restitution"]["alternatives"]
    if not summaries:
        return ()
    workflow, _, _, _, _ = load_validated_contracts()
    rule_id = workflow_result["compliance"]["workflow_rule_id"]
    rules = [item for item in workflow["recommendations"] if item["id"] == rule_id]
    if len(rules) != 1:
        _error("AEXFLW011", "workflow result has no unique managed alternative rule")
    procedure_ids = rules[0]["alternative_procedure_ids"]
    if len(procedure_ids) != len(summaries):
        _error("AEXFLW011", "workflow alternative summaries and procedures differ")
    procedures = {item["id"]: item for item in workflow["procedures"]}
    artifact_id = workflow_result["selection"]["primary"]
    alternatives: list[Mapping[str, Any]] = []
    for summary, procedure_id in zip(summaries, procedure_ids, strict=True):
        procedure = procedures.get(procedure_id)
        if not isinstance(procedure, Mapping) or len(procedure["steps"]) != 1:
            _error("AEXFLW011", "workflow alternative procedure is missing or ambiguous")
        step = _format_artifact(procedure["steps"][0], artifact_id)
        if step.get("kind") != "decision" or not isinstance(step.get("response"), str):
            _error("AEXFLW011", "workflow alternative is not a complete decision step")
        alternatives.append(
            {
                "summary": summary,
                "procedure_id": procedure_id,
                "decision_right": step["decision_right"],
                "subject": step["artifact"],
                "required_accountable_role": step["role"],
                "recommendation": step["decision"],
                "command_or_suggested_response": {
                    "kind": "response",
                    "value": step["response"],
                },
                "effects": step["effects"],
                "non_effects": step["non_effects"],
            }
        )
    return tuple(alternatives)


def candidate_commit_stop(
    *,
    work_order_id: str,
    repository: str,
    evaluator: EvaluatorIdentity,
    declared_paths: Iterable[str],
    changed_paths: Iterable[str],
    gates: Sequence[Mapping[str, Any]],
    evidence: Sequence[Mapping[str, str]],
    residual_uncertainty: Sequence[str],
) -> DelegatedStop:
    """Project the required zero-effect stop before a commit-bound VREC."""

    if not _gates_pass(gates, _operation(PREPARE_OPERATION)["gate_ids"]):
        _error("AEXFLW006", "candidate-commit stop requires passing VREC-preparation gates")
    step = _managed_step(
        "PROC-CANDIDATE-COMMIT",
        "STEP-CANDIDATE-COMMIT-AUTHORIZE",
        work_order_id,
    )
    decision = {
        key: step[key]
        for key in ("decision_right", "role", "artifact", "decision", "outcomes")
    }
    result = build_result(
        operation=PREPARE_OPERATION,
        outcome="completed",
        primary=work_order_id,
        artifacts=[work_order_id],
        governing=[],
        dependencies=[],
        declared_paths=declared_paths,
        changed_paths=changed_paths,
        change_set_complete=True,
        compliance={
            "checkpoint": "pre-action",
            "workflow_rule_id": "WFL-WO-PREPARE-VREC",
            "procedure_id": "PROC-CANDIDATE-COMMIT",
            "status": "pass",
            "gates": [dict(item) for item in gates],
        },
        procedure={
            "id": "PROC-CANDIDATE-COMMIT",
            "current_step": step["id"],
            "steps": [step],
        },
        restitution={
            "outcome": "completed",
            "done": ["Validated delegated VREC-preparation prerequisites up to the Git boundary."],
            "not_done": ["No candidate commit or verification record was created."],
            "blocked_by": [],
            "current_lifecycle_state": [f"{work_order_id} is implemented."],
            "decision_required": decision,
            "next": {
                "procedure_id": "PROC-CANDIDATE-COMMIT",
                "step_id": step["id"],
                "action": "Authorize creation of the exact candidate commit",
            },
            "command_or_response": {"kind": "response", "value": step["response"]},
            "alternatives": [],
        },
        before=[{"id": work_order_id, "status": "implemented"}],
        after=[{"id": work_order_id, "status": "implemented"}],
    )
    packet = project_decision_packet(
        result,
        _packet_context(
            repository=repository,
            candidate_commit=None,
            evaluator=evaluator,
            evidence=evidence,
            residual_uncertainty=residual_uncertainty,
            preview={
                "kind": "external-action",
                "artifact": None,
                "from_status": None,
                "to_status": None,
                "action": "create-candidate-commit",
                "target": repository,
            },
        ),
    )
    return DelegatedStop(PREPARE_OPERATION, "candidate commit is required", result, packet)


def delegated_work_order_start(
    repository: Path,
    *,
    work_order_id: str,
    delegate: str,
    execution_profile: str,
    gates: Sequence[Mapping[str, Any]],
    evaluator: EvaluatorIdentity,
    runtime_store: RuntimeStateStore,
    retry_ordinal: int = 0,
    observer: Observer = observe_stable_repository,
    fresh_observer: Callable[..., ContractDocument] = observe_repository,
    authority_guard: AuthorityGuard = mutation_guard.require_mutation_authority,
    now: Callable[[], datetime] = lambda: datetime.now(UTC),
) -> DelegatedLifecycleResult:
    """Admit and apply only ``approved -> in_progress`` and retain its receipt."""

    root = ensure_target(repository, must_exist=True)
    delegation, stable, derivation, work_order_path = _authorize(
        root,
        operation=START_OPERATION,
        work_order_id=work_order_id,
        delegate=delegate,
        execution_profile=execution_profile,
        paths=(_work_order(root, work_order_id)[1],),
        gates=gates,
        evaluator=evaluator,
        previous_receipt_sha256=None,
        retry_ordinal=retry_ordinal,
        observer=observer,
        authority_guard=authority_guard,
        now=now,
    )
    if stable.clean is not True or _changed_paths(root):
        _error("AEXFLW003", "delegated start requires an exact clean Git baseline")
    evidence = (
        {
            "kind": "delegation",
            "path": work_order_path,
            "sha256": delegation.work_order_sha256,
        },
    )
    _lifecycle_receipt(
        operation=START_OPERATION,
        work_order_id=work_order_id,
        repository_id=stable.document.value["repository"],
        envelope=derivation.envelope,
        execution_profile=execution_profile,
        before_sha256=stable.document.sha256,
        after_sha256=stable.document.sha256,
        changed_paths=(work_order_path,),
        evidence=evidence,
        gates=gates,
        deviations=(),
        residual_uncertainty=("Execution receipts do not authenticate a real-world actor.",),
        evaluator=evaluator,
        arguments={
            "work_order": work_order_id,
            "decision_right": "DR-WO-START",
            "delegate": delegate,
            "target_status": "in_progress",
        },
    )
    session: RuntimeSession | None = None
    admitted = False
    transition_applied = False
    try:
        session = runtime_store.start_session(
            stable.document.value["repository"],
            delegate,
            started_at=now().astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        fresh = fresh_observer(
            root,
            work_order_id=work_order_id,
            evaluator=evaluator,
            previous_receipt_sha256=None,
        )
        admit_fresh_envelope(
            envelope=derivation.envelope,
            fresh_observation=fresh,
            current_delegation_sha256=delegation.document.sha256,
            now=now().astimezone(UTC),
            runtime_store=runtime_store,
            session=session,
            gates_passed=True,
        )
        admitted = True
        plan_transition(
            root,
            {work_order_id: "in_progress"},
            {work_order_id: delegate},
            {},
            apply=True,
        )
        transition_applied = True
        after = observer(
            root,
            work_order_id=work_order_id,
            evaluator=evaluator,
            previous_receipt_sha256=None,
        ).document
        if _changed_paths(root) != (work_order_path,):
            _error("AEXFLW008", "delegated start produced an unexplained changed path")
        receipt = _lifecycle_receipt(
            operation=START_OPERATION,
            work_order_id=work_order_id,
            repository_id=stable.document.value["repository"],
            envelope=derivation.envelope,
            execution_profile=execution_profile,
            before_sha256=stable.document.sha256,
            after_sha256=after.sha256,
            changed_paths=(work_order_path,),
            evidence=evidence,
            gates=gates,
            deviations=(),
            residual_uncertainty=("Execution receipts do not authenticate a real-world actor.",),
            evaluator=evaluator,
            arguments={
                "work_order": work_order_id,
                "decision_right": "DR-WO-START",
                "delegate": delegate,
                "target_status": "in_progress",
            },
        )
        runtime_store.record_terminal(
            session,
            nonce=derivation.envelope.value["authority"]["nonce"],
            outcome="completed",
            receipt_sha256=receipt.sha256,
        )
        result = _transition_result(
            operation=START_OPERATION,
            work_order_id=work_order_id,
            before_status="approved",
            after_status="in_progress",
            declared_paths=delegation.execution_scope,
            changed_paths=(work_order_path,),
            gates=gates,
            next_procedure="PROC-WO-IMPLEMENT",
            next_step="STEP-WO-IMPLEMENT-CHECK",
            next_action="Submit the next proposed change bundle through the current coordinator session",
            decision_required=None,
            command_or_response={
                "kind": "response",
                "value": "Continue the current delegated implementation session.",
            },
        )
        return DelegatedLifecycleResult(
            START_OPERATION,
            result,
            receipt,
            derivation.envelope,
            stable.document,
            after,
            session,
        )
    except Exception:
        if session is not None:
            if admitted:
                _close_failed_session(
                    runtime_store,
                    session,
                    nonce=derivation.envelope.value["authority"]["nonce"],
                    recovery_required=transition_applied,
                )
            else:
                try:
                    runtime_store.close_session(session)
                except Exception:
                    pass
        raise


def delegated_change_bundle_apply(
    repository: Path,
    *,
    work_order_id: str,
    delegate: str,
    execution_profile: str,
    requested_paths: Sequence[str],
    baseline_workspace: Path,
    proposed_workspace: Path,
    object_store: Path,
    intended_deletions: Sequence[str],
    previous_receipt_sha256: str,
    gates: Sequence[Mapping[str, Any]],
    evidence: Sequence[Mapping[str, str]],
    deviations: Sequence[Mapping[str, str]],
    evaluator: EvaluatorIdentity,
    runtime_store: RuntimeStateStore,
    session: RuntimeSession,
    retry_ordinal: int = 0,
    observer: Observer = observe_stable_repository,
    fresh_observer: Callable[..., ContractDocument] = observe_repository,
    authority_guard: AuthorityGuard = mutation_guard.require_mutation_authority,
    now: Callable[[], datetime] = lambda: datetime.now(UTC),
) -> DelegatedEffectResult:
    """Derive, construct, freshly admit, and broker one sequential change bundle."""

    root = ensure_target(repository, must_exist=True)
    paths = tuple(
        sorted(
            {validate_portable_path(item) for item in requested_paths},
            key=lambda item: item.encode("utf-8"),
        )
    )
    if not paths or len(paths) != len(requested_paths):
        _error("AEXFLW008", "effect request paths are empty or duplicated")
    delegation, stable, derivation, _ = _authorize(
        root,
        operation=EFFECT_OPERATION,
        work_order_id=work_order_id,
        delegate=delegate,
        execution_profile=execution_profile,
        paths=paths,
        gates=gates,
        evaluator=evaluator,
        previous_receipt_sha256=previous_receipt_sha256,
        retry_ordinal=retry_ordinal,
        observer=observer,
        authority_guard=authority_guard,
        now=now,
    )
    bundle = construct_change_bundle(
        baseline_workspace=baseline_workspace,
        proposed_workspace=proposed_workspace,
        object_store=object_store,
        work_order=work_order_id,
        envelope_sha256=derivation.envelope.sha256,
        repository_state_before=stable.document.sha256,
        intended_deletions=intended_deletions,
    )
    if bundle.proposed_paths != paths:
        _error("AEXFLW008", "constructed bundle differs from the exact requested path set")
    effect = apply_change_bundle(
        repository=root,
        bundle_bytes=bundle.bundle.canonical_bytes,
        object_store=object_store,
        envelope=derivation.envelope,
        current_delegation_sha256=delegation.document.sha256,
        evaluator=evaluator,
        runtime_store=runtime_store,
        session=session,
        gates_passed=True,
        gate_results=tuple({"id": item["id"], "status": item["status"]} for item in gates),
        deviations=deviations,
        evidence=evidence,
        now=now,
        observer=fresh_observer,
        authority_guard=authority_guard,
    )
    after = fresh_observer(
        root,
        work_order_id=work_order_id,
        evaluator=evaluator,
        previous_receipt_sha256=previous_receipt_sha256,
    )
    if effect.receipt.value["state"]["state_after"] != after.sha256:
        _error("AEXFLW004", "broker receipt does not bind the fresh post-effect observation")
    return DelegatedEffectResult(
        EFFECT_OPERATION,
        effect,
        bundle,
        derivation.envelope,
        stable.document,
        after,
    )


def _within(path: str, scope: str) -> bool:
    return path.startswith(scope) if scope.endswith("/") else path == scope


def _file_sha256(root: Path, relative: str) -> str:
    target = root.joinpath(*relative.split("/"))
    try:
        if target.is_symlink() or not target.is_file():
            _error("AEXFLW007", f"required evidence is not a regular file: {relative}")
        return hashlib.sha256(target.read_bytes()).hexdigest()
    except OSError as exc:
        _error("AEXFLW007", f"cannot read required evidence {relative}: {exc}")


def _contract_document(
    value: ContractDocument | Mapping[str, Any],
    *,
    schema: str,
) -> ContractDocument:
    raw = value.value if isinstance(value, ContractDocument) else value
    return validate_contract(raw, expected_schema=schema)


def _validate_lifecycle_proof(
    proof: LifecycleProof,
    *,
    work_order_id: str,
    operation: str,
    evaluator: EvaluatorIdentity,
) -> tuple[ContractDocument, ContractDocument, ContractDocument, ContractDocument]:
    """Validate a lifecycle receipt against its retained authority and states."""

    row = _operation(operation)
    receipt_value = proof.receipt.value if isinstance(proof.receipt, ContractDocument) else proof.receipt
    receipt = validate_execution_receipt(receipt_value)
    envelope = _contract_document(proof.envelope, schema=AUTONOMY_ENVELOPE_V2_SCHEMA)
    before = _contract_document(proof.before_observation, schema=REPOSITORY_OBSERVATION_SCHEMA)
    after = _contract_document(proof.after_observation, schema=REPOSITORY_OBSERVATION_SCHEMA)
    operation_ids = [item["id"] for item in receipt.value["execution"]["operations"]]
    receipt_evaluator = receipt.value["validation"]["evaluator"]
    expected_receipt_evaluator = _evaluator_receipt_identity(evaluator)
    state_before = receipt.value["effects"]["state_before"]
    state_after = receipt.value["effects"]["state_after"]
    if (
        receipt.value["selection"]["artifact"] != work_order_id
        or receipt.value["selection"]["repository"] != before.value["repository"]
        or receipt.value["selection"]["autonomy_envelope_sha256"] != envelope.sha256
        or receipt.value["validation"]["outcome"] != "completed"
        or not operation_ids
        or operation_ids[0] != operation
        or operation_ids.count(operation) != 1
        or receipt_evaluator != expected_receipt_evaluator
        or state_before != [{"kind": "repository-state", "sha256": before.sha256}]
        or state_after != [{"kind": "repository-state", "sha256": after.sha256}]
    ):
        _error("AEXFLW004", f"{operation} receipt does not bind its retained lifecycle proof")
    envelope_value = envelope.value
    if (
        envelope_value["selection"]["work_order"] != work_order_id
        or envelope_value["selection"]["repository_state"] != before.sha256
        or envelope_value["selection"]["evaluator_payload_sha256"] != evaluator.payload_sha256
        or envelope_value["authority"]["expected_repository_state"] != before.sha256
        or envelope_value["authority"]["decision_right"] != row["decision_right"]
        or envelope_value["delegation"]["operations"] != [operation]
        or envelope_value["authority"]["previous_receipt_sha256"]
        != before.value["previous_receipt_sha256"]
        or after.value["previous_receipt_sha256"]
        != before.value["previous_receipt_sha256"]
    ):
        _error("AEXFLW004", f"{operation} envelope or receipt-chain anchor is inconsistent")
    for observation in (before, after):
        if (
            observation.value["repository"] != before.value["repository"]
            or observation.value["evaluator"] != evaluator.as_dict()
            or observation.value["governance"]["work_order"] != work_order_id
        ):
            _error("AEXFLW004", f"{operation} observation identity is inconsistent")
    if (
        before.value["governance"]["work_order_status"] != row["current_status"]
        or after.value["governance"]["work_order_status"] != row["result_status"]
    ):
        _error("AEXFLW004", f"{operation} lifecycle states differ from the managed catalog")
    return receipt, envelope, before, after


def _validate_completion_proof(
    root: Path,
    *,
    work_order_id: str,
    work_order_path: str,
    delegation: ResolvedDelegation,
    proof: CompletionProof,
    evaluator: EvaluatorIdentity,
    observer: Observer,
) -> tuple[str, ContractDocument, tuple[str, ...], tuple[Mapping[str, str], ...]]:
    start, _, _, start_after = _validate_lifecycle_proof(
        proof.start,
        work_order_id=work_order_id,
        operation=START_OPERATION,
        evaluator=evaluator,
    )
    if [item["id"] for item in start.value["execution"]["operations"]] != [START_OPERATION]:
        _error("AEXFLW004", "start receipt contains an unexpected operation")
    if not proof.effects:
        _error("AEXFLW004", "completion proof has no admitted effect receipt")
    expected_previous = start.sha256
    previous_after = start_after
    effect_paths: set[str] = set()
    last_receipt: EffectReceipt | None = None
    last_after: ContractDocument | None = None
    for index, item in enumerate(proof.effects):
        receipt = validate_effect_receipt(item.receipt.value if isinstance(item.receipt, EffectReceipt) else item.receipt)
        before = validate_contract(item.before_observation.value, expected_schema="se-harness-repository-observation-v1")
        after = validate_contract(item.after_observation.value, expected_schema="se-harness-repository-observation-v1")
        if (
            receipt.value["identity"]["work_order"] != work_order_id
            or receipt.value["identity"]["evaluator"] != evaluator.as_dict()
            or receipt.value["state"]["previous_receipt_sha256"] != expected_previous
            or before.value["previous_receipt_sha256"] != expected_previous
            or after.value["previous_receipt_sha256"] != expected_previous
            or receipt.value["state"]["state_before"] != before.sha256
            or receipt.value["state"]["state_after"] != after.sha256
        ):
            _error("AEXFLW004", f"effect receipt identity or state link is invalid at ordinal {index}")
        if previous_after is not None:
            _ensure_same_live_state(previous_after, before, f"effect receipt {index}")
        for entry in receipt.value["entries"]:
            effect_paths.add(entry["path"])
        expected_previous = receipt.sha256
        previous_after = after
        last_receipt = receipt
        last_after = after
    assert last_receipt is not None and last_after is not None
    historical = observer(
        root,
        work_order_id=work_order_id,
        evaluator=evaluator,
        previous_receipt_sha256=last_receipt.value["state"]["previous_receipt_sha256"],
    ).document
    if historical.sha256 != last_after.sha256:
        _error("AEXFLW004", "fresh live state differs from the terminal effect receipt")
    changed = tuple(
        sorted(
            {validate_portable_path(item) for item in proof.changed_paths},
            key=lambda item: item.encode("utf-8"),
        )
    )
    if len(changed) != len(proof.changed_paths):
        _error("AEXFLW008", "completion proof changed paths contain duplicates")
    if not set(changed).issubset(effect_paths):
        _error("AEXFLW008", "a final changed path has no admitted effect receipt")
    all_effect_paths = effect_paths | set(changed)
    if any(
        not any(_within(path, scope) for scope in delegation.execution_scope)
        or not any(_within(path, scope) for scope in delegation.document.value["paths"])
        for path in all_effect_paths
    ):
        _error("AEXFLW008", "completion proof contains a path outside exact work and delegation scope")
    current_changed = _changed_paths(root)
    expected_changed = tuple(
        sorted({*changed, work_order_path}, key=lambda item: item.encode("utf-8"))
    )
    if current_changed != expected_changed:
        _error("AEXFLW008", "live Git changed paths differ from the complete declared change set")
    if not proof.tests or any(item.get("status") != "passed" for item in proof.tests):
        _error("AEXFLW009", "required verification results are missing or unsuccessful")
    operation_ids = [item.get("id") for item in proof.tests]
    if (
        any(not isinstance(item, str) or item == COMPLETE_OPERATION for item in operation_ids)
        or len(set(operation_ids)) != len(operation_ids)
    ):
        _error("AEXFLW009", "verification operation identities are invalid or duplicated")
    if not _gates_pass(proof.gates, _operation(COMPLETE_OPERATION)["gate_ids"]):
        _error("AEXFLW006", "completion gates did not all pass")
    evidence: list[Mapping[str, str]] = []
    evidence_keys: set[tuple[str, str]] = set()
    for raw in proof.evidence:
        if set(raw) != {"kind", "path", "sha256"}:
            _error("AEXFLW007", "completion evidence has an invalid field set")
        kind = raw["kind"]
        path = validate_portable_path(raw["path"])
        digest = raw["sha256"]
        if not isinstance(kind, str) or len(digest) != 64 or (kind, path) in evidence_keys:
            _error("AEXFLW007", "completion evidence identity or digest is invalid")
        if _file_sha256(root, path) != digest:
            _error("AEXFLW007", f"completion evidence digest differs from live bytes: {path}")
        evidence_keys.add((kind, path))
        evidence.append({"kind": kind, "path": path, "sha256": digest})
    if not set(_required_evidence(delegation)).issubset(evidence_keys):
        _error("AEXFLW007", "formal delegation evidence obligations are incomplete")
    return last_receipt.sha256, last_after, changed, tuple(evidence)


def delegated_work_order_complete(
    repository: Path,
    *,
    work_order_id: str,
    delegate: str,
    execution_profile: str,
    proof: CompletionProof,
    evaluator: EvaluatorIdentity,
    runtime_store: RuntimeStateStore,
    session: RuntimeSession,
    retry_ordinal: int = 0,
    observer: Observer = observe_stable_repository,
    fresh_observer: Callable[..., ContractDocument] = observe_repository,
    authority_guard: AuthorityGuard = mutation_guard.require_mutation_authority,
    now: Callable[[], datetime] = lambda: datetime.now(UTC),
) -> DelegatedLifecycleResult:
    """Prove receipt continuity and apply only ``in_progress -> implemented``."""

    root = ensure_target(repository, must_exist=True)
    _, work_order_path, raw = _work_order(root, work_order_id)
    delegation = resolve_delegation(raw, phase4_delegation_policy())
    if runtime_store.read_effect_journal(session.repository_id) is not None:
        _error("AEXFLW010", "a nonterminal broker journal blocks completion")
    previous_receipt, last_after, changed, evidence = _validate_completion_proof(
        root,
        work_order_id=work_order_id,
        work_order_path=work_order_path,
        delegation=delegation,
        proof=proof,
        evaluator=evaluator,
        observer=observer,
    )
    delegation, stable, derivation, _ = _authorize(
        root,
        operation=COMPLETE_OPERATION,
        work_order_id=work_order_id,
        delegate=delegate,
        execution_profile=execution_profile,
        paths=(work_order_path,),
        gates=proof.gates,
        evaluator=evaluator,
        previous_receipt_sha256=previous_receipt,
        retry_ordinal=retry_ordinal,
        observer=observer,
        authority_guard=authority_guard,
        now=now,
    )
    _ensure_same_live_state(last_after, stable.document, "completion admission")
    expected_changed = tuple(sorted({*changed, work_order_path}, key=lambda item: item.encode("utf-8")))
    receipt_evidence = list(evidence)
    if all(item["path"] != work_order_path for item in receipt_evidence):
        receipt_evidence.append(
            {
                "kind": "delegation",
                "path": work_order_path,
                "sha256": delegation.work_order_sha256,
            }
        )
    receipt_arguments = {
        "work_order": work_order_id,
        "decision_right": "DR-WO-COMPLETE",
        "delegate": delegate,
        "effect_receipts": [
            validate_effect_receipt(
                item.receipt.value if isinstance(item.receipt, EffectReceipt) else item.receipt
            ).sha256
            for item in proof.effects
        ],
        "changed_paths": list(changed),
    }
    _lifecycle_receipt(
        operation=COMPLETE_OPERATION,
        work_order_id=work_order_id,
        repository_id=stable.document.value["repository"],
        envelope=derivation.envelope,
        execution_profile=execution_profile,
        before_sha256=stable.document.sha256,
        after_sha256=stable.document.sha256,
        changed_paths=expected_changed,
        evidence=receipt_evidence,
        gates=proof.gates,
        deviations=proof.deviations,
        residual_uncertainty=proof.residual_uncertainty,
        evaluator=evaluator,
        arguments=receipt_arguments,
        additional_operations=proof.tests,
    )
    admitted = False
    transition_applied = False
    try:
        fresh = fresh_observer(
            root,
            work_order_id=work_order_id,
            evaluator=evaluator,
            previous_receipt_sha256=previous_receipt,
        )
        admit_fresh_envelope(
            envelope=derivation.envelope,
            fresh_observation=fresh,
            current_delegation_sha256=delegation.document.sha256,
            now=now().astimezone(UTC),
            runtime_store=runtime_store,
            session=session,
            gates_passed=True,
        )
        admitted = True
        plan_transition(
            root,
            {work_order_id: "implemented"},
            {work_order_id: delegate},
            {},
            apply=True,
        )
        transition_applied = True
        after = observer(
            root,
            work_order_id=work_order_id,
            evaluator=evaluator,
            previous_receipt_sha256=previous_receipt,
        ).document
        if _changed_paths(root) != expected_changed:
            _error("AEXFLW008", "completion transition produced an unexplained changed path")
        receipt = _lifecycle_receipt(
            operation=COMPLETE_OPERATION,
            work_order_id=work_order_id,
            repository_id=stable.document.value["repository"],
            envelope=derivation.envelope,
            execution_profile=execution_profile,
            before_sha256=stable.document.sha256,
            after_sha256=after.sha256,
            changed_paths=expected_changed,
            evidence=receipt_evidence,
            gates=proof.gates,
            deviations=proof.deviations,
            residual_uncertainty=proof.residual_uncertainty,
            evaluator=evaluator,
            arguments=receipt_arguments,
            additional_operations=proof.tests,
        )
        runtime_store.record_terminal(
            session,
            nonce=derivation.envelope.value["authority"]["nonce"],
            outcome="completed",
            receipt_sha256=receipt.sha256,
        )
        runtime_store.close_session(session)
        decision = {
            "decision_right": "DR-EXTERNAL-ACTION",
            "role": "repository-owner",
            "artifact": work_order_id,
            "decision": "whether the exact candidate commit may be created",
            "outcomes": ["authorize", "stop"],
        }
        result = _transition_result(
            operation=COMPLETE_OPERATION,
            work_order_id=work_order_id,
            before_status="in_progress",
            after_status="implemented",
            declared_paths=delegation.execution_scope,
            changed_paths=expected_changed,
            gates=proof.gates,
            next_procedure="PROC-CANDIDATE-COMMIT",
            next_step="STEP-CANDIDATE-COMMIT-AUTHORIZE",
            next_action="Authorize creation of the exact candidate commit",
            decision_required=decision,
            command_or_response={
                "kind": "response",
                "value": f"Authorize creating the exact candidate commit for {work_order_id}.",
            },
        )
        return DelegatedLifecycleResult(
            COMPLETE_OPERATION,
            result,
            receipt,
            derivation.envelope,
            stable.document,
            after,
            None,
        )
    except Exception:
        if admitted:
            _close_failed_session(
                runtime_store,
                session,
                nonce=derivation.envelope.value["authority"]["nonce"],
                recovery_required=transition_applied,
            )
        else:
            try:
                runtime_store.close_session(session)
            except Exception:
                pass
        raise


def _precheck_prepare(
    root: Path,
    *,
    work_order_id: str,
    delegate: str,
    execution_profile: str,
    gates: Sequence[Mapping[str, Any]],
) -> tuple[ResolvedDelegation, str, Mapping[str, Any]]:
    _, work_order_path, raw = _work_order(root, work_order_id)
    delegation = resolve_delegation(raw, phase4_delegation_policy())
    declaration = delegation.document.value
    row = _operation(PREPARE_OPERATION)
    if (
        delegation.work_order_status != row["current_status"]
        or row["id"] not in declaration["operations"]
        or row["decision_right"] not in declaration["decision_rights"]
        or delegate != declaration["delegate"]
        or execution_profile not in declaration["execution_profiles"]
    ):
        _error("AEXFLW005", "VREC-preparation request differs from current formal delegation")
    if not _gates_pass(gates, row["gate_ids"]):
        _error("AEXFLW006", "VREC-preparation gates did not all pass")
    return delegation, work_order_path, _front_matter(raw)


def delegated_vrec_prepare(
    repository: Path,
    *,
    work_order_id: str,
    record_id: str,
    verification_ids: Sequence[str],
    evidence_paths: Sequence[str],
    owner: str,
    output: str,
    domain: str,
    delegate: str,
    execution_profile: str,
    gates: Sequence[Mapping[str, Any]],
    completion_proof: LifecycleProof,
    evaluator: EvaluatorIdentity,
    runtime_store: RuntimeStateStore,
    residual_uncertainty: Sequence[str] = (),
    retry_ordinal: int = 0,
    observer: Observer = observe_stable_repository,
    fresh_observer: Callable[..., ContractDocument] = observe_repository,
    authority_guard: AuthorityGuard = mutation_guard.require_mutation_authority,
    now: Callable[[], datetime] = lambda: datetime.now(UTC),
) -> DelegatedPreparationResult | DelegatedStop:
    """Prepare one undecided ready VREC, or stop exactly at the Git boundary."""

    root = ensure_target(repository, must_exist=True)
    completion, _, _, completion_after = _validate_lifecycle_proof(
        completion_proof,
        work_order_id=work_order_id,
        operation=COMPLETE_OPERATION,
        evaluator=evaluator,
    )
    delegation, _, metadata = _precheck_prepare(
        root,
        work_order_id=work_order_id,
        delegate=delegate,
        execution_profile=execution_profile,
        gates=gates,
    )
    output_path = validate_portable_path(output)
    evidence_output = validate_portable_path(
        f"docs/engineering/{domain}/evidence/{record_id}-evaluator.json"
    )
    previous_receipt = completion.sha256
    delegation, stable, derivation, _ = _authorize(
        root,
        operation=PREPARE_OPERATION,
        work_order_id=work_order_id,
        delegate=delegate,
        execution_profile=execution_profile,
        paths=(output_path, evidence_output),
        gates=gates,
        evaluator=evaluator,
        previous_receipt_sha256=previous_receipt,
        retry_ordinal=retry_ordinal,
        observer=observer,
        authority_guard=authority_guard,
        now=now,
    )
    receipt_evidence = tuple(completion.value["effects"]["evidence"])
    dirty = _changed_paths(root)
    assurance = metadata.get("assurance")
    commit_required = (
        isinstance(assurance, Mapping)
        and assurance.get("commit_bound_verification") == "required"
    )
    if dirty:
        if not commit_required:
            _error("AEXFLW003", "verification preparation requires a clean existing candidate")
        _ensure_same_live_state(completion_after, stable.document, "pre-commit VREC preparation")
        probe = runtime_store.start_session(
            stable.document.value["repository"],
            delegate,
            started_at=now().astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        runtime_store.close_session(probe)
        return candidate_commit_stop(
            work_order_id=work_order_id,
            repository=completion.value["selection"]["repository"],
            evaluator=evaluator,
            declared_paths=delegation.execution_scope,
            changed_paths=dirty,
            gates=gates,
            evidence=receipt_evidence,
            residual_uncertainty=residual_uncertainty,
        )
    require_clean_worktree(root)
    _ensure_same_candidate_content(completion_after, stable.document, "post-commit VREC preparation")
    if stable.document.value["git"]["head"] == completion_after.value["git"]["head"]:
        _error("AEXFLW003", "VREC preparation has no separately created candidate commit")
    receipt_arguments = {
        "work_order": work_order_id,
        "record": record_id,
        "verification": list(verification_ids),
        "evidence": list(evidence_paths),
    }
    _lifecycle_receipt(
        operation=PREPARE_OPERATION,
        work_order_id=work_order_id,
        repository_id=stable.document.value["repository"],
        envelope=derivation.envelope,
        execution_profile=execution_profile,
        before_sha256=stable.document.sha256,
        after_sha256=stable.document.sha256,
        changed_paths=(evidence_output, output_path),
        evidence=(
            {"kind": "verification-record", "path": output_path, "sha256": "0" * 64},
            {"kind": "evaluator", "path": evidence_output, "sha256": "1" * 64},
        ),
        gates=gates,
        deviations=(),
        residual_uncertainty=residual_uncertainty,
        evaluator=evaluator,
        arguments=receipt_arguments,
    )
    session: RuntimeSession | None = None
    admitted = False
    preparation_applied = False
    try:
        session = runtime_store.start_session(
            stable.document.value["repository"],
            delegate,
            started_at=now().astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
        fresh = fresh_observer(
            root,
            work_order_id=work_order_id,
            evaluator=evaluator,
            previous_receipt_sha256=previous_receipt,
        )
        admit_fresh_envelope(
            envelope=derivation.envelope,
            fresh_observation=fresh,
            current_delegation_sha256=delegation.document.sha256,
            now=now().astimezone(UTC),
            runtime_store=runtime_store,
            session=session,
            gates_passed=True,
        )
        admitted = True
        record = capture_verification(
            root,
            record_id=record_id,
            work_order_ids=[work_order_id],
            verification_ids=list(verification_ids),
            evidence_paths=list(evidence_paths),
            owner=owner,
            output=output_path,
            domain=domain,
        )
        preparation_applied = True
        if record.relative_to(root).as_posix() != output_path:
            _error("AEXFLW011", "provenance preparation returned an unexpected record path")
        changed = _changed_paths(root)
        expected_changed = tuple(sorted((evidence_output, output_path), key=lambda item: item.encode("utf-8")))
        if changed != expected_changed:
            _error("AEXFLW008", "VREC preparation produced an unexplained changed path")
        after = observer(
            root,
            work_order_id=work_order_id,
            evaluator=evaluator,
            previous_receipt_sha256=previous_receipt,
        ).document
        prepared_evidence = (
            {"kind": "verification-record", "path": output_path, "sha256": _file_sha256(root, output_path)},
            {"kind": "evaluator", "path": evidence_output, "sha256": _file_sha256(root, evidence_output)},
        )
        receipt = _lifecycle_receipt(
            operation=PREPARE_OPERATION,
            work_order_id=work_order_id,
            repository_id=stable.document.value["repository"],
            envelope=derivation.envelope,
            execution_profile=execution_profile,
            before_sha256=stable.document.sha256,
            after_sha256=after.sha256,
            changed_paths=expected_changed,
            evidence=prepared_evidence,
            gates=gates,
            deviations=(),
            residual_uncertainty=residual_uncertainty,
            evaluator=evaluator,
            arguments=receipt_arguments,
        )
        runtime_store.record_terminal(
            session,
            nonce=derivation.envelope.value["authority"]["nonce"],
            outcome="completed",
            receipt_sha256=receipt.sha256,
        )
        runtime_store.close_session(session)
        session = None
        workflow_result = focus_schema2(root, artifact_id=record_id)
        commit, _ = git_identity(root)
        packet = project_decision_packet(
            workflow_result,
            _packet_context(
                repository=stable.document.value["repository"],
                candidate_commit=commit,
                evaluator=evaluator,
                evidence=prepared_evidence,
                residual_uncertainty=residual_uncertainty,
                alternatives=_packet_alternatives(workflow_result),
            ),
        )
        return DelegatedPreparationResult(
            PREPARE_OPERATION,
            workflow_result,
            receipt,
            packet,
            record,
        )
    except Exception:
        if session is not None:
            if admitted:
                _close_failed_session(
                    runtime_store,
                    session,
                    nonce=derivation.envelope.value["authority"]["nonce"],
                    recovery_required=preparation_applied,
                )
            else:
                try:
                    runtime_store.close_session(session)
                except Exception:
                    pass
        raise


def refuse_prohibited_action(
    action: str,
    *,
    work_order_id: str,
    repository: str,
    evaluator: EvaluatorIdentity,
    evidence: Sequence[Mapping[str, str]],
) -> DelegatedStop:
    """Return a zero-effect stop for a reserved or prohibited Phase 4 request."""

    if action not in PROHIBITED_ACTIONS:
        _error("AEXFLW012", "requested action is neither activated nor a known prohibited action")
    decision = {
        "decision_right": "DR-EXTERNAL-ACTION",
        "role": "accountable-external-action-owner",
        "artifact": work_order_id,
        "decision": f"whether the exact prohibited request may be separately authorized: {action}",
        "outcomes": ["authorize", "stop"],
    }
    response = f"State and separately authorize the exact {action} action and target for {work_order_id}."
    step = {
        "id": "STEP-EXTERNAL-ACTION",
        "kind": "decision",
        **decision,
        "response": response,
        "gate_ids": ["QG-G5-EXTERNAL-ACTION"],
        "effects": [f"Permits only the exact separately authorized {action} action."],
        "non_effects": [f"This stop did not perform {action} or any repository, Git, network, credential, release, or external effect."],
    }
    result = build_result(
        operation=f"refuse-{action}",
        outcome="completed",
        primary=work_order_id,
        artifacts=[work_order_id],
        governing=[],
        dependencies=[],
        declared_paths=[],
        changed_paths=[],
        change_set_complete=True,
        compliance={
            "checkpoint": "pre-action",
            "workflow_rule_id": "WFL-RLS-EXTERNAL",
            "procedure_id": "PROC-EXTERNAL-ACTION",
            "status": "pass",
            "gates": [],
        },
        procedure={"id": "PROC-EXTERNAL-ACTION", "current_step": step["id"], "steps": [step]},
        restitution={
            "outcome": "completed",
            "done": [f"Refused the Phase 4 {action} request with zero effect."],
            "not_done": [f"The requested {action} was not performed."],
            "blocked_by": [],
            "current_lifecycle_state": [f"{work_order_id} is unchanged."],
            "decision_required": decision,
            "next": {
                "procedure_id": "PROC-EXTERNAL-ACTION",
                "step_id": step["id"],
                "action": f"Obtain separate exact authority for {action}",
            },
            "command_or_response": {"kind": "response", "value": response},
            "alternatives": [],
        },
        before=[{"id": work_order_id, "status": "implemented"}],
        after=[{"id": work_order_id, "status": "implemented"}],
    )
    packet = project_decision_packet(
        result,
        _packet_context(
            repository=repository,
            candidate_commit=None,
            evaluator=evaluator,
            evidence=evidence,
            residual_uncertainty=(f"The prohibited {action} request was not performed.",),
            preview={
                "kind": "external-action",
                "artifact": None,
                "from_status": None,
                "to_status": None,
                "action": action,
                "target": repository,
            },
        ),
    )
    return DelegatedStop(f"refuse-{action}", f"{action} is outside Phase 4", result, packet)


__all__ = [
    "COMPLETE_OPERATION",
    "CompletionProof",
    "DelegatedEffectResult",
    "DelegatedLifecycleResult",
    "DelegatedPreparationResult",
    "DelegatedStop",
    "DelegatedWorkflowError",
    "EFFECT_OPERATION",
    "EffectProof",
    "LifecycleProof",
    "PHASE4_OPERATIONS",
    "PREPARE_OPERATION",
    "PROHIBITED_ACTIONS",
    "START_OPERATION",
    "candidate_commit_stop",
    "delegated_change_bundle_apply",
    "delegated_vrec_prepare",
    "delegated_work_order_complete",
    "delegated_work_order_start",
    "phase4_delegation_policy",
    "phase4_operation_catalog",
    "refuse_prohibited_action",
]
