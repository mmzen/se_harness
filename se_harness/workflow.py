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
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping

from se_harness.installer import HarnessError, ensure_target, safe_destination
from se_harness.preflight import _load_validator_module, run_preflight


SCHEMA = 1
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
TRANSITIONS: dict[str, dict[str, set[str]]] = {
    "definition": {
        "draft": {"approved", "rejected"},
        "approved": {"implemented", "rejected"},
    },
    "work_order": {
        "draft": {"approved", "rejected"},
        "approved": {"in_progress", "rejected"},
        "in_progress": {"implemented", "rejected"},
        "implemented": {"verified", "released"},
        "verified": {"released"},
    },
    "verification_record": {
        "ready": {"verified", "rejected", "superseded"},
    },
    "release_record": {
        "ready": {"released", "rejected"},
    },
}
_CONTROL = re.compile(r"[\x00-\x1f\x7f]")


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


def _handoff(
    *,
    completed: Iterable[str],
    current: Iterable[str],
    next_step: Mapping[str, str],
    authority: Mapping[str, str],
    command: Mapping[str, str],
    alternatives: Iterable[Mapping[str, str]] = (),
) -> dict[str, Any]:
    return {
        "completed": list(completed),
        "current_lifecycle_state": list(current),
        "recommended_next_step": dict(next_step),
        "human_decision_or_approval_required": dict(authority),
        "command_or_suggested_response": dict(command),
        "alternative_next_steps": [dict(item) for item in alternatives],
    }


def _result(
    *,
    kind: str,
    outcome: str,
    primary: str | None,
    artifacts: Iterable[str],
    governing: Iterable[str] = (),
    dependencies: Iterable[str] = (),
    before: Iterable[tuple[str, str]] = (),
    after: Iterable[tuple[str, str]] = (),
    scoped_blockers: Iterable[Mapping[str, Any]] = (),
    repository_blockers: Iterable[Mapping[str, Any]] = (),
    background: Iterable[Mapping[str, Any]] = (),
    writes: Iterable[Mapping[str, Any]] = (),
    handoff: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "operation": {"kind": kind, "outcome": outcome},
        "selection": {"primary": primary, "artifacts": sorted(set(artifacts))},
        "scope": {
            "governing": sorted(set(governing)),
            "dependencies": sorted(set(dependencies)),
        },
        "state": {"before": _state(before), "after": _state(after)},
        "findings": {
            "scoped_blockers": sorted((dict(item) for item in scoped_blockers), key=_finding_key),
            "repository_blockers": sorted((dict(item) for item in repository_blockers), key=_finding_key),
            "background_summary": sorted((dict(item) for item in background), key=_finding_key),
        },
        "mutation": {
            "writes": sorted(
                (dict(item) for item in writes),
                key=lambda item: (str(item.get("id", "")), str(item.get("path", ""))),
            )
        },
        "handoff": dict(handoff or _handoff(
            completed=(),
            current=(),
            next_step={},
            authority={},
            command={},
        )),
    }


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
    finding = {"code": code, "message": _terminal_text(message)}
    return _result(
        kind=kind,
        outcome="failed",
        primary=primary,
        artifacts=([primary] if primary else []),
        scoped_blockers=[] if repository_blocker else [finding],
        repository_blockers=[finding] if repository_blocker else [],
        handoff=_handoff(
            completed=[],
            current=["No lifecycle state was changed."],
            next_step={"action": "remediate", "detail": finding["message"]},
            authority={"required": "none until the reported blocker is resolved"},
            command={"kind": "guidance", "value": "Resolve the reported blocker, then rerun the same command."},
        ),
    )


def _terminal_text(value: object) -> str:
    text = str(value)
    return "".join(character if character >= " " and character != "\x7f" else "?" for character in text)


def render_json(result: Mapping[str, Any]) -> str:
    return json.dumps(result, indent=2, ensure_ascii=True) + "\n"


