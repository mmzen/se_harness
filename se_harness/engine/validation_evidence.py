"""The evidence seam: record identity, timestamps, evidence paths, the evaluator-evidence binding and the type-specific metadata pass.
"""

from __future__ import annotations

import json
import re
from dataclasses import field
from datetime import datetime
from pathlib import Path, PurePosixPath

from se_harness.codes import E005, E009, E012
from se_harness.evaluator_evidence import (
    EvaluatorEvidenceError,
    MAX_EVIDENCE_BYTES,
    canonical_evidence_bytes,
    normalize_evaluator_identity,
    unique_evidence_object,
    validate_evaluator_evidence,
)
from se_harness.integrity import raw_sha256
from se_harness.engine.validation_core import (
    Artifact,
    Diagnostic,
    add_error,
    require_non_empty_string,
    require_non_empty_string_list,
)
from se_harness.engine.validation_lifecycle import WORKFLOW_LIFECYCLES


EVIDENCE_WORK_ORDER_PATTERN = re.compile(
    r"^(WO-(?:[A-Z0-9-]*-)?\d{3})(?:-|\.|$)"
)


SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


# The legacy release-evidence declaration mechanism (SPEC-LRE-001) was retired
# under WO-LRE-002 (the evaluator-evidence floor, owner decision of 2026-08-30):
# a released record carrying neither evaluator-evidence field is not assessed.
# The diagnostic code W024 is retired and stays reserved, never reused.
GIT_COMMIT_PATTERNS = {
    "sha1": re.compile(r"^[0-9a-f]{40}$"),
    "sha256": re.compile(r"^[0-9a-f]{64}$"),
}


def evidence_work_order_keys(evidence_path: str) -> tuple[str, ...]:
    """Extract exact work-order keys from a normalized repository path."""
    parts = PurePosixPath(evidence_path).parts
    if not parts:
        return ()
    candidates = [parts[-1]]
    if "evidence" in parts:
        candidates.extend(parts[parts.index("evidence") + 1 :])
    keys = {
        match.group(1)
        for component in candidates
        if (match := EVIDENCE_WORK_ORDER_PATTERN.match(component)) is not None
    }
    return tuple(sorted(keys))


def evidence_path_is_keyed_to(evidence_path: str, work_order_id: str) -> bool:
    return work_order_id in evidence_work_order_keys(evidence_path)


def _validate_git_identity(
    artifact: Artifact,
    errors: list[Diagnostic],
    report_root: Path,
) -> tuple[str | None, str | None]:
    commit = require_non_empty_string(
        artifact, "commit", errors, report_root, plane="governance"
    )
    object_format = require_non_empty_string(
        artifact, "git_object_format", errors, report_root, plane="governance"
    )
    if object_format is not None and object_format not in GIT_COMMIT_PATTERNS:
        add_error(
            errors,
            artifact,
            report_root,
            E009,
            "field 'git_object_format' must be 'sha1' or 'sha256'",
            plane="governance",
        )
    elif commit is not None and object_format is not None and not GIT_COMMIT_PATTERNS[object_format].fullmatch(commit):
        add_error(
            errors,
            artifact,
            report_root,
            E009,
            f"field 'commit' must be a full lowercase {object_format} Git object ID",
            plane="governance",
        )
    return commit, object_format


def _validate_timestamp(
    artifact: Artifact,
    field: str,
    errors: list[Diagnostic],
    report_root: Path,
) -> None:
    value = require_non_empty_string(
        artifact, field, errors, report_root, plane="governance"
    )
    if value is not None:
        try:
            datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            add_error(
                errors,
                artifact,
                report_root,
                E009,
                f"field '{field}' must use a valid YYYY-MM-DDTHH:MM:SSZ timestamp",
                plane="governance",
            )


