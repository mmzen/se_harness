"""Deterministic, provider-neutral governance workflow execution.

The module owns selected-scope projection, lifecycle policy, transaction
planning, atomic application, and the semantic result rendered by every agent.
It intentionally uses only the Python standard library.
"""

from __future__ import annotations

import json
import os
import re
import tomllib

from se_harness import front_matter
from se_harness.gate_source import (
    DELEGATED_RIGHTS,
    DELEGATED_ROLE,
    DELEGATED_TRANSITIONS,
    DelegationError,
    authorize_delegated_right,
    delegated_reason,
)
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping

from se_harness.installer import HarnessError, ensure_target, safe_destination
from se_harness.integrity import stage_bytes
from se_harness.engine import validate_engineering_artifacts as _validator_module
from se_harness.workflow_contract import lifecycle_family, load_validated_contracts
from se_harness.engine.validation_core import relation_targets
from se_harness import mutation_guard
from se_harness.preflight import run_preflight
from se_harness.risks import refuse_bare_risk_transition
from se_harness.workflow_compliance import (
    build_context,
    declared_change_set,
    ensure_governed_checkpoint,
    execution_scope,
    remediation_result,
    selected_result,
    transition_gate_results,
)
from se_harness.workflow_result import restitution_digest
from se_harness.codes import CodedError, E001, E003, WEX001, WEX190, WEX_ECP_001

# The seams of this module (SPEC-ECP-024 ECP-ENG-019, ECP-ENG-020): every public name stays importable here.
from se_harness.repository_graph import (  # noqa: F401
    PRIMARY_TYPES,
    RepositoryWorkflowError,
    artifact_catalog,
    diagnostic_payload,
    inverse_targets,
    project_scope,
    validated_repository,
    work_scope,
)
from se_harness.workflow_edges import (  # noqa: F401
    LIFECYCLE_REGISTRY,
    PreconditionError,
    TRANSITIONS,
    WORKFLOW_CONTRACT,
    grants_authority,
    revision_policy,
    structural_precondition_results,
    validate_edge,
)


@dataclass(frozen=True)
class PlannedWrite:
    artifact_id: str
    path: Path
    original: bytes
    replacement: bytes
    fields: tuple[str, ...]


@dataclass(frozen=True)
class PlannedInput:
    path: Path
    original: bytes


@dataclass(frozen=True)
class TransitionPlan:
    root: Path
    inputs: tuple[PlannedInput, ...]
    writes: tuple[PlannedWrite, ...]
    result: dict[str, Any]


def _state(items: Iterable[tuple[str, str]]) -> list[dict[str, str]]:
    return [{"id": artifact_id, "status": status} for artifact_id, status in sorted(items)]


def failed_result(
    kind: str,
    primary: str | None,
    message: str,
    *,
    code: str = WEX001,
    repository_blocker: bool = False,
) -> dict[str, Any]:
    finding = {"code": code, "message": _terminal_text(message)}
    return remediation_result(kind, primary, finding, repository_blocker=repository_blocker)


def _terminal_text(value: object) -> str:
    text = str(value)
    return "".join(character if character >= " " and character != "\x7f" else "?" for character in text)


