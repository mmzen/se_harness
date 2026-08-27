"""Canonical evaluator-built change bundles and immutable content objects."""

from __future__ import annotations

import hashlib
import os
import re
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from se_harness.agent_contract import (
    AgentContractError,
    canonical_json_bytes,
    parse_json_bytes,
    validate_portable_path,
    validate_sha256,
)


CHANGE_BUNDLE_SCHEMA = "se-harness-change-bundle-v1"
MAX_BUNDLE_BYTES = 1_048_576
MAX_CHANGES = 1_024
MAX_FILE_BYTES = 16 * 1024 * 1024
MAX_TOTAL_AFTER_BYTES = 64 * 1024 * 1024
MAX_SCANNED_FILES = 100_000
_WORK_ORDER = re.compile(r"WO-[A-Z0-9](?:[A-Z0-9-]{0,126}[A-Z0-9])?")
_REPARSE_POINT = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)


class ChangeBundleError(ValueError):
    """One stable, bounded bundle or content-object diagnostic."""

    def __init__(self, code: str, path: str, message: str) -> None:
        safe = "".join(character if character >= " " else "?" for character in str(message))[:512]
        super().__init__(f"{code} {path}: {safe or 'change bundle rejected'}")
        self.code = code
        self.path = path
        self.message = safe


@dataclass(frozen=True)
class ChangeBundle:
    """Validated semantic value plus its canonical bytes and external digest."""

    value: Mapping[str, Any]
    canonical_bytes: bytes
    sha256: str


@dataclass(frozen=True)
class BundleConstruction:
    """Evaluator-owned bundle construction result with immutable object inventory."""

    bundle: ChangeBundle
    object_paths: tuple[Path, ...]
    proposed_paths: tuple[str, ...]
    total_after_bytes: int
    non_effects: tuple[str, ...] = (
        "No target repository path was changed.",
        "The bundle contains proposed bytes and foreign-key digests, not authority.",
    )


def _error(code: str, path: str, message: str) -> None:
    raise ChangeBundleError(code, path, message)