def _validate_evidence_paths(
    artifact: Artifact,
    errors: list[Diagnostic],
    repository_root: Path,
) -> None:
    paths = require_non_empty_string_list(
        artifact,
        "evidence_paths",
        errors,
        repository_root,
        plane="governance",
    )
    if paths is None:
        return
    resolved_root = repository_root.resolve()
    for raw_path in paths:
        relative = Path(raw_path)
        if relative.is_absolute() or "\\" in raw_path or any(part in {"", ".", ".."} for part in relative.parts):
            add_error(
                errors,
                artifact,
                repository_root,
                E012,
                f"evidence path must be a normalized repository-relative path: '{raw_path}'",
                plane="governance",
            )
            continue
        candidate = repository_root / relative
        probe = repository_root
        symlinked = False
        for part in relative.parts:
            probe = probe / part
            if probe.is_symlink():
                symlinked = True
                break
        try:
            resolved = candidate.resolve()
            resolved.relative_to(resolved_root)
        except (OSError, ValueError):
            add_error(
                errors,
                artifact,
                repository_root,
                E012,
                f"evidence path escapes the repository: '{raw_path}'",
                plane="governance",
            )
            continue
        if symlinked:
            add_error(
                errors,
                artifact,
                repository_root,
                E012,
                f"evidence path must not traverse a symlink: '{raw_path}'",
                plane="governance",
            )
        elif not candidate.is_file():
            add_error(
                errors,
                artifact,
                repository_root,
                E012,
                f"evidence path does not identify an existing file: '{raw_path}'",
                plane="governance",
            )


def _evaluator_binding_error(
    artifact: Artifact,
    errors: list[Diagnostic],
    repository_root: Path,
    message: str,
) -> None:
    add_error(errors, artifact, repository_root, E012, message, plane="governance")


#: ECP-ENG-006: the engine's E012 message for each reason the one evidence validator raises.
EVIDENCE_MESSAGES = {
    "field_set": "evaluator evidence field set is not canonical",
    "schema": "evaluator evidence schema or role is invalid",
    "role": "evaluator evidence schema or role is invalid",
    "identity_field_set": "evaluator identity field set is not canonical",
    "payload_manifest": "evaluator payload manifest is unsupported",
    "version": "evaluator version is invalid",
    "payload_sha256": "evaluator payload digest is invalid",
    "archive_pair": "evaluator archive fields must appear together",
    "archive_name": "evaluator archive identity is invalid",
    "archive_sha256": "evaluator archive identity is invalid",
    "archive_required": "release evaluator evidence requires an archive name and SHA-256",
    "origins_field_set": "evaluator origins are not canonical",
    "origin": "evaluator origins are not canonical",
    "environment_field_set": "evaluator environment proof is invalid",
    "environment_boolean": "evaluator environment proof is invalid",
    "isolated_python": "evaluator environment proof is invalid",
    "user_site": "evaluator environment proof is invalid",
    "pythonpath": "evaluator environment proof is invalid",
    "entry_point": "evaluator environment proof is invalid",
    "checkout": "evaluator environment proof is invalid",
    "diagnostics": "evaluator environment proof is invalid",
    "lock": "evaluator evidence differs from the standard lock",
}