def project_selected(
    repository: Path,
    artifact_id: str | None = None,
    *,
    include_background: bool = False,
) -> dict[str, Any]:
    """Project the selected artifact's rule, procedure, next step and execution context; evaluate no gate.

    This is `check` without a checkpoint (SPEC-ECP-011, ECP-ONE-001/-002); the
    `focus` alias that shared it was removed after 0.10.0 (SPEC-ECP-013). Since
    WO-ECP-019 it carries the `context` object `next` introduced (SPEC-ECP-014,
    ECP-CTX-001 to -003) and selects the single in_progress work order when no
    artifact is named; `next` is its alias for one release.
    """

    root = ensure_target(repository, must_exist=True)
    _, report = validated_repository(root)
    catalog = artifact_catalog(report)
    if artifact_id is None:
        candidates = sorted(
            item.artifact_id
            for item in catalog.values()
            if item.artifact_type == "work_order" and item.status == "in_progress"
        )
        if len(candidates) != 1:
            raise CodedError(WEX_ECP_001, f"{len(candidates)} work orders are in_progress; name one with --artifact"
                + (f" ({', '.join(candidates)})" if candidates else "")
            )
        artifact_id = candidates[0]
    primary = catalog.get(artifact_id)
    if primary is None:
        raise HarnessError(f"unknown artifact ID: {artifact_id}")
    if primary.artifact_type not in PRIMARY_TYPES:
        raise HarnessError("check accepts only WO, VREC, RLS, or DEC artifacts")
    governing, dependencies = project_scope(catalog, primary)
    scope_paths = {
        catalog[item].path.resolve()
        for item in governing | dependencies | {artifact_id}
        if item in catalog
    }
    scoped: list[dict[str, str]] = []
    repository: list[dict[str, str]] = []
    background: list[dict[str, Any]] = []
    counts: dict[tuple[str, str], int] = {}
    for item in report.errors:
        diagnostic = diagnostic_payload(item)
        candidate = safe_destination(root, Path(item.path))
        if item.code in {E001, E003}:
            repository.append(diagnostic)
        elif candidate.resolve() in scope_paths:
            scoped.append(diagnostic)
        else:
            counts[(item.code, item.plane)] = counts.get((item.code, item.plane), 0) + 1
    for item in report.warnings:
        candidate = safe_destination(root, Path(item.path))
        if candidate.resolve() in scope_paths:
            continue
        counts[(item.code, item.plane)] = counts.get((item.code, item.plane), 0) + 1
    if include_background:
        for (code, plane), count in sorted(counts.items()):
            background.append({"code": code, "plane": plane, "count": count, "message": f"{count} unrelated finding(s)"})
    elif counts:
        total = sum(counts.values())
        background.append({
            "code": WEX190,
            "count": total,
            "message": f"{total} unrelated finding(s); use --include-background for categories",
        })
    blockers = [*repository, *scoped]
    projected = selected_result(
        root,
        operation="check",
        primary=primary,
        related=[catalog[item] for item in dependencies if item in catalog],
        governing=governing,
        dependencies=dependencies,
        blocked_by=[f"{item.get('code', 'WEX')}: {item.get('message', '')}" for item in blockers],
        before=[{"id": artifact_id, "status": primary.status}],
        after=[{"id": artifact_id, "status": primary.status}],
        scoped_blockers=scoped,
        repository_blockers=repository,
        unrelated_count=sum(int(item.get("count", 0)) for item in background),
    )
    declared: tuple[str, ...] = ()
    if primary.artifact_type == "work_order":
        try:
            declared = execution_scope(primary)
        except HarnessError:
            declared = ()
    command = projected["restitution"]["command_or_response"]
    step = projected["restitution"]["next"]
    result = dict(projected)
    result["context"] = {
        "reading_manifest": list(_reading_manifest(root, catalog, primary, report)),
        "governing": list(projected["scope"]["governing"]),
        "declared_paths": list(declared),
        "state": {"status": primary.status, "family": lifecycle_family(primary.artifact_type)},
        "next": {
            "argv": list(command.get("argv", [])) if command.get("kind") == "command" else [],
            "procedure_id": step["procedure_id"],
            "step_id": step["step_id"],
        },
        "decision_required": projected["restitution"]["decision_required"],
    }
    result["result_sha256"] = restitution_digest(result)
    return result


def _next_phase(status: str) -> str:
    return "start" if status in {"approved", "in_progress"} else "review"


def _reading_manifest(root: Path, catalog: Mapping[str, Any], primary: Any, report: Any | None = None) -> tuple[str, ...]:
    """The preflight reading manifest for the phase the selected state implies (ECP-NXT-005).

    A work order reads its own preflight. A verification or release record has
    no preflight of its own; it reads the review manifest of the first work
    order it verifies or releases, which is the chain a reviewer needs.
    """

    if primary.artifact_type == "work_order":
        work_order_id, phase = primary.artifact_id, _next_phase(primary.status)
    else:
        relation = "verifies_work_order" if primary.artifact_type == "verification_record" else "releases_work"
        targets = sorted(relation_targets(primary, relation))
        if not targets:
            return ()
        work_order_id, phase = targets[0], "review"
    try:
        return tuple(run_preflight(root, work_order_id=work_order_id, phase=phase, report=report).reading_manifest)
    except HarnessError:
        return ()


