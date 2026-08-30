"""Versioned integrity semantics for harness-managed UTF-8 text."""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any


LOCK_SCHEMA = 3
HASH_ALGORITHM = "sha256"
HASH_MODE = "utf8-text-lf-v1"
EVALUATOR_PAYLOAD_MANIFEST = "se-harness-installed-payload-v1"
MANAGED_MODES = {"managed", "fragment"}
ENTRY_MODES = MANAGED_MODES | {"seed"}
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
EVALUATOR_FIELDS = {
    "version",
    "payload_manifest",
    "payload_sha256",
    "archive_name",
    "archive_sha256",
}
VERSION_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.!+\-]{0,127}")


class IntegrityError(ValueError):
    """A bounded managed-integrity error."""


def raw_sha256(value: bytes) -> str:
    """Return the exact-byte SHA-256 digest (hash-bound raw mode)."""

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
    if type(schema) is int and schema in {1, 2}:
        raise IntegrityError(
            f"lock schema {schema} predates the supported floor (schema {LOCK_SCHEMA}); "
            "remove the stale .engineering-harness.lock and re-adopt the repository "
            "with harnessctl adopt"
        )
    if type(schema) is not int or schema != LOCK_SCHEMA:
        raise IntegrityError("unsupported lock schema")
    if value.get("hash_algorithm") != HASH_ALGORITHM:
        raise IntegrityError("unsupported lock hash algorithm")
    if value.get("hash_mode") != HASH_MODE:
        raise IntegrityError("unsupported lock hash mode")
    if schema == LOCK_SCHEMA:
        evaluator = value.get("evaluator")
        if not isinstance(evaluator, dict):
            raise IntegrityError("schema-3 lock evaluator must be an object")
        unknown = set(evaluator) - EVALUATOR_FIELDS
        if unknown:
            raise IntegrityError(f"unknown evaluator lock field: {sorted(unknown)[0]}")
        version = evaluator.get("version")
        if not isinstance(version, str) or VERSION_PATTERN.fullmatch(version) is None:
            raise IntegrityError("invalid evaluator version")
        if value.get("tool_version") != version:
            raise IntegrityError("lock tool version and evaluator version differ")
        if evaluator.get("payload_manifest") != EVALUATOR_PAYLOAD_MANIFEST:
            raise IntegrityError("unsupported evaluator payload manifest")
        payload_sha256 = evaluator.get("payload_sha256")
        if not isinstance(payload_sha256, str) or SHA256_PATTERN.fullmatch(payload_sha256) is None:
            raise IntegrityError("invalid evaluator payload SHA-256")
        archive_name = evaluator.get("archive_name")
        archive_sha256 = evaluator.get("archive_sha256")
        if (archive_name is None) != (archive_sha256 is None):
            raise IntegrityError("evaluator archive name and SHA-256 must appear together")
        if archive_name is not None:
            expected_name = f"se_harness-{version.replace('-', '_')}-py3-none-any.whl"
            if not isinstance(archive_name, str) or archive_name != expected_name:
                raise IntegrityError("invalid evaluator archive name")
            if not isinstance(archive_sha256, str) or SHA256_PATTERN.fullmatch(archive_sha256) is None:
                raise IntegrityError("invalid evaluator archive SHA-256")
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


def compare_lock_entry(
    lock: dict[str, Any],
    entry: dict[str, Any],
    current: bytes,
) -> str:
    """Return canonical or mismatch."""

    expected = entry.get("sha256")
    return "canonical" if canonical_sha256(current) == expected else "mismatch"
