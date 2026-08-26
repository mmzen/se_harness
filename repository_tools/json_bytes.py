"""The one definition of the JSON and hashing helpers the CI scripts share.

`WO-CIP-002` (`REQ-CIP-003`, `SPEC-CIP-001` CIP-QLF 5). Before it, canonical
JSON encoding, duplicate-key-rejecting JSON parsing and streaming SHA-256 were
each defined three or four times across `.github/scripts/`, once per script and
each raising that script's own error type. They are defined here once; a
script passes its own error class through `error=` so its callers keep seeing
the exception type they always did. Standard library only.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

DEFAULT_MAX_BYTES = 16 * 1024 * 1024


def canonical_json_bytes(value: Any, *, error: type[Exception] = ValueError) -> bytes:
    """Sorted keys, minimal separators, UTF-8, one trailing LF; refuses NaN and unencodable values."""

    try:
        rendered = json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(",", ":"), sort_keys=True)
    except (TypeError, ValueError) as exc:
        raise error("value cannot be encoded as canonical JSON") from exc
    return (rendered + "\n").encode("utf-8")


def pretty_json_bytes(value: Any) -> bytes:
    """Sorted keys, two-space indent, UTF-8, one trailing LF: the retained-document form."""

    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path, *, error: type[Exception] = OSError, label: str | None = None) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(block)
    except OSError as exc:
        raise error(f"cannot hash file: {label or path}") from exc
    return digest.hexdigest()


def parse_json_object(
    raw: bytes,
    *,
    error: type[Exception] = ValueError,
    label: str = "document",
    max_bytes: int | None = DEFAULT_MAX_BYTES,
) -> dict[str, Any]:
    """Parse one JSON object from bytes, refusing a BOM, an oversized input, duplicate keys and a non-object root."""

    if max_bytes is not None and len(raw) > max_bytes:
        raise error(f"{label} exceeds the size limit")
    if raw.startswith(b"\xef\xbb\xbf"):
        raise error(f"{label} must not contain a UTF-8 BOM")

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, item in pairs:
            if key in result:
                raise error(f"{label} contains duplicate key: {key}")
            result[key] = item
        return result

    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=unique)
    except error:
        raise
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise error(f"{label} is not valid UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise error(f"{label} root must be an object")
    return value


def read_json_object(path: Path, *, error: type[Exception] = ValueError, max_bytes: int | None = DEFAULT_MAX_BYTES) -> dict[str, Any]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise error(f"invalid JSON file: {path}") from exc
    return parse_json_object(raw, error=error, label=str(path), max_bytes=max_bytes)
