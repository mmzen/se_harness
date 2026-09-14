"""Prepare commit-bound verification and release records without granting authority."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Any


from se_harness.integrity import atomic_create_bytes
from se_harness import mutation_guard
from se_harness._process import run as _launch, text as _text
from se_harness.gate_source import DelegationError, authorize_delegated_right
from se_harness.artifact_layout import ID_PATTERN, common_artifact_domain, repository_record_relative_path, validate_domain
from se_harness.engine import validate_engineering_artifacts
from se_harness.installer import HarnessError, ensure_target, safe_destination
from se_harness.workflow_contract import IMPLEMENTED_OR_LATER_STATUSES, load_lifecycle_registry


VERSION_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]{0,63}$")
OWNER_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9@._ -]{0,127}$")
TAG_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/+-]{0,127}$")
LIFECYCLE_REGISTRY = load_lifecycle_registry()


class RecordRefusal(HarnessError):
    """A refused record preparation, labelled by its cause class (SPEC-ECP-016, ECP-CLI-007).

    The CLI maps the class to a code of `codes.VERIFICATION_RECORD_REFUSALS` or
    `codes.RELEASE_RECORD_REFUSALS`.
    """

    cause = "state"


class StateRefusal(RecordRefusal):
    cause = "state"


class ProvenanceRefusal(RecordRefusal):
    cause = "provenance"


class EvidenceRefusal(RecordRefusal):
    cause = "evidence"


class InputRefusal(RecordRefusal):
    cause = "inputs"



def _grants_authority(family: str, status: object) -> bool:
    row = LIFECYCLE_REGISTRY.get(family, {}).get(status) if isinstance(status, str) else None
    return bool(row and row.grants_authority)


def _reserves_version(status: object) -> bool:
    row = LIFECYCLE_REGISTRY["release_record"].get(status) if isinstance(status, str) else None
    return bool(row and row.reserves_version)


def _run(command: list[str], *, cwd: Path, refusal: type[RecordRefusal] = EvidenceRefusal) -> subprocess.CompletedProcess[str]:
    # ECP-PRM-001: the one launcher, decoded as UTF-8 so the record never depends on the locale.
    completed = _launch(
        command, cwd=cwd, timeout=30,
        error=lambda message: refusal(f"command failed to start safely: {command[0]}: {message}"),
    )
    return subprocess.CompletedProcess(completed.args, completed.returncode, _text(completed.stdout), _text(completed.stderr))


def _git(repository_root: Path, *arguments: str) -> str:
    executable = shutil.which("git")
    if executable is None:
        raise ProvenanceRefusal("Git is required for revision provenance")
    completed = _run([executable, "-C", str(repository_root), *arguments], cwd=repository_root, refusal=ProvenanceRefusal)
    if completed.returncode != 0:
        detail = completed.stderr.strip().splitlines()
        message = detail[0] if detail else "Git command failed"
        raise ProvenanceRefusal(message)
    return completed.stdout.strip()


def git_identity(repository_root: Path) -> tuple[str, str]:
    commit = _git(repository_root, "rev-parse", "HEAD").lower()
    try:
        object_format = _git(repository_root, "rev-parse", "--show-object-format").lower()
    except HarnessError:
        object_format = "sha1" if len(commit) == 40 else "sha256" if len(commit) == 64 else ""
    expected = 40 if object_format == "sha1" else 64 if object_format == "sha256" else 0
    if len(commit) != expected or re.fullmatch(r"[0-9a-f]+", commit) is None:
        raise ProvenanceRefusal("HEAD did not resolve to a supported full SHA-1 or SHA-256 commit")
    return commit, object_format


def require_clean_worktree(repository_root: Path) -> None:
    status = _git(repository_root, "status", "--porcelain", "--untracked-files=all")
    if status:
        raise ProvenanceRefusal("revision provenance requires a clean Git worktree")


def standing_deviations_for_work(root: Path, catalog: dict[str, Any], work_ids: list[str]) -> list[tuple[str, str]]:
    """(decision id, departed rule) for every accepted deviation standing on the selected work (SPEC-DCM-001 rule 9).

    Read from the validated artifacts' metadata (ECP-ENG-011): nothing is parsed again.
    """

    del root
    closed: set[str] = set()
    accepted: list[tuple[str, str, set[str]]] = []
    for item in catalog.values():
        if item.artifact_type != "decision" or item.status != "decided":
            continue
        metadata = item.metadata
        if metadata.get("kind") != "deviation":
            continue
        disposition = metadata.get("disposition") if isinstance(metadata.get("disposition"), dict) else {}
        against = metadata.get("against") if isinstance(metadata.get("against"), str) else ""
        relations = metadata.get("relations") if isinstance(metadata.get("relations"), dict) else {}
        concerned = {value for value in relations.get("concerns", []) if isinstance(value, str)} if isinstance(relations.get("concerns"), list) else set()
        option = disposition.get("option")
        if option in {"amend", "supersede"}:
            closed.add(against)
        elif option == "accept" and against:
            accepted.append((item.artifact_id, against, concerned))
    return sorted(
        (decision_id, against)
        for decision_id, against, concerned in accepted
        if against not in closed and concerned & set(work_ids)
    )


def _validation_catalog(repository_root: Path, report: Any | None = None,
                        selected_ids: list[str] | None = None) -> dict[str, Any]:
    from se_harness.repository_graph import artifact_catalog, classify_diagnostics
    validation = report if report is not None else validate_engineering_artifacts.validate_repository(repository_root)
    catalog = artifact_catalog(validation)
    errors = validation.errors
    if selected_ids is not None:
        errors = []
        for identifier in selected_ids:
            if identifier not in catalog:
                raise StateRefusal(f"unknown selected work order: {identifier}")
            scoped, global_errors, _ = classify_diagnostics(validation, catalog, catalog[identifier], repository_root)
            errors.extend(scoped + global_errors)
    if errors:
        first = errors[0]
        message = first["message"] if isinstance(first, dict) else first.message
        raise StateRefusal(f"artifact graph must be valid before recording provenance: {message}")
    return catalog



def _require_artifact(catalog: dict[str, Any], artifact_id: str, artifact_type: str) -> Any:
    artifact = catalog.get(artifact_id)
    if artifact is None:
        raise InputRefusal(f"unknown artifact ID: {artifact_id}")
    if artifact.artifact_type != artifact_type:
        raise InputRefusal(f"artifact {artifact_id} must have type {artifact_type}")
    return artifact


def _load_metadata(repository_root: Path, artifact: Any) -> dict[str, Any]:
    """The artifact's front matter as the validator parsed it (ECP-ENG-011): no second read."""

    del repository_root
    return dict(artifact.metadata)


