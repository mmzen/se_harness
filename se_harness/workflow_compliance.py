"""Stateless selected-scope workflow checkpoint evaluation."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping

from se_harness.installer import HarnessError, ensure_target
from se_harness.preflight import lifecycle_relevant, lock_files, orphaned_ready_records, run_preflight
from se_harness.integrity import atomic_write_bytes
from se_harness.workflow_contract import (
    CHECKPOINTS,
    EVIDENCE_CHECKPOINTS,
    ContractError,
    aggregation_order,
    effective_checkpoints,
    lifecycle_family,
    load_validated_contracts,
    select_rule,
    transition_binding,
)
from se_harness.workflow_procedures import (
    ProcedureError,
    command_or_response,
    corrective_response,
    decision_required,
    resolve_procedure,
    select_current_step,
)
from se_harness.repository_graph import (
    REPOSITORY_ERROR_CODES,
    artifact_catalog,
    classify_diagnostics,
    project_scope,
    validated_repository,
)
from se_harness.workflow_edges import structural_precondition_results
from se_harness.workflow_result import build_result
from se_harness.codes import (
    CodedError,
    WEX201,
    WEX210,
    WEX220,
    WEX_ADS_001,
    WEX_ECP_002,
    WEX_ECP_010,
    WEX_ECP_011,
    WEX_ECP_012,
    W_ADS_001,
    W_ADS_002,
)

# The seams of this module (SPEC-ECP-024 ECP-ENG-019): every public name stays importable here.
from se_harness.workflow_change_set import (  # noqa: F401
    CHANGE_SET_SCHEMA,
    ChangeSet,
    added_paths,
    validate_changed_targets,
    declared_change_set,
    execution_scope,
    formal_snapshot_digest,
    git_change_set,
    normalize_path,
    own_record_paths,
    parse_change_manifest,
    path_is_admitted,
    risk_admissions,
)
from se_harness.workflow_evidence_packet import (  # noqa: F401
    EVIDENCE_HEADER_KEYS,
    RFC3339_TIMESTAMP,
    evidence_packet_path,
    line_ending_conversion,
    parse_evidence_header,
    rebind_handoff_packet,
    render_evidence_header,
    retain_handoff_result,
)
from se_harness.workflow_predicates import (  # noqa: F401
    CheckpointContext,
    authoring_ready,
    blocking_decisions,
    decision_gate_clear,
    pull_request_body_findings,
    release_unit_ready,
    review_evidence,
)


def lifecycle_relevant_diagnostics(root: Path, report: Any) -> list[Any]:
    """The one preflight-diagnostic filter (ECP-KRN-007).

    Candidate-distribution comparisons and lock entries the released root never
    recorded are candidate-versus-released skew, not installation facts; every
    other diagnostic blocks a lifecycle stage.
    """

    # ECP-ENG-014: the classifier lives with preflight, which reports skew apart already;
    # applying it here keeps a report built elsewhere on the same footing.
    locked = lock_files(root)
    return [item for item in report.diagnostics if lifecycle_relevant(item, locked)]


def _preflight_status(context: CheckpointContext, phase: str) -> tuple[str, str]:
    if context.artifact.artifact_type != "work_order":
        return "pass", f"{phase} preflight does not apply to {context.artifact.artifact_type}."
    report = run_preflight(context.root, work_order_id=context.artifact.artifact_id, phase=phase, report=context.report)
    relevant = lifecycle_relevant_diagnostics(context.root, report)
    if relevant:
        return "fail", relevant[0].message
    return "pass", f"Released-installation {phase} preflight inputs are ready."


#: The gate the `scope` checkpoint evaluates for a work order in any state (ECP-SCP-002).
SCOPE_CHECKPOINT_GATE = "QG-G4-IMPLEMENTATION-EVIDENCE"
#: Corrective forms for a blocked scope check (ECP-SCP-005): the step the state selects
#: may declare none for the scope predicates, so the checkpoint carries its own, the
#: same forms STEP-WO-IMPLEMENT-CHECK declares for them at handoff.
SCOPE_CHECKPOINT_CORRECTIVE = {
    "QGP-G4I-SCOPE": {"kind": "escalation", "decision_right": "DR-WO-SELECT"},
    "QGP-G4I-COMPLETE": {
        "kind": "command",
        "argv": ["harnessctl", "check", ".", "--artifact", "{artifact_id}", "--checkpoint", "scope", "--from-git", "<base>"],
    },
    "QGP-G4I-PATHS": {"kind": "escalation", "decision_right": "DR-REMEDIATION-SCOPE"},
}


def write_evidence_packet(
    repository: Path,
    *,
    artifact_id: str,
    checkpoint: str,
    now: str,
) -> dict[str, Any]:
    """Write or rebind one evidence packet and return the schema-2 result (ECP-EVD-001 to -007)."""

    if checkpoint not in EVIDENCE_CHECKPOINTS:  # ECP-PRM-012: the contract module's set
        raise CodedError(WEX_ECP_010, "the checkpoint must be start, pre-action, transition, or handoff")
    if not RFC3339_TIMESTAMP.fullmatch(now):
        raise CodedError(WEX_ECP_010, "rebound_at must be RFC 3339 UTC at second precision")
    root = ensure_target(repository, must_exist=True)
    _, report = validated_repository(root)
    catalog = artifact_catalog(report)
    primary = catalog.get(artifact_id)
    if primary is None:
        raise CodedError(WEX_ECP_010, f"unknown artifact ID: {artifact_id}")
    if primary.artifact_type != "work_order":
        raise CodedError(WEX_ECP_010, "evidence packets are keyed by a work order")
    in_progress = sorted(
        item.artifact_id for item in catalog.values()
        if item.artifact_type == "work_order" and item.status == "in_progress"
    )
    if len(in_progress) == 1 and in_progress[0] != artifact_id:
        raise CodedError(WEX_ECP_012, f"the working tree selects {in_progress[0]} (the one in_progress work order), not {artifact_id}"
        )
    path = evidence_packet_path(root, primary, checkpoint)
    relative = path.relative_to(root).as_posix()
    conversion = line_ending_conversion(root, relative)
    if conversion is not None:
        raise CodedError(WEX_ECP_011, f"a .gitattributes rule would convert line endings of {relative} ({conversion})")
    snapshot = formal_snapshot_digest(root, report.artifacts)
    header = {
        "artifact": artifact_id,
        "checkpoint": checkpoint,
        "formal_snapshot_sha256": snapshot,
        "rebound_at": now,
    }
    action = "create"
    if path.exists():
        if path.is_symlink() or not path.is_file():
            raise CodedError(WEX_ECP_010, f"{relative} is not an ordinary file")
        existing, body = parse_evidence_header(path.read_bytes())
        if existing is None:
            raise CodedError(WEX_ECP_010, f"{relative} carries no evidence packet header at byte offset 0")
        if existing["artifact"] != artifact_id or existing["checkpoint"] != checkpoint:
            raise CodedError(WEX_ECP_010, f"{relative} is the packet of {existing['artifact']} at {existing['checkpoint']}, "
                f"not {artifact_id} at {checkpoint}"
            )
        action = "rebind"
    else:
        body = (
            f"\n# {artifact_id} {checkpoint} evidence\n\n"
            "Retained by `harnessctl evidence`; body content is owner-authored.\n"
        ).encode("utf-8")
    content = render_evidence_header(header) + body
    try:
        atomic_write_bytes(path, content)  # ECP-PRM-008: fsync, then replace
    except OSError as exc:
        raise CodedError(WEX_ECP_010, f"cannot write the evidence packet: {exc}") from exc
    governing, dependencies = project_scope(catalog, primary)
    return selected_result(
        root,
        operation="evidence",
        primary=primary,
        related=[catalog[item] for item in dependencies if item in catalog],
        governing=governing,
        dependencies=dependencies,
        done=[
            f"{'Rebound' if action == 'rebind' else 'Wrote'} the {checkpoint} evidence packet of {artifact_id} "
            f"at {relative} to formal snapshot {snapshot}."
        ],
        after=[{"id": artifact_id, "status": primary.status}],
        writes=[{"id": artifact_id, "path": relative, "fields": list(EVIDENCE_HEADER_KEYS)}],
    )


def _evaluate(name: str, predicate: Mapping[str, Any], context: CheckpointContext) -> tuple[str, str]:
    if name == "artifact_status":
        statuses = predicate.get("statuses", [])
        if context.artifact.status in statuses:
            return "pass", f"{context.artifact.artifact_id} status is {context.artifact.status}."
        return "fail", f"{context.artifact.artifact_id} status {context.artifact.status} is not one of {', '.join(statuses)}."
    if name == "formal_graph_valid":
        if context.scoped_errors:
            return "fail", f"Selected graph validation failed: {context.scoped_errors[0]['message']}"
        return "pass", "The selected formal graph is valid."
    if name == "repository_integrity":
        if context.repository_errors:
            return "fail", f"Repository integrity failed: {context.repository_errors[0]['message']}"
        return "pass", "No repository-integrity blocker prevents selected evaluation."
    if name == "execution_scope_declared":
        if context.declared_scope:
            return "pass", f"{context.artifact.artifact_id} declares {len(context.declared_scope)} normalized scope path(s)."
        return "not_assessable", f"{context.artifact.artifact_id} has no assessable execution scope."
    if name == "change_set_complete":
        if context.change_set.complete:
            return "pass", "The caller explicitly asserted that the declared change set is complete."
        return "not_assessable", "Change-set completeness was not asserted; absence of undeclared changes cannot be inferred."
    if name == "changed_paths_within_scope":
        if not context.change_set.complete:
            return "not_assessable", "Changed-path scope cannot pass without an explicit completeness assertion."
        outside = [path for path in context.change_set.paths if not path_is_admitted(path, context.admitted_scope)]
        if outside:
            return "fail", f"{WEX201}: changed path is outside execution scope: {outside[0]}"
        return "pass", f"All {len(context.change_set.paths)} declared changed path(s) are within execution scope."
    if name == "start_preflight_ready":
        return _preflight_status(context, "start")
    if name == "review_preflight_ready":
        return _preflight_status(context, "review")
    if name == "review_evidence_available":
        return review_evidence(context)
    if name == "authoring_ready":
        return authoring_ready(context.artifact, context.root)
    if name == "release_unit_ready":
        return release_unit_ready(context.artifact, context.root, context.catalog)
    if name == "decision_gate_clear":
        return decision_gate_clear(context)
    raise ContractError(f"unknown predicate evaluator {name}")


def _aggregate(statuses: Iterable[str]) -> str:
    """ECP-PRM-021: the first status of the contract's `aggregation` that is present wins."""

    values = set(statuses)
    order = aggregation_order()
    return next((status for status in order if status in values), order[-1])


