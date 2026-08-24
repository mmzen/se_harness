"""Bounded authorization for one released-evaluator identity transition."""

from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from se_harness.evaluator_identity import InstalledEvaluatorIdentity
from se_harness.hash_bound import (
    LOCK_RELATIVE,
    MATCH_MISMATCH,
    HashBoundError,
    compare_declared_digest,
)
from se_harness.legacy_release_evidence import (
    DECLARATION_FIELD,
    MAX_DECLARED_RECORDS,
    RELEASE_RECORD_PATTERN,
)


UPGRADE_AUTHORIZATION_SCHEMA = "se-harness-evaluator-upgrade-v1"
UPGRADE_EVIDENCE_SCHEMA = "se-harness-evaluator-upgrade-evidence-v1"
WORK_ORDER_PATTERN = re.compile(r"WO-[A-Z][A-Z0-9-]*-\d{3}")
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
VERSION_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.!+\-]{0,127}")
AUTHORIZATION_FIELDS = {
    "schema",
    "scope",
    "prior_lock_sha256",
    "target_version",
    "target_payload_sha256",
    "target_archive_name",
    "target_archive_sha256",
    "publication",
    "authorized_by",
}
# SPEC-LRE-001 rule 2: the required field set is unchanged and this is the only
# permitted optional key. Any further key remains rejected.
OPTIONAL_AUTHORIZATION_FIELDS = {DECLARATION_FIELD}
EXCLUDED_PARTS = {".git", "evidence", "node_modules", "target", "templates"}
MAX_ARTIFACT_BYTES = 256 * 1024


class UpgradeAuthorizationError(ValueError):
    """An evaluator transition has no exact, separately governed authority."""


@dataclass(frozen=True)
class UpgradeAuthorization:
    work_order: str
    artifact_path: str
    prior_lock_sha256: str
    target_version: str
    target_payload_sha256: str
    target_archive_name: str
    target_archive_sha256: str
    authorized_by: str
    # Ordered before the defaulted field below, which a dataclass requires of
    # every field without a default.
    prior_lock_match: str
    legacy_releases_without_evaluator_evidence: tuple[str, ...] = ()


def evaluator_transition_required(
    old_lock: dict[str, Any],
    target_identity: InstalledEvaluatorIdentity,
) -> bool:
    """Return whether applying the installed distribution changes evaluator identity."""

    return not (
        old_lock.get("schema") == 3
        and old_lock.get("tool_version") == target_identity.version
        and old_lock.get("evaluator") == target_identity.to_lock()
    )


def _front_matter(path: Path) -> dict[str, Any] | None:
    try:
        if path.is_symlink() or path.stat().st_size > MAX_ARTIFACT_BYTES:
            return None
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except (OSError, UnicodeError):
        return None
    if not lines or lines[0].strip() != "+++":
        return None
    try:
        closing = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "+++")
        value = tomllib.loads("\n".join(lines[1:closing]))
    except (StopIteration, tomllib.TOMLDecodeError):
        return None
    return value if isinstance(value, dict) else None


def _selected_work_order(repository: Path, work_order: str) -> tuple[Path, dict[str, Any]]:
    if WORK_ORDER_PATTERN.fullmatch(work_order) is None:
        raise UpgradeAuthorizationError("upgrade work order has an invalid ID")
    artifact_root = repository / "docs" / "engineering"
    matches: list[tuple[Path, dict[str, Any]]] = []
    if artifact_root.is_dir():
        for path in sorted(artifact_root.rglob("*.md"), key=lambda item: item.as_posix()):
            relative = path.relative_to(artifact_root)
            if any(part in EXCLUDED_PARTS for part in relative.parts):
                continue
            metadata = _front_matter(path)
            if metadata is not None and metadata.get("id") == work_order:
                matches.append((path, metadata))
    if len(matches) != 1:
        raise UpgradeAuthorizationError(
            f"upgrade work order {work_order} must resolve to exactly one formal artifact; found {len(matches)}"
        )
    path, metadata = matches[0]
    if metadata.get("type") != "work_order":
        raise UpgradeAuthorizationError(f"upgrade authority {work_order} is not a work order")
    if metadata.get("status") not in {"approved", "in_progress"}:
        raise UpgradeAuthorizationError(
            f"upgrade work order {work_order} must be approved or in_progress"
        )
    return path, metadata


def _required_text(value: dict[str, Any], field: str) -> str:
    selected = value.get(field)
    if not isinstance(selected, str) or not selected.strip():
        raise UpgradeAuthorizationError(f"evaluator_upgrade.{field} must be non-empty text")
    return selected.strip()


def _legacy_release_declaration(value: dict[str, Any]) -> tuple[str, ...]:
    """Return the packet's declared pre-enforcement release records, deduplicated."""

    declared = value.get(DECLARATION_FIELD)
    if declared is None:
        return ()
    if not isinstance(declared, list) or not all(isinstance(item, str) for item in declared):
        raise UpgradeAuthorizationError(f"evaluator_upgrade.{DECLARATION_FIELD} must be a string array")
    if len(declared) > MAX_DECLARED_RECORDS:
        raise UpgradeAuthorizationError(
            f"evaluator_upgrade.{DECLARATION_FIELD} exceeds {MAX_DECLARED_RECORDS} entries"
        )
    invalid = sorted({item for item in declared if RELEASE_RECORD_PATTERN.fullmatch(item) is None})
    if invalid:
        raise UpgradeAuthorizationError(
            f"evaluator_upgrade.{DECLARATION_FIELD} has an invalid release record ID: {invalid[0]!r}"
        )
    return tuple(sorted(set(declared)))


