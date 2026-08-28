"""Stateless selected-scope workflow checkpoint evaluation."""

from __future__ import annotations

import hashlib
import tomllib
import json
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Iterable, Mapping

from se_harness.installer import HarnessError, ensure_target, safe_destination
from se_harness.preflight import orphaned_ready_records, run_preflight
from se_harness.workflow_contract import (
    ContractError,
    effective_checkpoints,
    load_validated_contracts,
    select_rule,
    transition_binding,
)
from se_harness.workflow_procedures import (
    ProcedureError,
    command_or_response,
    corrective_response,
    decision_required,
    resolve_procedure,
    select_current_step,
)
from se_harness.workflow_result import build_result


CHANGE_SET_SCHEMA = "se-harness-change-set-v1"
_CONTROL = re.compile(r"[\x00-\x1f\x7f]")
_RESERVED = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{index}" for index in range(1, 10)),
    *(f"LPT{index}" for index in range(1, 10)),
}
_REPOSITORY_ERROR_CODES = {"E001", "E003"}


@dataclass(frozen=True)
class ChangeSet:
    paths: tuple[str, ...]
    complete: bool
    source: str


@dataclass
class CheckpointContext:
    root: Path
    artifact: Any
    report: Any
    catalog: Mapping[str, Any]
    scoped_errors: list[dict[str, Any]]
    repository_errors: list[dict[str, Any]]
    unrelated_count: int
    declared_scope: tuple[str, ...]
    admitted_scope: tuple[str, ...]
    change_set: ChangeSet
    checkpoint: str
    formal_snapshot_sha256: str
    target: str | None = None


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise HarnessError(f"WEX200: duplicate JSON key in change manifest: {key}")
        result[key] = value
    return result


def normalize_path(value: object, *, directory_allowed: bool = False) -> str:
    if not isinstance(value, str) or not value or len(value) > 4096:
        raise HarnessError("WEX200: path must be non-empty UTF-8 text of at most 4096 characters")
    if _CONTROL.search(value) or "\\" in value or ":" in value or any(token in value for token in ("*", "?", "[", "]")):
        raise HarnessError(f"WEX200: path is not a normalized repository path: {value!r}")
    directory = value.endswith("/")
    if directory and not directory_allowed:
        raise HarnessError(f"WEX200: changed path must name a file or component: {value!r}")
    candidate = value[:-1] if directory else value
    if not candidate or candidate.startswith("/") or candidate.startswith("//"):
        raise HarnessError(f"WEX200: absolute or empty path is forbidden: {value!r}")
    parts = PurePosixPath(candidate).parts
    if not parts or any(part in {"", ".", ".."} for part in parts):
        raise HarnessError(f"WEX200: dot or empty path component is forbidden: {value!r}")
    for part in parts:
        stem = part.rstrip(". ").split(".", 1)[0].upper()
        if stem in _RESERVED or part.endswith((".", " ")):
            raise HarnessError(f"WEX200: reserved path component is forbidden: {value!r}")
    normalized = PurePosixPath(*parts).as_posix() + ("/" if directory else "")
    if normalized != value:
        raise HarnessError(f"WEX200: path is not normalized: {value!r}")
    return normalized


