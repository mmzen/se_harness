"""Canonical, privacy-bounded released-evaluator evidence."""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from se_harness.evaluator_identity import PAYLOAD_MANIFEST
from se_harness.runtime_identity import RuntimeIdentity


EVIDENCE_SCHEMA = "se-harness-evaluator-evidence-v1"
MAX_EVIDENCE_BYTES = 64 * 1024
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
VERSION_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.!+\-]{0,127}")
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
    """Evaluator evidence is malformed, unsafe, or inconsistent."""


@dataclass(frozen=True)
class EvaluatorEvidence:
    value: dict[str, Any]
    canonical_bytes: bytes
    sha256: str


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise EvaluatorEvidenceError(f"duplicate evaluator evidence field: {key}")
        value[key] = item
    return value


def canonical_evidence_bytes(value: dict[str, Any]) -> bytes:
    return (
        json.dumps(value, ensure_ascii=True, separators=(",", ":"), sort_keys=True) + "\n"
    ).encode("utf-8")


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


def _validate_field_set(value: Any, expected: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != expected:
        raise EvaluatorEvidenceError(f"{label} field set is not canonical")
    return value


def validate_evaluator_evidence(
    value: Any,
    *,
    expected_evaluator: dict[str, Any] | None = None,
) -> dict[str, Any]:
    evidence = _validate_field_set(value, TOP_LEVEL_FIELDS, "evaluator evidence")
    if evidence.get("schema") != EVIDENCE_SCHEMA:
        raise EvaluatorEvidenceError("unsupported evaluator evidence schema")
    if evidence.get("role") != "released-evaluator":
        raise EvaluatorEvidenceError("evaluator evidence role must be released-evaluator")

    evaluator = _validate_field_set(evidence.get("evaluator"), EVALUATOR_FIELDS, "evaluator identity")
    version = evaluator.get("version")
    if not isinstance(version, str) or VERSION_PATTERN.fullmatch(version) is None:
        raise EvaluatorEvidenceError("invalid evaluator evidence version")
    if evaluator.get("payload_manifest") != PAYLOAD_MANIFEST:
        raise EvaluatorEvidenceError("unsupported evaluator evidence payload manifest")
    payload_sha256 = evaluator.get("payload_sha256")
    if not isinstance(payload_sha256, str) or SHA256_PATTERN.fullmatch(payload_sha256) is None:
        raise EvaluatorEvidenceError("invalid evaluator evidence payload SHA-256")
    archive_name = evaluator.get("archive_name")
    archive_sha256 = evaluator.get("archive_sha256")
    if (archive_name is None) != (archive_sha256 is None):
        raise EvaluatorEvidenceError("evaluator evidence archive fields must appear together")
    if archive_name is not None:
        expected_name = f"se_harness-{version.replace('-', '_')}-py3-none-any.whl"
        if archive_name != expected_name:
            raise EvaluatorEvidenceError("invalid evaluator evidence archive name")
        if not isinstance(archive_sha256, str) or SHA256_PATTERN.fullmatch(archive_sha256) is None:
            raise EvaluatorEvidenceError("invalid evaluator evidence archive SHA-256")
    if expected_evaluator is not None:
        expected = {
            "version": expected_evaluator.get("version"),
            "payload_manifest": expected_evaluator.get("payload_manifest"),
            "payload_sha256": expected_evaluator.get("payload_sha256"),
            "archive_name": expected_evaluator.get("archive_name"),
            "archive_sha256": expected_evaluator.get("archive_sha256"),
        }
        if evaluator != expected:
            raise EvaluatorEvidenceError("evaluator evidence differs from the standard lock")

    origins = _validate_field_set(evidence.get("origins"), ORIGIN_FIELDS, "evaluator origins")
    for label in sorted(ORIGIN_FIELDS):
        origin = origins.get(label)
        if not _is_normalized_origin(origin):
            raise EvaluatorEvidenceError(f"evaluator evidence origin is not normalized: {label}")

    environment = _validate_field_set(
        evidence.get("environment"), ENVIRONMENT_FIELDS, "evaluator environment"
    )
    if any(type(environment.get(field)) is not bool for field in ENVIRONMENT_FIELDS):
        raise EvaluatorEvidenceError("evaluator evidence environment fields must be Boolean")
    if environment["user_site_enabled"]:
        raise EvaluatorEvidenceError("evaluator evidence enables user site-packages")
    if environment["pythonpath_present"]:
        raise EvaluatorEvidenceError("evaluator evidence inherited PYTHONPATH")
    if not environment["entry_point_resolved"]:
        raise EvaluatorEvidenceError("evaluator evidence has no resolved entry point")
    if not environment["checkout_excluded"]:
        raise EvaluatorEvidenceError("evaluator evidence does not exclude the checkout")
    if evidence.get("diagnostics") != []:
        raise EvaluatorEvidenceError("authoritative evaluator evidence must have no diagnostics")
    return evidence


def parse_evaluator_evidence(
    raw: bytes,
    *,
    expected_evaluator: dict[str, Any] | None = None,
) -> EvaluatorEvidence:
    if not raw or len(raw) > MAX_EVIDENCE_BYTES:
        raise EvaluatorEvidenceError("evaluator evidence size is invalid")
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvaluatorEvidenceError("evaluator evidence is not canonical UTF-8 JSON") from exc
    validated = validate_evaluator_evidence(value, expected_evaluator=expected_evaluator)
    canonical = canonical_evidence_bytes(validated)
    if raw != canonical:
        raise EvaluatorEvidenceError("evaluator evidence bytes are not canonical")
    return EvaluatorEvidence(validated, canonical, hashlib.sha256(canonical).hexdigest())


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
    return EvaluatorEvidence(value, canonical, hashlib.sha256(canonical).hexdigest())
