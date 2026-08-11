"""Versioned integrity semantics for harness-managed UTF-8 text."""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any


LOCK_SCHEMA = 2
HASH_ALGORITHM = "sha256"
HASH_MODE = "utf8-text-lf-v1"
MANAGED_MODES = {"managed", "fragment"}
ENTRY_MODES = MANAGED_MODES | {"seed"}
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")


class IntegrityError(ValueError):
    """A bounded managed-integrity error."""


def raw_sha256(value: bytes) -> str:
    """Return the legacy exact-byte SHA-256 digest."""

    return hashlib.sha256(value).hexdigest()


def canonical_text_bytes(value: bytes) -> bytes:
    """Return the utf8-text-lf-v1 canonical representation."""

    try:
        text = value.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise IntegrityError("managed text must be valid UTF-8") from exc
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def canonical_sha256(value: bytes) -> str:
    """Hash managed text after versioned newline canonicalization."""

    return raw_sha256(canonical_text_bytes(value))


def canonical_text_equal(left: bytes, right: bytes) -> bool:
    return canonical_text_bytes(left) == canonical_text_bytes(right)


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise IntegrityError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def parse_lock(text: str) -> dict[str, Any]:
    try:
        value = json.loads(text, object_pairs_hook=_unique_object)
    except json.JSONDecodeError as exc:
        raise IntegrityError(f"invalid lock JSON: {exc}") from exc
    return validate_lock(value)


def validate_lock(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise IntegrityError("lock root must be an object")
    schema = value.get("schema")
    if type(schema) is not int or schema not in {1, LOCK_SCHEMA}:
        raise IntegrityError("unsupported lock schema")
    if schema == LOCK_SCHEMA:
        if value.get("hash_algorithm") != HASH_ALGORITHM:
            raise IntegrityError("unsupported lock hash algorithm")
        if value.get("hash_mode") != HASH_MODE:
            raise IntegrityError("unsupported lock hash mode")
    files = value.get("files")
    if not isinstance(files, dict):
        raise IntegrityError("lock files must be an object")
    for relative, entry in files.items():
        if not isinstance(relative, str) or not relative:
            raise IntegrityError("lock paths must be non-empty strings")
        if not isinstance(entry, dict):
            raise IntegrityError(f"lock entry must be an object: {relative}")
        mode = entry.get("mode")
        if mode not in ENTRY_MODES:
            raise IntegrityError(f"unsupported lock entry mode for {relative}")
        if mode == "seed":
            if entry.get("state") not in {"present", "removed"}:
                raise IntegrityError(f"invalid seed state for {relative}")
            continue
        digest = entry.get("sha256")
        if not isinstance(digest, str) or SHA256_PATTERN.fullmatch(digest) is None:
            raise IntegrityError(f"invalid SHA-256 for {relative}")
    return value


def legacy_tracked_sha256(value: bytes, mode: str) -> str:
    """Reproduce schema-1 hashing, including its fragment CRLF behavior."""

    legacy = value.replace(b"\r\n", b"\n") if mode == "fragment" else value
    return raw_sha256(legacy)


def digest_for_schema(value: bytes, schema: int, mode: str) -> str:
    if schema == 1:
        return legacy_tracked_sha256(value, mode)
    if schema == LOCK_SCHEMA:
        return canonical_sha256(value)
    raise IntegrityError("unsupported lock schema")


def compare_lock_entry(
    lock: dict[str, Any],
    entry: dict[str, Any],
    current: bytes,
    *,
    desired: bytes | None = None,
) -> str:
    """Return exact, canonical, legacy-canonical, or mismatch."""

    schema = lock.get("schema")
    expected = entry.get("sha256")
    if schema == LOCK_SCHEMA:
        return "canonical" if canonical_sha256(current) == expected else "mismatch"
    if schema == 1:
        if legacy_tracked_sha256(current, str(entry.get("mode"))) == expected:
            return "exact"
        if desired is not None and canonical_text_equal(current, desired):
            return "legacy-canonical"
        return "mismatch"
    raise IntegrityError("unsupported lock schema")
