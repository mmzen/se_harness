"""Canonical, privacy-bounded released-evaluator evidence."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from se_harness.evaluator_identity import PAYLOAD_MANIFEST
from se_harness.runtime_identity import RuntimeIdentity
from se_harness.integrity import VERSION_PATTERN, canonical_json_bytes, raw_sha256, unique_object_hook


EVIDENCE_SCHEMA = "se-harness-evaluator-evidence-v1"
MAX_EVIDENCE_BYTES = 64 * 1024
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
NORMALIZED_ORIGIN_PATTERN = re.compile(r"<evaluator-root>(?:/[A-Za-z0-9._+()@ -]+)*")
TOP_LEVEL_FIELDS = {"schema", "role", "evaluator", "origins", "environment", "diagnostics"}
EVALUATOR_FIELDS = {
    "version",
    "payload_manifest",
    "payload_sha256",
    "archive_name",
    "archive_sha256",
}
ORIGIN_FIELDS = {"python_executable", "module", "distribution", "templates", "entry_point"}
ENVIRONMENT_FIELDS = {
    "isolated_python",
    "user_site_enabled",
    "pythonpath_present",
    "entry_point_resolved",
    "checkout_excluded",
}


class EvaluatorEvidenceError(ValueError):
    """Evaluator evidence is malformed, unsafe, or inconsistent.

    `reason` names the check that refused (ECP-ENG-006), so the engine can render its own
    diagnostic for the same defect; the message is this module's.
    """

    def __init__(self, message: str, reason: str = "") -> None:
        super().__init__(message)
        self.reason = reason


@dataclass(frozen=True)
class EvaluatorEvidence:
    value: dict[str, Any]
    canonical_bytes: bytes
    sha256: str


_unique_object = unique_object_hook(lambda key: EvaluatorEvidenceError(f"duplicate evaluator evidence field: {key}", "duplicate_field"))
#: The duplicate-key hook every reader of evidence JSON passes (the engine included).
unique_evidence_object = _unique_object


def canonical_evidence_bytes(value: dict[str, Any]) -> bytes:
    return canonical_json_bytes(value, ensure_ascii=True)  # ECP-PRM-006, ECP-PRM-007: the same bytes


def _lexical_relative(path: Path, root: Path) -> Path | None:
    try:
        return Path(os.path.abspath(path)).relative_to(Path(os.path.abspath(root)))
    except ValueError:
        return None


def _resolved_relative(path: Path, root: Path) -> Path | None:
    try:
        return path.resolve().relative_to(root.resolve())
    except (OSError, ValueError):
        return None


def _normalized_origin(raw: str, evaluator_root: Path) -> str:
    path = Path(raw)
    relative = _lexical_relative(path, evaluator_root)
    if relative is None:
        relative = _resolved_relative(path, evaluator_root)
    if relative is None or any(part in {"", ".", ".."} for part in relative.parts):
        raise EvaluatorEvidenceError("runtime origin is outside the evaluator root")
    suffix = relative.as_posix()
    return "<evaluator-root>" if suffix == "." else f"<evaluator-root>/{suffix}"


def _is_normalized_origin(value: Any) -> bool:
    if not isinstance(value, str) or NORMALIZED_ORIGIN_PATTERN.fullmatch(value) is None:
        return False
    suffix = value.removeprefix("<evaluator-root>").removeprefix("/")
    return not suffix or all(part not in {"", ".", ".."} for part in suffix.split("/"))


def _validate_field_set(value: Any, expected: set[str], label: str, reason: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != expected:
        raise EvaluatorEvidenceError(f"{label} field set is not canonical", reason)
    return value


def normalize_evaluator_identity(expected: dict[str, Any]) -> dict[str, Any]:
    """The five identity fields of a lock's evaluator table, in the evidence's shape."""

    return {
        "version": expected.get("version"),
        "payload_manifest": expected.get("payload_manifest"),
        "payload_sha256": expected.get("payload_sha256"),
        "archive_name": expected.get("archive_name"),
        "archive_sha256": expected.get("archive_sha256"),
    }


#: Every `reason` `validate_evaluator_evidence` can raise, in the order it checks them.
EVIDENCE_REASONS = (
    "field_set", "schema", "role", "identity_field_set", "payload_manifest", "version", "payload_sha256",
    "archive_pair", "archive_name", "archive_sha256", "archive_required", "origins_field_set", "origin",
    "environment_field_set", "environment_boolean", "isolated_python", "user_site", "pythonpath",
    "entry_point", "checkout", "diagnostics", "lock",
)


def validate_evaluator_evidence(
    value: Any,
    *,
    expected_evaluator: dict[str, Any] | None = None,
    require_archive: bool = False,
    require_isolated_python: bool = False,
) -> dict[str, Any]:
    """The one validator of an evaluator-evidence document (ECP-ENG-006).

    Checks run in the engine's order; each refusal carries its `reason`. The
    engine requires an isolated interpreter and, for a release record, an archive;
    the package's own readers take the defaults.
    """

    evidence = _validate_field_set(value, TOP_LEVEL_FIELDS, "evaluator evidence", "field_set")
    if evidence.get("schema") != EVIDENCE_SCHEMA:
        raise EvaluatorEvidenceError("unsupported evaluator evidence schema", "schema")
    if evidence.get("role") != "released-evaluator":
        raise EvaluatorEvidenceError("evaluator evidence role must be released-evaluator", "role")

    evaluator = _validate_field_set(evidence.get("evaluator"), EVALUATOR_FIELDS, "evaluator identity", "identity_field_set")
    if evaluator.get("payload_manifest") != PAYLOAD_MANIFEST:
        raise EvaluatorEvidenceError("unsupported evaluator evidence payload manifest", "payload_manifest")
    version = evaluator.get("version")
    if not isinstance(version, str) or VERSION_PATTERN.fullmatch(version) is None:
        raise EvaluatorEvidenceError("invalid evaluator evidence version", "version")
    payload_sha256 = evaluator.get("payload_sha256")
    if not isinstance(payload_sha256, str) or SHA256_PATTERN.fullmatch(payload_sha256) is None:
        raise EvaluatorEvidenceError("invalid evaluator evidence payload SHA-256", "payload_sha256")
    archive_name = evaluator.get("archive_name")
    archive_sha256 = evaluator.get("archive_sha256")
    if (archive_name is None) != (archive_sha256 is None):
        raise EvaluatorEvidenceError("evaluator evidence archive fields must appear together", "archive_pair")
    if archive_name is not None:
        expected_name = f"se_harness-{version.replace('-', '_')}-py3-none-any.whl"
        if archive_name != expected_name:
            raise EvaluatorEvidenceError("invalid evaluator evidence archive name", "archive_name")
        if not isinstance(archive_sha256, str) or SHA256_PATTERN.fullmatch(archive_sha256) is None:
            raise EvaluatorEvidenceError("invalid evaluator evidence archive SHA-256", "archive_sha256")
    if require_archive and archive_name is None:
        raise EvaluatorEvidenceError("release evaluator evidence requires an archive name and SHA-256", "archive_required")

    origins = _validate_field_set(evidence.get("origins"), ORIGIN_FIELDS, "evaluator origins", "origins_field_set")
    for label in sorted(ORIGIN_FIELDS):
        origin = origins.get(label)
        if not _is_normalized_origin(origin):
            raise EvaluatorEvidenceError(f"evaluator evidence origin is not normalized: {label}", "origin")

    environment = _validate_field_set(
        evidence.get("environment"), ENVIRONMENT_FIELDS, "evaluator environment", "environment_field_set"
    )
    if any(type(environment.get(field)) is not bool for field in ENVIRONMENT_FIELDS):
        raise EvaluatorEvidenceError("evaluator evidence environment fields must be Boolean", "environment_boolean")
    if require_isolated_python and not environment["isolated_python"]:
        raise EvaluatorEvidenceError("evaluator evidence was not produced under an isolated interpreter", "isolated_python")
    if environment["user_site_enabled"]:
        raise EvaluatorEvidenceError("evaluator evidence enables user site-packages", "user_site")
    if environment["pythonpath_present"]:
        raise EvaluatorEvidenceError("evaluator evidence inherited PYTHONPATH", "pythonpath")
    if not environment["entry_point_resolved"]:
        raise EvaluatorEvidenceError("evaluator evidence has no resolved entry point", "entry_point")
    if not environment["checkout_excluded"]:
        raise EvaluatorEvidenceError("evaluator evidence does not exclude the checkout", "checkout")
    if evidence.get("diagnostics") != []:
        raise EvaluatorEvidenceError("authoritative evaluator evidence must have no diagnostics", "diagnostics")
    if expected_evaluator is not None and evaluator != normalize_evaluator_identity(expected_evaluator):
        raise EvaluatorEvidenceError("evaluator evidence differs from the standard lock", "lock")
    return evidence


def parse_evaluator_evidence(
    raw: bytes,
    *,
    expected_evaluator: dict[str, Any] | None = None,
) -> EvaluatorEvidence:
    if not raw or len(raw) > MAX_EVIDENCE_BYTES:
        raise EvaluatorEvidenceError("evaluator evidence size is invalid", "size")
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvaluatorEvidenceError("evaluator evidence is not canonical UTF-8 JSON", "json") from exc
    validated = validate_evaluator_evidence(value, expected_evaluator=expected_evaluator)
    canonical = canonical_evidence_bytes(validated)
    if raw != canonical:
        raise EvaluatorEvidenceError("evaluator evidence bytes are not canonical", "canonical")
    return EvaluatorEvidence(validated, canonical, raw_sha256(canonical))


def build_evaluator_evidence(identity: RuntimeIdentity) -> EvaluatorEvidence:
    if not identity.passed or identity.role != "released-evaluator" or identity.diagnostics:
        raise EvaluatorEvidenceError("only a passing released evaluator can produce authority evidence")
    if identity.entry_point_origin is None:
        raise EvaluatorEvidenceError("released evaluator entry point is unavailable")
    if identity.evaluator_payload_manifest is None or identity.evaluator_payload_sha256 is None:
        raise EvaluatorEvidenceError("released evaluator payload identity is unavailable")
    evaluator_root = Path(identity.expected_root)
    value: dict[str, Any] = {
        "schema": EVIDENCE_SCHEMA,
        "role": "released-evaluator",
        "evaluator": {
            "version": identity.harness_version,
            "payload_manifest": identity.evaluator_payload_manifest,
            "payload_sha256": identity.evaluator_payload_sha256,
            "archive_name": identity.evaluator_archive_name,
            "archive_sha256": identity.evaluator_archive_sha256,
        },
        "origins": {
            "python_executable": _normalized_origin(identity.python_executable, evaluator_root),
            "module": _normalized_origin(identity.module_origin, evaluator_root),
            "distribution": _normalized_origin(identity.distribution_origin, evaluator_root),
            "templates": _normalized_origin(identity.template_origin, evaluator_root),
            "entry_point": _normalized_origin(identity.entry_point_origin, evaluator_root),
        },
        "environment": {
            "isolated_python": identity.isolated_python,
            "user_site_enabled": identity.user_site_enabled,
            "pythonpath_present": identity.pythonpath_present,
            "entry_point_resolved": identity.entry_point_origin is not None,
            "checkout_excluded": identity.checkout_root is not None,
        },
        "diagnostics": [],
    }
    validate_evaluator_evidence(value)
    canonical = canonical_evidence_bytes(value)
    return EvaluatorEvidence(value, canonical, raw_sha256(canonical))
