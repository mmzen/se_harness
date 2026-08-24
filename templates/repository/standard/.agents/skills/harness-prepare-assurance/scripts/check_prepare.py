#!/usr/bin/env python3
"""Admit one exact-candidate VREC preparation before an injected callback."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import PurePosixPath
from typing import Any, Callable, Mapping, Sequence


SKILL = "harness-prepare-assurance"
VREC_ID = re.compile(r"VREC-[A-Z0-9]+-[0-9]+")
COMMIT = re.compile(r"[0-9a-f]{40}|[0-9a-f]{64}")
CONTROL = re.compile(r"[\x00-\x1f\x7f]")


class AssuranceGuardError(ValueError):
    """A bounded assurance-preparation rejection."""

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
        raise AssuranceGuardError("AEXASR007", "record destination is not portable")
    path = PurePosixPath(value)
    if path.is_absolute() or value.startswith("/") or any(part in {"", ".", ".."} for part in path.parts):
        raise AssuranceGuardError("AEXASR007", "record destination escapes or is ambiguous")
    selected = path.as_posix()
    if not selected.startswith("docs/engineering/") or not selected.endswith(".md"):
        raise AssuranceGuardError("AEXASR007", "record destination is not a canonical engineering Markdown path")
    return selected


def admit_assurance_preparation(
    request: Mapping[str, Any],
    *,
    recheck: Callable[[], Mapping[str, Any]],
    effect: Callable[[str], Any],
) -> Any:
    """Invoke ``effect`` only for a current clean candidate and unused VREC."""

    fields = {
        "explicit_skill", "record_id", "record_destination", "candidate_commit",
        "candidate_ready", "record_exists", "preparation_actor",
    }
    if set(request) != fields:
        raise AssuranceGuardError("AEXASR001", "request fields differ from the closed assurance guard input")
    if request["explicit_skill"] != SKILL:
        raise AssuranceGuardError("AEXASR002", "explicit harness-prepare-assurance activation is required")
    if not isinstance(request["record_id"], str) or VREC_ID.fullmatch(request["record_id"]) is None:
        raise AssuranceGuardError("AEXASR003", "one valid VREC identifier is required")
    if not isinstance(request["candidate_commit"], str) or COMMIT.fullmatch(request["candidate_commit"]) is None:
        raise AssuranceGuardError("AEXASR004", "an exact lowercase candidate commit is required")
    if request["candidate_ready"] is not True or request["record_exists"] is not False:
        raise AssuranceGuardError("AEXASR005", "candidate must be ready and the VREC identifier unused")
    actor = request["preparation_actor"]
    if not isinstance(actor, str) or not actor.strip() or len(actor) > 256 or CONTROL.search(actor):
        raise AssuranceGuardError("AEXASR006", "an explicit bounded preparation actor is required")
    destination = portable_path(request["record_destination"])
    expected = {
        "candidate_commit": request["candidate_commit"],
        "candidate_ready": True,
        "record_exists": False,
        "record_id": request["record_id"],
        "record_destination": destination,
    }
    if recheck() != expected:
        raise AssuranceGuardError("AEXASR008", "current candidate or VREC state differs from the admitted plan")
    return effect(destination)


def _load_request(path: str) -> dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            value = json.load(handle)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise AssuranceGuardError("AEXASR009", "request is not readable UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise AssuranceGuardError("AEXASR009", "request JSON must be an object")
    return value


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request-json", required=True)
    args = parser.parse_args(argv)
    try:
        request = _load_request(args.request_json)
        destination = portable_path(request.get("record_destination"))
        result = admit_assurance_preparation(
            request,
            recheck=lambda: {
                "candidate_commit": request.get("candidate_commit"),
                "candidate_ready": request.get("candidate_ready"),
                "record_exists": request.get("record_exists"),
                "record_id": request.get("record_id"),
                "record_destination": destination,
            },
            effect=lambda path: {"effect_invoked": False, "planned_paths": [path]},
        )
        print(json.dumps({"outcome": "planned", **result}, sort_keys=True, separators=(",", ":")))
        return 0
    except AssuranceGuardError as exc:
        print(json.dumps({"code": exc.code, "outcome": "blocked"}, sort_keys=True, separators=(",", ":")))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