def _evidence(descriptors: Iterable[Mapping[str, Any]], artifact_id: str, checkpoint: str) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for descriptor in descriptors:
        result.append(
            {
                "kind": str(descriptor.get("kind", "result")),
                "reference": str(descriptor.get("reference", "")).replace("{artifact_id}", artifact_id).replace("{checkpoint}", checkpoint),
            }
        )
    return result


def _gate_results(
    gate_ids: Iterable[str],
    gates: Mapping[str, Mapping[str, Any]],
    context: CheckpointContext,
    predicate_ids: Iterable[str] | None = None,
) -> list[dict[str, Any]]:
    selected = None if predicate_ids is None else set(predicate_ids)
    result: list[dict[str, Any]] = []
    for gate_id in gate_ids:
        gate = gates[gate_id]
        if context.checkpoint not in gate["checkpoints"]:
            raise CodedError(WEX210, f"gate {gate_id} does not apply at checkpoint {context.checkpoint}"
            )
        predicates: list[dict[str, Any]] = []
        for predicate in gate["predicates"]:
            if selected is not None and predicate["id"] not in selected:
                continue
            if context.checkpoint not in effective_checkpoints(gate, predicate):
                continue
            status, message = _evaluate(predicate["evaluator"], predicate, context)
            predicates.append(
                {
                    "id": predicate["id"],
                    "status": status,
                    "evidence": _evidence(predicate["required_evidence"], context.artifact.artifact_id, context.checkpoint),
                    "message": message,
                }
            )
        result.append({"id": gate_id, "status": _aggregate(item["status"] for item in predicates), "predicates": predicates})
    return result


