#!/usr/bin/env python3
"""Validate specification-driven engineering artifacts.

The validator intentionally uses only the Python 3.11+ standard library so it can
run before the repository's normal toolchain is available.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Any, Iterable

try:
    import tomllib
except ModuleNotFoundError as exc:  # pragma: no cover - version guard
    raise SystemExit("Python 3.11 or later is required (missing tomllib).") from exc

_LAYOUT_PATH = Path(__file__).with_name("artifact_layout_registry.py")
_LAYOUT_SPEC = importlib.util.spec_from_file_location("_se_harness_artifact_layout_registry", _LAYOUT_PATH)
if _LAYOUT_SPEC is None or _LAYOUT_SPEC.loader is None:
    raise RuntimeError(f"cannot load artifact layout registry: {_LAYOUT_PATH}")
_LAYOUT = importlib.util.module_from_spec(_LAYOUT_SPEC)
_LAYOUT_SPEC.loader.exec_module(_LAYOUT)
ARTIFACT_DIRECTORIES = _LAYOUT.ARTIFACT_DIRECTORIES
ARTIFACT_PREFIXES = _LAYOUT.ARTIFACT_PREFIXES
artifact_domain_from_relative_path = _LAYOUT.artifact_domain_from_relative_path
canonical_artifact_relative_path = _LAYOUT.canonical_artifact_relative_path
common_artifact_domain = _LAYOUT.common_artifact_domain
repository_record_relative_path = _LAYOUT.repository_record_relative_path


TAXONOMY_VERSION = "se-harness-validation-taxonomy-v1"
VALIDATION_PLANES = ("structure", "governance", "policy", "maintenance")

TYPE_PREFIX = {**ARTIFACT_PREFIXES, "risk_acceptance": "RISK-"}

ID_PATTERN = re.compile(r"^[A-Z][A-Z0-9-]*-\d{3}$")
EVIDENCE_WORK_ORDER_PATTERN = re.compile(
    r"^(WO-(?:[A-Z0-9-]*-)?\d{3})(?:-|\.|$)"
)
ISO_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
EVALUATOR_EVIDENCE_SCHEMA = "se-harness-evaluator-evidence-v1"
EVALUATOR_PAYLOAD_MANIFEST = "se-harness-installed-payload-v1"
EVALUATOR_EVIDENCE_MAX_BYTES = 64 * 1024
EVALUATOR_ORIGIN_PATTERN = re.compile(r"^<evaluator-root>(?:/[A-Za-z0-9._+()@ -]+)*$")
EVALUATOR_VERSION_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.!+\-]{0,127}$")
RELEASE_BOOTSTRAP_SCHEMA = "se-harness-release-bootstrap-v1"
PREDECESSOR_PREPARATION_SCHEMA = "se-harness-predecessor-bootstrap-v1"
PREDECESSOR_VIEW_EVIDENCE_SCHEMA = "se-harness-predecessor-preparation-view-v1"
PREDECESSOR_VIEW_EVIDENCE_MAX_BYTES = 128 * 1024
RELEASE_BOOTSTRAP_KEYS = {
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
LEGACY_RELEASES_WITHOUT_EVALUATOR_EVIDENCE = frozenset(
    {"RLS-SEH-001", "RLS-SEH-002", "RLS-SEH-004", "RLS-SEH-005", "RLS-SEH-006", "RLS-SEH-007"}
)
GIT_COMMIT_PATTERNS = {
    "sha1": re.compile(r"^[0-9a-f]{40}$"),
    "sha256": re.compile(r"^[0-9a-f]{64}$"),
}

RELEASABLE_WORK_STATUSES = {
    "implemented",
    "verified",
    "released",
}


@dataclass(frozen=True)
class LifecycleStatePolicy:
    transitions_to: tuple[str, ...]
    grants_authority: bool
    reserves_version: bool
    transitionable: bool
    must_remain_visible: bool
    predecessor_adapter: str


_LIFECYCLE_FAMILIES = {"definition", "work_order", "verification_record", "release_record"}
_LIFECYCLE_FIELDS = {
    "transitions_to",
    "grants_authority",
    "reserves_version",
    "transitionable",
    "must_remain_visible",
    "predecessor_adapter",
}
_PREDECESSOR_ADAPTER_VALUES = {"none", "required"}
_STATE_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")


def _workflow_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise RuntimeError(f"managed workflow contract contains duplicate JSON key: {key}")
        value[key] = item
    return value


def _load_workflow_lifecycles() -> MappingProxyType:
    path = Path(__file__).resolve().parent.parent / "docs" / "engineering" / "WORKFLOW.json"
    try:
        raw = path.read_bytes()
        if len(raw) > 2_000_000:
            raise RuntimeError(f"managed workflow contract exceeds 2 MB: {path}")
        contract = json.loads(raw.decode("utf-8"), object_pairs_hook=_workflow_object)
    except RuntimeError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"cannot load managed workflow contract: {path}") from exc
    if not isinstance(contract, dict) or contract.get("schema") != "se-harness-workflow-v3":
        raise RuntimeError("managed workflow contract has an unsupported schema")
    source = contract.get("lifecycles")
    if not isinstance(source, dict) or set(source) != _LIFECYCLE_FAMILIES:
        raise RuntimeError("managed workflow contract must declare exactly the four lifecycle families")
    lifecycles: dict[str, dict[str, LifecycleStatePolicy]] = {}
    for family in sorted(_LIFECYCLE_FAMILIES):
        raw_states = source.get(family)
        if not isinstance(raw_states, dict) or not raw_states:
            raise RuntimeError(f"managed workflow lifecycle family {family} must contain states")
        states: dict[str, LifecycleStatePolicy] = {}
        for current, raw_row in raw_states.items():
            if not isinstance(current, str) or _STATE_NAME_PATTERN.fullmatch(current) is None:
                raise RuntimeError(f"managed workflow lifecycle family {family} has an invalid state")
            if not isinstance(raw_row, dict) or set(raw_row) != _LIFECYCLE_FIELDS:
                raise RuntimeError(f"managed workflow lifecycle {family}:{current} has invalid fields")
            targets = raw_row.get("transitions_to")
            if (
                not isinstance(targets, list)
                or not all(isinstance(target, str) and _STATE_NAME_PATTERN.fullmatch(target) for target in targets)
                or len(targets) != len(set(targets))
            ):
                raise RuntimeError(f"managed workflow lifecycle {family}:{current} has invalid transitions_to")
            boolean_fields = (
                "grants_authority",
                "reserves_version",
                "transitionable",
                "must_remain_visible",
            )
            if any(type(raw_row.get(field)) is not bool for field in boolean_fields):
                raise RuntimeError(f"managed workflow lifecycle {family}:{current} has a non-boolean property")
            adapter = raw_row.get("predecessor_adapter")
            if adapter not in _PREDECESSOR_ADAPTER_VALUES:
                raise RuntimeError(f"managed workflow lifecycle {family}:{current} has invalid predecessor_adapter")
            if raw_row["transitionable"] != bool(targets):
                raise RuntimeError(
                    f"managed workflow lifecycle {family}:{current} transitionable disagrees with transitions_to"
                )
            if not raw_row["must_remain_visible"]:
                raise RuntimeError(f"managed workflow lifecycle {family}:{current} must remain visible")
            if family != "release_record" and raw_row["reserves_version"]:
                raise RuntimeError(f"managed workflow lifecycle {family}:{current} cannot reserve a version")
            states[current] = LifecycleStatePolicy(
                transitions_to=tuple(targets),
                grants_authority=raw_row["grants_authority"],
                reserves_version=raw_row["reserves_version"],
                transitionable=raw_row["transitionable"],
                must_remain_visible=raw_row["must_remain_visible"],
                predecessor_adapter=adapter,
            )
        for current, row in states.items():
            unknown = set(row.transitions_to) - set(states)
            if unknown:
                raise RuntimeError(
                    f"managed workflow lifecycle {family}:{current} targets unknown state {sorted(unknown)[0]}"
                )
        lifecycles[family] = MappingProxyType(states)
    return MappingProxyType(lifecycles)


WORKFLOW_LIFECYCLES = _load_workflow_lifecycles()
WORKFLOW_TRANSITIONS = MappingProxyType({
    family: MappingProxyType(
        {state: frozenset(row.transitions_to) for state, row in states.items()}
    )
    for family, states in WORKFLOW_LIFECYCLES.items()
})
ALLOWED_STATUSES = frozenset({
    state
    for states in WORKFLOW_LIFECYCLES.values()
    for state in states
})
ACTIVE_COVERAGE_STATUSES = frozenset({
    state
    for family in ("definition", "work_order")
    for state, row in WORKFLOW_LIFECYCLES[family].items()
    if row.grants_authority
})


def _lifecycle_family(artifact_type: str) -> str:
    return artifact_type if artifact_type in {"work_order", "verification_record", "release_record"} else "definition"


def _lifecycle_policy(artifact_type: str, status: str) -> LifecycleStatePolicy | None:
    return WORKFLOW_LIFECYCLES[_lifecycle_family(artifact_type)].get(status)


def _grants_authority(artifact_type: str, status: str) -> bool:
    row = _lifecycle_policy(artifact_type, status)
    return bool(row and row.grants_authority)


def _reserves_version(status: str) -> bool:
    row = WORKFLOW_LIFECYCLES["release_record"].get(status)
    return bool(row and row.reserves_version)


def _active_record_status(artifact_type: str, status: str) -> bool:
    """Return whether a VREC/RLS is a live proposal or grants authority."""

    row = _lifecycle_policy(artifact_type, status)
    return bool(row and (row.transitionable or row.grants_authority))
DECISION_ASSESSMENT_OUTCOMES = {"adr_required", "no_significant_decision"}
DECISION_TRIGGERS = {
    "system-boundary",
    "responsibility-or-dependency-direction",
    "public-interface-or-protocol",
    "data-ownership-or-persistence",
    "security-privacy-or-trust-boundary",
    "deployment-or-operating-model",
    "concurrency-consistency-reliability-or-failure-strategy",
    "technology-framework-vendor-or-external-service",
    "material-performance-scalability-or-cost-tradeoff",
    "cross-cutting-policy",
    "difficult-to-reverse",
    "material-alternatives",
}
LEGACY_ARCHITECTURE_STATUSES = {"implemented", "verified", "released"}
MAX_ASSESSMENT_RATIONALE_LENGTH = 2000
MAX_ASSESSOR_LENGTH = 128
WORK_ORDER_ASSURANCE_VALUES = {"required", "not_required"}
WORK_ORDER_ASSURANCE_FIELDS = {
    "commit_bound_verification",
    "rationale",
    "decided_by",
}
MAX_ASSURANCE_RATIONALE_LENGTH = 2000
MAX_ASSURANCE_DECIDER_LENGTH = 128
EXCLUDED_DIRECTORY_NAMES = {"templates", "evidence", ".git", ".idea", "target", "node_modules"}

RELATION_TARGET_TYPES: dict[tuple[str, str], set[str]] = {
    ("architecture", "addresses"): {"requirement"},
    ("architecture", "conforms_to"): {"specification"},
    ("architecture", "constrains"): {"requirement", "specification"},
    ("operating_contract", "assures"): {"requirement"},
    ("verification_record", "verifies_work_order"): {"work_order"},
    ("verification_record", "conforms_to"): {"verification"},
    ("verification_record", "superseded_by"): {"verification_record"},
    ("release_record", "satisfies"): {"release_contract"},
    ("release_record", "includes_verification"): {"verification_record"},
    ("release_record", "releases_work"): {"work_order"},
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


@dataclass(frozen=True, order=True)
class Diagnostic:
    path: str
    code: str
    message: str
    plane: str

    def __post_init__(self) -> None:
        if self.plane not in VALIDATION_PLANES:
            raise ValueError(f"unknown validation plane: {self.plane!r}")


@dataclass
class Artifact:
    path: Path
    metadata: dict[str, Any]
    body: str

    @property
    def artifact_id(self) -> str:
        value = self.metadata.get("id")
        return value if isinstance(value, str) else "<unknown>"

    @property
    def artifact_type(self) -> str:
        value = self.metadata.get("type")
        return value if isinstance(value, str) else "<unknown>"

    @property
    def status(self) -> str:
        value = self.metadata.get("status")
        return value if isinstance(value, str) else "<unknown>"

    @property
    def relations(self) -> dict[str, Any]:
        value = self.metadata.get("relations", {})
        return value if isinstance(value, dict) else {}


@dataclass
class ValidationReport:
    artifacts: list[Artifact]
    errors: list[Diagnostic]
    warnings: list[Diagnostic]

    @property
    def valid(self) -> bool:
        return not self.errors

    def to_dict(self, root: Path) -> dict[str, Any]:
        def relative(path: Path) -> str:
            try:
                return path.resolve().relative_to(root.resolve()).as_posix()
            except ValueError:
                return path.as_posix()

        plane_counts = {
            plane: {
                "errors": sum(item.plane == plane for item in self.errors),
                "warnings": sum(item.plane == plane for item in self.warnings),
            }
            for plane in VALIDATION_PLANES
        }
        return {
            "taxonomy": TAXONOMY_VERSION,
            "valid": self.valid,
            "artifact_count": len(self.artifacts),
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "errors": [asdict(item) for item in sorted(self.errors)],
            "warnings": [asdict(item) for item in sorted(self.warnings)],
            "plane_counts": plane_counts,
            "artifacts": [
                {
                    "id": artifact.artifact_id,
                    "type": artifact.artifact_type,
                    "status": artifact.status,
                    "path": relative(artifact.path),
                }
                for artifact in sorted(self.artifacts, key=lambda item: (item.artifact_id, item.path.as_posix()))
            ],
        }


def load_revision_policy(repository_root: Path) -> dict[str, bool]:
    defaults = {"required_for_verified_work": False, "required_for_release": False}
    path = repository_root / ".engineering-harness.toml"
    if not path.is_file():
        return defaults
    try:
        metadata = tomllib.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError):
        return defaults
    policy = metadata.get("revision_provenance", {})
    if not isinstance(policy, dict):
        return defaults
    return {
        key: value if isinstance((value := policy.get(key)), bool) else default
        for key, default in defaults.items()
    }


def _display_path(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _is_excluded(path: Path, artifact_root: Path) -> bool:
    try:
        relative_parts = path.relative_to(artifact_root).parts
    except ValueError:
        relative_parts = path.parts
    return any(part in EXCLUDED_DIRECTORY_NAMES for part in relative_parts[:-1])


def discover_candidate_files(artifact_root: Path) -> list[Path]:
    if not artifact_root.exists():
        return []
    return sorted(
        path
        for path in artifact_root.rglob("*.md")
        if path.is_file() and not _is_excluded(path, artifact_root)
    )


def parse_formal_artifact(path: Path, report_root: Path) -> tuple[Artifact | None, Diagnostic | None]:
    try:
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        return None, Diagnostic(_display_path(path, report_root), "E001", f"cannot read artifact: {exc}", "structure")

    if not text.startswith("+++\n") and text != "+++":
        return None, None

    lines = text.splitlines()
    try:
        closing_index = lines.index("+++", 1)
    except ValueError:
        return None, Diagnostic(
            _display_path(path, report_root),
            "E001",
            "formal artifact starts TOML front matter but has no closing +++ delimiter",
            "structure",
        )

    front_matter_text = "\n".join(lines[1:closing_index])
    body = "\n".join(lines[closing_index + 1 :]).lstrip("\n")

    try:
        metadata = tomllib.loads(front_matter_text)
    except tomllib.TOMLDecodeError as exc:
        return None, Diagnostic(
            _display_path(path, report_root),
            "E001",
            f"invalid TOML front matter: {exc}",
            "structure",
        )

    if not isinstance(metadata, dict):
        return None, Diagnostic(
            _display_path(path, report_root),
            "E001",
            "front matter must be a TOML table",
            "structure",
        )

    return Artifact(path=path, metadata=metadata, body=body), None


def load_artifacts(artifact_root: Path, report_root: Path) -> tuple[list[Artifact], list[Diagnostic]]:
    artifacts: list[Artifact] = []
    errors: list[Diagnostic] = []
    for path in discover_candidate_files(artifact_root):
        artifact, error = parse_formal_artifact(path, report_root)
        if error is not None:
            errors.append(error)
        elif artifact is not None:
            artifacts.append(artifact)
    return artifacts, errors


def _add_error(
    errors: list[Diagnostic],
    artifact: Artifact,
    report_root: Path,
    code: str,
    message: str,
    *,
    plane: str,
) -> None:
    errors.append(Diagnostic(_display_path(artifact.path, report_root), code, message, plane))


def _require_non_empty_string(
    artifact: Artifact,
    field: str,
    errors: list[Diagnostic],
    report_root: Path,
    *,
    plane: str = "structure",
) -> str | None:
    value = artifact.metadata.get(field)
    if not isinstance(value, str) or not value.strip():
        _add_error(
            errors,
            artifact,
            report_root,
            "E002",
            f"field '{field}' must be a non-empty string",
            plane=plane,
        )
        return None
    return value.strip()


def _require_non_empty_string_list(
    artifact: Artifact,
    field: str,
    errors: list[Diagnostic],
    report_root: Path,
    *,
    code: str = "E002",
    container: dict[str, Any] | None = None,
    plane: str = "structure",
) -> list[str] | None:
    source = artifact.metadata if container is None else container
    value = source.get(field)
    if not isinstance(value, list) or not value or any(not isinstance(item, str) or not item.strip() for item in value):
        _add_error(
            errors,
            artifact,
            report_root,
            code,
            f"field '{field}' must be a non-empty array of strings",
            plane=plane,
        )
        return None
    return [item.strip() for item in value]


def _validate_git_identity(
    artifact: Artifact,
    errors: list[Diagnostic],
    report_root: Path,
) -> tuple[str | None, str | None]:
    commit = _require_non_empty_string(
        artifact, "commit", errors, report_root, plane="governance"
    )
    object_format = _require_non_empty_string(
        artifact, "git_object_format", errors, report_root, plane="governance"
    )
    if object_format is not None and object_format not in GIT_COMMIT_PATTERNS:
        _add_error(
            errors,
            artifact,
            report_root,
            "E009",
            "field 'git_object_format' must be 'sha1' or 'sha256'",
            plane="governance",
        )
    elif commit is not None and object_format is not None and not GIT_COMMIT_PATTERNS[object_format].fullmatch(commit):
        _add_error(
            errors,
            artifact,
            report_root,
            "E009",
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
    value = _require_non_empty_string(
        artifact, field, errors, report_root, plane="governance"
    )
    if value is not None:
        try:
            datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            _add_error(
                errors,
                artifact,
                report_root,
                "E009",
                f"field '{field}' must use a valid YYYY-MM-DDTHH:MM:SSZ timestamp",
                plane="governance",
            )


def _validate_evidence_paths(
    artifact: Artifact,
    errors: list[Diagnostic],
    repository_root: Path,
) -> None:
    paths = _require_non_empty_string_list(
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
            _add_error(
                errors,
                artifact,
                repository_root,
                "E012",
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
            _add_error(
                errors,
                artifact,
                repository_root,
                "E012",
                f"evidence path escapes the repository: '{raw_path}'",
                plane="governance",
            )
            continue
        if symlinked:
            _add_error(
                errors,
                artifact,
                repository_root,
                "E012",
                f"evidence path must not traverse a symlink: '{raw_path}'",
                plane="governance",
            )
        elif not candidate.is_file():
            _add_error(
                errors,
                artifact,
                repository_root,
                "E012",
                f"evidence path does not identify an existing file: '{raw_path}'",
                plane="governance",
            )


def _unique_evaluator_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate evaluator evidence field: {key}")
        value[key] = item
    return value


def _evaluator_binding_error(
    artifact: Artifact,
    errors: list[Diagnostic],
    repository_root: Path,
    message: str,
) -> None:
    _add_error(errors, artifact, repository_root, "E012", message, plane="governance")


def _valid_evaluator_origin(value: Any) -> bool:
    if not isinstance(value, str) or EVALUATOR_ORIGIN_PATTERN.fullmatch(value) is None:
        return False
    suffix = value.removeprefix("<evaluator-root>").removeprefix("/")
    return not suffix or all(part not in {"", ".", ".."} for part in suffix.split("/"))


def _validated_release_bootstrap(
    contract: Artifact,
    errors: list[Diagnostic],
    repository_root: Path,
) -> dict[str, Any] | None:
    value = contract.metadata.get("bootstrap")
    if value is None:
        return None
    if not isinstance(value, dict) or set(value) != RELEASE_BOOTSTRAP_KEYS:
        _add_error(
            errors,
            contract,
            repository_root,
            "E012",
            "release bootstrap field set is not canonical",
            plane="governance",
        )
        return None
    version = value.get("version")
    evaluator_version = value.get("evaluator_version")
    release_record = value.get("release_record")
    archive_name = value.get("evaluator_archive_name")
    valid = (
        value.get("schema") == RELEASE_BOOTSTRAP_SCHEMA
        and isinstance(release_record, str)
        and release_record.startswith("RLS-")
        and ID_PATTERN.fullmatch(release_record) is not None
        and isinstance(version, str)
        and EVALUATOR_VERSION_PATTERN.fullmatch(version) is not None
        and type(value.get("from_lock_schema")) is int
        and value.get("from_lock_schema") == 2
        and isinstance(value.get("from_lock_tool_version"), str)
        and EVALUATOR_VERSION_PATTERN.fullmatch(value["from_lock_tool_version"]) is not None
        and isinstance(value.get("from_lock_sha256"), str)
        and SHA256_PATTERN.fullmatch(value["from_lock_sha256"]) is not None
        and isinstance(evaluator_version, str)
        and EVALUATOR_VERSION_PATTERN.fullmatch(evaluator_version) is not None
        and evaluator_version == value.get("from_lock_tool_version")
        and isinstance(archive_name, str)
        and archive_name == f"se_harness-{evaluator_version.replace('-', '_')}-py3-none-any.whl"
        and isinstance(value.get("evaluator_archive_sha256"), str)
        and SHA256_PATTERN.fullmatch(value["evaluator_archive_sha256"]) is not None
    )
    if not valid:
        _add_error(
            errors,
            contract,
            repository_root,
            "E012",
            "release bootstrap tuple is invalid",
            plane="governance",
        )
        return None
    return value


def _canonical_utf8_text_lf(raw: bytes) -> bytes:
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("UTF-8 byte-order mark is unsupported")
    text = raw.decode("utf-8")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def _bootstrap_for_release_record(
    artifact: Artifact,
    artifacts: list[Artifact],
    errors: list[Diagnostic],
    repository_root: Path,
) -> dict[str, Any] | None:
    marker = artifact.metadata.get("preparation_schema")
    if marker is None:
        return None
    if marker != PREDECESSOR_PREPARATION_SCHEMA:
        _evaluator_binding_error(
            artifact, errors, repository_root, "release preparation_schema is unsupported"
        )
        return None
    satisfies = artifact.relations.get("satisfies")
    if not isinstance(satisfies, list) or len(satisfies) != 1 or not isinstance(satisfies[0], str):
        _evaluator_binding_error(
            artifact,
            errors,
            repository_root,
            "predecessor bootstrap release must satisfy exactly one release contract",
        )
        return None
    contract_status = "rejected" if artifact.status == "rejected" else "approved"
    matching = [
        item
        for item in artifacts
        if item.artifact_type == "release_contract"
        and item.artifact_id == satisfies[0]
        and item.status == contract_status
    ]
    if len(matching) != 1:
        _evaluator_binding_error(
            artifact,
            errors,
            repository_root,
            f"predecessor bootstrap {artifact.status} release requires one exact "
            f"{contract_status} release contract",
        )
        return None
    value = _validated_release_bootstrap(matching[0], errors, repository_root)
    if value is None:
        return None
    claimants = [
        item
        for item in artifacts
        if item.artifact_type == "release_contract"
        and item.status == contract_status
        and isinstance(item.metadata.get("bootstrap"), dict)
        and item.metadata["bootstrap"].get("release_record") == artifact.artifact_id
    ]
    if len(claimants) != 1 or claimants[0].artifact_id != matching[0].artifact_id:
        _evaluator_binding_error(
            artifact,
            errors,
            repository_root,
            "predecessor bootstrap release-record declaration is ambiguous",
        )
        return None
    if artifact.artifact_id != value["release_record"] or artifact.metadata.get("version") != value["version"]:
        _evaluator_binding_error(
            artifact,
            errors,
            repository_root,
            "release record ID or version differs from the predecessor bootstrap contract",
        )
        return None
    return value


def _validate_evaluator_evidence_binding(
    artifact: Artifact,
    errors: list[Diagnostic],
    repository_root: Path,
    *,
    required: bool,
    require_archive: bool = False,
    match_current_lock: bool = True,
    bootstrap_contract: dict[str, Any] | None = None,
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
    if not raw or len(raw) > EVALUATOR_EVIDENCE_MAX_BYTES:
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator evidence size is invalid")
        return
    if hashlib.sha256(raw).hexdigest() != raw_digest:
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator evidence digest does not match its bytes")
        return
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_evaluator_object)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        _evaluator_binding_error(artifact, errors, repository_root, f"invalid evaluator evidence JSON: {exc}")
        return
    canonical = (json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True) + "\n").encode("utf-8")
    if raw != canonical or not isinstance(value, dict):
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator evidence bytes are not canonical")
        return
    if set(value) != {"schema", "role", "evaluator", "origins", "environment", "diagnostics"}:
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator evidence field set is not canonical")
        return
    evaluator = value.get("evaluator")
    origins = value.get("origins")
    environment = value.get("environment")
    if value.get("schema") != EVALUATOR_EVIDENCE_SCHEMA or value.get("role") != "released-evaluator":
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator evidence schema or role is invalid")
        return
    if not isinstance(evaluator, dict) or set(evaluator) != {
        "version", "payload_manifest", "payload_sha256", "archive_name", "archive_sha256"
    }:
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator identity field set is not canonical")
        return
    if evaluator.get("payload_manifest") != EVALUATOR_PAYLOAD_MANIFEST:
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator payload manifest is unsupported")
        return
    evaluator_version = evaluator.get("version")
    if not isinstance(evaluator_version, str) or EVALUATOR_VERSION_PATTERN.fullmatch(evaluator_version) is None:
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator version is invalid")
        return
    if not isinstance(evaluator.get("payload_sha256"), str) or SHA256_PATTERN.fullmatch(evaluator["payload_sha256"]) is None:
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator payload digest is invalid")
        return
    archive_name = evaluator.get("archive_name")
    archive_sha256 = evaluator.get("archive_sha256")
    if (archive_name is None) != (archive_sha256 is None):
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator archive fields must appear together")
        return
    if archive_name is not None and (
        not isinstance(archive_name, str)
        or archive_name != f"se_harness-{evaluator_version.replace('-', '_')}-py3-none-any.whl"
        or not isinstance(archive_sha256, str)
        or SHA256_PATTERN.fullmatch(archive_sha256) is None
    ):
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator archive identity is invalid")
        return
    if require_archive and archive_name is None:
        _evaluator_binding_error(
            artifact,
            errors,
            repository_root,
            "release evaluator evidence requires an archive name and SHA-256",
        )
        return
    if not isinstance(origins, dict) or set(origins) != {
        "python_executable", "module", "distribution", "templates", "entry_point"
    } or any(not _valid_evaluator_origin(item) for item in origins.values()):
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator origins are not canonical")
        return
    expected_environment = {
        "isolated_python", "user_site_enabled", "pythonpath_present", "entry_point_resolved", "checkout_excluded"
    }
    if (
        not isinstance(environment, dict)
        or set(environment) != expected_environment
        or any(type(environment.get(field)) is not bool for field in expected_environment)
        or not environment.get("isolated_python")
        or environment.get("user_site_enabled")
        or environment.get("pythonpath_present")
        or not environment.get("entry_point_resolved")
        or not environment.get("checkout_excluded")
        or value.get("diagnostics") != []
    ):
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator environment proof is invalid")
        return
    if bootstrap_contract is not None:
        if (
            evaluator.get("version") != bootstrap_contract.get("evaluator_version")
            or evaluator.get("archive_name") != bootstrap_contract.get("evaluator_archive_name")
            or evaluator.get("archive_sha256") != bootstrap_contract.get("evaluator_archive_sha256")
        ):
            _evaluator_binding_error(
                artifact, errors, repository_root, "evaluator evidence differs from the bootstrap contract"
            )
            return
        if not match_current_lock:
            return
        try:
            lock_raw = (repository_root / ".engineering-harness.lock").read_bytes()
            lock = json.loads(lock_raw.decode("utf-8"), object_pairs_hook=_unique_evaluator_object)
            config = tomllib.loads(
                (repository_root / ".engineering-harness.toml").read_text(encoding="utf-8")
            )
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError, tomllib.TOMLDecodeError) as exc:
            _evaluator_binding_error(
                artifact, errors, repository_root, f"cannot read predecessor bootstrap root: {exc}"
            )
            return
        harness = config.get("harness") if isinstance(config, dict) else None
        if (
            hashlib.sha256(_canonical_utf8_text_lf(lock_raw)).hexdigest()
            != bootstrap_contract.get("from_lock_sha256")
            or not isinstance(lock, dict)
            or lock.get("schema") != bootstrap_contract.get("from_lock_schema")
            or lock.get("tool_version") != bootstrap_contract.get("from_lock_tool_version")
            or lock.get("hash_algorithm") != "sha256"
            or lock.get("hash_mode") != "utf8-text-lf-v1"
            or not isinstance(harness, dict)
            or harness.get("tool_version") != bootstrap_contract.get("from_lock_tool_version")
        ):
            _evaluator_binding_error(
                artifact, errors, repository_root, "current predecessor root differs from the bootstrap contract"
            )
        return
    if not match_current_lock:
        return
    try:
        lock = json.loads(
            (repository_root / ".engineering-harness.lock").read_text(encoding="utf-8"),
            object_pairs_hook=_unique_evaluator_object,
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
    normalized_expected = (
        {
            "version": expected_evaluator.get("version"),
            "payload_manifest": expected_evaluator.get("payload_manifest"),
            "payload_sha256": expected_evaluator.get("payload_sha256"),
            "archive_name": expected_evaluator.get("archive_name"),
            "archive_sha256": expected_evaluator.get("archive_sha256"),
        }
        if isinstance(expected_evaluator, dict)
        else None
    )
    if normalized_expected is None or evaluator != normalized_expected:
        _evaluator_binding_error(artifact, errors, repository_root, "evaluator evidence differs from the standard lock")


def _validate_predecessor_view_evidence(
    artifact: Artifact,
    artifacts: list[Artifact],
    errors: list[Diagnostic],
    repository_root: Path,
    *,
    required: bool,
    bootstrap_contract: dict[str, Any] | None,
) -> None:
    raw_path = artifact.metadata.get("preparation_view_evidence_path")
    raw_digest = artifact.metadata.get("preparation_view_evidence_sha256")
    if raw_path is None and raw_digest is None and not required:
        return
    if not isinstance(raw_path, str) or not raw_path:
        _evaluator_binding_error(
            artifact, errors, repository_root,
            "field 'preparation_view_evidence_path' must be a non-empty string",
        )
        return
    if not isinstance(raw_digest, str) or SHA256_PATTERN.fullmatch(raw_digest) is None:
        _evaluator_binding_error(
            artifact, errors, repository_root,
            "field 'preparation_view_evidence_sha256' must be a lowercase SHA-256 value",
        )
        return
    relative = Path(raw_path)
    if (
        relative.is_absolute()
        or "\\" in raw_path
        or any(part in {"", ".", ".."} for part in relative.parts)
        or relative.name != f"{artifact.artifact_id}-preparation-view.json"
        or relative.parts[:2] != ("docs", "engineering")
        or "evidence" not in relative.parts
    ):
        _evaluator_binding_error(
            artifact, errors, repository_root,
            "preparation-view evidence path must be canonical and repository-relative",
        )
        return
    candidate = repository_root / relative
    probe = repository_root
    for part in relative.parts:
        probe = probe / part
        if probe.is_symlink():
            _evaluator_binding_error(
                artifact, errors, repository_root,
                "preparation-view evidence path must not traverse a symlink",
            )
            return
    try:
        candidate.resolve().relative_to(repository_root.resolve())
        raw = candidate.read_bytes()
    except (OSError, ValueError):
        _evaluator_binding_error(
            artifact, errors, repository_root,
            "preparation-view evidence is unavailable or escapes the repository",
        )
        return
    if not raw or len(raw) > PREDECESSOR_VIEW_EVIDENCE_MAX_BYTES:
        _evaluator_binding_error(artifact, errors, repository_root, "preparation-view evidence size is invalid")
        return
    if hashlib.sha256(raw).hexdigest() != raw_digest:
        _evaluator_binding_error(
            artifact, errors, repository_root,
            "preparation-view evidence digest does not match its bytes",
        )
        return
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_evaluator_object)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        _evaluator_binding_error(
            artifact, errors, repository_root, f"invalid preparation-view evidence JSON: {exc}"
        )
        return
    canonical = (json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True) + "\n").encode("utf-8")
    if raw != canonical or not isinstance(value, dict):
        _evaluator_binding_error(artifact, errors, repository_root, "preparation-view evidence bytes are not canonical")
        return
    if set(value) != {"schema", "source", "candidate", "release", "evaluator", "command", "view", "output"}:
        _evaluator_binding_error(artifact, errors, repository_root, "preparation-view evidence field set is not canonical")
        return
    source = value.get("source")
    candidate_identity = value.get("candidate")
    release = value.get("release")
    evaluator = value.get("evaluator")
    command = value.get("command")
    view = value.get("view")
    output = value.get("output")
    if value.get("schema") != PREDECESSOR_VIEW_EVIDENCE_SCHEMA:
        _evaluator_binding_error(artifact, errors, repository_root, "preparation-view evidence schema is invalid")
        return
    if not isinstance(source, dict) or set(source) != {"commit", "git_object_format", "tree"}:
        _evaluator_binding_error(artifact, errors, repository_root, "preparation-view source identity is invalid")
        return
    source_format = source.get("git_object_format")
    source_pattern = GIT_COMMIT_PATTERNS.get(source_format)
    if (
        source_pattern is None
        or not isinstance(source.get("commit"), str)
        or source_pattern.fullmatch(source["commit"]) is None
        or not isinstance(source.get("tree"), str)
        or source_pattern.fullmatch(source["tree"]) is None
    ):
        _evaluator_binding_error(artifact, errors, repository_root, "preparation-view source Git identity is invalid")
        return
    if (
        not isinstance(candidate_identity, dict)
        or set(candidate_identity) != {"commit", "git_object_format"}
        or candidate_identity.get("commit") != artifact.metadata.get("commit")
        or candidate_identity.get("git_object_format") != artifact.metadata.get("git_object_format")
    ):
        _evaluator_binding_error(
            artifact, errors, repository_root,
            "preparation-view candidate identity differs from the release",
        )
        return
    if not isinstance(release, dict) or set(release) != {
        "contract", "record", "verification_records", "version", "work_orders"
    }:
        _evaluator_binding_error(artifact, errors, repository_root, "preparation-view release identity is invalid")
        return
    satisfies = sorted(_relation_targets(artifact, "satisfies"))
    if (
        release.get("record") != artifact.artifact_id
        or release.get("version") != artifact.metadata.get("version")
        or satisfies != [release.get("contract")]
        or release.get("verification_records") != sorted(_relation_targets(artifact, "includes_verification"))
        or release.get("work_orders") != sorted(_relation_targets(artifact, "releases_work"))
    ):
        _evaluator_binding_error(artifact, errors, repository_root, "preparation-view release scope differs from the RLS")
        return
    arguments = command.get("arguments") if isinstance(command, dict) and set(command) == {"arguments"} else None
    if (
        not isinstance(arguments, list)
        or not arguments
        or any(not isinstance(item, str) or not item or "\\" in item for item in arguments)
        or arguments[:5] != ["-I", "-m", "se_harness", "prepare-release", "."]
    ):
        _evaluator_binding_error(artifact, errors, repository_root, "preparation-view command identity is invalid")
        return
    try:
        output_path = artifact.path.relative_to(repository_root).as_posix()
        output_parts = PurePosixPath(output_path).parts
    except ValueError:
        output_parts = ()
        output_path = ""
    expected_arguments = [
        "-I", "-m", "se_harness", "prepare-release", ".",
        "--id", artifact.artifact_id,
        "--release-contract", str(release.get("contract")),
    ]
    for verification_id in sorted(_relation_targets(artifact, "includes_verification")):
        expected_arguments.extend(("--verification-record", verification_id))
    for work_order_id in sorted(_relation_targets(artifact, "releases_work")):
        expected_arguments.extend(("--work-order", work_order_id))
    expected_arguments.extend(
        (
            "--version", str(artifact.metadata.get("version")),
            "--authorized-by", str(artifact.metadata.get("authorized_by")),
        )
    )
    if artifact.metadata.get("tag") is not None:
        expected_arguments.extend(("--tag", str(artifact.metadata.get("tag"))))
    if len(output_parts) < 3 or output_parts[:2] != ("docs", "engineering"):
        _evaluator_binding_error(artifact, errors, repository_root, "preparation-view RLS path is not canonical")
        return
    expected_arguments.extend(("--output", output_path, "--domain", output_parts[2]))
    if arguments != expected_arguments:
        _evaluator_binding_error(
            artifact, errors, repository_root,
            "preparation-view command differs from the exact RLS preparation scope",
        )
        return
    if (
        not isinstance(evaluator, dict)
        or set(evaluator) != {"archive_name", "archive_sha256", "runtime_identity_schema", "version"}
        or bootstrap_contract is None
        or evaluator.get("version") != bootstrap_contract.get("evaluator_version")
        or evaluator.get("archive_name") != bootstrap_contract.get("evaluator_archive_name")
        or evaluator.get("archive_sha256") != bootstrap_contract.get("evaluator_archive_sha256")
        or evaluator.get("runtime_identity_schema") not in {
            "se-harness-runtime-identity-v2", "se-harness-runtime-identity-v3"
        }
    ):
        _evaluator_binding_error(artifact, errors, repository_root, "preparation-view evaluator identity is invalid")
        return
    if (
        not isinstance(output, dict)
        or set(output) != {"predecessor_record_sha256"}
        or not isinstance(output.get("predecessor_record_sha256"), str)
        or SHA256_PATTERN.fullmatch(output["predecessor_record_sha256"]) is None
    ):
        _evaluator_binding_error(artifact, errors, repository_root, "preparation-view predecessor output identity is invalid")
        return
    if artifact.status == "ready":
        try:
            record_raw = artifact.path.read_bytes()
        except OSError:
            _evaluator_binding_error(artifact, errors, repository_root, "preparation-view RLS bytes are unavailable")
            return
        newline = b"\r\n" if record_raw.startswith(b"+++\r\n") else b"\n"
        view_block = (
            f'preparation_view_evidence_path = "{raw_path}"'.encode("utf-8") + newline
            + f'preparation_view_evidence_sha256 = "{raw_digest}"'.encode("utf-8") + newline * 2
        )
        if record_raw.count(view_block) != 1:
            _evaluator_binding_error(artifact, errors, repository_root, "preparation-view RLS binding is not canonical")
            return
        predecessor_raw = record_raw.replace(view_block, b"", 1)
        evaluator_fields = (
            artifact.metadata.get("preparation_schema"),
            artifact.metadata.get("evaluator_evidence_path"),
            artifact.metadata.get("evaluator_evidence_sha256"),
        )
        if any(item is not None for item in evaluator_fields):
            preparation_schema, evaluator_path, evaluator_digest = evaluator_fields
            if (
                preparation_schema != PREDECESSOR_PREPARATION_SCHEMA
                or not isinstance(evaluator_path, str)
                or not isinstance(evaluator_digest, str)
                or SHA256_PATTERN.fullmatch(evaluator_digest) is None
            ):
                _evaluator_binding_error(artifact, errors, repository_root, "preparation-view evaluator binding is incomplete")
                return
            evaluator_block = (
                f'preparation_schema = "{preparation_schema}"'.encode("utf-8") + newline
                + f'evaluator_evidence_path = "{evaluator_path}"'.encode("utf-8") + newline
                + f'evaluator_evidence_sha256 = "{evaluator_digest}"'.encode("utf-8") + newline * 2
            )
            if predecessor_raw.count(evaluator_block) != 1:
                _evaluator_binding_error(artifact, errors, repository_root, "preparation-view evaluator binding is not canonical")
                return
            predecessor_raw = predecessor_raw.replace(evaluator_block, b"", 1)
        if hashlib.sha256(predecessor_raw).hexdigest() != output["predecessor_record_sha256"]:
            _evaluator_binding_error(
                artifact, errors, repository_root,
                "preparation-view predecessor output digest differs from the bound RLS bytes",
            )
            return
    omitted = view.get("omitted_history") if isinstance(view, dict) else None
    sparse_digest = view.get("sparse_spec_sha256") if isinstance(view, dict) else None
    if (
        not isinstance(view, dict)
        or set(view) != {"omitted_history", "sparse_spec_sha256"}
        or not isinstance(sparse_digest, str)
        or SHA256_PATTERN.fullmatch(sparse_digest) is None
        or not isinstance(omitted, list)
        or len(omitted) != 2
    ):
        _evaluator_binding_error(artifact, errors, repository_root, "preparation-view omission set is invalid")
        return
    artifact_by_id = {item.artifact_id: item for item in artifacts}
    observed_types: set[str] = set()
    observed_ids: set[str] = set()
    paths: list[str] = []
    for descriptor in omitted:
        expected_fields = {"artifact_id", "artifact_type", "status", "path", "git_blob", "bytes", "sha256"}
        if not isinstance(descriptor, dict) or set(descriptor) != expected_fields:
            _evaluator_binding_error(artifact, errors, repository_root, "preparation-view history descriptor is invalid")
            return
        artifact_id = descriptor.get("artifact_id")
        item = artifact_by_id.get(artifact_id) if isinstance(artifact_id, str) else None
        object_pattern = GIT_COMMIT_PATTERNS[source_format]
        if (
            item is None
            or item.artifact_type != descriptor.get("artifact_type")
            or item.status != "rejected"
            or descriptor.get("status") != "rejected"
            or not isinstance(descriptor.get("path"), str)
            or not isinstance(descriptor.get("git_blob"), str)
            or object_pattern.fullmatch(descriptor["git_blob"]) is None
            or not isinstance(descriptor.get("bytes"), int)
            or isinstance(descriptor.get("bytes"), bool)
            or descriptor["bytes"] < 1
            or not isinstance(descriptor.get("sha256"), str)
            or SHA256_PATTERN.fullmatch(descriptor["sha256"]) is None
        ):
            _evaluator_binding_error(artifact, errors, repository_root, "preparation-view rejected history identity is invalid")
            return
        try:
            item_path = item.path.relative_to(repository_root).as_posix()
            canonical_item = _canonical_utf8_text_lf(item.path.read_bytes())
        except (OSError, UnicodeError, ValueError):
            _evaluator_binding_error(artifact, errors, repository_root, "preparation-view rejected history is unavailable")
            return
        if (
            descriptor["path"] != item_path
            or descriptor["bytes"] != len(canonical_item)
            or descriptor["sha256"] != hashlib.sha256(canonical_item).hexdigest()
        ):
            _evaluator_binding_error(artifact, errors, repository_root, "preparation-view rejected history bytes differ")
            return
        observed_types.add(item.artifact_type)
        observed_ids.add(item.artifact_id)
        paths.append(item_path)
    if observed_types != {"release_contract", "release_record"} or len(observed_ids) != 2:
        _evaluator_binding_error(artifact, errors, repository_root, "preparation view must omit one rejected RLS/REL pair")
        return
    expected_sparse = ("/*\n" + "".join(f"!/{path}\n" for path in sorted(paths))).encode("utf-8")
    if hashlib.sha256(expected_sparse).hexdigest() != sparse_digest:
        _evaluator_binding_error(artifact, errors, repository_root, "preparation-view sparse specification differs")
        return
    rejected_record = next(
        (item for item in artifacts if item.artifact_id in observed_ids and item.artifact_type == "release_record"),
        None,
    )
    rejected_contract = next(
        (item for item in artifacts if item.artifact_id in observed_ids and item.artifact_type == "release_contract"),
        None,
    )
    if (
        rejected_record is None
        or rejected_contract is None
        or _relation_targets(rejected_record, "satisfies") != {rejected_contract.artifact_id}
        or rejected_record.metadata.get("version") != artifact.metadata.get("version")
        or not isinstance(rejected_contract.metadata.get("bootstrap"), dict)
        or rejected_contract.metadata["bootstrap"].get("release_record") != rejected_record.artifact_id
        or rejected_contract.metadata["bootstrap"].get("version") != artifact.metadata.get("version")
    ):
        _evaluator_binding_error(
            artifact, errors, repository_root,
            "preparation-view omitted history is not one exact closed pair",
        )


def validate_common_metadata(artifacts: list[Artifact], report_root: Path) -> list[Diagnostic]:
    errors: list[Diagnostic] = []
    seen: dict[str, Artifact] = {}

    for artifact in artifacts:
        artifact_id = _require_non_empty_string(artifact, "id", errors, report_root)
        artifact_type = _require_non_empty_string(artifact, "type", errors, report_root)
        _require_non_empty_string(artifact, "title", errors, report_root)
        status = _require_non_empty_string(artifact, "status", errors, report_root)
        _require_non_empty_string_list(artifact, "owners", errors, report_root)
        created = _require_non_empty_string(artifact, "created", errors, report_root)
        updated = _require_non_empty_string(artifact, "updated", errors, report_root)

        if artifact_id is not None:
            if not ID_PATTERN.fullmatch(artifact_id):
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E002",
                    f"id '{artifact_id}' must use uppercase letters/digits/hyphens and end in a three-digit sequence",
                    plane="structure",
                )
            previous = seen.get(artifact_id)
            if previous is not None:
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E003",
                    f"duplicate id '{artifact_id}' also declared in {_display_path(previous.path, report_root)}",
                    plane="structure",
                )
            else:
                seen[artifact_id] = artifact

        if artifact_type is not None:
            expected_prefix = TYPE_PREFIX.get(artifact_type)
            if expected_prefix is None:
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E002",
                    f"unknown artifact type '{artifact_type}'",
                    plane="structure",
                )
            elif artifact_id is not None and not artifact_id.startswith(expected_prefix):
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E004",
                    f"id '{artifact_id}' must start with '{expected_prefix}' for type '{artifact_type}'",
                    plane="structure",
                )

        if (
            status is not None
            and artifact_type is not None
            and status not in WORKFLOW_LIFECYCLES[_lifecycle_family(artifact_type)]
        ):
            _add_error(
                errors,
                artifact,
                report_root,
                "E002",
                f"status '{status}' is not declared for {_lifecycle_family(artifact_type)} artifacts",
                plane="structure",
            )

        for field_name, field_value in (("created", created), ("updated", updated)):
            if field_value is not None and not ISO_DATE_PATTERN.fullmatch(field_value):
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E002",
                    f"field '{field_name}' must use YYYY-MM-DD",
                    plane="structure",
                )

        relations = artifact.metadata.get("relations", {})
        if not isinstance(relations, dict):
            _add_error(
                errors,
                artifact,
                report_root,
                "E006",
                "field 'relations' must be a TOML table",
                plane="structure",
            )

    return errors


def validate_lifecycle_events(artifacts: list[Artifact], report_root: Path) -> list[Diagnostic]:
    """Validate append-only decision events when the new contract is present.

    Historical artifacts without events remain valid. Once an event exists, its
    chain and any target-specific decision fields must be internally consistent.
    """

    errors: list[Diagnostic] = []
    for artifact in artifacts:
        events = artifact.metadata.get("lifecycle_events")
        if events is None:
            continue
        if not isinstance(events, list) or not events:
            _add_error(
                errors, artifact, report_root, "E014",
                "field 'lifecycle_events' must be a non-empty array of tables when present",
                plane="governance",
            )
            continue
        previous_to: str | None = None
        previous_at: str | None = None
        valid_events: list[dict[str, str]] = []
        family = _lifecycle_family(artifact.artifact_type)
        for index, event in enumerate(events):
            if not isinstance(event, dict):
                _add_error(
                    errors, artifact, report_root, "E014",
                    f"lifecycle event {index + 1} must be a TOML table",
                    plane="governance",
                )
                continue
            values: dict[str, str] = {}
            for field in ("from", "to", "decided_at", "decided_by"):
                value = event.get(field)
                if not isinstance(value, str) or not value.strip():
                    _add_error(
                        errors, artifact, report_root, "E014",
                        f"lifecycle event {index + 1} field '{field}' must be a non-empty string",
                        plane="governance",
                    )
                else:
                    values[field] = value.strip()
            reason = event.get("reason")
            if reason is not None and (not isinstance(reason, str) or not reason.strip()):
                _add_error(
                    errors, artifact, report_root, "E014",
                    f"lifecycle event {index + 1} field 'reason' must be a non-empty string when present",
                    plane="governance",
                )
            decided_at = values.get("decided_at")
            if decided_at is not None:
                try:
                    datetime.strptime(decided_at, "%Y-%m-%dT%H:%M:%SZ")
                except ValueError:
                    _add_error(
                        errors, artifact, report_root, "E014",
                        f"lifecycle event {index + 1} field 'decided_at' must use a valid YYYY-MM-DDTHH:MM:SSZ timestamp",
                        plane="governance",
                    )
                if previous_at is not None and decided_at < previous_at:
                    _add_error(
                        errors, artifact, report_root, "E014",
                        "lifecycle events must be ordered chronologically",
                        plane="governance",
                    )
                previous_at = decided_at
            source = values.get("from")
            target = values.get("to")
            if source is not None and target is not None:
                if target not in WORKFLOW_TRANSITIONS.get(family, {}).get(source, set()):
                    _add_error(
                        errors, artifact, report_root, "E014",
                        f"lifecycle event {index + 1} contains unsupported transition {source} -> {target}",
                        plane="governance",
                    )
                if previous_to is not None and source != previous_to:
                    _add_error(
                        errors, artifact, report_root, "E014",
                        f"lifecycle event {index + 1} starts at '{source}' instead of previous target '{previous_to}'",
                        plane="governance",
                    )
                previous_to = target
            if len(values) == 4:
                valid_events.append(values)
        if previous_to is not None and previous_to != artifact.status:
            _add_error(
                errors, artifact, report_root, "E014",
                f"last lifecycle event target '{previous_to}' must equal artifact status '{artifact.status}'",
                plane="governance",
            )
        if not valid_events:
            continue
        latest = valid_events[-1]
        expected_fields: tuple[str, str] | None = None
        if artifact.artifact_type == "verification_record" and latest["to"] == "verified":
            expected_fields = ("verified_at", "verified_by")
        elif artifact.artifact_type == "release_record" and latest["to"] == "released":
            expected_fields = ("released_at", "authorized_by")
        elif latest["to"] == "rejected":
            expected_fields = ("rejected_at", "rejected_by")
            reason = events[-1].get("reason") if isinstance(events[-1], dict) else None
            if not isinstance(reason, str) or not reason.strip():
                _add_error(
                    errors, artifact, report_root, "E014",
                    "rejection lifecycle event requires a non-empty reason",
                    plane="governance",
                )
            if artifact.metadata.get("rejection_reason") != reason:
                _add_error(
                    errors, artifact, report_root, "E014",
                    "field 'rejection_reason' must equal the rejection lifecycle event reason",
                    plane="governance",
                )
        elif artifact.artifact_type == "verification_record" and latest["to"] == "superseded":
            expected_fields = ("superseded_at", "supersession_authorized_by")
            reason = events[-1].get("reason") if isinstance(events[-1], dict) else None
            successors = artifact.relations.get("superseded_by", [])
            if not isinstance(reason, str) or successors != [reason]:
                _add_error(
                    errors, artifact, report_root, "E014",
                    "supersession lifecycle event reason must equal the single superseded_by target",
                    plane="governance",
                )
        if expected_fields is not None:
            timestamp_field, actor_field = expected_fields
            legacy_decision_record = (
                artifact.artifact_type in {"verification_record", "release_record"}
                and "prepared_at" not in artifact.metadata
                and latest["to"] in {"verified", "released"}
            )
            if not legacy_decision_record and artifact.metadata.get(timestamp_field) != latest["decided_at"]:
                _add_error(
                    errors, artifact, report_root, "E014",
                    f"field '{timestamp_field}' must equal the latest lifecycle decision timestamp",
                    plane="governance",
                )
            if not legacy_decision_record and artifact.metadata.get(actor_field) != latest["decided_by"]:
                _add_error(
                    errors, artifact, report_root, "E014",
                    f"field '{actor_field}' must equal the latest lifecycle decision actor",
                    plane="governance",
                )
    return errors


def validate_type_specific_metadata(artifacts: list[Artifact], report_root: Path) -> list[Diagnostic]:
    errors: list[Diagnostic] = []

    approved_bootstrap_contracts = [
        artifact
        for artifact in artifacts
        if artifact.artifact_type == "release_contract"
        and artifact.status == "approved"
        and "bootstrap" in artifact.metadata
    ]
    if len(approved_bootstrap_contracts) > 1:
        for contract in approved_bootstrap_contracts:
            _add_error(
                errors,
                contract,
                report_root,
                "E012",
                "repository must contain at most one approved predecessor bootstrap contract",
                plane="governance",
            )

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
    }

    for artifact in artifacts:
        artifact_type = artifact.metadata.get("type")
        if not isinstance(artifact_type, str):
            continue

        if artifact_type == "requirement":
            statement = _require_non_empty_string(artifact, "statement", errors, report_root)
            _require_non_empty_string(artifact, "verification_method", errors, report_root)
            if statement is not None and re.search(r"\bSHALL\b", statement) is None:
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E005",
                    "requirement statement must contain normative keyword SHALL",
                    plane="structure",
                )

        if artifact_type == "release_contract" and "bootstrap" in artifact.metadata:
            _validated_release_bootstrap(artifact, errors, report_root)

        if artifact_type == "verification_record":
            _validate_git_identity(artifact, errors, report_root)
            worktree_state = _require_non_empty_string(
                artifact, "worktree_state", errors, report_root, plane="governance"
            )
            if worktree_state is not None and worktree_state != "clean":
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E009",
                    "field 'worktree_state' must be 'clean'",
                    plane="governance",
                )
            prepared = "prepared_at" in artifact.metadata or "prepared_by" in artifact.metadata
            if prepared:
                _validate_timestamp(artifact, "prepared_at", errors, report_root)
                _require_non_empty_string(artifact, "prepared_by", errors, report_root, plane="governance")
            if artifact.status in {"verified", "released"}:
                _validate_timestamp(artifact, "verified_at", errors, report_root)
                if prepared:
                    _require_non_empty_string(artifact, "verified_by", errors, report_root, plane="governance")
            elif artifact.status == "superseded":
                if prepared:
                    for field_name in ("verified_at", "verified_by"):
                        if field_name in artifact.metadata:
                            _add_error(
                                errors, artifact, report_root, "E009",
                                f"prepared superseded verification_record must omit decision field '{field_name}'",
                                plane="governance",
                            )
                else:
                    _validate_timestamp(artifact, "verified_at", errors, report_root)
            snapshot_hash = _require_non_empty_string(
                artifact,
                "artifact_snapshot_sha256",
                errors,
                report_root,
                plane="governance",
            )
            if snapshot_hash is not None and not SHA256_PATTERN.fullmatch(snapshot_hash):
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E009",
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
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E009",
                    "verification_record status is not declared by the workflow lifecycle registry",
                    plane="governance",
                )
            if artifact.status == "ready" and prepared:
                for field_name in ("verified_at", "verified_by"):
                    if field_name in artifact.metadata:
                        _add_error(
                            errors, artifact, report_root, "E009",
                            f"ready verification_record must omit decision field '{field_name}'",
                            plane="governance",
                        )
            if artifact.status == "rejected":
                _validate_timestamp(artifact, "rejected_at", errors, report_root)
                _require_non_empty_string(artifact, "rejected_by", errors, report_root, plane="governance")
                _require_non_empty_string(artifact, "rejection_reason", errors, report_root, plane="governance")
            if artifact.status == "superseded":
                _validate_timestamp(artifact, "superseded_at", errors, report_root)
                _require_non_empty_string(artifact, "supersession_authorized_by", errors, report_root)
                successors = _require_non_empty_string_list(
                    artifact,
                    "superseded_by",
                    errors,
                    report_root,
                    code="E009",
                    container=artifact.relations,
                    plane="governance",
                )
                if successors is not None and len(successors) != 1:
                    _add_error(
                        errors,
                        artifact,
                        report_root,
                        "E009",
                        "relation 'superseded_by' must contain exactly one verification record",
                        plane="governance",
                    )
            else:
                for field_name in ("superseded_at", "supersession_authorized_by"):
                    if field_name in artifact.metadata:
                        _add_error(
                            errors,
                            artifact,
                            report_root,
                            "E009",
                            f"field '{field_name}' is allowed only when verification_record status is superseded",
                            plane="governance",
                        )
                if "superseded_by" in artifact.relations:
                    _add_error(
                        errors,
                        artifact,
                        report_root,
                        "E009",
                        "relation 'superseded_by' is allowed only when verification_record status is superseded",
                        plane="governance",
                    )

        if artifact_type == "release_record":
            bootstrap_contract = _bootstrap_for_release_record(
                artifact, artifacts, errors, report_root
            )
            rejected_predecessor_history = any(
                item.artifact_type == "release_record"
                and item.status == "rejected"
                and item.artifact_id != artifact.artifact_id
                and item.metadata.get("version") == artifact.metadata.get("version")
                and item.metadata.get("preparation_schema") == PREDECESSOR_PREPARATION_SCHEMA
                for item in artifacts
            )
            _validate_predecessor_view_evidence(
                artifact,
                artifacts,
                errors,
                report_root,
                required=(
                    _active_record_status("release_record", artifact.status)
                    and bootstrap_contract is not None
                    and rejected_predecessor_history
                ),
                bootstrap_contract=bootstrap_contract,
            )
            _validate_git_identity(artifact, errors, report_root)
            release_version = _require_non_empty_string(
                artifact, "version", errors, report_root, plane="governance"
            )
            prepared = "prepared_at" in artifact.metadata or "prepared_by" in artifact.metadata
            if prepared:
                _validate_timestamp(artifact, "prepared_at", errors, report_root)
                _require_non_empty_string(artifact, "prepared_by", errors, report_root, plane="governance")
            authorized_by: str | None = None
            if artifact.status == "released":
                _validate_timestamp(artifact, "released_at", errors, report_root)
                authorized_by = _require_non_empty_string(
                    artifact, "authorized_by", errors, report_root, plane="governance"
                )
            owners = artifact.metadata.get("owners", [])
            if authorized_by is not None and isinstance(owners, list) and authorized_by not in owners:
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E009",
                    "field 'authorized_by' must identify one of the record owners",
                    plane="governance",
                )
            tag = artifact.metadata.get("tag")
            if tag is not None and (not isinstance(tag, str) or not tag.strip()):
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E009",
                    "field 'tag' must be a non-empty string when present",
                    plane="governance",
                )
            if artifact.status == "ready" and prepared:
                for field_name in ("released_at", "authorized_by"):
                    if field_name in artifact.metadata:
                        _add_error(
                            errors, artifact, report_root, "E009",
                            f"ready release_record must omit decision field '{field_name}'",
                            plane="governance",
                        )
            if artifact.status == "ready" and bootstrap_contract is not None:
                if prepared:
                    _add_error(
                        errors,
                        artifact,
                        report_root,
                        "E009",
                        "predecessor-prepared ready release_record must omit successor preparation fields",
                        plane="governance",
                    )
                _validate_timestamp(artifact, "released_at", errors, report_root)
                predecessor_actor = _require_non_empty_string(
                    artifact, "authorized_by", errors, report_root, plane="governance"
                )
                if (
                    predecessor_actor is not None
                    and isinstance(owners, list)
                    and predecessor_actor not in owners
                ):
                    _add_error(
                        errors,
                        artifact,
                        report_root,
                        "E009",
                        "predecessor preparation actor must identify one of the record owners",
                        plane="governance",
                    )
            if artifact.status == "rejected":
                _validate_timestamp(artifact, "rejected_at", errors, report_root)
                _require_non_empty_string(artifact, "rejected_by", errors, report_root, plane="governance")
                _require_non_empty_string(artifact, "rejection_reason", errors, report_root, plane="governance")
            if artifact.status not in WORKFLOW_LIFECYCLES["release_record"]:
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E009",
                    "release_record status is not declared by the workflow lifecycle registry",
                    plane="governance",
                )
            legacy_without_binding = (
                artifact.status == "released"
                and artifact.artifact_id in LEGACY_RELEASES_WITHOUT_EVALUATOR_EVIDENCE
                and artifact.metadata.get("evaluator_evidence_path") is None
                and artifact.metadata.get("evaluator_evidence_sha256") is None
            )
            _validate_evaluator_evidence_binding(
                artifact,
                errors,
                report_root,
                required=not legacy_without_binding,
                require_archive=True,
                match_current_lock=artifact.status == "ready",
                bootstrap_contract=bootstrap_contract,
            )

        if artifact_type == "work_order" and "architecture" in artifact.relations:
            _require_non_empty_string_list(
                artifact,
                "architecture",
                errors,
                report_root,
                code="E005",
                container=artifact.relations,
            )

        required_relations = relation_requirements.get(artifact_type, ())
        relations = artifact.metadata.get("relations", {})
        if not isinstance(relations, dict):
            continue
        for relation_name in required_relations:
            _require_non_empty_string_list(
                artifact,
                relation_name,
                errors,
                report_root,
                code="E005",
                container=relations,
            )

    return errors


def validate_relations(artifacts: list[Artifact], report_root: Path) -> list[Diagnostic]:
    errors: list[Diagnostic] = []
    catalog = {
        artifact.artifact_id: artifact
        for artifact in artifacts
        if artifact.artifact_id != "<unknown>"
    }

    for artifact in artifacts:
        relations = artifact.metadata.get("relations", {})
        if not isinstance(relations, dict):
            continue
        for relation_name, targets in sorted(relations.items()):
            if not isinstance(targets, list):
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E006",
                    f"relation '{relation_name}' must be an array of artifact IDs",
                    plane="structure",
                )
                continue
            for target in targets:
                if not isinstance(target, str) or not target.strip():
                    _add_error(
                        errors,
                        artifact,
                        report_root,
                        "E006",
                        f"relation '{relation_name}' contains a non-string or empty target",
                        plane="structure",
                    )
                    continue
                if target == artifact.artifact_id:
                    _add_error(
                        errors,
                        artifact,
                        report_root,
                        "E006",
                        f"artifact '{artifact.artifact_id}' must not reference itself via '{relation_name}'",
                        plane="structure",
                    )
                elif target not in catalog:
                    _add_error(
                        errors,
                        artifact,
                        report_root,
                        "E006",
                        f"artifact '{artifact.artifact_id}' relation '{relation_name}' references unknown target '{target}'",
                        plane="structure",
                    )
                else:
                    allowed_types = RELATION_TARGET_TYPES.get((artifact.artifact_type, relation_name))
                    target_type = catalog[target].artifact_type
                    if allowed_types is not None and target_type not in allowed_types:
                        expected = ", ".join(sorted(allowed_types))
                        _add_error(
                            errors,
                            artifact,
                            report_root,
                            "E011",
                            f"relation '{relation_name}' target '{target}' must have type {expected}, found {target_type}",
                            plane="structure",
                        )
    return errors


def validate_revision_consistency(
    artifacts: list[Artifact],
    report_root: Path,
    *,
    require_verified_work: bool = False,
) -> list[Diagnostic]:
    errors: list[Diagnostic] = []
    catalog = {artifact.artifact_id: artifact for artifact in artifacts if artifact.artifact_id != "<unknown>"}
    release_versions: dict[str, list[Artifact]] = {}
    supersession_cycle_nodes = _supersession_cycle_nodes(artifacts)

    if require_verified_work:
        verified_work = {
            work_order_id
            for record in artifacts
            if record.artifact_type == "verification_record"
            and _grants_authority(record.artifact_type, record.status)
            for work_order_id in _relation_targets(record, "verifies_work_order")
        }
        for work_order in artifacts:
            if (
                work_order.artifact_type == "work_order"
                and work_order.status in {"verified", "released"}
                and work_order.artifact_id not in verified_work
            ):
                _add_error(
                    errors,
                    work_order,
                    report_root,
                    "E010",
                    f"{work_order.status} work order requires coverage by a verified or released verification record",
                    plane="policy",
                )

    for artifact in artifacts:
        if artifact.artifact_type == "verification_record":
            for field_name in ("evidence_paths",):
                duplicates = _duplicate_strings(artifact.metadata.get(field_name))
                if duplicates:
                    _add_error(
                        errors,
                        artifact,
                        report_root,
                        "E010",
                        f"field '{field_name}' contains duplicate values: {', '.join(duplicates)}",
                        plane="governance",
                    )
            for relation_name in ("verifies_work_order", "conforms_to", "superseded_by"):
                duplicates = _duplicate_strings(artifact.relations.get(relation_name))
                if duplicates:
                    _add_error(
                        errors,
                        artifact,
                        report_root,
                        "E010",
                        f"relation '{relation_name}' contains duplicate targets: {', '.join(duplicates)}",
                        plane="governance",
                    )
            work_order_ids = _relation_targets(artifact, "verifies_work_order")
            verification_ids = _relation_targets(artifact, "conforms_to")
            declared_verification: set[str] = set()
            for work_order_id in work_order_ids:
                work_order = catalog.get(work_order_id)
                if work_order is None or work_order.artifact_type != "work_order":
                    continue
                declared_verification.update(_relation_targets(work_order, "verification"))
                if (
                    _active_record_status(artifact.artifact_type, artifact.status)
                    and not _grants_authority(work_order.artifact_type, work_order.status)
                ):
                    _add_error(
                        errors,
                        artifact,
                        report_root,
                        "E010",
                        f"active verification record requires active work order '{work_order_id}'",
                        plane="governance",
                    )
            for verification_id in verification_ids:
                verification = catalog.get(verification_id)
                if (
                    verification is not None
                    and verification.artifact_type == "verification"
                    and _active_record_status(artifact.artifact_type, artifact.status)
                    and not _grants_authority(verification.artifact_type, verification.status)
                ):
                    _add_error(
                        errors,
                        artifact,
                        report_root,
                        "E010",
                        f"active verification record requires active verification contract '{verification_id}'",
                        plane="governance",
                    )
            missing_verification = declared_verification - verification_ids
            extra_verification = verification_ids - declared_verification
            if missing_verification and (
                "prepared_at" in artifact.metadata or len(work_order_ids) > 1
            ):
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E010",
                    f"verification record is missing contracts declared by selected work: {', '.join(sorted(missing_verification))}",
                    plane="governance",
                )
            if extra_verification:
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E010",
                    f"verification record includes contracts not declared by selected work: {', '.join(sorted(extra_verification))}",
                    plane="governance",
                )
            if len(work_order_ids) > 1:
                evidence_paths = artifact.metadata.get("evidence_paths", [])
                normalized_paths = [item for item in evidence_paths if isinstance(item, str)] if isinstance(evidence_paths, list) else []
                uncovered = [
                    work_order_id
                    for work_order_id in sorted(work_order_ids)
                    if not any(evidence_path_is_keyed_to(path, work_order_id) for path in normalized_paths)
                ]
                if uncovered:
                    _add_error(
                        errors,
                        artifact,
                        report_root,
                        "E010",
                        f"aggregate evidence is not keyed to work orders: {', '.join(uncovered)}",
                        plane="governance",
                    )
            if artifact.status == "superseded":
                successor_ids = sorted(_relation_targets(artifact, "superseded_by"))
                if len(successor_ids) == 1:
                    successor_id = successor_ids[0]
                    successor = catalog.get(successor_id)
                    if successor is not None and successor.artifact_type == "verification_record":
                        if not _grants_authority(successor.artifact_type, successor.status):
                            _add_error(
                                errors,
                                artifact,
                                report_root,
                                "E010",
                                f"superseding verification record '{successor_id}' must be verified or released",
                                plane="governance",
                            )
                        missing_work = work_order_ids - _relation_targets(successor, "verifies_work_order")
                        if missing_work:
                            _add_error(
                                errors,
                                artifact,
                                report_root,
                                "E010",
                                f"superseding verification record '{successor_id}' omits work orders: {', '.join(sorted(missing_work))}",
                                plane="governance",
                            )
            if artifact.artifact_id in supersession_cycle_nodes:
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E010",
                    f"verification supersession cycle detected among: {', '.join(sorted(supersession_cycle_nodes))}",
                    plane="governance",
                )

        if artifact.artifact_type != "release_record":
            continue
        for relation_name in ("satisfies", "includes_verification", "releases_work"):
            duplicates = _duplicate_strings(artifact.relations.get(relation_name))
            if duplicates:
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E010",
                    f"relation '{relation_name}' contains duplicate targets: {', '.join(duplicates)}",
                    plane="governance",
                )
        version = artifact.metadata.get("version")
        if _reserves_version(artifact.status) and isinstance(version, str) and version.strip():
            release_versions.setdefault(version.strip(), []).append(artifact)
        release_commit = artifact.metadata.get("commit")
        release_format = artifact.metadata.get("git_object_format")
        released_work = _relation_targets(artifact, "releases_work")
        for work_order_id in released_work:
            work_order = catalog.get(work_order_id)
            if (
                work_order is not None
                and work_order.artifact_type == "work_order"
                and _active_record_status(artifact.artifact_type, artifact.status)
                and work_order.status not in RELEASABLE_WORK_STATUSES
            ):
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E010",
                    f"active release record requires implemented, verified, or released work order '{work_order_id}'",
                    plane="governance",
                )
        verification_work: set[str] = set()
        for verification_id in _relation_targets(artifact, "includes_verification"):
            verification = catalog.get(verification_id)
            if verification is None or verification.artifact_type != "verification_record":
                continue
            if _active_record_status(verification.artifact_type, verification.status):
                verification_work.update(_relation_targets(verification, "verifies_work_order"))
            if _active_record_status(artifact.artifact_type, artifact.status) and verification.status == "superseded":
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E010",
                    f"active release record must not include superseded verification record '{verification_id}'",
                    plane="governance",
                )
            if release_commit != verification.metadata.get("commit") or release_format != verification.metadata.get("git_object_format"):
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E010",
                    f"release commit does not match verification record '{verification_id}'",
                    plane="governance",
                )
            if (
                _grants_authority(artifact.artifact_type, artifact.status)
                and not _grants_authority(verification.artifact_type, verification.status)
            ):
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E010",
                    f"released record requires verified included record '{verification_id}'",
                    plane="governance",
                )
        missing_work = released_work - verification_work
        if missing_work:
            _add_error(
                errors,
                artifact,
                report_root,
                "E010",
                f"released work orders are not covered by included verification records: {', '.join(sorted(missing_work))}",
                plane="governance",
            )
        extra_work = verification_work - released_work
        if extra_work:
            _add_error(
                errors,
                artifact,
                report_root,
                "E010",
                f"included verification records cover work orders absent from the release: {', '.join(sorted(extra_work))}",
                plane="governance",
            )
        for contract_id in _relation_targets(artifact, "satisfies"):
            contract = catalog.get(contract_id)
            if contract is None or contract.artifact_type != "release_contract":
                continue
            if (
                _active_record_status(artifact.artifact_type, artifact.status)
                and not _grants_authority(contract.artifact_type, contract.status)
            ):
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E010",
                    f"active release record requires active release contract '{contract_id}'",
                    plane="governance",
                )
            ungated = released_work - _relation_targets(contract, "gates")
            if ungated:
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E010",
                    f"release contract '{contract_id}' does not gate work orders: {', '.join(sorted(ungated))}",
                    plane="governance",
                )

    for version, records in sorted(release_versions.items()):
        if len(records) < 2:
            continue
        record_ids = ", ".join(sorted(record.artifact_id for record in records))
        for record in records:
            _add_error(
                errors,
                record,
                report_root,
                "E010",
                f"duplicate release record version '{version}' among {record_ids}",
                plane="governance",
            )
    return errors


def _supersession_cycle_nodes(artifacts: list[Artifact]) -> set[str]:
    graph = {
        artifact.artifact_id: sorted(_relation_targets(artifact, "superseded_by"))
        for artifact in artifacts
        if artifact.artifact_type == "verification_record"
    }
    state: dict[str, int] = {}
    cycle_nodes: set[str] = set()

    for start in sorted(graph):
        if state.get(start, 0) != 0:
            continue
        path = [start]
        positions = {start: 0}
        frames = [(start, 0)]
        state[start] = 1
        while frames:
            node, successor_index = frames[-1]
            successors = graph.get(node, [])
            if successor_index >= len(successors):
                frames.pop()
                path.pop()
                positions.pop(node, None)
                state[node] = 2
                continue
            successor = successors[successor_index]
            frames[-1] = (node, successor_index + 1)
            if successor not in graph:
                continue
            successor_state = state.get(successor, 0)
            if successor_state == 0:
                state[successor] = 1
                positions[successor] = len(path)
                path.append(successor)
                frames.append((successor, 0))
            elif successor_state == 1:
                cycle_nodes.update(path[positions[successor] :])
    return cycle_nodes


def _relation_targets(artifact: Artifact, relation_name: str) -> set[str]:
    value = artifact.relations.get(relation_name, [])
    if not isinstance(value, list):
        return set()
    return {item for item in value if isinstance(item, str)}


def _duplicate_strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    strings = [item.strip() for item in value if isinstance(item, str) and item.strip()]
    seen: set[str] = set()
    duplicates: set[str] = set()
    for item in strings:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return sorted(duplicates)


def validate_operating_contract_readiness(
    artifacts: list[Artifact],
    report_root: Path,
    *,
    require_verified_work: bool = False,
) -> list[Diagnostic]:
    """Validate the implementation path behind each active OPS assurance claim."""

    errors: list[Diagnostic] = []
    catalog = {
        artifact.artifact_id: artifact
        for artifact in artifacts
        if artifact.artifact_id != "<unknown>"
    }
    completed_work_by_requirement: dict[str, set[str]] = {}
    for work_order in artifacts:
        if (
            work_order.artifact_type != "work_order"
            or work_order.status not in RELEASABLE_WORK_STATUSES
        ):
            continue
        for requirement_id in _relation_targets(work_order, "implements"):
            completed_work_by_requirement.setdefault(requirement_id, set()).add(
                work_order.artifact_id
            )

    verified_work = {
        work_order_id
        for record in artifacts
        if record.artifact_type == "verification_record"
        and _grants_authority(record.artifact_type, record.status)
        for work_order_id in _relation_targets(record, "verifies_work_order")
    }

    for contract in artifacts:
        if (
            contract.artifact_type != "operating_contract"
            or not _grants_authority(contract.artifact_type, contract.status)
        ):
            continue
        for requirement_id in sorted(_relation_targets(contract, "assures")):
            requirement = catalog.get(requirement_id)
            # Missing and wrong-type targets are owned by validate_relations.
            if requirement is None or requirement.artifact_type != "requirement":
                continue
            if not _grants_authority(requirement.artifact_type, requirement.status):
                _add_error(
                    errors,
                    contract,
                    report_root,
                    "E017",
                    f"active operating contract assures inactive requirement '{requirement_id}'",
                    plane="governance",
                )
                continue

            completed_work = completed_work_by_requirement.get(requirement_id, set())
            if not completed_work:
                _add_error(
                    errors,
                    contract,
                    report_root,
                    "E017",
                    f"active operating contract assures requirement '{requirement_id}' without completed implementing work",
                    plane="governance",
                )
                continue

            if require_verified_work and completed_work.isdisjoint(verified_work):
                _add_error(
                    errors,
                    contract,
                    report_root,
                    "E018",
                    f"active operating contract assures requirement '{requirement_id}' without a verified or released VREC covering completed implementing work",
                    plane="policy",
                )

    return errors


def architecture_traceability_state(
    artifact: Artifact,
    catalog: dict[str, Artifact],
) -> dict[str, Any]:
    """Return deterministic typed or compatibility architecture traceability."""

    if artifact.artifact_type != "architecture":
        return {
            "state": "not_applicable",
            "addresses": [],
            "conforms_to": [],
            "transitive_requirements": [],
            "missing_from_conforming_specifications": [],
            "legacy_targets": [],
            "issues": [],
        }

    relations = artifact.relations
    issues: list[str] = []

    def values(name: str, *, required: bool) -> list[str]:
        raw = relations.get(name)
        if raw is None:
            if required:
                issues.append(f"architecture relation '{name}' is required")
            return []
        if not isinstance(raw, list):
            issues.append(f"architecture relation '{name}' must be an array")
            return []
        invalid = [item for item in raw if not isinstance(item, str) or not item.strip()]
        if invalid:
            issues.append(f"architecture relation '{name}' contains a non-string or empty target")
        clean = [item.strip() for item in raw if isinstance(item, str) and item.strip()]
        duplicates = _duplicate_strings(raw)
        if duplicates:
            issues.append(f"architecture relation '{name}' contains duplicates: {', '.join(duplicates)}")
        if required and not clean:
            issues.append(f"architecture relation '{name}' must not be empty")
        return sorted(set(clean))

    typed_present = "addresses" in relations or "conforms_to" in relations
    legacy_present = "constrains" in relations
    addresses = values("addresses", required=typed_present)
    conforms_to = values("conforms_to", required=typed_present)
    legacy_targets = values("constrains", required=legacy_present)

    transitive_requirements: set[str] = set()
    for specification_id in conforms_to:
        specification = catalog.get(specification_id)
        if specification is None or specification.artifact_type != "specification":
            continue
        transitive_requirements.update(_relation_targets(specification, "specifies"))
        if (
            _grants_authority(artifact.artifact_type, artifact.status)
            and not _grants_authority(specification.artifact_type, specification.status)
        ):
            issues.append(
                f"active architecture conforms to inactive specification '{specification_id}'"
            )

    if _grants_authority(artifact.artifact_type, artifact.status):
        for requirement_id in addresses:
            requirement = catalog.get(requirement_id)
            if (
                requirement is not None
                and requirement.artifact_type == "requirement"
                and not _grants_authority(requirement.artifact_type, requirement.status)
            ):
                issues.append(
                    f"active architecture addresses inactive requirement '{requirement_id}'"
                )

    missing = sorted(set(addresses) - transitive_requirements)
    if typed_present and missing:
        issues.append(
            "addressed requirements are not specified by a conforming specification: "
            + ", ".join(missing)
        )

    state = "typed"
    if typed_present:
        if legacy_present:
            for target_id in legacy_targets:
                target = catalog.get(target_id)
                if target is None:
                    continue
                if target.artifact_type == "requirement" and target_id not in addresses:
                    issues.append(
                        f"legacy requirement target '{target_id}' is absent from addresses"
                    )
                elif target.artifact_type == "specification" and target_id not in conforms_to:
                    issues.append(
                        f"legacy specification target '{target_id}' is absent from conforms_to"
                    )
                elif target.artifact_type not in {"requirement", "specification"}:
                    issues.append(
                        f"legacy target '{target_id}' has unsupported type '{target.artifact_type}'"
                    )
            state = "dual_declared"
    elif legacy_present and artifact.status in LEGACY_ARCHITECTURE_STATUSES:
        target_types = {
            catalog[target_id].artifact_type
            for target_id in legacy_targets
            if target_id in catalog
        }
        if target_types == {"requirement"}:
            state = "legacy_requirement_trace"
        elif target_types == {"specification"}:
            state = "legacy_specification_trace"
        else:
            state = "legacy_ambiguous"
            issues.append(
                "completed legacy architecture constrains relation must target only requirements or only specifications"
            )
    else:
        state = "missing_typed_relations"
        issues.append(
            "new or ongoing architecture requires typed addresses and conforms_to relations"
        )

    if issues:
        state = "invalid"
    return {
        "state": state,
        "addresses": addresses,
        "conforms_to": conforms_to,
        "transitive_requirements": sorted(transitive_requirements),
        "missing_from_conforming_specifications": missing,
        "legacy_targets": legacy_targets,
        "issues": sorted(set(issues)),
    }


def validate_architecture_traceability(
    artifacts: list[Artifact],
    report_root: Path,
) -> tuple[list[Diagnostic], list[Diagnostic]]:
    errors: list[Diagnostic] = []
    warnings: list[Diagnostic] = []
    catalog = {
        artifact.artifact_id: artifact
        for artifact in artifacts
        if artifact.artifact_id != "<unknown>"
    }
    for artifact in artifacts:
        if artifact.artifact_type != "architecture":
            continue
        traceability = architecture_traceability_state(artifact, catalog)
        for issue in traceability["issues"]:
            _add_error(
                errors,
                artifact,
                report_root,
                "E016",
                issue,
                plane="governance",
            )
        if traceability["state"] in {
            "dual_declared",
            "legacy_requirement_trace",
            "legacy_specification_trace",
        }:
            warnings.append(
                Diagnostic(
                    _display_path(artifact.path, report_root),
                    "W015",
                    f"architecture uses deprecated constrains relation ({traceability['state']}); migrate through accountable governance",
                    "maintenance",
                )
            )
    return errors, warnings


def decision_assessment_state(artifact: Artifact) -> dict[str, Any]:
    """Return a deterministic, non-authoritative architecture assessment state."""

    raw = artifact.metadata.get("decision_assessment")
    if artifact.artifact_type != "architecture":
        return {
            "state": "invalid" if raw is not None else "not_applicable",
            "outcome": None,
            "triggers": [],
            "rationale": None,
            "assessed_by": None,
            "issues": ["decision_assessment is allowed only on architecture artifacts"] if raw is not None else [],
        }
    if raw is None:
        legacy = artifact.status in LEGACY_ARCHITECTURE_STATUSES
        return {
            "state": "legacy_missing" if legacy else "missing",
            "outcome": None,
            "triggers": [],
            "rationale": None,
            "assessed_by": None,
            "issues": [] if legacy else ["architecture decision assessment is required"],
        }
    if not isinstance(raw, dict):
        return {
            "state": "invalid",
            "outcome": None,
            "triggers": [],
            "rationale": None,
            "assessed_by": None,
            "issues": ["decision_assessment must be a TOML table"],
        }

    issues: list[str] = []
    outcome_value = raw.get("outcome")
    outcome = outcome_value.strip() if isinstance(outcome_value, str) else None
    if outcome not in DECISION_ASSESSMENT_OUTCOMES:
        issues.append("decision_assessment outcome must be adr_required or no_significant_decision")

    triggers_value = raw.get("triggers")
    triggers: list[str] = []
    if not isinstance(triggers_value, list):
        issues.append("decision_assessment triggers must be an array")
    else:
        invalid_items = [item for item in triggers_value if not isinstance(item, str) or not item.strip()]
        if invalid_items:
            issues.append("decision_assessment triggers contain a non-string or empty value")
        triggers = [item.strip() for item in triggers_value if isinstance(item, str) and item.strip()]
        duplicates = _duplicate_strings(triggers_value)
        if duplicates:
            issues.append(f"decision_assessment triggers contain duplicates: {', '.join(duplicates)}")
        unknown = sorted(set(triggers) - DECISION_TRIGGERS)
        if unknown:
            issues.append(f"decision_assessment triggers are unknown: {', '.join(unknown)}")

    rationale_value = raw.get("rationale")
    rationale = rationale_value.strip() if isinstance(rationale_value, str) else None
    if not rationale:
        issues.append("decision_assessment rationale must be a non-empty string")
    elif len(rationale) > MAX_ASSESSMENT_RATIONALE_LENGTH:
        issues.append(
            f"decision_assessment rationale exceeds {MAX_ASSESSMENT_RATIONALE_LENGTH} characters"
        )

    assessor_value = raw.get("assessed_by")
    assessed_by = assessor_value.strip() if isinstance(assessor_value, str) else None
    if not assessed_by:
        issues.append("decision_assessment assessed_by must be a non-empty string")
    elif len(assessed_by) > MAX_ASSESSOR_LENGTH:
        issues.append(f"decision_assessment assessed_by exceeds {MAX_ASSESSOR_LENGTH} characters")

    unknown_fields = sorted(set(raw) - {"outcome", "triggers", "rationale", "assessed_by"})
    if unknown_fields:
        issues.append(f"decision_assessment contains unknown fields: {', '.join(unknown_fields)}")
    if outcome == "adr_required" and not triggers:
        issues.append("adr_required decision assessment must declare at least one trigger")
    if outcome == "no_significant_decision" and triggers:
        issues.append("no_significant_decision assessment must not declare triggers")

    return {
        "state": "invalid" if issues else "valid",
        "outcome": outcome,
        "triggers": sorted(set(triggers)),
        "rationale": rationale,
        "assessed_by": assessed_by,
        "issues": issues,
    }


def work_order_assurance_state(artifact: Artifact) -> dict[str, Any]:
    """Return the explicit commit-bound assurance classification for a work order."""

    raw = artifact.metadata.get("assurance")
    if artifact.artifact_type != "work_order":
        return {
            "state": "invalid" if raw is not None else "not_applicable",
            "commit_bound_verification": None,
            "rationale": None,
            "decided_by": None,
            "issues": ["assurance is allowed only on work-order artifacts"] if raw is not None else [],
        }
    if raw is None:
        return {
            "state": "missing",
            "commit_bound_verification": None,
            "rationale": None,
            "decided_by": None,
            "issues": [],
        }
    if not isinstance(raw, dict):
        return {
            "state": "invalid",
            "commit_bound_verification": None,
            "rationale": None,
            "decided_by": None,
            "issues": ["assurance must be a TOML table"],
        }

    issues: list[str] = []
    classification_value = raw.get("commit_bound_verification")
    classification = (
        classification_value.strip()
        if isinstance(classification_value, str)
        else None
    )
    if classification not in WORK_ORDER_ASSURANCE_VALUES:
        issues.append(
            "assurance commit_bound_verification must be required or not_required"
        )

    rationale_value = raw.get("rationale")
    rationale = rationale_value.strip() if isinstance(rationale_value, str) else None
    if not rationale:
        issues.append("assurance rationale must be a non-empty string")
    elif len(rationale) > MAX_ASSURANCE_RATIONALE_LENGTH:
        issues.append(
            f"assurance rationale exceeds {MAX_ASSURANCE_RATIONALE_LENGTH} characters"
        )

    decider_value = raw.get("decided_by")
    decided_by = decider_value.strip() if isinstance(decider_value, str) else None
    if not decided_by:
        issues.append("assurance decided_by must be a non-empty string")
    elif len(decided_by) > MAX_ASSURANCE_DECIDER_LENGTH:
        issues.append(
            f"assurance decided_by exceeds {MAX_ASSURANCE_DECIDER_LENGTH} characters"
        )

    unknown_fields = sorted(set(raw) - WORK_ORDER_ASSURANCE_FIELDS)
    if unknown_fields:
        issues.append(f"assurance contains unknown fields: {', '.join(unknown_fields)}")

    return {
        "state": "invalid" if issues else "valid",
        "commit_bound_verification": classification,
        "rationale": rationale,
        "decided_by": decided_by,
        "issues": issues,
    }


def validate_work_order_assurance(
    artifacts: list[Artifact],
    report_root: Path,
) -> list[Diagnostic]:
    errors: list[Diagnostic] = []
    for artifact in artifacts:
        assurance = work_order_assurance_state(artifact)
        for issue in assurance["issues"]:
            _add_error(
                errors,
                artifact,
                report_root,
                "E019",
                issue,
                plane="governance",
            )
        if (
            artifact.artifact_type == "work_order"
            and assurance["state"] == "missing"
            and artifact.status in {"approved", "in_progress"}
        ):
            _add_error(
                errors,
                artifact,
                report_root,
                "E019",
                "approved or in-progress work order requires an explicit assurance classification",
                plane="governance",
            )
    return errors


def _execution_scope_path_issue(value: object) -> str | None:
    if not isinstance(value, str) or not value or len(value) > 4096:
        return "path must be non-empty text of at most 4096 characters"
    if re.search(r"[\x00-\x1f\x7f]", value):
        return "path contains a control character"
    if "\\" in value or ":" in value or any(token in value for token in ("*", "?", "[", "]")):
        return "path contains an alternate separator, drive/URI marker, or wildcard"
    directory = value.endswith("/")
    candidate = value[:-1] if directory else value
    if not candidate or candidate.startswith("/"):
        return "path is empty or absolute"
    parts = PurePosixPath(candidate).parts
    if not parts or any(part in {"", ".", ".."} for part in parts):
        return "path contains an empty or dot component"
    reserved = {"CON", "PRN", "AUX", "NUL"} | {
        f"{prefix}{index}" for prefix in ("COM", "LPT") for index in range(1, 10)
    }
    for part in parts:
        if part.endswith((".", " ")) or part.rstrip(". ").split(".", 1)[0].upper() in reserved:
            return "path contains a reserved device or trailing dot/space component"
    normalized = PurePosixPath(*parts).as_posix() + ("/" if directory else "")
    if normalized != value:
        return "path is not normalized"
    return None


def validate_work_order_execution_scope(
    artifacts: list[Artifact],
    report_root: Path,
) -> list[Diagnostic]:
    errors: list[Diagnostic] = []
    for artifact in artifacts:
        if artifact.artifact_type != "work_order":
            continue
        table = artifact.metadata.get("execution_scope")
        if table is None:
            # Compatibility: the validator cannot infer whether an active work
            # order predates this contract. Checkpoint evaluation treats an
            # absent scope as not assessable; authoring templates require it for
            # new or resumed implementation.
            continue
        if not isinstance(table, dict) or set(table) != {"paths"}:
            _add_error(
                errors,
                artifact,
                report_root,
                "E020",
                "execution_scope must contain only paths",
                plane="governance",
            )
            continue
        paths = table.get("paths")
        if not isinstance(paths, list) or not paths:
            _add_error(
                errors,
                artifact,
                report_root,
                "E020",
                "execution_scope.paths must be a non-empty array",
                plane="governance",
            )
            continue
        folded: dict[str, str] = {}
        for value in paths:
            issue = _execution_scope_path_issue(value)
            if issue is not None:
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E020",
                    f"invalid execution scope path {value!r}: {issue}",
                    plane="governance",
                )
                continue
            key = value.casefold()
            if key in folded:
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E020",
                    f"duplicate or case-ambiguous execution scope path: {value!r}",
                    plane="governance",
                )
            folded[key] = value
    return errors


def validate_decision_assessments(
    artifacts: list[Artifact],
    report_root: Path,
) -> tuple[list[Diagnostic], list[Diagnostic]]:
    errors: list[Diagnostic] = []
    warnings: list[Diagnostic] = []
    active_decisions_by_architecture: dict[str, set[str]] = {}
    for decision in artifacts:
        if decision.artifact_type != "adr" or not _grants_authority(decision.artifact_type, decision.status):
            continue
        for architecture_id in _relation_targets(decision, "decides"):
            active_decisions_by_architecture.setdefault(architecture_id, set()).add(decision.artifact_id)

    for artifact in artifacts:
        assessment = decision_assessment_state(artifact)
        if artifact.artifact_type != "architecture":
            for issue in assessment["issues"]:
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E014",
                    issue,
                    plane="governance",
                )
            continue

        state = assessment["state"]
        if state in {"missing", "invalid"}:
            for issue in assessment["issues"]:
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E014",
                    issue,
                    plane="governance",
                )
            continue
        deciding = active_decisions_by_architecture.get(artifact.artifact_id, set())
        if state == "legacy_missing":
            warnings.append(
                Diagnostic(
                    _display_path(artifact.path, report_root),
                    "W014",
                    "completed legacy architecture has no decision_assessment; migrate during the compatibility window",
                    "maintenance",
                )
            )
            if not deciding:
                _add_error(
                    errors,
                    artifact,
                    report_root,
                    "E015",
                    "completed legacy architecture without decision_assessment requires an active deciding ADR",
                    plane="governance",
                )
            continue
        if (
            _grants_authority(artifact.artifact_type, artifact.status)
            and assessment["outcome"] == "adr_required"
            and not deciding
        ):
            _add_error(
                errors,
                artifact,
                report_root,
                "E015",
                "adr_required architecture has no active ADR whose decides relation targets it",
                plane="governance",
            )
    return errors, warnings


def validate_requirement_coverage(artifacts: list[Artifact], report_root: Path) -> list[Diagnostic]:
    errors: list[Diagnostic] = []
    active_specs = [
        artifact
        for artifact in artifacts
        if artifact.artifact_type == "specification"
        and _grants_authority(artifact.artifact_type, artifact.status)
    ]
    active_verifications = [
        artifact
        for artifact in artifacts
        if artifact.artifact_type == "verification"
        and _grants_authority(artifact.artifact_type, artifact.status)
    ]

    specified = set().union(*(_relation_targets(item, "specifies") for item in active_specs)) if active_specs else set()
    verified = set().union(*(_relation_targets(item, "verifies") for item in active_verifications)) if active_verifications else set()

    for artifact in artifacts:
        if (
            artifact.artifact_type != "requirement"
            or not _grants_authority(artifact.artifact_type, artifact.status)
        ):
            continue
        if artifact.artifact_id not in specified:
            _add_error(
                errors,
                artifact,
                report_root,
                "E007",
                f"active requirement '{artifact.artifact_id}' has no active specification coverage",
                plane="governance",
            )
        if artifact.artifact_id not in verified:
            _add_error(
                errors,
                artifact,
                report_root,
                "E008",
                f"active requirement '{artifact.artifact_id}' has no active verification coverage",
                plane="governance",
            )

    return errors


def validate_canonical_layout(
    artifacts: list[Artifact],
    repository_root: Path,
    artifact_root: Path,
    errors: list[Diagnostic],
) -> list[Diagnostic]:
    canonical_root = repository_root / "docs" / "engineering"
    if artifact_root.resolve() != canonical_root.resolve():
        return []

    invalid_paths = {item.path for item in errors}
    id_counts = Counter(artifact.artifact_id for artifact in artifacts)
    catalog = {
        artifact.artifact_id: artifact
        for artifact in artifacts
        if artifact.artifact_id != "<unknown>" and id_counts[artifact.artifact_id] == 1
    }
    warnings: list[Diagnostic] = []

    for artifact in artifacts:
        actual = _display_path(artifact.path, repository_root)
        artifact_type = artifact.artifact_type
        artifact_id = artifact.artifact_id
        if (
            actual in invalid_paths
            or artifact_type not in ARTIFACT_DIRECTORIES
            or id_counts[artifact_id] != 1
            or ID_PATTERN.fullmatch(artifact_id) is None
            or not artifact_id.startswith(ARTIFACT_PREFIXES[artifact_type])
        ):
            continue

        if artifact_type in {"verification_record", "release_record"}:
            relation = "verifies_work_order" if artifact_type == "verification_record" else "releases_work"
            work_order_ids = sorted(_relation_targets(artifact, relation))
            work_order_paths: list[str] = []
            complete = bool(work_order_ids)
            for work_order_id in work_order_ids:
                work_order = catalog.get(work_order_id)
                if work_order is None or work_order.artifact_type != "work_order":
                    complete = False
                    break
                work_order_paths.append(_display_path(work_order.path, repository_root))
            if not complete:
                continue
            domain = common_artifact_domain(work_order_paths)
            expected = repository_record_relative_path(artifact_type, artifact_id, domain)
        else:
            domain = artifact_domain_from_relative_path(actual)
            if domain is None:
                continue
            expected = canonical_artifact_relative_path(domain, artifact_type, artifact_id)

        expected_text = expected.as_posix()
        if actual != expected_text:
            warnings.append(
                Diagnostic(
                    actual,
                    "W013",
                    f"artifact '{artifact_id}' is valid outside its canonical location; expected '{expected_text}'",
                    "maintenance",
                )
            )
    return sorted(set(warnings))


def validate_repository(repository_root: Path, artifact_root: Path | None = None) -> ValidationReport:
    repository_root = repository_root.resolve()
    selected_artifact_root = (artifact_root or repository_root / "docs" / "engineering").resolve()
    revision_policy = load_revision_policy(repository_root)

    artifacts, parse_errors = load_artifacts(selected_artifact_root, repository_root)
    errors = list(parse_errors)

    assessment_warnings: list[Diagnostic] = []
    traceability_warnings: list[Diagnostic] = []
    if not selected_artifact_root.exists():
        errors.append(
            Diagnostic(
                _display_path(selected_artifact_root, repository_root),
                "E001",
                "artifact root does not exist",
                "structure",
            )
        )
    else:
        errors.extend(validate_common_metadata(artifacts, repository_root))
        errors.extend(validate_lifecycle_events(artifacts, repository_root))
        errors.extend(validate_type_specific_metadata(artifacts, repository_root))
        errors.extend(validate_relations(artifacts, repository_root))
        traceability_errors, traceability_warnings = validate_architecture_traceability(
            artifacts,
            repository_root,
        )
        errors.extend(traceability_errors)
        assessment_errors, assessment_warnings = validate_decision_assessments(
            artifacts,
            repository_root,
        )
        errors.extend(assessment_errors)
        errors.extend(validate_work_order_assurance(artifacts, repository_root))
        errors.extend(validate_work_order_execution_scope(artifacts, repository_root))
        errors.extend(
            validate_revision_consistency(
                artifacts,
                repository_root,
                require_verified_work=revision_policy["required_for_verified_work"],
            )
        )
        errors.extend(
            validate_operating_contract_readiness(
                artifacts,
                repository_root,
                require_verified_work=revision_policy["required_for_verified_work"],
            )
        )
        errors.extend(validate_requirement_coverage(artifacts, repository_root))

    warnings = [
        *assessment_warnings,
        *traceability_warnings,
        *validate_canonical_layout(artifacts, repository_root, selected_artifact_root, errors),
    ]
    return ValidationReport(
        artifacts=artifacts,
        errors=sorted(set(errors)),
        warnings=sorted(set(warnings)),
    )


def render_human(report: ValidationReport) -> str:
    status = "PASS" if report.valid else "FAIL"
    plane_summary = " | ".join(
        f"{plane} E{sum(item.plane == plane for item in report.errors)}/W{sum(item.plane == plane for item in report.warnings)}"
        for plane in VALIDATION_PLANES
    )
    lines = [
        f"Engineering artifact validation: {status}",
        f"Artifacts: {len(report.artifacts)} | Errors: {len(report.errors)} | Warnings: {len(report.warnings)}",
        f"Planes: {plane_summary}",
    ]
    if report.errors:
        lines.append("")
        lines.append("Errors:")
        for diagnostic in sorted(report.errors):
            lines.append(
                f"- [{diagnostic.code}] [{diagnostic.plane}] {diagnostic.path}: {diagnostic.message}"
            )
    if report.warnings:
        lines.append("")
        lines.append("Warnings:")
        for diagnostic in sorted(report.warnings):
            lines.append(
                f"- [{diagnostic.code}] [{diagnostic.plane}] {diagnostic.path}: {diagnostic.message}"
            )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate engineering artifact identity, relations, and coverage.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root (default: current directory).")
    parser.add_argument(
        "--artifact-root",
        type=Path,
        default=None,
        help="Artifact directory. Relative paths are resolved below --root; default: docs/engineering.",
    )
    parser.add_argument("--json", action="store_true", dest="as_json", help="Emit a machine-readable JSON report.")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    repository_root = args.root.resolve()
    artifact_root = args.artifact_root
    if artifact_root is not None and not artifact_root.is_absolute():
        artifact_root = repository_root / artifact_root

    report = validate_repository(repository_root, artifact_root)
    if args.as_json:
        print(json.dumps(report.to_dict(repository_root), indent=2, sort_keys=True))
    else:
        print(render_human(report))
    return 0 if report.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
