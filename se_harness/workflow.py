"""Deterministic, provider-neutral governance workflow execution.

The module owns selected-scope projection, lifecycle policy, transaction
planning, atomic application, and the semantic result rendered by every agent.
It intentionally uses only the Python standard library.
"""

from __future__ import annotations

import json
import os
import re
import tempfile
import tomllib

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
from se_harness.preflight import _load_validator_module
from se_harness.workflow_contract import load_workflow_contract, validate_lifecycle_registry


PRIMARY_TYPES = {"work_order", "verification_record", "release_record"}
DEFINITION_TYPES = {
    "intent",
    "capability",
    "requirement",
    "specification",
    "architecture",
    "adr",
    "verification",
    "release_contract",
    "operating_contract",
}

WORKFLOW_CONTRACT = load_workflow_contract()
LIFECYCLE_REGISTRY = validate_lifecycle_registry(WORKFLOW_CONTRACT)
# Compatibility projection for callers that only need transition edges.  The
# lifecycle registry remains the sole policy source.
TRANSITIONS: dict[str, dict[str, set[str]]] = {
    family: {
        source: set(row.transitions_to)
        for source, row in states.items()
    }
    for family, states in LIFECYCLE_REGISTRY.items()
}
_CONTROL = re.compile(r"[\x00-\x1f\x7f]")


class RepositoryWorkflowError(HarnessError):
    """The repository cannot be evaluated at all: the validator or its identities failed."""


class PreconditionError(HarnessError):
    """A refused transition, labelled by the check that refused it (ECP-KRN-008)."""

    def __init__(self, predicate_id: str, message: str) -> None:
        super().__init__(message)
        self.predicate_id = predicate_id


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


def _finding_key(item: Mapping[str, Any]) -> tuple[str, str, str]:
    return (str(item.get("code", "")), str(item.get("path", "")), str(item.get("message", "")))


def failed_result(
    kind: str,
    primary: str | None,
    message: str,
    *,
    code: str = "WEX001",
    repository_blocker: bool = False,
) -> dict[str, Any]:
    from se_harness.workflow_compliance import remediation_result

    finding = {"code": code, "message": _terminal_text(message)}
    return remediation_result(kind, primary, finding, repository_blocker=repository_blocker)


def _terminal_text(value: object) -> str:
    text = str(value)
    return "".join(character if character >= " " and character != "\x7f" else "?" for character in text)


def _validation(root: Path) -> tuple[Any, Any]:
    try:
        validator = _load_validator_module()
        return validator, validator.validate_repository(root)
    except HarnessError as exc:
        raise RepositoryWorkflowError(str(exc)) from exc


def _catalog(report: Any) -> dict[str, Any]:
    catalog: dict[str, Any] = {}
    duplicates: set[str] = set()
    folded: dict[str, str] = {}
    case_collisions: set[str] = set()
    for artifact in report.artifacts:
        if artifact.artifact_id in catalog:
            duplicates.add(artifact.artifact_id)
        key = artifact.artifact_id.casefold()
        previous = folded.get(key)
        if previous is not None and previous != artifact.artifact_id:
            case_collisions.update((previous, artifact.artifact_id))
        folded[key] = artifact.artifact_id
        catalog[artifact.artifact_id] = artifact
    if duplicates:
        raise RepositoryWorkflowError(f"formal artifact IDs are not unique: {', '.join(sorted(duplicates))}")
    if case_collisions:
        raise RepositoryWorkflowError(
            "formal artifact IDs are not unique under case-insensitive comparison: "
            + ", ".join(sorted(case_collisions, key=lambda item: (item.casefold(), item)))
        )
    return catalog


def _targets(artifact: Any, relation: str) -> set[str]:
    value = artifact.relations.get(relation, [])
    return {item for item in value if isinstance(item, str)} if isinstance(value, list) else set()


