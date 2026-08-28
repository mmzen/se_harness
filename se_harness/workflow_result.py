"""Canonical schema-2 workflow results and restitution rendering."""

from __future__ import annotations

import hashlib
import json
import shlex
from typing import Any, Iterable, Mapping


SCHEMA = "se-harness-workflow-result-v2"
OUTCOMES = {"completed", "blocked"}
STATUSES = {"pass", "fail", "not_assessable"}


def _text(value: object) -> str:
    return "".join(
        character if character >= " " and character != "\x7f" else "?"
        for character in str(value)
    )


def _sentences(values: Iterable[object]) -> list[str]:
    result: list[str] = []
    for value in values:
        text = _text(value).strip()
        if text:
            result.append(text)
    return result


def _validate_restitution(value: Mapping[str, Any], outcome: str) -> None:
    required = {
        "outcome",
        "done",
        "not_done",
        "blocked_by",
        "current_lifecycle_state",
        "decision_required",
        "next",
        "command_or_response",
        "alternatives",
    }
    if set(value) != required:
        raise ValueError("WEX230: restitution fields do not match schema 2")
    if value.get("outcome") != outcome:
        raise ValueError("WEX230: restitution outcome does not match operation outcome")
    for name in ("done", "not_done", "blocked_by", "current_lifecycle_state", "alternatives"):
        if not isinstance(value.get(name), list):
            raise ValueError(f"WEX230: restitution {name} must be an array")
    if outcome == "completed" and value["blocked_by"]:
        raise ValueError("WEX230: completed restitution cannot contain blockers")
    if outcome == "blocked" and not value["blocked_by"]:
        raise ValueError("WEX230: blocked restitution requires an exact blocker")
    next_step = value.get("next")
    if not isinstance(next_step, dict) or set(next_step) != {"procedure_id", "step_id", "action"}:
        raise ValueError("WEX230: restitution must contain exactly one typed next step")
    command = value.get("command_or_response")
    if not isinstance(command, dict) or command.get("kind") not in {"command", "response"}:
        raise ValueError("WEX230: command_or_response must be command or response")
    if command["kind"] == "command":
        if set(command) != {"kind", "argv"} or not isinstance(command["argv"], list):
            raise ValueError("WEX230: command authority must be an argument array")
    elif set(command) != {"kind", "value"} or not isinstance(command["value"], str):
        raise ValueError("WEX230: response authority must be text")