def _split_document(data: bytes) -> tuple[list[str], str, str, str]:
    # ECP-PRM-005: the one parser; the document's newline and BOM are kept for the write-back.
    document = front_matter.split_document(data, error=HarnessError)
    return list(document.front_lines), document.body, document.newline, document.opening


def _top_level_end(lines: list[str]) -> int:
    return next((index for index, line in enumerate(lines) if line.startswith("[")), len(lines))


def _set_scalar(lines: list[str], field: str, value: str) -> None:
    encoded = f"{field} = {json.dumps(value)}"
    end = _top_level_end(lines)
    pattern = re.compile(rf"^{re.escape(field)}\s*=")
    for index in range(end):
        if pattern.match(lines[index]):
            lines[index] = encoded
            return
    lines.insert(end, encoded)


def _set_relation(lines: list[str], relation: str, values: list[str]) -> None:
    try:
        start = lines.index("[relations]") + 1
    except ValueError as exc:
        raise HarnessError("formal artifact has no relations table") from exc
    end = next((index for index in range(start, len(lines)) if lines[index].startswith("[")), len(lines))
    encoded = f"{relation} = [" + ", ".join(json.dumps(item) for item in values) + "]"
    pattern = re.compile(rf"^{re.escape(relation)}\s*=")
    for index in range(start, end):
        if pattern.match(lines[index]):
            lines[index] = encoded
            return
    # A new relation joins the table's last row, above the blank lines that separate tables.
    while end > start and lines[end - 1] == "":
        end -= 1
    lines.insert(end, encoded)


def _set_disposition(lines: list[str], fields: Mapping[str, Any]) -> None:
    """Write the decision's `[disposition]` table before its lifecycle events (SPEC-DCM-001 rule 6)."""

    start = next((index for index, line in enumerate(lines) if line.strip() == "[disposition]"), None)
    if start is not None:
        end = next((index for index in range(start + 1, len(lines)) if lines[index].startswith("[")), len(lines))
        del lines[start:end]
    insert_at = next((index for index, line in enumerate(lines) if line.strip() == "[[lifecycle_events]]"), len(lines))
    while insert_at > 0 and lines[insert_at - 1] == "":
        insert_at -= 1
    rendered = ["", "[disposition]"]
    for key in ("option", "label", "decided_by", "decided_at", "reason", "revisit", "scope"):
        value = fields.get(key)
        if value is None:
            continue
        if isinstance(value, list):
            rendered.append(f"{key} = [" + ", ".join(json.dumps(item) for item in value) + "]")
        else:
            rendered.append(f"{key} = {json.dumps(value)}")
    rendered.append("")
    lines[insert_at:insert_at] = rendered


def _append_event(lines: list[str], source: str, target: str, actor: str, now: str, reason: str | None) -> None:
    if lines and lines[-1] != "":
        lines.append("")
    lines.extend([
        "[[lifecycle_events]]",
        f"from = {json.dumps(source)}",
        f"to = {json.dumps(target)}",
        f"decided_at = {json.dumps(now)}",
        f"decided_by = {json.dumps(actor)}",
    ])
    if reason is not None:
        lines.append(f"reason = {json.dumps(reason)}")


