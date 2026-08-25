#!/usr/bin/env python3
"""Admit one in-progress work-order effect before an injected callback."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import PurePosixPath
from typing import Any, Callable, Iterable, Mapping, Sequence


SKILL = "harness-execute-work-order"
ALLOWED_EFFECTS = {"implementation-write", "test-execution", "evidence-write", "risk-raise"}
RISK_PATH = re.compile(r"docs/engineering/[a-z0-9-]+/risks/RISK-[A-Z][A-Z0-9-]*-[0-9]{3}\.md")
ARTIFACT_ID = re.compile(r"WO-[A-Z0-9]+-[0-9]+")
CONTROL = re.compile(r"[\x00-\x1f\x7f]")
MAX_PATHS = 512


class ScopeGuardError(ValueError):
    """A bounded work-order scope rejection."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code


def portable_path(value: Any, *, allow_prefix: bool = False) -> str:
    if (
        not isinstance(value, str)
        or not value
        or len(value) > 4096
        or CONTROL.search(value)
        or "\\" in value
        or "://" in value
        or "*" in value
        or "?" in value
    ):
        raise ScopeGuardError("AEXEXE007", "path is not portable")
    trailing = value.endswith("/")
    candidate = value[:-1] if trailing else value
    path = PurePosixPath(candidate)
    if path.is_absolute() or candidate.startswith("/") or any(part in {"", ".", ".."} for part in path.parts):
        raise ScopeGuardError("AEXEXE007", "path escapes or is ambiguous")
    return path.as_posix() + ("/" if trailing and allow_prefix else "")


def _paths(values: Iterable[Any], *, allow_prefix: bool = False) -> tuple[str, ...]:
    result = tuple(portable_path(value, allow_prefix=allow_prefix) for value in values)
    if not result or len(result) > MAX_PATHS or len({item.casefold() for item in result}) != len(result):
        raise ScopeGuardError("AEXEXE008", "paths are empty, excessive, duplicate, or case-ambiguous")
    return result


def _admitted(path: str, scope: tuple[str, ...]) -> bool:
    folded = path.casefold()
    for item in scope:
        item_folded = item.casefold()
        if item.endswith("/") and folded.startswith(item_folded):
            return True
        if folded == item_folded:
            return True
    return False


def scope_digest(scope: tuple[str, ...]) -> str:
    raw = json.dumps(list(scope), ensure_ascii=False, separators=(",", ":")).encode("utf-8") + b"\n"
    return hashlib.sha256(raw).hexdigest()


def admit_work_order_effect(
    request: Mapping[str, Any],
    *,
    recheck: Callable[[], Mapping[str, Any]],
    effect: Callable[[tuple[str, ...]], Any],
) -> Any:
    """Invoke ``effect`` only for current in-progress work and admitted paths."""

    fields = {"explicit_skill", "work_order", "state", "effect_class", "planned_paths", "execution_scope"}
    if set(request) != fields:
        raise ScopeGuardError("AEXEXE001", "request fields differ from the closed scope guard input")
    if request["explicit_skill"] != SKILL:
        raise ScopeGuardError("AEXEXE002", "explicit harness-execute-work-order activation is required")
    if not isinstance(request["work_order"], str) or ARTIFACT_ID.fullmatch(request["work_order"]) is None:
        raise ScopeGuardError("AEXEXE003", "one valid work-order ID is required")
    if request["state"] != "in_progress":
        raise ScopeGuardError("AEXEXE004", "the selected work order is not in_progress")
    if request["effect_class"] not in ALLOWED_EFFECTS:
        raise ScopeGuardError("AEXEXE005", "effect class is not admitted")
    if not isinstance(request["planned_paths"], list) or not isinstance(request["execution_scope"], list):
        raise ScopeGuardError("AEXEXE006", "path sets must be arrays")
    planned = _paths(request["planned_paths"])
    scope = _paths(request["execution_scope"], allow_prefix=True)
    if request["effect_class"] == "risk-raise":
        # A new risk is always an admitted effect (RSK2-SKL-001); it must be a risk file and nothing else.
        if any(RISK_PATH.fullmatch(path) is None for path in planned):
            raise ScopeGuardError("AEXEXE011", "risk-raise admits only new risk artifact paths")
    elif any(not _admitted(path, scope) for path in planned):
        raise ScopeGuardError("AEXEXE009", "planned path is outside the current execution scope")
    expected = {
        "work_order": request["work_order"],
        "state": "in_progress",
        "scope_sha256": scope_digest(scope),
    }
    if recheck() != expected:
        raise ScopeGuardError("AEXEXE010", "current work-order state or scope differs from the admitted plan")
    return effect(planned)


def _load_request(path: str) -> dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            value = json.load(handle)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ScopeGuardError("AEXEXE011", "request is not readable UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise ScopeGuardError("AEXEXE011", "request JSON must be an object")
    return value


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request-json", required=True)
    args = parser.parse_args(argv)
    try:
        request = _load_request(args.request_json)
        scope = _paths(request.get("execution_scope", []), allow_prefix=True)
        result = admit_work_order_effect(
            request,
            recheck=lambda: {
                "work_order": request.get("work_order"),
                "state": request.get("state"),
                "scope_sha256": scope_digest(scope),
            },
            effect=lambda paths: {"effect_invoked": False, "planned_paths": list(paths)},
        )
        print(json.dumps({"outcome": "planned", **result}, sort_keys=True, separators=(",", ":")))
        return 0
    except ScopeGuardError as exc:
        print(json.dumps({"code": exc.code, "outcome": "blocked"}, sort_keys=True, separators=(",", ":")))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
