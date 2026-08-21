"""Typed workflow procedure resolution without shell evaluation."""

from __future__ import annotations

import re
from typing import Any, Iterable, Mapping

from se_harness.workflow_contract import ContractError


_PLACEHOLDER = re.compile(r"\{([a-z][a-z0-9_]*)\}")
_ARTIFACT_ID = re.compile(r"^[A-Z][A-Z0-9-]*-\d{3}$")
_CONTROL = re.compile(r"[\x00-\x1f\x7f]")


class ProcedureError(RuntimeError):
    """A typed procedure or parameter cannot resolve safely."""


def _typed(value: str, parameter_type: str, name: str) -> str:
    if not value or len(value) > 4096 or _CONTROL.search(value):
        raise ProcedureError(f"WEX221: procedure parameter {name} has an invalid value")
    if parameter_type == "artifact_id" and _ARTIFACT_ID.fullmatch(value) is None:
        raise ProcedureError(f"WEX221: procedure parameter {name} is not an artifact ID")
    if parameter_type == "path":
        parts = value.split("/")
        if value.startswith("/") or "\\" in value or ":" in value or any(part in {"", ".", ".."} for part in parts):
            raise ProcedureError(f"WEX221: procedure parameter {name} is not a normalized path")
    if parameter_type == "status" and re.fullmatch(r"[a-z][a-z0-9_]*", value) is None:
        raise ProcedureError(f"WEX221: procedure parameter {name} is not a status")
    return value


def _values(procedure: Mapping[str, Any], supplied: Mapping[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for parameter in procedure.get("parameters", []):
        name = parameter["name"]
        value = supplied.get(name)
        cardinality = parameter["cardinality"]
        parameter_type = parameter["type"]
        if cardinality == "one":
            if not isinstance(value, str) or not value:
                raise ProcedureError(f"WEX221: required procedure parameter {name} is unavailable")
            result[name] = _typed(value, parameter_type, name)
        elif cardinality == "zero_or_one":
            if value is not None and (not isinstance(value, str) or not value):
                raise ProcedureError(f"WEX221: optional procedure parameter {name} has an invalid value")
            result[name] = _typed(value, parameter_type, name) if value is not None else None
        else:
            if not isinstance(value, (list, tuple)) or not value or not all(isinstance(item, str) and item for item in value):
                raise ProcedureError(f"WEX221: repeated procedure parameter {name} is unavailable")
            item_type = "path" if parameter_type == "path_list" else parameter_type
            result[name] = [_typed(item, item_type, name) for item in value]
    return result


def _expand_text(template: str, values: Mapping[str, Any]) -> str:
    def substitute(match: re.Match[str]) -> str:
        value = values.get(match.group(1))
        if isinstance(value, list):
            raise ProcedureError(f"WEX221: repeated parameter {match.group(1)} must occupy one argv element")
        if value is None:
            raise ProcedureError(f"WEX221: procedure parameter {match.group(1)} is unavailable")
        return str(value)

    return _PLACEHOLDER.sub(substitute, template)


def _expand_argv(argv: Iterable[str], values: Mapping[str, Any]) -> list[str]:
    result: list[str] = []
    for item in argv:
        match = _PLACEHOLDER.fullmatch(item)
        if match is not None and isinstance(values.get(match.group(1)), list):
            result.extend(str(value) for value in values[match.group(1)])
        else:
            result.append(_expand_text(item, values))
    return result


def _expand_list(values_to_expand: Iterable[str], values: Mapping[str, Any]) -> list[str]:
    return [_expand_text(item, values) for item in values_to_expand]


def resolve_procedure(
    procedures: Mapping[str, Mapping[str, Any]],
    procedure_id: str,
    parameters: Mapping[str, Any],
) -> dict[str, Any]:
    procedure = procedures.get(procedure_id)
    if procedure is None:
        raise ProcedureError(f"WEX220: unknown procedure {procedure_id}")
    values = _values(procedure, parameters)
    resolved: list[dict[str, Any]] = []
    for step in procedure["steps"]:
        item: dict[str, Any] = {
            "id": step["id"],
            "kind": step["kind"],
            "gate_ids": list(step["gate_ids"]),
            "effects": _expand_list(step["effects"], values),
            "non_effects": _expand_list(step["non_effects"], values),
        }
        if step["kind"] == "command":
            item["argv"] = _expand_argv(step["argv"], values)
        elif step["kind"] == "decision":
            item.update(
                {
                    "decision_right": step["decision_right"],
                    "role": step["role"],
                    "artifact": _expand_text(step["artifact"], values),
                    "decision": _expand_text(step["decision"], values),
                    "outcomes": list(step["outcomes"]),
                    "response": _expand_text(step["response"], values),
                }
            )
        else:
            item["procedure_id"] = step["procedure_id"]
        resolved.append(item)
    return {"id": procedure_id, "parameters": dict(values), "steps": resolved}


def select_current_step(
    procedure: Mapping[str, Any],
    *,
    checkpoint: str,
    passed: bool,
) -> Mapping[str, Any]:
    steps = procedure.get("steps", [])
    if not isinstance(steps, list) or not steps:
        raise ProcedureError(f"WEX220: procedure {procedure.get('id')} has no steps")
    if checkpoint == "start":
        if passed:
            return next((step for step in steps if step.get("kind") == "decision"), steps[-1])
        return next(
            (
                step for step in steps
                if step.get("kind") == "command" and "preflight" in step.get("argv", [])
            ),
            steps[0],
        )
    if checkpoint == "handoff":
        if passed:
            return next((step for step in steps if step.get("kind") == "decision"), steps[-1])
        return next(
            (
                step for step in steps
                if step.get("kind") == "command" and "check" in step.get("argv", [])
            ),
            steps[0],
        )
    return steps[0]


def command_or_response(step: Mapping[str, Any]) -> dict[str, Any]:
    if step.get("kind") == "command":
        return {"kind": "command", "argv": list(step.get("argv", []))}
    if step.get("kind") == "decision":
        return {"kind": "response", "value": str(step.get("response", ""))}
    return {"kind": "response", "value": f"Continue with {step.get('procedure_id')}."}


def decision_required(step: Mapping[str, Any]) -> dict[str, Any] | None:
    if step.get("kind") != "decision":
        return None
    return {
        "decision_right": step["decision_right"],
        "role": step["role"],
        "artifact": step["artifact"],
        "decision": step["decision"],
        "outcomes": list(step["outcomes"]),
    }


def ensure_validated(procedures: Mapping[str, Mapping[str, Any]]) -> None:
    """Keep a stable public failure type for callers validating injected policy."""

    if not procedures:
        raise ContractError("procedure registry is empty")