def _unique_paths(values: Iterable[object], *, directory_allowed: bool) -> tuple[str, ...]:
    result: list[str] = []
    folded: dict[str, str] = {}
    for value in values:
        path = normalize_path(value, directory_allowed=directory_allowed)
        key = path.casefold()
        if key in folded:
            raise HarnessError(f"WEX200: duplicate or case-ambiguous path: {path!r}")
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
            raise HarnessError("WEX200: change manifest must remain inside the repository") from exc
    else:
        normalized = normalize_path(raw)
        candidate = safe_destination(root, Path(normalized))
        try:
            candidate = candidate.resolve(strict=True)
            candidate.relative_to(root)
        except (OSError, ValueError) as exc:
            raise HarnessError("WEX200: change manifest cannot resolve safely") from exc
    if candidate.is_symlink() or not candidate.is_file():
        raise HarnessError("WEX200: change manifest must be one ordinary file")
    try:
        data = candidate.read_bytes()
        if len(data) > 10_000_000:
            raise HarnessError("WEX200: change manifest exceeds 10 MB")
        value = json.loads(data.decode("utf-8"), object_pairs_hook=_pairs)
    except HarnessError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise HarnessError(f"WEX200: invalid change manifest: {exc}") from exc
    if not isinstance(value, dict) or set(value) != {"schema", "complete", "paths"}:
        raise HarnessError("WEX200: change manifest fields must be schema, complete, and paths")
    if value.get("schema") != CHANGE_SET_SCHEMA or not isinstance(value.get("complete"), bool):
        raise HarnessError("WEX200: change manifest schema or completeness value is invalid")
    if not isinstance(value.get("paths"), list):
        raise HarnessError("WEX200: change manifest paths must be an array")
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
    import subprocess

    try:
        completed = subprocess.run(
            ["git", "-C", str(root), *arguments],
            capture_output=True, check=False, timeout=120,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise HarnessError(f"WEX-ECP-003: git is unavailable for base {base!r}: {exc}") from exc
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", "replace").strip().splitlines()
        raise HarnessError(
            f"WEX-ECP-003: git {arguments[0]} failed for base {base!r} with exit status {completed.returncode}"
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
        raise HarnessError(f"WEX-ECP-003: the Git base must be a revision, not {base!r}")
    if not (root / ".git").exists():
        raise HarnessError(f"WEX-ECP-003: {root} is not a Git checkout; --from-git needs one")
    _git_lines(root, ["rev-parse", "--verify", "--quiet", f"{base}^{{commit}}"], base=base)
    changed = _git_lines(root, ["diff", "-z", "--name-only", "--no-renames", base, "--"], base=base)
    untracked = _git_lines(root, ["ls-files", "-z", "--others", "--exclude-standard"], base=base)
    ordered: list[str] = []
    for item in [*changed, *untracked]:
        if item not in ordered:
            ordered.append(item)
    try:
        paths = _unique_paths(ordered, directory_allowed=False)
    except HarnessError as exc:
        raise HarnessError(f"WEX-ECP-003: the Git change set is not a normalized path set: {exc}") from exc
    return ChangeSet(paths=paths, complete=True, source="git")


def _validate_changed_targets(root: Path, change_set: ChangeSet) -> None:
    for value in change_set.paths:
        candidate = safe_destination(root, Path(value))
        if not candidate.exists() and not candidate.is_symlink():
            continue
        try:
            resolved = candidate.resolve(strict=True)
            resolved.relative_to(root)
        except (OSError, ValueError) as exc:
            raise HarnessError(f"WEX200: changed path escapes the repository: {value}") from exc


def execution_scope(artifact: Any) -> tuple[str, ...]:
    table = artifact.metadata.get("execution_scope")
    if not isinstance(table, dict) or set(table) != {"paths"} or not isinstance(table.get("paths"), list):
        raise HarnessError(f"WEX200: {artifact.artifact_id} has no valid [execution_scope].paths declaration")
    paths = _unique_paths(table["paths"], directory_allowed=True)
    if not paths:
        raise HarnessError(f"WEX200: {artifact.artifact_id} execution scope is empty")
    return paths


def path_is_admitted(path: str, scope: Iterable[str]) -> bool:
    return any(
        path.startswith(entry) if entry.endswith("/") else path == entry
        for entry in scope
    )


def formal_snapshot_digest(root: Path, artifacts: Iterable[Any]) -> str:
    digest = hashlib.sha256()
    for artifact in sorted(artifacts, key=lambda item: item.path.relative_to(root).as_posix()):
        relative = artifact.path.relative_to(root).as_posix().encode("utf-8")
        content = artifact.path.read_bytes()
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()


def _diagnostic(item: Any) -> dict[str, Any]:
    return {"code": item.code, "path": item.path, "message": item.message, "plane": item.plane}


def _classify(report: Any, catalog: Mapping[str, Any], primary: Any, root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], int]:
    from se_harness.workflow import PRIMARY_TYPES, project_scope

    if primary.artifact_type in PRIMARY_TYPES:
        governing, dependencies = project_scope(catalog, primary)
    else:
        # A definition's selected scope is itself (transition checkpoint, ECP-KRN-004).
        governing, dependencies = set(), set()
    scope_paths = {
        catalog[identifier].path.resolve()
        for identifier in governing | dependencies | {primary.artifact_id}
        if identifier in catalog
    }
    scoped: list[dict[str, Any]] = []
    repository: list[dict[str, Any]] = []
    unrelated = 0
    for item in report.errors:
        diagnostic = _diagnostic(item)
        if item.code in _REPOSITORY_ERROR_CODES:
            repository.append(diagnostic)
            continue
        try:
            candidate = safe_destination(root, Path(item.path)).resolve()
        except HarnessError:
            repository.append({**diagnostic, "code": "WEX200"})
            continue
        if candidate in scope_paths:
            scoped.append(diagnostic)
        else:
            unrelated += 1
    for item in report.warnings:
        try:
            selected = safe_destination(root, Path(item.path)).resolve() in scope_paths
        except HarnessError:
            selected = False
        if not selected:
            unrelated += 1
    return scoped, repository, unrelated


def lifecycle_relevant_diagnostics(root: Path, report: Any) -> list[Any]:
    """The one preflight-diagnostic filter (ECP-KRN-007).

    Candidate-distribution comparisons and lock entries the released root never
    recorded are candidate-versus-released skew, not installation facts; every
    other diagnostic blocks a lifecycle stage.
    """

    lock_files: set[str] = set()
    try:
        lock = json.loads((root / ".engineering-harness.lock").read_text(encoding="utf-8"))
        if isinstance(lock, dict) and isinstance(lock.get("files"), dict):
            lock_files = {str(path) for path in lock["files"]}
    except (OSError, UnicodeError, json.JSONDecodeError):
        pass

    def relevant(item: Any) -> bool:
        path = str(item.path)
        if item.code == "I001" and path.startswith("distribution:"):
            return False
        candidate = path.removeprefix("lock-entry:")
        if item.code == "I001" and item.message in {"missing", "required"} and candidate not in lock_files:
            return False
        return True

    return [item for item in report.diagnostics if relevant(item)]


def _preflight_status(context: CheckpointContext, phase: str) -> tuple[str, str]:
    if context.artifact.artifact_type != "work_order":
        return "pass", f"{phase} preflight does not apply to {context.artifact.artifact_type}."
    report = run_preflight(context.root, work_order_id=context.artifact.artifact_id, phase=phase)
    relevant = lifecycle_relevant_diagnostics(context.root, report)
    if relevant:
        return "fail", relevant[0].message
    return "pass", f"Released-installation {phase} preflight inputs are ready."


EVIDENCE_HEADER_KEYS = ("artifact", "checkpoint", "formal_snapshot_sha256", "rebound_at")
_HEADER_OPEN = b"```toml\n"
_HEADER_CLOSE = b"\n```\n"
_RFC3339 = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def parse_evidence_header(data: bytes) -> tuple[dict[str, str] | None, bytes]:
    """Split a packet into its machine header and retained body (ECP-EVD-002, -004).

    Returns `(None, data)` when no fenced TOML block starts at byte offset 0.
    A block that starts there but is not valid TOML with exactly the four
    header keys raises `WEX-ECP-010`.
    """

    if not data.startswith(_HEADER_OPEN):
        return None, data
    end = data.find(_HEADER_CLOSE, len(_HEADER_OPEN))
    if end < 0:
        raise HarnessError("WEX-ECP-010: the evidence packet header fence is not closed")
    raw = data[len(_HEADER_OPEN):end]
    try:
        parsed = tomllib.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        raise HarnessError(f"WEX-ECP-010: the evidence packet header is not valid TOML: {exc}") from exc
    if set(parsed) != set(EVIDENCE_HEADER_KEYS) or not all(isinstance(parsed[key], str) for key in EVIDENCE_HEADER_KEYS):
        raise HarnessError(
            "WEX-ECP-010: the evidence packet header must carry exactly "
            + ", ".join(EVIDENCE_HEADER_KEYS)
        )
    return {key: parsed[key] for key in EVIDENCE_HEADER_KEYS}, data[end + len(_HEADER_CLOSE):]


def render_evidence_header(fields: Mapping[str, str]) -> bytes:
    lines = [f'{key} = "{fields[key]}"' for key in EVIDENCE_HEADER_KEYS]
    return _HEADER_OPEN + "\n".join(lines).encode("utf-8") + _HEADER_CLOSE


def evidence_packet_path(root: Path, artifact: Any, checkpoint: str) -> Path:
    """`DOMAIN/evidence/WO-ID/WO-ID-CHECKPOINT.md` (ECP-EVD-001)."""

    from se_harness.artifact_layout import artifact_domain_from_relative_path

    domain = artifact_domain_from_relative_path(artifact.path.relative_to(root))
    if domain is None:
        raise HarnessError(f"WEX-ECP-010: {artifact.artifact_id} is not under a domain directory")
    return root / "docs" / "engineering" / domain / "evidence" / artifact.artifact_id / f"{artifact.artifact_id}-{checkpoint}.md"


def _line_ending_conversion(root: Path, relative: str) -> str | None:
    """The attribute rule that would convert this path's line endings, if any (ECP-EVD-006)."""

    import subprocess

    if not (root / ".git").exists():
        return None
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), "check-attr", "-z", "text", "eol", "--", relative],
            capture_output=True, check=False, timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if completed.returncode != 0:
        return None
    fields = completed.stdout.split(b"\0")
    values: dict[str, str] = {}
    for index in range(0, len(fields) - 2, 3):
        values[fields[index + 1].decode("utf-8", "replace")] = fields[index + 2].decode("utf-8", "replace")
    text, eol = values.get("text", "unspecified"), values.get("eol", "unspecified")
    if text in {"set", "auto"} and eol != "lf":
        return f"text={text} eol={eol}"
    return None