def build_context(
    root: Path,
    report: Any,
    catalog: Mapping[str, Any],
    primary: Any,
    *,
    checkpoint: str,
    change_set: ChangeSet,
    target: str | None = None,
) -> CheckpointContext:
    """The one context builder `check` and `transition` share (ECP-KRN-004)."""

    scoped, repository_errors, unrelated = classify_diagnostics(report, catalog, primary, root)
    try:
        scope = execution_scope(primary) if primary.artifact_type == "work_order" else ()
    except HarnessError:
        scope = ()
    return CheckpointContext(
        root=root,
        artifact=primary,
        catalog=catalog,
        report=report,
        scoped_errors=scoped,
        repository_errors=repository_errors,
        unrelated_count=unrelated,
        declared_scope=scope,
        # ECP-CHG-007: the selected work order's own artifact path is admitted by
        # construction; only `transition` writes it and it is in every Git diff
        # after the work order's own approval and start.
        admitted_scope=(
            *scope,
            primary.path.relative_to(root).as_posix(),
            # ECP-PRB-002 (amended): the harness retains the packet and the handoff
            # result under the work order's packet directory; harness-written
            # evidence at its own path is admitted with the work order's file.
            *(
                (evidence_packet_path(root, primary, "handoff").parent.relative_to(root).as_posix() + "/",)
                if primary.artifact_type == "work_order" else ()
            ),
            # ECP-ADM-001: the verification and release records that name the
            # selected work order, and their evaluator evidence, as exact paths.
            *(own_record_paths(root, catalog, primary.artifact_id) if primary.artifact_type == "work_order" else ()),
            # SPEC-RSK-010 RSK-MGT-026: a risk recorded mid-execution, added in the
            # work order's own domain, never widens the declared scope.
            *risk_admissions(root, primary, change_set),
        ),
        change_set=change_set,
        checkpoint=checkpoint,
        formal_snapshot_sha256=formal_snapshot_digest(root, report.artifacts),
        target=target,
    )