def _relative_path(repository_root: Path, artifact: Any) -> str:
    try:
        return artifact.path.resolve().relative_to(repository_root.resolve()).as_posix()
    except ValueError:
        return artifact.path.as_posix()


def _relation_targets(metadata: dict[str, Any], name: str) -> set[str]:
    relations = metadata.get("relations", {})
    value = relations.get(name, []) if isinstance(relations, dict) else []
    return {item for item in value if isinstance(item, str)} if isinstance(value, list) else set()


def _validate_id(value: str, prefix: str) -> str:
    if ID_PATTERN.fullmatch(value) is None or not value.startswith(prefix):
        raise InputRefusal(f"record ID must use the {prefix} prefix and a three-digit suffix")
    return value


def _validate_owner(value: str) -> str:
    if OWNER_PATTERN.fullmatch(value) is None:
        raise InputRefusal("owner must use 1-128 letters, numbers, spaces, @, dots, underscores, or hyphens")
    return value


def _normalized_unique(values: str | list[str], label: str) -> list[str]:
    supplied = [values] if isinstance(values, str) else list(values)
    if not supplied or any(not isinstance(item, str) or not item.strip() for item in supplied):
        raise InputRefusal(f"{label} must contain at least one non-empty value")
    normalized = [item.strip() for item in supplied]
    seen: set[str] = set()
    duplicates: set[str] = set()
    for item in normalized:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    if duplicates:
        raise InputRefusal(f"{label} contains duplicate values: {', '.join(sorted(duplicates))}")
    return sorted(normalized)