def _inverse(catalog: Mapping[str, Any], target_id: str, relation: str, artifact_type: str) -> set[str]:
    return {
        item.artifact_id
        for item in catalog.values()
        if item.artifact_type == artifact_type and target_id in _targets(item, relation)
    }


def _work_scope(catalog: Mapping[str, Any], work_order: Any) -> tuple[set[str], set[str]]:
    governing = set().union(
        _targets(work_order, "implements"),
        _targets(work_order, "specifications"),
        _targets(work_order, "architecture"),
        _targets(work_order, "verification"),
    )
    requirements = {
        item for item in governing if item in catalog and catalog[item].artifact_type == "requirement"
    }
    capabilities: set[str] = set()
    for requirement_id in requirements:
        capabilities.update(_targets(catalog[requirement_id], "derives_from"))
    governing.update(capabilities)
    for capability_id in capabilities:
        if capability_id in catalog:
            governing.update(_targets(catalog[capability_id], "derives_from"))
    vrecs = _inverse(catalog, work_order.artifact_id, "verifies_work_order", "verification_record")
    releases = _inverse(catalog, work_order.artifact_id, "releases_work", "release_record")
    return governing, vrecs | releases


def project_scope(catalog: Mapping[str, Any], primary: Any) -> tuple[set[str], set[str]]:
    if primary.artifact_type == "work_order":
        return _work_scope(catalog, primary)
    if primary.artifact_type == "verification_record":
        governing = _targets(primary, "conforms_to")
        work = _targets(primary, "verifies_work_order")
        governing.update(work)
        dependencies: set[str] = set()
        for work_id in work:
            if work_id in catalog:
                upstream, _ = _work_scope(catalog, catalog[work_id])
                governing.update(upstream)
        dependencies.update(_inverse(catalog, primary.artifact_id, "includes_verification", "release_record"))
        return governing, dependencies
    if primary.artifact_type == "release_record":
        governing = set().union(
            _targets(primary, "satisfies"),
            _targets(primary, "includes_verification"),
            _targets(primary, "releases_work"),
        )
        for work_id in _targets(primary, "releases_work"):
            if work_id in catalog:
                upstream, _ = _work_scope(catalog, catalog[work_id])
                governing.update(upstream)
        return governing, set()
    raise HarnessError("check accepts only WO, VREC, or RLS artifacts")


def _diagnostic(item: Any) -> dict[str, str]:
    return {
        "code": item.code,
        "path": item.path,
        "message": item.message,
        "plane": item.plane,
    }


