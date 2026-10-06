"""SPEC-HAG-001 byte identities, independent of storage and evaluator policy.

These functions bind content already parsed/admitted by the released evaluator.
They do not parse formal artifacts, grant authority, or save drafts. Wire-shape
and evaluator-identity checks remain the caller's responsibility.
"""
from __future__ import annotations

import base64
import binascii
import hashlib
import json
from typing import Any

REVISION_SCHEME = "se-harness-artifact-revision/v1"
BASELINE_SCHEME = "se-harness-artifact-baseline/v1"
DOCUMENT_LIMIT = 1024 * 1024


class CanonicalError(ValueError):
    """The input cannot represent the specified canonical content."""


def _reject_number(value: str) -> None:
    raise CanonicalError("JSON numbers must be integers")


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CanonicalError("duplicate JSON object key")
        result[key] = value
    return result


def decode_json(raw: bytes, *, max_bytes: int) -> Any:
    """Decode bounded UTF-8 without duplicate keys, BOM or floating numbers."""
    if type(raw) is not bytes or type(max_bytes) is not int or max_bytes < 0:
        raise CanonicalError("expected bytes and a non-negative byte limit")
    if len(raw) > max_bytes:
        raise CanonicalError("JSON exceeds the byte limit")
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object,
                           parse_float=_reject_number, parse_constant=_reject_number)
        _json_value(value)
        return value
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise CanonicalError("invalid UTF-8 JSON") from exc


def _json_value(value: Any) -> None:
    if value is None or type(value) in (bool, int):
        return
    if type(value) is str:
        value.encode("utf-8", errors="strict")
        return
    if type(value) is list:
        for item in value:
            _json_value(item)
        return
    if type(value) is dict and all(type(key) is str for key in value):
        for key, item in value.items():
            _json_value(key)
            _json_value(item)
        return
    raise CanonicalError("only JSON objects, arrays, strings, integers, booleans and null are supported")


def canonical_json(value: Any) -> bytes:
    """Preserve sequence and Unicode forms; only object keys are reordered."""
    try:
        _json_value(value)
        return json.dumps(value, sort_keys=True, ensure_ascii=False,
                          separators=(",", ":"), allow_nan=False).encode("utf-8")
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise CanonicalError("invalid or recursive JSON value") from exc


def _copy(value: Any) -> Any:
    raw = canonical_json(value)
    return decode_json(raw, max_bytes=len(raw))


def named_digest(scheme: str, value: Any) -> str:
    if not isinstance(scheme, str) or not scheme or "\n" in scheme or "\r" in scheme:
        raise CanonicalError("invalid digest scheme")
    return hashlib.sha256(scheme.encode("utf-8") + b"\n" + canonical_json(value)).hexdigest()


def _relations(relations: dict[str, list[str]]) -> dict[str, list[str]]:
    if type(relations) is not dict:
        raise CanonicalError("relations must be an object")
    result = {}
    for kind, targets in relations.items():
        if (type(kind) is not str or not kind or type(targets) is not list
                or any(type(target) is not str or not target for target in targets)):
            raise CanonicalError("relation sets require a name and string targets")
        result[kind] = sorted(set(targets))
    return dict(sorted(result.items()))


def _source_path(path: str | None) -> None:
    if path is None:
        return
    if (type(path) is not str or "\\" in path or ":" in path or "\x00" in path
            or any(part in ("", ".", "..") for part in path.split("/"))):
        raise CanonicalError("original path must be a contained relative POSIX path")


def make_revision(*, project_id: str, artifact_id: str, document: bytes,
                  declared_relations: dict[str, list[str]], provenance: dict[str, Any],
                  original_path: str | None = None) -> dict[str, Any]:
    """Bind exact document bytes to explicit parsed identity and provenance."""
    if type(document) is not bytes or len(document) > DOCUMENT_LIMIT:
        raise CanonicalError("document must be bytes within the 1 MiB limit")
    try:
        document.decode("utf-8", errors="strict")
    except UnicodeError as exc:
        raise CanonicalError("document must be UTF-8") from exc
    _source_path(original_path)
    envelope = {"schema": REVISION_SCHEME, "project_id": project_id,
                "artifact_id": artifact_id, "document_sha256": hashlib.sha256(document).hexdigest(),
                "original_path": original_path, "declared_relations": _relations(declared_relations),
                "provenance": _copy(provenance)}
    return {"revision_id": "sha256:" + named_digest(REVISION_SCHEME, envelope),
            "envelope": envelope, "document_base64": base64.b64encode(document).decode("ascii")}


def verify_revision(stored: dict[str, Any]) -> dict[str, Any]:
    """Reject inconsistent bytes/identities; return an independent value."""
    if type(stored) is not dict or set(stored) != {"revision_id", "envelope", "document_base64"}:
        raise CanonicalError("invalid stored revision fields")
    try:
        encoded = stored["document_base64"]
        if type(encoded) is not str or len(encoded) > 4 * ((DOCUMENT_LIMIT + 2) // 3):
            raise CanonicalError("encoded document exceeds the 1 MiB document limit")
        document = base64.b64decode(encoded, validate=True)
        if base64.b64encode(document).decode("ascii") != encoded:
            raise CanonicalError("document base64 is not canonical")
        envelope = stored["envelope"]
        rebuilt = make_revision(project_id=envelope["project_id"], artifact_id=envelope["artifact_id"],
                                document=document, declared_relations=envelope["declared_relations"],
                                provenance=envelope["provenance"], original_path=envelope["original_path"])
    except (KeyError, TypeError, ValueError, binascii.Error) as exc:
        raise CanonicalError("invalid stored revision") from exc
    if canonical_json(rebuilt) != canonical_json(stored):
        raise CanonicalError("stored revision bytes, envelope or identity disagree")
    return rebuilt


def make_baseline(*, project_id: str, revisions: dict[str, dict[str, Any]],
                  provenance: dict[str, Any], evaluator: dict[str, str]) -> dict[str, Any]:
    """Freeze a complete selection as a value; this performs no database write."""
    selected = {}
    for artifact_id, stored in sorted(revisions.items()):
        revision = verify_revision(stored)
        envelope = revision["envelope"]
        if envelope["project_id"] != project_id or envelope["artifact_id"] != artifact_id:
            raise CanonicalError("revision does not belong to the selected project and artifact")
        selected[artifact_id] = revision
    edges = set()
    for revision in selected.values():
        for kind, targets in revision["envelope"]["declared_relations"].items():
            for target in targets:
                if target not in selected:
                    raise CanonicalError("unresolved declared target: " + target)
                edges.add((revision["revision_id"], kind, selected[target]["revision_id"]))
    manifest = {"schema": BASELINE_SCHEME, "project_id": project_id,
                "revision_scheme": REVISION_SCHEME,
                "selection": {key: value["revision_id"] for key, value in selected.items()},
                "resolved_relations": [list(edge) for edge in sorted(edges)],
                "provenance": _copy(provenance), "evaluator": _copy(evaluator)}
    return {"schema": BASELINE_SCHEME,
            "baseline_id": BASELINE_SCHEME + ":sha256:" + named_digest(BASELINE_SCHEME, manifest),
            "manifest": manifest}