def _mutate(
    data: bytes,
    artifact: Any,
    target: str,
    actor: str,
    reason: str | None,
    now: str,
    disposition: Mapping[str, Any] | None = None,
) -> tuple[bytes, tuple[str, ...]]:
    front, body, newline, opening = _split_document(data)
    fields = {"status", "updated", "lifecycle_events"}
    _set_scalar(front, "status", target)
    _set_scalar(front, "updated", now[:10])
    if artifact.artifact_type == "decision":
        assert disposition is not None
        _set_disposition(front, {**disposition, "decided_at": now})
        fields.add("disposition")
    elif artifact.artifact_type == "risk" and disposition is not None:
        # SPEC-RSK-010 RSK-MGT-018 to RSK-MGT-020: the answer copied from the paired
        # decision, and the work order or design record it names.
        table = {key: value for key, value in disposition.items() if key not in {"mitigated_by", "avoided_by"}}
        _set_disposition(front, {**table, "decided_at": now})
        fields.add("disposition")
        for relation in ("mitigated_by", "avoided_by"):
            targets = disposition.get(relation)
            if targets:
                _set_relation(front, relation, list(targets))
                fields.add(f"relations.{relation}")
    elif target == "verified" and artifact.artifact_type == "verification_record":
        if "prepared_at" in artifact.metadata or "verified_at" not in artifact.metadata:
            _set_scalar(front, "verified_at", now)
            fields.add("verified_at")
        _set_scalar(front, "verified_by", actor)
        fields.add("verified_by")
    elif target == "released" and artifact.artifact_type == "release_record":
        if "prepared_at" in artifact.metadata or "released_at" not in artifact.metadata:
            _set_scalar(front, "released_at", now)
            fields.add("released_at")
        if "prepared_at" in artifact.metadata or "authorized_by" not in artifact.metadata:
            _set_scalar(front, "authorized_by", actor)
            fields.add("authorized_by")
    elif target == "rejected":
        assert reason is not None
        _set_scalar(front, "rejected_at", now)
        _set_scalar(front, "rejected_by", actor)
        _set_scalar(front, "rejection_reason", reason)
        fields.update({"rejected_at", "rejected_by", "rejection_reason"})
    elif target == "superseded":
        assert reason is not None
        _set_scalar(front, "superseded_at", now)
        _set_scalar(front, "supersession_authorized_by", actor)
        _set_relation(front, "superseded_by", [reason])
        fields.update({"superseded_at", "supersession_authorized_by", "relations.superseded_by"})
    _append_event(front, artifact.status, target, actor, now, reason)
    output = opening + newline.join(front) + newline + "+++" + newline + body
    return output.encode("utf-8"), tuple(sorted(fields))


def _validate_artifacts(validator: Any, artifacts: list[Any], root: Path) -> list[Any]:
    policy = validator.load_revision_policy(root)
    errors: list[Any] = []
    errors.extend(validator.validate_common_metadata(artifacts, root))
    errors.extend(validator.validate_lifecycle_events(artifacts, root))
    errors.extend(validator.validate_type_specific_metadata(artifacts, root))
    errors.extend(validator.validate_relations(artifacts, root))
    traceability_errors, _ = validator.validate_architecture_traceability(artifacts, root)
    errors.extend(traceability_errors)
    assessment_errors, _ = validator.validate_decision_assessments(artifacts, root)
    errors.extend(assessment_errors)
    errors.extend(validator.validate_work_order_assurance(artifacts, root))
    errors.extend(validator.validate_work_order_execution_scope(artifacts, root))
    if hasattr(validator, "validate_decisions"):
        decision_errors, _ = validator.validate_decisions(artifacts, root)
        errors.extend(decision_errors)
    if hasattr(validator, "validate_risks"):
        risk_errors, _ = validator.validate_risks(artifacts, root)
        errors.extend(risk_errors)
    errors.extend(validator.validate_revision_consistency(
        artifacts,
        root,
        require_verified_work=policy["required_for_verified_work"],
    ))
    errors.extend(validator.validate_operating_contract_readiness(
        artifacts,
        root,
        require_verified_work=policy["required_for_verified_work"],
    ))
    errors.extend(validator.validate_requirement_coverage(artifacts, root))
    return sorted(set(errors))


def _proposed_artifacts(validator: Any, report: Any, replacements: Mapping[Path, bytes], root: Path) -> list[Any]:
    proposed: list[Any] = []
    for artifact in report.artifacts:
        replacement = replacements.get(artifact.path.resolve())
        if replacement is None:
            proposed.append(artifact)
            continue
        front, body, _, _ = _split_document(replacement)
        try:
            metadata = tomllib.loads("\n".join(front))
        except tomllib.TOMLDecodeError as exc:
            raise HarnessError(f"planned metadata for {artifact.artifact_id} is invalid: {exc}") from exc
        proposed.append(validator.Artifact(path=artifact.path, metadata=metadata, body=body.lstrip("\r\n")))
    return proposed