def _toml_array(values: list[str]) -> str:
    return "[" + ", ".join(json.dumps(item) for item in values) + "]"





def _supported_commit(metadata: dict[str, Any], record_id: str) -> tuple[str, str]:
    commit = metadata.get("commit")
    object_format = metadata.get("git_object_format")
    expected = 40 if object_format == "sha1" else 64 if object_format == "sha256" else 0
    if not isinstance(commit, str) or len(commit) != expected or re.fullmatch(r"[0-9a-f]+", commit) is None:
        raise InputRefusal(f"verification record {record_id} does not contain a supported full commit")
    return commit, object_format


def _relative_file(repository_root: Path, value: str) -> tuple[Path, str]:
    raw = Path(value)
    if raw.is_absolute() or "\\" in value or ".." in raw.parts:
        raise InputRefusal("evidence must use a normalized repository-relative path")
    path = safe_destination(repository_root, raw)
    if not path.is_file():
        raise InputRefusal(f"evidence file does not exist: {value}")
    return path, raw.as_posix()


def _output_path(repository_root: Path, supplied: str | None, default: Path) -> Path:
    relative = Path(supplied) if supplied is not None else default
    if relative.is_absolute() or ".." in relative.parts:
        raise InputRefusal("record output must be a repository-relative path")
    if relative.suffix.lower() != ".md" or relative.parts[:2] != ("docs", "engineering"):
        raise InputRefusal("record output must be a Markdown file below docs/engineering")
    output = safe_destination(repository_root, relative)
    if output.exists():
        raise InputRefusal(f"record output already exists: {relative.as_posix()}")
    return output


def _record_domain(
    repository_root: Path,
    catalog: dict[str, Any],
    work_order_ids: list[str],
    explicit_domain: str | None,
) -> str | None:
    if explicit_domain is not None:
        try:
            return validate_domain(explicit_domain)
        except HarnessError as exc:
            raise InputRefusal(str(exc)) from exc
    paths: list[str] = []
    for work_order_id in work_order_ids:
        artifact = catalog.get(work_order_id)
        if artifact is None:
            return None
        paths.append(_relative_path(repository_root, artifact))
    return common_artifact_domain(paths)


def _atomic_write(path: Path, content: str) -> None:
    # ECP-PRM-008: the one create-once writer; a record is never overwritten.
    atomic_create_bytes(
        path,
        content.encode("utf-8"),
        exists=lambda: InputRefusal(f"record output already exists: {path}"),
        failed=lambda detail: InputRefusal(f"cannot create record output atomically: {detail}"),
    )


def _atomic_write_bytes(path: Path, content: bytes) -> None:
    atomic_create_bytes(
        path,
        content,
        exists=lambda: InputRefusal(f"evaluator evidence already exists: {path}"),
        failed=lambda detail: InputRefusal(f"cannot create evaluator evidence atomically: {detail}"),
    )


def _evaluator_evidence_output(
    repository_root: Path,
    record_id: str,
    domain: str | None,
) -> tuple[Path, str]:
    relative = Path("docs") / "engineering"
    if domain is not None:
        relative = relative / domain
    relative = relative / "evidence" / f"{record_id}-evaluator.json"
    destination = safe_destination(repository_root, relative)
    if destination.exists():
        raise InputRefusal(f"evaluator evidence already exists: {relative.as_posix()}")
    return destination, relative.as_posix()


