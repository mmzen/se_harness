"""Read-only dual-plane publication validation for predecessor releases.

Publication governance can legitimately retain lifecycle syntax that an
immutable predecessor evaluator cannot parse.  This adapter validates the
complete committed graph with current semantics, replays the released RLS
preparation/evaluator bindings, and runs that predecessor against the exact
two-omission view already used to prepare the RLS.  It grants no lifecycle or
publication authority and performs no repository or external mutation.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import re
import shutil
import tempfile
import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterator

from repository_tools import predecessor_assessment as assessment
from repository_tools import predecessor_preparation as preparation
from repository_tools import release_bootstrap as bootstrap


EVIDENCE_SCHEMA = "se-harness-predecessor-publication-view-v1"
PREPARATION_SCHEMA = "se-harness-predecessor-preparation-view-v1"
EVALUATOR_EVIDENCE_SCHEMA = "se-harness-evaluator-evidence-v1"
MAX_COMMAND_OUTPUT_BYTES = 4 * 1024 * 1024
MAX_EVIDENCE_BYTES = 256 * 1024
RUNTIME_IDENTITY_SCHEMAS = frozenset(
    {"se-harness-runtime-identity-v2", "se-harness-runtime-identity-v3"}
)
FORBIDDEN_CREDENTIALS = frozenset(
    {
        "ACTIONS_ID_TOKEN_REQUEST_TOKEN",
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_SESSION_TOKEN",
        "AZURE_CLIENT_SECRET",
        "GH_TOKEN",
        "GITHUB_TOKEN",
        "GOOGLE_APPLICATION_CREDENTIALS",
        "PYPI_API_TOKEN",
        "TWINE_PASSWORD",
    }
)
FORBIDDEN_PROCESS_STATE = frozenset(
    {
        "GIT_ALTERNATE_OBJECT_DIRECTORIES",
        "GIT_COMMON_DIR",
        "GIT_DIR",
        "GIT_INDEX_FILE",
        "GIT_OBJECT_DIRECTORY",
        "GIT_WORK_TREE",
        "PYTHONHOME",
        "PYTHONPATH",
    }
)
SENSITIVE_NAME = re.compile(r"(?:^|_)(?:CREDENTIALS?|PASSWORD|SECRET|TOKEN)(?:_|$)")
OUTPUT_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,126}\.json")
VIEW_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")
WINDOWS_RESERVED_NAMES = frozenset(
    {"CON", "PRN", "AUX", "NUL"}
    | {f"COM{index}" for index in range(1, 10)}
    | {f"LPT{index}" for index in range(1, 10)}
)


class PredecessorPublicationError(RuntimeError):
    """A publication-view input or observation violates the contract."""


@dataclass(frozen=True)
class PublicationPlan:
    schema: str
    source_commit: str
    source_tree: str
    git_object_format: str
    release_record: str
    release_contract: str
    version: str
    candidate_commit: str
    evaluator_version: str
    evaluator_archive_name: str
    evaluator_archive_sha256: str
    evaluator_payload_sha256: str
    omitted_history: tuple[preparation.HistoryDescriptor, ...]
    sparse_spec_sha256: str
    current_artifact_count: int
    current_warning_count: int
    predecessor_artifact_count: int
    predecessor_warning_count: int
    observation_sha256: str
    observation_path: str | None
    retained_view: bool
    source_unchanged: bool
    applied: bool

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["omitted_history"] = [asdict(item) for item in self.omitted_history]
        return value


def _canonical_json(value: Any) -> bytes:
    return preparation._canonical_json(value)


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _relations(metadata: dict[str, Any], name: str) -> tuple[str, ...]:
    return preparation._relations(metadata, name)


def _credential_names() -> set[str]:
    return {name for name in os.environ if SENSITIVE_NAME.search(name.upper())}


def _inherited_git_config_is_safe_directory_only() -> bool:
    count_value = os.environ.get("GIT_CONFIG_COUNT")
    if count_value is None:
        return not any(name.startswith("GIT_CONFIG_KEY_") or name.startswith("GIT_CONFIG_VALUE_") for name in os.environ)
    try:
        count = int(count_value)
    except ValueError:
        return False
    if count < 0 or count > 16:
        return False
    expected = {
        *(f"GIT_CONFIG_KEY_{index}" for index in range(count)),
        *(f"GIT_CONFIG_VALUE_{index}" for index in range(count)),
    }
    present = {
        name
        for name in os.environ
        if name.startswith("GIT_CONFIG_KEY_") or name.startswith("GIT_CONFIG_VALUE_")
    }
    return present == expected and all(
        os.environ.get(f"GIT_CONFIG_KEY_{index}") == "safe.directory"
        and bool(os.environ.get(f"GIT_CONFIG_VALUE_{index}"))
        for index in range(count)
    )


@contextlib.contextmanager
def _isolated_process_environment(root: Path) -> Iterator[None]:
    """Keep action-runtime and incidental credentials out of every child."""

    removed: dict[str, str] = {}
    git_config = {name for name in os.environ if name.startswith("GIT_CONFIG_")}
    for name in sorted(_credential_names() | set(FORBIDDEN_PROCESS_STATE) | git_config):
        if name in os.environ:
            removed[name] = os.environ.pop(name)
    os.environ["GIT_CONFIG_COUNT"] = "2"
    os.environ["GIT_CONFIG_KEY_0"] = "safe.directory"
    os.environ["GIT_CONFIG_VALUE_0"] = root.as_posix()
    os.environ["GIT_CONFIG_KEY_1"] = "safe.directory"
    os.environ["GIT_CONFIG_VALUE_1"] = (root / ".git").as_posix()
    try:
        yield
    finally:
        for name in (
            "GIT_CONFIG_COUNT",
            "GIT_CONFIG_KEY_0",
            "GIT_CONFIG_VALUE_0",
            "GIT_CONFIG_KEY_1",
            "GIT_CONFIG_VALUE_1",
        ):
            os.environ.pop(name, None)
        os.environ.update(removed)


def _reject_environment() -> None:
    credentials = sorted(name for name in FORBIDDEN_CREDENTIALS if os.environ.get(name))
    if credentials:
        raise PredecessorPublicationError(
            "publication credentials are forbidden during predecessor validation: "
            + ", ".join(credentials)
        )
    alternate = sorted(name for name in FORBIDDEN_PROCESS_STATE if os.environ.get(name))
    if alternate:
        raise PredecessorPublicationError(
            "alternate Python or Git process state is forbidden: " + ", ".join(alternate)
        )
    if not _inherited_git_config_is_safe_directory_only():
        raise PredecessorPublicationError(
            "inherited Git configuration may contain only safe.directory entries"
        )


def _ordinary_output(path: Path, root: Path) -> Path:
    if OUTPUT_NAME.fullmatch(path.name) is None or path.stem.upper() in WINDOWS_RESERVED_NAMES:
        raise PredecessorPublicationError("observation output name is invalid")
    lexical = Path(os.path.abspath(path))
    if bootstrap._path_has_link(lexical.parent):
        raise PredecessorPublicationError("observation output parent must be unlinked")
    try:
        parent = lexical.parent.resolve(strict=True)
        repository = root.resolve(strict=True)
    except OSError as exc:
        raise PredecessorPublicationError("observation output parent is unavailable") from exc
    if not parent.is_dir():
        raise PredecessorPublicationError("observation output parent is not a directory")
    candidate = parent / lexical.name
    try:
        candidate.relative_to(repository)
    except ValueError:
        return candidate
    raise PredecessorPublicationError("observation output must be outside the repository")


def _ordinary_view_output(path: Path, root: Path) -> Path:
    if (
        VIEW_NAME.fullmatch(path.name) is None
        or path.name.split(".", 1)[0].upper() in WINDOWS_RESERVED_NAMES
    ):
        raise PredecessorPublicationError("publication view output name is invalid")
    lexical = Path(os.path.abspath(path))
    if bootstrap._path_has_link(lexical.parent):
        raise PredecessorPublicationError("publication view output parent must be unlinked")
    try:
        parent = lexical.parent.resolve(strict=True)
        repository = root.resolve(strict=True)
    except OSError as exc:
        raise PredecessorPublicationError("publication view output parent is unavailable") from exc
    if not parent.is_dir():
        raise PredecessorPublicationError("publication view output parent is not a directory")
    candidate = parent / lexical.name
    try:
        candidate.relative_to(repository)
    except ValueError:
        if candidate.exists():
            raise PredecessorPublicationError("publication view output already exists")
        return candidate
    raise PredecessorPublicationError("publication view output must be outside the repository")


def _write_exclusive(path: Path, payload: bytes) -> None:
    descriptor: int | None = None
    created = False
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        created = True
        with os.fdopen(descriptor, "wb") as handle:
            descriptor = None
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
    except OSError as exc:
        if descriptor is not None:
            os.close(descriptor)
        if created:
            try:
                path.unlink()
            except OSError:
                pass
        raise PredecessorPublicationError(f"cannot create observation output: {exc}") from exc


def _discard_retained_view(path: Path) -> None:
    shutil.rmtree(path, ignore_errors=True)
    if path.exists():
        raise PredecessorPublicationError("retained publication view cleanup could not be proven")


def _safe_relative(value: Any, *, label: str, expected_name: str | None = None) -> str:
    if not isinstance(value, str):
        raise PredecessorPublicationError(f"{label} path is missing")
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or "\\" in value
        or any(part in {"", ".", ".."} for part in path.parts)
        or path.parts[:2] != ("docs", "engineering")
        or (expected_name is not None and path.name != expected_name)
    ):
        raise PredecessorPublicationError(f"{label} path is unsafe")
    return value


def _committed_file(
    root: Path,
    commit: str,
    relative: str,
    *,
    label: str,
    exact_worktree_bytes: bool = False,
) -> bytes:
    path = root / PurePosixPath(relative)
    if not path.is_file() or bootstrap._path_has_link(path, root):
        raise PredecessorPublicationError(f"{label} is unavailable or linked")
    committed = preparation._committed_bytes(root, commit, relative)
    try:
        current = path.read_bytes()
    except OSError as exc:
        raise PredecessorPublicationError(f"{label} cannot be read") from exc
    if current != committed and exact_worktree_bytes:
        raise PredecessorPublicationError(f"{label} differs from committed bytes")
    if current != committed:
        try:
            canonical_current = bootstrap._canonical_utf8_text_lf(current, label)
        except bootstrap.ReleaseBootstrapError as exc:
            raise PredecessorPublicationError(str(exc)) from exc
        if canonical_current != committed:
            raise PredecessorPublicationError(f"{label} differs from committed content")
    return committed


def _metadata_from_bytes(raw: bytes, *, label: str) -> dict[str, Any]:
    try:
        text = raw.decode("utf-8")
    except UnicodeError as exc:
        raise PredecessorPublicationError(f"{label} is not UTF-8") from exc
    lines = text.splitlines()
    if not lines or lines[0].strip() != "+++":
        raise PredecessorPublicationError(f"{label} has no TOML front matter")
    try:
        closing = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "+++")
        metadata = tomllib.loads("\n".join(lines[1:closing]))
    except (StopIteration, tomllib.TOMLDecodeError) as exc:
        raise PredecessorPublicationError(f"{label} front matter is invalid") from exc
    if not isinstance(metadata, dict):
        raise PredecessorPublicationError(f"{label} front matter is invalid")
    return metadata


def _canonical_bound_json(
    root: Path,
    commit: str,
    *,
    relative: str,
    digest: Any,
    label: str,
    max_bytes: int,
) -> tuple[dict[str, Any], bytes]:
    if not isinstance(digest, str) or bootstrap.SHA256_PATTERN.fullmatch(digest) is None:
        raise PredecessorPublicationError(f"{label} digest is invalid")
    raw = _committed_file(
        root,
        commit,
        relative,
        label=label,
        exact_worktree_bytes=True,
    )
    if not raw or len(raw) > max_bytes or _sha256(raw) != digest:
        raise PredecessorPublicationError(f"{label} digest or size differs")
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=bootstrap._unique_object)
    except (UnicodeError, json.JSONDecodeError, bootstrap.ReleaseBootstrapError) as exc:
        raise PredecessorPublicationError(f"{label} JSON is invalid") from exc
    if not isinstance(value, dict) or raw != _canonical_json(value):
        raise PredecessorPublicationError(f"{label} is not canonical JSON")
    return value, raw


def _validate_evaluator_evidence(
    root: Path,
    commit: str,
    record: dict[str, Any],
    contract: bootstrap.BootstrapContract,
) -> tuple[dict[str, Any], str, str]:
    relative = _safe_relative(
        record.get("evaluator_evidence_path"),
        label="evaluator evidence",
        expected_name=f"{record['id']}-evaluator.json",
    )
    value, _raw = _canonical_bound_json(
        root,
        commit,
        relative=relative,
        digest=record.get("evaluator_evidence_sha256"),
        label="evaluator evidence",
        max_bytes=preparation.MAX_EVIDENCE_BYTES,
    )
    if set(value) != {"schema", "role", "evaluator", "origins", "environment", "diagnostics"}:
        raise PredecessorPublicationError("evaluator evidence field set differs")
    evaluator = value.get("evaluator")
    origins = value.get("origins")
    environment = value.get("environment")
    if (
        value.get("schema") != EVALUATOR_EVIDENCE_SCHEMA
        or value.get("role") != "released-evaluator"
        or value.get("diagnostics") != []
        or not isinstance(evaluator, dict)
        or set(evaluator)
        != {"archive_name", "archive_sha256", "payload_manifest", "payload_sha256", "version"}
        or evaluator.get("payload_manifest") != bootstrap.PAYLOAD_MANIFEST
        or evaluator.get("version") != contract.evaluator_version
        or evaluator.get("archive_name") != contract.evaluator_archive_name
        or evaluator.get("archive_sha256") != contract.evaluator_archive_sha256
        or not isinstance(evaluator.get("payload_sha256"), str)
        or bootstrap.SHA256_PATTERN.fullmatch(evaluator["payload_sha256"]) is None
    ):
        raise PredecessorPublicationError("evaluator evidence identity differs")
    if (
        not isinstance(origins, dict)
        or set(origins)
        != {"distribution", "entry_point", "module", "python_executable", "templates"}
        or any(not isinstance(item, str) or not item.startswith("<evaluator-root>/") for item in origins.values())
    ):
        raise PredecessorPublicationError("evaluator evidence origins differ")
    environment_fields = {
        "checkout_excluded",
        "entry_point_resolved",
        "isolated_python",
        "pythonpath_present",
        "user_site_enabled",
    }
    if (
        not isinstance(environment, dict)
        or set(environment) != environment_fields
        or any(type(environment.get(item)) is not bool for item in environment_fields)
        or environment
        != {
            "checkout_excluded": True,
            "entry_point_resolved": True,
            "isolated_python": True,
            "pythonpath_present": False,
            "user_site_enabled": False,
        }
    ):
        raise PredecessorPublicationError("evaluator evidence environment differs")
    return value, relative, str(record["evaluator_evidence_sha256"])


def _validate_preparation_evidence(
    root: Path,
    commit: str,
    object_format: str,
    record_path: Path,
    record: dict[str, Any],
    catalog: dict[str, tuple[Path, dict[str, Any]]],
    contract: bootstrap.BootstrapContract,
) -> tuple[dict[str, Any], tuple[preparation.HistoryDescriptor, ...], str, str]:
    relative = _safe_relative(
        record.get("preparation_view_evidence_path"),
        label="preparation-view evidence",
        expected_name=f"{record['id']}-preparation-view.json",
    )
    value, evidence_raw = _canonical_bound_json(
        root,
        commit,
        relative=relative,
        digest=record.get("preparation_view_evidence_sha256"),
        label="preparation-view evidence",
        max_bytes=preparation.MAX_EVIDENCE_BYTES,
    )
    expected_fields = {"candidate", "command", "evaluator", "output", "release", "schema", "source", "view"}
    if set(value) != expected_fields or value.get("schema") != PREPARATION_SCHEMA:
        raise PredecessorPublicationError("preparation-view evidence field set or schema differs")
    source = value.get("source")
    candidate = value.get("candidate")
    release = value.get("release")
    evaluator = value.get("evaluator")
    command = value.get("command")
    view = value.get("view")
    output = value.get("output")
    pattern = preparation.COMMIT_PATTERNS[object_format]
    if not isinstance(source, dict) or set(source) != {"commit", "git_object_format", "tree"}:
        raise PredecessorPublicationError("preparation-view source identity is invalid")
    evidence_commit = source.get("commit")
    evidence_tree = source.get("tree")
    if (
        source.get("git_object_format") != object_format
        or not isinstance(evidence_commit, str)
        or pattern.fullmatch(evidence_commit) is None
        or not isinstance(evidence_tree, str)
        or pattern.fullmatch(evidence_tree) is None
        or preparation._git_text(root, "rev-parse", f"{evidence_commit}^{{tree}}").lower() != evidence_tree
        or preparation._run(
            [preparation._git_executable(), "-C", str(root), "merge-base", "--is-ancestor", evidence_commit, commit],
            cwd=root,
        ).returncode
        != 0
    ):
        raise PredecessorPublicationError("preparation-view source Git identity differs")
    verification_records = _relations(record, "includes_verification")
    work_orders = _relations(record, "releases_work")
    satisfies = _relations(record, "satisfies")
    if candidate != {"commit": record.get("commit"), "git_object_format": record.get("git_object_format")}:
        raise PredecessorPublicationError("preparation-view candidate identity differs")
    if release != {
        "contract": contract.release_contract,
        "record": record.get("id"),
        "verification_records": list(verification_records),
        "version": record.get("version"),
        "work_orders": list(work_orders),
    } or satisfies != (contract.release_contract,):
        raise PredecessorPublicationError("preparation-view release scope differs")
    runtime_schema = evaluator.get("runtime_identity_schema") if isinstance(evaluator, dict) else None
    if not isinstance(evaluator, dict) or evaluator != {
        "archive_name": contract.evaluator_archive_name,
        "archive_sha256": contract.evaluator_archive_sha256,
        "runtime_identity_schema": runtime_schema,
        "version": contract.evaluator_version,
    } or runtime_schema not in RUNTIME_IDENTITY_SCHEMAS:
        raise PredecessorPublicationError("preparation-view evaluator identity differs")
    record_relative = record_path.relative_to(root).as_posix()
    expected_arguments = preparation._command_arguments(
        record_id=str(record["id"]),
        release_contract_id=contract.release_contract,
        verification_records=verification_records,
        work_orders=work_orders,
        version=str(record["version"]),
        authorized_by=str(record["authorized_by"]),
        tag=record.get("tag"),
        output=record_relative,
        domain=record_path.relative_to(root).parts[2],
    )
    if command != {"arguments": expected_arguments}:
        raise PredecessorPublicationError("preparation-view command differs from release scope")
    if (
        not isinstance(output, dict)
        or set(output) != {"predecessor_record_sha256"}
        or not isinstance(output.get("predecessor_record_sha256"), str)
        or bootstrap.SHA256_PATTERN.fullmatch(output["predecessor_record_sha256"]) is None
    ):
        raise PredecessorPublicationError("preparation-view predecessor output identity is invalid")
    history = preparation._derive_history(root, catalog, str(record["version"]), commit, object_format)
    if (
        not isinstance(view, dict)
        or set(view) != {"omitted_history", "sparse_spec_sha256"}
        or view.get("omitted_history") != [asdict(item) for item in history]
        or view.get("sparse_spec_sha256") != _sha256(preparation._sparse_spec(history))
    ):
        raise PredecessorPublicationError("preparation-view omission identity differs")

    additions = [
        line
        for line in preparation._git_text(
            root,
            "log",
            "--reverse",
            "--diff-filter=A",
            "--format=%H",
            f"{evidence_commit}..{commit}",
            "--",
            record_relative,
        ).splitlines()
        if line
    ]
    if len(additions) != 1:
        raise PredecessorPublicationError("prepared release has no unique introduction commit")
    introduced_raw = preparation._committed_bytes(root, additions[0], record_relative)
    introduced = _metadata_from_bytes(introduced_raw, label="introduced prepared release")
    if introduced.get("status") != "ready":
        raise PredecessorPublicationError("introduced prepared release was not ready")
    introduced_evidence = preparation._committed_bytes(root, additions[0], relative)
    if introduced_evidence != evidence_raw:
        raise PredecessorPublicationError("preparation-view evidence changed after introduction")
    predecessor_raw = preparation._unbound_predecessor_record(
        introduced_raw,
        introduced,
        relative,
        str(record["preparation_view_evidence_sha256"]),
    )
    if _sha256(predecessor_raw) != output["predecessor_record_sha256"]:
        raise PredecessorPublicationError("preparation-view predecessor output differs from Git history")
    return value, history, relative, str(record["preparation_view_evidence_sha256"])


def _selected_release(
    root: Path,
    commit: str,
    object_format: str,
    record_id: str,
) -> tuple[Path, dict[str, Any], dict[str, tuple[Path, dict[str, Any]]], bootstrap.BootstrapContract]:
    if bootstrap.ARTIFACT_ID_PATTERN.fullmatch(record_id) is None or not record_id.startswith("RLS-"):
        raise PredecessorPublicationError("release record ID is invalid")
    catalog = bootstrap._artifact_catalog(root)
    record_path, record = preparation._artifact(catalog, record_id, "release_record")
    relative = record_path.relative_to(root)
    if relative.parts[:2] != ("docs", "engineering") or relative.parts[-2] != "releases" or relative.name != f"{record_id}.md":
        raise PredecessorPublicationError("released RLS is outside a canonical release directory")
    _committed_file(root, commit, relative.as_posix(), label="released RLS")
    pattern = preparation.COMMIT_PATTERNS[object_format]
    if (
        record.get("status") != "released"
        or not isinstance(record.get("version"), str)
        or bootstrap.VERSION_PATTERN.fullmatch(record["version"]) is None
        or not isinstance(record.get("commit"), str)
        or pattern.fullmatch(record["commit"]) is None
        or record.get("git_object_format") != object_format
        or record.get("tag") != f"v{record['version']}"
        or not isinstance(record.get("authorized_by"), str)
        or not record["authorized_by"]
    ):
        raise PredecessorPublicationError("released RLS identity is invalid")
    same_version = [
        metadata.get("id")
        for _path, metadata in catalog.values()
        if metadata.get("type") == "release_record"
        and metadata.get("status") == "released"
        and metadata.get("version") == record["version"]
    ]
    if same_version != [record_id]:
        raise PredecessorPublicationError("released RLS selection is ambiguous")
    satisfies = _relations(record, "satisfies")
    if len(satisfies) != 1:
        raise PredecessorPublicationError("released RLS must satisfy exactly one release contract")
    _contract_path, contract_metadata = preparation._artifact(catalog, satisfies[0], "release_contract")
    try:
        contract = bootstrap.parse_bootstrap_contract(contract_metadata)
    except bootstrap.ReleaseBootstrapError as exc:
        raise PredecessorPublicationError(str(exc)) from exc
    if (
        contract.release_record != record_id
        or contract.version != record["version"]
        or set(_relations(contract_metadata, "gates")) != set(_relations(record, "releases_work"))
    ):
        raise PredecessorPublicationError("released RLS differs from its bootstrap contract")
    return record_path, record, catalog, contract


def _tag_identity(
    root: Path,
    *,
    tag: str,
    candidate_commit: str,
    source_commit: str,
    object_format: str,
) -> str:
    pattern = preparation.COMMIT_PATTERNS[object_format]
    try:
        tag_object = preparation._git_text(root, "rev-parse", "--verify", f"refs/tags/{tag}").lower()
        tag_target = preparation._git_text(root, "rev-parse", f"refs/tags/{tag}^{{commit}}").lower()
    except preparation.PredecessorPreparationError as exc:
        raise PredecessorPublicationError("released tag is unavailable") from exc
    ancestor = preparation._run(
        [
            preparation._git_executable(),
            "-C",
            str(root),
            "merge-base",
            "--is-ancestor",
            candidate_commit,
            source_commit,
        ],
        cwd=root,
    )
    if (
        pattern.fullmatch(tag_object) is None
        or tag_target != candidate_commit
        or ancestor.returncode != 0
    ):
        raise PredecessorPublicationError("released tag or candidate ancestry differs")
    return tag_object


def _report_counts(report: dict[str, Any], label: str) -> tuple[int, int]:
    try:
        return assessment._validate_candidate_report(report, label)
    except assessment.PredecessorAssessmentError as exc:
        raise PredecessorPublicationError(str(exc)) from exc


def _run_predecessor(
    view: Path,
    python: Path,
    evaluator_root: Path,
    entry_point: Path,
    wheel: Path,
    contract: bootstrap.BootstrapContract,
    expected_payload: str,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], str]:
    try:
        bootstrap._validate_old_root(view, contract)
        identity, identity_arguments, identity_run = assessment._released_identity(
            view, python, entry_point, contract
        )
        installed_payload = bootstrap._installed_payload(identity, evaluator_root)
        wheel_payload = bootstrap._wheel_payload(wheel, contract.evaluator_version)
    except (
        OSError,
        assessment.PredecessorAssessmentError,
        bootstrap.ReleaseBootstrapError,
    ) as exc:
        raise PredecessorPublicationError(str(exc)) from exc
    if installed_payload != wheel_payload or installed_payload != expected_payload:
        raise PredecessorPublicationError("released-evaluator installed payload differs from retained evidence")

    doctor_arguments = ["doctor", "."]
    doctor = preparation._run([str(entry_point), *doctor_arguments], cwd=view)
    if len(doctor.stdout) > MAX_COMMAND_OUTPUT_BYTES or len(doctor.stderr) > MAX_COMMAND_OUTPUT_BYTES:
        raise PredecessorPublicationError("predecessor doctor output exceeds the byte limit")
    if doctor.returncode != 0:
        raise PredecessorPublicationError("released-evaluator doctor failed in the exact publication view")

    validate_arguments = ["validate", ".", "--json"]
    validate = preparation._run([str(entry_point), *validate_arguments], cwd=view)
    try:
        report = assessment._json_report(validate, "predecessor publication validation")
    except assessment.PredecessorAssessmentError as exc:
        raise PredecessorPublicationError(str(exc)) from exc
    if validate.returncode != 0:
        raise PredecessorPublicationError("released-evaluator validation failed in the exact publication view")
    _report_counts(report, "predecessor publication view")

    replacements = {view: "<publication-view>", evaluator_root: "<evaluator-root>"}
    command_evidence = {
        "doctor": {
            "arguments": ["<evaluator-entry-point>", *doctor_arguments],
            "returncode": doctor.returncode,
            "stderr_sha256": _sha256(assessment._normalized_output(doctor.stderr, replacements)),
            "stdout_sha256": _sha256(assessment._normalized_output(doctor.stdout, replacements)),
        },
        "identity": assessment._identity_evidence(
            identity,
            identity_arguments,
            identity_run,
            checkout_root=view,
            checkout_marker="<publication-view>",
            evaluator_root=evaluator_root,
        ),
        "validate": {
            "arguments": ["<evaluator-entry-point>", *validate_arguments],
            "report_sha256": _sha256(_canonical_json(report)),
            "returncode": validate.returncode,
        },
    }
    return identity, report, command_evidence, installed_payload


def validate_predecessor_publication(
    repository: Path,
    *,
    release_record_id: str,
    evaluator_python: Path,
    evaluator_entry_point: Path,
    evaluator_wheel: Path,
    output: Path | None = None,
    view_output: Path | None = None,
) -> PublicationPlan:
    """Validate both publication planes and optionally retain canonical JSON."""

    _reject_environment()
    try:
        root = preparation._ordinary_root(repository)
    except preparation.PredecessorPreparationError as exc:
        raise PredecessorPublicationError(str(exc)) from exc
    output_path = _ordinary_output(output, root) if output is not None else None
    retained_view_path = _ordinary_view_output(view_output, root) if view_output is not None else None
    if output_path is not None and output_path.exists():
        raise PredecessorPublicationError("observation output already exists")

    with _isolated_process_environment(root):
        try:
            current_before = preparation._candidate_validation(root)
            source_commit, source_tree, object_format = preparation._source_identity(root)
            record_path, record, catalog, contract = _selected_release(
                root, source_commit, object_format, release_record_id
            )
            tag_object = _tag_identity(
                root,
                tag=str(record["tag"]),
                candidate_commit=str(record["commit"]),
                source_commit=source_commit,
                object_format=object_format,
            )
            evaluator_evidence, evaluator_evidence_path, evaluator_evidence_sha = _validate_evaluator_evidence(
                root, source_commit, record, contract
            )
            preparation_evidence, history, preparation_evidence_path, preparation_evidence_sha = _validate_preparation_evidence(
                root,
                source_commit,
                object_format,
                record_path,
                record,
                catalog,
                contract,
            )
            interpreter = preparation._safe_interpreter(
                evaluator_python, "evaluator interpreter", root
            )
            python = interpreter.entry_point
            evaluator_root = interpreter.environment_root
            entry_point = preparation._ordinary_external(
                evaluator_entry_point, "evaluator entry point", root
            )
            wheel = preparation._ordinary_external(evaluator_wheel, "evaluator wheel", root)
        except (preparation.PredecessorPreparationError, bootstrap.ReleaseBootstrapError) as exc:
            raise PredecessorPublicationError(str(exc)) from exc
        if (
            wheel.name != contract.evaluator_archive_name
            or bootstrap._sha256_file(wheel) != contract.evaluator_archive_sha256
        ):
            raise PredecessorPublicationError("evaluator wheel differs from the released RLS contract")

        temporary_path: Path | None = None
        retained_view = False
        try:
            temporary_options = (
                {"dir": retained_view_path.parent}
                if retained_view_path is not None
                else {}
            )
            with tempfile.TemporaryDirectory(
                prefix="se-harness-predecessor-publication-", **temporary_options
            ) as temporary:
                temporary_path = Path(temporary)
                view, sparse_spec = preparation._create_view(
                    root, source_commit, history, temporary_path
                )
                identity, predecessor_report, commands, installed_payload = _run_predecessor(
                    view,
                    python,
                    evaluator_root,
                    entry_point,
                    wheel,
                    contract,
                    str(evaluator_evidence["evaluator"]["payload_sha256"]),
                )
                if preparation._git_text(view, "status", "--porcelain", "--untracked-files=all"):
                    raise PredecessorPublicationError("publication view changed during predecessor validation")
                if preparation._git_text(view, "rev-parse", "HEAD").lower() != source_commit:
                    raise PredecessorPublicationError("publication view commit changed during validation")

                try:
                    current_after = preparation._candidate_validation(root)
                    final_commit, final_tree, final_format = preparation._source_identity(root)
                    final_catalog = bootstrap._artifact_catalog(root)
                    final_history = preparation._derive_history(
                        root, final_catalog, str(record["version"]), final_commit, final_format
                    )
                except preparation.PredecessorPreparationError as exc:
                    raise PredecessorPublicationError(str(exc)) from exc
                if (final_commit, final_tree, final_format) != (source_commit, source_tree, object_format):
                    raise PredecessorPublicationError("source identity changed during publication validation")
                if final_history != history:
                    raise PredecessorPublicationError("rejected history changed during publication validation")
                final_tag_object = _tag_identity(
                    root,
                    tag=str(record["tag"]),
                    candidate_commit=str(record["commit"]),
                    source_commit=final_commit,
                    object_format=final_format,
                )
                if final_tag_object != tag_object:
                    raise PredecessorPublicationError("released tag changed during publication validation")
                if _canonical_json(current_after) != _canonical_json(current_before):
                    raise PredecessorPublicationError("complete current validation changed during publication validation")

                if retained_view_path is not None:
                    view.replace(retained_view_path)
                    retained_view = True
                    if preparation._git_text(retained_view_path, "status", "--porcelain", "--untracked-files=all"):
                        raise PredecessorPublicationError("retained publication view is not clean")
                    if preparation._git_text(retained_view_path, "rev-parse", "HEAD").lower() != source_commit:
                        raise PredecessorPublicationError("retained publication view commit changed")
        except preparation.PredecessorPreparationError as exc:
            if retained_view and retained_view_path is not None:
                _discard_retained_view(retained_view_path)
            raise PredecessorPublicationError(str(exc)) from exc
        except Exception:
            if retained_view and retained_view_path is not None:
                _discard_retained_view(retained_view_path)
            raise
        if temporary_path is None or temporary_path.exists():
            if retained_view and retained_view_path is not None:
                _discard_retained_view(retained_view_path)
            raise PredecessorPublicationError("publication view cleanup could not be proven")
        if retained_view_path is not None and (
            not retained_view or not retained_view_path.is_dir()
        ):
            raise PredecessorPublicationError("publication view retention could not be proven")

    try:
        current_artifacts, current_warnings = _report_counts(current_before, "complete current graph")
        predecessor_artifacts, predecessor_warnings = _report_counts(
            predecessor_report, "predecessor publication view"
        )
        observation = {
            "commands": commands,
            "current": {
                "after_report_sha256": _sha256(_canonical_json(current_after)),
                "artifact_count": current_artifacts,
                "before_report_sha256": _sha256(_canonical_json(current_before)),
                "warning_count": current_warnings,
            },
            "evaluator": {
                "archive_name": contract.evaluator_archive_name,
                "archive_sha256": contract.evaluator_archive_sha256,
                "evidence_path": evaluator_evidence_path,
                "evidence_sha256": evaluator_evidence_sha,
                "payload_sha256": installed_payload,
                "runtime_identity_schema": identity.get("schema"),
                "version": contract.evaluator_version,
            },
            "release": {
                "candidate_commit": record["commit"],
                "contract": contract.release_contract,
                "record": record["id"],
                "status": record["status"],
                "tag": record["tag"],
                "tag_object": tag_object,
                "version": record["version"],
            },
            "schema": EVIDENCE_SCHEMA,
            "source": {
                "commit": source_commit,
                "git_object_format": object_format,
                "tree": source_tree,
                "unchanged": True,
            },
            "view": {
                "artifact_count": predecessor_artifacts,
                "omitted_history": [asdict(item) for item in history],
                "preparation_evidence_path": preparation_evidence_path,
                "preparation_evidence_sha256": preparation_evidence_sha,
                "preparation_source_commit": preparation_evidence["source"]["commit"],
                "report_sha256": _sha256(_canonical_json(predecessor_report)),
                "sparse_spec_sha256": _sha256(sparse_spec),
                "warning_count": predecessor_warnings,
            },
        }
        observation_bytes = _canonical_json(observation)
        if len(observation_bytes) > MAX_EVIDENCE_BYTES:
            raise PredecessorPublicationError("publication observation exceeds the byte limit")
        observation_sha = _sha256(observation_bytes)
        if output_path is not None:
            _write_exclusive(output_path, observation_bytes)
    except Exception:
        if retained_view and retained_view_path is not None:
            _discard_retained_view(retained_view_path)
        raise
    return PublicationPlan(
        schema=EVIDENCE_SCHEMA,
        source_commit=source_commit,
        source_tree=source_tree,
        git_object_format=object_format,
        release_record=str(record["id"]),
        release_contract=contract.release_contract,
        version=str(record["version"]),
        candidate_commit=str(record["commit"]),
        evaluator_version=contract.evaluator_version,
        evaluator_archive_name=contract.evaluator_archive_name,
        evaluator_archive_sha256=contract.evaluator_archive_sha256,
        evaluator_payload_sha256=installed_payload,
        omitted_history=history,
        sparse_spec_sha256=_sha256(sparse_spec),
        current_artifact_count=current_artifacts,
        current_warning_count=current_warnings,
        predecessor_artifact_count=predecessor_artifacts,
        predecessor_warning_count=predecessor_warnings,
        observation_sha256=observation_sha,
        observation_path=(
            f"<external-publication-output>/{output_path.name}" if output_path is not None else None
        ),
        retained_view=retained_view,
        source_unchanged=True,
        applied=output_path is not None,
    )
