"""Single-writer transactional application of admitted change bundles."""

from __future__ import annotations

import hashlib
import os
import secrets
import stat
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping

from se_harness.agent_contract import (
    AgentContractError,
    AUTONOMY_ENVELOPE_V2_SCHEMA,
    ContractDocument,
    canonical_json_bytes,
    canonical_sha256,
    portable_path_within,
    parse_json_bytes,
    validate_contract,
    validate_portable_path,
    validate_sha256,
)
from se_harness.change_bundle import (
    ChangeBundleError,
    parse_change_bundle_bytes,
    read_content_object,
)
from se_harness.delegated_authority import LiveAdmission, admit_fresh_envelope
from se_harness.mutation_guard import require_mutation_authority
from se_harness.repository_state import EvaluatorIdentity, observe_repository
from se_harness.runtime_state import (
    EFFECT_JOURNAL_SCHEMA,
    MAX_EFFECT_JOURNAL_BYTES,
    RuntimeSession,
    RuntimeStateError,
    RuntimeStateStore,
)


EFFECT_RECEIPT_SCHEMA = "se-harness-effect-receipt-v1"
EFFECT_OPERATION = "change-bundle-apply"
_REPARSE = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
_TERMINAL = {
    "committed", "rolled-back", "recovered-prior", "recovered-result",
    "human-recovery-stop",
}
_DEFAULT_DENIED = (
    ".git/",
    ".engineering-harness.lock",
    ".engineering-harness.toml",
    ".github/workflows/engineering-harness.yml",
    "ENGINEERING_HARNESS.md",
    "docs/engineering/DECISION_RIGHTS.md",
    "docs/engineering/QUALITY_GATES.json",
    "docs/engineering/QUALITY_GATES.md",
    "docs/engineering/TRACEABILITY.md",
    "docs/engineering/WORKFLOW.json",
    "docs/engineering/WORKFLOW.md",
    "docs/engineering/templates/",
    "scripts/artifact_layout_registry.py",
    "scripts/check_engineering_harness.ps1",
    "scripts/check_engineering_harness.sh",
    "scripts/generate_harness_dashboard.py",
    "scripts/harness_explorer/",
    "scripts/inspect_engineering_artifacts.py",
    "scripts/select_harness_work_order.py",
    "scripts/validate_engineering_artifacts.py",
)


class EffectBrokerError(RuntimeError):
    """A stable, bounded broker, rollback, or recovery diagnostic."""

    def __init__(self, code: str, message: str, *, uncertain_paths: Iterable[str] = ()) -> None:
        safe = "".join(character if character >= " " else "?" for character in str(message))[:512]
        super().__init__(f"{code}: {safe or 'effect broker stopped'}")
        self.code = code
        self.message = safe
        self.uncertain_paths = tuple(sorted(set(uncertain_paths)))


@dataclass(frozen=True)
class EffectReceipt:
    value: Mapping[str, Any]
    canonical_bytes: bytes
    sha256: str


@dataclass(frozen=True)
class EffectResult:
    outcome: str
    receipt: EffectReceipt
    bundle_sha256: str
    transaction_id: str
    journal_path: Path


@dataclass(frozen=True)
class RecoveryResult:
    outcome: str
    transaction_id: str
    journal_path: Path | None
    uncertain_paths: tuple[str, ...] = ()
    receipt: EffectReceipt | None = None


def _now() -> datetime:
    return datetime.now(UTC)


def _timestamp(value: datetime) -> str:
    if not isinstance(value, datetime) or value.tzinfo is None:
        raise EffectBrokerError("AEXEFF001", "broker time must be timezone-aware")
    return value.astimezone(UTC).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def _normal_directory(path: Path, label: str) -> None:
    try:
        metadata = path.lstat()
    except OSError as exc:
        raise EffectBrokerError("AEXEFF006", f"cannot inspect {label}: {exc}") from exc
    attributes = getattr(metadata, "st_file_attributes", 0)
    if (
        stat.S_ISLNK(metadata.st_mode)
        or (_REPARSE and attributes & _REPARSE)
        or not stat.S_ISDIR(metadata.st_mode)
    ):
        raise EffectBrokerError("AEXEFF006", f"{label} is not a normal directory")


def _file_state(path: Path) -> dict[str, Any] | None:
    try:
        metadata = path.lstat()
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise EffectBrokerError("AEXEFF006", f"cannot inspect target path: {exc}") from exc
    attributes = getattr(metadata, "st_file_attributes", 0)
    if stat.S_ISLNK(metadata.st_mode) or (_REPARSE and attributes & _REPARSE):
        raise EffectBrokerError("AEXEFF006", "link or reparse target is prohibited")
    if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
        raise EffectBrokerError("AEXEFF006", "only unaliased regular target files are supported")
    digest = hashlib.sha256()
    descriptor: int | None = None
    try:
        flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(path, flags)
        opened = os.fstat(descriptor)
        if (
            opened.st_dev,
            opened.st_ino,
            opened.st_mode,
            opened.st_nlink,
            opened.st_size,
        ) != (
            metadata.st_dev,
            metadata.st_ino,
            metadata.st_mode,
            metadata.st_nlink,
            metadata.st_size,
        ):
            raise EffectBrokerError("AEXEFF007", "target changed before it was opened")
        with os.fdopen(descriptor, "rb", closefd=True) as stream:
            descriptor = None
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
        after = path.lstat()
    except EffectBrokerError:
        raise
    except OSError as exc:
        raise EffectBrokerError("AEXEFF006", f"cannot read target path: {exc}") from exc
    finally:
        if descriptor is not None:
            os.close(descriptor)
    if (metadata.st_dev, metadata.st_size, metadata.st_mtime_ns, metadata.st_ino) != (
        after.st_dev, after.st_size, after.st_mtime_ns, after.st_ino
    ):
        raise EffectBrokerError("AEXEFF007", "target changed while it was observed")
    return {"sha256": digest.hexdigest(), "size": metadata.st_size}