def _evidence_digest(relative: str, content: bytes) -> str:
    from se_harness.evaluator_evidence import parse_evaluator_evidence
    return parse_evaluator_evidence(content).sha256




def _write_record_and_evidence(
    record: Path,
    content: str,
    evidence: Path,
    evidence_bytes: bytes,
) -> None:
    wrote_evidence = False
    try:
        _atomic_write_bytes(evidence, evidence_bytes)
        wrote_evidence = True
        _atomic_write(record, content)
    except BaseException as exc:
        if wrote_evidence:
            try:
                evidence.unlink()
            except OSError as cleanup_error:
                raise InputRefusal(
                    f"record creation failed and evaluator-evidence rollback was incomplete: {cleanup_error}"
                ) from exc
        raise


def _timestamp() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _generate_snapshot(repository_root: Path, report: Any, selected_ids: list[str]) -> str:
    from se_harness.workflow_change_set import formal_snapshot_digest
    return formal_snapshot_digest(repository_root, report.artifacts, selected_ids)


def _refresh_note(root: Path, catalog: dict[str, Any], source_id: str,
                  work: list[str], verification: list[str], evidence: list[str]) -> str:
    """Reuse a ready record only after comparing its relevant Git tree entries."""
    from se_harness.installer import load_lock
    from se_harness.repository_graph import project_scope
    from se_harness.workflow_change_set import execution_scope, own_record_paths, path_is_admitted

    source = _require_artifact(catalog, source_id, "verification_record")
    if source.status != "ready":
        raise StateRefusal("refresh requires a ready verification record; verified history is immutable")
    if (set(work) != _relation_targets(source.metadata, "verifies_work_order")
            or set(verification) != _relation_targets(source.metadata, "conforms_to")
            or set(evidence) != set(source.metadata.get("evidence_paths", []))):
        raise InputRefusal("refresh must retain the original work, contracts, and evidence selection")
    commit, _ = _supported_commit(source.metadata, source_id)
    current, _ = git_identity(root)
    scope = {".engineering-harness.toml", ".engineering-harness.lock", ".gitattributes",
             "AGENTS.md", "CLAUDE.md", "ENGINEERING_HARNESS.md", *load_lock(root)["files"], *evidence}
    outputs: set[str] = set()
    for identifier in work:
        artifact = catalog[identifier]
        governing, _ = project_scope(catalog, artifact)
        scope.update(_relative_path(root, catalog[item]) for item in {*governing, identifier})
        scope.update(execution_scope(artifact))
        outputs.update(own_record_paths(root, catalog, identifier))

    def entries(revision: str) -> dict[str, str]:
        rows = _git(root, "ls-tree", "-r", "-z", revision).split("\0")
        result = {}
        for row in rows:
            if not row:
                continue
            identity, path = row.split("\t", 1)
            if path_is_admitted(path, scope) and (path not in outputs or path in evidence):
                result[path] = identity  # mode, object type, and blob ID; no checkout newline conversion
        return result

    previous, latest = entries(commit), entries(current)
    changed = sorted(path for path in previous.keys() | latest.keys() if previous.get(path) != latest.get(path))
    if changed:
        raise EvidenceRefusal("relevant files changed; run fresh candidate tests: " + ", ".join(changed))
    return (f"\n\n## Evidence reused after explicit refresh\n\n"
            f"Source: `{source_id}` at `{commit}`. New candidate: `{current}`. "
            f"Compared {len(latest)} relevant Git tree entries, including governing inputs and retained evidence; all are unchanged. "
            "The original record and evidence were preserved. No tests were rerun and neither record was verified by this command.")