def _validate_evaluator_evidence_binding(
    artifact: Artifact,
    errors: list[Diagnostic],
    repository_root: Path,
    *,
    required: bool,
    require_archive: bool = False,
    match_current_lock: bool = True,
) -> None:
    raw_path = artifact.metadata.get("evaluator_evidence_path")
    raw_digest = artifact.metadata.get("evaluator_evidence_sha256")
    if raw_path is None and raw_digest is None and not required:
        return
    if not isinstance(raw_path, str) or not raw_path:
        _evaluator_binding_error(
            artifact, errors, repository_root, "field 'evaluator_evidence_path' must be a non-empty string"
        )
        return
    if not isinstance(raw_digest, str) or SHA256_PATTERN.fullmatch(raw_digest) is None:
        _evaluator_binding_error(
            artifact,
            errors,
            repository_root,
            "field 'evaluator_evidence_sha256' must be a lowercase SHA-256 value",
        )
        return
    relative = Path(raw_path)
    if (
        relative.is_absolute()
        or "\\" in raw_path
        or any(part in {"", ".", ".."} for part in relative.parts)
        or relative.suffix != ".json"
        or relative.parts[:2] != ("docs", "engineering")
        or "evidence" not in relative.parts
    ):
        _evaluator_binding_error(
            artifact, errors, repository_root, "evaluator evidence path must be normalized and repository-relative"
        )
        return
    candidate = repository_root / relative
    probe = repository_root
    for part in relative.parts:
        probe = probe / part
        if probe.is_symlink():
            _evaluator_binding_error(
                artifact, errors, repository_root, "evaluator evidence path must not traverse a symlink"
            )
            return
    try:
        candidate.resolve().relative_to(repository_root.resolve())
        raw = candidate.read_bytes()
    except (OSError, ValueError):
        _evaluator_binding_error(
            artifact, errors, repository_root, "evaluator evidence path is unavailable or escapes the repository"
        )
        return
    if not raw or len(raw) > MAX_EVIDENCE_BYTES:
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator evidence size is invalid")
        return
    if raw_sha256(raw) != raw_digest:
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator evidence digest does not match its bytes")
        return
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_evidence_object)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        _evaluator_binding_error(artifact, errors, repository_root, f"invalid evaluator evidence JSON: {exc}")
        return
    canonical = canonical_evidence_bytes(value)
    if raw != canonical or not isinstance(value, dict):
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator evidence bytes are not canonical")
        return
    # ECP-ENG-006: one validator of the document; the engine renders its own message per reason.
    try:
        validate_evaluator_evidence(value, require_archive=require_archive, require_isolated_python=True)
    except EvaluatorEvidenceError as exc:
        _evaluator_binding_error(artifact, errors, repository_root, EVIDENCE_MESSAGES.get(exc.reason, str(exc)))
        return
    if not match_current_lock:
        return
    try:
        lock = json.loads(
            (repository_root / ".engineering-harness.lock").read_text(encoding="utf-8"),
            object_pairs_hook=unique_evidence_object,
        )
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        _evaluator_binding_error(artifact, errors, repository_root, f"cannot read standard evaluator lock: {exc}")
        return
    expected_evaluator = lock.get("evaluator") if isinstance(lock, dict) and lock.get("schema") == 3 else None
    expected_fields = {"version", "payload_manifest", "payload_sha256", "archive_name", "archive_sha256"}
    if (
        not isinstance(expected_evaluator, dict)
        or set(expected_evaluator) - expected_fields
        or lock.get("tool_version") != expected_evaluator.get("version")
    ):
        _evaluator_binding_error(artifact, errors, repository_root, "standard evaluator lock identity is invalid")
        return
    if value["evaluator"] != normalize_evaluator_identity(expected_evaluator):
        _evaluator_binding_error(artifact, errors, repository_root, EVIDENCE_MESSAGES["lock"])


