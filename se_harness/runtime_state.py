"""External, single-writer runtime state for agentic admission.

All writes are confined to an explicitly supplied directory that must neither
alias, contain, nor be contained by the target repository.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
import threading
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping

from se_harness.agent_contract import canonical_json_bytes


RUNTIME_STATE_SCHEMA = "se-harness-agentic-runtime-state-v1"
SESSION_SCHEMA = "se-harness-agentic-session-v1"
NONCE_LEDGER_SCHEMA = "se-harness-agentic-nonce-ledger-v1"
RECOVERY_SCHEMA = "se-harness-agentic-recovery-v1"
REVOCATION_SCHEMA = "se-harness-agentic-revocations-v1"
MAX_NONCES = 1_024
_SHA256 = re.compile(r"[0-9a-f]{64}")
_NONCE = re.compile(r"[0-9a-f]{32,128}")
_REPOSITORY_ID = re.compile(r"[0-9a-f]{64}")
_TIMESTAMP = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")


class RuntimeStateError(RuntimeError):
    """A stable, bounded runtime-state diagnostic."""

    def __init__(self, code: str, message: str) -> None:
        text = "".join(character if character >= " " else "?" for character in str(message))[:512]
        super().__init__(f"{code}: {text or 'runtime state failure'}")
        self.code = code
        self.message = text


@dataclass(frozen=True)
class RuntimeSession:
    repository_id: str
    session_id: str
    owner_sha256: str


def _now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _require(pattern: re.Pattern[str], value: str, label: str) -> str:
    if not isinstance(value, str) or pattern.fullmatch(value) is None:
        raise RuntimeStateError("AEXRT001", f"{label} has an invalid form")
    return value


def _read_json(path: Path) -> dict[str, Any]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise RuntimeStateError("AEXRT002", f"cannot read runtime state: {exc}") from exc
    if len(raw) > 1_048_576:
        raise RuntimeStateError("AEXRT002", "runtime state exceeds its byte bound")
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise RuntimeStateError("AEXRT002", "runtime state is not valid UTF-8 JSON") from exc
    if not isinstance(value, dict) or canonical_json_bytes(value) != raw:
        raise RuntimeStateError("AEXRT002", "runtime state is not canonical JSON")
    return value


def _secure_directory(path: Path) -> None:
    try:
        path.mkdir(parents=True, exist_ok=True)
        if path.is_symlink() or not path.is_dir():
            raise RuntimeStateError("AEXRT004", "runtime path is not a regular directory")
        if os.name != "nt":
            path.chmod(0o700)
    except OSError as exc:
        raise RuntimeStateError("AEXRT004", f"cannot create secure runtime directory: {exc}") from exc


def _atomic_write(path: Path, value: Mapping[str, Any], *, exclusive: bool = False) -> None:
    raw = canonical_json_bytes(dict(value))
    flags = os.O_WRONLY | os.O_CREAT | (os.O_EXCL if exclusive else os.O_TRUNC)
    if exclusive:
        target = path
    else:
        target = path.with_name(f".{path.name}.{secrets.token_hex(8)}.tmp")
        flags |= os.O_EXCL
    descriptor: int | None = None
    try:
        descriptor = os.open(target, flags, 0o600)
        with os.fdopen(descriptor, "wb", closefd=True) as stream:
            descriptor = None
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        if not exclusive:
            os.replace(target, path)
        if os.name != "nt":
            path.chmod(0o600)
    except FileExistsError as exc:
        raise RuntimeStateError("AEXRT003", "a repository session is already active") from exc
    except OSError as exc:
        raise RuntimeStateError("AEXRT004", f"cannot persist runtime state: {exc}") from exc
    finally:
        if descriptor is not None:
            os.close(descriptor)
        if not exclusive and target.exists():
            try:
                target.unlink()
            except OSError:
                pass


class RuntimeStateStore:
    """One external state store with one active writer per repository."""

    def __init__(self, runtime_root: Path, target_repository: Path) -> None:
        target = target_repository.resolve(strict=True)
        candidate = runtime_root.resolve(strict=False)
        try:
            candidate.relative_to(target)
            overlaps = True
        except ValueError:
            try:
                target.relative_to(candidate)
                overlaps = True
            except ValueError:
                overlaps = False
        if overlaps:
            raise RuntimeStateError(
                "AEXRT005", "runtime directory must be external to the target repository"
            )
        _secure_directory(candidate)
        resolved = candidate.resolve(strict=True)
        if resolved != candidate:
            raise RuntimeStateError("AEXRT005", "runtime directory has an aliased identity")
        self.root = resolved
        self.target = target
        self._mutex = threading.RLock()

    def _repository_directory(self, repository_id: str) -> Path:
        identifier = _require(_REPOSITORY_ID, repository_id, "repository ID")
        path = self.root / "repositories" / identifier
        _secure_directory(path)
        return path

    @staticmethod
    def _session_path(path: Path) -> Path:
        return path / "session.json"

    @staticmethod
    def _recovery_path(path: Path) -> Path:
        return path / "recovery.json"

    @staticmethod
    def _ledger_path(path: Path) -> Path:
        return path / "nonces.json"

    @staticmethod
    def _revocation_path(path: Path) -> Path:
        return path / "revocations.json"

    def start_session(
        self, repository_id: str, owner: str, *, started_at: str | None = None
    ) -> RuntimeSession:
        directory = self._repository_directory(repository_id)
        recovery_path = self._recovery_path(directory)
        if recovery_path.exists():
            recovery = _read_json(recovery_path)
            if recovery.get("schema") != RECOVERY_SCHEMA or recovery.get("repository_id") != repository_id:
                raise RuntimeStateError("AEXRT002", "recovery record is inconsistent")
            if recovery.get("required") is True:
                raise RuntimeStateError("AEXRT006", "repository runtime recovery is required")
        if not isinstance(owner, str) or not owner or len(owner) > 512:
            raise RuntimeStateError("AEXRT001", "session owner must be bounded non-empty text")
        timestamp = _require(_TIMESTAMP, started_at or _now(), "session timestamp")
        owner_sha256 = hashlib.sha256(owner.encode("utf-8")).hexdigest()
        session = RuntimeSession(repository_id, secrets.token_hex(16), owner_sha256)
        _atomic_write(
            self._session_path(directory),
            {
                "schema": SESSION_SCHEMA,
                "repository_id": repository_id,
                "session_id": session.session_id,
                "owner_sha256": owner_sha256,
                "started_at": timestamp,
            },
            exclusive=True,
        )
        ledger = self._ledger_path(directory)
        if not ledger.exists():
            _atomic_write(
                ledger,
                {
                    "schema": NONCE_LEDGER_SCHEMA,
                    "repository_id": repository_id,
                    "admissions": [],
                },
            )
        return session

    def _require_session(
        self, session: RuntimeSession, *, allow_recovery: bool = False
    ) -> Path:
        directory = self._repository_directory(session.repository_id)
        value = _read_json(self._session_path(directory))
        expected = {
            "schema": SESSION_SCHEMA,
            "repository_id": session.repository_id,
            "session_id": session.session_id,
            "owner_sha256": session.owner_sha256,
        }
        if any(value.get(key) != item for key, item in expected.items()):
            raise RuntimeStateError("AEXRT007", "runtime session identity does not match")
        recovery_path = self._recovery_path(directory)
        if (
            not allow_recovery
            and recovery_path.exists()
            and _read_json(recovery_path).get("required") is True
        ):
            raise RuntimeStateError("AEXRT006", "repository runtime recovery is required")
        return directory

    def consume_nonce(
        self,
        session: RuntimeSession,
        *,
        nonce: str,
        envelope_sha256: str,
        repository_state_sha256: str,
        admitted_at: str | None = None,
    ) -> Mapping[str, Any]:
        """Atomically record a nonce before any caller-side effect."""

        with self._mutex:
            return self._consume_nonce(
                session,
                nonce=nonce,
                envelope_sha256=envelope_sha256,
                repository_state_sha256=repository_state_sha256,
                admitted_at=admitted_at,
            )

    def _consume_nonce(
        self,
        session: RuntimeSession,
        *,
        nonce: str,
        envelope_sha256: str,
        repository_state_sha256: str,
        admitted_at: str | None,
    ) -> Mapping[str, Any]:
        directory = self._require_session(session)
        nonce = _require(_NONCE, nonce, "nonce")
        envelope_sha256 = _require(_SHA256, envelope_sha256, "envelope digest")
        repository_state_sha256 = _require(
            _SHA256, repository_state_sha256, "repository-state digest"
        )
        timestamp = _require(_TIMESTAMP, admitted_at or _now(), "admission timestamp")
        ledger_path = self._ledger_path(directory)
        ledger = _read_json(ledger_path)
        if (
            ledger.get("schema") != NONCE_LEDGER_SCHEMA
            or ledger.get("repository_id") != session.repository_id
            or not isinstance(ledger.get("admissions"), list)
        ):
            raise RuntimeStateError("AEXRT002", "nonce ledger is inconsistent")
        admissions = list(ledger["admissions"])
        if any(isinstance(item, dict) and item.get("nonce") == nonce for item in admissions):
            raise RuntimeStateError("AEXRT008", "nonce has already been consumed")
        if len(admissions) >= MAX_NONCES:
            raise RuntimeStateError("AEXRT009", "nonce ledger reached its retention bound")
        record = {
            "nonce": nonce,
            "envelope_sha256": envelope_sha256,
            "repository_state_sha256": repository_state_sha256,
            "admitted_at": timestamp,
            "session_id": session.session_id,
        }
        admissions.append(record)
        admissions.sort(key=lambda item: item["nonce"].encode("utf-8"))
        _atomic_write(
            ledger_path,
            {
                "schema": NONCE_LEDGER_SCHEMA,
                "repository_id": session.repository_id,
                "admissions": admissions,
            },
        )
        return record

    def record_terminal(
        self,
        session: RuntimeSession,
        *,
        nonce: str,
        outcome: str,
        receipt_sha256: str | None = None,
        recorded_at: str | None = None,
    ) -> Mapping[str, Any]:
        """Record the terminal disposition of one previously consumed nonce."""

        directory = self._require_session(
            session, allow_recovery=outcome == "recovery-required"
        )
        nonce = _require(_NONCE, nonce, "nonce")
        if outcome not in {"completed", "failed-consumed", "recovery-required"}:
            raise RuntimeStateError("AEXRT001", "terminal outcome is unsupported")
        if receipt_sha256 is not None:
            receipt_sha256 = _require(_SHA256, receipt_sha256, "receipt digest")
        ledger_path = self._ledger_path(directory)
        ledger = _read_json(ledger_path)
        admissions = ledger.get("admissions")
        if not isinstance(admissions, list):
            raise RuntimeStateError("AEXRT002", "nonce ledger is inconsistent")
        matches = [
            item
            for item in admissions
            if isinstance(item, dict)
            and item.get("nonce") == nonce
            and item.get("session_id") == session.session_id
        ]
        if len(matches) != 1:
            raise RuntimeStateError("AEXRT010", "nonce is not admitted in this session")
        record = matches[0]
        if "terminal" in record:
            raise RuntimeStateError("AEXRT010", "nonce already has a terminal outcome")
        terminal = {
            "outcome": outcome,
            "receipt_sha256": receipt_sha256,
            "recorded_at": _require(
                _TIMESTAMP, recorded_at or _now(), "terminal timestamp"
            ),
        }
        record["terminal"] = terminal
        _atomic_write(ledger_path, ledger)
        return terminal

    def revoke_delegation(
        self,
        session: RuntimeSession,
        delegation_sha256: str,
        *,
        revoked_at: str | None = None,
    ) -> None:
        """Persist a session-independent digest revocation."""

        directory = self._require_session(session)
        delegation_sha256 = _require(
            _SHA256, delegation_sha256, "delegation digest"
        )
        path = self._revocation_path(directory)
        if path.exists():
            value = _read_json(path)
        else:
            value = {
                "schema": REVOCATION_SCHEMA,
                "repository_id": session.repository_id,
                "revocations": [],
            }
        if (
            value.get("schema") != REVOCATION_SCHEMA
            or value.get("repository_id") != session.repository_id
            or not isinstance(value.get("revocations"), list)
        ):
            raise RuntimeStateError("AEXRT002", "revocation state is inconsistent")
        if not any(
            isinstance(item, dict)
            and item.get("delegation_sha256") == delegation_sha256
            for item in value["revocations"]
        ):
            value["revocations"].append(
                {
                    "delegation_sha256": delegation_sha256,
                    "revoked_at": _require(
                        _TIMESTAMP, revoked_at or _now(), "revocation timestamp"
                    ),
                }
            )
            value["revocations"].sort(
                key=lambda item: item["delegation_sha256"].encode("utf-8")
            )
            _atomic_write(path, value)

    def is_revoked(self, repository_id: str, delegation_sha256: str) -> bool:
        directory = self._repository_directory(repository_id)
        delegation_sha256 = _require(
            _SHA256, delegation_sha256, "delegation digest"
        )
        path = self._revocation_path(directory)
        if not path.exists():
            return False
        value = _read_json(path)
        if (
            value.get("schema") != REVOCATION_SCHEMA
            or value.get("repository_id") != repository_id
            or not isinstance(value.get("revocations"), list)
        ):
            raise RuntimeStateError("AEXRT002", "revocation state is inconsistent")
        return any(
            isinstance(item, dict)
            and item.get("delegation_sha256") == delegation_sha256
            for item in value["revocations"]
        )

    def mark_recovery_required(
        self, session: RuntimeSession, reason: str, *, recorded_at: str | None = None
    ) -> None:
        directory = self._require_session(session)
        if not isinstance(reason, str) or not reason or len(reason) > 512:
            raise RuntimeStateError("AEXRT001", "recovery reason must be bounded non-empty text")
        _atomic_write(
            self._recovery_path(directory),
            {
                "schema": RECOVERY_SCHEMA,
                "repository_id": session.repository_id,
                "required": True,
                "session_id": session.session_id,
                "reason_sha256": hashlib.sha256(reason.encode("utf-8")).hexdigest(),
                "recorded_at": _require(
                    _TIMESTAMP, recorded_at or _now(), "recovery timestamp"
                ),
            },
        )

    def acknowledge_recovery(
        self, repository_id: str, *, acknowledged_at: str | None = None
    ) -> None:
        directory = self._repository_directory(repository_id)
        recovery_path = self._recovery_path(directory)
        recovery = _read_json(recovery_path)
        if recovery.get("schema") != RECOVERY_SCHEMA or recovery.get("required") is not True:
            raise RuntimeStateError("AEXRT002", "no valid required-recovery record exists")
        _atomic_write(
            recovery_path,
            {
                **recovery,
                "required": False,
                "acknowledged_at": _require(
                    _TIMESTAMP, acknowledged_at or _now(), "recovery acknowledgement"
                ),
            },
        )

    def close_session(self, session: RuntimeSession) -> None:
        directory = self._require_session(session, allow_recovery=True)
        try:
            self._session_path(directory).unlink()
        except OSError as exc:
            raise RuntimeStateError("AEXRT004", f"cannot close runtime session: {exc}") from exc


__all__ = [
    "RuntimeSession",
    "RuntimeStateError",
    "RuntimeStateStore",
]