def capture_committed_verification(repository: Path, *, candidate_commit: str,
                                   test_command: list[str], **options: Any) -> Path:
    root = ensure_target(repository, must_exist=True)
    if not candidate_commit or candidate_commit.startswith("-") or not test_command:
        raise InputRefusal("an explicit candidate needs a commit and --test-command argv")
    mutation_guard.require_mutation_authority(root, operation="capture-verification")
    from se_harness.repository_graph import artifact_catalog
    caller_catalog = artifact_catalog(validate_engineering_artifacts.validate_repository(root))
    if options["record_id"] in caller_catalog:
        raise InputRefusal(f"artifact ID already exists: {options['record_id']}")
    options.pop("report", None)  # The temporary checkout gets its own validation.
    commit = _git(root, "rev-parse", "--verify", f"{candidate_commit}^{{commit}}")
    # Git creates and removes only this newly allocated temporary checkout.
    with tempfile.TemporaryDirectory(prefix="se-harness-candidate-") as directory:
        checkout = Path(directory).resolve() / "checkout"
        _git(root, "worktree", "add", "--detach", str(checkout), commit)
        try:
            checked = _launch(test_command, cwd=checkout, timeout=3600, error=EvidenceRefusal)
            if checked.returncode:
                raise EvidenceRefusal(f"candidate tests failed (exit {checked.returncode}): "
                                      + _text(checked.stderr or checked.stdout)[-2000:])
            # Test-created outputs must be ignored, not silently included in evidence.
            require_clean_worktree(checkout)
            record = capture_verification(checkout, **options)
            from se_harness.front_matter import parse
            metadata = parse(record.read_text(encoding="utf-8"))
            destination = _output_path(root, record.relative_to(checkout).as_posix(), record)
            evidence_relative = metadata["evaluator_evidence_path"]
            evidence_destination = safe_destination(root, Path(evidence_relative))
            content = record.read_text(encoding="utf-8")
            content += "\n## Candidate test run\n\nCommit: `" + commit + "`. Exit status: 0.\n\n"
            content += "Command arguments: `" + json.dumps(test_command) + "`.\n\n"
            content += "```text\n" + _text(checked.stdout + checked.stderr)[-6000:].replace("```", "~~~") + "\n```\n"
            evidence_bytes = (checkout / evidence_relative).read_bytes()
        finally:
            # The target is the allocated checkout, never a caller-supplied directory.
            checkout.resolve().relative_to(Path(directory).resolve())
            _git(root, "worktree", "remove", "--force", str(checkout))
    _write_record_and_evidence(destination, content, evidence_destination, evidence_bytes)
    return destination


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
    report: Any | None = None,
    refresh_from: str | None = None,
) -> Path:
    root = ensure_target(repository, must_exist=True)
    _validate_id(record_id, "VREC-")
    _validate_owner(owner)
    selected_work = _normalized_unique(work_order_ids, "work orders")
    selected_verification = _normalized_unique(verification_ids, "verification contracts")
    selected_evidence = _normalized_unique(evidence_paths, "evidence paths")
    authority = mutation_guard.require_mutation_authority(
        root,
        operation="capture-verification",
    )
    from se_harness.workflow_compliance import ensure_governed_checkpoint

    # ECP-ENG-010: one validation serves the governed checkpoint, the catalog and the snapshot;
    # the CLI hands in the one it took for the prepared result.
    report = report if report is not None else validate_engineering_artifacts.validate_repository(root)
    ensure_governed_checkpoint(root, selected_work, report=report)
    catalog = _validation_catalog(root, report, selected_work)
    if record_id in catalog:
        raise InputRefusal(f"artifact ID already exists: {record_id}")
    declared_verification: set[str] = set()
    for work_order_id in selected_work:
        work_order = _require_artifact(catalog, work_order_id, "work_order")
        if work_order.status not in IMPLEMENTED_OR_LATER_STATUSES:
            raise StateRefusal(f"work order {work_order_id} must be implemented, verified, or released")
        work_order_metadata = _load_metadata(root, work_order)
        declared_verification.update(_relation_targets(work_order_metadata, "verification"))
        try:
            authorize_delegated_right(
                root, work_order_metadata=work_order_metadata,
                work_order_path=work_order.path, right="DR-VREC-PREPARE",
            )
        except DelegationError as exc:
            raise StateRefusal(f"{exc.code}: {exc.message}") from exc
    for verification_id in selected_verification:
        verification = _require_artifact(catalog, verification_id, "verification")
        if not _grants_authority("definition", verification.status):
            raise StateRefusal(f"verification contract {verification_id} must be active")
    supplied_verification = set(selected_verification)
    missing_verification = declared_verification - supplied_verification
    extra_verification = supplied_verification - declared_verification
    if missing_verification or extra_verification:
        details: list[str] = []
        if missing_verification:
            details.append(f"missing {', '.join(sorted(missing_verification))}")
        if extra_verification:
            details.append(f"not declared by selected work {', '.join(sorted(extra_verification))}")
        raise InputRefusal(f"verification contract selection does not match selected work orders: {'; '.join(details)}")
    normalized_evidence = [_relative_file(root, evidence)[1] for evidence in selected_evidence]
    reuse_note = _refresh_note(root, catalog, refresh_from, selected_work, selected_verification, normalized_evidence) if refresh_from else ""
    selected_domain = _record_domain(root, catalog, selected_work, domain)
    destination = _output_path(
        root,
        output,
        repository_record_relative_path("verification_record", record_id, selected_domain),
    )
    evidence_destination, evaluator_evidence_path = _evaluator_evidence_output(
        root,
        record_id,
        selected_domain,
    )
    evidence_sha256 = _evidence_digest(evaluator_evidence_path, authority.evidence_bytes)
    require_clean_worktree(root)
    commit, object_format = git_identity(root)
    snapshot_hash = _generate_snapshot(root, report, selected_work)
    require_clean_worktree(root)
    now = _timestamp()
    title_scope = selected_work[0] if len(selected_work) == 1 else f"{len(selected_work)} work orders"
    evidence_array = _toml_array(normalized_evidence)
    work_array = _toml_array(selected_work)
    verification_array = _toml_array(selected_verification)
    readable_work = ", ".join(f"`{item}`" for item in selected_work)
    refresh_line = f'\nrefreshed_from = "{refresh_from}"' if refresh_from else ""
    deviations = standing_deviations_for_work(root, catalog, selected_work)
    deviation_section = (
        "\n\n## Standing deviations\n\nAccepted deviations standing on the selected work at this candidate; each names the rule it departs from and is retained here for the assurance decision:\n\n"
        + "\n".join(f"- `{decision_id}` against `{against}`" for decision_id, against in deviations)
        if deviations
        else ""
    )
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
prepared_at = "{now}"
prepared_by = "{owner}"
artifact_snapshot_sha256 = "{snapshot_hash}"
evidence_paths = {evidence_array}
evaluator_evidence_path = "{evaluator_evidence_path}"
evaluator_evidence_sha256 = "{evidence_sha256}"{refresh_line}