def _matches(actual: Mapping[str, Any] | None, expected: Mapping[str, Any] | None) -> bool:
    if actual is None or expected is None:
        return actual is expected
    return (
        actual.get("sha256") == expected.get("sha256")
        and actual.get("size") == expected.get("size")
    )


def _target(root: Path, relative: str, *, allow_missing: bool) -> tuple[Path, tuple[str, ...]]:
    portable = validate_portable_path(relative)
    candidate = root.joinpath(*portable.split("/"))
    current = root
    missing: list[str] = []
    for component in portable.split("/")[:-1]:
        current = current / component
        if current.exists():
            _normal_directory(current, component)
        elif allow_missing:
            missing.append(current.relative_to(root).as_posix())
        else:
            raise EffectBrokerError("AEXEFF006", f"target parent is absent: {component}")
    try:
        candidate.absolute().relative_to(root.absolute())
    except ValueError as exc:
        raise EffectBrokerError("AEXEFF005", "target path escapes the repository") from exc
    return candidate, tuple(missing)


def _snapshot(root: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for current, directories, files in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        if current_path == root:
            directories[:] = [item for item in directories if item != ".git"]
        for name in tuple(directories):
            _normal_directory(current_path / name, name)
        for name in files:
            path = current_path / name
            relative = validate_portable_path(path.relative_to(root).as_posix())
            state = _file_state(path)
            assert state is not None
            entries.append({"path": relative, **state})
    entries.sort(key=lambda item: item["path"].encode("utf-8"))
    folded: dict[str, str] = {}
    for item in entries:
        prior = folded.get(item["path"].casefold())
        if prior is not None and prior != item["path"]:
            raise EffectBrokerError("AEXEFF005", "repository has a case-folded path collision")
        folded[item["path"].casefold()] = item["path"]
    return entries


def _manifest_sha256(entries: Iterable[Mapping[str, Any]]) -> str:
    return canonical_sha256([dict(item) for item in entries])


def _expected_manifest(
    prior: Iterable[Mapping[str, Any]], changes: Iterable[Mapping[str, Any]]
) -> list[dict[str, Any]]:
    expected = {item["path"]: dict(item) for item in prior}
    for entry in changes:
        if entry["after"] is None:
            expected.pop(entry["path"], None)
        else:
            expected[entry["path"]] = {
                "path": entry["path"],
                "sha256": entry["after"]["sha256"],
                "size": entry["after"]["size"],
            }
    return sorted(expected.values(), key=lambda item: item["path"].encode("utf-8"))


def _write_object(directory: Path, content: bytes, digest: str) -> Path:
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    _normal_directory(directory, "recovery object directory")
    target = directory / validate_sha256(digest)
    if target.exists():
        if _file_state(target) != {"sha256": digest, "size": len(content)}:
            raise EffectBrokerError("AEXEFF008", "recovery object is inconsistent")
        return target
    descriptor: int | None = None
    try:
        descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o400)
        with os.fdopen(descriptor, "wb", closefd=True) as stream:
            descriptor = None
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        if os.name != "nt":
            target.chmod(0o400)
    except OSError as exc:
        if descriptor is not None:
            os.close(descriptor)
        target.unlink(missing_ok=True)
        raise EffectBrokerError("AEXEFF008", f"cannot persist recovery object: {exc}") from exc
    return target


def _write_receipt(path: Path, content: bytes) -> None:
    descriptor: int | None = None
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o400)
        with os.fdopen(descriptor, "wb", closefd=True) as stream:
            descriptor = None
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        if os.name != "nt":
            path.chmod(0o400)
    except OSError as exc:
        if descriptor is not None:
            os.close(descriptor)
        path.unlink(missing_ok=True)
        raise EffectBrokerError("AEXEFF015", f"cannot retain effect receipt: {exc}") from exc


def _read_exact(path: Path, expected: Mapping[str, Any], label: str) -> bytes:
    if not _matches(_file_state(path), expected):
        raise EffectBrokerError("AEXEFF008", f"{label} digest or size differs")
    try:
        return path.read_bytes()
    except OSError as exc:
        raise EffectBrokerError("AEXEFF008", f"cannot read {label}: {exc}") from exc


def _atomic_materialize(path: Path, content: bytes, transaction_id: str) -> None:
    temporary = path.with_name(f".se-harness-{transaction_id}-restore.tmp")
    descriptor: int | None = None
    try:
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "wb", closefd=True) as stream:
            descriptor = None
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except OSError as exc:
        raise EffectBrokerError("AEXEFF012", f"cannot restore prior target bytes: {exc}") from exc
    finally:
        if descriptor is not None:
            os.close(descriptor)
        temporary.unlink(missing_ok=True)