def project_selected(
    repository: Path,
    artifact_id: str,
    *,
    include_background: bool = False,
) -> dict[str, Any]:
    """Project the selected artifact's rule, procedure and next step; evaluate no gate.

    This is `check` without a checkpoint (SPEC-ECP-011, ECP-ONE-001/-002); the
    `focus` alias that shared it was removed after 0.10.0 (SPEC-ECP-013).
    """

    root = ensure_target(repository, must_exist=True)
    _, report = _validation(root)
    catalog = _catalog(report)
    primary = catalog.get(artifact_id)
    if primary is None:
        raise HarnessError(f"unknown artifact ID: {artifact_id}")
    if primary.artifact_type not in PRIMARY_TYPES:
        raise HarnessError("check accepts only WO, VREC, or RLS artifacts")
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
        diagnostic = _diagnostic(item)
        candidate = safe_destination(root, Path(item.path))
        if item.code in {"E001", "E003"}:
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
            "code": "WEX190",
            "count": total,
            "message": f"{total} unrelated finding(s); use --include-background for categories",
        })
    from se_harness.workflow_compliance import selected_result

    blockers = [*repository, *scoped]
    return selected_result(
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


def _next_phase(status: str) -> str:
    return "start" if status in {"approved", "in_progress"} else "review"


def _reading_manifest(root: Path, catalog: Mapping[str, Any], primary: Any) -> tuple[str, ...]:
    """The preflight reading manifest for the phase the selected state implies (ECP-NXT-005).

    A work order reads its own preflight. A verification or release record has
    no preflight of its own; it reads the review manifest of the first work
    order it verifies or releases, which is the chain a reviewer needs.
    """

    from se_harness.preflight import run_preflight

    if primary.artifact_type == "work_order":
        work_order_id, phase = primary.artifact_id, _next_phase(primary.status)
    else:
        relation = "verifies_work_order" if primary.artifact_type == "verification_record" else "releases_work"
        targets = sorted(_targets(primary, relation))
        if not targets:
            return ()
        work_order_id, phase = targets[0], "review"
    try:
        return tuple(run_preflight(root, work_order_id=work_order_id, phase=phase).reading_manifest)
    except HarnessError:
        return ()


def next_step(repository: Path, artifact_id: str | None = None) -> dict[str, Any]:
    """One call returning the selected artifact's complete execution context (ECP-NXT-001 to -007).

    The result is the `check` projection of the selected artifact with the
    operation kind `next` and an additive `context` object; the next argv, the
    procedure and the step are the ones `check` already selects, so
    `next` holds no private mapping. It writes nothing.
    """

    from se_harness.workflow_compliance import execution_scope
    from se_harness.workflow_result import restitution_digest

    root = ensure_target(repository, must_exist=True)
    _, report = _validation(root)
    catalog = _catalog(report)
    if artifact_id is None:
        candidates = sorted(
            item.artifact_id
            for item in catalog.values()
            if item.artifact_type == "work_order" and item.status == "in_progress"
        )
        if len(candidates) != 1:
            raise HarnessError(
                f"WEX-ECP-001: {len(candidates)} work orders are in_progress; name one with --artifact"
                + (f" ({', '.join(candidates)})" if candidates else "")
            )
        artifact_id = candidates[0]
    primary = catalog.get(artifact_id)
    if primary is None:
        raise HarnessError(f"unknown artifact ID: {artifact_id}")
    if primary.artifact_type not in PRIMARY_TYPES:
        raise HarnessError("next accepts only WO, VREC, or RLS artifacts")
    projected = project_selected(root, artifact_id)
    declared: tuple[str, ...] = ()
    if primary.artifact_type == "work_order":
        try:
            declared = execution_scope(primary)
        except HarnessError:
            declared = ()
    command = projected["restitution"]["command_or_response"]
    step = projected["restitution"]["next"]
    context = {
        "reading_manifest": list(_reading_manifest(root, catalog, primary)),
        "governing": list(projected["scope"]["governing"]),
        "declared_paths": list(declared),
        "state": {"status": primary.status, "family": _family(primary.artifact_type)},
        "next": {
            "argv": list(command.get("argv", [])) if command.get("kind") == "command" else [],
            "procedure_id": step["procedure_id"],
            "step_id": step["step_id"],
        },
        "decision_required": projected["restitution"]["decision_required"],
    }
    result = dict(projected)
    result["operation"] = {**projected["operation"], "kind": "next"}
    result["context"] = context
    result["result_sha256"] = restitution_digest(result)
    return result


def _assertion(value: str, label: str, *, limit: int) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > limit or _CONTROL.search(value):
        raise HarnessError(f"{label} must be non-empty, single-line text of at most {limit} characters")
    return value.strip()


def _split_document(data: bytes) -> tuple[list[str], str, str, str]:
    try:
        text = data.decode("utf-8-sig")
    except UnicodeError as exc:
        raise HarnessError(f"formal artifact is not valid UTF-8: {exc}") from exc
    lines = text.splitlines(keepends=True)
    clean = [line.rstrip("\r\n") for line in lines]
    if not clean or clean[0] != "+++":
        raise HarnessError("formal artifact has no TOML front matter")
    try:
        closing = clean.index("+++", 1)
    except ValueError as exc:
        raise HarnessError("formal artifact has no closing front-matter delimiter") from exc
    opening_ending = lines[0][len(clean[0]) :]
    newline = opening_ending or ("\r\n" if "\r\n" in text else "\n")
    closing_ending = lines[closing][len(clean[closing]) :]
    body = "".join(lines[closing + 1 :])
    bom = "\ufeff" if data.startswith(b"\xef\xbb\xbf") else ""
    return clean[1:closing], body, newline, bom + "+++" + newline


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
    lines.insert(end, encoded)


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


def _mutate(data: bytes, artifact: Any, target: str, actor: str, reason: str | None, now: str) -> tuple[bytes, tuple[str, ...]]:
    front, body, newline, opening = _split_document(data)
    fields = {"status", "updated", "lifecycle_events"}
    _set_scalar(front, "status", target)
    _set_scalar(front, "updated", now[:10])
    if target == "verified" and artifact.artifact_type == "verification_record":
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


def _family(artifact_type: str) -> str:
    return "definition" if artifact_type in DEFINITION_TYPES else artifact_type


def _grants_authority(family: str, status: str) -> bool:
    row = LIFECYCLE_REGISTRY.get(family, {}).get(status)
    return bool(row and row.grants_authority)


def _revision_policy(root: Path) -> dict[str, bool]:
    path = root / ".engineering-harness.toml"
    if not path.is_file():
        return {"required_for_verified_work": False, "required_for_release": False}
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError):
        return {"required_for_verified_work": False, "required_for_release": False}
    table = data.get("revision_provenance", {})
    return {
        name: bool(table.get(name, False)) if isinstance(table, dict) else False
        for name in ("required_for_verified_work", "required_for_release")
    }