def plan_transition(
    repository: Path,
    transitions: Mapping[str, str],
    decisions: Mapping[str, str],
    reasons: Mapping[str, str],
    *,
    apply: bool = False,
    dispositions: Mapping[str, Mapping[str, Any]] | None = None,
) -> TransitionPlan:
    root = ensure_target(repository, must_exist=True)
    policy = revision_policy(root)  # ECP-PRM-011: read once per plan
    dispositions = dict(dispositions or {})
    if not transitions:
        raise HarnessError("at least one --set ID=STATUS is required")
    if set(decisions) != set(transitions):
        missing = sorted(set(transitions) - set(decisions))
        extra = sorted(set(decisions) - set(transitions))
        detail = []
        if missing:
            detail.append("missing decisions for " + ", ".join(missing))
        if extra:
            detail.append("decisions for unselected IDs " + ", ".join(extra))
        raise HarnessError("decision selection must exactly match transitions: " + "; ".join(detail))
    if not set(reasons).issubset(transitions):
        raise HarnessError("reasons may be supplied only for selected IDs")
    validator, report = validated_repository(root)
    effective_reasons: dict[str, str] = dict(reasons)
    if report.errors:
        first = report.errors[0]
        message = f"current artifact graph is invalid [{first.code}]: {first.message}"
        if first.code in {E001, E003}:
            raise RepositoryWorkflowError(message)
        raise HarnessError(message)
    catalog = artifact_catalog(report)
    ensure_governed_checkpoint(root, transitions, report=report, catalog=catalog)
    input_paths: set[Path] = set()
    for artifact in report.artifacts:
        input_paths.add(safe_destination(root, artifact.path.relative_to(root)))
        evidence_paths = artifact.metadata.get("evidence_paths", [])
        if isinstance(evidence_paths, list):
            for raw_path in evidence_paths:
                if isinstance(raw_path, str):
                    input_paths.add(safe_destination(root, Path(raw_path)))
    policy_path = safe_destination(root, Path(".engineering-harness.toml"))
    if policy_path.is_file():
        input_paths.add(policy_path)
    inputs = tuple(
        PlannedInput(path=path, original=path.read_bytes())
        for path in sorted(input_paths, key=lambda item: item.relative_to(root).as_posix())
    )
    now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ") if apply else ""
    replacements: dict[Path, bytes] = {}
    writes: list[PlannedWrite] = []
    before: list[tuple[str, str]] = []
    after: list[tuple[str, str]] = []
    for artifact_id, target in sorted(transitions.items()):
        artifact = catalog.get(artifact_id)
        if artifact is None:
            raise HarnessError(f"unknown artifact ID: {artifact_id}")
        disposition_fields = validate_edge(
            root, artifact, target, decisions[artifact_id], reasons.get(artifact_id), catalog, dispositions.get(artifact_id),
            policy=policy,  # ECP-PRM-011: the planner's one reading
        )
        if artifact.artifact_type == "decision" and disposition_fields is None:
            raise HarnessError(
                f"transition {artifact_id}: a decision is disposed with harnessctl decide . --artifact {artifact_id} --option OPTION-ID --decision ROLE --reason TEXT"
            )
        if artifact.artifact_type == "risk" and disposition_fields is None:
            # SPEC-RSK-010 RSK-MGT-021: raised or answered through its commands only.
            refuse_bare_risk_transition(artifact, target, reasons.get(artifact_id))
        if decisions[artifact_id] == DELEGATED_ROLE:
            # SPEC-ECP-006 ECP-DLG-002/-003/-005/-006/-007: the delegated route.
            right = DELEGATED_TRANSITIONS.get((lifecycle_family(artifact.artifact_type), artifact.status, target))
            try:
                reading = authorize_delegated_right(
                    root, work_order_metadata=artifact.metadata, work_order_path=artifact.path, right=right,
                )
            except DelegationError as exc:
                raise PreconditionError(exc.code, exc.message) from exc
            if apply:
                mutation_guard.require_mutation_authority(root, operation=DELEGATED_RIGHTS[str(right)])
            effective_reasons[artifact_id] = delegated_reason(str(right), reading, reasons.get(artifact_id))
        path = safe_destination(root, artifact.path.relative_to(root))
        original = path.read_bytes()
        # Plans intentionally expose no execution timestamp. A fixed valid value
        # permits complete graph validation without becoming retained data.
        rendered_now = now or "9999-12-31T23:59:59Z"
        replacement, fields = _mutate(
            original,
            artifact,
            target,
            decisions[artifact_id],
            effective_reasons.get(artifact_id),
            rendered_now,
            disposition_fields,
        )
        replacements[path.resolve()] = replacement
        writes.append(PlannedWrite(artifact_id, path, original, replacement, fields))
        before.append((artifact_id, artifact.status))
        after.append((artifact_id, target))
    proposed = _proposed_artifacts(validator, report, replacements, root)
    proposed_catalog = {item.artifact_id: item for item in proposed}
    primary_id = sorted(transitions)[0]
    # ECP-KRN-004: every transitioned artifact is evaluated against the
    # contract's transition bindings through the gate evaluator check uses, with
    # the same context builder; the graph-structural checks are appended.
    _, quality, _, _, gates = load_validated_contracts()
    gate_results: list[dict[str, Any]] = []
    blocked_by: list[str] = []
    refusals: list[tuple[str, str]] = []
    for artifact_id, target in sorted(transitions.items()):
        artifact = catalog[artifact_id]
        context = build_context(
            root, report, catalog, artifact,
            checkpoint="transition", change_set=declared_change_set((), complete=False), target=target,
        )
        structural = structural_precondition_results(root, catalog, proposed_catalog, artifact, target, effective_reasons.get(artifact_id), policy=policy)
        for gate in transition_gate_results(quality, gates, context, structural=structural):
            gate_results.append(gate)
            for predicate in gate["predicates"]:
                if predicate["status"] != "pass":
                    refusals.append((str(predicate["id"]), str(predicate["message"])))
                    blocked_by.append(f"{predicate['id']}: {predicate['message']}")
    if refusals and apply:
        # A programmatic apply fails closed, labelled by the first refusing check
        # (ECP-KRN-008); a plan renders the blocked result instead.
        predicate_id, message = refusals[0]
        raise PreconditionError(predicate_id, "; ".join([message, *blocked_by[1:]]))
    if blocked_by:
        current = catalog[primary_id]
        _, current_dependencies = project_scope(catalog, current) if current.artifact_type in PRIMARY_TYPES else (set(), set())
        result = selected_result(
            root,
            operation="transition",
            primary=current,
            related=[catalog[item] for item in current_dependencies if item in catalog],
            artifacts=sorted(transitions),
            dependencies=current_dependencies,
            blocked_by=blocked_by,
            before=_state(before),
            after=_state(before),
            checkpoint="transition",
            gates=gate_results,
        )
        return TransitionPlan(root=root, inputs=inputs, writes=(), result=result)
    errors = _validate_artifacts(validator, proposed, root)
    if errors:
        first = errors[0]
        raise HarnessError(f"proposed final graph is invalid [{first.code}]: {first.message}")
    primary = proposed_catalog[primary_id]
    completed = (
        [f"Applied {len(writes)} explicit lifecycle transition(s) atomically."]
        if apply
        else [f"Planned {len(writes)} explicit lifecycle transition(s); no files were written."]
    )
    dependencies: set[str] = set()
    if primary.artifact_type in PRIMARY_TYPES:
        _, dependencies = project_scope(proposed_catalog, primary)
    result = selected_result(
        root,
        operation="transition",
        primary=primary,
        related=[proposed_catalog[item] for item in dependencies if item in proposed_catalog],
        artifacts=sorted(transitions),
        dependencies=dependencies,
        done=completed,
        before=_state(before),
        after=_state(after),
        writes=[
            {
                "id": item.artifact_id,
                "path": item.path.relative_to(root).as_posix(),
                "fields": list(item.fields),
            }
            for item in writes
        ],
        checkpoint="transition",
        gates=gate_results,
    )
    plan = TransitionPlan(root=root, inputs=inputs, writes=tuple(writes), result=result)
    if apply:
        apply_transition(plan)
    return plan


