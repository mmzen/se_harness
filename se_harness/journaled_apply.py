"""Journaled multi-file apply with rollback and a human-recovery stop.

This is the one property of the Phase 4 effect broker that `ADR-ECP-002` keeps
(`SPEC-ECP-006`, the `ECP-JNL-` rules): a set of file replacements is staged,
recorded in a journal before the first target is touched, applied in journal
order, and either completes as a whole or is rolled back to its pre-images. A
rollback that cannot prove the prior state leaves the journal in
`human-recovery-stop`, and no further apply runs until that journal is
resolved. There is no bundle, envelope, token, receipt or session here: the
caller names the targets and their pre- and post-images, and a journal
directory of its choosing.

Wiring this apply into every harness-owned multi-file write is `REQ-ECP-017`'s
work; this module is the retained code and its fault matrix.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Iterable, Mapping

JOURNAL_SCHEMA = "se-harness-apply-journal-v1"
MAX_JOURNAL_BYTES = 4_194_304
ACTIVE_JOURNAL = "journal.json"
HUMAN_RECOVERY_STOP = "human-recovery-stop"
_TERMINAL = {"committed", "rolled-back", "recovered-prior", "recovered-result", HUMAN_RECOVERY_STOP}
_REPARSE = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)

FaultHook = Callable[[str], None]


class JournaledApplyError(RuntimeError):
    """A stable, bounded apply, rollback or recovery diagnostic."""

    def __init__(self, code: str, message: str, *, uncertain_paths: Iterable[str] = ()) -> None:
        safe = "".join(character if character >= " " else "?" for character in str(message))[:512]
        super().__init__(f"{code}: {safe or 'journaled apply stopped'}")
        self.code = code
        self.message = safe
        self.uncertain_paths = tuple(sorted(set(uncertain_paths)))


@dataclass(frozen=True)
class Target:
    """One file the apply replaces, creates (`before is None`) or deletes (`after is None`)."""

    path: str
    before: bytes | None
    after: bytes | None


@dataclass(frozen=True)
class ApplyResult:
    outcome: str
    transaction_id: str
    journal_path: Path


@dataclass(frozen=True)
class RecoveryResult:
    outcome: str
    transaction_id: str
    journal_path: Path | None
    uncertain_paths: tuple[str, ...] = ()


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _image(content: bytes | None) -> dict[str, Any] | None:
    return None if content is None else {"sha256": _sha256(content), "size": len(content)}


def _timestamp() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _relative(path: str) -> PurePosixPath:
    pure = PurePosixPath(path)
    if (
        not path
        or path != pure.as_posix()
        or pure.is_absolute()
        or "\\" in path
        or any(part in {"", ".", ".."} for part in pure.parts)
        or path.endswith("/")
    ):
        raise JournaledApplyError("JNL001", f"target path is not a normalized relative path: {path!r}")
    return pure


def _target(root: Path, relative: str) -> Path:
    pure = _relative(relative)
    target = root.joinpath(*pure.parts)
    for ancestor in [target, *target.parents]:
        if ancestor == root:
            break
        try:
            info = os.lstat(ancestor)
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or (getattr(info, "st_file_attributes", 0) & _REPARSE):
            raise JournaledApplyError("JNL002", f"target path crosses a link: {relative}")
    return target


def _file_state(path: Path) -> dict[str, Any] | None:
    try:
        info = os.lstat(path)
    except FileNotFoundError:
        return None
    if not stat.S_ISREG(info.st_mode):
        raise JournaledApplyError("JNL002", f"target is not a regular file: {path.name}")
    content = path.read_bytes()
    return {"sha256": _sha256(content), "size": len(content)}


def _matches(actual: dict[str, Any] | None, expected: dict[str, Any] | None) -> bool:
    if actual is None or expected is None:
        return actual is None and expected is None
    return actual["sha256"] == expected["sha256"] and actual["size"] == expected["size"]


def _write_json(path: Path, value: Mapping[str, Any], *, exclusive: bool = False) -> None:
    raw = (json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True) + "\n").encode("utf-8")
    if len(raw) > MAX_JOURNAL_BYTES:
        raise JournaledApplyError("JNL003", "journal exceeds its size bound")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    with os.fdopen(os.open(temporary, flags, 0o600), "wb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    if exclusive and path.exists():
        temporary.unlink()
        raise JournaledApplyError("JNL004", "a journal already exists")
    os.replace(temporary, path)


def _atomic_write(target: Path, content: bytes, transaction_id: str) -> None:
    temporary = target.with_name(f".{target.name}.{transaction_id}.recover")
    with os.fdopen(os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "wb") as stream:
        stream.write(content)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, target)


def read_journal(journal_directory: Path) -> dict[str, Any] | None:
    """Return the active journal, or `None` when no apply is in flight."""

    path = journal_directory / ACTIVE_JOURNAL
    if not path.exists():
        return None
    raw = path.read_bytes()
    if len(raw) > MAX_JOURNAL_BYTES:
        raise JournaledApplyError("JNL003", "journal exceeds its size bound")
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeError, ValueError) as exc:
        raise JournaledApplyError("JNL005", f"journal is not readable: {exc}") from exc
    if not isinstance(value, dict) or value.get("schema") != JOURNAL_SCHEMA:
        raise JournaledApplyError("JNL005", "journal schema is unsupported")
    return value


def _validate_journal(journal: Mapping[str, Any]) -> dict[str, Any]:
    value = dict(journal)
    entries = value.get("entries")
    if (
        not isinstance(value.get("transaction_id"), str)
        or not isinstance(entries, list)
        or any(not isinstance(item, dict) or "path" not in item for item in entries)
    ):
        raise JournaledApplyError("JNL005", "journal entries are malformed")
    digest = value.pop("entries_sha256", None)
    expected = _sha256(json.dumps(entries, sort_keys=True, separators=(",", ":")).encode("utf-8"))
    if digest != expected:
        raise JournaledApplyError("JNL005", "journal checksum differs from its entries")
    value["entries_sha256"] = digest
    return value


def _advance(journal_directory: Path, journal: dict[str, Any], state: str | None = None) -> None:
    if state is not None:
        journal["state"] = state
    journal["updated_at"] = _timestamp()
    _write_json(journal_directory / ACTIVE_JOURNAL, journal)


def _archive(journal_directory: Path, journal: dict[str, Any]) -> Path:
    archived = journal_directory / "archive" / f"{journal['transaction_id']}.json"
    _write_json(archived, journal)
    (journal_directory / ACTIVE_JOURNAL).unlink()
    material = journal_directory / journal["transaction_id"]
    if material.exists():
        shutil.rmtree(material, ignore_errors=True)
    return archived


def _human_stop(journal_directory: Path, journal: dict[str, Any], paths: Iterable[str], reason: str) -> None:
    journal["uncertain_paths"] = sorted(set(paths))
    journal["stop_reason"] = reason[:512]
    _advance(journal_directory, journal, HUMAN_RECOVERY_STOP)


def _rollback(root: Path, journal_directory: Path, journal: dict[str, Any], *, recovered: bool) -> Path:
    backups = journal_directory / journal["transaction_id"] / "backups"
    uncertain: list[str] = []
    try:
        for entry in reversed(journal["entries"]):
            target = _target(root, entry["path"])
            actual = _file_state(target)
            before, after = entry["before"], entry["after"]
            if _matches(actual, before):
                continue
            if not _matches(actual, after):
                uncertain.append(entry["path"])
                continue
            if before is None:
                target.unlink()
            else:
                backup = backups / before["sha256"]
                content = backup.read_bytes()
                if _sha256(content) != before["sha256"] or len(content) != before["size"]:
                    raise JournaledApplyError("JNL014", f"recovery backup differs for {entry['path']}")
                _atomic_write(target, content, journal["transaction_id"])
        for relative in journal.get("temporaries", []):
            temporary = _target(root, relative)
            if temporary.exists():
                temporary.unlink()
        for relative in reversed(journal.get("created_parents", [])):
            parent = root.joinpath(*relative.split("/"))
            if parent.exists() and not any(parent.iterdir()):
                parent.rmdir()
        if uncertain:
            raise JournaledApplyError(
                "JNL014", "current target is neither the planned prior nor result state", uncertain_paths=uncertain
            )
        for entry in journal["entries"]:
            if not _matches(_file_state(_target(root, entry["path"])), entry["before"]):
                raise JournaledApplyError("JNL013", f"rollback did not reproduce the prior state of {entry['path']}")
        journal["applied"] = []
        _advance(journal_directory, journal, "recovered-prior" if recovered else "rolled-back")
        return _archive(journal_directory, journal)
    except Exception as exc:
        paths = uncertain or [item["path"] for item in journal.get("entries", [])]
        try:
            _human_stop(journal_directory, journal, paths, str(exc))
        except Exception:
            pass
        raise JournaledApplyError(
            "WEX-ECP-041",
            f"{'recovery' if recovered else 'rollback'} could not prove prior state; "
            f"journal {journal_directory / ACTIVE_JOURNAL} requires accountable human recovery: {exc}",
            uncertain_paths=paths,
        ) from exc


def apply_journaled(
    repository: Path,
    targets: Iterable[Target],
    *,
    journal_directory: Path,
    transaction_id: str | None = None,
    fault: FaultHook | None = None,
) -> ApplyResult:
    """Replace every target as a whole, or restore every pre-image.

    `fault` is the test hook of the fault matrix: it is called with the name of
    each stage the apply passes, and may raise to simulate a crash there.
    """

    root = repository.resolve(strict=True)
    journal_directory = journal_directory.resolve()
    if journal_directory == root or root in journal_directory.parents:
        pass  # a journal inside the repository is the caller's choice; it is never a target
    selected_fault = fault or (lambda _stage: None)
    planned = list(targets)
    if not planned:
        raise JournaledApplyError("JNL006", "nothing to apply")
    existing = read_journal(journal_directory)
    if existing is not None:
        if existing.get("state") == HUMAN_RECOVERY_STOP:
            raise JournaledApplyError(
                "WEX-ECP-042",
                f"journal {journal_directory / ACTIVE_JOURNAL} is in {HUMAN_RECOVERY_STOP}; resolve it before any write",
                uncertain_paths=existing.get("uncertain_paths", ()),
            )
        raise JournaledApplyError("JNL004", "an apply is already in flight; recover it first")
    seen: set[str] = set()
    entries: list[dict[str, Any]] = []
    contents: dict[str, bytes] = {}
    for target in planned:
        _relative(target.path)
        folded = target.path.casefold()
        if folded in seen:
            raise JournaledApplyError("JNL001", f"duplicate target path: {target.path}")
        seen.add(folded)
        if target.before is None and target.after is None:
            raise JournaledApplyError("JNL006", f"target has neither pre-image nor post-image: {target.path}")
        path = _target(root, target.path)
        if journal_directory == path or journal_directory in path.parents:
            raise JournaledApplyError("JNL001", f"target is inside the journal directory: {target.path}")
        # ECP-JNL-005: every target's current bytes must be the bytes planned against.
        if not _matches(_file_state(path), _image(target.before)):
            raise JournaledApplyError("JNL007", f"target changed since planning: {target.path}")
        entries.append({"path": target.path, "before": _image(target.before), "after": _image(target.after)})
        if target.after is not None:
            contents[target.path] = target.after
    transaction = transaction_id or uuid.uuid4().hex
    created_parents: list[str] = []
    temporaries: dict[str, str] = {}
    for entry in entries:
        if entry["after"] is None:
            continue
        pure = PurePosixPath(entry["path"])
        parent = pure.parent
        while str(parent) != "." and not root.joinpath(*parent.parts).exists():
            if parent.as_posix() not in created_parents:
                created_parents.append(parent.as_posix())
            parent = parent.parent
        temporaries[entry["path"]] = (pure.parent / f".{pure.name}.{transaction}.part").as_posix()
    created_parents.sort(key=lambda item: item.count("/"))
    journal: dict[str, Any] = {
        "schema": JOURNAL_SCHEMA,
        "transaction_id": transaction,
        "state": "prepared",
        "entries": entries,
        "entries_sha256": _sha256(json.dumps(entries, sort_keys=True, separators=(",", ":")).encode("utf-8")),
        "created_parents": created_parents,
        "temporaries": sorted(temporaries.values()),
        "applied": [],
        "uncertain_paths": [],
        "started_at": _timestamp(),
        "updated_at": _timestamp(),
    }
    backups = journal_directory / transaction / "backups"
    backups.mkdir(parents=True, exist_ok=False)
    for target in planned:
        if target.before is not None:
            (backups / _sha256(target.before)).write_bytes(target.before)
    persisted = False
    try:
        selected_fault("before-journal")
        _write_json(journal_directory / ACTIVE_JOURNAL, journal, exclusive=True)
        persisted = True
        selected_fault("after-journal-prepared")
        for relative in created_parents:
            root.joinpath(*relative.split("/")).mkdir()
            selected_fault(f"after-parent:{relative}")
        for entry in entries:
            if entry["after"] is None:
                continue
            temporary = _target(root, temporaries[entry["path"]])
            with os.fdopen(os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "wb") as stream:
                stream.write(contents[entry["path"]])
                stream.flush()
                os.fsync(stream.fileno())
            selected_fault(f"after-temp:{entry['path']}")
        _advance(journal_directory, journal, "applying")
        for entry in entries:
            target = _target(root, entry["path"])
            if not _matches(_file_state(target), entry["before"]):
                raise JournaledApplyError("JNL007", f"target changed before apply: {entry['path']}")
            try:
                if entry["after"] is None:
                    target.unlink()
                else:
                    os.replace(_target(root, temporaries[entry["path"]]), target)
            except OSError as exc:
                raise JournaledApplyError("JNL010", f"target apply failed for {entry['path']}: {exc}") from exc
            if not _matches(_file_state(target), entry["after"]):
                raise JournaledApplyError("JNL010", f"applied target differs: {entry['path']}")
            journal["applied"].append(entry["path"])
            _advance(journal_directory, journal)
            selected_fault(f"after-apply:{entry['path']}")
        selected_fault("before-commit")
        _advance(journal_directory, journal, "committed")
        selected_fault("after-journal-commit")
        journal_path = _archive(journal_directory, journal)
        return ApplyResult("committed", transaction, journal_path)
    except BaseException as exc:
        if not isinstance(exc, Exception):
            raise
        if not persisted:
            shutil.rmtree(journal_directory / transaction, ignore_errors=True)
            if isinstance(exc, JournaledApplyError):
                raise
            raise JournaledApplyError("JNL010", f"apply failed before the journal was written: {exc}") from exc
        if journal.get("state") == "committed":
            raise JournaledApplyError("JNL013", "committed apply requires journal finalization; run recovery") from exc
        _rollback(root, journal_directory, journal, recovered=False)
        if isinstance(exc, JournaledApplyError):
            raise
        raise JournaledApplyError("JNL010", f"apply failed and prior state was restored: {exc}") from exc


def recover_journaled(repository: Path, *, journal_directory: Path) -> RecoveryResult | None:
    """Resolve an active journal to a provable terminal state, or stop for a human."""

    root = repository.resolve(strict=True)
    journal_directory = journal_directory.resolve()
    selected = read_journal(journal_directory)
    if selected is None:
        return None
    journal = _validate_journal(selected)
    transaction = journal["transaction_id"]
    state = journal.get("state")
    if state == HUMAN_RECOVERY_STOP:
        raise JournaledApplyError(
            "WEX-ECP-041",
            f"journal {journal_directory / ACTIVE_JOURNAL} requires accountable human recovery",
            uncertain_paths=journal.get("uncertain_paths", ()),
        )
    if state == "committed":
        for entry in journal["entries"]:
            if not _matches(_file_state(_target(root, entry["path"])), entry["after"]):
                paths = [item["path"] for item in journal["entries"]]
                _human_stop(journal_directory, journal, paths, "committed result differs from live target")
                raise JournaledApplyError(
                    "WEX-ECP-041", "committed journal differs from live target", uncertain_paths=paths
                )
        for relative in journal.get("temporaries", []):
            temporary = _target(root, relative)
            if temporary.exists():
                temporary.unlink()
        path = _archive(journal_directory, journal)
        return RecoveryResult("recovered-result", transaction, path)
    if state in _TERMINAL:
        path = _archive(journal_directory, journal)
        return RecoveryResult(str(state), transaction, path)
    if state not in {"prepared", "applying"}:
        paths = [item["path"] for item in journal["entries"]]
        _human_stop(journal_directory, journal, paths, "unknown journal state")
        raise JournaledApplyError("WEX-ECP-041", "journal state is unknown", uncertain_paths=paths)
    path = _rollback(root, journal_directory, journal, recovered=True)
    return RecoveryResult("recovered-prior", transaction, path)


__all__ = [
    "ACTIVE_JOURNAL",
    "HUMAN_RECOVERY_STOP",
    "JOURNAL_SCHEMA",
    "ApplyResult",
    "JournaledApplyError",
    "RecoveryResult",
    "Target",
    "apply_journaled",
    "read_journal",
    "recover_journaled",
]
