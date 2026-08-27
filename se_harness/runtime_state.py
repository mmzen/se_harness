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
import stat
import threading
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, BinaryIO, Iterator, Mapping

from se_harness.agent_contract import AgentContractError, canonical_json_bytes


RUNTIME_STATE_SCHEMA = "se-harness-agentic-runtime-state-v1"
SESSION_SCHEMA = "se-harness-agentic-session-v1"
NONCE_LEDGER_SCHEMA = "se-harness-agentic-nonce-ledger-v1"
RECOVERY_SCHEMA = "se-harness-agentic-recovery-v1"
REVOCATION_SCHEMA = "se-harness-agentic-revocations-v1"
EFFECT_JOURNAL_SCHEMA = "se-harness-effect-journal-v1"
MAX_NONCES = 1_024
MAX_RUNTIME_STATE_BYTES = 1_048_576
MAX_EFFECT_JOURNAL_BYTES = 4_194_304
_SHA256 = re.compile(r"[0-9a-f]{64}")
_NONCE = re.compile(r"[0-9a-f]{32,128}")
_REPOSITORY_ID = re.compile(r"[0-9a-f]{64}")
_TIMESTAMP = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")
_TRANSACTION_ID = re.compile(r"[0-9a-f]{32}")


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


def _read_json(
    path: Path, *, maximum_bytes: int = MAX_RUNTIME_STATE_BYTES
) -> dict[str, Any]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise RuntimeStateError("AEXRT002", f"cannot read runtime state: {exc}") from exc
    if len(raw) > maximum_bytes:
        raise RuntimeStateError("AEXRT002", "runtime state exceeds its byte bound")
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise RuntimeStateError("AEXRT002", "runtime state is not valid UTF-8 JSON") from exc
    try:
        canonical = canonical_json_bytes(value, maximum_bytes=maximum_bytes)
    except AgentContractError as exc:
        raise RuntimeStateError(
            "AEXRT002", "runtime state violates canonical JSON bounds"
        ) from exc
    if not isinstance(value, dict) or canonical != raw:
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


def _atomic_write(
    path: Path,
    value: Mapping[str, Any],
    *,
    exclusive: bool = False,
    maximum_bytes: int = MAX_RUNTIME_STATE_BYTES,
) -> None:
    try:
        raw = canonical_json_bytes(dict(value), maximum_bytes=maximum_bytes)
    except AgentContractError as exc:
        raise RuntimeStateError(
            "AEXRT002", "runtime state violates canonical JSON bounds"
        ) from exc
    if len(raw) > maximum_bytes:
        raise RuntimeStateError("AEXRT002", "runtime state exceeds its byte bound")
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


def _acquire_os_lock(path: Path, code: str, message: str) -> BinaryIO:
    """Acquire a nonblocking OS lock that is released automatically on process exit."""

    try:
        stream = path.open("a+b")
        stream.seek(0, os.SEEK_END)
        if stream.tell() == 0:
            stream.write(b"\0")
            stream.flush()
            os.fsync(stream.fileno())
        stream.seek(0)
        if os.name == "nt":
            import msvcrt

            msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl

            fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        return stream
    except (OSError, ImportError) as exc:
        if "stream" in locals():
            stream.close()
        raise RuntimeStateError(code, message) from exc


def _release_os_lock(stream: BinaryIO) -> None:
    try:
        stream.seek(0)
        if os.name == "nt":
            import msvcrt

            msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            fcntl.flock(stream.fileno(), fcntl.LOCK_UN)
    finally:
        stream.close()


