"""Fail-closed released-evaluator authority for installed-root mutations."""

from __future__ import annotations

import os
import sys
import sysconfig
import tomllib
from dataclasses import dataclass
from pathlib import Path

from se_harness import __version__
from se_harness.evaluator_evidence import EvaluatorEvidence, build_evaluator_evidence
from se_harness.evaluator_identity import (
    EvaluatorIdentityError,
    InstalledEvaluatorIdentity,
    installed_evaluator_identity,
)
from se_harness.installer import CONFIG_NAME, HarnessError, ensure_target, load_lock, safe_destination
from se_harness.runtime_identity import RuntimeIdentity, inspect_runtime_identity


PUBLIC_MUTATION_OPERATIONS = frozenset(
    {
        "capture-verification",
        "create-artifact",
        "delegated-vrec-prepare",
        "delegated-work-order-complete",
        "delegated-work-order-start",
        "installed-root-apply",
        "prepare-release",
        "renumber-artifacts-apply",
        "scaffold-domain",
        "transition-apply",
        "upgrade-apply",
    }
)


def evaluator_transition_required(
    old_lock: dict,
    target_identity: InstalledEvaluatorIdentity,
) -> bool:
    """Return whether applying the installed distribution changes evaluator identity."""

    return not (
        old_lock.get("schema") == 3
        and old_lock.get("tool_version") == target_identity.version
        and old_lock.get("evaluator") == target_identity.to_lock()
    )


@dataclass(frozen=True)
class MutationAuthority:
    operation: str
    identity: RuntimeIdentity
    evidence: EvaluatorEvidence
    # Set on an upgrade: the installed evaluator that will own the root after the
    # write, and whether writing it changes the recorded evaluator identity
    # (SPEC-REB-012 rule 2). No packet, no work order: the installed released
    # evaluator's version and payload digest are its identity.
    target_identity: InstalledEvaluatorIdentity | None = None
    transition: bool = False

    @property
    def evidence_bytes(self) -> bytes:
        return self.evidence.canonical_bytes

    @property
    def evidence_sha256(self) -> str:
        return self.evidence.sha256


def _failure(code: str, operation: str, message: str) -> HarnessError:
    return HarnessError(f"mutation guard {code} ({operation}): {message}")


def _configured_version(root: Path, operation: str) -> str:
    try:
        config_path = safe_destination(root, Path(CONFIG_NAME))
        value = tomllib.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError, HarnessError) as exc:
        raise _failure("MG001", operation, f"cannot read the standard config: {exc}") from exc
    harness = value.get("harness") if isinstance(value, dict) else None
    version = harness.get("tool_version") if isinstance(harness, dict) else None
    if not isinstance(version, str) or not version:
        raise _failure("MG001", operation, "the standard config has no tool version")
    return version


def _entry_point() -> Path | None:
    scripts = Path(sysconfig.get_path("scripts"))
    candidates = [scripts / "harnessctl"]
    if os.name == "nt":
        candidates.insert(0, scripts / "harnessctl.exe")
    return next((item for item in candidates if item.is_file()), None)


def _runtime_report(
    root: Path,
    *,
    version: str,
    payload_sha256: str,
    archive_sha256: str | None,
) -> RuntimeIdentity:
    return inspect_runtime_identity(
        role="released-evaluator",
        expected_version=version,
        expected_root=Path(sys.prefix),
        checkout_root=root,
        evaluator_payload_sha256=payload_sha256,
        evaluator_wheel_sha256=archive_sha256,
        entry_point=_entry_point(),
        require_entry_point=True,
    )


def require_mutation_authority(
    repository: Path,
    *,
    operation: str,
    allow_upgrade_transition: bool = False,
    require_archive: bool = False,
) -> MutationAuthority:
    """Prove released-evaluator identity before an installed-root write."""

    if operation not in PUBLIC_MUTATION_OPERATIONS:
        raise HarnessError(f"mutation guard operation is not registered: {operation}")
    root = ensure_target(repository, must_exist=True)
    try:
        lock = load_lock(root)
    except HarnessError as exc:
        raise _failure("MG001", operation, f"cannot read the standard lock: {exc}") from exc
    configured_version = _configured_version(root, operation)
    locked_version = lock.get("tool_version")
    if not isinstance(locked_version, str) or configured_version != locked_version:
        raise _failure("MG003", operation, "standard config and lock tool versions differ")

    target_identity: InstalledEvaluatorIdentity | None = None
    transition = False
    if allow_upgrade_transition:
        # The installed released evaluator is the target identity: its version and
        # installed-payload digest, with the archive digest as corroboration only
        # when the installation recorded one (REQ-REB-027, REQ-REB-028). Index
        # installs record none, and that is not a failure.
        try:
            target_identity = installed_evaluator_identity()
        except EvaluatorIdentityError as exc:
            raise _failure("MG004", operation, f"cannot identify the target evaluator: {exc}") from exc
        report = _runtime_report(
            root,
            version=__version__,
            payload_sha256=target_identity.payload_sha256,
            archive_sha256=target_identity.archive_sha256,
        )
        transition = evaluator_transition_required(lock, target_identity)
    else:
        if lock.get("schema") != 3:
            raise _failure(
                "MG002",
                operation,
                "ordinary mutation requires a schema-3 evaluator identity; use a separately governed upgrade",
            )
        evaluator = lock.get("evaluator")
        if not isinstance(evaluator, dict):
            raise _failure("MG001", operation, "the standard lock evaluator identity is unavailable")
        version = evaluator.get("version")
        payload_sha256 = evaluator.get("payload_sha256")
        archive_sha256 = evaluator.get("archive_sha256")
        if not isinstance(version, str) or not isinstance(payload_sha256, str):
            raise _failure("MG001", operation, "the standard lock evaluator identity is incomplete")
        if archive_sha256 is not None and not isinstance(archive_sha256, str):
            raise _failure("MG001", operation, "the standard lock evaluator archive identity is invalid")
        if require_archive and archive_sha256 is None:
            raise _failure(
                "MG004",
                operation,
                "this mutation requires a locked evaluator archive identity",
            )
        report = _runtime_report(
            root,
            version=version,
            payload_sha256=payload_sha256,
            archive_sha256=archive_sha256,
        )
    if report.diagnostics:
        detail = "; ".join(
            f"{item.code} {item.subject}: {item.message}" for item in report.diagnostics
        )
        raise _failure("MG005", operation, detail)
    try:
        evidence = build_evaluator_evidence(report)
    except ValueError as exc:
        raise _failure("MG006", operation, f"cannot canonicalize evaluator evidence: {exc}") from exc
    return MutationAuthority(operation, report, evidence, target_identity, transition)