def _object(value: Any, fields: set[str], path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        _error("AEXBND003", path, "value must be an object")
    if set(value) != fields:
        missing = sorted(fields - set(value))
        unknown = sorted(set(value) - fields)
        detail = []
        if missing:
            detail.append("missing " + ", ".join(missing))
        if unknown:
            detail.append("unknown " + ", ".join(unknown))
        _error("AEXBND003", path, "; ".join(detail))
    return value


def _size(value: Any, path: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= MAX_FILE_BYTES:
        _error("AEXBND004", path, f"size must be an integer from 0 through {MAX_FILE_BYTES}")
    return value


def _digest(value: Any, path: str) -> str:
    try:
        return validate_sha256(value)
    except AgentContractError as exc:
        _error("AEXBND005", path, str(exc))


def _portable_path(value: Any, path: str) -> str:
    try:
        return validate_portable_path(value)
    except AgentContractError as exc:
        _error("AEXBND006", path, str(exc))


def _content(value: Any, path: str, *, after: bool) -> dict[str, Any]:
    fields = {"sha256", "size", "object"} if after else {"sha256", "size"}
    selected = _object(value, fields, path)
    digest = _digest(selected["sha256"], f"{path}.sha256")
    result: dict[str, Any] = {
        "sha256": digest,
        "size": _size(selected["size"], f"{path}.size"),
    }
    if after:
        expected = f"objects/{digest}"
        if selected["object"] != expected:
            _error("AEXBND008", f"{path}.object", "object path must be derived from its digest")
        result["object"] = expected
    return result


def validate_change_bundle(value: Any) -> ChangeBundle:
    """Validate and canonicalize one closed change-bundle v1 value."""

    root = _object(value, {"schema", "identity", "changes"}, "$")
    if root["schema"] != CHANGE_BUNDLE_SCHEMA:
        _error("AEXBND003", "$.schema", "unsupported change-bundle schema")
    identity = _object(
        root["identity"],
        {"work_order", "envelope_sha256", "repository_state_before"},
        "$.identity",
    )
    work_order = identity["work_order"]
    if not isinstance(work_order, str) or _WORK_ORDER.fullmatch(work_order) is None:
        _error("AEXBND005", "$.identity.work_order", "work-order identity is invalid")
    changes = root["changes"]
    if not isinstance(changes, list) or not 1 <= len(changes) <= MAX_CHANGES:
        _error("AEXBND004", "$.changes", f"changes must contain 1 through {MAX_CHANGES} entries")
    normalized: list[dict[str, Any]] = []
    total_after = 0
    seen: set[str] = set()
    folded: dict[str, str] = {}
    for index, item in enumerate(changes):
        path = f"$.changes[{index}]"
        entry = _object(item, {"operation", "path", "before", "after"}, path)
        operation = entry["operation"]
        if operation not in {"create", "replace", "delete"}:
            _error("AEXBND007", f"{path}.operation", "operation must be create, replace, or delete")
        portable = _portable_path(entry["path"], f"{path}.path")
        if portable in seen:
            _error("AEXBND006", f"{path}.path", "duplicate change path")
        prior = folded.get(portable.casefold())
        if prior is not None and prior != portable:
            _error("AEXBND006", f"{path}.path", "case-folded path collision")
        seen.add(portable)
        folded[portable.casefold()] = portable
        before = None if entry["before"] is None else _content(entry["before"], f"{path}.before", after=False)
        after_value = None if entry["after"] is None else _content(entry["after"], f"{path}.after", after=True)
        if operation == "create" and (before is not None or after_value is None):
            _error("AEXBND007", path, "create requires null before and non-null after")
        if operation == "replace" and (before is None or after_value is None):
            _error("AEXBND007", path, "replace requires non-null before and after")
        if operation == "delete" and (before is None or after_value is not None):
            _error("AEXBND007", path, "delete requires non-null before and null after")
        if after_value is not None:
            total_after += after_value["size"]
            if total_after > MAX_TOTAL_AFTER_BYTES:
                _error("AEXBND004", "$.changes", "total after-content exceeds 64 MiB")
        normalized.append(
            {
                "operation": operation,
                "path": portable,
                "before": before,
                "after": after_value,
            }
        )
    expected_order = sorted((item["path"] for item in normalized), key=lambda item: item.encode("utf-8"))
    if [item["path"] for item in normalized] != expected_order:
        _error("AEXBND002", "$.changes", "changes are not in canonical UTF-8 path order")
    result = {
        "schema": CHANGE_BUNDLE_SCHEMA,
        "identity": {
            "work_order": work_order,
            "envelope_sha256": _digest(identity["envelope_sha256"], "$.identity.envelope_sha256"),
            "repository_state_before": _digest(
                identity["repository_state_before"], "$.identity.repository_state_before"
            ),
        },
        "changes": normalized,
    }
    try:
        raw = canonical_json_bytes(result)
    except AgentContractError as exc:
        if exc.code == "AEXCON002":
            _error("AEXBND004", "$", "canonical bundle exceeds its document bound")
        _error("AEXBND001", "$", str(exc))
    if len(raw) > MAX_BUNDLE_BYTES:
        _error("AEXBND004", "$", "canonical bundle exceeds its document bound")
    return ChangeBundle(result, raw, hashlib.sha256(raw).hexdigest())


def parse_change_bundle_bytes(raw: bytes) -> ChangeBundle:
    """Parse duplicate-safe bytes and require exact canonical representation."""

    if not isinstance(raw, bytes) or len(raw) > MAX_BUNDLE_BYTES:
        _error("AEXBND004", "$", "bundle bytes exceed their document bound")
    try:
        value = parse_json_bytes(raw)
    except AgentContractError as exc:
        _error("AEXBND001", "$", str(exc))
    document = validate_change_bundle(value)
    if document.canonical_bytes != raw:
        _error("AEXBND002", "$", "bundle bytes are not canonical JSON")
    return document


def _normal_file(path: Path, *, label: str, maximum: int | None = None) -> os.stat_result:
    try:
        metadata = path.lstat()
    except OSError as exc:
        _error("AEXBND008", label, f"cannot inspect regular file: {exc}")
    attributes = getattr(metadata, "st_file_attributes", 0)
    if stat.S_ISLNK(metadata.st_mode) or (_REPARSE_POINT and attributes & _REPARSE_POINT):
        _error("AEXBND008", label, "link or reparse object is prohibited")
    if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
        _error("AEXBND008", label, "only unaliased regular files are supported")
    if maximum is not None and metadata.st_size > maximum:
        _error("AEXBND004", label, "file exceeds its byte bound")
    return metadata


def _normal_directory(path: Path, *, label: str) -> Path:
    try:
        metadata = path.lstat()
    except OSError as exc:
        _error("AEXBND008", label, f"cannot inspect directory: {exc}")
    attributes = getattr(metadata, "st_file_attributes", 0)
    if (
        stat.S_ISLNK(metadata.st_mode)
        or (_REPARSE_POINT and attributes & _REPARSE_POINT)
        or not stat.S_ISDIR(metadata.st_mode)
    ):
        _error("AEXBND008", label, "directory link, reparse point, or alias is prohibited")
    return path.resolve(strict=True)


def _read_file(path: Path, *, label: str, maximum: int) -> tuple[bytes, str]:
    before = _normal_file(path, label=label, maximum=maximum)
    descriptor: int | None = None
    try:
        flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(path, flags)
        opened = os.fstat(descriptor)
        if (
            opened.st_dev,
            opened.st_ino,
            opened.st_mode,
            opened.st_nlink,
            opened.st_size,
        ) != (
            before.st_dev,
            before.st_ino,
            before.st_mode,
            before.st_nlink,
            before.st_size,
        ):
            _error("AEXBND008", label, "file identity changed before it was read")
        with os.fdopen(descriptor, "rb", closefd=True) as stream:
            descriptor = None
            content = stream.read(maximum + 1)
        if len(content) > maximum:
            _error("AEXBND004", label, "file exceeds its byte bound")
        after = path.lstat()
    except OSError as exc:
        _error("AEXBND008", label, f"cannot read regular file: {exc}")
    finally:
        if descriptor is not None:
            os.close(descriptor)
    if (before.st_dev, before.st_size, before.st_mtime_ns, before.st_mode, before.st_ino) != (
        after.st_dev,
        after.st_size,
        after.st_mtime_ns,
        after.st_mode,
        after.st_ino,
    ):
        _error("AEXBND008", label, "file changed while it was read")
    return content, hashlib.sha256(content).hexdigest()


def read_content_object(object_store: Path, digest: str, size: int) -> bytes:
    """Read and independently verify one immutable digest-addressed object."""

    selected = _digest(digest, "$.object.sha256")
    expected_size = _size(size, "$.object.size")
    root = _normal_directory(object_store.absolute(), label="$.objects")
    objects = _normal_directory(root / "objects", label="$.objects")
    path = objects / selected
    content, actual = _read_file(path, label="$.object", maximum=MAX_FILE_BYTES)
    if len(content) != expected_size or actual != selected:
        _error("AEXBND008", "$.object", "content object digest or size differs")
    return content


def _store_object(object_store: Path, content: bytes, digest: str) -> Path:
    try:
        supplied = object_store.absolute()
        supplied.mkdir(parents=True, exist_ok=True)
        root = _normal_directory(supplied, label="$.objects")
        objects = root / "objects"
        objects.mkdir(mode=0o700, exist_ok=True)
        _normal_directory(objects, label="$.objects")
        target = objects / digest
        if target.exists():
            existing, actual = _read_file(target, label="$.objects", maximum=MAX_FILE_BYTES)
            if actual != digest or existing != content:
                _error("AEXBND008", "$.objects", "preexisting object does not match its digest")
            return target
        descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o400)
        try:
            with os.fdopen(descriptor, "wb", closefd=True) as stream:
                descriptor = -1
                stream.write(content)
                stream.flush()
                os.fsync(stream.fileno())
            if os.name != "nt":
                target.chmod(0o400)
        finally:
            if descriptor >= 0:
                os.close(descriptor)
        return target
    except ChangeBundleError:
        raise
    except OSError as exc:
        if 'target' in locals() and target.exists():
            try:
                target.unlink()
            except OSError:
                pass
        _error("AEXBND008", "$.objects", f"cannot materialize immutable object: {exc}")


def _scan_workspace(root: Path) -> dict[str, tuple[Path, int, str]]:
    selected = _normal_directory(root.absolute(), label="$.workspace")
    result: dict[str, tuple[Path, int, str]] = {}
    for current, directories, files in os.walk(selected, topdown=True, followlinks=False):
        current_path = Path(current)
        for name in tuple(directories):
            candidate = current_path / name
            metadata = candidate.lstat()
            attributes = getattr(metadata, "st_file_attributes", 0)
            if stat.S_ISLNK(metadata.st_mode) or (_REPARSE_POINT and attributes & _REPARSE_POINT):
                _error("AEXBND008", "$.workspace", "workspace link or reparse directory is prohibited")
        for name in files:
            candidate = current_path / name
            relative = _portable_path(candidate.relative_to(selected).as_posix(), "$.workspace.path")
            metadata = _normal_file(candidate, label=relative)
            if len(result) >= MAX_SCANNED_FILES:
                _error("AEXBND004", "$.workspace", "workspace file count exceeds its bound")
            _, digest = _read_file(candidate, label=relative, maximum=MAX_FILE_BYTES)
            result[relative] = (candidate, metadata.st_size, digest)
    folded: dict[str, str] = {}
    for path in result:
        prior = folded.get(path.casefold())
        if prior is not None and prior != path:
            _error("AEXBND006", "$.workspace", "case-folded workspace path collision")
        folded[path.casefold()] = path
    return result


def construct_change_bundle(
    *,
    baseline_workspace: Path,
    proposed_workspace: Path,
    object_store: Path,
    work_order: str,
    envelope_sha256: str,
    repository_state_before: str,
    intended_deletions: Iterable[str] = (),
) -> BundleConstruction:
    """Construct a bundle from an evaluator-owned isolated workspace delta."""

    baseline = _scan_workspace(baseline_workspace)
    proposed = _scan_workspace(proposed_workspace)
    requested_deletions = tuple(intended_deletions)
    deletions = tuple(
        sorted(
            {_portable_path(item, "$.intended_deletions") for item in requested_deletions},
            key=lambda item: item.encode("utf-8"),
        )
    )
    if len(deletions) != len(requested_deletions):
        _error("AEXBND006", "$.intended_deletions", "intended deletions contain duplicates")
    deletion_set = set(deletions)
    for path in deletion_set:
        if path not in baseline or path in proposed:
            _error("AEXBND007", "$.intended_deletions", "deletion must name an existing removed baseline file")
    missing = set(baseline) - set(proposed)
    if missing != deletion_set:
        _error("AEXBND007", "$.intended_deletions", "every removed file must be explicitly intended")
    entries: list[dict[str, Any]] = []
    objects: dict[str, Path] = {}
    for path in sorted(set(baseline) | set(proposed), key=lambda item: item.encode("utf-8")):
        before = baseline.get(path)
        after = proposed.get(path)
        if before is not None and after is not None and before[1:] == after[1:]:
            continue
        if before is None:
            operation = "create"
        elif after is None:
            operation = "delete"
        else:
            operation = "replace"
        before_value = None if before is None else {"sha256": before[2], "size": before[1]}
        after_value = None
        if after is not None:
            if after[1] > MAX_FILE_BYTES:
                _error("AEXBND004", path, "changed file exceeds 16 MiB")
            content, digest = _read_file(after[0], label=path, maximum=MAX_FILE_BYTES)
            if digest != after[2]:
                _error("AEXBND008", path, "proposed file changed during bundle construction")
            objects.setdefault(digest, _store_object(object_store, content, digest))
            after_value = {"sha256": digest, "size": len(content), "object": f"objects/{digest}"}
        entries.append(
            {"operation": operation, "path": path, "before": before_value, "after": after_value}
        )
    document = validate_change_bundle(
        {
            "schema": CHANGE_BUNDLE_SCHEMA,
            "identity": {
                "work_order": work_order,
                "envelope_sha256": envelope_sha256,
                "repository_state_before": repository_state_before,
            },
            "changes": entries,
        }
    )
    return BundleConstruction(
        document,
        tuple(objects[key] for key in sorted(objects)),
        tuple(item["path"] for item in document.value["changes"]),
        sum(item["after"]["size"] for item in document.value["changes"] if item["after"] is not None),
    )


__all__ = [
    "CHANGE_BUNDLE_SCHEMA",
    "MAX_CHANGES",
    "MAX_FILE_BYTES",
    "MAX_TOTAL_AFTER_BYTES",
    "BundleConstruction",
    "ChangeBundle",
    "ChangeBundleError",
    "construct_change_bundle",
    "parse_change_bundle_bytes",
    "read_content_object",
    "validate_change_bundle",
]