STRUCTURAL_GATE = "QG-STRUCTURAL"


def transition_gate_results(
    quality_gates: Mapping[str, Any],
    gates: Mapping[str, Mapping[str, Any]],
    context: CheckpointContext,
    *,
    structural: Iterable[Mapping[str, Any]] = (),
) -> list[dict[str, Any]]:
    """Evaluate the contract's transition bindings for one edge (ECP-KRN-004, -005).

    Gate predicates come from `QUALITY_GATES.json`; the graph-structural checks
    the caller evaluated are appended as the synthetic `QG-STRUCTURAL` gate so a
    refusal always names its check.
    """

    if context.target is None:
        raise CodedError(WEX210, "the transition checkpoint requires a target state")
    predicate_ids, _ = transition_binding(
        quality_gates, lifecycle_family(context.artifact.artifact_type), context.artifact.artifact_type, context.target
    )
    gate_order: list[str] = []
    for gate_id, gate in gates.items():
        if any(str(item["id"]) in predicate_ids for item in gate["predicates"]) and gate_id not in gate_order:
            gate_order.append(gate_id)
    results = _gate_results(gate_order, gates, context, predicate_ids=predicate_ids)
    structural_items = [dict(item) for item in structural]
    if structural_items:
        results.append({
            "id": STRUCTURAL_GATE,
            "status": _aggregate(item["status"] for item in structural_items),
            "predicates": structural_items,
        })
    return results