def _render_value(value: Any) -> str:
    if isinstance(value, dict):
        return "; ".join(f"{key}: {_terminal_text(item)}" for key, item in value.items()) or "none"
    if isinstance(value, list):
        return " | ".join(_render_value(item) for item in value) or "none"
    return _terminal_text(value) or "none"


def render_human(result: Mapping[str, Any]) -> str:
    operation = result["operation"]
    selection = result["selection"]
    handoff = result["handoff"]
    lines = [
        f"Workflow {operation['kind']}: {str(operation['outcome']).upper()}",
        f"Selected: {selection['primary'] or 'none'}",
        "",
        "Completed",
        _render_value(handoff["completed"]),
        "",
        "Current lifecycle state",
        _render_value(handoff["current_lifecycle_state"]),
        "",
        "Recommended next step",
        _render_value(handoff["recommended_next_step"]),
        "",
        "Human decision or approval required",
        _render_value(handoff["human_decision_or_approval_required"]),
        "",
        "Command or suggested response",
        _render_value(handoff["command_or_suggested_response"]),
        "",
        "Alternative next steps",
        _render_value(handoff["alternative_next_steps"]),
    ]
    findings = result["findings"]
    blockers = [*findings["repository_blockers"], *findings["scoped_blockers"]]
    if blockers:
        lines.extend(["", "Blockers"])
        lines.extend(
            f"- [{item.get('code', 'WEX')}] {_terminal_text(item.get('message', ''))}"
            for item in blockers
        )
    background = findings["background_summary"]
    if background:
        lines.extend(["", "Background"])
        lines.extend(
            f"- [{item.get('code', 'WEX')}] {_terminal_text(item.get('message', ''))}"
            for item in background
        )
    return "\n".join(lines) + "\n"