def _validate_journal(value: Mapping[str, Any], session: RuntimeSession) -> dict[str, Any]:
    fields = {
        "schema", "repository_id", "session_id", "transaction_id", "state",
        "bundle_sha256", "envelope_sha256", "nonce_sha256", "work_order",
        "state_before", "state_after", "previous_receipt_sha256", "entries",
        "prior_manifest_sha256", "expected_manifest_sha256", "plan_sha256",
        "created_parents", "temporaries", "applied", "receipt_sha256",
        "uncertain_paths", "started_at",
    }
    if not isinstance(value, dict) or set(value) != fields:
        raise EffectBrokerError("AEXEFF014", "effect journal field set is corrupt")
    if (
        value["schema"] != EFFECT_JOURNAL_SCHEMA
        or value["repository_id"] != session.repository_id
        or value["session_id"] != session.session_id
        or not isinstance(value["transaction_id"], str)
        or len(value["transaction_id"]) != 32
    ):
        raise EffectBrokerError("AEXEFF014", "effect journal identity is corrupt")
    try:
        int(value["transaction_id"], 16)
        for key in (
            "bundle_sha256", "envelope_sha256", "nonce_sha256", "state_before",
            "prior_manifest_sha256", "expected_manifest_sha256", "plan_sha256",
        ):
            validate_sha256(value[key])
        for key in ("state_after", "previous_receipt_sha256", "receipt_sha256"):
            if value[key] is not None:
                validate_sha256(value[key])
        datetime.strptime(value["started_at"], "%Y-%m-%dT%H:%M:%SZ")
    except (TypeError, ValueError) as exc:
        raise EffectBrokerError("AEXEFF014", "effect journal scalar identity is corrupt") from exc
    if value["state"] not in {
        "prepared", "applying", "result-observed", *_TERMINAL
    }:
        raise EffectBrokerError("AEXEFF014", "effect journal state is corrupt")
    entries: list[dict[str, Any]] = []
    for item in value["entries"]:
        if not isinstance(item, dict) or set(item) != {"operation", "path", "before", "after"}:
            raise EffectBrokerError("AEXEFF014", "effect journal entry is corrupt")
        path = validate_portable_path(item["path"])
        if item["operation"] not in {"create", "replace", "delete"}:
            raise EffectBrokerError("AEXEFF014", "effect journal operation is corrupt")
        before, after = item["before"], item["after"]
        for selected in (before, after):
            if selected is not None:
                if not isinstance(selected, dict) or set(selected) != {"sha256", "size"}:
                    raise EffectBrokerError("AEXEFF014", "effect journal content state is corrupt")
                validate_sha256(selected["sha256"])
                if (
                    isinstance(selected["size"], bool)
                    or not isinstance(selected["size"], int)
                    or selected["size"] < 0
                ):
                    raise EffectBrokerError("AEXEFF014", "effect journal content size is corrupt")
        if (
            item["operation"] == "create" and (before is not None or after is None)
        ) or (
            item["operation"] == "replace" and (before is None or after is None)
        ) or (
            item["operation"] == "delete" and (before is None or after is not None)
        ):
            raise EffectBrokerError("AEXEFF014", "effect journal operation invariant is corrupt")
        entries.append({"operation": item["operation"], "path": path, "before": before, "after": after})
    if entries != sorted(entries, key=lambda item: item["path"].encode("utf-8")):
        raise EffectBrokerError("AEXEFF014", "effect journal entries are not path ordered")
    parents = [validate_portable_path(item) for item in value["created_parents"]]
    temporaries = [validate_portable_path(item) for item in value["temporaries"]]
    paths = {item["path"] for item in entries}
    applied = [validate_portable_path(item) for item in value["applied"]]
    uncertain = [validate_portable_path(item) for item in value["uncertain_paths"]]
    if (
        len(paths) != len(entries)
        or not set(applied).issubset(paths)
        or len(applied) != len(set(applied))
        or len(parents) != len(set(parents))
        or len(temporaries) != len(set(temporaries))
        or len(uncertain) != len(set(uncertain))
    ):
        raise EffectBrokerError("AEXEFF014", "effect journal path coverage is corrupt")
    plan = {
        "bundle_sha256": value["bundle_sha256"],
        "envelope_sha256": value["envelope_sha256"],
        "entries": entries,
        "prior_manifest_sha256": value["prior_manifest_sha256"],
        "expected_manifest_sha256": value["expected_manifest_sha256"],
        "created_parents": parents,
        "temporaries": temporaries,
    }
    if (
        canonical_sha256(plan, maximum_bytes=MAX_EFFECT_JOURNAL_BYTES)
        != value["plan_sha256"]
    ):
        raise EffectBrokerError("AEXEFF014", "effect journal recovery checksum differs")
    return dict(value)


def _advance(
    store: RuntimeStateStore,
    session: RuntimeSession,
    journal: dict[str, Any],
    state: str | None = None,
) -> None:
    if state is not None:
        journal["state"] = state
    store.update_effect_transaction(session, journal["transaction_id"], journal)


def _human_stop(
    store: RuntimeStateStore,
    session: RuntimeSession,
    journal: dict[str, Any],
    paths: Iterable[str],
    reason: str,
) -> None:
    journal["state"] = "human-recovery-stop"
    journal["uncertain_paths"] = sorted(set(paths), key=lambda item: item.encode("utf-8"))
    _advance(store, session, journal)
    store.mark_recovery_required(session, reason)


