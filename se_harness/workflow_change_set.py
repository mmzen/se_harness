"""The change-set seam of the checkpoint evaluation (SPEC-ECP-024 ECP-ENG-019): path normalisation, the declared and Git-derived change sets, the execution scope and the formal snapshot digest.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping

from se_harness._process import run_git, text as _text
from se_harness.codes import CodedError, WEX200, WEX_ECP_003
from se_harness.installer import HarnessError, safe_destination
from se_harness.integrity import unique_object_hook


CHANGE_SET_SCHEMA = "se-harness-change-set-v1"

_CONTROL = re.compile(r"[\x00-\x1f\x7f]")

_RESERVED = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{index}" for index in range(1, 10)),
    *(f"LPT{index}" for index in range(1, 10)),
}


@dataclass(frozen=True)
class ChangeSet:
    paths: tuple[str, ...]
    complete: bool
    source: str
    #: The members that are new files, known only when Git derived the set (RSK-MGT-027).
    added: tuple[str, ...] = ()


_pairs = unique_object_hook(lambda key: CodedError(WEX200, f"duplicate JSON key in change manifest: {key}"))


def normalize_path(value: object, *, directory_allowed: bool = False) -> str:
    if not isinstance(value, str) or not value or len(value) > 4096:
        raise CodedError(WEX200, "path must be non-empty UTF-8 text of at most 4096 characters")
    if _CONTROL.search(value) or "\\" in value or ":" in value or any(token in value for token in ("*", "?", "[", "]")):
        raise CodedError(WEX200, f"path is not a normalized repository path: {value!r}")
    directory = value.endswith("/")
    if directory and not directory_allowed:
        raise CodedError(WEX200, f"changed path must name a file or component: {value!r}")
    candidate = value[:-1] if directory else value
    if not candidate or candidate.startswith("/") or candidate.startswith("//"):
        raise CodedError(WEX200, f"absolute or empty path is forbidden: {value!r}")
    parts = PurePosixPath(candidate).parts
    if not parts or any(part in {"", ".", ".."} for part in parts):
        raise CodedError(WEX200, f"dot or empty path component is forbidden: {value!r}")
    for part in parts:
        stem = part.rstrip(". ").split(".", 1)[0].upper()
        if stem in _RESERVED or part.endswith((".", " ")):
            raise CodedError(WEX200, f"reserved path component is forbidden: {value!r}")
    normalized = PurePosixPath(*parts).as_posix() + ("/" if directory else "")
    if normalized != value:
        raise CodedError(WEX200, f"path is not normalized: {value!r}")
    return normalized


def _unique_paths(values: Iterable[object], *, directory_allowed: bool) -> tuple[str, ...]:
    result: list[str] = []
    folded: dict[str, str] = {}
    for value in values:
        path = normalize_path(value, directory_allowed=directory_allowed)
        key = path.casefold()
        if key in folded:
            raise CodedError(WEX200, f"duplicate or case-ambiguous path: {path!r}")
        folded[key] = path
        result.append(path)
    return tuple(result)


def parse_change_manifest(root: Path, manifest: Path) -> ChangeSet:
    raw = manifest.as_posix()
    if manifest.is_absolute():
        try:
            candidate = manifest.resolve(strict=True)
            candidate.relative_to(root)
        except (OSError, ValueError) as exc:
            raise CodedError(WEX200, "change manifest must remain inside the repository") from exc
    else:
        normalized = normalize_path(raw)
        candidate = safe_destination(root, Path(normalized))
        try:
            candidate = candidate.resolve(strict=True)
            candidate.relative_to(root)
        except (OSError, ValueError) as exc:
            raise CodedError(WEX200, "change manifest cannot resolve safely") from exc
    if candidate.is_symlink() or not candidate.is_file():
        raise CodedError(WEX200, "change manifest must be one ordinary file")
    try:
        data = candidate.read_bytes()
        if len(data) > 10_000_000:
            raise CodedError(WEX200, "change manifest exceeds 10 MB")
        value = json.loads(data.decode("utf-8"), object_pairs_hook=_pairs)
    except HarnessError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise CodedError(WEX200, f"invalid change manifest: {exc}") from exc
    if not isinstance(value, dict) or set(value) != {"schema", "complete", "paths"}:
        raise CodedError(WEX200, "change manifest fields must be schema, complete, and paths")
    if value.get("schema") != CHANGE_SET_SCHEMA or not isinstance(value.get("complete"), bool):
        raise CodedError(WEX200, "change manifest schema or completeness value is invalid")
    if not isinstance(value.get("paths"), list):
        raise CodedError(WEX200, "change manifest paths must be an array")
    return ChangeSet(
        paths=_unique_paths(value["paths"], directory_allowed=False),
        complete=value["complete"],
        source=candidate.relative_to(root).as_posix(),
    )


def declared_change_set(paths: Iterable[str], *, complete: bool) -> ChangeSet:
    return ChangeSet(
        paths=_unique_paths(paths, directory_allowed=False),
        complete=bool(complete),
        source="arguments",
    )


def _git_lines(root: Path, arguments: list[str], *, base: str) -> list[str]:
    # ECP-PRM-003: the one launcher.
    completed = run_git(
        root, *arguments, timeout=120,
        error=lambda message: CodedError(WEX_ECP_003, f"git is unavailable for base {base!r}: {message}"),
    )
    if completed.returncode != 0:
        detail = _text(completed.stderr).strip().splitlines()
        raise CodedError(WEX_ECP_003, f"git {arguments[0]} failed for base {base!r} with exit status {completed.returncode}"
            + (f": {detail[0]}" if detail else "")
        )
    return [item.decode("utf-8") for item in completed.stdout.split(b"\0") if item]


def git_change_set(root: Path, base: str) -> ChangeSet:
    """Derive the change set from Git (ECP-CHG-002 to -004).

    The set is the union of `git diff --name-only BASE` against the working
    tree, renames contributing both names, and the untracked files Git does not
    ignore; every member passes `normalize_path`, and any Git failure blocks
    with `WEX-ECP-003` so no predicate is evaluated as `pass`.
    """

    if not isinstance(base, str) or not base.strip() or base.startswith("-"):
        raise CodedError(WEX_ECP_003, f"the Git base must be a revision, not {base!r}")
    if not (root / ".git").exists():
        raise CodedError(WEX_ECP_003, f"{root} is not a Git checkout; --from-git needs one")
    _git_lines(root, ["rev-parse", "--verify", "--quiet", f"{base}^{{commit}}"], base=base)
    # `-z --name-status` alternates one status letter and one path; an `A` names a
    # file absent from the base (SPEC-RSK-010 RSK-MGT-027 reads that fact).
    status = _git_lines(root, ["diff", "-z", "--name-status", "--no-renames", base, "--"], base=base)
    changed = list(status[1::2])
    new = {item for letter, item in zip(status[0::2], status[1::2]) if letter.startswith("A")}
    untracked = _git_lines(root, ["ls-files", "-z", "--others", "--exclude-standard"], base=base)
    new.update(untracked)
    ordered: list[str] = []
    for item in [*changed, *untracked]:
        if item not in ordered:
            ordered.append(item)
    try:
        paths = _unique_paths(ordered, directory_allowed=False)
    except HarnessError as exc:
        raise CodedError(WEX_ECP_003, f"the Git change set is not a normalized path set: {exc}") from exc
    return ChangeSet(paths=paths, complete=True, source="git", added=tuple(item for item in paths if item in new))


def validate_changed_targets(root: Path, change_set: ChangeSet) -> None:
    for value in change_set.paths:
        candidate = safe_destination(root, Path(value))
        if not candidate.exists() and not candidate.is_symlink():
            continue
        try:
            resolved = candidate.resolve(strict=True)
            resolved.relative_to(root)
        except (OSError, ValueError) as exc:
            raise CodedError(WEX200, f"changed path escapes the repository: {value}") from exc


def execution_scope(artifact: Any) -> tuple[str, ...]:
    table = artifact.metadata.get("execution_scope")
    if not isinstance(table, dict) or set(table) != {"paths"} or not isinstance(table.get("paths"), list):
        raise CodedError(WEX200, f"{artifact.artifact_id} has no valid [execution_scope].paths declaration")
    paths = _unique_paths(table["paths"], directory_allowed=True)
    if not paths:
        raise CodedError(WEX200, f"{artifact.artifact_id} execution scope is empty")
    return paths


def path_is_admitted(path: str, scope: Iterable[str]) -> bool:
    return any(
        path.startswith(entry) if entry.endswith("/") else path == entry
        for entry in scope
    )


def _snapshot_content(raw: bytes) -> bytes:
    """The bytes a formal snapshot hashes for one artifact (ECP-CSN-001, issue #256).

    Line endings are canonicalized as `utf8-text-lf-v1`, the rule the managed-file
    lock uses, so a CRLF checkout computes the same digest as the LF runner; content
    that is not UTF-8 text is hashed raw, as before.
    """

    from se_harness.integrity import IntegrityError, canonical_text_bytes

    try:
        return canonical_text_bytes(raw)
    except IntegrityError:
        return raw


def formal_snapshot_digest(root: Path, artifacts: Iterable[Any]) -> str:
    digest = hashlib.sha256()
    for artifact in sorted(artifacts, key=lambda item: item.path.relative_to(root).as_posix()):
        relative = artifact.path.relative_to(root).as_posix().encode("utf-8")
        content = _snapshot_content(artifact.path.read_bytes())
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()


def own_record_paths(root: Path, catalog: Mapping[str, Any], work_order_id: str) -> tuple[str, ...]:
    """SPEC-ECP-012 ECP-ADM-001/-002: the records that name the work order, as exact paths.

    A verification record whose ``verifies_work_order`` and a release record whose
    ``releases_work`` contains the selected work order are written by the harness
    at paths derived from the work order's own identity and land on its branch;
    each record's catalog path and its ``evaluator_evidence_path`` are admitted to
    the change set with the work order's own file. Admission is by relation, never
    by directory: nothing else under the records directories is admitted.
    """

    admitted: list[str] = []
    for item in catalog.values():
        relation = {"verification_record": "verifies_work_order", "release_record": "releases_work"}.get(
            getattr(item, "artifact_type", None)
        )
        if relation is None:
            continue
        named = item.relations.get(relation, [])
        if not isinstance(named, list) or work_order_id not in named:
            continue
        try:
            admitted.append(item.path.relative_to(root).as_posix())
        except ValueError:
            continue
        evidence = item.metadata.get("evaluator_evidence_path")
        if isinstance(evidence, str) and evidence:
            admitted.append(evidence)
    return tuple(sorted(set(admitted)))


_RISK_PATH = re.compile(r"^docs/engineering/([a-z0-9]+(?:-[a-z0-9]+)*)/risks/RISK-[A-Z][A-Z0-9]*-\d{3}\.md$")


def added_paths(root: Path, change_set: ChangeSet) -> frozenset[str]:
    """The change-set members that are new files (SPEC-RSK-010 RSK-MGT-027).

    A Git-derived set names them. A declared or manifest set is read against the
    checkout, where a member is new when it is untracked or staged as an addition;
    without a checkout nothing is provably new, so nothing is admitted as added.
    """

    if change_set.source == "git":
        return frozenset(change_set.added)
    if not (root / ".git").exists():
        return frozenset()
    try:
        untracked = _git_lines(root, ["ls-files", "-z", "--others", "--exclude-standard"], base="HEAD")
        staged = _git_lines(root, ["diff", "-z", "--cached", "--name-only", "--diff-filter=A", "--"], base="HEAD")
    except HarnessError:
        return frozenset()
    new = set(untracked) | set(staged)
    return frozenset(path for path in change_set.paths if path in new)


def risk_admissions(root: Path, primary: Any, change_set: ChangeSet) -> tuple[str, ...]:
    """SPEC-RSK-010 RSK-MGT-026 and RSK-MGT-027: the risk files an in-progress work order may add.

    Anyone may record a threat mid-execution, so an added
    `docs/engineering/<domain>/risks/RISK-<DOMAIN>-NNN.md` of the work order's own
    domain is admitted to its change set. A modified or deleted risk file, or one
    of another domain, still needs a declared path; the admission reads nothing
    but the work order's own path and the change set.
    """

    from se_harness.artifact_layout import artifact_domain_from_relative_path

    if getattr(primary, "artifact_type", None) != "work_order" or primary.status != "in_progress":
        return ()
    try:
        domain = artifact_domain_from_relative_path(primary.path.relative_to(root))
    except ValueError:
        return ()
    if domain is None:
        return ()
    new = added_paths(root, change_set)
    admitted = [
        path for path in change_set.paths
        if path in new and (match := _RISK_PATH.match(path)) is not None and match.group(1) == domain
    ]
    return tuple(sorted(admitted))
