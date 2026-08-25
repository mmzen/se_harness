"""Canonical, read-only observation of a live Git repository.

The observer does not write to the target, execute a shell, follow links, or
infer authority. Callers require two identical captures before derivation and
a fresh capture immediately before any future effect.
"""

from __future__ import annotations

import hashlib
import os
import stat
import subprocess
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from se_harness.agent_contract import (
    REPOSITORY_OBSERVATION_SCHEMA,
    ContractDocument,
    canonical_sha256,
    validate_contract,
)
from se_harness.preflight import _load_validator_module
from se_harness.workflow_compliance import formal_snapshot_digest


MAX_GIT_OUTPUT_BYTES = 67_108_864
MAX_OBSERVED_FILE_BYTES = 8_589_934_592
MAX_OBSERVED_FILES = 100_000
_WINDOWS_RESERVED = {
    "con",
    "prn",
    "aux",
    "nul",
    *(f"com{index}" for index in range(1, 10)),
    *(f"lpt{index}" for index in range(1, 10)),
}


class RepositoryObservationError(RuntimeError):
    """A stable, fail-closed live-observation failure."""

    def __init__(self, code: str, message: str) -> None:
        text = "".join(character if character >= " " else "?" for character in str(message))[:512]
        super().__init__(f"{code}: {text or 'repository observation failed'}")
        self.code = code
        self.message = text


@dataclass(frozen=True)
class EvaluatorIdentity:
    package: str
    version: str
    payload_sha256: str
    launcher_sha256: str

    def as_dict(self) -> dict[str, str]:
        return {
            "package": self.package,
            "version": self.version,
            "payload_sha256": self.payload_sha256,
            "launcher_sha256": self.launcher_sha256,
        }


@dataclass(frozen=True)
class StableRepositoryObservation:
    document: ContractDocument
    captures: int
    clean: bool
    non_effects: tuple[str, ...] = (
        "No target repository or external runtime state was mutated.",
        "No authority was derived and no operation was admitted or invoked.",
    )


def _digest_file(path: Path) -> tuple[int, str]:
    try:
        before = path.lstat()
    except OSError as exc:
        raise RepositoryObservationError("AEXOBS001", f"cannot stat {path.name}: {exc}") from exc
    reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    attributes = getattr(before, "st_file_attributes", 0)
    if stat.S_ISLNK(before.st_mode) or (reparse and attributes & reparse):
        raise RepositoryObservationError("AEXOBS002", f"link or reparse object is unsupported: {path.name}")
    if not stat.S_ISREG(before.st_mode):
        raise RepositoryObservationError(
            "AEXOBS002", f"non-regular filesystem object is unsupported: {path.name}"
        )
    if before.st_size > MAX_OBSERVED_FILE_BYTES:
        raise RepositoryObservationError("AEXOBS003", f"file exceeds observation bound: {path.name}")
    digest = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
        after = path.lstat()
    except OSError as exc:
        raise RepositoryObservationError("AEXOBS001", f"cannot read {path.name}: {exc}") from exc
    if (before.st_size, before.st_mtime_ns, before.st_mode) != (
        after.st_size,
        after.st_mtime_ns,
        after.st_mode,
    ):
        raise RepositoryObservationError("AEXOBS004", f"file changed during observation: {path.name}")
    return before.st_size, digest.hexdigest()


def _required_digest(root: Path, relative: str) -> str:
    candidate = root / Path(relative)
    _reject_link_components(root, candidate, relative)
    try:
        candidate.resolve(strict=True).relative_to(root)
    except (OSError, ValueError) as exc:
        raise RepositoryObservationError(
            "AEXOBS005", f"required governance file is unsafe: {relative}"
        ) from exc
    return _digest_file(candidate)[1]


def _reject_link_components(root: Path, candidate: Path, relative: str) -> None:
    probe = root
    reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    for part in Path(relative).parts:
        probe /= part
        try:
            details = probe.lstat()
        except OSError as exc:
            raise RepositoryObservationError(
                "AEXOBS001", f"cannot stat listed path: {relative}"
            ) from exc
        attributes = getattr(details, "st_file_attributes", 0)
        if stat.S_ISLNK(details.st_mode) or (reparse and attributes & reparse):
            raise RepositoryObservationError(
                "AEXOBS002", f"path traverses a link or reparse object: {relative}"
            )
    if probe != candidate:
        raise RepositoryObservationError("AEXOBS005", "listed path identity is ambiguous")