def _rollback_prior(
    root: Path,
    store: RuntimeStateStore,
    session: RuntimeSession,
    journal: dict[str, Any],
    *,
    recovered: bool,
) -> Path:
    material = store.effect_material_directory(session, journal["transaction_id"])
    uncertain: list[str] = []
    try:
        for entry in reversed(journal["entries"]):
            target, _ = _target(root, entry["path"], allow_missing=True)
            actual = _file_state(target)
            before, after = entry["before"], entry["after"]
            if _matches(actual, before):
                continue
            if not _matches(actual, after):
                uncertain.append(entry["path"])
                continue
            if before is None:
                target.unlink()
            else:
                backup = material / "backups" / before["sha256"]
                _atomic_materialize(
                    target,
                    _read_exact(backup, before, "recovery backup"),
                    journal["transaction_id"],
                )
        for relative in journal.get("temporaries", []):
            temporary, _ = _target(root, relative, allow_missing=True)
            if temporary.exists():
                _file_state(temporary)
                temporary.unlink()
        for relative in reversed(journal.get("created_parents", [])):
            parent = root.joinpath(*relative.split("/"))
            if parent.exists():
                parent.rmdir()
        if uncertain:
            raise EffectBrokerError(
                "AEXEFF014",
                "current target is neither the planned prior nor result state",
                uncertain_paths=uncertain,
            )
        if _manifest_sha256(_snapshot(root)) != journal["prior_manifest_sha256"]:
            raise EffectBrokerError("AEXEFF013", "rollback did not reproduce the prior manifest")
        journal["applied"] = []
        _advance(store, session, journal, "recovered-prior" if recovered else "rolled-back")
        store.record_terminal_by_nonce_sha256(
            session,
            nonce_sha256=journal["nonce_sha256"],
            outcome="failed-consumed",
        )
        return store.archive_effect_transaction(session, journal["transaction_id"])
    except Exception as exc:
        paths = uncertain or [item["path"] for item in journal.get("entries", [])]
        try:
            _human_stop(store, session, journal, paths, str(exc))
            store.record_terminal_by_nonce_sha256(
                session,
                nonce_sha256=journal["nonce_sha256"],
                outcome="recovery-required",
            )
        except Exception:
            pass
        raise EffectBrokerError(
            "AEXEFF014" if recovered else "AEXEFF013",
            f"{'recovery' if recovered else 'rollback'} could not prove prior state: {exc}",
            uncertain_paths=paths,
        ) from exc


def recover_effect_transaction(
    repository: Path,
    *,
    runtime_store: RuntimeStateStore,
    session: RuntimeSession,
) -> RecoveryResult | None:
    """Resolve an active journal to a provable terminal state or stop."""

    root = repository.resolve(strict=True)
    selected = runtime_store.read_effect_journal(session.repository_id)
    if selected is None:
        return None
    try:
        journal = _validate_journal(selected, session)
    except EffectBrokerError as exc:
        try:
            runtime_store.mark_recovery_required(session, str(exc))
        except RuntimeStateError:
            pass
        raise
    transaction_id = str(journal.get("transaction_id", ""))
    state = journal.get("state")
    if state == "human-recovery-stop":
        raise EffectBrokerError(
            "AEXEFF014",
            "journal requires accountable human recovery",
            uncertain_paths=journal.get("uncertain_paths", ()),
        )
    if state == "committed":
        if _manifest_sha256(_snapshot(root)) != journal.get("expected_manifest_sha256"):
            paths = [item["path"] for item in journal.get("entries", [])]
            _human_stop(runtime_store, session, journal, paths, "committed result differs")
            raise EffectBrokerError(
                "AEXEFF014", "committed journal differs from live target", uncertain_paths=paths
            )
        material = runtime_store.effect_material_directory(session, transaction_id)
        receipt_path = material / "receipt.json"
        try:
            receipt = parse_effect_receipt_bytes(receipt_path.read_bytes())
        except (OSError, EffectBrokerError) as exc:
            _human_stop(
                runtime_store,
                session,
                journal,
                [item["path"] for item in journal.get("entries", [])],
                "committed receipt is missing or corrupt",
            )
            raise EffectBrokerError(
                "AEXEFF014", f"committed receipt cannot be recovered: {exc}"
            ) from exc
        if receipt.sha256 != journal.get("receipt_sha256"):
            _human_stop(
                runtime_store,
                session,
                journal,
                [item["path"] for item in journal.get("entries", [])],
                "committed receipt digest differs",
            )
            raise EffectBrokerError("AEXEFF014", "committed receipt digest differs")
        runtime_store.record_terminal_by_nonce_sha256(
            session,
            nonce_sha256=journal["nonce_sha256"],
            outcome="completed",
            receipt_sha256=journal.get("receipt_sha256"),
        )
        path = runtime_store.archive_effect_transaction(session, transaction_id)
        try:
            runtime_store.acknowledge_recovery(session.repository_id)
        except RuntimeStateError:
            pass
        return RecoveryResult("recovered-result", transaction_id, path, receipt=receipt)
    if state in _TERMINAL:
        path = runtime_store.archive_effect_transaction(session, transaction_id)
        return RecoveryResult(str(state), transaction_id, path)
    if state not in {"prepared", "applying", "result-observed"}:
        paths = [item.get("path", "") for item in journal.get("entries", []) if item.get("path")]
        _human_stop(runtime_store, session, journal, paths, "unknown effect journal state")
        raise EffectBrokerError("AEXEFF014", "effect journal state is unknown")
    path = _rollback_prior(root, runtime_store, session, journal, recovered=True)
    try:
        runtime_store.acknowledge_recovery(session.repository_id)
    except RuntimeStateError:
        pass
    return RecoveryResult("recovered-prior", transaction_id, path)