def _validate_edge(root: Path, artifact: Any, target: str, actor: str, reason: str | None) -> None:
    family = _family(artifact.artifact_type)
    row = LIFECYCLE_REGISTRY.get(family, {}).get(artifact.status)
    if row is None or target not in row.transitions_to:
        raise PreconditionError("QGS-EDGE", f"transition {artifact.artifact_id}: {artifact.status} -> {target} is not allowed")
    _assertion(actor, f"decision actor for {artifact.artifact_id}", limit=128)
    if target in {"rejected", "superseded"}:
        if reason is None:
            detail = "successor VREC ID" if target == "superseded" else "rejection reason"
            raise HarnessError(f"transition {artifact.artifact_id} to {target} requires --reason with a {detail}")
        _assertion(reason, f"reason for {artifact.artifact_id}", limit=2000)
    elif reason is not None:
        _assertion(reason, f"reason for {artifact.artifact_id}", limit=2000)
    policy = _revision_policy(root)
    if family == "work_order" and artifact.status in {"implemented", "verified"}:
        setting = "required_for_verified_work" if target == "verified" else "required_for_release"
        if not policy[setting]:
            raise PreconditionError("QGS-EDGE", f"work order transition to {target} is not enabled by revision provenance policy")


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


def _status(catalog: Mapping[str, Any], replacements_catalog: Mapping[str, Any], artifact_id: str) -> str:
    return replacements_catalog.get(artifact_id, catalog[artifact_id]).status


def _structural(predicate_id: str, status: str, message: str, artifact_id: str) -> dict[str, Any]:
    return {
        "id": predicate_id,
        "status": status,
        "evidence": [{"kind": "artifact", "reference": artifact_id}],
        "message": message,
    }