def _resolve_change_set(
    root: Path,
    report: Any,
    primary: Any,
    *,
    checkpoint: str,
    from_git: str | None,
    change_manifest: Path | None,
    changed_paths: Iterable[str],
    changes_complete: bool,
) -> tuple[str | None, bool, ChangeSet]:
    """Rebind a self-binding handoff packet, derive the change set, and retain the handoff result path in it."""
    rebound: str | None = None
    self_binding = checkpoint == "handoff" and from_git is not None and primary.artifact_type == "work_order"
    if self_binding:
        # ECP-SBH-001: the run binds the packet to the snapshot it evaluates, before Git
        # derives the change set, so a rewritten packet is a change-set member like any other.
        from datetime import datetime, timezone

        rebound = rebind_handoff_packet(
            root,
            primary,
            formal_snapshot_digest(root, report.artifacts),
            datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
    if from_git is not None:
        change_set = git_change_set(root, from_git)
    elif change_manifest is not None:
        change_set = parse_change_manifest(root, change_manifest)
    else:
        change_set = declared_change_set(changed_paths, complete=changes_complete)
    if self_binding:
        # ECP-SBH-004: the retained result path is evaluated as a member whether or not
        # this run's write happened yet, so the first completed run is the fixed point.
        retained = evidence_packet_path(root, primary, "handoff").with_name("handoff.json").relative_to(root).as_posix()
        if retained not in change_set.paths:
            change_set = ChangeSet(
                paths=(*change_set.paths, retained), complete=change_set.complete, source=change_set.source, added=change_set.added
            )
    return rebound, self_binding, change_set


def _handoff_trap_blockers(
    root: Path,
    catalog: Mapping[str, Any],
    primary: Any,
    *,
    artifact_id: str,
    checkpoint: str,
    pull_request_body: Path | None,
) -> list[str]:
    """Collect the work-order handoff trap blockers: orphaned ready records and pull-request body findings."""
    trap_blockers: list[str] = []
    if checkpoint == "handoff" and primary.artifact_type == "work_order":
        trap_blockers.extend(
            f"{W_ADS_002}: {message}" for message in orphaned_ready_records(root, catalog.values(), artifact_id)
        )
        if pull_request_body is not None:
            trap_blockers.extend(f"{W_ADS_001}: {message}" for message in pull_request_body_findings(root, pull_request_body))
    return trap_blockers


def _corrective_action(
    current_step: Mapping[str, Any],
    gate_results: list[dict[str, Any]],
    *,
    artifact_id: str,
    checkpoint: str,
    formal_snapshot_sha256: str,
) -> tuple[str, dict[str, Any]]:
    """Select the corrective action and command for a blocked checkpoint from its first failing predicate."""
    first_failing = next(
        (
            predicate
            for gate in gate_results
            for predicate in gate["predicates"]
            if predicate["status"] != "pass"
        ),
        None,
    )
    corrective_step = current_step
    if checkpoint == "scope":
        declared_forms = dict(current_step.get("corrective") or {})
        for predicate_id, form in SCOPE_CHECKPOINT_CORRECTIVE.items():
            declared_forms.setdefault(predicate_id, {
                **form,
                **({"argv": [item.replace("{artifact_id}", artifact_id) for item in form["argv"]]} if "argv" in form else {}),
            })
        corrective_step = {**current_step, "corrective": declared_forms}
    action, next_command = corrective_response(
        corrective_step, first_failing, formal_snapshot_sha256=formal_snapshot_sha256
    )
    evaluated = ["harnessctl", "check", ".", "--artifact", artifact_id, "--checkpoint", checkpoint]
    if next_command.get("kind") == "command" and list(next_command.get("argv", [])) == evaluated:
        raise CodedError(WEX_ADS_001, "the corrective command repeats the evaluated command")
    return action, next_command


def check_workflow(
    repository: Path,
    *,
    artifact_id: str,
    checkpoint: str,
    procedure_id: str | None = None,
    changed_paths: Iterable[str] = (),
    changes_complete: bool = False,
    change_manifest: Path | None = None,
    pull_request_body: Path | None = None,
    target: str | None = None,
    from_git: str | None = None,
    retain_handoff: bool = False,
) -> dict[str, Any]:
    if from_git is not None and (list(changed_paths) or changes_complete or change_manifest is not None):
        raise CodedError(WEX_ECP_002, "--from-git is mutually exclusive with --changed-path, --changes-complete and --change-manifest"
        )
    if checkpoint not in CHECKPOINTS:  # ECP-PRM-012: the contract module's set
        raise CodedError(WEX210, "public check checkpoint must be start, pre-action, transition, handoff, or scope")
    if checkpoint == "transition" and not target:
        raise CodedError(WEX210, "--target is required for the transition checkpoint")
    if checkpoint != "transition" and target:
        raise CodedError(WEX210, "--target applies only to the transition checkpoint")
    root = ensure_target(repository, must_exist=True)
    _, quality_gates, rules, procedures, gates = load_validated_contracts()
    _, report = validated_repository(root)
    try:
        catalog = artifact_catalog(report)
    except HarnessError as exc:
        raise CodedError(WEX210, f"{exc}") from exc
    primary = catalog.get(artifact_id)
    if primary is None:
        raise CodedError(WEX210, f"unknown artifact ID: {artifact_id}")
    if primary.artifact_type not in {"work_order", "verification_record", "release_record"}:
        raise CodedError(WEX210, "check --checkpoint accepts only WO, VREC, or RLS artifacts "
            "(a decision is disposed with harnessctl decide; a risk is raised with harnessctl raise-risk and listed with harnessctl risks)"
        )
    if checkpoint == "scope" and primary.artifact_type != "work_order":
        raise CodedError(WEX210, "the scope checkpoint applies only to a work order")
    governing, dependencies = project_scope(catalog, primary)
    related = [catalog[item] for item in dependencies if item in catalog]
    rule, rule_context = select_rule(rules, primary, related=related)
    selected_procedure = str(rule["procedure_id"])
    alternatives = list(rule.get("alternative_procedure_ids", []))
    if checkpoint == "pre-action" and procedure_id is None:
        raise CodedError(WEX220, "--procedure is required for pre-action")
    if procedure_id is not None:
        if procedure_id not in {selected_procedure, *alternatives}:
            raise CodedError(WEX220, f"procedure {procedure_id} is not selected by workflow rule {rule['id']}")
        selected_procedure = procedure_id
    rebound, self_binding, change_set = _resolve_change_set(
        root,
        report,
        primary,
        checkpoint=checkpoint,
        from_git=from_git,
        change_manifest=change_manifest,
        changed_paths=changed_paths,
        changes_complete=changes_complete,
    )
    validate_changed_targets(root, change_set)
    context = build_context(
        root, report, catalog, primary, checkpoint=checkpoint, change_set=change_set, target=target
    )
    scoped, repository_errors, unrelated = context.scoped_errors, context.repository_errors, context.unrelated_count
    scope = context.declared_scope
    gate_ids = list(rule["gate_ids"])
    if checkpoint == "scope":
        # ECP-SCP-002: scope is judged against the diff in every lifecycle state, so
        # the gate comes from the contract, not from the rule the state selects; the
        # gate's predicate-level checkpoints leave only the scope predicates in play.
        gate_ids = [SCOPE_CHECKPOINT_GATE]
    resolved = resolve_procedure(
        procedures,
        selected_procedure,
        {
            "artifact_id": artifact_id,
            "status": primary.status,
            "changed_paths": list(change_set.paths),
            **rule_context,
        },
    )
    if checkpoint == "pre-action":
        first = resolved["steps"][0]
        gate_ids = list(dict.fromkeys([*gate_ids, *first.get("gate_ids", [])]))
    if checkpoint == "transition":
        structural = structural_precondition_results(root, catalog, catalog, primary, str(target), None)
        gate_results = transition_gate_results(quality_gates, gates, context, structural=structural)
    else:
        gate_results = _gate_results(gate_ids, gates, context)
    compliance_status = _aggregate([item["status"] for item in gate_results] or ["pass"])
    passed = compliance_status == "pass" and not scoped and not repository_errors
    outcome = "completed" if passed else "blocked"
    current_step = select_current_step(resolved, checkpoint=checkpoint, passed=passed)
    predicate_blockers = [
        f"{predicate['id']}: {predicate['message']}"
        for gate in gate_results
        for predicate in gate["predicates"]
        if predicate["status"] != "pass"
    ]
    finding_blockers = [
        f"{item['code']}: {item['message']}"
        for item in [*repository_errors, *scoped]
    ]
    trap_blockers = _handoff_trap_blockers(
        root, catalog, primary, artifact_id=artifact_id, checkpoint=checkpoint, pull_request_body=pull_request_body
    )
    if trap_blockers:
        passed = False
        outcome = "blocked"
        current_step = select_current_step(resolved, checkpoint=checkpoint, passed=False)
    blockers = [*predicate_blockers, *finding_blockers, *trap_blockers]
    action = (
        str(current_step.get("decision", "Provide the required decision"))
        if current_step["kind"] == "decision"
        else "Run the bound command"
        if current_step["kind"] == "command"
        else "Follow the bound reference"
    )
    next_command = command_or_response(current_step)
    if not passed:
        action, next_command = _corrective_action(
            current_step,
            gate_results,
            artifact_id=artifact_id,
            checkpoint=checkpoint,
            formal_snapshot_sha256=context.formal_snapshot_sha256,
        )
    restitution = {
        "outcome": outcome,
        "done": [f"Evaluated {checkpoint} compliance for {artifact_id}."],
        "not_done": [] if passed else [f"The {checkpoint} checkpoint did not pass."],
        "blocked_by": blockers,
        "current_lifecycle_state": [f"{artifact_id} is {primary.status}."],
        "decision_required": decision_required(current_step) if passed else None,
        "next": {"procedure_id": selected_procedure, "step_id": current_step["id"], "action": action},
        "command_or_response": next_command,
        "alternatives": [f"Use complete alternative procedure {identifier}." for identifier in alternatives],
    }
    if primary.artifact_type == "work_order" and passed:
        # ECP-DLG-010: a class-bearing work order is told when the decision due is delegated.
        from se_harness.gate_source import DelegationError, delegation_overlay

        try:
            restitution = delegation_overlay(
                root, work_order_metadata=primary.metadata, work_order_path=primary.path,
                artifact_id=artifact_id, restitution=restitution,
            )
        except DelegationError:
            # A misconfigured gate source never turns a completed projection into a blocked
            # one; the delegated route itself refuses with the coded reason when attempted.
            pass
    result = build_result(
        operation="check",
        outcome=outcome,
        primary=artifact_id,
        artifacts=[artifact_id],
        governing=governing,
        dependencies=dependencies,
        declared_paths=scope,
        changed_paths=change_set.paths,
        change_set_complete=change_set.complete,
        compliance={
            "checkpoint": checkpoint,
            "workflow_rule_id": rule["id"],
            "procedure_id": selected_procedure,
            "status": compliance_status if not (scoped or repository_errors) else "fail",
            "gates": gate_results,
            "formal_snapshot_sha256": context.formal_snapshot_sha256,
            "change_set_source": change_set.source,
        },
        procedure={"id": selected_procedure, "current_step": current_step["id"], "steps": resolved["steps"]},
        restitution=restitution,
        before=[{"id": artifact_id, "status": primary.status}],
        after=[{"id": artifact_id, "status": primary.status}],
        scoped_blockers=scoped,
        repository_blockers=repository_errors,
        unrelated_count=unrelated,
        # ECP-SBH-005: the rebind is reported outside the canonical restitution block,
        # so run one (which rebinds) and a repeat (which does not) share one digest.
        writes=(
            [{"id": artifact_id, "path": rebound, "fields": ["formal_snapshot_sha256", "rebound_at"]}]
            if rebound is not None
            else []
        ),
    )
    if retain_handoff and self_binding and result["operation"]["outcome"] == "completed":
        # ECP-PRB-002 (amended): a completed Git-derived handoff result is retained beside
        # the packet by the harness, never authored by the agent; ECP-ENG-010: from this
        # run's own catalog, not a second validation. ECP-SBH-005: the retained entry
        # joins the rebind entry rather than replacing it.
        retained = retain_handoff_result(root.resolve(), primary, result)
        result["mutation"]["writes"] = [
            *result["mutation"]["writes"],
            {"id": artifact_id, "path": retained, "fields": ["result_sha256"]},
        ]
    return result


def _rule_prose(rule: Mapping[str, Any], context: Mapping[str, str]) -> tuple[list[str], list[str]]:
    block = rule.get("restitution", {})
    done = [str(item).format_map(context) for item in block.get("done", [])]
    current = [str(item).format_map(context) for item in block.get("current_lifecycle_state", [])]
    return done, current


def selected_result(
    root: Path,
    *,
    operation: str,
    primary: Any,
    related: Iterable[Any] = (),
    artifacts: Iterable[str] | None = None,
    governing: Iterable[str] = (),
    dependencies: Iterable[str] = (),
    done: Iterable[str] | None = None,
    blocked_by: Iterable[str] = (),
    before: Iterable[Mapping[str, str]] = (),
    after: Iterable[Mapping[str, str]] = (),
    scoped_blockers: Iterable[Mapping[str, Any]] = (),
    repository_blockers: Iterable[Mapping[str, Any]] = (),
    unrelated_count: int = 0,
    writes: Iterable[Mapping[str, Any]] = (),
    checkpoint: str = "pre-action",
    gates: Iterable[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """Build the one schema-2 result for a selected artifact (ECP-KRN-001, -003).

    `check`, `transition`, `capture-verification` and `prepare-release` all
    render through here: `select_rule` over the primary and its related
    artifacts picks the workflow rule, the rule's procedure supplies the typed
    next step, and the rule's `restitution` prose supplies what was done and
    the lifecycle state. A blocked result keeps the rule's next step but says
    nothing was done.
    """

    _, _, rules, procedures, _ = load_validated_contracts()
    related_items = list(related)
    rule, rule_context = select_rule(rules, primary, related=related_items)
    resolved = resolve_procedure(
        procedures,
        str(rule["procedure_id"]),
        {"artifact_id": primary.artifact_id, "status": primary.status, **rule_context},
    )
    step = resolved["steps"][0]
    blockers = [str(item) for item in blocked_by]
    blocked = bool(blockers)
    gate_results = [dict(item) for item in gates]
    rule_done, current = _rule_prose(rule, rule_context)
    scope: tuple[str, ...] = ()
    if primary.artifact_type == "work_order":
        try:
            scope = execution_scope(primary)
        except HarnessError:
            scope = ()
    restitution = {
        "outcome": "blocked" if blocked else "completed",
        "done": [] if blocked else [str(item) for item in (rule_done if done is None else done)],
        "not_done": [f"The selected {operation} operation remains incomplete."] if blocked else [],
        "blocked_by": blockers,
        "current_lifecycle_state": ["No lifecycle state was changed."] if blocked else current,
        "decision_required": decision_required(step) if not blocked else None,
        "next": {
            "procedure_id": rule["procedure_id"],
            "step_id": step["id"],
            "action": str(step.get("decision", "Run the bound command" if step["kind"] == "command" else "Follow the bound reference")),
        },
        "command_or_response": command_or_response(step),
        "alternatives": [
            f"Use complete alternative procedure {identifier}."
            for identifier in rule.get("alternative_procedure_ids", [])
        ],
    }
    if operation == "check" and primary.artifact_type == "work_order" and not blocked:
        # ECP-DLG-010: the projection tells a class-bearing work order when its decision is delegated.
        from se_harness.gate_source import DelegationError, delegation_overlay

        try:
            restitution = delegation_overlay(
                root, work_order_metadata=primary.metadata, work_order_path=primary.path,
                artifact_id=primary.artifact_id, restitution=restitution,
            )
        except DelegationError:
            pass
    return build_result(
        operation=operation,
        outcome="blocked" if blocked else "completed",
        primary=primary.artifact_id,
        artifacts=[primary.artifact_id] if artifacts is None else list(artifacts),
        governing=governing,
        dependencies=dependencies,
        declared_paths=scope,
        changed_paths=[],
        change_set_complete=False,
        compliance={
            "checkpoint": checkpoint,
            "workflow_rule_id": rule["id"],
            "procedure_id": rule["procedure_id"],
            "status": (
                _aggregate(item["status"] for item in gate_results)
                if gate_results and not blocked
                else "fail" if blocked else "not_assessable"
            ),
            "gates": gate_results,
        },
        procedure={"id": rule["procedure_id"], "current_step": step["id"], "steps": resolved["steps"]},
        restitution=restitution,
        before=list(before),
        after=list(after),
        scoped_blockers=list(scoped_blockers),
        repository_blockers=list(repository_blockers),
        unrelated_count=unrelated_count,
        writes=list(writes),
    )


def remediation_result(
    operation: str,
    primary: str | None,
    finding: Mapping[str, Any],
    *,
    repository_blocker: bool = False,
) -> dict[str, Any]:
    """Build the schema-2 result of an operation that could not select or act."""

    workflow, _, _, procedures, _ = load_validated_contracts()
    failure = workflow["failure"]
    procedure_id = str(failure["procedure_id"])
    steps: list[dict[str, Any]] = []
    if primary:
        try:
            steps = resolve_procedure(procedures, procedure_id, {"artifact_id": primary})["steps"]
        except ProcedureError:
            steps = []
    step_id = steps[0]["id"] if steps else f"STEP-{procedure_id.removeprefix('PROC-')}-FOCUS"
    message = str(finding.get("message", ""))
    _, current = _rule_prose(failure, {"message": message})
    restitution = {
        "outcome": "blocked",
        "done": [],
        "not_done": ["The requested workflow operation remains incomplete."],
        "blocked_by": [f"{finding.get('code', 'WEX')}: {message}"],
        "current_lifecycle_state": current,
        "decision_required": None,
        "next": {"procedure_id": procedure_id, "step_id": step_id, "action": "remediate"},
        "command_or_response": (
            {"kind": "command", "argv": ["harnessctl", "check", ".", "--artifact", primary]}
            if primary
            else {"kind": "response", "value": "Resolve the reported blocker, then run harnessctl check . to obtain the selected context."}
        ),
        "alternatives": [],
    }
    return build_result(
        operation=operation,
        outcome="blocked",
        primary=primary or "",
        artifacts=[primary] if primary else [],
        governing=[],
        dependencies=[],
        declared_paths=[],
        changed_paths=[],
        change_set_complete=False,
        compliance={
            "checkpoint": "pre-action",
            "workflow_rule_id": str(failure["id"]),
            "procedure_id": procedure_id,
            "status": "fail",
            "gates": [],
        },
        procedure={"id": procedure_id, "current_step": step_id, "steps": steps},
        restitution=restitution,
        scoped_blockers=[] if repository_blocker else [dict(finding)],
        repository_blockers=[dict(finding)] if repository_blocker else [],
    )


def ensure_governed_checkpoint(
    repository: Path,
    artifact_ids: Iterable[str],
    *,
    report: Any | None = None,
    catalog: Mapping[str, Any] | None = None,
) -> None:
    """Fail closed on contract or repository-integrity damage before a mutation."""

    root = ensure_target(repository, must_exist=True)
    try:
        load_validated_contracts()
    except ContractError as exc:
        raise CodedError(WEX210, f"invalid machine policy: {exc}") from exc
    if report is None:
        _, report = validated_repository(root)
    if catalog is None:
        catalog = artifact_catalog(report)
    for artifact_id in artifact_ids:
        if artifact_id not in catalog:
            raise CodedError(WEX210, f"unknown governed artifact {artifact_id}")
    repository_errors = [item for item in report.errors if item.code in REPOSITORY_ERROR_CODES]
    if repository_errors:
        raise CodedError(WEX210, f"repository integrity prevents governed action: {repository_errors[0].message}")
    # The authoring and release-unit predicates a definition needs before it
    # leaves draft are evaluated by the contract's transition bindings
    # (QGP-G1/G2-AUTHORING, QGP-G5P-RELEASE-UNIT), not re-implemented here (WO-ECP-009).