def validate_effect_receipt(value: Any) -> EffectReceipt:
    """Validate the closed effect-receipt v1 evidence schema."""

    root_fields = {
        "schema", "operation", "identity", "entries", "state", "timing",
        "journal", "validation",
    }
    if not isinstance(value, dict) or set(value) != root_fields:
        raise EffectBrokerError("AEXEFF015", "effect receipt root field set is invalid")
    if value["schema"] != EFFECT_RECEIPT_SCHEMA or value["operation"] != EFFECT_OPERATION:
        raise EffectBrokerError("AEXEFF015", "effect receipt schema or operation is invalid")
    identity = value["identity"]
    if not isinstance(identity, dict) or set(identity) != {
        "bundle_sha256", "envelope_sha256", "nonce_sha256", "work_order", "evaluator"
    }:
        raise EffectBrokerError("AEXEFF015", "effect receipt identity is invalid")
    evaluator = identity["evaluator"]
    if not isinstance(evaluator, dict) or set(evaluator) != {
        "package", "version", "payload_sha256", "launcher_sha256"
    }:
        raise EffectBrokerError("AEXEFF015", "evaluator identity is invalid")
    entries: list[dict[str, Any]] = []
    for item in value["entries"]:
        if not isinstance(item, dict) or set(item) != {
            "operation", "path", "before_sha256", "after_sha256", "result"
        }:
            raise EffectBrokerError("AEXEFF015", "effect entry field set is invalid")
        if item["operation"] not in {"create", "replace", "delete"} or item["result"] != "applied":
            raise EffectBrokerError("AEXEFF015", "effect entry operation or result is invalid")
        entries.append(
            {
                "operation": item["operation"],
                "path": validate_portable_path(item["path"]),
                "before_sha256": (
                    None if item["before_sha256"] is None else validate_sha256(item["before_sha256"])
                ),
                "after_sha256": (
                    None if item["after_sha256"] is None else validate_sha256(item["after_sha256"])
                ),
                "result": "applied",
            }
        )
        if (
            item["operation"] == "create"
            and (entries[-1]["before_sha256"] is not None or entries[-1]["after_sha256"] is None)
        ) or (
            item["operation"] == "replace"
            and (entries[-1]["before_sha256"] is None or entries[-1]["after_sha256"] is None)
        ) or (
            item["operation"] == "delete"
            and (entries[-1]["before_sha256"] is None or entries[-1]["after_sha256"] is not None)
        ):
            raise EffectBrokerError("AEXEFF015", "effect receipt operation invariant is invalid")
    if not entries or entries != sorted(entries, key=lambda item: item["path"].encode("utf-8")):
        raise EffectBrokerError("AEXEFF015", "effect entries are empty or not path ordered")
    if len({item["path"] for item in entries}) != len(entries):
        raise EffectBrokerError("AEXEFF015", "effect receipt repeats a path")
    state = value["state"]
    timing = value["timing"]
    validation = value["validation"]
    if not isinstance(state, dict) or set(state) != {
        "state_before", "state_after", "previous_receipt_sha256", "transaction_id"
    }:
        raise EffectBrokerError("AEXEFF015", "effect receipt state is invalid")
    if not isinstance(timing, dict) or set(timing) != {"started_at", "completed_at"}:
        raise EffectBrokerError("AEXEFF015", "effect receipt timing is invalid")
    if value["journal"] != {"state": "committed"}:
        raise EffectBrokerError("AEXEFF015", "receipt does not name a committed journal")
    if not isinstance(validation, dict) or set(validation) != {"gates", "deviations", "evidence"}:
        raise EffectBrokerError("AEXEFF015", "effect receipt validation is invalid")
    gates = list(validation["gates"])
    deviations = list(validation["deviations"])
    evidence = list(validation["evidence"])
    if not all(
        isinstance(item, dict) and set(item) == {"id", "status"}
        and isinstance(item["id"], str) and item["status"] == "pass"
        for item in gates
    ):
        raise EffectBrokerError("AEXEFF015", "committed receipt gates must all pass")
    if not all(
        isinstance(item, dict) and set(item) == {"code", "message"}
        and isinstance(item["code"], str) and isinstance(item["message"], str)
        for item in deviations
    ):
        raise EffectBrokerError("AEXEFF015", "receipt deviations are invalid")
    if not all(
        isinstance(item, dict) and set(item) == {"kind", "path", "sha256"}
        and isinstance(item["kind"], str)
        for item in evidence
    ):
        raise EffectBrokerError("AEXEFF015", "receipt evidence is invalid")
    try:
        transaction_id = state["transaction_id"]
        if not isinstance(transaction_id, str) or len(transaction_id) != 32:
            raise ValueError
        int(transaction_id, 16)
        started = datetime.strptime(timing["started_at"], "%Y-%m-%dT%H:%M:%SZ")
        completed = datetime.strptime(timing["completed_at"], "%Y-%m-%dT%H:%M:%SZ")
        if completed < started:
            raise ValueError
    except (TypeError, ValueError) as exc:
        raise EffectBrokerError("AEXEFF015", "receipt transaction or timing is invalid") from exc
    if (
        not isinstance(identity["work_order"], str)
        or not identity["work_order"].startswith("WO-")
        or not isinstance(evaluator["package"], str)
        or not evaluator["package"]
        or not isinstance(evaluator["version"], str)
        or not evaluator["version"]
    ):
        raise EffectBrokerError("AEXEFF015", "receipt work-order or evaluator text is invalid")
    if len({item["id"] for item in gates}) != len(gates):
        raise EffectBrokerError("AEXEFF015", "receipt gates repeat an identity")
    evidence_paths = [item["path"] for item in evidence]
    if len(set(evidence_paths)) != len(evidence_paths):
        raise EffectBrokerError("AEXEFF015", "receipt evidence repeats a path")
    normalized = {
        "schema": EFFECT_RECEIPT_SCHEMA,
        "operation": EFFECT_OPERATION,
        "identity": {
            "bundle_sha256": validate_sha256(identity["bundle_sha256"]),
            "envelope_sha256": validate_sha256(identity["envelope_sha256"]),
            "nonce_sha256": validate_sha256(identity["nonce_sha256"]),
            "work_order": identity["work_order"],
            "evaluator": {
                "package": evaluator["package"],
                "version": evaluator["version"],
                "payload_sha256": validate_sha256(evaluator["payload_sha256"]),
                "launcher_sha256": validate_sha256(evaluator["launcher_sha256"]),
            },
        },
        "entries": entries,
        "state": {
            "state_before": validate_sha256(state["state_before"]),
            "state_after": validate_sha256(state["state_after"]),
            "previous_receipt_sha256": (
                None if state["previous_receipt_sha256"] is None
                else validate_sha256(state["previous_receipt_sha256"])
            ),
            "transaction_id": transaction_id,
        },
        "timing": dict(timing),
        "journal": {"state": "committed"},
        "validation": {
            "gates": sorted(gates, key=lambda item: item["id"].encode("utf-8")),
            "deviations": deviations,
            "evidence": sorted(
                (
                    {
                        "kind": item["kind"],
                        "path": validate_portable_path(item["path"]),
                        "sha256": validate_sha256(item["sha256"]),
                    }
                    for item in evidence
                ),
                key=lambda item: item["path"].encode("utf-8"),
            ),
        },
    }
    raw = canonical_json_bytes(normalized)
    return EffectReceipt(normalized, raw, hashlib.sha256(raw).hexdigest())