def write_evidence_packet(
    repository: Path,
    *,
    artifact_id: str,
    checkpoint: str,
    now: str,
) -> dict[str, Any]:
    """Write or rebind one evidence packet and return the schema-2 result (ECP-EVD-001 to -007)."""

    from se_harness.workflow import _catalog, _validation, project_scope

    if checkpoint not in {"start", "pre-action", "transition", "handoff"}:
        raise HarnessError("WEX-ECP-010: the checkpoint must be start, pre-action, transition, or handoff")
    if not _RFC3339.fullmatch(now):
        raise HarnessError("WEX-ECP-010: rebound_at must be RFC 3339 UTC at second precision")
    root = ensure_target(repository, must_exist=True)
    _, report = _validation(root)
    catalog = _catalog(report)
    primary = catalog.get(artifact_id)
    if primary is None:
        raise HarnessError(f"WEX-ECP-010: unknown artifact ID: {artifact_id}")
    if primary.artifact_type != "work_order":
        raise HarnessError("WEX-ECP-010: evidence packets are keyed by a work order")
    in_progress = sorted(
        item.artifact_id for item in catalog.values()
        if item.artifact_type == "work_order" and item.status == "in_progress"
    )
    if len(in_progress) == 1 and in_progress[0] != artifact_id:
        raise HarnessError(
            f"WEX-ECP-012: the working tree selects {in_progress[0]} (the one in_progress work order), not {artifact_id}"
        )
    path = evidence_packet_path(root, primary, checkpoint)
    relative = path.relative_to(root).as_posix()
    conversion = _line_ending_conversion(root, relative)
    if conversion is not None:
        raise HarnessError(f"WEX-ECP-011: a .gitattributes rule would convert line endings of {relative} ({conversion})")
    snapshot = formal_snapshot_digest(root, report.artifacts)
    header = {
        "artifact": artifact_id,
        "checkpoint": checkpoint,
        "formal_snapshot_sha256": snapshot,
        "rebound_at": now,
    }
    action = "create"
    if path.exists():
        if path.is_symlink() or not path.is_file():
            raise HarnessError(f"WEX-ECP-010: {relative} is not an ordinary file")
        existing, body = parse_evidence_header(path.read_bytes())
        if existing is None:
            raise HarnessError(f"WEX-ECP-010: {relative} carries no evidence packet header at byte offset 0")
        if existing["artifact"] != artifact_id or existing["checkpoint"] != checkpoint:
            raise HarnessError(
                f"WEX-ECP-010: {relative} is the packet of {existing['artifact']} at {existing['checkpoint']}, "
                f"not {artifact_id} at {checkpoint}"
            )
        action = "rebind"
    else:
        body = (
            f"\n# {artifact_id} {checkpoint} evidence\n\n"
            "Retained by `harnessctl evidence`; body content is owner-authored.\n"
        ).encode("utf-8")
    content = render_evidence_header(header) + body
    path.parent.mkdir(parents=True, exist_ok=True)
    staged = path.with_name(path.name + ".tmp")
    try:
        staged.write_bytes(content)
        staged.replace(path)
    except OSError as exc:
        staged.unlink(missing_ok=True)
        raise HarnessError(f"WEX-ECP-010: cannot write the evidence packet: {exc}") from exc
    governing, dependencies = project_scope(catalog, primary)
    return selected_result(
        root,
        operation="evidence",
        primary=primary,
        related=[catalog[item] for item in dependencies if item in catalog],
        governing=governing,
        dependencies=dependencies,
        done=[
            f"{'Rebound' if action == 'rebind' else 'Wrote'} the {checkpoint} evidence packet of {artifact_id} "
            f"at {relative} to formal snapshot {snapshot}."
        ],
        after=[{"id": artifact_id, "status": primary.status}],
        writes=[{"id": artifact_id, "path": relative, "fields": list(EVIDENCE_HEADER_KEYS)}],
    )


