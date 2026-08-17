"""Bounded GitHub pull-request inputs owned by the released package."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


MAX_EVENT_BYTES = 2 * 1024 * 1024
WORK_ORDER_LINE = re.compile(
    r"^Harness-Work-Order:[ \t]*(WO-[A-Z][A-Z0-9-]*-\d{3})[ \t]*$",
    re.MULTILINE,
)


class SelectionError(ValueError):
    """A bounded pull-request work-order selection error."""


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise SelectionError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def select_work_order(body: str) -> str:
    """Select exactly one standalone work-order declaration."""

    if not isinstance(body, str):
        raise SelectionError("pull-request body must be text")
    matches = WORK_ORDER_LINE.findall(body)
    if len(matches) != 1:
        raise SelectionError(
            f"expected exactly one standalone Harness-Work-Order field; found {len(matches)}"
        )
    return matches[0]


def select_from_event(path: Path) -> str:
    """Read one bounded GitHub event and select its declared work order."""

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
    return select_work_order(pull_request.get("body"))
