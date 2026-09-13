"""Bounded GitHub pull-request inputs owned by the released package."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any
from se_harness.integrity import unique_object_hook
from se_harness.codes import CodedError, WEX_ECP_014


MAX_EVENT_BYTES = 2 * 1024 * 1024
WORK_ORDER_LINE = re.compile(
    r"^Harness-Work-Order:[ \t]*(WO-[A-Z][A-Z0-9-]*-\d{3})[ \t]*$",
    re.MULTILINE,
)
RESTITUTION_LINE = re.compile(
    r"^Harness-Restitution:[ \t]*([0-9a-f]{64})[ \t]*$",
    re.MULTILINE,
)
FIELDS = ("work-order", "work-orders", "restitution-digest")


class SelectionError(ValueError):
    """A bounded pull-request work-order selection error."""


class SelectionRefusal(CodedError, SelectionError):
    """A coded selection refusal (W-ADS-001, WEX-ECP-014): a `SelectionError` that carries its code."""


_unique_object = unique_object_hook(lambda key: SelectionError(f"duplicate JSON key: {key}"))


def select_work_orders(body: str) -> list[str]:
    """Read either the singular declaration or one comma-separated plural declaration."""
    if not isinstance(body, str):
        raise SelectionError("pull-request body must be text")
    lines = [line for line in body.replace("\r\n", "\n").split("\n")
             if line.startswith(("Harness-Work-Order:", "Harness-Work-Orders:"))]
    if len(lines) != 1:
        raise SelectionError("expected exactly one standalone Harness-Work-Order or Harness-Work-Orders declaration")
    field, value = lines[0].split(":", 1)
    ids = [item.strip() for item in value.split(",")]
    if (field == "Harness-Work-Order" and len(ids) != 1) or any(
        not WORK_ORDER_LINE.fullmatch(f"Harness-Work-Order: {item}") for item in ids
    ) or len(ids) != len(set(ids)):
        raise SelectionError("work-order declaration contains malformed or duplicate IDs")
    return ids


def select_work_order(body: str) -> str:
    ids = select_work_orders(body)
    if len(ids) != 1:
        raise SelectionError("multiple work orders selected; use --field work-orders")
    return ids[0]



def select_restitution_digest(body: str) -> str:
    """Select at most one declared restitution digest; empty text when none is declared."""

    if not isinstance(body, str):
        raise SelectionError("pull-request body must be text")
    matches = RESTITUTION_LINE.findall(body.replace("\r\n", "\n"))
    if len(matches) > 1:
        raise SelectionError(f"expected at most one standalone Harness-Restitution field; found {len(matches)}")
    return matches[0] if matches else ""


def select_from_event(path: Path, field: str = "work-order") -> str:
    """Read one bounded GitHub event and select one declared field."""

    if field not in FIELDS:
        raise SelectionError(f"unknown field {field!r}")

    try:
        with path.open("rb") as event_file:
            raw_event = event_file.read(MAX_EVENT_BYTES + 1)
        if len(raw_event) > MAX_EVENT_BYTES:
            raise SelectionError("GitHub event exceeds the size limit")
        event = json.loads(raw_event.decode("utf-8"), object_pairs_hook=_unique_object)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SelectionError(f"cannot read GitHub event: {exc}") from exc
    if not isinstance(event, dict):
        raise SelectionError("GitHub event root must be an object")
    pull_request = event.get("pull_request")
    if not isinstance(pull_request, dict):
        raise SelectionError("GitHub event has no pull_request object")
    if field == "restitution-digest":
        return select_restitution_digest(pull_request.get("body"))
    if field == "work-orders":
        return "\n".join(select_work_orders(pull_request.get("body")))
    return select_work_order(pull_request.get("body"))


def render_pull_request_body(root: Path, artifact: Any, *, packet_directory: Path) -> str:
    """The pull-request body for one work order (ECP-PRB-001 to -005).

    LF line endings only; the first non-empty line is the standalone
    `Harness-Work-Order` field; a retained `handoff.json` of schema 2 adds one
    standalone `Harness-Restitution` line; the `Verification` section lists
    every evidence path under the packet directory.
    """

    if artifact.artifact_type != "work_order":
        raise SelectionRefusal(WEX_ECP_014, f"{artifact.artifact_id} is not a work order")
    if artifact.status == "draft":
        raise SelectionRefusal(WEX_ECP_014, f"{artifact.artifact_id} is draft; a pull request needs an approved or later work order")
    lines = [f"Harness-Work-Order: {artifact.artifact_id}"]
    handoff = packet_directory / "handoff.json"
    if handoff.is_file():
        try:
            value = json.loads(handoff.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise SelectionRefusal(WEX_ECP_014, f"{handoff.relative_to(root).as_posix()} is not readable JSON: {exc}") from exc
        digest = value.get("result_sha256") if isinstance(value, dict) else None
        if value.get("schema") == "se-harness-workflow-result-v2" and isinstance(digest, str) and RESTITUTION_LINE.fullmatch(f"Harness-Restitution: {digest}"):
            lines.append(f"Harness-Restitution: {digest}")
    title = str(artifact.metadata.get("title", artifact.artifact_id))
    lines.extend(["", "## Summary", "", f"- {artifact.artifact_id}: {title}", "", "## Verification", ""])
    evidence = sorted(
        path.relative_to(root).as_posix()
        for path in packet_directory.rglob("*")
        if path.is_file()
    ) if packet_directory.is_dir() else []
    lines.extend([f"- {path}" for path in evidence] or ["- No retained evidence under the packet directory yet."])
    body = "\n".join(lines).replace("\r", "") + "\n"
    if select_work_order(body) != artifact.artifact_id:
        raise SelectionRefusal(WEX_ECP_014, "the generated body does not round-trip through the selector")
    return body



def check_pull_request(root: Path, event: Path, base: str) -> dict[str, Any]:
    """Check each approved work order and the diff against their combined scope."""
    from se_harness.installer import ensure_target, HarnessError
    from se_harness.repository_graph import artifact_catalog, validated_repository
    from se_harness.preflight import run_preflight
    from se_harness.workflow_compliance import check_workflow, build_context
    from se_harness.workflow_change_set import git_change_set, path_is_admitted, validate_changed_targets

    root = ensure_target(root, must_exist=True)
    ids = select_from_event(event, "work-orders").splitlines()
    declared = select_from_event(event, "restitution-digest")
    if declared and len(ids) != 1:
        raise SelectionError("a restitution digest names one work order; omit it for a combined PR")
    _, report = validated_repository(root)
    catalog = artifact_catalog(report)
    changes = git_change_set(root, base)
    validate_changed_targets(root, changes)
    scopes = {}
    for identifier in ids:
        primary = catalog.get(identifier)
        if primary is None or primary.artifact_type != "work_order" or primary.status not in {"approved", "in_progress", "implemented"}:
            raise SelectionError(f"{identifier} is not an approved or implemented work order")
        preflight = run_preflight(root, work_order_id=identifier, phase="review", report=report)
        if not preflight.ready:
            raise SelectionError(f"{identifier}: {preflight.diagnostics[0].message}")
        context = build_context(root, report, catalog, primary, checkpoint="scope", change_set=changes)
        if not context.declared_scope:
            raise SelectionError(f"{identifier} has no execution scope")
        scopes[identifier] = context.admitted_scope
    union = tuple(path for scope in scopes.values() for path in scope)
    outside = [path for path in changes.paths if not path_is_admitted(path, union)]
    if outside:
        raise SelectionError(f"changed path is outside every selected work order: {outside[0]}")
    for identifier in ids:
        if catalog[identifier].status != "in_progress":
            continue
        # Each handoff covers the paths admitted by that work order. The union
        # check above already accounted for the complete repository diff.
        arguments = {"from_git": base} if len(ids) == 1 else {
            "changed_paths": [p for p in changes.paths if path_is_admitted(p, scopes[identifier])],
            "changes_complete": True,
        }
        result = check_workflow(root, artifact_id=identifier, checkpoint="handoff", **arguments)
        if result["operation"]["outcome"] != "completed":
            raise SelectionError(f"{identifier}: " + "; ".join(result["restitution"]["blocked_by"]))
        if declared and result.get("result_sha256") != declared:
            raise SelectionError("Declared Harness-Restitution does not match the handoff result")
    return {"work_orders": ids, "changed_paths": list(changes.paths), "status": "pass"}