def validate_type_specific_metadata(artifacts: list[Artifact], report_root: Path) -> list[Diagnostic]:
    errors: list[Diagnostic] = []

    relation_requirements: dict[str, tuple[str, ...]] = {
        "capability": ("derives_from",),
        "requirement": ("derives_from",),
        "specification": ("specifies",),
        "architecture": (),
        "adr": ("decides",),
        "verification": ("verifies",),
        "work_order": ("implements", "specifications", "verification"),
        "release_contract": ("gates",),
        "verification_record": ("verifies_work_order", "conforms_to"),
        "release_record": ("satisfies", "includes_verification", "releases_work"),
        "operating_contract": ("assures",),
        "decision": ("concerns", "blocks"),
        "risk": ("threatens",),
    }

    for artifact in artifacts:
        artifact_type = artifact.metadata.get("type")
        if not isinstance(artifact_type, str):
            continue

        if artifact_type == "requirement":
            statement = require_non_empty_string(artifact, "statement", errors, report_root)
            if not isinstance(artifact.metadata.get("verification_method"), list):
                require_non_empty_string(artifact, "verification_method", errors, report_root)
            if statement is not None and re.search(r"\bSHALL\b", statement) is None:
                add_error(
                    errors,
                    artifact,
                    report_root,
                    E005,
                    "requirement statement must contain normative keyword SHALL",
                    plane="structure",
                )

        if artifact_type == "verification_record":
            _validate_git_identity(artifact, errors, report_root)
            worktree_state = require_non_empty_string(
                artifact, "worktree_state", errors, report_root, plane="governance"
            )
            if worktree_state is not None and worktree_state != "clean":
                add_error(
                    errors,
                    artifact,
                    report_root,
                    E009,
                    "field 'worktree_state' must be 'clean'",
                    plane="governance",
                )
            prepared = "prepared_at" in artifact.metadata or "prepared_by" in artifact.metadata
            if prepared:
                _validate_timestamp(artifact, "prepared_at", errors, report_root)
                require_non_empty_string(artifact, "prepared_by", errors, report_root, plane="governance")
            if artifact.status in {"verified", "released"}:
                _validate_timestamp(artifact, "verified_at", errors, report_root)
                if prepared:
                    require_non_empty_string(artifact, "verified_by", errors, report_root, plane="governance")
            elif artifact.status == "superseded":
                if prepared:
                    for field_name in ("verified_at", "verified_by"):
                        if field_name in artifact.metadata:
                            add_error(
                                errors, artifact, report_root, E009,
                                f"prepared superseded verification_record must omit decision field '{field_name}'",
                                plane="governance",
                            )
                else:
                    _validate_timestamp(artifact, "verified_at", errors, report_root)
            snapshot_hash = require_non_empty_string(
                artifact,
                "artifact_snapshot_sha256",
                errors,
                report_root,
                plane="governance",
            )
            if snapshot_hash is not None and not SHA256_PATTERN.fullmatch(snapshot_hash):
                add_error(
                    errors,
                    artifact,
                    report_root,
                    E009,
                    "field 'artifact_snapshot_sha256' must be a lowercase SHA-256 value",
                    plane="governance",
            )
            _validate_evidence_paths(artifact, errors, report_root)
            _validate_evaluator_evidence_binding(
                artifact,
                errors,
                report_root,
                required=False,
                match_current_lock=artifact.status == "ready",
            )
            if artifact.status not in WORKFLOW_LIFECYCLES["verification_record"]:
                add_error(
                    errors,
                    artifact,
                    report_root,
                    E009,
                    "verification_record status is not declared by the workflow lifecycle registry",
                    plane="governance",
                )
            if artifact.status == "ready" and prepared:
                for field_name in ("verified_at", "verified_by"):
                    if field_name in artifact.metadata:
                        add_error(
                            errors, artifact, report_root, E009,
                            f"ready verification_record must omit decision field '{field_name}'",
                            plane="governance",
                        )
            if artifact.status == "rejected":
                _validate_timestamp(artifact, "rejected_at", errors, report_root)
                require_non_empty_string(artifact, "rejected_by", errors, report_root, plane="governance")
                require_non_empty_string(artifact, "rejection_reason", errors, report_root, plane="governance")
            if artifact.status == "superseded":
                _validate_timestamp(artifact, "superseded_at", errors, report_root)
                require_non_empty_string(artifact, "supersession_authorized_by", errors, report_root)
                successors = require_non_empty_string_list(
                    artifact,
                    "superseded_by",
                    errors,
                    report_root,
                    code=E009,
                    container=artifact.relations,
                    plane="governance",
                )
                if successors is not None and len(successors) != 1:
                    add_error(
                        errors,
                        artifact,
                        report_root,
                        E009,
                        "relation 'superseded_by' must contain exactly one verification record",
                        plane="governance",
                    )
            else:
                for field_name in ("superseded_at", "supersession_authorized_by"):
                    if field_name in artifact.metadata:
                        add_error(
                            errors,
                            artifact,
                            report_root,
                            E009,
                            f"field '{field_name}' is allowed only when verification_record status is superseded",
                            plane="governance",
                        )
                if "superseded_by" in artifact.relations:
                    add_error(
                        errors,
                        artifact,
                        report_root,
                        E009,
                        "relation 'superseded_by' is allowed only when verification_record status is superseded",
                        plane="governance",
                    )

        if artifact_type == "release_record":
            _validate_git_identity(artifact, errors, report_root)
            require_non_empty_string(artifact, "version", errors, report_root, plane="governance")
            prepared = "prepared_at" in artifact.metadata or "prepared_by" in artifact.metadata
            if prepared:
                _validate_timestamp(artifact, "prepared_at", errors, report_root)
                require_non_empty_string(artifact, "prepared_by", errors, report_root, plane="governance")
            authorized_by: str | None = None
            if artifact.status == "released":
                _validate_timestamp(artifact, "released_at", errors, report_root)
                authorized_by = require_non_empty_string(
                    artifact, "authorized_by", errors, report_root, plane="governance"
                )
            owners = artifact.metadata.get("owners", [])
            if authorized_by is not None and isinstance(owners, list) and authorized_by not in owners:
                add_error(
                    errors,
                    artifact,
                    report_root,
                    E009,
                    "field 'authorized_by' must identify one of the record owners",
                    plane="governance",
                )
            tag = artifact.metadata.get("tag")
            if tag is not None and (not isinstance(tag, str) or not tag.strip()):
                add_error(
                    errors,
                    artifact,
                    report_root,
                    E009,
                    "field 'tag' must be a non-empty string when present",
                    plane="governance",
                )
            if artifact.status == "ready" and prepared:
                for field_name in ("released_at", "authorized_by"):
                    if field_name in artifact.metadata:
                        add_error(
                            errors, artifact, report_root, E009,
                            f"ready release_record must omit decision field '{field_name}'",
                            plane="governance",
                        )
            if artifact.status == "rejected":
                _validate_timestamp(artifact, "rejected_at", errors, report_root)
                require_non_empty_string(artifact, "rejected_by", errors, report_root, plane="governance")
                require_non_empty_string(artifact, "rejection_reason", errors, report_root, plane="governance")
            if artifact.status not in WORKFLOW_LIFECYCLES["release_record"]:
                add_error(
                    errors,
                    artifact,
                    report_root,
                    E009,
                    "release_record status is not declared by the workflow lifecycle registry",
                    plane="governance",
                )
            # REQ-LRE-003 (the evaluator-evidence floor, owner decision of
            # 2026-08-30, WO-LRE-002): a released record carrying neither
            # evidence field is not assessed against the binding. A partially
            # bound record keeps its existing error.
            unbound = (
                artifact.status == "released"
                and artifact.metadata.get("evaluator_evidence_path") is None
                and artifact.metadata.get("evaluator_evidence_sha256") is None
            )
            _validate_evaluator_evidence_binding(
                artifact,
                errors,
                report_root,
                required=not unbound,
                require_archive=True,
                match_current_lock=artifact.status == "ready",
            )

        if artifact_type == "work_order" and "architecture" in artifact.relations:
            require_non_empty_string_list(
                artifact,
                "architecture",
                errors,
                report_root,
                code=E005,
                container=artifact.relations,
            )

        required_relations = relation_requirements.get(artifact_type, ())
        relations = artifact.metadata.get("relations", {})
        if not isinstance(relations, dict):
            continue
        for relation_name in required_relations:
            require_non_empty_string_list(
                artifact,
                relation_name,
                errors,
                report_root,
                code=E005,
                container=relations,
            )

    return errors