def _stage(path: Path, content: bytes) -> Path:
    # ECP-PRM-008: the transaction stages every file through integrity's one writer, then replaces them all.
    return stage_bytes(path, content, prefix=f".{path.name}.wex-")


def _replace(staged: Path, target: Path) -> None:
    os.replace(staged, target)


def apply_transition(plan: TransitionPlan) -> None:
    mutation_guard.require_mutation_authority(plan.root, operation="transition-apply")
    ensure_governed_checkpoint(plan.root, plan.result["selection"]["artifacts"])
    selected = {write.path: write.artifact_id for write in plan.writes}
    for planned_input in plan.inputs:
        try:
            current = planned_input.path.read_bytes()
        except OSError as exc:
            relative = planned_input.path.relative_to(plan.root).as_posix()
            raise HarnessError(f"cannot re-read planned input {relative}: {exc}") from exc
        if current != planned_input.original:
            identity = selected.get(planned_input.path)
            label = identity or planned_input.path.relative_to(plan.root).as_posix()
            raise HarnessError(f"stale transition plan: {label} changed before apply")
    staged: dict[Path, Path] = {}
    replaced: list[PlannedWrite] = []
    try:
        for write in plan.writes:
            staged[write.path] = _stage(write.path, write.replacement)
        for write in plan.writes:
            if write.path.read_bytes() != write.original:
                raise HarnessError(f"stale transition plan: {write.artifact_id} changed during apply")
            candidate = staged[write.path]
            _replace(candidate, write.path)
            staged.pop(write.path)
            replaced.append(write)
    except Exception as exc:
        rollback_errors: list[str] = []
        for write in reversed(replaced):
            rollback: Path | None = None
            try:
                rollback = _stage(write.path, write.original)
                _replace(rollback, write.path)
            except Exception as rollback_exc:  # pragma: no cover - catastrophic filesystem path
                rollback_errors.append(f"{write.artifact_id}: {rollback_exc}")
            finally:
                if rollback is not None:
                    rollback.unlink(missing_ok=True)
        if rollback_errors:
            raise HarnessError(
                "transition failed and rollback could not prove restoration: " + "; ".join(rollback_errors)
            ) from exc
        raise HarnessError(f"transition failed; all replaced files were restored: {exc}") from exc
    finally:
        for path in staged.values():
            path.unlink(missing_ok=True)