class RuntimeStateStore:
    """One external state store with one active writer per repository."""

    def __init__(self, runtime_root: Path, target_repository: Path) -> None:
        supplied_target = target_repository.absolute()
        try:
            target_metadata = supplied_target.lstat()
        except OSError as exc:
            raise RuntimeStateError("AEXRT005", f"target repository is unavailable: {exc}") from exc
        target_attributes = getattr(target_metadata, "st_file_attributes", 0)
        target_reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
        if (
            stat.S_ISLNK(target_metadata.st_mode)
            or (target_reparse and target_attributes & target_reparse)
            or not stat.S_ISDIR(target_metadata.st_mode)
        ):
            raise RuntimeStateError("AEXRT005", "target repository root is aliased")
        target = supplied_target.resolve(strict=True)
        candidate = runtime_root.absolute()
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
        self._session_locks: dict[str, BinaryIO] = {}

    def _repository_directory(self, repository_id: str) -> Path:
        identifier = _require(_REPOSITORY_ID, repository_id, "repository ID")
        path = self.root / "repositories" / identifier
        _secure_directory(path)
        return path

    @staticmethod
    def _session_path(path: Path) -> Path:
        return path / "session.json"

    @staticmethod
    def _session_lock_path(path: Path) -> Path:
        return path / "session.lock"

    @staticmethod
    def _recovery_path(path: Path) -> Path:
        return path / "recovery.json"

    @staticmethod
    def _ledger_path(path: Path) -> Path:
        return path / "nonces.json"

    @staticmethod
    def _revocation_path(path: Path) -> Path:
        return path / "revocations.json"

    @staticmethod
    def _effect_journal_path(path: Path) -> Path:
        return path / "effect-journal.json"

    @staticmethod
    def _effect_lock_path(path: Path) -> Path:
        return path / "effect.lock"

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
        lock = _acquire_os_lock(
            self._session_lock_path(directory),
            "AEXRT003",
            "a repository session is already active",
        )
        try:
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
        except Exception:
            _release_os_lock(lock)
            raise
        self._session_locks[session.session_id] = lock
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

    def resume_session(self, repository_id: str, owner: str) -> RuntimeSession:
        """Reacquire an interrupted session only when an active journal proves recovery."""

        directory = self._repository_directory(repository_id)
        if not isinstance(owner, str) or not owner or len(owner) > 512:
            raise RuntimeStateError("AEXRT001", "session owner must be bounded non-empty text")
        value = _read_json(self._session_path(directory))
        journal = self.read_effect_journal(repository_id)
        if journal is None:
            raise RuntimeStateError(
                "AEXRT015", "no active journal authorizes interrupted-session recovery"
            )
        owner_sha256 = hashlib.sha256(owner.encode("utf-8")).hexdigest()
        if (
            value.get("schema") != SESSION_SCHEMA
            or value.get("repository_id") != repository_id
            or value.get("owner_sha256") != owner_sha256
            or not isinstance(value.get("session_id"), str)
        ):
            raise RuntimeStateError("AEXRT007", "interrupted session identity does not match")
        session = RuntimeSession(repository_id, value["session_id"], owner_sha256)
        lock = _acquire_os_lock(
            self._session_lock_path(directory),
            "AEXRT003",
            "the interrupted repository session is still active",
        )
        self._session_locks[session.session_id] = lock
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
        if session.session_id not in self._session_locks:
            raise RuntimeStateError("AEXRT007", "runtime session OS lock is not held")
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
        allow_recovery: bool = False,
    ) -> Mapping[str, Any]:
        """Record the terminal disposition of one previously consumed nonce."""

        directory = self._require_session(
            session,
            allow_recovery=allow_recovery or outcome == "recovery-required",
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

    def record_terminal_by_nonce_sha256(
        self,
        session: RuntimeSession,
        *,
        nonce_sha256: str,
        outcome: str,
        receipt_sha256: str | None = None,
        recorded_at: str | None = None,
    ) -> Mapping[str, Any]:
        """Finalize a consumed nonce during journal-driven restart recovery."""

        digest = _require(_SHA256, nonce_sha256, "nonce digest")
        directory = self._require_session(session, allow_recovery=True)
        ledger = _read_json(self._ledger_path(directory))
        admissions = ledger.get("admissions")
        if not isinstance(admissions, list):
            raise RuntimeStateError("AEXRT002", "nonce ledger is inconsistent")
        matches = [
            item
            for item in admissions
            if isinstance(item, dict)
            and item.get("session_id") == session.session_id
            and isinstance(item.get("nonce"), str)
            and hashlib.sha256(item["nonce"].encode("ascii")).hexdigest() == digest
        ]
        if len(matches) != 1:
            raise RuntimeStateError("AEXRT010", "nonce digest is not admitted in this session")
        record = matches[0]
        if "terminal" in record:
            return record["terminal"]
        nonce = record["nonce"]
        return self.record_terminal(
            session,
            nonce=nonce,
            outcome=outcome,
            receipt_sha256=receipt_sha256,
            recorded_at=recorded_at,
            allow_recovery=True,
        )

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

    @contextmanager
    def effect_lock(self, session: RuntimeSession) -> Iterator[None]:
        """Acquire the cross-process, single-effect lock for one live session."""

        directory = self._require_session(session, allow_recovery=True)
        lock_path = self._effect_lock_path(directory)
        lock: BinaryIO | None = None
        try:
            lock = _acquire_os_lock(
                lock_path, "AEXRT011", "another target effect is active"
            )
            yield
        finally:
            if lock is not None:
                _release_os_lock(lock)

    def effect_material_directory(
        self, session: RuntimeSession, transaction_id: str
    ) -> Path:
        """Return one external, transaction-scoped recovery-material directory."""

        directory = self._require_session(session, allow_recovery=True)
        transaction = _require(_TRANSACTION_ID, transaction_id, "transaction ID")
        material = directory / "transactions" / transaction
        _secure_directory(material)
        return material

    def read_effect_journal(
        self, repository_id: str
    ) -> Mapping[str, Any] | None:
        """Read the active journal, if any, without inferring recovery."""

        directory = self._repository_directory(repository_id)
        path = self._effect_journal_path(directory)
        if not path.exists():
            return None
        value = _read_json(path, maximum_bytes=MAX_EFFECT_JOURNAL_BYTES)
        if (
            value.get("schema") != EFFECT_JOURNAL_SCHEMA
            or value.get("repository_id") != repository_id
        ):
            raise RuntimeStateError("AEXRT012", "effect journal is inconsistent")
        return value

    def begin_effect_transaction(
        self, session: RuntimeSession, journal: Mapping[str, Any]
    ) -> None:
        """Persist one exclusive durable journal before target-path mutation."""

        directory = self._require_session(session)
        value = dict(journal)
        if (
            value.get("schema") != EFFECT_JOURNAL_SCHEMA
            or value.get("repository_id") != session.repository_id
            or value.get("session_id") != session.session_id
            or _TRANSACTION_ID.fullmatch(str(value.get("transaction_id"))) is None
        ):
            raise RuntimeStateError("AEXRT012", "new effect journal identity is inconsistent")
        path = self._effect_journal_path(directory)
        if path.exists():
            raise RuntimeStateError("AEXRT013", "an effect journal already exists")
        _atomic_write(
            path,
            value,
            exclusive=True,
            maximum_bytes=MAX_EFFECT_JOURNAL_BYTES,
        )

    def update_effect_transaction(
        self,
        session: RuntimeSession,
        transaction_id: str,
        journal: Mapping[str, Any],
    ) -> None:
        """Atomically advance the exact active journal."""

        directory = self._require_session(session, allow_recovery=True)
        transaction = _require(_TRANSACTION_ID, transaction_id, "transaction ID")
        path = self._effect_journal_path(directory)
        current = _read_json(path, maximum_bytes=MAX_EFFECT_JOURNAL_BYTES)
        value = dict(journal)
        identity = {
            "schema": EFFECT_JOURNAL_SCHEMA,
            "repository_id": session.repository_id,
            "session_id": session.session_id,
            "transaction_id": transaction,
        }
        if any(current.get(key) != expected for key, expected in identity.items()):
            raise RuntimeStateError("AEXRT012", "active effect journal identity differs")
        if any(value.get(key) != expected for key, expected in identity.items()):
            raise RuntimeStateError("AEXRT012", "updated effect journal identity differs")
        _atomic_write(path, value, maximum_bytes=MAX_EFFECT_JOURNAL_BYTES)

    def archive_effect_transaction(
        self, session: RuntimeSession, transaction_id: str
    ) -> Path:
        """Move one terminal active journal into its immutable transaction record."""

        directory = self._require_session(session, allow_recovery=True)
        transaction = _require(_TRANSACTION_ID, transaction_id, "transaction ID")
        active = self._effect_journal_path(directory)
        journal = _read_json(active, maximum_bytes=MAX_EFFECT_JOURNAL_BYTES)
        if (
            journal.get("transaction_id") != transaction
            or journal.get("state")
            not in {
                "committed",
                "rolled-back",
                "recovered-prior",
                "recovered-result",
                "human-recovery-stop",
            }
        ):
            raise RuntimeStateError("AEXRT014", "only a terminal effect journal can be archived")
        material = self.effect_material_directory(session, transaction)
        destination = material / "journal.json"
        if destination.exists():
            raise RuntimeStateError("AEXRT014", "terminal journal archive already exists")
        try:
            os.replace(active, destination)
        except OSError as exc:
            raise RuntimeStateError("AEXRT004", f"cannot archive effect journal: {exc}") from exc
        return destination

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
        lock = self._session_locks.pop(session.session_id)
        _release_os_lock(lock)


__all__ = [
    "RuntimeSession",
    "RuntimeStateError",
    "RuntimeStateStore",
    "EFFECT_JOURNAL_SCHEMA",
]