def _validate_git_path(path: str, label: str) -> None:
    if (
        not path
        or len(path.encode("utf-8")) > 1_024
        or unicodedata.normalize("NFC", path) != path
        or "\\" in path
        or ":" in path
        or "*" in path
        or "?" in path
        or path.startswith("/")
        or any(ord(character) < 32 or ord(character) == 127 for character in path)
    ):
        raise RepositoryObservationError("AEXOBS007", f"{label} contains an unsafe path")
    for part in path.split("/"):
        if (
            not part
            or part in {".", ".."}
            or part.endswith((".", " "))
            or part.split(".", 1)[0].casefold() in _WINDOWS_RESERVED
        ):
            raise RepositoryObservationError("AEXOBS007", f"{label} contains an unsafe path")


def _git(root: Path, *arguments: str, allow_failure: bool = False) -> bytes | None:
    try:
        process = subprocess.run(
            ["git", "-C", os.fspath(root), *arguments],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise RepositoryObservationError("AEXOBS006", f"Git observation failed: {exc}") from exc
    if len(process.stdout) > MAX_GIT_OUTPUT_BYTES or len(process.stderr) > 65_536:
        raise RepositoryObservationError("AEXOBS003", "Git observation output exceeds its bound")
    if process.returncode != 0:
        if allow_failure:
            return None
        detail = process.stderr.decode("utf-8", errors="replace").strip()
        raise RepositoryObservationError("AEXOBS006", detail or "Git command failed")
    return process.stdout


def _decode_z_paths(raw: bytes, label: str) -> tuple[str, ...]:
    items = raw.split(b"\0")
    if items[-1:] == [b""]:
        items.pop()
    if len(items) > MAX_OBSERVED_FILES:
        raise RepositoryObservationError("AEXOBS003", f"{label} exceeds the file-count bound")
    try:
        paths = tuple(item.decode("utf-8") for item in items)
    except UnicodeDecodeError as exc:
        raise RepositoryObservationError("AEXOBS007", f"{label} contains a non-UTF-8 path") from exc
    if len(paths) != len(set(paths)):
        raise RepositoryObservationError("AEXOBS007", f"{label} contains duplicate paths")
    folded: dict[str, str] = {}
    for path in paths:
        _validate_git_path(path, label)
        prior = folded.setdefault(path.casefold(), path)
        if prior != path:
            raise RepositoryObservationError("AEXOBS007", f"{label} contains a case-folded collision")
    return tuple(sorted(paths, key=lambda item: item.encode("utf-8")))


def _index_entries(raw: bytes) -> tuple[list[dict[str, str]], bool, bool]:
    entries: list[dict[str, str]] = []
    conflicts = False
    submodules = False
    records = raw.split(b"\0")
    if records[-1:] == [b""]:
        records.pop()
    if len(records) > MAX_OBSERVED_FILES:
        raise RepositoryObservationError("AEXOBS003", "Git index exceeds the entry-count bound")
    for record in records:
        try:
            prefix, encoded_path = record.split(b"\t", 1)
            mode, object_id, stage = prefix.decode("ascii").split(" ")
            path = encoded_path.decode("utf-8")
        except (ValueError, UnicodeDecodeError) as exc:
            raise RepositoryObservationError("AEXOBS007", "Git index contains an invalid record") from exc
        _validate_git_path(path, "Git index")
        conflicts = conflicts or stage != "0"
        submodules = submodules or mode == "160000"
        entries.append({"mode": mode, "object_id": object_id, "path": path, "stage": stage})
    entries.sort(key=lambda item: (item["path"].encode("utf-8"), item["stage"]))
    return entries, conflicts, submodules


def _file_manifest(
    root: Path, paths: Iterable[str], *, missing_allowed: bool
) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    root_resolved = root.resolve(strict=True)
    for relative in paths:
        candidate = root / Path(*relative.split("/"))
        if not candidate.exists() and not candidate.is_symlink():
            if missing_allowed:
                entries.append({"kind": "absent", "path": relative})
                continue
            raise RepositoryObservationError("AEXOBS001", f"listed file is absent: {relative}")
        _reject_link_components(root, candidate, relative)
        try:
            candidate.resolve(strict=True).relative_to(root_resolved)
        except (OSError, ValueError) as exc:
            raise RepositoryObservationError(
                "AEXOBS005", f"listed path escapes the repository: {relative}"
            ) from exc
        size, digest = _digest_file(candidate)
        entries.append({"kind": "regular", "path": relative, "sha256": digest, "size": size})
    return entries


def _formal_state(root: Path, work_order_id: str) -> tuple[str, bytes, str]:
    validator = _load_validator_module()
    artifacts, parse_errors = validator.load_artifacts(root / "docs" / "engineering", root)
    if parse_errors:
        raise RepositoryObservationError("AEXOBS008", "formal artifacts contain parse errors")
    selected = [item for item in artifacts if item.artifact_id == work_order_id]
    if len(selected) != 1 or selected[0].artifact_type != "work_order":
        raise RepositoryObservationError("AEXOBS008", "selected work order is missing or ambiguous")
    work_order = selected[0]
    try:
        raw = work_order.path.read_bytes()
    except OSError as exc:
        raise RepositoryObservationError("AEXOBS001", f"cannot read selected work order: {exc}") from exc
    return formal_snapshot_digest(root, artifacts), raw, work_order.status


def observe_repository(
    repository: Path,
    *,
    work_order_id: str,
    evaluator: EvaluatorIdentity,
    previous_receipt_sha256: str | None = None,
) -> ContractDocument:
    """Capture one canonical repository observation without mutating the target."""

    try:
        requested = repository.absolute()
        root = repository.resolve(strict=True)
    except OSError as exc:
        raise RepositoryObservationError("AEXOBS001", f"repository is unavailable: {exc}") from exc
    if os.path.normcase(os.fspath(requested)) != os.path.normcase(os.fspath(root)):
        raise RepositoryObservationError("AEXOBS005", "repository root has an aliased identity")
    top_raw = _git(root, "rev-parse", "--show-toplevel")
    assert top_raw is not None
    try:
        top = Path(top_raw.decode("utf-8").strip()).resolve(strict=True)
    except (UnicodeDecodeError, OSError) as exc:
        raise RepositoryObservationError("AEXOBS006", "Git returned an invalid repository root") from exc
    if top != root:
        raise RepositoryObservationError(
            "AEXOBS005", "repository argument must name the exact Git worktree root"
        )

    object_format_raw = _git(root, "rev-parse", "--show-object-format")
    assert object_format_raw is not None
    object_format = object_format_raw.decode("ascii", errors="strict").strip()
    head_raw = _git(root, "rev-parse", "--verify", "HEAD", allow_failure=True)
    symbolic_raw = _git(root, "symbolic-ref", "-q", "HEAD", allow_failure=True)
    index_raw = _git(root, "ls-files", "--stage", "-z")
    tracked_raw = _git(root, "ls-files", "-z")
    untracked_raw = _git(root, "ls-files", "--others", "--exclude-standard", "-z")
    assert index_raw is not None and tracked_raw is not None and untracked_raw is not None
    index_entries, conflicts, submodules = _index_entries(index_raw)
    if conflicts:
        raise RepositoryObservationError("AEXOBS009", "Git index conflicts are unsupported")
    if submodules:
        raise RepositoryObservationError("AEXOBS009", "Git submodules are unsupported")
    tracked_paths = _decode_z_paths(tracked_raw, "tracked worktree")
    untracked_paths = _decode_z_paths(untracked_raw, "untracked worktree")
    combined = tuple(
        sorted(set(tracked_paths) | set(untracked_paths), key=lambda item: item.encode("utf-8"))
    )
    if len(combined) > MAX_OBSERVED_FILES:
        raise RepositoryObservationError("AEXOBS003", "regular-file manifest exceeds its bound")
    tracked_manifest = _file_manifest(root, tracked_paths, missing_allowed=True)
    untracked_manifest = _file_manifest(root, untracked_paths, missing_allowed=False)
    regular_manifest = [
        item
        for item in _file_manifest(root, combined, missing_allowed=True)
        if item["kind"] == "regular"
    ]
    formal_sha256, work_order_raw, status = _formal_state(root, work_order_id)

    observation = {
        "schema": REPOSITORY_OBSERVATION_SCHEMA,
        "repository": hashlib.sha256(
            os.fsencode(os.path.normcase(os.fspath(root)))
        ).hexdigest(),
        "evaluator": evaluator.as_dict(),
        "git": {
            "object_format": object_format,
            "head": None if head_raw is None else head_raw.decode("ascii").strip(),
            "symbolic_ref": (
                None if symbolic_raw is None else symbolic_raw.decode("utf-8").strip()
            ),
            "index_entries_sha256": canonical_sha256(index_entries),
            "tracked_worktree_sha256": canonical_sha256(tracked_manifest),
            "untracked_nonignored_sha256": canonical_sha256(untracked_manifest),
            "conflicts": False,
            "submodules": False,
        },
        "governance": {
            "managed_lock_sha256": _required_digest(root, ".engineering-harness.lock"),
            "formal_snapshot_sha256": formal_sha256,
            "workflow_contract_sha256": _required_digest(
                root, "docs/engineering/WORKFLOW.json"
            ),
            "decision_rights_sha256": _required_digest(
                root, "docs/engineering/DECISION_RIGHTS.md"
            ),
            "work_order": work_order_id,
            "work_order_sha256": hashlib.sha256(work_order_raw).hexdigest(),
            "work_order_status": status,
        },
        "filesystem": {
            "platform_family": "windows" if os.name == "nt" else "posix",
            "case_sensitive": os.path.normcase("A") != os.path.normcase("a"),
            "regular_file_manifest_sha256": canonical_sha256(regular_manifest),
            "unsupported_object_count": 0,
        },
        "previous_receipt_sha256": previous_receipt_sha256,
    }
    return validate_contract(
        observation, expected_schema=REPOSITORY_OBSERVATION_SCHEMA
    )


def observe_stable_repository(
    repository: Path,
    *,
    work_order_id: str,
    evaluator: EvaluatorIdentity,
    previous_receipt_sha256: str | None = None,
    max_captures: int = 3,
) -> StableRepositoryObservation:
    """Require two consecutive byte-identical observations."""

    if max_captures < 2 or max_captures > 10:
        raise RepositoryObservationError(
            "AEXOBS003", "max_captures must be between 2 and 10"
        )
    prior: ContractDocument | None = None
    prior_clean: bool | None = None
    for capture in range(1, max_captures + 1):
        current = observe_repository(
            repository,
            work_order_id=work_order_id,
            evaluator=evaluator,
            previous_receipt_sha256=previous_receipt_sha256,
        )
        status = _git(
            repository.resolve(strict=True),
            "status",
            "--porcelain=v1",
            "-z",
            "--untracked-files=all",
            "--ignore-submodules=none",
        )
        assert status is not None
        clean = status == b""
        if (
            prior is not None
            and prior.canonical_bytes == current.canonical_bytes
            and prior_clean == clean
        ):
            return StableRepositoryObservation(current, capture, clean)
        prior = current
        prior_clean = clean
    raise RepositoryObservationError(
        "AEXOBS004", "repository did not stabilize across consecutive captures"
    )


def require_fresh_observation(
    expected_sha256: str, current: ContractDocument
) -> ContractDocument:
    """Fail closed unless a fresh validated observation has the expected identity."""

    document = validate_contract(
        current.value, expected_schema=REPOSITORY_OBSERVATION_SCHEMA
    )
    if document.sha256 != expected_sha256:
        raise RepositoryObservationError(
            "AEXOBS010", "fresh repository state differs from the envelope"
        )
    return document


__all__ = [
    "EvaluatorIdentity",
    "RepositoryObservationError",
    "StableRepositoryObservation",
    "observe_repository",
    "observe_stable_repository",
    "require_fresh_observation",
]