def structural_precondition_results(
    root: Path,
    catalog: Mapping[str, Any],
    proposed_catalog: Mapping[str, Any],
    artifact: Any,
    target: str,
    reason: str | None,
) -> list[dict[str, Any]]:
    """Evaluate the graph-structural checks bound to one edge (ECP-KRN-005).

    These are properties of the artifact graph shape alone; every other
    precondition is a gate predicate in `QUALITY_GATES.json`. Each check is
    reported as a `QGS-` predicate so a refusal names it.
    """

    from se_harness.workflow_contract import load_validated_contracts, transition_binding

    _, quality, _, _, _ = load_validated_contracts()
    _, structural_ids = transition_binding(quality, _family(artifact.artifact_type), artifact.artifact_type, target)
    artifact_id = artifact.artifact_id
    results: list[dict[str, Any]] = []
    for check in structural_ids:
        if check == "QGS-EDGE":
            family = _family(artifact.artifact_type)
            row = LIFECYCLE_REGISTRY.get(family, {}).get(artifact.status)
            if row is None or target not in row.transitions_to:
                results.append(_structural(check, "fail", f"transition {artifact_id}: {artifact.status} -> {target} is not allowed", artifact_id))
                continue
            policy = _revision_policy(root)
            if family == "work_order" and artifact.status in {"implemented", "verified"}:
                setting = "required_for_verified_work" if target == "verified" else "required_for_release"
                if not policy[setting]:
                    results.append(_structural(check, "fail", f"work order transition to {target} is not enabled by revision provenance policy", artifact_id))
                    continue
            results.append(_structural(check, "pass", f"{artifact.status} -> {target} is a declared lifecycle edge for {artifact_id}.", artifact_id))
        elif check == "QGS-ASSURANCE":
            assurance = artifact.metadata.get("assurance")
            if not isinstance(assurance, dict) or assurance.get("commit_bound_verification") not in {"required", "not_required"}:
                results.append(_structural(check, "fail", f"work order {artifact_id} requires a complete assurance classification before approval", artifact_id))
            else:
                results.append(_structural(check, "pass", f"{artifact_id} classifies commit-bound verification as {assurance['commit_bound_verification']}.", artifact_id))
        elif check == "QGS-VREC-COVERAGE":
            covered = [
                item for item in proposed_catalog.values()
                if item.artifact_type == "verification_record"
                and _grants_authority("verification_record", item.status)
                and artifact_id in _targets(item, "verifies_work_order")
            ]
            if covered:
                results.append(_structural(check, "pass", f"{artifact_id} is covered by eligible verification record {sorted(item.artifact_id for item in covered)[0]}.", artifact_id))
            else:
                results.append(_structural(check, "fail", f"work order {artifact_id} has no direct eligible verification record", artifact_id))
        elif check == "QGS-RLS-COVERAGE":
            covered = [
                item for item in proposed_catalog.values()
                if item.artifact_type == "release_record"
                and _grants_authority("release_record", item.status)
                and artifact_id in _targets(item, "releases_work")
            ]
            if covered:
                results.append(_structural(check, "pass", f"{artifact_id} is released by {sorted(item.artifact_id for item in covered)[0]}.", artifact_id))
            else:
                results.append(_structural(check, "fail", f"work order {artifact_id} has no direct released release record", artifact_id))
        elif check == "QGS-VERIFIED-INCLUSION":
            missing = [
                vrec_id for vrec_id in sorted(_targets(artifact, "includes_verification"))
                if vrec_id not in proposed_catalog
                or not _grants_authority("verification_record", proposed_catalog[vrec_id].status)
            ]
            if missing:
                results.append(_structural(check, "fail", f"release record {artifact_id} requires verified VREC {missing[0]}", artifact_id))
            else:
                results.append(_structural(check, "pass", f"Every verification record {artifact_id} includes is verified.", artifact_id))
        elif check == "QGS-SUCCESSOR":
            successor_id = reason
            successor = proposed_catalog.get(successor_id) if successor_id else None
            if successor_id is None:
                results.append(_structural(check, "not_assessable", f"supersession of {artifact_id} names no successor VREC", artifact_id))
            elif successor is None or successor.artifact_type != "verification_record":
                results.append(_structural(check, "fail", f"supersession successor is not a VREC: {successor_id}", artifact_id))
            elif not _grants_authority("verification_record", successor.status):
                results.append(_structural(check, "fail", f"supersession successor {successor_id} must be verified or released", artifact_id))
            elif not _targets(artifact, "verifies_work_order").issubset(_targets(successor, "verifies_work_order")):
                results.append(_structural(check, "fail", f"supersession successor {successor_id} does not preserve work coverage", artifact_id))
            else:
                results.append(_structural(check, "pass", f"{successor_id} is an eligible successor preserving the coverage of {artifact_id}.", artifact_id))
        else:  # pragma: no cover - the loader rejects unknown structural ids
            raise HarnessError(f"WEX-ECP-030: unknown structural check {check}")
    return results