def retain_handoff_result(root: Path, artifact: Any, result: Mapping[str, Any]) -> str:
    """Retain a completed Git-derived handoff result beside the packet (ECP-PRB-002, amended)."""

    path = evidence_packet_path(root, artifact, "handoff").with_name("handoff.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(result, indent=2, ensure_ascii=True, sort_keys=True) + "\n").encode("utf-8")
    staged = path.with_name(path.name + ".tmp")
    try:
        staged.write_bytes(data)
        staged.replace(path)
    except OSError as exc:
        staged.unlink(missing_ok=True)
        raise HarnessError(f"WEX-ECP-010: cannot retain the handoff result: {exc}") from exc
    return path.relative_to(root).as_posix()


def _review_evidence(context: CheckpointContext) -> tuple[str, str]:
    if context.artifact.artifact_type != "work_order":
        return "pass", "Work-order implementation evidence does not apply to this artifact type."
    evidence_root = context.root / "docs" / "engineering"
    candidates = [
        path for path in evidence_root.rglob("*")
        if path.is_file()
        and "evidence" in path.parts
        and any(part.startswith(context.artifact.artifact_id) for part in path.parts[path.parts.index("evidence") + 1 :])
    ]
    binding = f"formal_snapshot_sha256: {context.formal_snapshot_sha256}"
    # The handoff checkpoint is the one that retains evidence; a transition to
    # implemented accepts the handoff-bound document for the same snapshot, so
    # the transition can never pass on weaker evidence than check evaluated.
    checkpoint = "handoff" if context.checkpoint == "transition" else context.checkpoint
    legacy: str | None = None
    for path in sorted(candidates):
        try:
            data = path.read_bytes()
        except OSError:
            continue
        relative = path.relative_to(context.root).as_posix()
        # ECP-EVD-005: the machine header is read through the TOML parser, never by substring.
        try:
            header, _ = parse_evidence_header(data)
        except HarnessError:
            header = None
        if header is not None:
            if (
                header["artifact"] == context.artifact.artifact_id
                and header["checkpoint"] == checkpoint
                and header["formal_snapshot_sha256"] == context.formal_snapshot_sha256
            ):
                return "pass", f"Fresh retained evidence is bound at {relative}."
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeError:
            continue
        if (
            legacy is None
            and f"artifact: {context.artifact.artifact_id}" in text
            and f"checkpoint: {checkpoint}" in text
            and binding in text
        ):
            legacy = relative
    if legacy is not None:
        # Compatibility for one release: substring-bound packets still pass, named by W-ECP-002.
        return "pass", (
            f"Fresh retained evidence is bound at {legacy}. W-ECP-002: the packet carries no machine header; "
            f"migrate it with harnessctl evidence . --artifact {context.artifact.artifact_id} --checkpoint {checkpoint}."
        )
    return "not_assessable", (
        f"No readable evidence for {context.artifact.artifact_id}, checkpoint {checkpoint}, "
        f"and formal snapshot {context.formal_snapshot_sha256} is available."
    )


def _evaluate(name: str, predicate: Mapping[str, Any], context: CheckpointContext) -> tuple[str, str]:
    if name == "artifact_status":
        statuses = predicate.get("statuses", [])
        if context.artifact.status in statuses:
            return "pass", f"{context.artifact.artifact_id} status is {context.artifact.status}."
        return "fail", f"{context.artifact.artifact_id} status {context.artifact.status} is not one of {', '.join(statuses)}."
    if name == "formal_graph_valid":
        if context.scoped_errors:
            return "fail", f"Selected graph validation failed: {context.scoped_errors[0]['message']}"
        return "pass", "The selected formal graph is valid."
    if name == "repository_integrity":
        if context.repository_errors:
            return "fail", f"Repository integrity failed: {context.repository_errors[0]['message']}"
        return "pass", "No repository-integrity blocker prevents selected evaluation."
    if name == "execution_scope_declared":
        if context.declared_scope:
            return "pass", f"{context.artifact.artifact_id} declares {len(context.declared_scope)} normalized scope path(s)."
        return "not_assessable", f"{context.artifact.artifact_id} has no assessable execution scope."
    if name == "change_set_complete":
        if context.change_set.complete:
            return "pass", "The caller explicitly asserted that the declared change set is complete."
        return "not_assessable", "Change-set completeness was not asserted; absence of undeclared changes cannot be inferred."
    if name == "changed_paths_within_scope":
        if not context.change_set.complete:
            return "not_assessable", "Changed-path scope cannot pass without an explicit completeness assertion."
        outside = [path for path in context.change_set.paths if not path_is_admitted(path, context.admitted_scope)]
        if outside:
            return "fail", f"WEX201: changed path is outside execution scope: {outside[0]}"
        return "pass", f"All {len(context.change_set.paths)} declared changed path(s) are within execution scope."
    if name == "start_preflight_ready":
        return _preflight_status(context, "start")
    if name == "review_preflight_ready":
        return _preflight_status(context, "review")
    if name == "review_evidence_available":
        return _review_evidence(context)
    if name == "authoring_ready":
        return authoring_ready(context.artifact)
    if name == "release_unit_ready":
        return release_unit_ready(context.artifact, context.root, context.catalog)
    raise ContractError(f"unknown predicate evaluator {name}")


def _aggregate(statuses: Iterable[str]) -> str:
    values = set(statuses)
    if "fail" in values:
        return "fail"
    if "not_assessable" in values:
        return "not_assessable"
    return "pass"


def _evidence(descriptors: Iterable[Mapping[str, Any]], artifact_id: str, checkpoint: str) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for descriptor in descriptors:
        result.append(
            {
                "kind": str(descriptor.get("kind", "result")),
                "reference": str(descriptor.get("reference", "")).replace("{artifact_id}", artifact_id).replace("{checkpoint}", checkpoint),
            }
        )
    return result


def _gate_results(
    gate_ids: Iterable[str],
    gates: Mapping[str, Mapping[str, Any]],
    context: CheckpointContext,
    predicate_ids: Iterable[str] | None = None,
) -> list[dict[str, Any]]:
    selected = None if predicate_ids is None else set(predicate_ids)
    result: list[dict[str, Any]] = []
    for gate_id in gate_ids:
        gate = gates[gate_id]
        if context.checkpoint not in gate["checkpoints"]:
            raise HarnessError(
                f"WEX210: gate {gate_id} does not apply at checkpoint {context.checkpoint}"
            )
        predicates: list[dict[str, Any]] = []
        for predicate in gate["predicates"]:
            if selected is not None and predicate["id"] not in selected:
                continue
            if context.checkpoint not in effective_checkpoints(gate, predicate):
                continue
            status, message = _evaluate(predicate["evaluator"], predicate, context)
            predicates.append(
                {
                    "id": predicate["id"],
                    "status": status,
                    "evidence": _evidence(predicate["required_evidence"], context.artifact.artifact_id, context.checkpoint),
                    "message": message,
                }
            )
        result.append({"id": gate_id, "status": _aggregate(item["status"] for item in predicates), "predicates": predicates})
    return result


def build_context(
    root: Path,
    report: Any,
    catalog: Mapping[str, Any],
    primary: Any,
    *,
    checkpoint: str,
    change_set: ChangeSet,
    target: str | None = None,
) -> CheckpointContext:
    """The one context builder `check` and `transition` share (ECP-KRN-004)."""

    scoped, repository_errors, unrelated = _classify(report, catalog, primary, root)
    try:
        scope = execution_scope(primary) if primary.artifact_type == "work_order" else ()
    except HarnessError:
        scope = ()
    return CheckpointContext(
        root=root,
        artifact=primary,
        report=report,
        catalog=catalog,
        scoped_errors=scoped,
        repository_errors=repository_errors,
        unrelated_count=unrelated,
        declared_scope=scope,
        # ECP-CHG-007: the selected work order's own artifact path is admitted by
        # construction; only `transition` writes it and it is in every Git diff
        # after the work order's own approval and start.
        admitted_scope=(
            *scope,
            primary.path.relative_to(root).as_posix(),
            # ECP-PRB-002 (amended): the harness retains the packet and the handoff
            # result under the work order's packet directory; harness-written
            # evidence at its own path is admitted with the work order's file.
            *(
                (evidence_packet_path(root, primary, "handoff").parent.relative_to(root).as_posix() + "/",)
                if primary.artifact_type == "work_order" else ()
            ),
        ),
        change_set=change_set,
        checkpoint=checkpoint,
        formal_snapshot_sha256=formal_snapshot_digest(root, report.artifacts),
        target=target,
    )


STRUCTURAL_GATE = "QG-STRUCTURAL"


def transition_gate_results(
    quality_gates: Mapping[str, Any],
    gates: Mapping[str, Mapping[str, Any]],
    context: CheckpointContext,
    *,
    structural: Iterable[Mapping[str, Any]] = (),
) -> list[dict[str, Any]]:
    """Evaluate the contract's transition bindings for one edge (ECP-KRN-004, -005).

    Gate predicates come from `QUALITY_GATES.json`; the graph-structural checks
    the caller evaluated are appended as the synthetic `QG-STRUCTURAL` gate so a
    refusal always names its check.
    """

    from se_harness.workflow import _family

    if context.target is None:
        raise HarnessError("WEX210: the transition checkpoint requires a target state")
    predicate_ids, _ = transition_binding(
        quality_gates, _family(context.artifact.artifact_type), context.artifact.artifact_type, context.target
    )
    gate_order: list[str] = []
    for gate_id, gate in gates.items():
        if any(str(item["id"]) in predicate_ids for item in gate["predicates"]) and gate_id not in gate_order:
            gate_order.append(gate_id)
    results = _gate_results(gate_order, gates, context, predicate_ids=predicate_ids)
    structural_items = [dict(item) for item in structural]
    if structural_items:
        results.append({
            "id": STRUCTURAL_GATE,
            "status": _aggregate(item["status"] for item in structural_items),
            "predicates": structural_items,
        })
    return results


def check_workflow(
    repository: Path,
    *,
    artifact_id: str,
    checkpoint: str,
    procedure_id: str | None = None,
    changed_paths: Iterable[str] = (),
    changes_complete: bool = False,
    change_manifest: Path | None = None,
    pull_request_body: Path | None = None,
    target: str | None = None,
    from_git: str | None = None,
) -> dict[str, Any]:
    if from_git is not None and (list(changed_paths) or changes_complete or change_manifest is not None):
        raise HarnessError(
            "WEX-ECP-002: --from-git is mutually exclusive with --changed-path, --changes-complete and --change-manifest"
        )
    if checkpoint not in {"start", "pre-action", "transition", "handoff"}:
        raise HarnessError("WEX210: public check checkpoint must be start, pre-action, transition, or handoff")
    if checkpoint == "transition" and not target:
        raise HarnessError("WEX210: --target is required for the transition checkpoint")
    if checkpoint != "transition" and target:
        raise HarnessError("WEX210: --target applies only to the transition checkpoint")
    root = ensure_target(repository, must_exist=True)
    workflow_contract, quality_gates, rules, procedures, gates = load_validated_contracts()
    from se_harness.workflow import _catalog, _validation, project_scope

    _, report = _validation(root)
    try:
        catalog = _catalog(report)
    except HarnessError as exc:
        raise HarnessError(f"WEX210: {exc}") from exc
    primary = catalog.get(artifact_id)
    if primary is None:
        raise HarnessError(f"WEX210: unknown artifact ID: {artifact_id}")
    if primary.artifact_type not in {"work_order", "verification_record", "release_record"}:
        raise HarnessError("WEX210: check accepts only WO, VREC, or RLS artifacts")
    governing, dependencies = project_scope(catalog, primary)
    related = [catalog[item] for item in dependencies if item in catalog]
    rule, rule_context = select_rule(rules, primary, related=related)
    selected_procedure = str(rule["procedure_id"])
    alternatives = list(rule.get("alternative_procedure_ids", []))
    if checkpoint == "pre-action" and procedure_id is None:
        raise HarnessError("WEX220: --procedure is required for pre-action")
    if procedure_id is not None:
        if procedure_id not in {selected_procedure, *alternatives}:
            raise HarnessError(f"WEX220: procedure {procedure_id} is not selected by workflow rule {rule['id']}")
        selected_procedure = procedure_id
    if from_git is not None:
        change_set = git_change_set(root, from_git)
    elif change_manifest is not None:
        change_set = parse_change_manifest(root, change_manifest)
    else:
        change_set = declared_change_set(changed_paths, complete=changes_complete)
    _validate_changed_targets(root, change_set)
    context = build_context(
        root, report, catalog, primary, checkpoint=checkpoint, change_set=change_set, target=target
    )
    scoped, repository_errors, unrelated = context.scoped_errors, context.repository_errors, context.unrelated_count
    scope = context.declared_scope
    gate_ids = list(rule["gate_ids"])
    resolved = resolve_procedure(
        procedures,
        selected_procedure,
        {
            "artifact_id": artifact_id,
            "status": primary.status,
            "changed_paths": list(change_set.paths),
            **rule_context,
        },
    )
    if checkpoint == "pre-action":
        first = resolved["steps"][0]
        gate_ids = list(dict.fromkeys([*gate_ids, *first.get("gate_ids", [])]))
    if checkpoint == "transition":
        from se_harness.workflow import structural_precondition_results

        structural = structural_precondition_results(root, catalog, catalog, primary, str(target), None)
        gate_results = transition_gate_results(quality_gates, gates, context, structural=structural)
    else:
        gate_results = _gate_results(gate_ids, gates, context)
    compliance_status = _aggregate([item["status"] for item in gate_results] or ["pass"])
    passed = compliance_status == "pass" and not scoped and not repository_errors
    outcome = "completed" if passed else "blocked"
    current_step = select_current_step(resolved, checkpoint=checkpoint, passed=passed)
    predicate_blockers = [
        f"{predicate['id']}: {predicate['message']}"
        for gate in gate_results
        for predicate in gate["predicates"]
        if predicate["status"] != "pass"
    ]
    finding_blockers = [
        f"{item['code']}: {item['message']}"
        for item in [*repository_errors, *scoped]
    ]
    trap_blockers: list[str] = []
    if checkpoint == "handoff" and primary.artifact_type == "work_order":
        trap_blockers.extend(
            f"W-ADS-002: {message}" for message in orphaned_ready_records(root, catalog.values(), artifact_id)
        )
        if pull_request_body is not None:
            trap_blockers.extend(f"W-ADS-001: {message}" for message in _pull_request_body_findings(root, pull_request_body))
    if trap_blockers:
        passed = False
        outcome = "blocked"
        current_step = select_current_step(resolved, checkpoint=checkpoint, passed=False)
    blockers = [*predicate_blockers, *finding_blockers, *trap_blockers]
    action = (
        str(current_step.get("decision", "Provide the required decision"))
        if current_step["kind"] == "decision"
        else "Run the bound command"
        if current_step["kind"] == "command"
        else "Follow the bound reference"
    )
    next_command = command_or_response(current_step)
    if not passed:
        first_failing = next(
            (
                predicate
                for gate in gate_results
                for predicate in gate["predicates"]
                if predicate["status"] != "pass"
            ),
            None,
        )
        action, next_command = corrective_response(
            current_step, first_failing, formal_snapshot_sha256=context.formal_snapshot_sha256
        )
        evaluated = ["harnessctl", "check", ".", "--artifact", artifact_id, "--checkpoint", checkpoint]
        if next_command.get("kind") == "command" and list(next_command.get("argv", [])) == evaluated:
            raise HarnessError("WEX-ADS-001: the corrective command repeats the evaluated command")
    restitution = {
        "outcome": outcome,
        "done": [f"Evaluated {checkpoint} compliance for {artifact_id}."],
        "not_done": [] if passed else [f"The {checkpoint} checkpoint did not pass."],
        "blocked_by": blockers,
        "current_lifecycle_state": [f"{artifact_id} is {primary.status}."],
        "decision_required": decision_required(current_step) if passed else None,
        "next": {"procedure_id": selected_procedure, "step_id": current_step["id"], "action": action},
        "command_or_response": next_command,
        "alternatives": [f"Use complete alternative procedure {identifier}." for identifier in alternatives],
    }
    return build_result(
        operation="check",
        outcome=outcome,
        primary=artifact_id,
        artifacts=[artifact_id],
        governing=governing,
        dependencies=dependencies,
        declared_paths=scope,
        changed_paths=change_set.paths,
        change_set_complete=change_set.complete,
        compliance={
            "checkpoint": checkpoint,
            "workflow_rule_id": rule["id"],
            "procedure_id": selected_procedure,
            "status": compliance_status if not (scoped or repository_errors) else "fail",
            "gates": gate_results,
            "formal_snapshot_sha256": context.formal_snapshot_sha256,
            "change_set_source": change_set.source,
        },
        procedure={"id": selected_procedure, "current_step": current_step["id"], "steps": resolved["steps"]},
        restitution=restitution,
        before=[{"id": artifact_id, "status": primary.status}],
        after=[{"id": artifact_id, "status": primary.status}],
        scoped_blockers=scoped,
        repository_blockers=repository_errors,
        unrelated_count=unrelated,
    )


def _rule_prose(rule: Mapping[str, Any], context: Mapping[str, str]) -> tuple[list[str], list[str]]:
    block = rule.get("restitution", {})
    done = [str(item).format_map(context) for item in block.get("done", [])]
    current = [str(item).format_map(context) for item in block.get("current_lifecycle_state", [])]
    return done, current


def selected_result(
    root: Path,
    *,
    operation: str,
    primary: Any,
    related: Iterable[Any] = (),
    artifacts: Iterable[str] | None = None,
    governing: Iterable[str] = (),
    dependencies: Iterable[str] = (),
    done: Iterable[str] | None = None,
    blocked_by: Iterable[str] = (),
    before: Iterable[Mapping[str, str]] = (),
    after: Iterable[Mapping[str, str]] = (),
    scoped_blockers: Iterable[Mapping[str, Any]] = (),
    repository_blockers: Iterable[Mapping[str, Any]] = (),
    unrelated_count: int = 0,
    writes: Iterable[Mapping[str, Any]] = (),
    checkpoint: str = "pre-action",
    gates: Iterable[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """Build the one schema-2 result for a selected artifact (ECP-KRN-001, -003).

    `focus`, `transition`, `capture-verification` and `prepare-release` all
    render through here: `select_rule` over the primary and its related
    artifacts picks the workflow rule, the rule's procedure supplies the typed
    next step, and the rule's `restitution` prose supplies what was done and
    the lifecycle state. A blocked result keeps the rule's next step but says
    nothing was done.
    """

    _, _, rules, procedures, _ = load_validated_contracts()
    related_items = list(related)
    rule, rule_context = select_rule(rules, primary, related=related_items)
    resolved = resolve_procedure(
        procedures,
        str(rule["procedure_id"]),
        {"artifact_id": primary.artifact_id, "status": primary.status, **rule_context},
    )
    step = resolved["steps"][0]
    blockers = [str(item) for item in blocked_by]
    blocked = bool(blockers)
    gate_results = [dict(item) for item in gates]
    rule_done, current = _rule_prose(rule, rule_context)
    scope: tuple[str, ...] = ()
    if primary.artifact_type == "work_order":
        try:
            scope = execution_scope(primary)
        except HarnessError:
            scope = ()
    restitution = {
        "outcome": "blocked" if blocked else "completed",
        "done": [] if blocked else [str(item) for item in (rule_done if done is None else done)],
        "not_done": [f"The selected {operation} operation remains incomplete."] if blocked else [],
        "blocked_by": blockers,
        "current_lifecycle_state": ["No lifecycle state was changed."] if blocked else current,
        "decision_required": decision_required(step) if not blocked else None,
        "next": {
            "procedure_id": rule["procedure_id"],
            "step_id": step["id"],
            "action": str(step.get("decision", "Run the bound command" if step["kind"] == "command" else "Follow the bound reference")),
        },
        "command_or_response": command_or_response(step),
        "alternatives": [
            f"Use complete alternative procedure {identifier}."
            for identifier in rule.get("alternative_procedure_ids", [])
        ],
    }
    return build_result(
        operation=operation,
        outcome="blocked" if blocked else "completed",
        primary=primary.artifact_id,
        artifacts=[primary.artifact_id] if artifacts is None else list(artifacts),
        governing=governing,
        dependencies=dependencies,
        declared_paths=scope,
        changed_paths=[],
        change_set_complete=False,
        compliance={
            "checkpoint": checkpoint,
            "workflow_rule_id": rule["id"],
            "procedure_id": rule["procedure_id"],
            "status": (
                _aggregate(item["status"] for item in gate_results)
                if gate_results and not blocked
                else "fail" if blocked else "not_assessable"
            ),
            "gates": gate_results,
        },
        procedure={"id": rule["procedure_id"], "current_step": step["id"], "steps": resolved["steps"]},
        restitution=restitution,
        before=list(before),
        after=list(after),
        scoped_blockers=list(scoped_blockers),
        repository_blockers=list(repository_blockers),
        unrelated_count=unrelated_count,
        writes=list(writes),
    )


def remediation_result(
    operation: str,
    primary: str | None,
    finding: Mapping[str, Any],
    *,
    repository_blocker: bool = False,
) -> dict[str, Any]:
    """Build the schema-2 result of an operation that could not select or act."""

    workflow, _, _, procedures, _ = load_validated_contracts()
    failure = workflow["failure"]
    procedure_id = str(failure["procedure_id"])
    steps: list[dict[str, Any]] = []
    if primary:
        try:
            steps = resolve_procedure(procedures, procedure_id, {"artifact_id": primary})["steps"]
        except ProcedureError:
            steps = []
    step_id = steps[0]["id"] if steps else f"STEP-{procedure_id.removeprefix('PROC-')}-FOCUS"
    message = str(finding.get("message", ""))
    _, current = _rule_prose(failure, {"message": message})
    restitution = {
        "outcome": "blocked",
        "done": [],
        "not_done": ["The requested workflow operation remains incomplete."],
        "blocked_by": [f"{finding.get('code', 'WEX')}: {message}"],
        "current_lifecycle_state": current,
        "decision_required": None,
        "next": {"procedure_id": procedure_id, "step_id": step_id, "action": "remediate"},
        "command_or_response": (
            {"kind": "command", "argv": ["harnessctl", "next", ".", "--artifact", primary]}
            if primary
            else {"kind": "response", "value": "Resolve the reported blocker, then run harnessctl next . to obtain the selected context."}
        ),
        "alternatives": [],
    }
    return build_result(
        operation=operation,
        outcome="blocked",
        primary=primary or "",
        artifacts=[primary] if primary else [],
        governing=[],
        dependencies=[],
        declared_paths=[],
        changed_paths=[],
        change_set_complete=False,
        compliance={
            "checkpoint": "pre-action",
            "workflow_rule_id": str(failure["id"]),
            "procedure_id": procedure_id,
            "status": "fail",
            "gates": [],
        },
        procedure={"id": procedure_id, "current_step": step_id, "steps": steps},
        restitution=restitution,
        scoped_blockers=[] if repository_blocker else [dict(finding)],
        repository_blockers=[dict(finding)] if repository_blocker else [],
    )


def focus_schema2(
    repository: Path,
    *,
    artifact_id: str,
    include_background: bool = False,
) -> dict[str, Any]:
    """Selected focus; the name is kept for callers, the result is `workflow.focus` (WO-ECP-005)."""

    from se_harness.workflow import focus

    return focus(repository, artifact_id, include_background=include_background)


def _pull_request_body_findings(root: Path, body_path: Path) -> list[str]:
    """Report W-ADS-001 for a pull-request body whose trailer carries a carriage return."""

    from se_harness.github_ci import MAX_EVENT_BYTES, carriage_return_trailer_offsets

    try:
        with body_path.open("rb") as handle:
            raw = handle.read(MAX_EVENT_BYTES + 1)
    except OSError as exc:
        raise HarnessError(f"WEX200: cannot read pull-request body: {exc}") from exc
    if len(raw) > MAX_EVENT_BYTES:
        raise HarnessError("WEX200: pull-request body exceeds the size limit")
    try:
        body = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HarnessError("WEX200: pull-request body must be UTF-8") from exc
    return [
        (
            f"the Harness-Work-Order line ends with a carriage return at byte offset {offset}; "
            "write the body with LF line endings (newline=\"\\n\" in Python, or core.autocrlf=false) before pushing"
        )
        for offset in carriage_return_trailer_offsets(body)
    ]


_PLACEHOLDER = re.compile(r"<[A-Za-z][^>\n]{2,80}>")
_FENCE = re.compile(r"```.*?```", re.DOTALL)
_INLINE_CODE = re.compile(r"`[^`\n]*`")
_DEFINITION_TYPES = {
    "intent", "capability", "requirement", "specification", "architecture", "adr",
    "verification", "release_contract", "operating_contract",
}


def authoring_ready(artifact: Any) -> tuple[str, str]:
    """AUT-GTE-001: no leftover template placeholder, and Open decisions closed."""

    try:
        text = artifact.path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        return "not_assessable", f"{artifact.artifact_id} cannot be read: {exc}"
    prose = _INLINE_CODE.sub("", _FENCE.sub("", text.replace("\r\n", "\n")))
    # the template's five shape comments live in the front matter; markdown headings stay
    head, separator, body = prose.partition("\n+++\n") if prose.startswith("+++\n") else ("", "", prose)
    if separator:
        head = "\n".join(line for line in head.split("\n") if not line.lstrip().startswith("#"))
    prose = head + separator + body
    match = _PLACEHOLDER.search(prose)
    if match is not None:
        return "fail", f"{artifact.artifact_id} still carries the template placeholder {match.group(0)}."
    lines = prose.split("\n")
    for index, line in enumerate(lines):
        if line.strip() == "## Open decisions":
            body = next((item.strip() for item in lines[index + 1:] if item.strip() and not item.startswith("## ")), "")
            if body not in {"None", "None."}:
                return "fail", f"{artifact.artifact_id} has an open decision: {body[:120]}"
            break
    return "pass", f"{artifact.artifact_id} carries no placeholder and no open decision."


def release_unit_ready(artifact: Any, root: Path, catalog: Mapping[str, Any]) -> tuple[str, str]:
    """CIP-RLU: a release contract that names a candidate commit declares the census the history yields.

    A contract without `candidate_commit` is the retained allow-list form and passes. A contract
    with one is re-measured with `se_harness.release_unit`; every `E-CIP-001` finding fails it.
    An unavailable history (no git, no tag) is `not_assessable`, never a pass.
    """

    metadata = artifact.metadata
    if artifact.artifact_type != "release_contract":
        return "not_assessable", f"{artifact.artifact_id} is not a release contract."
    candidate = metadata.get("candidate_commit")
    if not isinstance(candidate, str) or not candidate:
        return "pass", f"{artifact.artifact_id} declares no candidate_commit; the allow-list form is not re-measured."
    previous_tag = metadata.get("previous_release_tag")
    if not isinstance(previous_tag, str) or not previous_tag:
        return "fail", f"E-CIP-001: {artifact.artifact_id} names candidate_commit but no previous_release_tag."
    section = metadata.get("release_unit", {})
    exemptions = section.get("untraced_exemptions", []) if isinstance(section, dict) else []
    if not isinstance(exemptions, list) or not all(isinstance(item, str) for item in exemptions):
        return "fail", f"E-CIP-001: {artifact.artifact_id} release_unit.untraced_exemptions must be an array of full commit ids."
    from se_harness.release_unit import PACKAGED_SURFACE_PREFIXES, compare_with_contract, derive_release_unit

    def lookup(work_order: str) -> tuple[str | None, bool | None]:
        entry = catalog.get(work_order)
        if entry is None:
            return None, None
        status = entry.metadata.get("status")
        scope = entry.metadata.get("execution_scope", {})
        paths = scope.get("paths", []) if isinstance(scope, dict) else []
        packaged = any(isinstance(item, str) and item.startswith(PACKAGED_SURFACE_PREFIXES) for item in paths)
        return (status if isinstance(status, str) else None), packaged

    try:
        unit = derive_release_unit(root, from_ref=previous_tag, to_ref=candidate, exempt=exemptions, lookup=lookup)
    except HarnessError as exc:
        return "not_assessable", f"{artifact.artifact_id}: the release unit cannot be derived here: {exc}"
    findings = compare_with_contract(unit, metadata)
    if findings:
        return "fail", f"{artifact.artifact_id}: " + " ".join(findings)
    return "pass", f"{artifact.artifact_id} gates equal the census derived over {previous_tag}..{unit.to_commit[:12]} ({len(unit.gates)} work orders)."


def ensure_governed_checkpoint(
    repository: Path,
    artifact_ids: Iterable[str],
    *,
    report: Any | None = None,
    catalog: Mapping[str, Any] | None = None,
) -> None:
    """Fail closed on contract or repository-integrity damage before a mutation."""

    root = ensure_target(repository, must_exist=True)
    try:
        load_validated_contracts()
    except ContractError as exc:
        raise HarnessError(f"WEX210: invalid machine policy: {exc}") from exc
    from se_harness.workflow import _catalog, _validation

    if report is None:
        _, report = _validation(root)
    if catalog is None:
        catalog = _catalog(report)
    for artifact_id in artifact_ids:
        if artifact_id not in catalog:
            raise HarnessError(f"WEX210: unknown governed artifact {artifact_id}")
    repository_errors = [item for item in report.errors if item.code in _REPOSITORY_ERROR_CODES]
    if repository_errors:
        raise HarnessError(f"WEX210: repository integrity prevents governed action: {repository_errors[0].message}")
    # The authoring and release-unit predicates a definition needs before it
    # leaves draft are evaluated by the contract's transition bindings
    # (QGP-G1/G2-AUTHORING, QGP-G5P-RELEASE-UNIT), not re-implemented here (WO-ECP-009).