def _validation(root: Path) -> tuple[Any, Any]:
    validator = _load_validator_module()
    return validator, validator.validate_repository(root)


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
        raise HarnessError(f"formal artifact IDs are not unique: {', '.join(sorted(duplicates))}")
    if case_collisions:
        raise HarnessError(
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
    raise HarnessError("focus accepts only WO, VREC, or RLS artifacts")


def _diagnostic(item: Any) -> dict[str, str]:
    return {
        "code": item.code,
        "path": item.path,
        "message": item.message,
        "plane": item.plane,
    }


def _recommend(primary: Any, *, target: str | None = None) -> dict[str, Any]:
    status = target or primary.status
    artifact_id = primary.artifact_id
    if primary.artifact_type == "work_order":
        if status == "approved":
            return _handoff(
                completed=[f"Projected the selected scope for {artifact_id}."],
                current=[f"{artifact_id} is approved."],
                next_step={"action": "implementation-start decision", "detail": "Run start preflight, then obtain an explicit instruction to begin implementation."},
                authority={"required": "engineering owner"},
                command={"kind": "command", "value": f"harnessctl preflight . --work-order {artifact_id} --phase start"},
            )
        if status == "in_progress":
            return _handoff(
                completed=[f"Projected the selected scope for {artifact_id}."],
                current=[f"{artifact_id} is in_progress."],
                next_step={"action": "implement and verify", "detail": "Complete only this work order and retain its verification evidence."},
                authority={"required": "none for work already authorized by this work order"},
                command={"kind": "command", "value": f"harnessctl preflight . --work-order {artifact_id} --phase review"},
            )
        if status == "implemented":
            return _handoff(
                completed=[f"{artifact_id} is implemented; no assurance decision was inferred."],
                current=[f"{artifact_id} is implemented."],
                next_step={"action": "prepare verification record", "detail": "Capture the exact candidate and retained evidence for assurance review."},
                authority={"required": "assurance owner only after a ready VREC exists"},
                command={"kind": "guidance", "value": "Run harnessctl capture-verification with the exact work, contracts, and evidence."},
            )
        if status in {"verified", "released"}:
            return _handoff(
                completed=[f"Projected completed work state for {artifact_id}."],
                current=[f"{artifact_id} is {status}; its VREC and RLS remain independent records."],
                next_step={"action": "review independent lifecycle records", "detail": "Do not synchronize related artifacts implicitly."},
                authority={"required": "the owner of any separately selected record"},
                command={"kind": "command", "value": f"harnessctl focus . --artifact {artifact_id}"},
            )
    if primary.artifact_type == "verification_record" and status == "ready":
        return _handoff(
            completed=[f"Projected assurance candidate {artifact_id}."],
            current=[f"{artifact_id} is ready; referenced work orders were not changed."],
            next_step={"action": "assurance decision", "detail": "Review the retained evidence and candidate identity."},
            authority={"required": "assurance owner"},
            command={"kind": "suggested_response", "value": f"I verify {artifact_id} as assurance owner."},
            alternatives=[{"action": "reject", "detail": "Reject with a non-empty reason."}, {"action": "supersede", "detail": "Supersede with one eligible successor VREC."}],
        )
    if primary.artifact_type == "verification_record" and status == "verified":
        return _handoff(
            completed=[f"Recorded the assurance decision for {artifact_id}; referenced work orders were not changed."],
            current=[f"{artifact_id} is verified."],
            next_step={"action": "select the separately authorized delivery path", "detail": "Prepare a release only when release preparation is authorized."},
            authority={"required": "repository owner for external repository action, or release owner for release preparation"},
            command={"kind": "guidance", "value": "Run harnessctl prepare-release only with the exact verified coverage and authorized release values."},
            alternatives=[{"action": "repository action", "detail": "Request authority for the exact pull-request or integration action."}],
        )
    if primary.artifact_type == "release_record" and status == "ready":
        return _handoff(
            completed=[f"Projected release candidate {artifact_id}."],
            current=[f"{artifact_id} is ready; included VRECs and work orders were not changed."],
            next_step={"action": "release decision", "detail": "Review exact verified coverage and candidate identity."},
            authority={"required": "release owner"},
            command={"kind": "suggested_response", "value": f"I authorize release record {artifact_id}."},
            alternatives=[{"action": "reject", "detail": "Reject with a non-empty reason."}],
        )
    if primary.artifact_type == "release_record" and status == "released":
        return _handoff(
            completed=[f"Recorded the release decision for {artifact_id}; included VRECs and work orders were not changed."],
            current=[f"{artifact_id} is released."],
            next_step={"action": "perform only a separately authorized external action", "detail": "Release status does not create a tag, publish, deploy, or operate anything."},
            authority={"required": "the accountable owner of the exact external action"},
            command={"kind": "guidance", "value": "State the exact proposed external action and obtain its separate authority."},
        )
    if status == "rejected":
        return _handoff(
            completed=[f"Recorded rejection of {artifact_id}; related artifacts were not changed."],
            current=[f"{artifact_id} is rejected and terminal."],
            next_step={"action": "remediate through a new or revised authorized artifact", "detail": "Do not reopen or silently replace the rejected history."},
            authority={"required": "the owner of any new definition or work scope"},
            command={"kind": "guidance", "value": "Create or revise the bounded artifact chain, then obtain its normal approvals."},
        )
    if status == "superseded":
        successor = next(iter(_targets(primary, "superseded_by")), "the declared successor")
        return _handoff(
            completed=[f"Recorded supersession of {artifact_id}; its captured provenance remains unchanged."],
            current=[f"{artifact_id} is superseded by {successor}."],
            next_step={"action": "use the eligible successor record", "detail": "The superseded record remains historical and release-ineligible."},
            authority={"required": "none to inspect the declared successor"},
            command={"kind": "command", "value": f"harnessctl focus . --artifact {successor}"},
        )
    if primary.artifact_type in DEFINITION_TYPES:
        if status == "approved":
            return _handoff(
                completed=[f"Recorded approval of {artifact_id}."],
                current=[f"{artifact_id} is approved."],
                next_step={"action": "complete the bounded definition packet", "detail": "Approve the remaining governing artifacts or create and approve one bounded work order."},
                authority={"required": "the accountable owner of each remaining artifact"},
                command={"kind": "guidance", "value": "Use one explicit transition packet when definitions are mutually dependent."},
            )
        if status == "implemented":
            return _handoff(
                completed=[f"Recorded implemented definition state for {artifact_id}."],
                current=[f"{artifact_id} is implemented and terminal."],
                next_step={"action": "inspect the selected work order", "detail": "Continue only through a separately selected authorized WO."},
                authority={"required": "engineering owner for the work order"},
                command={"kind": "guidance", "value": "Run harnessctl focus with the exact related WO ID."},
            )
    return _handoff(
        completed=[f"Projected the selected scope for {artifact_id}."],
        current=[f"{artifact_id} is {status}."],
        next_step={"action": "review current state", "detail": "No automatic related-artifact transition is permitted."},
        authority={"required": "an accountable owner for any further formal decision"},
        command={"kind": "guidance", "value": "Select the next independently authorized artifact transition."},
    )


def focus(repository: Path, artifact_id: str, *, include_background: bool = False) -> dict[str, Any]:
    root = ensure_target(repository, must_exist=True)
    _, report = _validation(root)
    catalog = _catalog(report)
    primary = catalog.get(artifact_id)
    if primary is None:
        raise HarnessError(f"unknown artifact ID: {artifact_id}")
    if primary.artifact_type not in PRIMARY_TYPES:
        raise HarnessError("focus accepts only WO, VREC, or RLS artifacts")
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
    outcome = "failed" if scoped or repository else "completed"
    return _result(
        kind="focus",
        outcome=outcome,
        primary=artifact_id,
        artifacts=[artifact_id],
        governing=governing,
        dependencies=dependencies,
        before=[(artifact_id, primary.status)],
        after=[(artifact_id, primary.status)],
        scoped_blockers=scoped,
        repository_blockers=repository,
        background=background,
        handoff=_recommend(primary) if outcome == "completed" else failed_result("focus", artifact_id, "Resolve selected-scope blockers before continuing.")["handoff"],
    )


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
    allowed = TRANSITIONS.get(family, {}).get(artifact.status, set())
    if target not in allowed:
        raise HarnessError(f"transition {artifact.artifact_id}: {artifact.status} -> {target} is not allowed")
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
            raise HarnessError(f"work order transition to {target} is not enabled by revision provenance policy")


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


def _validate_preconditions(
    root: Path,
    catalog: Mapping[str, Any],
    proposed_catalog: Mapping[str, Any],
    transitions: Mapping[str, str],
    reasons: Mapping[str, str],
) -> None:
    for artifact_id, target in transitions.items():
        artifact = catalog[artifact_id]
        if artifact.artifact_type == "work_order" and target == "approved":
            assurance = artifact.metadata.get("assurance")
            if not isinstance(assurance, dict) or assurance.get("commit_bound_verification") not in {"required", "not_required"}:
                raise HarnessError(f"work order {artifact_id} requires a complete assurance classification before approval")
        if artifact.artifact_type == "work_order" and target == "in_progress":
            preflight = run_preflight(root, work_order_id=artifact_id, phase="start")
            if not preflight.ready:
                first = preflight.diagnostics[0].message if preflight.diagnostics else "start preflight failed"
                raise HarnessError(f"work order {artifact_id} is not start-ready: {first}")
        if artifact.artifact_type == "work_order" and target == "implemented":
            preflight = run_preflight(root, work_order_id=artifact_id, phase="review")
            if not preflight.ready:
                first = preflight.diagnostics[0].message if preflight.diagnostics else "review preflight failed"
                raise HarnessError(f"work order {artifact_id} is not review-ready: {first}")
            evidence = root / "docs" / "engineering"
            keyed = any(
                path.is_file()
                and "evidence" in path.parts
                and any(part.startswith(artifact_id) for part in path.parts[path.parts.index("evidence") + 1 :])
                for path in evidence.rglob("*")
            )
            if not keyed:
                raise HarnessError(f"work order {artifact_id} has no retained work-order-keyed evidence")
        if artifact.artifact_type == "work_order" and target == "verified":
            covered = [
                item for item in proposed_catalog.values()
                if item.artifact_type == "verification_record"
                and item.status in {"verified", "released"}
                and artifact_id in _targets(item, "verifies_work_order")
            ]
            if not covered:
                raise HarnessError(f"work order {artifact_id} has no direct eligible verification record")
        if artifact.artifact_type == "work_order" and target == "released":
            covered = [
                item for item in proposed_catalog.values()
                if item.artifact_type == "release_record"
                and item.status == "released"
                and artifact_id in _targets(item, "releases_work")
            ]
            if not covered:
                raise HarnessError(f"work order {artifact_id} has no direct released release record")
        if artifact.artifact_type == "release_record" and target == "released":
            for vrec_id in _targets(artifact, "includes_verification"):
                if vrec_id not in proposed_catalog or proposed_catalog[vrec_id].status != "verified":
                    raise HarnessError(f"release record {artifact_id} requires verified VREC {vrec_id}")
        if artifact.artifact_type == "verification_record" and target == "superseded":
            successor_id = reasons[artifact_id]
            successor = proposed_catalog.get(successor_id)
            if successor is None or successor.artifact_type != "verification_record":
                raise HarnessError(f"supersession successor is not a VREC: {successor_id}")
            if successor.status not in {"verified", "released"}:
                raise HarnessError(f"supersession successor {successor_id} must be verified or released")
            if not _targets(artifact, "verifies_work_order").issubset(_targets(successor, "verifies_work_order")):
                raise HarnessError(f"supersession successor {successor_id} does not preserve work coverage")


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
    if report.errors:
        first = report.errors[0]
        raise HarnessError(f"current artifact graph is invalid [{first.code}]: {first.message}")
    catalog = _catalog(report)
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
            reasons.get(artifact_id),
            rendered_now,
        )
        replacements[path.resolve()] = replacement
        writes.append(PlannedWrite(artifact_id, path, original, replacement, fields))
        before.append((artifact_id, artifact.status))
        after.append((artifact_id, target))
    proposed = _proposed_artifacts(validator, report, replacements, root)
    proposed_catalog = {item.artifact_id: item for item in proposed}
    _validate_preconditions(root, catalog, proposed_catalog, transitions, reasons)
    errors = _validate_artifacts(validator, proposed, root)
    if errors:
        first = errors[0]
        raise HarnessError(f"proposed final graph is invalid [{first.code}]: {first.message}")
    primary_id = sorted(transitions)[0]
    primary = proposed_catalog[primary_id]
    outcome = "completed" if apply else "planned"
    completed = (
        [f"Applied {len(writes)} explicit lifecycle transition(s) atomically."]
        if apply
        else [f"Planned {len(writes)} explicit lifecycle transition(s); no files were written."]
    )
    handoff = _recommend(primary, target=transitions[primary_id])
    handoff["completed"] = completed
    result = _result(
        kind="transition",
        outcome=outcome,
        primary=primary_id,
        artifacts=transitions,
        before=before,
        after=after,
        writes=[
            {
                "id": item.artifact_id,
                "path": item.path.relative_to(root).as_posix(),
                "fields": list(item.fields),
            }
            for item in writes
        ],
        handoff=handoff,
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
    handoff = _recommend(artifact)
    label = "verification record" if kind == "capture-verification" else "release record"
    handoff["completed"] = [
        f"Prepared ready {label} {artifact_id} at {path.relative_to(root).as_posix()}."
    ]
    return _result(
        kind=kind,
        outcome="completed",
        primary=artifact_id,
        artifacts=[artifact_id],
        governing=governing,
        dependencies=dependencies,
        before=[],
        after=[(artifact_id, artifact.status)],
        writes=[{
            "id": artifact_id,
            "path": path.relative_to(root).as_posix(),
            "fields": sorted(artifact.metadata),
        }],
        handoff=handoff,
    )
