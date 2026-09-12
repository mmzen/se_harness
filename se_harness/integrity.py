"""Versioned integrity semantics for harness-managed UTF-8 text."""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import tomllib
from collections.abc import Callable
from pathlib import Path
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
#: ECP-PRM-014: the one grammar both wheel-metadata parsers apply, X.Y.Z with an optional suffix.
WHEEL_VERSION_PATTERN = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+(?:[A-Za-z0-9.+-]*)?")


class IntegrityError(ValueError):
    """A bounded managed-integrity error."""


def raw_sha256(value: bytes) -> str:
    """Return the exact-byte SHA-256 digest (hash-bound raw mode)."""

    return hashlib.sha256(value).hexdigest()


def canonical_text(value: str) -> str:
    """The utf8-text-lf-v1 line-ending form of already decoded text: CRLF and lone CR become LF (ECP-PRM-010)."""

    return value.replace("\r\n", "\n").replace("\r", "\n")


def canonical_text_bytes(value: bytes) -> bytes:
    """Return the utf8-text-lf-v1 canonical representation."""

    try:
        text = value.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise IntegrityError("managed text must be valid UTF-8") from exc
    return canonical_text(text).encode("utf-8")


def canonical_json_bytes(value: Any, *, ensure_ascii: bool) -> bytes:
    """Sorted keys, minimal separators, one trailing LF, UTF-8 (ECP-PRM-006, ECP-PRM-007).

    `ensure_ascii` is explicit because the package's recorded digests were taken with
    it true and the repository tools' with it false; each caller keeps its bytes.
    """

    return (json.dumps(value, ensure_ascii=ensure_ascii, separators=(",", ":"), sort_keys=True) + "\n").encode("utf-8")


def pretty_json_bytes(value: Any, *, ensure_ascii: bool) -> bytes:
    """Sorted keys, two-space indent, one trailing LF, UTF-8: the retained-document form (ECP-PRM-006, ECP-PRM-007)."""

    return (json.dumps(value, ensure_ascii=ensure_ascii, indent=2, sort_keys=True) + "\n").encode("utf-8")


def unique_object_hook(error: Callable[[str], BaseException]) -> Callable[[list[tuple[str, Any]]], dict[str, Any]]:
    """The one duplicate-key hook for `json.loads`; `error(key)` builds the caller's own refusal (ECP-PRM-006)."""

    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, item in pairs:
            if key in result:
                raise error(key)
            result[key] = item
        return result

    return hook


def stage_bytes(path: Path, content: bytes, *, prefix: str | None = None) -> Path:
    """Write `content` to a sibling temporary file of `path`, fsynced, and return it for a later replace (ECP-PRM-008).

    A multi-file transaction stages every file first and replaces them all after; a
    failed stage removes its own temporary file and re-raises.
    """

    descriptor, temporary_name = tempfile.mkstemp(prefix=prefix or f".{path.name}.", dir=path.parent)
    staged = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
    except BaseException:
        staged.unlink(missing_ok=True)
        raise
    return staged


def fsync_directory(path: Path) -> None:
    """Flush directory entries on POSIX; Windows exposes no directory fsync.

    File contents are flushed by the atomic writers on both platforms. This
    additional barrier lets transactions order their journal and file entries
    where the operating system supports it; errors propagate to the caller.
    """

    if os.name == "nt":
        return
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def atomic_write_bytes(path: Path, content: bytes) -> None:
    """Write `content` to a sibling temporary file, fsync it and replace `path` (ECP-PRM-008).

    An interrupted write leaves the target untouched; `OSError` propagates for the
    caller to name in its own words.
    """

    path.parent.mkdir(parents=True, exist_ok=True)
    staged = stage_bytes(path, content)
    try:
        os.replace(staged, path)
    finally:
        staged.unlink(missing_ok=True)


def atomic_create_bytes(
    path: Path,
    content: bytes,
    *,
    exists: Callable[[], BaseException],
    failed: Callable[[str], BaseException],
) -> None:
    """Create `path` exactly once: write a sibling temporary file, fsync it and link it into place (ECP-PRM-008).

    An existing target raises `exists()`; any other link failure raises `failed(detail)`.
    """

    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(temporary_name, path)
        except FileExistsError as exc:
            raise exists() from exc
        except OSError as exc:
            raise failed(str(exc)) from exc
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)


def read_toml(path: Path) -> dict[str, Any]:
    """The one reader of a TOML configuration file, BOM-tolerant; every failure is an `IntegrityError` (ECP-PRM-011)."""

    try:
        value = tomllib.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
        raise IntegrityError(f"cannot read {path.name}: {exc}") from exc
    if not isinstance(value, dict):
        raise IntegrityError(f"{path.name} is not a TOML table")
    return value


def canonical_sha256(value: bytes) -> str:
    """Hash managed text after versioned newline canonicalization."""

    return raw_sha256(canonical_text_bytes(value))


def canonical_text_equal(left: bytes, right: bytes) -> bool:
    return canonical_text_bytes(left) == canonical_text_bytes(right)


_unique_object = unique_object_hook(lambda key: IntegrityError(f"duplicate JSON key: {key}"))


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
            "with harnessctl init"
        )
    if type(schema) is not int or schema not in {LOCK_SCHEMA, 4}:
        raise IntegrityError("unsupported lock schema")
    if schema == LOCK_SCHEMA and "skill_ownership" in value:
        raise IntegrityError("plugin ownership requires lock schema 4")
    if schema == 4:
        from se_harness.skill_ownership import validate_ownership_binding

        validate_ownership_binding(value.get("skill_ownership"))
    if value.get("hash_algorithm") != HASH_ALGORITHM:
        raise IntegrityError("unsupported lock hash algorithm")
    if value.get("hash_mode") != HASH_MODE:
        raise IntegrityError("unsupported lock hash mode")
    evaluator = value.get("evaluator")
    if not isinstance(evaluator, dict):
        raise IntegrityError("supported lock evaluator must be an object")
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
    if schema == 4:
        from se_harness.skill_ownership import catalog_paths

        if set(files) & catalog_paths():
            raise IntegrityError("plugin-owned catalog must not remain in repository lock entries")
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


def compare_lock_entry(entry: dict[str, Any], current: bytes) -> str:
    """Return canonical or mismatch."""

    expected = entry.get("sha256")
    return "canonical" if canonical_sha256(current) == expected else "mismatch"