def plan_transition(
    repository: Path,
    transitions: Mapping[str, str],
    decisions: Mapping[str, str],
    reasons: Mapping[str, str],
    *,
    apply: bool = False,
) -> TransitionPlan:
    root = ensure_target(repository, must_exist=True)
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
    validator, report = _validation(root)
    effective_reasons: dict[str, str] = dict(reasons)
    if report.errors:
        first = report.errors[0]
        message = f"current artifact graph is invalid [{first.code}]: {first.message}"
        if first.code in {"E001", "E003"}:
            raise RepositoryWorkflowError(message)
        raise HarnessError(message)
    catalog = _catalog(report)
    from se_harness.workflow_compliance import ensure_governed_checkpoint

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
        _validate_edge(root, artifact, target, decisions[artifact_id], reasons.get(artifact_id))
        if decisions[artifact_id] == DELEGATED_ROLE:
            # SPEC-ECP-006 ECP-DLG-002/-003/-005/-006/-007: the delegated route.
            right = DELEGATED_TRANSITIONS.get((_family(artifact.artifact_type), artifact.status, target))
            try:
                reading = authorize_delegated_right(
                    root, work_order_metadata=artifact.metadata, work_order_path=artifact.path, right=right,
                )
            except DelegationError as exc:
                raise PreconditionError(exc.code, exc.message) from exc
            if apply:
                from se_harness import mutation_guard

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
    from se_harness.workflow_compliance import (
        build_context,
        declared_change_set,
        selected_result,
        transition_gate_results,
    )
    from se_harness.workflow_contract import load_validated_contracts

    _, quality, _, _, gates = load_validated_contracts()
    gate_results: list[dict[str, Any]] = []
    blocked_by: list[str] = []
    for artifact_id, target in sorted(transitions.items()):
        artifact = catalog[artifact_id]
        context = build_context(
            root, report, catalog, artifact,
            checkpoint="transition", change_set=declared_change_set((), complete=False), target=target,
        )
        structural = structural_precondition_results(root, catalog, proposed_catalog, artifact, target, effective_reasons.get(artifact_id))
        for gate in transition_gate_results(quality, gates, context, structural=structural):
            gate_results.append(gate)
            for predicate in gate["predicates"]:
                if predicate["status"] != "pass":
                    blocked_by.append(f"{predicate['id']}: {predicate['message']}")
    if blocked_by and apply:
        # A programmatic apply fails closed, labelled by the first refusing check
        # (ECP-KRN-008); a plan renders the blocked result instead.
        predicate_id, _, message = blocked_by[0].partition(": ")
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
    descriptor, name = tempfile.mkstemp(prefix=f".{path.name}.wex-", dir=path.parent)
    staged = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
    except Exception:
        staged.unlink(missing_ok=True)
        raise
    return staged


def _replace(staged: Path, target: Path) -> None:
    os.replace(staged, target)


def apply_transition(plan: TransitionPlan) -> None:
    from se_harness import mutation_guard
    from se_harness.workflow_compliance import ensure_governed_checkpoint

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


def preparation_result(repository: Path, artifact_id: str, kind: str, path: Path) -> dict[str, Any]:
    root = ensure_target(repository, must_exist=True)
    _, report = _validation(root)
    catalog = _catalog(report)
    artifact = catalog.get(artifact_id)
    if artifact is None:
        raise HarnessError(f"prepared artifact is not discoverable: {artifact_id}")
    governing, dependencies = project_scope(catalog, artifact)
    label = "verification record" if kind == "capture-verification" else "release record"
    from se_harness.workflow_compliance import selected_result

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
