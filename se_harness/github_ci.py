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
_WORK_ORDER_LINE_WITH_CR = re.compile(
    r"^Harness-Work-Order:[ \t]*WO-[A-Z][A-Z0-9-]*-\d{3}[ \t]*(\r)$",
    re.MULTILINE,
)
RESTITUTION_LINE = re.compile(
    r"^Harness-Restitution:[ \t]*([0-9a-f]{64})[ \t]*$",
    re.MULTILINE,
)
FIELDS = ("work-order", "restitution-digest")


class SelectionError(ValueError):
    """A bounded pull-request work-order selection error."""


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise SelectionError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def carriage_return_trailer_offsets(body: str) -> list[int]:
    """UTF-8 byte offsets of a carriage return that ends a Harness-Work-Order line (W-ADS-001)."""

    return [
        len(body[: match.start(1)].encode("utf-8"))
        for match in _WORK_ORDER_LINE_WITH_CR.finditer(body)
    ]


def select_work_order(body: str) -> str:
    """Select exactly one standalone work-order declaration."""

    if not isinstance(body, str):
        raise SelectionError("pull-request body must be text")
    matches = WORK_ORDER_LINE.findall(body)
    if len(matches) != 1:
        offsets = carriage_return_trailer_offsets(body)
        if offsets:
            raise SelectionError(
                f"W-ADS-001: the Harness-Work-Order line ends with a carriage return at byte offset {offsets[0]}; "
                "write the body with LF line endings (newline=\"\\n\" in Python, or core.autocrlf=false) and push again"
            )
        raise SelectionError(
            f"expected exactly one standalone Harness-Work-Order field; found {len(matches)}"
        )
    return matches[0]


def select_restitution_digest(body: str) -> str:
    """Select at most one declared restitution digest; empty text when none is declared."""

    if not isinstance(body, str):
        raise SelectionError("pull-request body must be text")
    matches = RESTITUTION_LINE.findall(body)
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
    return select_work_order(pull_request.get("body"))


def render_pull_request_body(root: Path, artifact: Any, *, packet_directory: Path) -> str:
    """The pull-request body for one work order (ECP-PRB-001 to -005).

    LF line endings only; the first non-empty line is the standalone
    `Harness-Work-Order` field; a retained `handoff.json` of schema 2 adds one
    standalone `Harness-Restitution` line; the `Verification` section lists
    every evidence path under the packet directory.
    """

    if artifact.artifact_type != "work_order":
        raise SelectionError(f"WEX-ECP-014: {artifact.artifact_id} is not a work order")
    if artifact.status == "draft":
        raise SelectionError(f"WEX-ECP-014: {artifact.artifact_id} is draft; a pull request needs an approved or later work order")
    lines = [f"Harness-Work-Order: {artifact.artifact_id}"]
    handoff = packet_directory / "handoff.json"
    if handoff.is_file():
        try:
            value = json.loads(handoff.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise SelectionError(f"WEX-ECP-014: {handoff.relative_to(root).as_posix()} is not readable JSON: {exc}") from exc
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
    if select_work_order(body) != artifact.artifact_id or carriage_return_trailer_offsets(body):
        raise SelectionError("WEX-ECP-014: the generated body does not round-trip through the selector")
    return body