def build_result(
    *,
    operation: str,
    outcome: str,
    primary: str,
    artifacts: Iterable[str],
    governing: Iterable[str],
    dependencies: Iterable[str],
    declared_paths: Iterable[str],
    changed_paths: Iterable[str],
    change_set_complete: bool,
    compliance: Mapping[str, Any],
    procedure: Mapping[str, Any],
    restitution: Mapping[str, Any],
    before: Iterable[Mapping[str, str]] = (),
    after: Iterable[Mapping[str, str]] = (),
    scoped_blockers: Iterable[Mapping[str, Any]] = (),
    repository_blockers: Iterable[Mapping[str, Any]] = (),
    unrelated_count: int = 0,
    writes: Iterable[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    if outcome not in OUTCOMES:
        raise ValueError(f"WEX230: invalid schema-2 outcome {outcome!r}")
    status = compliance.get("status")
    if status not in STATUSES:
        raise ValueError(f"WEX230: invalid compliance status {status!r}")
    _validate_restitution(restitution, outcome)
    result = {
        "schema": SCHEMA,
        "operation": {"kind": operation, "outcome": outcome},
        "selection": {"primary": primary, "artifacts": sorted(set(artifacts))},
        "scope": {
            "mode": "selected",
            "governing": sorted(set(governing)),
            "dependencies": sorted(set(dependencies)),
            "declared_paths": sorted(set(declared_paths), key=lambda item: (item.casefold(), item)),
            "changed_paths": sorted(set(changed_paths), key=lambda item: (item.casefold(), item)),
            "change_set_complete": bool(change_set_complete),
        },
        "compliance": dict(compliance),
        "procedure": dict(procedure),
        "state": {"before": list(before), "after": list(after)},
        "findings": {
            "scoped_blockers": list(scoped_blockers),
            "repository_blockers": list(repository_blockers),
            "unrelated_count": int(unrelated_count),
        },
        "mutation": {"writes": list(writes)},
        "restitution": dict(restitution),
    }
    result["result_sha256"] = restitution_digest(result)
    return result


def canonical_block_bytes(result: Mapping[str, Any]) -> bytes:
    """Canonical restitution bytes: UTF-8, LF, no trailing whitespace, one final LF (ADS-DIG-001)."""

    lines = [line.rstrip() for line in render_human(result).split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    return ("\n".join(lines) + "\n").encode("utf-8")


def restitution_digest(result: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_block_bytes(result)).hexdigest()


def render_json(result: Mapping[str, Any]) -> str:
    return json.dumps(result, indent=2, ensure_ascii=True) + "\n"


def _render_list(values: Iterable[object]) -> list[str]:
    items = _sentences(values)
    return [f"- {item}" for item in items] if items else ["None."]


def _render_decision(value: object) -> list[str]:
    if value is None:
        return ["None."]
    if not isinstance(value, Mapping):
        raise ValueError("WEX230: decision_required must be null or an object")
    outcomes = ", ".join(_text(item) for item in value.get("outcomes", []))
    return [
        (
            f"{_text(value.get('role', ''))} must decide {_text(value.get('decision', ''))} "
            f"for {_text(value.get('artifact', ''))} under {_text(value.get('decision_right', ''))}; "
            f"permitted outcomes: {outcomes}."
        )
    ]


def _render_command(value: Mapping[str, Any]) -> list[str]:
    if value.get("kind") == "command":
        return [shlex.join([_text(item) for item in value.get("argv", [])])]
    return [_text(value.get("value", "")) or "None."]


def render_human(result: Mapping[str, Any]) -> str:
    if result.get("schema") != SCHEMA:
        raise ValueError("WEX230: canonical restitution requires schema 2")
    restitution = result.get("restitution")
    if not isinstance(restitution, Mapping):
        raise ValueError("WEX230: schema-2 result has no restitution")
    outcome = str(result.get("operation", {}).get("outcome", ""))
    _validate_restitution(restitution, outcome)
    next_step = restitution["next"]
    lines = [
        "Outcome",
        "Completed." if outcome == "completed" else "Blocked.",
        "",
        "Done",
        *_render_list(restitution["done"]),
        "",
        "Not done",
        *_render_list(restitution["not_done"]),
    ]
    if outcome == "blocked":
        lines.extend(["", "Blocked by", *_render_list(restitution["blocked_by"])])
    lines.extend(
        [
            "",
            "Current lifecycle state",
            *_render_list(restitution["current_lifecycle_state"]),
            "",
            "Decision required",
            *_render_decision(restitution["decision_required"]),
            "",
            "Next",
            (
                f"{_text(next_step['action'])} "
                f"({_text(next_step['procedure_id'])}/{_text(next_step['step_id'])})."
            ),
            "",
            "Command or response",
            *_render_command(restitution["command_or_response"]),
        ]
    )
    # ECP-DIG-001: the change set and every predicate status are part of the
    # canonical block, so result_sha256 binds them (WO-ECP-003).
    scope = result.get("scope", {})
    changed = [_text(item) for item in scope.get("changed_paths", [])]
    lines.extend(["", "Change set", *([f"- {item}" for item in changed] or ["None."]), f"complete: {'true' if scope.get('change_set_complete') else 'false'}"])
    gate_lines = [
        f"{_text(predicate.get('id', ''))}: {_text(predicate.get('status', ''))}"
        for gate in result.get("compliance", {}).get("gates", [])
        for predicate in gate.get("predicates", [])
    ]
    lines.extend(["", "Gates", *(gate_lines or ["None."])])
    context = result.get("context")
    if context is not None:
        lines.extend(["", "Context", *_render_context(context)])
    if restitution["alternatives"]:
        lines.extend(["", "Alternatives", *_render_list(restitution["alternatives"])])
    return "\n".join(lines) + "\n"


def _render_context(value: object) -> list[str]:
    """Render the `next` context as ordered, labelled lines (ECP-NXT-007)."""

    if not isinstance(value, Mapping):
        raise ValueError("WEX230: context must be an object")
    state = value.get("state", {})
    step = value.get("next", {})
    argv = [_text(item) for item in step.get("argv", [])]
    lines = [
        f"State: {_text(state.get('status', ''))} ({_text(state.get('family', ''))})",
        "Governing: " + (", ".join(_text(item) for item in value.get("governing", [])) or "none"),
        "Declared paths: " + (", ".join(_text(item) for item in value.get("declared_paths", [])) or "none"),
        "Reading manifest:",
        *([f"- {_text(item)}" for item in value.get("reading_manifest", [])] or ["- none"]),
        f"Next argv: {shlex.join(argv) if argv else 'none'} ({_text(step.get('procedure_id', ''))}/{_text(step.get('step_id', ''))})",
        "Decision required: " + " ".join(_render_decision(value.get("decision_required"))),
    ]
    return lines