def preparation_result(repository: Path, artifact_id: str, kind: str, path: Path, report: Any | None = None) -> dict[str, Any]:
    root = ensure_target(repository, must_exist=True)
    if report is None:
        _, report = validated_repository(root)
        catalog = artifact_catalog(report)
    else:
        # ECP-ENG-010: the graph was validated before the write; the one new record is parsed
        # alone and joins that catalog, so the command validates once.
        catalog = artifact_catalog(report)
        prepared, error = _validator_module.parse_formal_artifact(path, root)
        if prepared is None:
            raise HarnessError(f"prepared artifact is not readable: {error.message if error else artifact_id}")
        catalog[prepared.artifact_id] = prepared
    artifact = catalog.get(artifact_id)
    if artifact is None:
        raise HarnessError(f"prepared artifact is not discoverable: {artifact_id}")
    governing, dependencies = project_scope(catalog, artifact)
    label = "verification record" if kind == "capture-verification" else "release record"
    return selected_result(
        root,
        operation=kind,
        primary=artifact,
        related=[catalog[item] for item in dependencies if item in catalog],
        governing=governing,
        dependencies=dependencies,
        done=[f"Prepared ready {label} {artifact_id} at {path.relative_to(root).as_posix()}."],
        after=[{"id": artifact_id, "status": artifact.status}],
        writes=[{
            "id": artifact_id,
            "path": path.relative_to(root).as_posix(),
            "fields": sorted(artifact.metadata),
        }],
    )