def parse_effect_receipt_bytes(raw: bytes) -> EffectReceipt:
    """Parse duplicate-safe effect-receipt bytes and require canonical form."""

    try:
        value = parse_json_bytes(raw)
    except AgentContractError as exc:
        raise EffectBrokerError("AEXEFF015", str(exc)) from exc
    receipt = validate_effect_receipt(value)
    if receipt.canonical_bytes != raw:
        raise EffectBrokerError("AEXEFF015", "effect receipt bytes are not canonical")
    return receipt


def _observe(
    observer: Callable[..., ContractDocument],
    root: Path,
    work_order: str,
    evaluator: EvaluatorIdentity,
    previous_receipt_sha256: str | None,
) -> ContractDocument:
    return observer(
        root,
        work_order_id=work_order,
        evaluator=evaluator,
        previous_receipt_sha256=previous_receipt_sha256,
    )


def apply_change_bundle(
    repository: Path,
    *,
    bundle_bytes: bytes,
    object_store: Path,
    envelope: ContractDocument,
    current_delegation_sha256: str,
    evaluator: EvaluatorIdentity,
    runtime_store: RuntimeStateStore,
    session: RuntimeSession,
    gates_passed: bool,
    managed_denied_paths: Iterable[str] = (),
    gate_results: Iterable[Mapping[str, str]] = (),
    deviations: Iterable[Mapping[str, str]] = (),
    evidence: Iterable[Mapping[str, str]] = (),
    now: Callable[[], datetime] = _now,
    observer: Callable[..., ContractDocument] = observe_repository,
    authority_guard: Callable[..., Any] | None = None,
    admission: Callable[..., LiveAdmission] = admit_fresh_envelope,
    fault: Callable[[str], None] | None = None,
    transaction_id_factory: Callable[[], str] = lambda: secrets.token_hex(16),
) -> EffectResult:
    """Admit and transactionally apply one exact evaluator-built bundle."""

    supplied_root = repository.absolute()
    _normal_directory(supplied_root, "repository root")
    root = supplied_root.resolve(strict=True)
    document = validate_contract(envelope.value, expected_schema=AUTONOMY_ENVELOPE_V2_SCHEMA)
    envelope_value = document.value
    selected_guard = authority_guard or require_mutation_authority
    authority = selected_guard(root, operation=EFFECT_OPERATION)
    actual_payload = getattr(
        getattr(authority, "identity", None), "evaluator_payload_sha256", None
    )
    if actual_payload is not None and actual_payload != evaluator.payload_sha256:
        raise EffectBrokerError("AEXEFF002", "mutation authority and observer evaluator differ")
    supplied_objects = object_store.absolute()
    _normal_directory(supplied_objects, "content object store")
    object_root = supplied_objects.resolve(strict=True)
    try:
        object_root.relative_to(root)
    except ValueError:
        pass
    else:
        raise EffectBrokerError("AEXEFF005", "content object store must be external")
    denied = tuple(
        sorted(
            {
                *(validate_portable_path(item, prefix_allowed=True) for item in _DEFAULT_DENIED),
                *(
                    validate_portable_path(item, prefix_allowed=True)
                    for item in managed_denied_paths
                ),
            },
            key=lambda item: item.encode("utf-8"),
        )
    )
    if EFFECT_OPERATION not in envelope_value["delegation"]["operations"]:
        raise EffectBrokerError("AEXEFF003", "envelope does not admit change-bundle-apply")
    previous_receipt = envelope_value["authority"]["previous_receipt_sha256"]
    nonce = envelope_value["authority"]["nonce"]
    started = _timestamp(now())
    selected_fault = fault or (lambda stage: None)
    journal: dict[str, Any] | None = None
    journal_persisted = False
    with runtime_store.effect_lock(session):
        recover_effect_transaction(root, runtime_store=runtime_store, session=session)
        fresh = _observe(
            observer,
            root,
            envelope_value["selection"]["work_order"],
            evaluator,
            previous_receipt,
        )
        admitted = admission(
            envelope=document,
            fresh_observation=fresh,
            current_delegation_sha256=current_delegation_sha256,
            now=now(),
            runtime_store=runtime_store,
            session=session,
            gates_passed=gates_passed,
        )
        try:
            bundle = parse_change_bundle_bytes(bundle_bytes)
            identity = bundle.value["identity"]
            if (
                identity["work_order"] != envelope_value["selection"]["work_order"]
                or identity["envelope_sha256"] != document.sha256
                or identity["repository_state_before"] != fresh.sha256
            ):
                raise EffectBrokerError(
                    "AEXEFF004", "bundle, envelope, and live-state identities differ"
                )
            scope = envelope_value["delegation"]["path_scope"]
            objects: dict[str, bytes] = {}
            missing_parents: dict[str, tuple[str, ...]] = {}
            for entry in bundle.value["changes"]:
                path = entry["path"]
                if not any(portable_path_within(path, item) for item in scope):
                    raise EffectBrokerError("AEXEFF005", f"path is outside scope: {path}")
                if any(portable_path_within(path, item) for item in denied):
                    raise EffectBrokerError("AEXEFF005", f"path is managed-denied: {path}")
                target, missing = _target(root, path, allow_missing=True)
                missing_parents[path] = missing
                if not _matches(_file_state(target), entry["before"]):
                    raise EffectBrokerError("AEXEFF007", f"stale before state: {path}")
                if entry["after"] is not None:
                    objects[path] = read_content_object(
                        object_root,
                        entry["after"]["sha256"],
                        entry["after"]["size"],
                    )
            prior_manifest = _snapshot(root)
            preflight_observation = _observe(
                observer,
                root,
                identity["work_order"],
                evaluator,
                previous_receipt,
            )
            if (
                preflight_observation.sha256 != fresh.sha256
                or _snapshot(root) != prior_manifest
            ):
                raise EffectBrokerError(
                    "AEXEFF007", "repository changed during complete effect preflight"
                )
            expected_manifest = _expected_manifest(prior_manifest, bundle.value["changes"])
            transaction_id = transaction_id_factory()
            try:
                if not isinstance(transaction_id, str) or len(transaction_id) != 32:
                    raise ValueError
                int(transaction_id, 16)
            except ValueError as exc:
                raise EffectBrokerError("AEXEFF001", "transaction ID source is invalid") from exc
            material = runtime_store.effect_material_directory(session, transaction_id)
            entries: list[dict[str, Any]] = []
            for entry in bundle.value["changes"]:
                before = entry["before"]
                if before is not None:
                    target, _ = _target(root, entry["path"], allow_missing=True)
                    _write_object(
                        material / "backups",
                        _read_exact(target, before, "target backup source"),
                        before["sha256"],
                    )
                entries.append(
                    {
                        "operation": entry["operation"],
                        "path": entry["path"],
                        "before": before,
                        "after": (
                            None
                            if entry["after"] is None
                            else {
                                "sha256": entry["after"]["sha256"],
                                "size": entry["after"]["size"],
                            }
                        ),
                    }
                )
            prior_manifest_sha256 = _manifest_sha256(prior_manifest)
            expected_manifest_sha256 = _manifest_sha256(expected_manifest)
            planned_parents = sorted(
                {
                    parent
                    for values in missing_parents.values()
                    for parent in values
                },
                key=lambda item: (item.count("/"), item.encode("utf-8")),
            )
            temporary_by_path = {
                entry["path"]: validate_portable_path(
                    (
                        Path(entry["path"]).parent
                        / f".se-harness-{transaction_id}-{index}.tmp"
                    ).as_posix()
                )
                for index, entry in enumerate(entries)
                if entry["after"] is not None
            }
            planned_temporaries = [
                temporary_by_path[entry["path"]]
                for entry in entries
                if entry["after"] is not None
            ]
            for relative in planned_temporaries:
                temporary, _ = _target(root, relative, allow_missing=True)
                if temporary.exists():
                    _file_state(temporary)
                    raise EffectBrokerError(
                        "AEXEFF009", f"planned temporary already exists: {relative}"
                    )
            plan = {
                "bundle_sha256": bundle.sha256,
                "envelope_sha256": document.sha256,
                "entries": entries,
                "prior_manifest_sha256": prior_manifest_sha256,
                "expected_manifest_sha256": expected_manifest_sha256,
                "created_parents": planned_parents,
                "temporaries": planned_temporaries,
            }
            journal = {
                "schema": EFFECT_JOURNAL_SCHEMA,
                "repository_id": session.repository_id,
                "session_id": session.session_id,
                "transaction_id": transaction_id,
                "state": "prepared",
                "bundle_sha256": bundle.sha256,
                "envelope_sha256": document.sha256,
                "nonce_sha256": admitted.nonce_sha256,
                "work_order": identity["work_order"],
                "state_before": fresh.sha256,
                "state_after": None,
                "previous_receipt_sha256": previous_receipt,
                "entries": entries,
                "prior_manifest_sha256": prior_manifest_sha256,
                "expected_manifest_sha256": expected_manifest_sha256,
                "plan_sha256": canonical_sha256(
                    plan, maximum_bytes=MAX_EFFECT_JOURNAL_BYTES
                ),
                "created_parents": planned_parents,
                "temporaries": planned_temporaries,
                "applied": [],
                "receipt_sha256": None,
                "uncertain_paths": [],
                "started_at": started,
            }
            selected_fault("before-journal")
            runtime_store.begin_effect_transaction(session, journal)
            journal_persisted = True
            selected_fault("after-journal-prepared")
            for relative in planned_parents:
                parent = root.joinpath(*relative.split("/"))
                try:
                    parent.mkdir()
                except OSError as exc:
                    raise EffectBrokerError(
                        "AEXEFF009", f"cannot create admitted parent: {exc}"
                    ) from exc
                selected_fault(f"after-parent:{relative}")
            for index, entry in enumerate(entries):
                if entry["after"] is None:
                    continue
                target, _ = _target(root, entry["path"], allow_missing=False)
                relative = temporary_by_path[entry["path"]]
                temporary, _ = _target(root, relative, allow_missing=False)
                descriptor: int | None = None
                try:
                    descriptor = os.open(
                        temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600
                    )
                    with os.fdopen(descriptor, "wb", closefd=True) as stream:
                        descriptor = None
                        stream.write(objects[entry["path"]])
                        stream.flush()
                        os.fsync(stream.fileno())
                except OSError as exc:
                    if descriptor is not None:
                        os.close(descriptor)
                    raise EffectBrokerError(
                        "AEXEFF009", f"cannot prepare replacement: {exc}"
                    ) from exc
                selected_fault(f"after-temp:{entry['path']}")
            _advance(runtime_store, session, journal, "applying")
            for entry in entries:
                target, _ = _target(root, entry["path"], allow_missing=False)
                if not _matches(_file_state(target), entry["before"]):
                    raise EffectBrokerError(
                        "AEXEFF007", f"target changed before apply: {entry['path']}"
                    )
                try:
                    if entry["after"] is None:
                        target.unlink()
                    else:
                        temporary, _ = _target(
                            root, temporary_by_path[entry["path"]], allow_missing=False
                        )
                        if not _matches(_file_state(temporary), entry["after"]):
                            raise EffectBrokerError(
                                "AEXEFF008", "prepared replacement object changed"
                            )
                        os.replace(temporary, target)
                    if not _matches(_file_state(target), entry["after"]):
                        raise EffectBrokerError(
                            "AEXEFF010", f"applied target differs: {entry['path']}"
                        )
                except EffectBrokerError:
                    raise
                except OSError as exc:
                    raise EffectBrokerError("AEXEFF010", f"target apply failed: {exc}") from exc
                journal["applied"].append(entry["path"])
                _advance(runtime_store, session, journal)
                selected_fault(f"after-apply:{entry['path']}")
            selected_fault("before-result-observation")
            if _snapshot(root) != expected_manifest:
                raise EffectBrokerError(
                    "AEXEFF011", "complete target manifest differs from planned result"
                )
            after_observation = _observe(
                observer,
                root,
                identity["work_order"],
                evaluator,
                previous_receipt,
            )
            journal["state_after"] = after_observation.sha256
            _advance(runtime_store, session, journal, "result-observed")
            selected_fault("before-receipt")
            receipt = validate_effect_receipt(
                {
                    "schema": EFFECT_RECEIPT_SCHEMA,
                    "operation": EFFECT_OPERATION,
                    "identity": {
                        "bundle_sha256": bundle.sha256,
                        "envelope_sha256": document.sha256,
                        "nonce_sha256": admitted.nonce_sha256,
                        "work_order": identity["work_order"],
                        "evaluator": evaluator.as_dict(),
                    },
                    "entries": [
                        {
                            "operation": entry["operation"],
                            "path": entry["path"],
                            "before_sha256": (
                                None if entry["before"] is None
                                else entry["before"]["sha256"]
                            ),
                            "after_sha256": (
                                None if entry["after"] is None
                                else entry["after"]["sha256"]
                            ),
                            "result": "applied",
                        }
                        for entry in entries
                    ],
                    "state": {
                        "state_before": fresh.sha256,
                        "state_after": after_observation.sha256,
                        "previous_receipt_sha256": previous_receipt,
                        "transaction_id": transaction_id,
                    },
                    "timing": {
                        "started_at": started,
                        "completed_at": _timestamp(now()),
                    },
                    "journal": {"state": "committed"},
                    "validation": {
                        "gates": list(gate_results)
                        or [{"id": "live-admission", "status": "pass"}],
                        "deviations": list(deviations),
                        "evidence": list(evidence),
                    },
                }
            )
            selected_fault("before-commit")
            _write_receipt(material / "receipt.json", receipt.canonical_bytes)
            journal["receipt_sha256"] = receipt.sha256
            _advance(runtime_store, session, journal, "committed")
            selected_fault("after-journal-commit")
            runtime_store.record_terminal(
                session,
                nonce=nonce,
                outcome="completed",
                receipt_sha256=receipt.sha256,
            )
            journal_path = runtime_store.archive_effect_transaction(
                session, transaction_id
            )
            return EffectResult(
                "committed", receipt, bundle.sha256, transaction_id, journal_path
            )
        except BaseException as exc:
            if not isinstance(exc, Exception):
                raise
            if journal is None or not journal_persisted:
                try:
                    runtime_store.record_terminal(
                        session, nonce=nonce, outcome="failed-consumed"
                    )
                except RuntimeStateError:
                    pass
            elif journal.get("state") == "committed":
                try:
                    runtime_store.mark_recovery_required(session, str(exc))
                except RuntimeStateError:
                    pass
                raise EffectBrokerError(
                    "AEXEFF013", "committed target requires journal finalization"
                ) from exc
            else:
                _rollback_prior(
                    root, runtime_store, session, journal, recovered=False
                )
            if isinstance(exc, EffectBrokerError):
                raise
            if isinstance(exc, ChangeBundleError):
                raise EffectBrokerError("AEXEFF003", str(exc)) from exc
            raise EffectBrokerError(
                "AEXEFF010", f"effect failed and prior state was restored: {exc}"
            ) from exc


__all__ = [
    "EFFECT_OPERATION",
    "EFFECT_RECEIPT_SCHEMA",
    "EffectBrokerError",
    "EffectReceipt",
    "EffectResult",
    "RecoveryResult",
    "apply_change_bundle",
    "recover_effect_transaction",
    "parse_effect_receipt_bytes",
    "validate_effect_receipt",
]
