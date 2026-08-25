#!/usr/bin/env python3
"""Validate a closed draft-change effect plan before an injected callback."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import PurePosixPath
from typing import Any, Callable, Iterable, Mapping, Sequence


SKILL = "harness-draft-change"
ALLOWED_EFFECTS = {"draft-create", "draft-revise", "planning-note-write", "risk-raise"}
RISK_PATH = re.compile(r"docs/engineering/[a-z0-9-]+/risks/RISK-[A-Z][A-Z0-9-]*-[0-9]{3}\.md")
ARTIFACT_ID = re.compile(r"[A-Z][A-Z0-9]*-[A-Z0-9]+-[0-9]+")
CONTROL = re.compile(r"[\x00-\x1f\x7f]")
MAX_PATHS = 128


class DraftGuardError(ValueError):
    """A bounded draft-plan rejection."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code


def portable_path(value: Any) -> str:
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
        raise DraftGuardError("AEXDRF007", "planned path is not portable")
    path = PurePosixPath(value)
    if path.is_absolute() or value.startswith("/") or any(part in {"", ".", ".."} for part in path.parts):
        raise DraftGuardError("AEXDRF007", "planned path escapes or is ambiguous")
    return path.as_posix()


def _closed_paths(values: Iterable[Any]) -> tuple[str, ...]:
    result = tuple(portable_path(value) for value in values)
    if not result or len(result) > MAX_PATHS or len({item.casefold() for item in result}) != len(result):
        raise DraftGuardError("AEXDRF008", "planned paths are empty, excessive, duplicate, or case-ambiguous")
    return result


def admit_draft_effect(
    request: Mapping[str, Any],
    *,
    recheck: Callable[[], Mapping[str, Any]],
    effect: Callable[[tuple[str, ...]], Any],
) -> Any:
    """Invoke ``effect`` only after activation, state, path, and fresh checks pass."""

    expected_fields = {"explicit_skill", "effect_class", "planned_paths", "allowed_paths", "revisions"}
    if set(request) != expected_fields:
        raise DraftGuardError("AEXDRF001", "request fields differ from the closed draft guard input")
    if request["explicit_skill"] != SKILL:
        raise DraftGuardError("AEXDRF002", "explicit harness-draft-change activation is required")
    if request["effect_class"] not in ALLOWED_EFFECTS:
        raise DraftGuardError("AEXDRF003", "effect class is not admitted")
    if not isinstance(request["planned_paths"], list) or not isinstance(request["allowed_paths"], list):
        raise DraftGuardError("AEXDRF004", "path sets must be arrays")
    planned = _closed_paths(request["planned_paths"])
    allowed = _closed_paths(request["allowed_paths"])
    if not set(planned).issubset(allowed):
        raise DraftGuardError("AEXDRF009", "planned path is outside declared draft destinations")
    if request["effect_class"] == "risk-raise" and any(RISK_PATH.fullmatch(path) is None for path in planned):
        raise DraftGuardError("AEXDRF013", "risk-raise admits only new risk artifact paths")
    if request["effect_class"] == "planning-note-write" and (
        len(planned) != 1 or not planned[0].startswith("docs/notes/") or not planned[0].endswith(".md")
    ):
        raise DraftGuardError("AEXDRF010", "planning-note effect requires one declared Markdown note")
    revisions = request["revisions"]
    if not isinstance(revisions, dict) or len(revisions) > MAX_PATHS:
        raise DraftGuardError("AEXDRF005", "revisions must be a bounded object")
    for artifact, state in revisions.items():
        if not isinstance(artifact, str) or ARTIFACT_ID.fullmatch(artifact) is None or state != "draft":
            raise DraftGuardError("AEXDRF011", "every selected revision must identify a current draft")
    fresh = recheck()
    if fresh != {"allowed_paths": list(allowed), "revisions": revisions}:
        raise DraftGuardError("AEXDRF012", "current draft state differs from the admitted plan")
    return effect(planned)


def _load_request(path: str) -> dict[str, Any]:
    try:
        value = json.loads(open(path, "r", encoding="utf-8").read())
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise DraftGuardError("AEXDRF006", "request is not readable UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise DraftGuardError("AEXDRF006", "request JSON must be an object")
    return value


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request-json", required=True)
    args = parser.parse_args(argv)
    try:
        request = _load_request(args.request_json)
        result = admit_draft_effect(
            request,
            recheck=lambda: {
                "allowed_paths": request.get("allowed_paths"),
                "revisions": request.get("revisions"),
            },
            effect=lambda paths: {"effect_invoked": False, "planned_paths": list(paths)},
        )
        print(json.dumps({"outcome": "planned", **result}, sort_keys=True, separators=(",", ":")))
        return 0
    except DraftGuardError as exc:
        print(json.dumps({"code": exc.code, "outcome": "blocked"}, sort_keys=True, separators=(",", ":")))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