def load_upgrade_authorization(
    repository: Path,
    *,
    work_order: str,
    old_lock_bytes: bytes,
    target_identity: InstalledEvaluatorIdentity,
) -> UpgradeAuthorization:
    """Load and match one approved root-only upgrade packet."""

    path, metadata = _selected_work_order(repository, work_order)
    raw = metadata.get("evaluator_upgrade")
    if not isinstance(raw, dict):
        raise UpgradeAuthorizationError(
            f"upgrade work order {work_order} has no [evaluator_upgrade] packet"
        )
    unknown = sorted(set(raw) - AUTHORIZATION_FIELDS - OPTIONAL_AUTHORIZATION_FIELDS)
    missing = sorted(AUTHORIZATION_FIELDS - set(raw))
    if unknown or missing:
        details = []
        if missing:
            details.append("missing " + ", ".join(missing))
        if unknown:
            details.append("unknown " + ", ".join(unknown))
        raise UpgradeAuthorizationError("evaluator_upgrade field set is not canonical: " + "; ".join(details))
    if raw.get("schema") != UPGRADE_AUTHORIZATION_SCHEMA:
        raise UpgradeAuthorizationError("unsupported evaluator_upgrade schema")
    if raw.get("scope") != "standard-root-only":
        raise UpgradeAuthorizationError("evaluator_upgrade scope must be standard-root-only")
    if raw.get("publication") != "immutable":
        raise UpgradeAuthorizationError("target evaluator publication must be declared immutable")

    prior_lock_sha256 = _required_text(raw, "prior_lock_sha256")
    if SHA256_PATTERN.fullmatch(prior_lock_sha256) is None:
        raise UpgradeAuthorizationError("evaluator_upgrade.prior_lock_sha256 is invalid")
    try:
        prior_lock_match = compare_declared_digest(
            LOCK_RELATIVE, old_lock_bytes, prior_lock_sha256
        )
    except HashBoundError as exc:
        raise UpgradeAuthorizationError(
            f"cannot compare the prior lock under its declared hash-bound class: {exc}"
        ) from exc
    if prior_lock_match == MATCH_MISMATCH:
        raise UpgradeAuthorizationError("upgrade work order prior lock identity does not match the repository")

    target_version = _required_text(raw, "target_version")
    target_payload_sha256 = _required_text(raw, "target_payload_sha256")
    target_archive_name = _required_text(raw, "target_archive_name")
    target_archive_sha256 = _required_text(raw, "target_archive_sha256")
    authorized_by = _required_text(raw, "authorized_by")
    if VERSION_PATTERN.fullmatch(target_version) is None:
        raise UpgradeAuthorizationError("evaluator_upgrade.target_version is invalid")
    if SHA256_PATTERN.fullmatch(target_payload_sha256) is None:
        raise UpgradeAuthorizationError("evaluator_upgrade.target_payload_sha256 is invalid")
    if SHA256_PATTERN.fullmatch(target_archive_sha256) is None:
        raise UpgradeAuthorizationError("evaluator_upgrade.target_archive_sha256 is invalid")
    expected = target_identity.to_lock()
    if (
        target_version != expected.get("version")
        or target_payload_sha256 != expected.get("payload_sha256")
        or target_archive_name != expected.get("archive_name")
        or target_archive_sha256 != expected.get("archive_sha256")
    ):
        raise UpgradeAuthorizationError(
            "upgrade work order target identity does not match the installed released evaluator"
        )
    declared = _legacy_release_declaration(raw)
    return UpgradeAuthorization(
        work_order=work_order,
        artifact_path=path.relative_to(repository).as_posix(),
        prior_lock_sha256=prior_lock_sha256,
        target_version=target_version,
        target_payload_sha256=target_payload_sha256,
        target_archive_name=target_archive_name,
        target_archive_sha256=target_archive_sha256,
        authorized_by=authorized_by,
        prior_lock_match=prior_lock_match,
        legacy_releases_without_evaluator_evidence=declared,
    )


def validate_upgrade_evidence_path(path: Path, work_order: str) -> PurePosixPath:
    """Require work-order-keyed repository evidence below docs/engineering."""

    if path.is_absolute() or ".." in path.parts:
        raise UpgradeAuthorizationError("upgrade evidence path must be repository-relative")
    normalized = PurePosixPath(path.as_posix())
    if (
        len(normalized.parts) < 4
        or normalized.parts[:2] != ("docs", "engineering")
        or "evidence" not in normalized.parts[2:-1]
        or normalized.suffix != ".json"
        or not normalized.name.startswith(f"{work_order}-")
    ):
        raise UpgradeAuthorizationError(
            "upgrade evidence must be a WO-keyed JSON path below docs/engineering/.../evidence/"
        )
    return normalized
