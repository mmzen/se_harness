"""Contract-bound preparation of one predecessor-format release record.

The operational repository can contain lifecycle syntax that the immutable
predecessor evaluator does not understand.  This module derives one exact
closed rejected bootstrap pair, omits only that pair from an isolated local
clone, and lets the predecessor generate the successor RLS.  It never grants a
release decision and never changes the operational root evaluator.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass, replace
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

from repository_tools import release_bootstrap as bootstrap


EVIDENCE_SCHEMA = "se-harness-predecessor-preparation-view-v1"
VIEW_BINDING_FIELDS = (
    "preparation_view_evidence_path",
    "preparation_view_evidence_sha256",
)
COMMIT_PATTERNS = {
    "sha1": re.compile(r"[0-9a-f]{40}"),
    "sha256": re.compile(r"[0-9a-f]{64}"),
}
RELEASABLE_WORK_STATUSES = frozenset({"implemented", "verified", "released"})
MAX_EVIDENCE_BYTES = 128 * 1024
MAX_PROCESS_SECONDS = 180


class PredecessorPreparationError(RuntimeError):
    """A predecessor preparation input or observation violates the contract."""


@dataclass(frozen=True)
class HistoryDescriptor:
    artifact_id: str
    artifact_type: str
    status: str
    path: str
    git_blob: str
    bytes: int
    sha256: str


@dataclass(frozen=True)
class PreparationPlan:
    schema: str
    source_commit: str
    source_tree: str
    git_object_format: str
    candidate_commit: str
    release_contract: str
    release_record: str
    version: str
    verification_records: tuple[str, ...]
    work_orders: tuple[str, ...]
    omitted_history: tuple[HistoryDescriptor, ...]
    sparse_spec_sha256: str
    predecessor_output_sha256: str
    preparation_view_evidence_path: str
    preparation_view_evidence_sha256: str
    release_record_path: str
    changed: bool
    applied: bool

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["verification_records"] = list(self.verification_records)
        value["work_orders"] = list(self.work_orders)
        value["omitted_history"] = [asdict(item) for item in self.omitted_history]
        return value


@dataclass(frozen=True)
class _Prepared:
    root: Path
    record_path: Path
    record_bytes: bytes
    evidence_path: Path
    evidence_bytes: bytes
    plan: PreparationPlan


def _canonical_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True) + "\n").encode(
        "utf-8"
    )


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _safe_environment() -> dict[str, str]:
    environment = dict(os.environ)
    for name in ("PYTHONPATH", "PYTHONHOME", "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        environment.pop(name, None)
    environment["PYTHONNOUSERSITE"] = "1"
    environment["GIT_CONFIG_NOSYSTEM"] = "1"
    environment["GIT_CONFIG_GLOBAL"] = os.devnull
    environment["GIT_TERMINAL_PROMPT"] = "0"
    return environment


def _git_executable() -> str:
    supplied = shutil.which("git")
    if supplied is None:
        raise PredecessorPreparationError("Git is required for predecessor preparation")
    try:
        executable = Path(supplied).resolve(strict=True)
    except OSError as exc:
        raise PredecessorPreparationError("Git executable cannot be resolved") from exc
    if not executable.is_file() or bootstrap._path_has_link(executable):
        raise PredecessorPreparationError("Git executable must be an ordinary non-linked file")
    return str(executable)


def _run(
    command: list[str],
    *,
    cwd: Path,
    input_bytes: bytes | None = None,
    timeout: int = MAX_PROCESS_SECONDS,
) -> subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            env=_safe_environment(),
            input=input_bytes,
            check=False,
            capture_output=True,
            timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise PredecessorPreparationError(f"command could not run safely: {Path(command[0]).name}") from exc


def _completed(command: list[str], *, cwd: Path, input_bytes: bytes | None = None) -> bytes:
    result = _run(command, cwd=cwd, input_bytes=input_bytes)
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", "replace").strip().splitlines()
        message = detail[0] if detail else "command failed"
        raise PredecessorPreparationError(message)
    return result.stdout


def _git(root: Path, *arguments: str, input_bytes: bytes | None = None) -> bytes:
    executable = _git_executable()
    return _completed([executable, "-C", str(root), *arguments], cwd=root, input_bytes=input_bytes)


def _git_text(root: Path, *arguments: str) -> str:
    return _git(root, *arguments).decode("utf-8", "strict").strip()


def _ordinary_root(repository: Path) -> Path:
    try:
        root = repository.resolve(strict=True)
    except OSError as exc:
        raise PredecessorPreparationError("repository does not exist") from exc
    if not root.is_dir() or bootstrap._path_has_link(root):
        raise PredecessorPreparationError("repository must be an ordinary directory")
    git_dir = root / ".git"
    if not git_dir.exists():
        raise PredecessorPreparationError("repository must be a Git worktree")
    return root


def _ordinary_external(path: Path, label: str, root: Path) -> Path:
    try:
        candidate = path.resolve(strict=True)
    except OSError as exc:
        raise PredecessorPreparationError(f"{label} does not exist") from exc
    if not candidate.is_file() or bootstrap._path_has_link(candidate):
        raise PredecessorPreparationError(f"{label} must be an ordinary external file")
    try:
        candidate.relative_to(root)
    except ValueError:
        return candidate
    raise PredecessorPreparationError(f"{label} must be outside the repository")


def _normalized_unique(values: Iterable[str], label: str) -> tuple[str, ...]:
    result = tuple(sorted(item.strip() for item in values if isinstance(item, str) and item.strip()))
    if not result:
        raise PredecessorPreparationError(f"{label} must not be empty")
    if len(result) != len(set(result)):
        raise PredecessorPreparationError(f"{label} contains duplicate values")
    return result


def _relations(metadata: dict[str, Any], name: str) -> tuple[str, ...]:
    relations = metadata.get("relations")
    value = relations.get(name) if isinstance(relations, dict) else None
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise PredecessorPreparationError(f"relation {name} is missing or invalid")
    if len(value) != len(set(value)):
        raise PredecessorPreparationError(f"relation {name} contains duplicate targets")
    return tuple(sorted(value))


def _artifact(
    catalog: dict[str, tuple[Path, dict[str, Any]]], artifact_id: str, artifact_type: str
) -> tuple[Path, dict[str, Any]]:
    item = catalog.get(artifact_id)
    if item is None or item[1].get("type") != artifact_type:
        raise PredecessorPreparationError(f"artifact is missing or has the wrong type: {artifact_id}")
    return item


def _candidate_validation(root: Path) -> dict[str, Any]:
    validator = root / "templates" / "repository" / "standard" / "scripts" / "validate_engineering_artifacts.py"
    if not validator.is_file() or bootstrap._path_has_link(validator, root):
        raise PredecessorPreparationError("candidate validator is unavailable")
    result = _run([sys.executable, str(validator), "--root", str(root), "--json"], cwd=root)
    try:
        report = json.loads(result.stdout.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise PredecessorPreparationError("candidate validator returned an invalid contract") from exc
    if not isinstance(report, dict):
        raise PredecessorPreparationError("candidate validator returned an invalid report")
    if result.returncode != 0 or report.get("valid") is not True:
        errors = report.get("errors")
        first = errors[0].get("message") if isinstance(errors, list) and errors and isinstance(errors[0], dict) else None
        raise PredecessorPreparationError(
            f"complete candidate graph is invalid: {first or 'candidate validation failed'}"
        )
    return report


def _source_identity(root: Path) -> tuple[str, str, str]:
    if _git_text(root, "status", "--porcelain", "--untracked-files=all"):
        raise PredecessorPreparationError("predecessor preparation requires a clean Git worktree")
    commit = _git_text(root, "rev-parse", "HEAD").lower()
    object_format = _git_text(root, "rev-parse", "--show-object-format").lower()
    pattern = COMMIT_PATTERNS.get(object_format)
    if pattern is None or pattern.fullmatch(commit) is None:
        raise PredecessorPreparationError("source commit uses an unsupported Git object format")
    tree = _git_text(root, "rev-parse", f"{commit}^{{tree}}").lower()
    if pattern.fullmatch(tree) is None:
        raise PredecessorPreparationError("source tree identity is invalid")
    return commit, tree, object_format


def _committed_bytes(root: Path, commit: str, relative: str) -> bytes:
    path = PurePosixPath(relative)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise PredecessorPreparationError("history path is not normalized")
    result = _run(
        [_git_executable(), "-C", str(root), "show", f"{commit}:{relative}"], cwd=root
    )
    if result.returncode != 0:
        raise PredecessorPreparationError(f"history path is not committed: {relative}")
    return result.stdout


def _history_descriptor(
    root: Path,
    commit: str,
    object_format: str,
    path: Path,
    metadata: dict[str, Any],
) -> HistoryDescriptor:
    relative = path.relative_to(root).as_posix()
    if bootstrap._path_has_link(path, root):
        raise PredecessorPreparationError(f"history path traverses a link: {relative}")
    raw = _committed_bytes(root, commit, relative)
    try:
        current = path.read_bytes()
    except OSError as exc:
        raise PredecessorPreparationError(f"history path is unavailable: {relative}") from exc
    try:
        canonical_current = bootstrap._canonical_utf8_text_lf(current, "history artifact")
    except bootstrap.ReleaseBootstrapError as exc:
        raise PredecessorPreparationError(str(exc)) from exc
    if canonical_current != raw:
        raise PredecessorPreparationError(f"history path differs from its committed Git blob: {relative}")
    blob = _git_text(root, "rev-parse", f"{commit}:{relative}").lower()
    if COMMIT_PATTERNS[object_format].fullmatch(blob) is None:
        raise PredecessorPreparationError(f"history blob identity is invalid: {relative}")
    return HistoryDescriptor(
        artifact_id=str(metadata["id"]),
        artifact_type=str(metadata["type"]),
        status=str(metadata["status"]),
        path=relative,
        git_blob=blob,
        bytes=len(raw),
        sha256=_sha256(raw),
    )


def _derive_history(
    root: Path,
    catalog: dict[str, tuple[Path, dict[str, Any]]],
    version: str,
    commit: str,
    object_format: str,
) -> tuple[HistoryDescriptor, HistoryDescriptor]:
    rejected_records = [
        (path, metadata)
        for path, metadata in catalog.values()
        if metadata.get("type") == "release_record" and metadata.get("status") == "rejected"
    ]
    matching = [item for item in rejected_records if item[1].get("version") == version]
    if len(rejected_records) != 1 or len(matching) != 1:
        raise PredecessorPreparationError(
            "compatibility view requires exactly one rejected release record, for the successor version"
        )
    record_path, record = matching[0]
    if record.get("preparation_schema") != bootstrap.PREPARATION_SCHEMA:
        raise PredecessorPreparationError("rejected history is not a predecessor-bootstrap release")
    satisfied = _relations(record, "satisfies")
    if len(satisfied) != 1:
        raise PredecessorPreparationError("rejected predecessor history must satisfy exactly one contract")
    contract_path, contract = _artifact(catalog, satisfied[0], "release_contract")
    if contract.get("status") != "rejected":
        raise PredecessorPreparationError("rejected predecessor history requires its exact rejected contract")
    try:
        tuple_value = contract["bootstrap"]
    except KeyError as exc:
        raise PredecessorPreparationError("rejected history contract has no bootstrap tuple") from exc
    if (
        not isinstance(tuple_value, dict)
        or tuple_value.get("release_record") != record.get("id")
        or tuple_value.get("version") != version
    ):
        raise PredecessorPreparationError("rejected history contract tuple differs from its record")
    evidence_path = record.get("evaluator_evidence_path")
    evidence_sha = record.get("evaluator_evidence_sha256")
    if not isinstance(evidence_path, str) or not isinstance(evidence_sha, str):
        raise PredecessorPreparationError("rejected history has no complete evaluator evidence binding")
    evidence = root / PurePosixPath(evidence_path)
    try:
        evidence_raw = evidence.read_bytes()
    except OSError as exc:
        raise PredecessorPreparationError("rejected history evaluator evidence is unavailable") from exc
    if _sha256(evidence_raw) != evidence_sha:
        raise PredecessorPreparationError("rejected history evaluator evidence digest differs")
    descriptors = (
        _history_descriptor(root, commit, object_format, contract_path, contract),
        _history_descriptor(root, commit, object_format, record_path, record),
    )
    return tuple(sorted(descriptors, key=lambda item: item.path))  # type: ignore[return-value]


def _release_destination(root: Path, contract_path: Path, record_id: str) -> tuple[Path, str]:
    relative = contract_path.relative_to(root)
    parts = relative.parts
    if len(parts) < 5 or parts[:2] != ("docs", "engineering") or parts[-2] != "release":
        raise PredecessorPreparationError("successor release contract is outside a canonical domain")
    domain_root = contract_path.parent.parent
    destination = domain_root / "releases" / f"{record_id}.md"
    evidence = domain_root / "evidence" / f"{record_id}-preparation-view.json"
    if (
        not destination.parent.is_dir()
        or not evidence.parent.is_dir()
        or bootstrap._path_has_link(destination.parent, root)
        or bootstrap._path_has_link(evidence.parent, root)
    ):
        raise PredecessorPreparationError("successor release or evidence directory is unavailable")
    return destination, evidence.relative_to(root).as_posix()


def _validate_inputs(
    root: Path,
    catalog: dict[str, tuple[Path, dict[str, Any]]],
    *,
    record_id: str,
    release_contract_id: str,
    verification_records: tuple[str, ...],
    work_orders: tuple[str, ...],
    version: str,
    authorized_by: str,
    tag: str | None,
) -> tuple[Path, bootstrap.BootstrapContract, str, str]:
    if bootstrap.ARTIFACT_ID_PATTERN.fullmatch(record_id) is None or not record_id.startswith("RLS-"):
        raise PredecessorPreparationError("release record ID is invalid")
    contract_path, contract_metadata = _artifact(catalog, release_contract_id, "release_contract")
    try:
        contract = bootstrap.parse_bootstrap_contract(contract_metadata)
    except bootstrap.ReleaseBootstrapError as exc:
        raise PredecessorPreparationError(str(exc)) from exc
    if contract.release_record != record_id or contract.version != version:
        raise PredecessorPreparationError("successor ID or version differs from its approved contract")
    if set(_relations(contract_metadata, "gates")) != set(work_orders):
        raise PredecessorPreparationError("successor work set differs from its release contract")
    if not authorized_by or authorized_by not in contract_metadata.get("owners", []):
        raise PredecessorPreparationError("authorized owner is not declared by the release contract")
    if tag is not None and tag != f"v{version}":
        raise PredecessorPreparationError("successor tag must exactly match the release version")
    verified_work: set[str] = set()
    identities: set[tuple[str, str]] = set()
    for verification_id in verification_records:
        _path, verification = _artifact(catalog, verification_id, "verification_record")
        if verification.get("status") != "verified":
            raise PredecessorPreparationError(f"verification record is not verified: {verification_id}")
        verified_work.update(_relations(verification, "verifies_work_order"))
        commit = verification.get("commit")
        object_format = verification.get("git_object_format")
        pattern = COMMIT_PATTERNS.get(object_format)
        if not isinstance(commit, str) or pattern is None or pattern.fullmatch(commit) is None:
            raise PredecessorPreparationError(f"verification candidate identity is invalid: {verification_id}")
        identities.add((commit, object_format))
    if len(identities) != 1:
        raise PredecessorPreparationError("verification records do not identify one candidate")
    if verified_work != set(work_orders):
        raise PredecessorPreparationError("verification coverage differs from the successor work set")
    for work_order in work_orders:
        _path, metadata = _artifact(catalog, work_order, "work_order")
        if metadata.get("status") not in RELEASABLE_WORK_STATUSES:
            raise PredecessorPreparationError(f"work order is not releasable: {work_order}")
    active = [
        metadata.get("id")
        for _path, metadata in catalog.values()
        if metadata.get("type") == "release_record"
        and metadata.get("id") != record_id
        and metadata.get("status") in {"ready", "released"}
        and metadata.get("version") == version
    ]
    if active:
        raise PredecessorPreparationError(f"release version already has an active record: {active[0]}")
    candidate_commit, candidate_format = next(iter(identities))
    return contract_path, contract, candidate_commit, candidate_format


def _sparse_spec(history: tuple[HistoryDescriptor, ...]) -> bytes:
    lines = ["/*", *(f"!/{item.path}" for item in history)]
    return ("\n".join(lines) + "\n").encode("utf-8")


def _create_view(root: Path, commit: str, history: tuple[HistoryDescriptor, ...], parent: Path) -> tuple[Path, bytes]:
    view = parent / "repository"
    executable = _git_executable()
    _completed(
        [
            executable,
            "-c",
            "protocol.file.allow=always",
            "clone",
            "--no-local",
            "--no-checkout",
            str(root),
            str(view),
        ],
        cwd=parent,
    )
    spec = _sparse_spec(history)
    _git(view, "sparse-checkout", "init", "--no-cone")
    _git(view, "sparse-checkout", "set", "--no-cone", "--stdin", input_bytes=spec)
    sparse_path = Path(_git_text(view, "rev-parse", "--git-path", "info/sparse-checkout"))
    if not sparse_path.is_absolute():
        sparse_path = view / sparse_path
    try:
        sparse_bytes = sparse_path.read_bytes()
    except OSError as exc:
        raise PredecessorPreparationError("preparation sparse specification is unavailable") from exc
    if (
        sparse_bytes != spec
        or _git_text(view, "config", "--worktree", "--get", "core.sparseCheckout") != "true"
        or _git_text(view, "config", "--worktree", "--get", "core.sparseCheckoutCone") != "false"
    ):
        raise PredecessorPreparationError("preparation sparse specification differs from the contract")
    _git(view, "checkout", "--detach", commit)
    if _git_text(view, "rev-parse", "HEAD").lower() != commit:
        raise PredecessorPreparationError("preparation view resolved another commit")
    if _git_text(view, "status", "--porcelain", "--untracked-files=all"):
        raise PredecessorPreparationError("preparation view is not clean")
    alternates = view / ".git" / "objects" / "info" / "alternates"
    if alternates.exists():
        raise PredecessorPreparationError("preparation view uses an alternate Git object database")
    omitted = {item.path for item in history}
    tracked = set(_git_text(view, "ls-tree", "-r", "--name-only", commit).splitlines())
    if not omitted.issubset(tracked):
        raise PredecessorPreparationError("preparation view omission is absent from the source tree")
    missing = []
    for relative in sorted(tracked):
        present = (view / PurePosixPath(relative)).exists()
        if relative in omitted:
            if present:
                raise PredecessorPreparationError(f"preparation view did not omit: {relative}")
        elif not present:
            missing.append(relative)
        elif bootstrap._path_has_link(view / PurePosixPath(relative), view):
            raise PredecessorPreparationError(f"preparation view materialized a linked path: {relative}")
    if missing:
        raise PredecessorPreparationError(f"preparation view omitted an unexpected path: {missing[0]}")
    return view, spec


def _command_arguments(
    *,
    record_id: str,
    release_contract_id: str,
    verification_records: tuple[str, ...],
    work_orders: tuple[str, ...],
    version: str,
    authorized_by: str,
    tag: str | None,
    output: str,
    domain: str,
) -> list[str]:
    arguments = [
        "-I",
        "-m",
        "se_harness",
        "prepare-release",
        ".",
        "--id",
        record_id,
        "--release-contract",
        release_contract_id,
    ]
    for item in verification_records:
        arguments.extend(("--verification-record", item))
    for item in work_orders:
        arguments.extend(("--work-order", item))
    arguments.extend(("--version", version, "--authorized-by", authorized_by))
    if tag is not None:
        arguments.extend(("--tag", tag))
    arguments.extend(("--output", output, "--domain", domain))
    return arguments


def _validate_predecessor_output(
    path: Path,
    *,
    record_id: str,
    release_contract_id: str,
    verification_records: tuple[str, ...],
    work_orders: tuple[str, ...],
    version: str,
    authorized_by: str,
    tag: str | None,
    candidate_commit: str,
    candidate_format: str,
) -> bytes:
    try:
        metadata, raw, _lines, _closing = bootstrap._read_front_matter(path, "predecessor output")
    except bootstrap.ReleaseBootstrapError as exc:
        raise PredecessorPreparationError(str(exc)) from exc
    expected = {
        "id": record_id,
        "type": "release_record",
        "status": "ready",
        "version": version,
        "commit": candidate_commit,
        "git_object_format": candidate_format,
        "authorized_by": authorized_by,
    }
    for field, value in expected.items():
        if metadata.get(field) != value:
            raise PredecessorPreparationError(f"predecessor output field differs: {field}")
    if metadata.get("owners") != [authorized_by]:
        raise PredecessorPreparationError("predecessor output owner differs")
    if not isinstance(metadata.get("released_at"), str) or not metadata["released_at"]:
        raise PredecessorPreparationError("predecessor output timestamp is unavailable")
    if metadata.get("tag") != tag:
        raise PredecessorPreparationError("predecessor output tag differs")
    if _relations(metadata, "satisfies") != (release_contract_id,):
        raise PredecessorPreparationError("predecessor output release contract differs")
    if _relations(metadata, "includes_verification") != verification_records:
        raise PredecessorPreparationError("predecessor output verification set differs")
    if _relations(metadata, "releases_work") != work_orders:
        raise PredecessorPreparationError("predecessor output work set differs")
    if any(field in metadata for field in (*VIEW_BINDING_FIELDS, "preparation_schema")):
        raise PredecessorPreparationError("predecessor output contains a non-predecessor binding")
    return raw


def _attach_view_binding(raw: bytes, evidence_path: str, evidence_sha256: str) -> bytes:
    try:
        text = raw.decode("utf-8")
    except UnicodeError as exc:
        raise PredecessorPreparationError("predecessor output is not UTF-8") from exc
    lines = text.splitlines(keepends=True)
    closing = next((index for index, line in enumerate(lines[1:], 1) if line.strip() == "+++"), -1)
    relation_index = next(
        (index for index, line in enumerate(lines[1:closing], 1) if line.strip() == "[relations]"), -1
    )
    if closing < 0 or relation_index < 0:
        raise PredecessorPreparationError("predecessor output has no relations table")
    newline = "\r\n" if lines[0].endswith("\r\n") else "\n"
    insertion = (
        f'preparation_view_evidence_path = "{evidence_path}"{newline}'
        f'preparation_view_evidence_sha256 = "{evidence_sha256}"{newline}{newline}'
    )
    return ("".join(lines[:relation_index]) + insertion + "".join(lines[relation_index:])).encode("utf-8")


def _prepare(
    repository: Path,
    *,
    record_id: str,
    release_contract_id: str,
    verification_record_ids: Iterable[str],
    work_order_ids: Iterable[str],
    version: str,
    authorized_by: str,
    tag: str | None,
    evaluator_python: Path,
    evaluator_entry_point: Path,
    evaluator_wheel: Path,
) -> _Prepared:
    root = _ordinary_root(repository)
    verification_records = _normalized_unique(verification_record_ids, "verification records")
    work_orders = _normalized_unique(work_order_ids, "work orders")
    _candidate_validation(root)
    source_commit, source_tree, object_format = _source_identity(root)
    catalog = bootstrap._artifact_catalog(root)
    contract_path, contract, candidate_commit, candidate_format = _validate_inputs(
        root,
        catalog,
        record_id=record_id,
        release_contract_id=release_contract_id,
        verification_records=verification_records,
        work_orders=work_orders,
        version=version,
        authorized_by=authorized_by,
        tag=tag,
    )
    history = _derive_history(root, catalog, version, source_commit, object_format)
    python = _ordinary_external(evaluator_python, "evaluator interpreter", root)
    entry_point = _ordinary_external(evaluator_entry_point, "evaluator entry point", root)
    wheel = _ordinary_external(evaluator_wheel, "evaluator wheel", root)
    if wheel.name != contract.evaluator_archive_name or bootstrap._sha256_file(wheel) != contract.evaluator_archive_sha256:
        raise PredecessorPreparationError("evaluator wheel differs from the successor contract")
    record_path, evidence_relative = _release_destination(root, contract_path, record_id)
    evidence_path = root / PurePosixPath(evidence_relative)
    if record_path.exists() or evidence_path.exists():
        raise PredecessorPreparationError("preparation destination already exists or is partial")
    output_relative = record_path.relative_to(root).as_posix()
    domain = contract_path.relative_to(root).parts[2]
    arguments = _command_arguments(
        record_id=record_id,
        release_contract_id=release_contract_id,
        verification_records=verification_records,
        work_orders=work_orders,
        version=version,
        authorized_by=authorized_by,
        tag=tag,
        output=output_relative,
        domain=domain,
    )
    with tempfile.TemporaryDirectory(prefix="se-harness-predecessor-view-") as temporary:
        parent = Path(temporary)
        view, sparse_spec = _create_view(root, source_commit, history, parent)
        try:
            identity = bootstrap._run_released_evaluator(view, python, entry_point, contract)
        except bootstrap.ReleaseBootstrapError as exc:
            raise PredecessorPreparationError(str(exc)) from exc
        try:
            installed_payload = bootstrap._installed_payload(identity, python.parent.parent)
            wheel_payload = bootstrap._wheel_payload(wheel, contract.evaluator_version)
        except (OSError, bootstrap.ReleaseBootstrapError) as exc:
            raise PredecessorPreparationError(str(exc)) from exc
        if installed_payload != wheel_payload:
            raise PredecessorPreparationError(
                "released-evaluator installed payload differs from the exact public wheel"
            )
        result = _run([str(python), *arguments], cwd=view)
        if result.returncode != 0:
            detail = result.stderr.decode("utf-8", "replace").strip().splitlines()
            raise PredecessorPreparationError(
                f"predecessor prepare-release failed: {detail[0] if detail else 'unknown failure'}"
            )
        predecessor_path = view / PurePosixPath(output_relative)
        predecessor_raw = _validate_predecessor_output(
            predecessor_path,
            record_id=record_id,
            release_contract_id=release_contract_id,
            verification_records=verification_records,
            work_orders=work_orders,
            version=version,
            authorized_by=authorized_by,
            tag=tag,
            candidate_commit=candidate_commit,
            candidate_format=candidate_format,
        )
    evidence_value = {
        "candidate": {"commit": candidate_commit, "git_object_format": candidate_format},
        "command": {"arguments": arguments},
        "evaluator": {
            "archive_name": contract.evaluator_archive_name,
            "archive_sha256": contract.evaluator_archive_sha256,
            "runtime_identity_schema": identity.get("schema"),
            "version": contract.evaluator_version,
        },
        "output": {"predecessor_record_sha256": _sha256(predecessor_raw)},
        "release": {
            "contract": release_contract_id,
            "record": record_id,
            "verification_records": list(verification_records),
            "version": version,
            "work_orders": list(work_orders),
        },
        "schema": EVIDENCE_SCHEMA,
        "source": {
            "commit": source_commit,
            "git_object_format": object_format,
            "tree": source_tree,
        },
        "view": {
            "omitted_history": [asdict(item) for item in history],
            "sparse_spec_sha256": _sha256(sparse_spec),
        },
    }
    evidence_bytes = _canonical_json(evidence_value)
    if len(evidence_bytes) > MAX_EVIDENCE_BYTES:
        raise PredecessorPreparationError("preparation-view evidence exceeds the byte limit")
    evidence_sha256 = _sha256(evidence_bytes)
    record_bytes = _attach_view_binding(predecessor_raw, evidence_relative, evidence_sha256)
    plan = PreparationPlan(
        schema=EVIDENCE_SCHEMA,
        source_commit=source_commit,
        source_tree=source_tree,
        git_object_format=object_format,
        candidate_commit=candidate_commit,
        release_contract=release_contract_id,
        release_record=record_id,
        version=version,
        verification_records=verification_records,
        work_orders=work_orders,
        omitted_history=history,
        sparse_spec_sha256=_sha256(sparse_spec),
        predecessor_output_sha256=_sha256(predecessor_raw),
        preparation_view_evidence_path=evidence_relative,
        preparation_view_evidence_sha256=evidence_sha256,
        release_record_path=output_relative,
        changed=True,
        applied=False,
    )
    return _Prepared(root, record_path, record_bytes, evidence_path, evidence_bytes, plan)


def _unbound_predecessor_record(
    raw: bytes,
    metadata: dict[str, Any],
    evidence_path: str,
    evidence_sha256: str,
) -> bytes:
    newline = b"\r\n" if raw.startswith(b"+++\r\n") else b"\n"
    view_block = (
        f'preparation_view_evidence_path = "{evidence_path}"'.encode("utf-8") + newline
        + f'preparation_view_evidence_sha256 = "{evidence_sha256}"'.encode("utf-8")
        + newline * 2
    )
    if raw.count(view_block) != 1:
        raise PredecessorPreparationError("existing preparation-view binding is not canonical")
    result = raw.replace(view_block, b"", 1)
    evaluator_fields = (
        metadata.get("preparation_schema"),
        metadata.get("evaluator_evidence_path"),
        metadata.get("evaluator_evidence_sha256"),
    )
    if any(item is not None for item in evaluator_fields):
        preparation_schema, evaluator_path, evaluator_digest = evaluator_fields
        if (
            preparation_schema != bootstrap.PREPARATION_SCHEMA
            or not isinstance(evaluator_path, str)
            or not isinstance(evaluator_digest, str)
            or bootstrap.SHA256_PATTERN.fullmatch(evaluator_digest) is None
        ):
            raise PredecessorPreparationError("existing evaluator binding is incomplete")
        evaluator_block = (
            f'preparation_schema = "{preparation_schema}"'.encode("utf-8") + newline
            + f'evaluator_evidence_path = "{evaluator_path}"'.encode("utf-8") + newline
            + f'evaluator_evidence_sha256 = "{evaluator_digest}"'.encode("utf-8")
            + newline * 2
        )
        if result.count(evaluator_block) != 1:
            raise PredecessorPreparationError("existing evaluator binding is not canonical")
        result = result.replace(evaluator_block, b"", 1)
    return result


def _existing_preparation(
    repository: Path,
    *,
    record_id: str,
    release_contract_id: str,
    verification_record_ids: Iterable[str],
    work_order_ids: Iterable[str],
    version: str,
    authorized_by: str,
    tag: str | None,
    evaluator_python: Path,
    evaluator_entry_point: Path,
    evaluator_wheel: Path,
) -> PreparationPlan | None:
    root = _ordinary_root(repository)
    catalog = bootstrap._artifact_catalog(root)
    contract_path, contract_metadata = _artifact(
        catalog, release_contract_id, "release_contract"
    )
    record_path, evidence_relative = _release_destination(root, contract_path, record_id)
    evidence_path = root / PurePosixPath(evidence_relative)
    if not record_path.exists() and not evidence_path.exists():
        return None
    if not record_path.is_file() or not evidence_path.is_file():
        raise PredecessorPreparationError("preparation destination already exists or is partial")
    if bootstrap._path_has_link(record_path, root) or bootstrap._path_has_link(evidence_path, root):
        raise PredecessorPreparationError("existing preparation output traverses a link")
    verification_records = _normalized_unique(verification_record_ids, "verification records")
    work_orders = _normalized_unique(work_order_ids, "work orders")
    try:
        contract = bootstrap.parse_bootstrap_contract(contract_metadata)
        record, record_raw, _record_lines, _record_closing = bootstrap._read_front_matter(
            record_path, "existing prepared release"
        )
        evidence_raw = evidence_path.read_bytes()
    except (OSError, bootstrap.ReleaseBootstrapError) as exc:
        raise PredecessorPreparationError(str(exc)) from exc
    if (
        record.get("preparation_view_evidence_path") != evidence_relative
        or not isinstance(record.get("preparation_view_evidence_sha256"), str)
        or record["preparation_view_evidence_sha256"] != _sha256(evidence_raw)
    ):
        raise PredecessorPreparationError("existing preparation-view binding differs")
    try:
        value = json.loads(evidence_raw.decode("utf-8"), object_pairs_hook=bootstrap._unique_object)
    except (UnicodeError, json.JSONDecodeError, bootstrap.ReleaseBootstrapError) as exc:
        raise PredecessorPreparationError("existing preparation-view evidence is invalid") from exc
    if (
        evidence_raw != _canonical_json(value)
        or not isinstance(value, dict)
        or set(value) != {"schema", "source", "candidate", "release", "evaluator", "command", "view", "output"}
        or value.get("schema") != EVIDENCE_SCHEMA
    ):
        raise PredecessorPreparationError("existing preparation-view evidence is not canonical")
    contract_path, validated_contract, candidate_commit, candidate_format = _validate_inputs(
        root,
        catalog,
        record_id=record_id,
        release_contract_id=release_contract_id,
        verification_records=verification_records,
        work_orders=work_orders,
        version=version,
        authorized_by=authorized_by,
        tag=tag,
    )
    if validated_contract != contract:
        raise PredecessorPreparationError("existing successor contract changed")
    expected_record = {
        "id": record_id,
        "type": "release_record",
        "status": "ready",
        "version": version,
        "commit": candidate_commit,
        "git_object_format": candidate_format,
        "authorized_by": authorized_by,
        "tag": tag,
    }
    if any(record.get(field) != expected for field, expected in expected_record.items()):
        raise PredecessorPreparationError("existing prepared release identity differs")
    if record.get("owners") != [authorized_by]:
        raise PredecessorPreparationError("existing prepared release owner differs")
    if (
        _relations(record, "satisfies") != (release_contract_id,)
        or _relations(record, "includes_verification") != verification_records
        or _relations(record, "releases_work") != work_orders
    ):
        raise PredecessorPreparationError("existing prepared release scope differs")
    source = value.get("source")
    candidate = value.get("candidate")
    release = value.get("release")
    evaluator = value.get("evaluator")
    command = value.get("command")
    view_value = value.get("view")
    output = value.get("output")
    if not isinstance(source, dict) or set(source) != {"commit", "git_object_format", "tree"}:
        raise PredecessorPreparationError("existing preparation source identity is invalid")
    source_commit = source.get("commit")
    source_tree = source.get("tree")
    object_format = source.get("git_object_format")
    pattern = COMMIT_PATTERNS.get(object_format)
    if (
        pattern is None
        or not isinstance(source_commit, str)
        or pattern.fullmatch(source_commit) is None
        or not isinstance(source_tree, str)
        or pattern.fullmatch(source_tree) is None
        or _git_text(root, "rev-parse", "--show-object-format") != object_format
        or _git_text(root, "rev-parse", f"{source_commit}^{{tree}}").lower() != source_tree
        or _run(
            [_git_executable(), "-C", str(root), "merge-base", "--is-ancestor", source_commit, "HEAD"],
            cwd=root,
        ).returncode
        != 0
    ):
        raise PredecessorPreparationError("existing preparation source Git identity differs")
    history = _derive_history(root, catalog, version, source_commit, object_format)
    history_value = view_value.get("omitted_history") if isinstance(view_value, dict) else None
    sparse_digest = view_value.get("sparse_spec_sha256") if isinstance(view_value, dict) else None
    if (
        not isinstance(history_value, list)
        or history_value != [asdict(item) for item in history]
        or sparse_digest != _sha256(_sparse_spec(history))
    ):
        raise PredecessorPreparationError("existing preparation omission identity differs")
    expected_release = {
        "contract": release_contract_id,
        "record": record_id,
        "verification_records": list(verification_records),
        "version": version,
        "work_orders": list(work_orders),
    }
    if release != expected_release or candidate != {
        "commit": candidate_commit,
        "git_object_format": candidate_format,
    }:
        raise PredecessorPreparationError("existing preparation candidate or release scope differs")
    output_relative = record_path.relative_to(root).as_posix()
    expected_arguments = _command_arguments(
        record_id=record_id,
        release_contract_id=release_contract_id,
        verification_records=verification_records,
        work_orders=work_orders,
        version=version,
        authorized_by=authorized_by,
        tag=tag,
        output=output_relative,
        domain=contract_path.relative_to(root).parts[2],
    )
    if command != {"arguments": expected_arguments}:
        raise PredecessorPreparationError("existing preparation command scope differs")
    predecessor_raw = _unbound_predecessor_record(
        record_raw,
        record,
        evidence_relative,
        record["preparation_view_evidence_sha256"],
    )
    predecessor_digest = output.get("predecessor_record_sha256") if isinstance(output, dict) else None
    if predecessor_digest != _sha256(predecessor_raw):
        raise PredecessorPreparationError("existing predecessor output digest differs")
    python = _ordinary_external(evaluator_python, "evaluator interpreter", root)
    entry_point = _ordinary_external(evaluator_entry_point, "evaluator entry point", root)
    wheel = _ordinary_external(evaluator_wheel, "evaluator wheel", root)
    if wheel.name != contract.evaluator_archive_name or bootstrap._sha256_file(wheel) != contract.evaluator_archive_sha256:
        raise PredecessorPreparationError("evaluator wheel differs from the successor contract")
    with tempfile.TemporaryDirectory(prefix="se-harness-predecessor-replay-") as temporary:
        replay, sparse_spec = _create_view(root, source_commit, history, Path(temporary))
        try:
            identity = bootstrap._run_released_evaluator(replay, python, entry_point, contract)
            installed_payload = bootstrap._installed_payload(identity, python.parent.parent)
            wheel_payload = bootstrap._wheel_payload(wheel, contract.evaluator_version)
        except (OSError, bootstrap.ReleaseBootstrapError) as exc:
            raise PredecessorPreparationError(str(exc)) from exc
    if installed_payload != wheel_payload:
        raise PredecessorPreparationError(
            "released-evaluator installed payload differs from the exact public wheel"
        )
    expected_evaluator = {
        "archive_name": contract.evaluator_archive_name,
        "archive_sha256": contract.evaluator_archive_sha256,
        "runtime_identity_schema": identity.get("schema"),
        "version": contract.evaluator_version,
    }
    if evaluator != expected_evaluator:
        raise PredecessorPreparationError("existing preparation evaluator identity differs")
    for arguments in (("diff", "--quiet", "HEAD", "--"), ("diff", "--cached", "--quiet", "HEAD", "--")):
        if _run([_git_executable(), "-C", str(root), *arguments], cwd=root).returncode != 0:
            raise PredecessorPreparationError("existing preparation has unrelated tracked changes")
    untracked = {
        item.decode("utf-8", "strict")
        for item in _git(root, "ls-files", "--others", "--exclude-standard", "-z").split(b"\0")
        if item
    }
    expected_untracked = set()
    for path_value in (record_path, evidence_path):
        relative = path_value.relative_to(root).as_posix()
        tracked = _run(
            [_git_executable(), "-C", str(root), "ls-files", "--error-unmatch", "--", relative],
            cwd=root,
        ).returncode == 0
        if not tracked:
            expected_untracked.add(relative)
    if untracked != expected_untracked:
        raise PredecessorPreparationError("existing preparation has unrelated untracked changes")
    return PreparationPlan(
        schema=EVIDENCE_SCHEMA,
        source_commit=source_commit,
        source_tree=source_tree,
        git_object_format=object_format,
        candidate_commit=candidate_commit,
        release_contract=release_contract_id,
        release_record=record_id,
        version=version,
        verification_records=verification_records,
        work_orders=work_orders,
        omitted_history=history,
        sparse_spec_sha256=_sha256(sparse_spec),
        predecessor_output_sha256=predecessor_digest,
        preparation_view_evidence_path=evidence_relative,
        preparation_view_evidence_sha256=_sha256(evidence_raw),
        release_record_path=output_relative,
        changed=False,
        applied=False,
    )


def plan_predecessor_release(
    repository: Path,
    **arguments: Any,
) -> PreparationPlan:
    """Validate and rehearse the exact predecessor operation without repository writes."""
    existing = _existing_preparation(repository, **arguments)
    if existing is not None:
        return existing
    return _prepare(repository, **arguments).plan


def _assert_apply_state(prepared: _Prepared, created: tuple[Path, ...]) -> None:
    root = prepared.root
    if _git_text(root, "rev-parse", "HEAD").lower() != prepared.plan.source_commit:
        raise PredecessorPreparationError("source commit changed after predecessor preparation")
    if _git_text(root, "rev-parse", "HEAD^{tree}").lower() != prepared.plan.source_tree:
        raise PredecessorPreparationError("source tree changed after predecessor preparation")
    for arguments in (("diff", "--quiet", "HEAD", "--"), ("diff", "--cached", "--quiet", "HEAD", "--")):
        result = _run([_git_executable(), "-C", str(root), *arguments], cwd=root)
        if result.returncode != 0:
            raise PredecessorPreparationError("tracked source changed after predecessor preparation")
    untracked_raw = _git(root, "ls-files", "--others", "--exclude-standard", "-z")
    untracked = {
        item.decode("utf-8", "strict")
        for item in untracked_raw.split(b"\0")
        if item
    }
    expected_untracked = {path.relative_to(root).as_posix() for path in created}
    if untracked != expected_untracked:
        raise PredecessorPreparationError("untracked source changed after predecessor preparation")
    history_by_path = {item.path: item for item in prepared.plan.omitted_history}
    for relative, descriptor in history_by_path.items():
        path = root / PurePosixPath(relative)
        try:
            current = bootstrap._canonical_utf8_text_lf(path.read_bytes(), "history artifact")
        except (OSError, bootstrap.ReleaseBootstrapError) as exc:
            raise PredecessorPreparationError(f"history path changed after preparation: {relative}") from exc
        if len(current) != descriptor.bytes or _sha256(current) != descriptor.sha256:
            raise PredecessorPreparationError(f"history path changed after preparation: {relative}")
    expected_payloads = {
        prepared.evidence_path: prepared.evidence_bytes,
        prepared.record_path: prepared.record_bytes,
    }
    for path, payload in expected_payloads.items():
        if path in created:
            try:
                current = path.read_bytes()
            except OSError as exc:
                raise PredecessorPreparationError(
                    f"preparation output changed after creation: {path.name}"
                ) from exc
            if current != payload:
                raise PredecessorPreparationError(
                    f"preparation output changed after creation: {path.name}"
                )
        elif path.exists():
            raise PredecessorPreparationError(
                f"preparation destination appeared after planning: {path.name}"
            )


def _open_exclusive(path: Path) -> int:
    """Open one adapter output without exposing process-global os.open to tests."""
    return os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)


def apply_predecessor_release(
    repository: Path,
    **arguments: Any,
) -> PreparationPlan:
    """Exclusive-create the predecessor-generated RLS and canonical view evidence."""
    existing = _existing_preparation(repository, **arguments)
    if existing is not None:
        return replace(existing, applied=True)
    prepared = _prepare(repository, **arguments)
    created: list[Path] = []
    try:
        _assert_apply_state(prepared, ())
        for path, payload in (
            (prepared.evidence_path, prepared.evidence_bytes),
            (prepared.record_path, prepared.record_bytes),
        ):
            descriptor = _open_exclusive(path)
            created.append(path)
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            _assert_apply_state(prepared, tuple(created))
    except (OSError, PredecessorPreparationError) as exc:
        for path in reversed(created):
            try:
                path.unlink()
            except OSError as rollback_exc:
                raise PredecessorPreparationError(
                    f"preparation failed and rollback failed: {rollback_exc}"
                ) from exc
        if isinstance(exc, PredecessorPreparationError):
            raise
        raise PredecessorPreparationError(f"cannot create predecessor preparation outputs: {exc}") from exc
    return replace(prepared.plan, applied=True)