[relations]
verifies_work_order = {work_array}
conforms_to = {verification_array}
+++

# Verification Record Candidate

This ready record binds retained evidence for {readable_work} to candidate commit `{commit}`. Preparation uses each selected work order's recorded execution approval. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.{deviation_section}{reuse_note}
'''
    _write_record_and_evidence(
        destination,
        content,
        evidence_destination,
        authority.evidence_bytes,
    )
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
    report: Any | None = None,
) -> Path:
    root = ensure_target(repository, must_exist=True)
    _validate_id(record_id, "RLS-")
    _validate_owner(authorized_by)
    if VERSION_PATTERN.fullmatch(version) is None:
        raise InputRefusal("version must use 1-64 letters, numbers, dots, underscores, pluses, or hyphens")
    if tag is not None and TAG_PATTERN.fullmatch(tag) is None:
        raise InputRefusal("tag contains unsupported characters")
    selected_verification_records = _normalized_unique(verification_record_ids, "verification records")
    if len(selected_verification_records) != 1:
        raise InputRefusal("select one final-candidate verification record covering the complete release; earlier records remain supporting evidence")
    selected_work = _normalized_unique(work_order_ids, "work orders")
    authority = mutation_guard.require_mutation_authority(
        root,
        operation="prepare-release",
    )
    from se_harness.workflow_compliance import ensure_governed_checkpoint

    # ECP-ENG-010: one validation serves the governed checkpoint and the catalog; the CLI hands
    # in the one it took for the prepared result.
    report = report if report is not None else validate_engineering_artifacts.validate_repository(root)
    ensure_governed_checkpoint(root, [*selected_verification_records, *selected_work], report=report)
    catalog = _validation_catalog(root, report)
    if record_id in catalog:
        raise InputRefusal(f"artifact ID already exists: {record_id}")
    contract = _require_artifact(catalog, release_contract_id, "release_contract")
    if not _grants_authority("definition", contract.status):
        raise StateRefusal("release contract must be active")
    contract_metadata = _load_metadata(root, contract)
    for work_order_id in selected_work:
        work_order = _require_artifact(catalog, work_order_id, "work_order")
        if work_order.status not in IMPLEMENTED_OR_LATER_STATUSES:
            raise StateRefusal(f"work order {work_order_id} must be implemented, verified, or released")
    for artifact in catalog.values():
        if artifact.artifact_type != "release_record":
            continue
        existing_metadata = _load_metadata(root, artifact)
        if not _reserves_version(existing_metadata.get("status")):
            continue
        if existing_metadata.get("version") == version:
            raise InputRefusal(f"release version already exists: {version}")
    ungated = set(selected_work) - _relation_targets(contract_metadata, "gates")
    if ungated:
        raise InputRefusal(f"release contract {release_contract_id} does not gate work orders: {', '.join(sorted(ungated))}")
    verification_record_id = selected_verification_records[0]
    verification_record = _require_artifact(catalog, verification_record_id, "verification_record")
    if not _grants_authority("verification_record", verification_record.status):
        raise StateRefusal(f"verification record {verification_record_id} must be verified or released authority")
    verification_metadata = _load_metadata(root, verification_record)
    verification_work = _relation_targets(verification_metadata, "verifies_work_order")
    required_contracts = set().union(*(_relation_targets(catalog[item].metadata, "verification") for item in selected_work))
    if _relation_targets(verification_metadata, "conforms_to") != required_contracts:
        raise InputRefusal("the final verification must cover every verification contract declared by released work")
    commit, object_format = _supported_commit(verification_metadata, verification_record_id)
    if contract_metadata.get("candidate_commit", commit) != commit:
        raise InputRefusal("the final verification does not identify the release contract's candidate commit")
    released_work = set(selected_work)
    verified_only = verification_work - released_work
    released_only = released_work - verification_work
    if verified_only or released_only:
        details = []
        if verified_only:
            details.append(f"verified but not released {', '.join(sorted(verified_only))}")
        if released_only:
            details.append(f"released but not verified {', '.join(sorted(released_only))}")
        raise InputRefusal(f"released work does not match verification coverage: {'; '.join(details)}")
    selected_domain = _record_domain(root, catalog, selected_work, domain)
    destination = _output_path(
        root,
        output,
        repository_record_relative_path("release_record", record_id, selected_domain),
    )
    evidence_destination, evaluator_evidence_path = _evaluator_evidence_output(
        root,
        record_id,
        selected_domain,
    )
    evidence_sha256 = _evidence_digest(evaluator_evidence_path, authority.evidence_bytes)
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
prepared_at = "{now}"
prepared_by = "{authorized_by}"
evaluator_evidence_path = "{evaluator_evidence_path}"
evaluator_evidence_sha256 = "{evidence_sha256}"
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
    _write_record_and_evidence(
        destination,
        content,
        evidence_destination,
        authority.evidence_bytes,
    )
    return destination
