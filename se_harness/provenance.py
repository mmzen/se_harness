"""Prepare commit-bound verification and release records without granting authority."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import tomllib

from se_harness.artifact_layout import common_artifact_domain, repository_record_relative_path, validate_domain
from se_harness.installer import HarnessError, ensure_target, safe_destination, template_root


ID_PATTERN = re.compile(r"^[A-Z][A-Z0-9-]*-\d{3}$")
VERSION_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]{0,63}$")
OWNER_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9@._ -]{0,127}$")
TAG_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/+-]{0,127}$")
ACTIVE_STATUSES = {"approved", "in_progress", "implemented", "verified", "released"}
RELEASABLE_WORK_STATUSES = {"implemented", "verified", "released"}


def _run(command: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise HarnessError(f"command failed to start safely: {command[0]}: {exc}") from exc


def _git(repository_root: Path, *arguments: str) -> str:
    executable = shutil.which("git")
    if executable is None:
        raise HarnessError("Git is required for revision provenance")
    completed = _run([executable, "-C", str(repository_root), *arguments], cwd=repository_root)
    if completed.returncode != 0:
        detail = completed.stderr.strip().splitlines()
        message = detail[0] if detail else "Git command failed"
        raise HarnessError(message)
    return completed.stdout.strip()


def git_identity(repository_root: Path) -> tuple[str, str]:
    commit = _git(repository_root, "rev-parse", "HEAD").lower()
    try:
        object_format = _git(repository_root, "rev-parse", "--show-object-format").lower()
    except HarnessError:
        object_format = "sha1" if len(commit) == 40 else "sha256" if len(commit) == 64 else ""
    expected = 40 if object_format == "sha1" else 64 if object_format == "sha256" else 0
    if len(commit) != expected or re.fullmatch(r"[0-9a-f]+", commit) is None:
        raise HarnessError("HEAD did not resolve to a supported full SHA-1 or SHA-256 commit")
    return commit, object_format


def require_clean_worktree(repository_root: Path) -> None:
    status = _git(repository_root, "status", "--porcelain", "--untracked-files=all")
    if status:
        raise HarnessError("revision provenance requires a clean Git worktree")


def _validation_catalog(repository_root: Path) -> dict[str, dict[str, Any]]:
    script = template_root() / "scripts" / "validate_engineering_artifacts.py"
    if not script.is_file():
        raise HarnessError(f"missing managed validator: {script}")
    completed = _run([sys.executable, str(script), "--root", str(repository_root), "--json"], cwd=repository_root)
    try:
        report = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise HarnessError("validator did not return its JSON contract") from exc
    if completed.returncode != 0 or not report.get("valid"):
        errors = report.get("errors", [])
        first = errors[0].get("message") if errors and isinstance(errors[0], dict) else "artifact graph is invalid"
        raise HarnessError(f"artifact graph must be valid before recording provenance: {first}")
    return {
        item["id"]: item
        for item in report.get("artifacts", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }


def _require_artifact(catalog: dict[str, dict[str, Any]], artifact_id: str, artifact_type: str) -> dict[str, Any]:
    artifact = catalog.get(artifact_id)
    if artifact is None:
        raise HarnessError(f"unknown artifact ID: {artifact_id}")
    if artifact.get("type") != artifact_type:
        raise HarnessError(f"artifact {artifact_id} must have type {artifact_type}")
    return artifact


def _load_metadata(repository_root: Path, artifact: dict[str, Any]) -> dict[str, Any]:
    path = safe_destination(repository_root, Path(artifact["path"]))
    try:
        text = path.read_text(encoding="utf-8-sig")
        lines = text.splitlines()
        closing = lines.index("+++", 1)
        return tomllib.loads("\n".join(lines[1:closing]))
    except (OSError, UnicodeError, ValueError, tomllib.TOMLDecodeError) as exc:
        raise HarnessError(f"cannot read formal metadata for {artifact['id']}: {exc}") from exc


def _relation_targets(metadata: dict[str, Any], name: str) -> set[str]:
    relations = metadata.get("relations", {})
    value = relations.get(name, []) if isinstance(relations, dict) else []
    return {item for item in value if isinstance(item, str)} if isinstance(value, list) else set()


def _validate_id(value: str, prefix: str) -> str:
    if ID_PATTERN.fullmatch(value) is None or not value.startswith(prefix):
        raise HarnessError(f"record ID must use the {prefix} prefix and a three-digit suffix")
    return value


def _validate_owner(value: str) -> str:
    if OWNER_PATTERN.fullmatch(value) is None:
        raise HarnessError("owner must use 1-128 letters, numbers, spaces, @, dots, underscores, or hyphens")
    return value


def _normalized_unique(values: str | list[str], label: str) -> list[str]:
    supplied = [values] if isinstance(values, str) else list(values)
    if not supplied or any(not isinstance(item, str) or not item.strip() for item in supplied):
        raise HarnessError(f"{label} must contain at least one non-empty value")
    normalized = [item.strip() for item in supplied]
    seen: set[str] = set()
    duplicates: set[str] = set()
    for item in normalized:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    if duplicates:
        raise HarnessError(f"{label} contains duplicate values: {', '.join(sorted(duplicates))}")
    return sorted(normalized)


def _toml_array(values: list[str]) -> str:
    return "[" + ", ".join(json.dumps(item) for item in values) + "]"


def _evidence_is_keyed_to(evidence_path: str, work_order_id: str) -> bool:
    return re.match(rf"^{re.escape(work_order_id)}(?:-|\.|$)", Path(evidence_path).name) is not None


def _supported_commit(metadata: dict[str, Any], record_id: str) -> tuple[str, str]:
    commit = metadata.get("commit")
    object_format = metadata.get("git_object_format")
    expected = 40 if object_format == "sha1" else 64 if object_format == "sha256" else 0
    if not isinstance(commit, str) or len(commit) != expected or re.fullmatch(r"[0-9a-f]+", commit) is None:
        raise HarnessError(f"verification record {record_id} does not contain a supported full commit")
    return commit, object_format


def _relative_file(repository_root: Path, value: str) -> tuple[Path, str]:
    raw = Path(value)
    if raw.is_absolute() or "\\" in value or ".." in raw.parts:
        raise HarnessError("evidence must use a normalized repository-relative path")
    path = safe_destination(repository_root, raw)
    if not path.is_file():
        raise HarnessError(f"evidence file does not exist: {value}")
    return path, raw.as_posix()


def _output_path(repository_root: Path, supplied: str | None, default: Path) -> Path:
    relative = Path(supplied) if supplied is not None else default
    if relative.is_absolute() or ".." in relative.parts:
        raise HarnessError("record output must be a repository-relative path")
    if relative.suffix.lower() != ".md" or relative.parts[:2] != ("docs", "engineering"):
        raise HarnessError("record output must be a Markdown file below docs/engineering")
    output = safe_destination(repository_root, relative)
    if output.exists():
        raise HarnessError(f"record output already exists: {relative.as_posix()}")
    return output


def _record_domain(
    catalog: dict[str, dict[str, Any]],
    work_order_ids: list[str],
    explicit_domain: str | None,
) -> str | None:
    if explicit_domain is not None:
        return validate_domain(explicit_domain)
    paths: list[str] = []
    for work_order_id in work_order_ids:
        artifact = catalog.get(work_order_id)
        path = artifact.get("path") if isinstance(artifact, dict) else None
        if not isinstance(path, str):
            return None
        paths.append(path)
    return common_artifact_domain(paths)


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(temporary_name, path)
        except FileExistsError as exc:
            raise HarnessError(f"record output already exists: {path}") from exc
        except OSError as exc:
            raise HarnessError(f"cannot create record output atomically: {exc}") from exc
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)


def _timestamp() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _generate_snapshot(repository_root: Path) -> str:
    script = template_root() / "scripts" / "generate_harness_dashboard.py"
    if not script.is_file():
        raise HarnessError(f"missing managed dashboard generator: {script}")
    completed = _run([sys.executable, str(script), "--root", str(repository_root)], cwd=repository_root)
    if completed.returncode != 0:
        raise HarnessError("dashboard generation must pass before recording verification")
    snapshot = repository_root / "target" / "harness-dashboard" / "dashboard-data.json"
    if not snapshot.is_file():
        raise HarnessError("dashboard generator did not create dashboard-data.json")
    return hashlib.sha256(snapshot.read_bytes()).hexdigest()


def capture_verification(
    repository: Path,
    *,
    record_id: str,
    work_order_ids: list[str] | str,
    verification_ids: list[str] | str,
    evidence_paths: list[str] | str,
    owner: str,
    output: str | None,
    domain: str | None = None,
) -> Path:
    root = ensure_target(repository, must_exist=True)
    _validate_id(record_id, "VREC-")
    _validate_owner(owner)
    selected_work = _normalized_unique(work_order_ids, "work orders")
    selected_verification = _normalized_unique(verification_ids, "verification contracts")
    selected_evidence = _normalized_unique(evidence_paths, "evidence paths")
    catalog = _validation_catalog(root)
    if record_id in catalog:
        raise HarnessError(f"artifact ID already exists: {record_id}")
    declared_verification: set[str] = set()
    for work_order_id in selected_work:
        work_order = _require_artifact(catalog, work_order_id, "work_order")
        if work_order.get("status") not in ACTIVE_STATUSES:
            raise HarnessError(f"work order {work_order_id} must be active")
        declared_verification.update(_relation_targets(_load_metadata(root, work_order), "verification"))
    for verification_id in selected_verification:
        verification = _require_artifact(catalog, verification_id, "verification")
        if verification.get("status") not in ACTIVE_STATUSES:
            raise HarnessError(f"verification contract {verification_id} must be active")
    supplied_verification = set(selected_verification)
    missing_verification = declared_verification - supplied_verification
    extra_verification = supplied_verification - declared_verification
    if (len(selected_work) > 1 and missing_verification) or extra_verification:
        details: list[str] = []
        if len(selected_work) > 1 and missing_verification:
            details.append(f"missing {', '.join(sorted(missing_verification))}")
        if extra_verification:
            details.append(f"not declared by selected work {', '.join(sorted(extra_verification))}")
        raise HarnessError(f"verification contract selection does not match selected work orders: {'; '.join(details)}")
    normalized_evidence = [_relative_file(root, evidence)[1] for evidence in selected_evidence]
    if len(selected_work) > 1:
        uncovered = [
            work_order_id
            for work_order_id in selected_work
            if not any(_evidence_is_keyed_to(evidence, work_order_id) for evidence in normalized_evidence)
        ]
        if uncovered:
            raise HarnessError(f"aggregate evidence is not keyed to work orders: {', '.join(uncovered)}")
    selected_domain = _record_domain(catalog, selected_work, domain)
    destination = _output_path(
        root,
        output,
        repository_record_relative_path("verification_record", record_id, selected_domain),
    )
    require_clean_worktree(root)
    commit, object_format = git_identity(root)
    snapshot_hash = _generate_snapshot(root)
    require_clean_worktree(root)
    now = _timestamp()
    title_scope = selected_work[0] if len(selected_work) == 1 else f"{len(selected_work)} work orders"
    evidence_array = _toml_array(normalized_evidence)
    work_array = _toml_array(selected_work)
    verification_array = _toml_array(selected_verification)
    readable_work = ", ".join(f"`{item}`" for item in selected_work)
    content = f'''+++
id = "{record_id}"
type = "verification_record"
title = "Verification candidate for {title_scope}"
status = "ready"
owners = ["{owner}"]
created = "{now[:10]}"
updated = "{now[:10]}"
commit = "{commit}"
git_object_format = "{object_format}"
worktree_state = "clean"
verified_at = "{now}"
artifact_snapshot_sha256 = "{snapshot_hash}"
evidence_paths = {evidence_array}

[relations]
verifies_work_order = {work_array}
conforms_to = {verification_array}
+++

# Verification Record Candidate

This ready record binds retained evidence for {readable_work} to candidate commit `{commit}`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.
'''
    _atomic_write(destination, content)
    return destination


def prepare_release(
    repository: Path,
    *,
    record_id: str,
    release_contract_id: str,
    verification_record_ids: list[str] | str,
    work_order_ids: list[str] | str,
    version: str,
    authorized_by: str,
    tag: str | None,
    output: str | None,
    domain: str | None = None,
) -> Path:
    root = ensure_target(repository, must_exist=True)
    _validate_id(record_id, "RLS-")
    _validate_owner(authorized_by)
    if VERSION_PATTERN.fullmatch(version) is None:
        raise HarnessError("version must use 1-64 letters, numbers, dots, underscores, pluses, or hyphens")
    if tag is not None and TAG_PATTERN.fullmatch(tag) is None:
        raise HarnessError("tag contains unsupported characters")
    selected_verification_records = _normalized_unique(verification_record_ids, "verification records")
    selected_work = _normalized_unique(work_order_ids, "work orders")
    catalog = _validation_catalog(root)
    if record_id in catalog:
        raise HarnessError(f"artifact ID already exists: {record_id}")
    contract = _require_artifact(catalog, release_contract_id, "release_contract")
    if contract.get("status") not in ACTIVE_STATUSES:
        raise HarnessError("release contract must be active")
    contract_metadata = _load_metadata(root, contract)
    for work_order_id in selected_work:
        work_order = _require_artifact(catalog, work_order_id, "work_order")
        if work_order.get("status") not in RELEASABLE_WORK_STATUSES:
            raise HarnessError(f"work order {work_order_id} must be implemented, verified, or released")
    for artifact in catalog.values():
        if artifact.get("type") != "release_record":
            continue
        existing_metadata = _load_metadata(root, artifact)
        if existing_metadata.get("version") == version:
            raise HarnessError(f"release version already exists: {version}")
    ungated = set(selected_work) - _relation_targets(contract_metadata, "gates")
    if ungated:
        raise HarnessError(f"release contract {release_contract_id} does not gate work orders: {', '.join(sorted(ungated))}")
    verification_work: set[str] = set()
    identities: set[tuple[str, str]] = set()
    for verification_record_id in selected_verification_records:
        verification_record = _require_artifact(catalog, verification_record_id, "verification_record")
        if verification_record.get("status") not in {"ready", "verified", "released"}:
            raise HarnessError(f"verification record {verification_record_id} must be ready, verified, or released")
        verification_metadata = _load_metadata(root, verification_record)
        verification_work.update(_relation_targets(verification_metadata, "verifies_work_order"))
        identities.add(_supported_commit(verification_metadata, verification_record_id))
    released_work = set(selected_work)
    verified_only = verification_work - released_work
    released_only = released_work - verification_work
    if verified_only or released_only:
        details = []
        if verified_only:
            details.append(f"verified but not released {', '.join(sorted(verified_only))}")
        if released_only:
            details.append(f"released but not verified {', '.join(sorted(released_only))}")
        raise HarnessError(f"released work does not match verification coverage: {'; '.join(details)}")
    if len(identities) != 1:
        raise HarnessError("included verification records do not identify one candidate commit and object format")
    commit, object_format = next(iter(identities))
    selected_domain = _record_domain(catalog, selected_work, domain)
    destination = _output_path(
        root,
        output,
        repository_record_relative_path("release_record", record_id, selected_domain),
    )
    require_clean_worktree(root)
    now = _timestamp()
    tag_line = f'tag = "{tag}"\n' if tag is not None else ""
    verification_array = _toml_array(selected_verification_records)
    work_array = _toml_array(selected_work)
    readable_work = ", ".join(f"`{item}`" for item in selected_work)
    content = f'''+++
id = "{record_id}"
type = "release_record"
title = "Release candidate {version}"
status = "ready"
owners = ["{authorized_by}"]
created = "{now[:10]}"
updated = "{now[:10]}"
version = "{version}"
commit = "{commit}"
git_object_format = "{object_format}"
released_at = "{now}"
authorized_by = "{authorized_by}"
{tag_line}
[relations]
satisfies = ["{release_contract_id}"]
includes_verification = {verification_array}
releases_work = {work_array}
+++

# Release Record Candidate

This ready record proposes release `{version}` for {readable_work} from candidate commit `{commit}`. An accountable release owner must review and transition it to `released`; this command did not approve, commit, tag, release, or publish anything.

The release candidate commit may precede the governance commit retaining this record. Any release tag must be created and checked by the authorized release process.
'''
    _atomic_write(destination, content)
    return destination
