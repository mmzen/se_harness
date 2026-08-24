"""Repository-owned predecessor-evaluator bootstrap binding policy."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
import tempfile
import tomllib
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

from repository_tools import interpreter_safety
from se_harness.hash_bound import (
    LOCK_RELATIVE,
    MATCH_DECLARED,
    MATCH_LEGACY_NEWLINE,
    HashBoundError,
    compare_declared_digest,
)


BOOTSTRAP_SCHEMA = "se-harness-release-bootstrap-v1"
PREPARATION_SCHEMA = "se-harness-predecessor-bootstrap-v1"
EVIDENCE_SCHEMA = "se-harness-evaluator-evidence-v1"
PAYLOAD_MANIFEST = "se-harness-installed-payload-v1"
RUNTIME_IDENTITY_SCHEMAS = frozenset(
    {"se-harness-runtime-identity-v2", "se-harness-runtime-identity-v3"}
)
BOOTSTRAP_KEYS = frozenset(
    {
        "schema",
        "release_record",
        "version",
        "from_lock_schema",
        "from_lock_tool_version",
        "from_lock_sha256",
        "evaluator_version",
        "evaluator_archive_name",
        "evaluator_archive_sha256",
    }
)
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
VERSION_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.!+\-]{0,127}")
ARTIFACT_ID_PATTERN = re.compile(r"[A-Z][A-Z0-9-]*-[0-9]{3}")
COMMIT_PATTERNS = {
    "sha1": re.compile(r"[0-9a-f]{40}"),
    "sha256": re.compile(r"[0-9a-f]{64}"),
}
MAX_RECORD_BYTES = 1024 * 1024
MAX_EVIDENCE_BYTES = 64 * 1024
MAX_PAYLOAD_FILES = 4096
MAX_PAYLOAD_MEMBER_BYTES = 16 * 1024 * 1024
MAX_PAYLOAD_BYTES = 128 * 1024 * 1024


class ReleaseBootstrapError(RuntimeError):
    """A predecessor-evaluator bootstrap input violates the approved policy."""


@dataclass(frozen=True)
class BootstrapContract:
    release_contract: str
    release_record: str
    version: str
    from_lock_schema: int
    from_lock_tool_version: str
    from_lock_sha256: str
    evaluator_version: str
    evaluator_archive_name: str
    evaluator_archive_sha256: str


@dataclass(frozen=True)
class BootstrapPlan:
    schema: str
    release_contract: str
    release_record: str
    version: str
    candidate_commit: str
    lock_sha256: str
    evaluator_archive_name: str
    evaluator_archive_sha256: str
    evaluator_payload_sha256: str
    evaluator_evidence_path: str
    evaluator_evidence_sha256: str
    release_record_path: str
    changed: bool
    applied: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class _PreparedBinding:
    root: Path
    record_path: Path
    record_original: bytes
    record_updated: bytes
    evidence_path: Path
    evidence_bytes: bytes
    contract: BootstrapContract
    candidate_commit: str
    payload_sha256: str
    changed: bool

    def result(self, *, applied: bool) -> BootstrapPlan:
        return BootstrapPlan(
            schema=PREPARATION_SCHEMA,
            release_contract=self.contract.release_contract,
            release_record=self.contract.release_record,
            version=self.contract.version,
            candidate_commit=self.candidate_commit,
            lock_sha256=self.contract.from_lock_sha256,
            evaluator_archive_name=self.contract.evaluator_archive_name,
            evaluator_archive_sha256=self.contract.evaluator_archive_sha256,
            evaluator_payload_sha256=self.payload_sha256,
            evaluator_evidence_path=self.evidence_path.relative_to(self.root).as_posix(),
            evaluator_evidence_sha256=hashlib.sha256(self.evidence_bytes).hexdigest(),
            release_record_path=self.record_path.relative_to(self.root).as_posix(),
            changed=self.changed,
            applied=applied,
        )


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise ReleaseBootstrapError(f"cannot hash file: {path}") from exc
    return digest.hexdigest()


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ReleaseBootstrapError(f"JSON object repeats field: {key}")
        result[key] = value
    return result


def _canonical_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True) + "\n").encode(
        "utf-8"
    )


def _canonical_utf8_text_lf(raw: bytes, label: str) -> bytes:
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ReleaseBootstrapError(f"{label} must use UTF-8 without a byte-order mark")
    try:
        text = raw.decode("utf-8")
    except UnicodeError as exc:
        raise ReleaseBootstrapError(f"{label} must use UTF-8") from exc
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def _read_front_matter(path: Path, label: str) -> tuple[dict[str, Any], bytes, list[str], int]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise ReleaseBootstrapError(f"cannot read {label}: {path}") from exc
    if not raw or len(raw) > MAX_RECORD_BYTES or raw.startswith(b"\xef\xbb\xbf"):
        raise ReleaseBootstrapError(f"{label} bytes are invalid")
    try:
        text = raw.decode("utf-8")
    except UnicodeError as exc:
        raise ReleaseBootstrapError(f"{label} must use UTF-8 without a byte-order mark") from exc
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "+++":
        raise ReleaseBootstrapError(f"{label} has no TOML front matter")
    closing = next((index for index, line in enumerate(lines[1:], 1) if line.strip() == "+++"), -1)
    if closing < 0:
        raise ReleaseBootstrapError(f"{label} front matter is not closed")
    try:
        metadata = tomllib.loads("".join(lines[1:closing]))
    except tomllib.TOMLDecodeError as exc:
        raise ReleaseBootstrapError(f"{label} metadata is invalid: {exc}") from exc
    if not isinstance(metadata, dict):
        raise ReleaseBootstrapError(f"{label} metadata must be a TOML table")
    return metadata, raw, lines, closing


def _path_has_link(path: Path, stop: Path | None = None) -> bool:
    probe = path
    while True:
        if probe.is_symlink() or (hasattr(probe, "is_junction") and probe.is_junction()):
            return True
        if probe == probe.parent or (stop is not None and probe == stop):
            return False
        probe = probe.parent


def _repository_file(root: Path, supplied: Path, label: str) -> Path:
    if supplied.is_absolute() or ".." in supplied.parts:
        raise ReleaseBootstrapError(f"{label} must be repository-relative")
    candidate = root / supplied
    if _path_has_link(candidate, root):
        raise ReleaseBootstrapError(f"{label} must not traverse a link")
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root)
    except (OSError, ValueError) as exc:
        raise ReleaseBootstrapError(f"{label} must resolve inside the repository") from exc
    if not resolved.is_file():
        raise ReleaseBootstrapError(f"{label} must be an ordinary file")
    return resolved


def _ordinary_external_file(path: Path, label: str) -> Path:
    if _path_has_link(path):
        raise ReleaseBootstrapError(f"{label} must not traverse a link")
    try:
        resolved = path.resolve(strict=True)
    except OSError as exc:
        raise ReleaseBootstrapError(f"{label} does not exist") from exc
    if not resolved.is_file():
        raise ReleaseBootstrapError(f"{label} must be an ordinary file")
    return resolved


def _safe_interpreter(
    path: Path,
    label: str,
    *,
    checkout_root: Path | None = None,
    declared_root: Path | None = None,
) -> interpreter_safety.SafeEntryPoint:
    """Accept an external interpreter through the declared safety rule.

    An interpreter is not an ordinary external file: a POSIX virtual
    environment normally exposes ``bin/python`` as a terminal symbolic link,
    and the lexical path is the execution boundary rather than the resolved
    system binary. Refusals are reported with their declared case identifier so
    the diagnostic names the rule that rejected the path.
    """

    try:
        return interpreter_safety.evaluate(
            path, checkout_root=checkout_root, declared_root=declared_root
        )
    except interpreter_safety.InterpreterSafetyRefusal as refusal:
        raise ReleaseBootstrapError(
            f"{label} is refused by {refusal.case}: {refusal.detail}"
        ) from refusal
    except interpreter_safety.InterpreterSafetyError as exc:
        raise ReleaseBootstrapError(f"{label} cannot be evaluated: {exc}") from exc


def _require_sha(value: Any, label: str) -> str:
    if not isinstance(value, str) or SHA256_PATTERN.fullmatch(value) is None:
        raise ReleaseBootstrapError(f"{label} must be 64 lowercase hexadecimal characters")
    return value


def _require_version(value: Any, label: str) -> str:
    if not isinstance(value, str) or VERSION_PATTERN.fullmatch(value) is None:
        raise ReleaseBootstrapError(f"{label} is invalid")
    return value


def parse_bootstrap_contract(metadata: dict[str, Any]) -> BootstrapContract:
    contract_id = metadata.get("id")
    if (
        metadata.get("type") != "release_contract"
        or metadata.get("status") != "approved"
        or not isinstance(contract_id, str)
        or ARTIFACT_ID_PATTERN.fullmatch(contract_id) is None
    ):
        raise ReleaseBootstrapError("bootstrap requires one approved release_contract")
    value = metadata.get("bootstrap")
    if not isinstance(value, dict) or set(value) != BOOTSTRAP_KEYS:
        missing = sorted(BOOTSTRAP_KEYS - set(value)) if isinstance(value, dict) else sorted(BOOTSTRAP_KEYS)
        extra = sorted(set(value) - BOOTSTRAP_KEYS) if isinstance(value, dict) else []
        details = []
        if missing:
            details.append(f"missing {', '.join(missing)}")
        if extra:
            details.append(f"unexpected {', '.join(extra)}")
        raise ReleaseBootstrapError(f"bootstrap field set is invalid ({'; '.join(details)})")
    if value.get("schema") != BOOTSTRAP_SCHEMA:
        raise ReleaseBootstrapError(f"bootstrap schema must be {BOOTSTRAP_SCHEMA}")
    release_record = value.get("release_record")
    if not isinstance(release_record, str) or not release_record.startswith("RLS-") or ARTIFACT_ID_PATTERN.fullmatch(release_record) is None:
        raise ReleaseBootstrapError("bootstrap release_record is invalid")
    version = _require_version(value.get("version"), "bootstrap version")
    lock_schema = value.get("from_lock_schema")
    if type(lock_schema) is not int or lock_schema != 2:
        raise ReleaseBootstrapError("bootstrap from_lock_schema must be integer 2")
    evaluator_version = _require_version(value.get("evaluator_version"), "bootstrap evaluator_version")
    archive_name = value.get("evaluator_archive_name")
    expected_name = f"se_harness-{evaluator_version.replace('-', '_')}-py3-none-any.whl"
    if (
        not isinstance(archive_name, str)
        or PurePosixPath(archive_name).name != archive_name
        or "\\" in archive_name
        or archive_name != expected_name
    ):
        raise ReleaseBootstrapError("bootstrap evaluator_archive_name is invalid")
    return BootstrapContract(
        release_contract=contract_id,
        release_record=release_record,
        version=version,
        from_lock_schema=lock_schema,
        from_lock_tool_version=_require_version(
            value.get("from_lock_tool_version"), "bootstrap from_lock_tool_version"
        ),
        from_lock_sha256=_require_sha(value.get("from_lock_sha256"), "bootstrap from_lock_sha256"),
        evaluator_version=evaluator_version,
        evaluator_archive_name=archive_name,
        evaluator_archive_sha256=_require_sha(
            value.get("evaluator_archive_sha256"), "bootstrap evaluator_archive_sha256"
        ),
    )


def _relations(metadata: dict[str, Any], name: str) -> list[str]:
    relations = metadata.get("relations")
    value = relations.get(name) if isinstance(relations, dict) else None
    if not isinstance(value, list) or not value or not all(isinstance(item, str) for item in value):
        raise ReleaseBootstrapError(f"relation '{name}' must be a non-empty string list")
    if len(set(value)) != len(value):
        raise ReleaseBootstrapError(f"relation '{name}' contains duplicates")
    return value


def _artifact_catalog(root: Path) -> dict[str, tuple[Path, dict[str, Any]]]:
    catalog: dict[str, tuple[Path, dict[str, Any]]] = {}
    engineering = root / "docs" / "engineering"
    for path in sorted(engineering.rglob("*.md")):
        if not path.is_file() or _path_has_link(path, root):
            continue
        try:
            metadata, _raw, _lines, _closing = _read_front_matter(path, "engineering artifact")
        except ReleaseBootstrapError:
            continue
        artifact_id = metadata.get("id")
        if isinstance(artifact_id, str):
            if artifact_id in catalog:
                raise ReleaseBootstrapError(f"artifact ID is ambiguous: {artifact_id}")
            catalog[artifact_id] = (path, metadata)
    return catalog


def _validate_release_graph(
    root: Path,
    record: dict[str, Any],
    contract_metadata: dict[str, Any],
    contract: BootstrapContract,
) -> str:
    if record.get("type") != "release_record" or record.get("status") != "ready":
        raise ReleaseBootstrapError("bootstrap binding requires one predecessor-prepared ready release_record")
    if record.get("id") != contract.release_record or record.get("version") != contract.version:
        raise ReleaseBootstrapError("release record ID or version differs from the bootstrap contract")
    if _relations(record, "satisfies") != [contract.release_contract]:
        raise ReleaseBootstrapError("release record must satisfy exactly the bootstrap release contract")
    gated_work = _relations(contract_metadata, "gates")
    released_work = _relations(record, "releases_work")
    if len(gated_work) != len(released_work) or set(gated_work) != set(released_work):
        raise ReleaseBootstrapError("release record work set differs from the release contract")
    verification_ids = _relations(record, "includes_verification")
    commit = record.get("commit")
    object_format = record.get("git_object_format")
    pattern = COMMIT_PATTERNS.get(object_format)
    if not isinstance(commit, str) or pattern is None or pattern.fullmatch(commit) is None:
        raise ReleaseBootstrapError("release record candidate identity is invalid")
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--verify", f"{commit}^{{commit}}"],
            check=False,
            capture_output=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise ReleaseBootstrapError("candidate Git identity could not be resolved") from exc
    resolved_commit = completed.stdout.decode("ascii", "replace").strip().lower()
    if completed.returncode != 0 or resolved_commit != commit:
        raise ReleaseBootstrapError("release record candidate does not resolve as one exact commit")
    catalog = _artifact_catalog(root)
    verified_work: set[str] = set()
    for verification_id in verification_ids:
        item = catalog.get(verification_id)
        if item is None or item[1].get("type") != "verification_record":
            raise ReleaseBootstrapError(f"included verification record is missing: {verification_id}")
        verification = item[1]
        if verification.get("status") not in {"verified", "released"}:
            raise ReleaseBootstrapError(f"included verification record is not verified: {verification_id}")
        if verification.get("commit") != commit or verification.get("git_object_format") != object_format:
            raise ReleaseBootstrapError(f"included verification candidate differs: {verification_id}")
        verified_work.update(_relations(verification, "verifies_work_order"))
    if verified_work != set(released_work):
        raise ReleaseBootstrapError("included verification coverage differs from the release work set")
    return commit


def _validate_bootstrap_cardinality(
    root: Path,
    selected_path: Path,
    selected: BootstrapContract,
) -> None:
    approved: list[tuple[Path, BootstrapContract]] = []
    for path, metadata in _artifact_catalog(root).values():
        if (
            metadata.get("type") == "release_contract"
            and metadata.get("status") == "approved"
            and "bootstrap" in metadata
        ):
            approved.append((path, parse_bootstrap_contract(metadata)))
    if len(approved) != 1:
        raise ReleaseBootstrapError(
            "repository must contain exactly one approved predecessor bootstrap contract"
        )
    approved_path, approved_contract = approved[0]
    if approved_path != selected_path or approved_contract != selected:
        raise ReleaseBootstrapError(
            "selected release contract is not the repository's exact approved bootstrap contract"
        )


def _validate_old_root(root: Path, contract: BootstrapContract) -> None:
    config_path = root / ".engineering-harness.toml"
    lock_path = root / LOCK_RELATIVE
    if _path_has_link(config_path, root) or _path_has_link(lock_path, root):
        raise ReleaseBootstrapError("standard configuration and lock must not traverse links")
    try:
        config = tomllib.loads(config_path.read_text(encoding="utf-8"))
        lock_raw = lock_path.read_bytes()
        lock = json.loads(lock_raw.decode("utf-8"), object_pairs_hook=_unique_object)
    except (OSError, UnicodeError, tomllib.TOMLDecodeError, json.JSONDecodeError) as exc:
        raise ReleaseBootstrapError("standard configuration or lock is invalid") from exc
    harness = config.get("harness") if isinstance(config, dict) else None
    if not isinstance(harness, dict) or harness.get("tool_version") != contract.from_lock_tool_version:
        raise ReleaseBootstrapError("configured evaluator version differs from the bootstrap contract")
    # The mode comes from the lock's declared hash-bound class, not from a local
    # canonicalization, so this caller and upgrade authorization cannot diverge
    # again. The byte-order-mark refusal below is retained: it is a separate
    # existing check that the declared mode does not perform.
    if lock_raw.startswith(b"\xef\xbb\xbf"):
        raise ReleaseBootstrapError("standard lock must use UTF-8 without a byte-order mark")
    try:
        lock_match = compare_declared_digest(LOCK_RELATIVE, lock_raw, contract.from_lock_sha256)
    except HashBoundError as exc:
        raise ReleaseBootstrapError(
            f"cannot compare the standard lock under its declared hash-bound class: {exc}"
        ) from exc
    if lock_match == MATCH_LEGACY_NEWLINE:
        raise ReleaseBootstrapError(
            "standard lock matches the bootstrap contract only as a legacy newline variant; "
            "this contract records a canonical digest"
        )
    if lock_match != MATCH_DECLARED:
        raise ReleaseBootstrapError("canonical standard lock digest differs from the bootstrap contract")
    if (
        not isinstance(lock, dict)
        or lock.get("schema") != contract.from_lock_schema
        or lock.get("tool_version") != contract.from_lock_tool_version
        or lock.get("hash_algorithm") != "sha256"
        or lock.get("hash_mode") != "utf8-text-lf-v1"
    ):
        raise ReleaseBootstrapError("standard schema-2 lock differs from the bootstrap contract")
    if contract.evaluator_version != contract.from_lock_tool_version:
        raise ReleaseBootstrapError("bootstrap evaluator and old-lock versions differ")


def _within(path: Path, parent: Path) -> bool:
    try:
        path.resolve(strict=True).relative_to(parent.resolve(strict=True))
    except (OSError, ValueError):
        return False
    return True


def _normalize_origin(path: Path, evaluator_root: Path) -> str:
    if not _within(path, evaluator_root):
        raise ReleaseBootstrapError("released-evaluator origin is outside its declared root")
    relative = path.resolve(strict=True).relative_to(evaluator_root.resolve(strict=True)).as_posix()
    return "<evaluator-root>" + (f"/{relative}" if relative else "")


def _lexical_origin(path: Path, evaluator_root: Path) -> str:
    """Normalize an interpreter origin without resolving it.

    The interpreter is the one origin that may legitimately be a terminal
    symbolic link, so resolving it before normalization would leave the
    declared root and refuse every POSIX virtual environment.
    """

    lexical = Path(os.path.abspath(path))
    try:
        relative = lexical.relative_to(Path(os.path.abspath(evaluator_root))).as_posix()
    except ValueError as exc:
        raise ReleaseBootstrapError(
            "released-evaluator origin is outside its declared root"
        ) from exc
    return "<evaluator-root>" + (f"/{relative}" if relative else "")


def _run_released_evaluator(
    root: Path,
    evaluator_python: Path,
    evaluator_entry_point: Path,
    contract: BootstrapContract,
) -> dict[str, Any]:
    safe = _safe_interpreter(
        evaluator_python, "released-evaluator interpreter", checkout_root=root
    )
    evaluator_root = safe.environment_root
    if not _within(evaluator_entry_point, evaluator_root):
        raise ReleaseBootstrapError("released-evaluator entry point is outside the interpreter environment")
    environment = dict(os.environ)
    environment.pop("PYTHONPATH", None)
    identity_command = [
        str(safe.entry_point),
        "-I",
        "-m",
        "se_harness",
        "identity",
        "--role",
        "released-evaluator",
        "--expected-version",
        contract.evaluator_version,
        "--expected-root",
        str(evaluator_root),
        "--checkout-root",
        str(root),
        "--entry-point",
        str(evaluator_entry_point),
        "--require-isolated-python",
        "--require-entry-point",
    ]
    try:
        identity_run = subprocess.run(
            identity_command,
            cwd=root,
            env=environment,
            check=False,
            capture_output=True,
            timeout=60,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise ReleaseBootstrapError("released-evaluator identity command failed to start") from exc
    if identity_run.returncode != 0:
        detail = identity_run.stderr.decode("utf-8", "replace").strip()
        raise ReleaseBootstrapError(f"released-evaluator identity failed: {detail or 'no diagnostic'}")
    try:
        identity = json.loads(identity_run.stdout.decode("utf-8"), object_pairs_hook=_unique_object)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ReleaseBootstrapError("released-evaluator identity output is invalid") from exc
    required = {
        "schema",
        "passed",
        "role",
        "python_executable",
        "harness_version",
        "module_origin",
        "distribution_origin",
        "template_origin",
        "entry_point_origin",
        "expected_root",
        "checkout_root",
        "candidate_commit",
        "isolated_python",
        "user_site_enabled",
        "pythonpath_present",
        "diagnostics",
    }
    if not isinstance(identity, dict) or not required.issubset(identity):
        raise ReleaseBootstrapError("released-evaluator identity field set is incomplete")
    if (
        identity.get("schema") not in RUNTIME_IDENTITY_SCHEMAS
        or identity.get("passed") is not True
        or identity.get("role") != "released-evaluator"
        or identity.get("harness_version") != contract.evaluator_version
        or identity.get("candidate_commit") is not None
        or identity.get("isolated_python") is not True
        or identity.get("user_site_enabled") is not False
        or identity.get("pythonpath_present") is not False
        or identity.get("diagnostics") != []
    ):
        raise ReleaseBootstrapError("released-evaluator identity proof is not acceptable")
    reported_python = identity.get("python_executable")
    if (
        not isinstance(reported_python, str)
        or Path(os.path.abspath(reported_python)) != safe.entry_point
    ):
        raise ReleaseBootstrapError("released-evaluator identity python_executable differs")
    exact_paths = {
        "entry_point_origin": evaluator_entry_point,
        "expected_root": evaluator_root,
        "checkout_root": root,
    }
    for field, expected in exact_paths.items():
        value = identity.get(field)
        try:
            observed = Path(value).resolve(strict=True) if isinstance(value, str) else None
        except OSError:
            observed = None
        if observed != expected.resolve(strict=True):
            raise ReleaseBootstrapError(f"released-evaluator identity {field} differs")
    reported_facts = {
        "python_entry_is_link": safe.entry_is_link,
        "python_binary_position": safe.binary_position,
        "python_binary_sha256": safe.binary_sha256,
    }
    for field, expected_fact in reported_facts.items():
        if field in identity and identity[field] != expected_fact:
            raise ReleaseBootstrapError(f"released-evaluator identity {field} differs")
    for field in ("module_origin", "distribution_origin", "template_origin"):
        value = identity.get(field)
        if not isinstance(value, str) or not _within(Path(value), evaluator_root):
            raise ReleaseBootstrapError(f"released-evaluator {field} is outside its environment")
        if _within(Path(value), root):
            raise ReleaseBootstrapError(f"released-evaluator {field} resolves inside the checkout")
    validate_command = [str(evaluator_python), "-I", "-m", "se_harness", "validate", str(root), "--json"]
    try:
        validation = subprocess.run(
            validate_command,
            cwd=root,
            env=environment,
            check=False,
            capture_output=True,
            timeout=120,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise ReleaseBootstrapError("released-evaluator validation failed to start") from exc
    if validation.returncode != 0:
        raise ReleaseBootstrapError("released-evaluator validation did not pass before binding")
    return identity


def _installed_payload(identity: dict[str, Any], evaluator_root: Path) -> str:
    module = Path(identity["module_origin"]).resolve(strict=True)
    package_root = module.parent
    templates_root = Path(identity["template_origin"]).resolve(strict=True)
    if package_root.name != "se_harness" or not _within(package_root, evaluator_root):
        raise ReleaseBootstrapError("released-evaluator package origin is invalid")
    entries: list[dict[str, Any]] = []
    total = 0
    files: list[tuple[str, Path]] = []
    for prefix, payload_root in (
        ("se_harness", package_root),
        ("templates/repository/standard", templates_root),
    ):
        for path in payload_root.rglob("*"):
            if _path_has_link(path, evaluator_root):
                raise ReleaseBootstrapError("released-evaluator installed payload contains a link")
            if not path.is_file() or "__pycache__" in path.parts or path.suffix.lower() in {".pyc", ".pyo"}:
                continue
            files.append((f"{prefix}/{path.relative_to(payload_root).as_posix()}", path))
    files.sort(key=lambda item: item[0])
    if not files or len(files) > MAX_PAYLOAD_FILES:
        raise ReleaseBootstrapError("released-evaluator installed payload file count is invalid")
    for relative, path in files:
        try:
            content = path.read_bytes()
        except OSError as exc:
            raise ReleaseBootstrapError(f"cannot read installed payload member: {relative}") from exc
        if len(content) > MAX_PAYLOAD_MEMBER_BYTES:
            raise ReleaseBootstrapError(f"installed payload member is too large: {relative}")
        total += len(content)
        if total > MAX_PAYLOAD_BYTES:
            raise ReleaseBootstrapError("released-evaluator installed payload is too large")
        entries.append(
            {"bytes": len(content), "path": relative, "sha256": hashlib.sha256(content).hexdigest()}
        )
    return hashlib.sha256(_canonical_json({"files": entries, "schema": PAYLOAD_MANIFEST})).hexdigest()


def _wheel_payload(wheel: Path, version: str) -> str:
    template_prefix = (
        f"se_harness-{version}.data/data/share/se-harness/templates/repository/standard/"
    )
    entries: list[dict[str, Any]] = []
    seen: set[str] = set()
    total = 0
    try:
        with zipfile.ZipFile(wheel) as archive:
            members = archive.infolist()
            if len(members) > MAX_PAYLOAD_FILES * 4:
                raise ReleaseBootstrapError("released-evaluator wheel has too many members")
            for member in members:
                name = member.filename
                path = PurePosixPath(name)
                if (
                    not name
                    or "\\" in name
                    or path.is_absolute()
                    or any(part in {"", ".", ".."} for part in path.parts)
                    or name in seen
                ):
                    raise ReleaseBootstrapError("released-evaluator wheel contains an unsafe member")
                seen.add(name)
                mode = (member.external_attr >> 16) & 0o170000
                if mode == stat.S_IFLNK:
                    raise ReleaseBootstrapError("released-evaluator wheel contains a symbolic link")
                if member.is_dir():
                    continue
                logical: str | None = None
                if name.startswith("se_harness/"):
                    logical = name
                elif name.startswith(template_prefix):
                    logical = "templates/repository/standard/" + name.removeprefix(template_prefix)
                if logical is None:
                    continue
                if member.file_size > MAX_PAYLOAD_MEMBER_BYTES:
                    raise ReleaseBootstrapError(f"released-evaluator wheel member is too large: {name}")
                content = archive.read(member)
                if len(content) != member.file_size:
                    raise ReleaseBootstrapError(f"released-evaluator wheel member size differs: {name}")
                total += len(content)
                if total > MAX_PAYLOAD_BYTES:
                    raise ReleaseBootstrapError("released-evaluator wheel payload is too large")
                entries.append(
                    {"bytes": len(content), "path": logical, "sha256": hashlib.sha256(content).hexdigest()}
                )
    except (OSError, zipfile.BadZipFile, RuntimeError) as exc:
        raise ReleaseBootstrapError("released-evaluator wheel is not a safe ZIP archive") from exc
    entries.sort(key=lambda item: item["path"])
    if not entries or len(entries) > MAX_PAYLOAD_FILES:
        raise ReleaseBootstrapError("released-evaluator wheel payload file count is invalid")
    logical_paths = [entry["path"] for entry in entries]
    if len(set(logical_paths)) != len(logical_paths):
        raise ReleaseBootstrapError("released-evaluator wheel payload path is ambiguous")
    if not any(path.startswith("se_harness/") for path in logical_paths) or not any(
        path.startswith("templates/repository/standard/") for path in logical_paths
    ):
        raise ReleaseBootstrapError("released-evaluator wheel payload is incomplete")
    return hashlib.sha256(_canonical_json({"files": entries, "schema": PAYLOAD_MANIFEST})).hexdigest()


def _evidence_bytes(
    identity: dict[str, Any],
    evaluator_root: Path,
    contract: BootstrapContract,
    payload_sha256: str,
) -> bytes:
    evidence = {
        "schema": EVIDENCE_SCHEMA,
        "role": "released-evaluator",
        "evaluator": {
            "version": contract.evaluator_version,
            "payload_manifest": PAYLOAD_MANIFEST,
            "payload_sha256": payload_sha256,
            "archive_name": contract.evaluator_archive_name,
            "archive_sha256": contract.evaluator_archive_sha256,
        },
        "origins": {
            "python_executable": _lexical_origin(Path(identity["python_executable"]), evaluator_root),
            "module": _normalize_origin(Path(identity["module_origin"]), evaluator_root),
            "distribution": _normalize_origin(Path(identity["distribution_origin"]), evaluator_root),
            "templates": _normalize_origin(Path(identity["template_origin"]), evaluator_root),
            "entry_point": _normalize_origin(Path(identity["entry_point_origin"]), evaluator_root),
        },
        "environment": {
            "isolated_python": True,
            "user_site_enabled": False,
            "pythonpath_present": False,
            "entry_point_resolved": True,
            "checkout_excluded": True,
        },
        "diagnostics": [],
    }
    raw = _canonical_json(evidence)
    if len(raw) > MAX_EVIDENCE_BYTES:
        raise ReleaseBootstrapError("canonical evaluator evidence exceeds the byte limit")
    return raw


def _updated_record(
    metadata: dict[str, Any],
    lines: list[str],
    closing: int,
    evidence_relative: str,
    evidence_sha256: str,
) -> bytes:
    existing_fields = {
        "preparation_schema": metadata.get("preparation_schema"),
        "evaluator_evidence_path": metadata.get("evaluator_evidence_path"),
        "evaluator_evidence_sha256": metadata.get("evaluator_evidence_sha256"),
    }
    expected_fields = {
        "preparation_schema": PREPARATION_SCHEMA,
        "evaluator_evidence_path": evidence_relative,
        "evaluator_evidence_sha256": evidence_sha256,
    }
    if any(value is not None for value in existing_fields.values()):
        if existing_fields != expected_fields:
            raise ReleaseBootstrapError("release record contains a conflicting bootstrap binding")
        return "".join(lines).encode("utf-8")
    relation_index = next(
        (index for index, line in enumerate(lines[1:closing], 1) if line.strip() == "[relations]"), -1
    )
    if relation_index < 0:
        raise ReleaseBootstrapError("release record has no relations table")
    newline = "\r\n" if lines[0].endswith("\r\n") else "\n"
    insertion = (
        f'preparation_schema = "{PREPARATION_SCHEMA}"{newline}'
        f'evaluator_evidence_path = "{evidence_relative}"{newline}'
        f'evaluator_evidence_sha256 = "{evidence_sha256}"{newline}{newline}'
    )
    return ("".join(lines[:relation_index]) + insertion + "".join(lines[relation_index:])).encode("utf-8")


def _prepare(
    repository: Path,
    release_record: Path,
    release_contract: Path,
    evaluator_python: Path,
    evaluator_entry_point: Path,
    evaluator_wheel: Path,
) -> _PreparedBinding:
    try:
        root = repository.resolve(strict=True)
    except OSError as exc:
        raise ReleaseBootstrapError("repository does not exist") from exc
    record_path = _repository_file(root, release_record, "release record")
    contract_path = _repository_file(root, release_contract, "release contract")
    python_entry = _safe_interpreter(
        evaluator_python, "released-evaluator interpreter", checkout_root=root
    )
    entry_point_path = _ordinary_external_file(evaluator_entry_point, "released-evaluator entry point")
    wheel_path = _ordinary_external_file(evaluator_wheel, "released-evaluator wheel")
    contract_metadata, _contract_raw, _contract_lines, _contract_closing = _read_front_matter(
        contract_path, "release contract"
    )
    contract = parse_bootstrap_contract(contract_metadata)
    _validate_bootstrap_cardinality(root, contract_path, contract)
    if wheel_path.name != contract.evaluator_archive_name:
        raise ReleaseBootstrapError("released-evaluator wheel name differs from the bootstrap contract")
    if _sha256_file(wheel_path) != contract.evaluator_archive_sha256:
        raise ReleaseBootstrapError("released-evaluator wheel digest differs from the bootstrap contract")
    _validate_old_root(root, contract)
    record_metadata, record_raw, lines, closing = _read_front_matter(record_path, "release record")
    candidate_commit = _validate_release_graph(root, record_metadata, contract_metadata, contract)
    identity = _run_released_evaluator(root, python_entry.entry_point, entry_point_path, contract)
    evaluator_root = python_entry.environment_root
    payload_sha256 = _installed_payload(identity, evaluator_root)
    wheel_payload_sha256 = _wheel_payload(wheel_path, contract.evaluator_version)
    if wheel_payload_sha256 != payload_sha256:
        raise ReleaseBootstrapError(
            "released-evaluator installed payload differs from the exact public wheel"
        )
    evidence = _evidence_bytes(identity, evaluator_root, contract, payload_sha256)
    evidence_path = record_path.parent.parent / "evidence" / f"{contract.release_record}-evaluator.json"
    if not evidence_path.parent.is_dir() or _path_has_link(evidence_path.parent, root):
        raise ReleaseBootstrapError("release evidence directory is unavailable or linked")
    try:
        evidence_path.parent.resolve(strict=True).relative_to(root)
    except (OSError, ValueError) as exc:
        raise ReleaseBootstrapError("release evidence directory escapes the repository") from exc
    evidence_relative = evidence_path.relative_to(root).as_posix()
    evidence_sha256 = hashlib.sha256(evidence).hexdigest()
    updated = _updated_record(record_metadata, lines, closing, evidence_relative, evidence_sha256)
    evidence_exists = evidence_path.exists()
    if evidence_exists:
        if _path_has_link(evidence_path, root) or not evidence_path.is_file():
            raise ReleaseBootstrapError("existing evaluator evidence destination is not an ordinary file")
        try:
            existing_evidence = evidence_path.read_bytes()
        except OSError as exc:
            raise ReleaseBootstrapError("existing evaluator evidence cannot be read") from exc
        if existing_evidence != evidence:
            raise ReleaseBootstrapError("existing evaluator evidence differs from canonical bytes")
    binding_already_present = updated == record_raw
    if evidence_exists != binding_already_present:
        raise ReleaseBootstrapError("partial bootstrap binding exists; refusing repair or overwrite")
    return _PreparedBinding(
        root=root,
        record_path=record_path,
        record_original=record_raw,
        record_updated=updated,
        evidence_path=evidence_path,
        evidence_bytes=evidence,
        contract=contract,
        candidate_commit=candidate_commit,
        payload_sha256=payload_sha256,
        changed=not binding_already_present,
    )


def plan_bootstrap_binding(
    repository: Path,
    release_record: Path,
    release_contract: Path,
    evaluator_python: Path,
    evaluator_entry_point: Path,
    evaluator_wheel: Path,
) -> BootstrapPlan:
    """Validate every input and return a read-only exact binding plan."""
    prepared = _prepare(
        repository,
        release_record,
        release_contract,
        evaluator_python,
        evaluator_entry_point,
        evaluator_wheel,
    )
    return prepared.result(applied=False)


def _atomic_replace(path: Path, payload: bytes) -> None:
    mode = stat.S_IMODE(path.stat().st_mode)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary_name, mode)
        os.replace(temporary_name, path)
    except OSError as exc:
        raise ReleaseBootstrapError(f"cannot replace release record atomically: {exc}") from exc
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)


def apply_bootstrap_binding(
    repository: Path,
    release_record: Path,
    release_contract: Path,
    evaluator_python: Path,
    evaluator_entry_point: Path,
    evaluator_wheel: Path,
) -> BootstrapPlan:
    """Apply one exclusive-create plus atomic RLS update, rolling back on failure."""
    prepared = _prepare(
        repository,
        release_record,
        release_contract,
        evaluator_python,
        evaluator_entry_point,
        evaluator_wheel,
    )
    if not prepared.changed:
        return prepared.result(applied=True)
    created = False
    try:
        descriptor = os.open(prepared.evidence_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        created = True
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(prepared.evidence_bytes)
            handle.flush()
            os.fsync(handle.fileno())
        if prepared.record_path.read_bytes() != prepared.record_original:
            raise ReleaseBootstrapError("release record changed after bootstrap planning")
        _atomic_replace(prepared.record_path, prepared.record_updated)
    except (OSError, ReleaseBootstrapError) as exc:
        if created:
            try:
                prepared.evidence_path.unlink()
            except OSError as rollback_exc:
                raise ReleaseBootstrapError(
                    f"bootstrap binding failed and evidence rollback failed: {rollback_exc}"
                ) from exc
        if isinstance(exc, ReleaseBootstrapError):
            raise
        raise ReleaseBootstrapError(f"cannot create evaluator evidence exclusively: {exc}") from exc
    return prepared.result(applied=True)


def bootstrap_contracts(paths: Iterable[Path]) -> list[BootstrapContract]:
    """Parse approved bootstrap contracts from an explicitly bounded path set."""
    result: list[BootstrapContract] = []
    for path in paths:
        metadata, _raw, _lines, _closing = _read_front_matter(path, "release contract")
        if metadata.get("type") == "release_contract" and "bootstrap" in metadata:
            result.append(parse_bootstrap_contract(metadata))
    return result
