"""Pure runtime-neutral contracts for agentic execution.

This module validates supplied semantic values only.  It deliberately has no
filesystem, Git, process, credential, network, lifecycle, callback, or other
effect boundary.  Successful envelope outcomes are therefore ``constructed``
and ``admissible``; this module can never derive authority or admit an effect.
"""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Iterable, Mapping, Sequence


CATALOG_SCHEMA = "se-harness-agent-contract-catalog-v1"
CANONICAL_JSON_SCHEMA = "se-harness-canonical-json-v1"
AUTONOMY_ENVELOPE_SCHEMA = "se-harness-autonomy-envelope-v1"
AUTONOMY_ENVELOPE_V2_SCHEMA = "se-harness-autonomy-envelope-v2"
DELEGATION_SCHEMA = "se-harness-agentic-delegation-v1"
PACKET_CONTEXT_SCHEMA = "se-harness-decision-packet-context-v1"
PACKET_V1_SCHEMA = "se-harness-decision-packet-v1"
PACKET_V2_SCHEMA = "se-harness-decision-packet-v2"
RECEIPT_SCHEMA = "se-harness-execution-receipt-v1"
PROFILE_SCHEMA = "se-harness-logical-execution-profile-v1"
REPOSITORY_STATE_SCHEMA = "se-harness-repository-state-binding-v1"
REPOSITORY_OBSERVATION_SCHEMA = "se-harness-repository-observation-v1"
WORKTREE_STATE_SCHEMA = "se-harness-worktree-state-v1"
WORKFLOW_RESULT_SCHEMA = "se-harness-workflow-result-v2"

MAX_DOCUMENT_BYTES = 1_048_576
MAX_NESTING = 32
MAX_OBJECT_MEMBERS = 1_024
MAX_ARRAY_ENTRIES = 1_024
MAX_STRING_SCALARS = 16_384
MAX_PATH_BYTES = 1_024
MAX_PARALLEL_WRITERS = 32
MAX_RETRY = 10
MAX_INTEGER = (1 << 63) - 1
WORKTREE_MAX_ENTRIES = 100_000
MANIFEST_MAX_BYTES = 67_108_864

MANDATORY_STOPS = frozenset(
    {"accountable-decision-required", "action-time-authorization-required"}
)
SCHEMA_ROOTS = {
    AUTONOMY_ENVELOPE_SCHEMA: "autonomy-envelope",
    AUTONOMY_ENVELOPE_V2_SCHEMA: "autonomy-envelope-v2",
    DELEGATION_SCHEMA: "agentic-delegation",
    PACKET_CONTEXT_SCHEMA: "decision-packet-context",
    PACKET_V1_SCHEMA: "decision-packet",
    PACKET_V2_SCHEMA: "decision-packet-v2",
    RECEIPT_SCHEMA: "execution-receipt",
    PROFILE_SCHEMA: "logical-execution-profile",
    REPOSITORY_STATE_SCHEMA: "repository-state-binding",
    REPOSITORY_OBSERVATION_SCHEMA: "repository-observation",
    WORKTREE_STATE_SCHEMA: "worktree-state",
}
DIAGNOSTICS = {
    "AEXCON001": "malformed bytes, invalid UTF-8, or invalid JSON",
    "AEXCON002": "resource bound exceeded",
    "AEXCON003": "duplicate key or duplicate collection identity",
    "AEXCON004": "unsupported catalog or schema identifier",
    "AEXCON005": "missing or unknown field",
    "AEXCON006": "invalid scalar, nullability, or collection type",
    "AEXCON007": "invalid enum, identifier, digest, or cross-reference",
    "AEXCON008": "invalid, ambiguous, or escaping portable path",
    "AEXCON009": "non-canonical object, bytes, or ordering",
    "AEXCON010": "widened child or request outside managed scope",
    "AEXCON011": "stale or mismatched repository, work-order, evaluator, or parent identity",
    "AEXCON012": "missing, conflicting, or non-authoritative actor assertion",
    "AEXCON013": "failed or not-assessable required gate",
    "AEXCON014": "incomplete or non-lossless decision-packet source or projection",
    "AEXCON015": "incomplete or inconsistent execution receipt",
    "AEXCON016": "authority claim, secret, hidden reasoning, or prohibited metadata",
    "AEXCON017": "invalid or provider-bound logical profile",
    "AEXCON018": "internal failure without partial result",
}

_PORTABLE_ID = re.compile(r"[a-z0-9](?:[a-z0-9._-]{0,126}[a-z0-9])?")
_PROFILE_NAME = re.compile(r"[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?")
_ARTIFACT_ID = re.compile(r"[A-Z][A-Z0-9]*-[A-Z0-9][A-Z0-9-]*")
_WORK_ORDER_ID = re.compile(r"WO-[A-Z0-9][A-Z0-9-]*")
_SEMANTIC_VERSION = re.compile(
    r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:[-+][0-9A-Za-z.-]+)?"
)
_DIAGNOSTIC_ID = re.compile(r"(?:[A-Z][A-Z0-9._-]{0,127}|[a-z0-9](?:[a-z0-9._-]{0,126}[a-z0-9])?)")
_SHA256 = re.compile(r"[0-9a-f]{64}")
_NONCE = re.compile(r"[0-9a-f]{32,128}")
_UTC_TIMESTAMP = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")
_GIT_OBJECT_ID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")
_CONTROL = re.compile(r"[\x00-\x1f\x7f]")
_WINDOWS_RESERVED = {
    "con",
    "prn",
    "aux",
    "nul",
    *(f"com{index}" for index in range(1, 10)),
    *(f"lpt{index}" for index in range(1, 10)),
}
_PROVIDER_MARKERS = {
    "anthropic",
    "chatgpt",
    "claude",
    "codex",
    "copilot",
    "gemini",
    "openai",
}


class AgentContractError(ValueError):
    """One stable, bounded AEX contract diagnostic."""

    def __init__(self, code: str, path: str, message: str) -> None:
        if code not in DIAGNOSTICS:
            code = "AEXCON018"
        bounded = _safe_message(message)
        super().__init__(f"{code} at {path}: {bounded}")
        self.code = code
        self.path = path
        self.message = bounded

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "path": self.path, "message": self.message}


@dataclass(frozen=True)
class ContractDocument:
    """A validated semantic object and its canonical identity."""

    value: Mapping[str, Any]
    canonical_bytes: bytes
    sha256: str


@dataclass(frozen=True)
class EnvelopeConstruction:
    """A non-authoritative envelope candidate built from supplied values."""

    outcome: str
    state_binding: ContractDocument
    envelope: ContractDocument
    selected_work_order: str
    procedure_id: str
    evaluator_payload_sha256: str
    formal_snapshot_sha256: str
    narrowing: tuple[str, ...]
    non_effects: tuple[str, ...] = (
        "No repository, lifecycle, Git, process, credential, network, or external mutation occurred.",
        "No accountable decision, authoritative derivation, or effect admission occurred.",
    )


@dataclass(frozen=True)
class AdmissionAssessment:
    """A pure admissibility result; it is never effect authorization."""

    outcome: str
    envelope_sha256: str
    operation: str
    target_paths: tuple[str, ...]
    expected_current_repository_state: str
    required_evidence: tuple[str, ...]
    diagnostics: tuple[Mapping[str, str], ...]
    non_effects: tuple[str, ...] = (
        "No effect callback exists or was invoked.",
        "The operation was not admitted and no authority was created.",
    )


@dataclass(frozen=True)
class ReceiptExpectations:
    """Independent plan facts used to assess a receipt."""

    profiles: tuple[str, ...]
    skill_names: tuple[str, ...]
    operation_ids: tuple[str, ...]
    worker_ids: tuple[str, ...]
    changed_paths: tuple[str, ...]
    evidence: tuple[tuple[str, str | None, str], ...]
    state_before: tuple[tuple[str, str], ...]
    state_after: tuple[tuple[str, str], ...]
    autonomy_envelope_sha256: str | None = None
    evaluator_payload_sha256: str | None = None


def _safe_message(value: object) -> str:
    text = str(value)
    text = "".join(character if character >= " " and character != "\x7f" else "?" for character in text)
    return text[:512] or "contract validation failed"


def _error(code: str, path: str, message: str) -> None:
    raise AgentContractError(code, path, message)


def _duplicate_object(pairs: Iterable[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            _error("AEXCON003", f"$.{key}", "duplicate JSON object key")
        result[key] = value
    return result


def _bounded_walk(
    value: Any,
    *,
    path: str = "$",
    depth: int = 0,
    array_limit: int = MAX_ARRAY_ENTRIES,
) -> None:
    if depth > MAX_NESTING:
        _error("AEXCON002", path, "JSON nesting exceeds 32 levels below the root")
    if value is None or isinstance(value, bool):
        return
    if isinstance(value, int):
        if not -MAX_INTEGER <= value <= MAX_INTEGER:
            _error("AEXCON006", path, "integer is outside the canonical range")
        return
    if isinstance(value, float):
        _error("AEXCON006", path, "floating-point values are prohibited")
    if isinstance(value, str):
        if len(value) > MAX_STRING_SCALARS:
            _error("AEXCON002", path, "string exceeds 16,384 Unicode scalar values")
        try:
            value.encode("utf-8")
        except UnicodeEncodeError:
            _error("AEXCON006", path, "string is not valid Unicode")
        return
    if isinstance(value, list):
        if len(value) > array_limit:
            _error("AEXCON002", path, f"array exceeds {array_limit} entries")
        for index, item in enumerate(value):
            _bounded_walk(item, path=f"{path}[{index}]", depth=depth + 1, array_limit=array_limit)
        return
    if isinstance(value, dict):
        if len(value) > MAX_OBJECT_MEMBERS:
            _error("AEXCON002", path, "object exceeds 1,024 members")
        for key, item in value.items():
            if not isinstance(key, str):
                _error("AEXCON006", path, "object keys must be strings")
            _bounded_walk(item, path=f"{path}.{key}", depth=depth + 1, array_limit=array_limit)
        return
    _error("AEXCON006", path, "unsupported JSON value type")


def _parse_json_bytes(raw: bytes, *, document_limit: int, array_limit: int) -> Any:
    if not isinstance(raw, bytes):
        _error("AEXCON001", "$", "input must be bytes")
    if len(raw) > document_limit:
        _error("AEXCON002", "$", f"input document exceeds {document_limit} bytes")
    if raw.startswith(b"\xef\xbb\xbf"):
        _error("AEXCON001", "$", "UTF-8 byte-order marks are prohibited")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        _error("AEXCON001", "$", "input document is not valid UTF-8")

    def reject_number(_: str) -> None:
        _error("AEXCON006", "$", "floating-point and non-finite numbers are prohibited")

    try:
        value = json.loads(
            text,
            object_pairs_hook=_duplicate_object,
            parse_float=reject_number,
            parse_constant=reject_number,
        )
    except AgentContractError:
        raise
    except (json.JSONDecodeError, RecursionError, ValueError):
        _error("AEXCON001", "$", "input document is not valid bounded JSON")
    _bounded_walk(value, array_limit=array_limit)
    return value


def parse_json_bytes(raw: bytes) -> Any:
    """Parse ordinary bounded UTF-8 JSON with duplicate-key and float rejection."""

    return _parse_json_bytes(raw, document_limit=MAX_DOCUMENT_BYTES, array_limit=MAX_ARRAY_ENTRIES)


def canonical_json_bytes(value: Any) -> bytes:
    """Return ``se-harness-canonical-json-v1`` bytes for a JSON value."""

    is_worktree = isinstance(value, dict) and value.get("schema") == WORKTREE_STATE_SCHEMA
    _bounded_walk(value, array_limit=WORKTREE_MAX_ENTRIES if is_worktree else MAX_ARRAY_ENTRIES)
    try:
        encoded = (
            json.dumps(
                value,
                ensure_ascii=False,
                allow_nan=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
            + b"\n"
        )
        limit = MANIFEST_MAX_BYTES if is_worktree else MAX_DOCUMENT_BYTES
        if len(encoded) > limit:
            _error("AEXCON002", "$", f"canonical document exceeds {limit} bytes")
        return encoded
    except (UnicodeEncodeError, TypeError, ValueError):
        _error("AEXCON006", "$", "value cannot be canonically encoded as UTF-8 JSON")


def canonical_sha256(value: Any) -> str:
    """Return the lowercase SHA-256 identity of canonical JSON bytes."""

    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _document(value: Mapping[str, Any]) -> ContractDocument:
    encoded = canonical_json_bytes(value)
    return ContractDocument(value, encoded, hashlib.sha256(encoded).hexdigest())


def _object(value: Any, fields: set[str], path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        _error("AEXCON006", path, "value must be an object")
    missing = sorted(fields - value.keys())
    unknown = sorted(value.keys() - fields)
    if missing:
        _error("AEXCON005", path, f"missing fields: {', '.join(missing)}")
    if unknown:
        _error("AEXCON005", path, f"unknown fields: {', '.join(unknown)}")
    return value


def _array(value: Any, path: str, *, maximum: int = MAX_ARRAY_ENTRIES) -> list[Any]:
    if not isinstance(value, list):
        _error("AEXCON006", path, "value must be an array")
    if len(value) > maximum:
        _error("AEXCON002", path, f"array exceeds {maximum} entries")
    return value


def _boolean(value: Any, path: str) -> bool:
    if not isinstance(value, bool):
        _error("AEXCON006", path, "value must be a boolean")
    return value


def _integer(value: Any, path: str, *, minimum: int, maximum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        _error("AEXCON006", path, "value must be an integer")
    if not minimum <= value <= maximum:
        _error("AEXCON006", path, f"integer must be from {minimum} through {maximum}")
    return value


def _text(
    value: Any,
    path: str,
    *,
    maximum: int = MAX_STRING_SCALARS,
    pattern: re.Pattern[str] | None = None,
    code: str = "AEXCON006",
) -> str:
    if not isinstance(value, str) or not value or len(value) > maximum:
        _error(code, path, f"value must be non-empty text of at most {maximum} scalars")
    if _CONTROL.search(value) or "\ufeff" in value:
        _error(code, path, "control characters and byte-order marks are prohibited")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        _error(code, path, "value must be valid UTF-8 text")
    if pattern is not None and pattern.fullmatch(value) is None:
        _error(code, path, "value has an invalid identifier form")
    return value


def _nullable_text(value: Any, path: str, validator: Any) -> str | None:
    return None if value is None else validator(value, path)


def _portable_id(value: Any, path: str) -> str:
    return _text(value, path, maximum=128, pattern=_PORTABLE_ID, code="AEXCON007")


def _profile_name(value: Any, path: str) -> str:
    return _text(value, path, maximum=64, pattern=_PROFILE_NAME, code="AEXCON007")


def _managed_id(value: Any, path: str) -> str:
    if isinstance(value, str) and _ARTIFACT_ID.fullmatch(value):
        return value
    return _portable_id(value, path)


def _diagnostic_id(value: Any, path: str) -> str:
    return _text(value, path, maximum=128, pattern=_DIAGNOSTIC_ID, code="AEXCON007")


def _artifact_id(value: Any, path: str) -> str:
    return _text(value, path, maximum=128, pattern=_ARTIFACT_ID, code="AEXCON007")


def _work_order_id(value: Any, path: str) -> str:
    return _text(value, path, maximum=128, pattern=_WORK_ORDER_ID, code="AEXCON007")


def _sha256(value: Any, path: str) -> str:
    return _text(value, path, maximum=64, pattern=_SHA256, code="AEXCON007")


def _nullable_sha256(value: Any, path: str) -> str | None:
    return None if value is None else _sha256(value, path)


def _utc_timestamp(value: Any, path: str) -> str:
    result = _text(value, path, maximum=20, pattern=_UTC_TIMESTAMP, code="AEXCON007")
    try:
        parsed = datetime.strptime(result, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
    except ValueError:
        _error("AEXCON007", path, "timestamp is not a valid UTC instant")
    if parsed.strftime("%Y-%m-%dT%H:%M:%SZ") != result:
        _error("AEXCON009", path, "timestamp is not canonical UTC")
    return result


def _nonce(value: Any, path: str) -> str:
    return _text(value, path, maximum=128, pattern=_NONCE, code="AEXCON007")


def _git_object_id(value: Any, path: str, object_format: str | None = None) -> str:
    result = _text(value, path, maximum=64, pattern=_GIT_OBJECT_ID, code="AEXCON007")
    expected = 40 if object_format == "sha1" else 64 if object_format == "sha256" else None
    if expected is not None and len(result) != expected:
        _error("AEXCON007", path, f"object ID length does not match {object_format}")
    return result


def _semantic_version(value: Any, path: str) -> str:
    return _text(value, path, maximum=128, pattern=_SEMANTIC_VERSION, code="AEXCON007")


def _path(value: Any, path: str, *, prefix_allowed: bool = False) -> str:
    if not isinstance(value, str) or not value:
        _error("AEXCON008", path, "portable path must be non-empty text")
    is_prefix = value.endswith("/")
    if is_prefix and not prefix_allowed:
        _error("AEXCON008", path, "an exact file path cannot end in a separator")
    candidate = value[:-1] if is_prefix else value
    try:
        encoded = value.encode("utf-8")
    except UnicodeEncodeError:
        _error("AEXCON008", path, "portable path must be valid UTF-8")
    if len(encoded) > MAX_PATH_BYTES:
        _error("AEXCON002", path, "portable path exceeds 1,024 UTF-8 bytes")
    if unicodedata.normalize("NFC", value) != value:
        _error("AEXCON009", path, "portable path must be NFC-normalized")
    if (
        not candidate
        or candidate.startswith("/")
        or "\\" in candidate
        or ":" in candidate
        or "*" in candidate
        or "?" in candidate
        or "://" in candidate
        or _CONTROL.search(candidate)
    ):
        _error("AEXCON008", path, "portable path is absolute, ambiguous, or contains a prohibited character")
    for component in candidate.split("/"):
        if not component or component in {".", ".."} or component[-1:] in {".", " "}:
            _error("AEXCON008", path, "portable path contains an unsafe component")
        if component.split(".", 1)[0].casefold() in _WINDOWS_RESERVED:
            _error("AEXCON008", path, "portable path contains a reserved device component")
    return value


def _string_set(
    value: Any,
    path: str,
    validator: Any,
    *,
    minimum: int = 0,
    paths: bool = False,
) -> list[str]:
    selected = [validator(item, f"{path}[{index}]") for index, item in enumerate(_array(value, path))]
    if len(selected) < minimum:
        _error("AEXCON006", path, f"collection requires at least {minimum} entries")
    if len(set(selected)) != len(selected):
        _error("AEXCON003", path, "collection contains a duplicate value")
    if paths:
        _reject_case_collisions(selected, path)
    return sorted(selected, key=lambda item: item.encode("utf-8"))


def _sequence(value: Any, path: str, validator: Any) -> list[Any]:
    return [validator(item, f"{path}[{index}]") for index, item in enumerate(_array(value, path))]


def _identity_set(
    value: Any,
    path: str,
    validator: Any,
    identity: str,
    *,
    maximum: int = MAX_ARRAY_ENTRIES,
) -> list[dict[str, Any]]:
    result = [
        validator(item, f"{path}[{index}]")
        for index, item in enumerate(_array(value, path, maximum=maximum))
    ]
    identities = [str(item[identity]) for item in result]
    if len(set(identities)) != len(identities):
        _error("AEXCON003", path, f"collection contains a duplicate {identity}")
    if identity == "path":
        _reject_case_collisions(identities, path)
    return sorted(result, key=lambda item: str(item[identity]).encode("utf-8"))


def _reject_case_collisions(values: Sequence[str], path: str) -> None:
    seen: dict[str, str] = {}
    for value in values:
        key = value.casefold()
        prior = seen.get(key)
        if prior is not None and prior != value:
            _error("AEXCON008", path, "portable path collection has a case-folded collision")
        seen[key] = value


def _path_within(child: str, parent: str) -> bool:
    if parent.endswith("/"):
        return child.startswith(parent)
    return child == parent


def _path_scope(value: Any, path: str, *, minimum: int = 0) -> list[str]:
    selected = _string_set(
        value,
        path,
        lambda item, item_path: _path(item, item_path, prefix_allowed=True),
        minimum=minimum,
        paths=True,
    )
    for index, current in enumerate(selected):
        for other in selected[index + 1 :]:
            if _path_within(other, current) or _path_within(current, other):
                _error("AEXCON008", path, "path scope contains overlapping or redundant entries")
    return selected


def _enum(value: Any, path: str, allowed: set[str]) -> str:
    result = _text(value, path, maximum=128, code="AEXCON007")
    if result not in allowed:
        _error("AEXCON007", path, "value is not an allowed enum member")
    return result


def _validate_worktree_entry(value: Any, path: str, object_format: str) -> dict[str, Any]:
    entry = _object(
        value,
        {
            "path",
            "index_mode",
            "index_object_id",
            "worktree_kind",
            "worktree_mode",
            "worktree_sha256",
            "worktree_object_id",
        },
        path,
    )
    result: dict[str, Any] = {"path": _path(entry["path"], f"{path}.path")}
    index_mode = entry["index_mode"]
    if index_mode is not None:
        index_mode = _enum(index_mode, f"{path}.index_mode", {"100644", "100755", "120000", "160000"})
    index_object_id = entry["index_object_id"]
    if (index_mode is None) != (index_object_id is None):
        _error("AEXCON007", path, "index mode and object ID nullability disagree")
    result["index_mode"] = index_mode
    result["index_object_id"] = (
        None if index_object_id is None else _git_object_id(index_object_id, f"{path}.index_object_id", object_format)
    )
    kind = _enum(entry["worktree_kind"], f"{path}.worktree_kind", {"absent", "regular", "symlink", "gitlink"})
    expected_modes = {
        "absent": {None},
        "regular": {"100644", "100755"},
        "symlink": {"120000"},
        "gitlink": {"160000"},
    }
    mode = entry["worktree_mode"]
    if mode not in expected_modes[kind]:
        _error("AEXCON007", f"{path}.worktree_mode", "worktree mode is inconsistent with worktree kind")
    digest = entry["worktree_sha256"]
    if kind in {"regular", "symlink"}:
        digest = _sha256(digest, f"{path}.worktree_sha256")
    elif digest is not None:
        _error("AEXCON007", f"{path}.worktree_sha256", "digest must be null for absent or gitlink entries")
    object_id = entry["worktree_object_id"]
    if kind == "gitlink":
        object_id = _git_object_id(object_id, f"{path}.worktree_object_id", object_format)
    elif object_id is not None:
        _error("AEXCON007", f"{path}.worktree_object_id", "object ID is valid only for a gitlink")
    result.update(
        {
            "worktree_kind": kind,
            "worktree_mode": mode,
            "worktree_sha256": digest,
            "worktree_object_id": object_id,
        }
    )
    return result


def _validate_worktree_state(value: Any, path: str = "$") -> dict[str, Any]:
    root = _object(value, {"schema", "git_object_format", "head", "tree", "entries"}, path)
    if root["schema"] != WORKTREE_STATE_SCHEMA:
        _error("AEXCON004", f"{path}.schema", "unsupported worktree-state schema")
    object_format = _enum(root["git_object_format"], f"{path}.git_object_format", {"sha1", "sha256"})
    entries_raw = _array(root["entries"], f"{path}.entries", maximum=WORKTREE_MAX_ENTRIES)
    entries = _identity_set(
        entries_raw,
        f"{path}.entries",
        lambda item, item_path: _validate_worktree_entry(item, item_path, object_format),
        "path",
        maximum=WORKTREE_MAX_ENTRIES,
    )
    return {
        "schema": WORKTREE_STATE_SCHEMA,
        "git_object_format": object_format,
        "head": _git_object_id(root["head"], f"{path}.head", object_format),
        "tree": _git_object_id(root["tree"], f"{path}.tree", object_format),
        "entries": entries,
    }


def _validate_repository_state(value: Any, path: str = "$") -> dict[str, Any]:
    root = _object(value, {"schema", "repository", "governance"}, path)
    if root["schema"] != REPOSITORY_STATE_SCHEMA:
        _error("AEXCON004", f"{path}.schema", "unsupported repository-state schema")
    repository = _object(
        root["repository"],
        {"git_object_format", "head", "tree", "worktree_state_sha256"},
        f"{path}.repository",
    )
    object_format = _enum(
        repository["git_object_format"], f"{path}.repository.git_object_format", {"sha1", "sha256"}
    )
    governance = _object(
        root["governance"],
        {"formal_snapshot_sha256", "managed_lock_sha256", "work_order", "work_order_sha256"},
        f"{path}.governance",
    )
    return {
        "schema": REPOSITORY_STATE_SCHEMA,
        "repository": {
            "git_object_format": object_format,
            "head": _git_object_id(repository["head"], f"{path}.repository.head", object_format),
            "tree": _git_object_id(repository["tree"], f"{path}.repository.tree", object_format),
            "worktree_state_sha256": _sha256(
                repository["worktree_state_sha256"], f"{path}.repository.worktree_state_sha256"
            ),
        },
        "governance": {
            "formal_snapshot_sha256": _sha256(
                governance["formal_snapshot_sha256"], f"{path}.governance.formal_snapshot_sha256"
            ),
            "managed_lock_sha256": _sha256(
                governance["managed_lock_sha256"], f"{path}.governance.managed_lock_sha256"
            ),
            "work_order": _work_order_id(governance["work_order"], f"{path}.governance.work_order"),
            "work_order_sha256": _sha256(
                governance["work_order_sha256"], f"{path}.governance.work_order_sha256"
            ),
        },
    }


def _validate_repository_observation(value: Any, path: str = "$") -> dict[str, Any]:
    root = _object(
        value,
        {"schema", "repository", "evaluator", "git", "governance", "filesystem", "previous_receipt_sha256"},
        path,
    )
    if root["schema"] != REPOSITORY_OBSERVATION_SCHEMA:
        _error("AEXCON004", f"{path}.schema", "unsupported repository-observation schema")
    evaluator = _object(
        root["evaluator"],
        {"package", "version", "payload_sha256", "launcher_sha256"},
        f"{path}.evaluator",
    )
    git = _object(
        root["git"],
        {
            "object_format",
            "head",
            "symbolic_ref",
            "index_entries_sha256",
            "tracked_worktree_sha256",
            "untracked_nonignored_sha256",
            "conflicts",
            "submodules",
        },
        f"{path}.git",
    )
    object_format = _enum(git["object_format"], f"{path}.git.object_format", {"sha1", "sha256"})
    head = git["head"]
    if head is not None:
        head = _git_object_id(head, f"{path}.git.head", object_format)
    symbolic_ref = git["symbolic_ref"]
    if symbolic_ref is not None:
        symbolic_ref = _text(symbolic_ref, f"{path}.git.symbolic_ref", maximum=512)
        if not symbolic_ref.startswith("refs/"):
            _error("AEXCON007", f"{path}.git.symbolic_ref", "symbolic ref must start with refs/")
    governance = _object(
        root["governance"],
        {
            "managed_lock_sha256",
            "formal_snapshot_sha256",
            "workflow_contract_sha256",
            "decision_rights_sha256",
            "work_order",
            "work_order_sha256",
            "work_order_status",
        },
        f"{path}.governance",
    )
    filesystem = _object(
        root["filesystem"],
        {"platform_family", "case_sensitive", "regular_file_manifest_sha256", "unsupported_object_count"},
        f"{path}.filesystem",
    )
    return {
        "schema": REPOSITORY_OBSERVATION_SCHEMA,
        "repository": _sha256(root["repository"], f"{path}.repository"),
        "evaluator": {
            "package": _portable_id(evaluator["package"], f"{path}.evaluator.package"),
            "version": _semantic_version(evaluator["version"], f"{path}.evaluator.version"),
            "payload_sha256": _sha256(evaluator["payload_sha256"], f"{path}.evaluator.payload_sha256"),
            "launcher_sha256": _sha256(evaluator["launcher_sha256"], f"{path}.evaluator.launcher_sha256"),
        },
        "git": {
            "object_format": object_format,
            "head": head,
            "symbolic_ref": symbolic_ref,
            "index_entries_sha256": _sha256(git["index_entries_sha256"], f"{path}.git.index_entries_sha256"),
            "tracked_worktree_sha256": _sha256(
                git["tracked_worktree_sha256"], f"{path}.git.tracked_worktree_sha256"
            ),
            "untracked_nonignored_sha256": _sha256(
                git["untracked_nonignored_sha256"], f"{path}.git.untracked_nonignored_sha256"
            ),
            "conflicts": _boolean(git["conflicts"], f"{path}.git.conflicts"),
            "submodules": _boolean(git["submodules"], f"{path}.git.submodules"),
        },
        "governance": {
            "managed_lock_sha256": _sha256(
                governance["managed_lock_sha256"], f"{path}.governance.managed_lock_sha256"
            ),
            "formal_snapshot_sha256": _sha256(
                governance["formal_snapshot_sha256"], f"{path}.governance.formal_snapshot_sha256"
            ),
            "workflow_contract_sha256": _sha256(
                governance["workflow_contract_sha256"], f"{path}.governance.workflow_contract_sha256"
            ),
            "decision_rights_sha256": _sha256(
                governance["decision_rights_sha256"], f"{path}.governance.decision_rights_sha256"
            ),
            "work_order": _work_order_id(governance["work_order"], f"{path}.governance.work_order"),
            "work_order_sha256": _sha256(
                governance["work_order_sha256"], f"{path}.governance.work_order_sha256"
            ),
            "work_order_status": _managed_id(
                governance["work_order_status"], f"{path}.governance.work_order_status"
            ),
        },
        "filesystem": {
            "platform_family": _enum(
                filesystem["platform_family"], f"{path}.filesystem.platform_family", {"posix", "windows"}
            ),
            "case_sensitive": _boolean(filesystem["case_sensitive"], f"{path}.filesystem.case_sensitive"),
            "regular_file_manifest_sha256": _sha256(
                filesystem["regular_file_manifest_sha256"],
                f"{path}.filesystem.regular_file_manifest_sha256",
            ),
            "unsupported_object_count": _integer(
                filesystem["unsupported_object_count"],
                f"{path}.filesystem.unsupported_object_count",
                minimum=0,
                maximum=MAX_INTEGER,
            ),
        },
        "previous_receipt_sha256": _nullable_sha256(
            root["previous_receipt_sha256"], f"{path}.previous_receipt_sha256"
        ),
    }


def _validate_agentic_delegation(value: Any, path: str = "$") -> dict[str, Any]:
    root = _object(
        value,
        {
            "schema",
            "delegated_by",
            "delegate",
            "decision_rights",
            "operations",
            "execution_profiles",
            "paths",
            "required_evidence",
            "valid_until",
            "max_retry",
            "max_parallel_writers",
            "child_delegation",
            "stop_before",
        },
        path,
    )
    if root["schema"] != DELEGATION_SCHEMA:
        _error("AEXCON004", f"{path}.schema", "unsupported agentic-delegation schema")
    paths = _path_scope(root["paths"], f"{path}.paths", minimum=1)
    evidence = _identity_set(
        root["required_evidence"],
        f"{path}.required_evidence",
        lambda item, item_path: {
            "kind": _portable_id(
                _object(item, {"kind", "path"}, item_path)["kind"],
                f"{item_path}.kind",
            ),
            "path": _path(item["path"], f"{item_path}.path"),
        },
        "path",
    )
    if not evidence:
        _error("AEXCON006", f"{path}.required_evidence", "collection requires at least 1 entry")
    stops = _string_set(root["stop_before"], f"{path}.stop_before", _managed_id)
    if not MANDATORY_STOPS.issubset(stops):
        _error("AEXCON012", f"{path}.stop_before", "mandatory accountable stop boundaries are missing")
    for item in evidence:
        if not any(_path_within(item["path"], parent) for parent in paths):
            _error("AEXCON010", f"{path}.required_evidence", "required evidence is outside delegated paths")
    if _integer(root["max_parallel_writers"], f"{path}.max_parallel_writers", minimum=0, maximum=1) != 1:
        _error("AEXCON012", f"{path}.max_parallel_writers", "delegation requires exactly one writer")
    if _boolean(root["child_delegation"], f"{path}.child_delegation") is not False:
        _error("AEXCON012", f"{path}.child_delegation", "child delegation is prohibited")
    return {
        "schema": DELEGATION_SCHEMA,
        "delegated_by": _text(root["delegated_by"], f"{path}.delegated_by", maximum=512),
        "delegate": _portable_id(root["delegate"], f"{path}.delegate"),
        "decision_rights": _string_set(
            root["decision_rights"], f"{path}.decision_rights", _managed_id
        ),
        "operations": _string_set(root["operations"], f"{path}.operations", _managed_id, minimum=1),
        "execution_profiles": _string_set(
            root["execution_profiles"], f"{path}.execution_profiles", _profile_name, minimum=1
        ),
        "paths": paths,
        "required_evidence": evidence,
        "valid_until": _utc_timestamp(root["valid_until"], f"{path}.valid_until"),
        "max_retry": _integer(root["max_retry"], f"{path}.max_retry", minimum=0, maximum=3),
        "max_parallel_writers": 1,
        "child_delegation": False,
        "stop_before": stops,
    }


def _validate_envelope(value: Any, path: str = "$") -> dict[str, Any]:
    root = _object(value, {"schema", "selection", "delegation", "evidence"}, path)
    if root["schema"] != AUTONOMY_ENVELOPE_SCHEMA:
        _error("AEXCON004", f"{path}.schema", "unsupported autonomy-envelope schema")
    selection = _object(
        root["selection"],
        {"work_order", "work_order_sha256", "repository_state", "evaluator_payload_sha256"},
        f"{path}.selection",
    )
    delegation = _object(
        root["delegation"],
        {
            "asserted_by",
            "operations",
            "path_scope",
            "execution_profiles",
            "max_parallel_writers",
            "retry_limits",
            "stop_before",
        },
        f"{path}.delegation",
    )
    operations = _string_set(delegation["operations"], f"{path}.delegation.operations", _managed_id, minimum=1)
    profiles = _string_set(
        delegation["execution_profiles"], f"{path}.delegation.execution_profiles", _profile_name, minimum=1
    )
    scope = _path_scope(delegation["path_scope"], f"{path}.delegation.path_scope", minimum=1)
    retry_raw = delegation["retry_limits"]
    if not isinstance(retry_raw, dict):
        _error("AEXCON006", f"{path}.delegation.retry_limits", "retry limits must be an object map")
    retries: dict[str, int] = {}
    for key, item in retry_raw.items():
        selected_key = _managed_id(key, f"{path}.delegation.retry_limits.{key}")
        retries[selected_key] = _integer(
            item, f"{path}.delegation.retry_limits.{key}", minimum=0, maximum=MAX_RETRY
        )
    if set(retries) != set(operations):
        _error("AEXCON007", f"{path}.delegation.retry_limits", "retry-limit keys must equal operations")
    stops = _string_set(delegation["stop_before"], f"{path}.delegation.stop_before", _managed_id)
    if not MANDATORY_STOPS.issubset(stops):
        _error("AEXCON012", f"{path}.delegation.stop_before", "mandatory accountable stop boundaries are missing")
    evidence = _object(root["evidence"], {"required_receipt", "required_paths"}, f"{path}.evidence")
    evidence_paths = _path_scope(evidence["required_paths"], f"{path}.evidence.required_paths")
    for item in evidence_paths:
        if not any(_path_within(item, parent) for parent in scope):
            _error("AEXCON010", f"{path}.evidence.required_paths", "required evidence is outside delegated path scope")
    return {
        "schema": AUTONOMY_ENVELOPE_SCHEMA,
        "selection": {
            "work_order": _work_order_id(selection["work_order"], f"{path}.selection.work_order"),
            "work_order_sha256": _sha256(selection["work_order_sha256"], f"{path}.selection.work_order_sha256"),
            "repository_state": _sha256(selection["repository_state"], f"{path}.selection.repository_state"),
            "evaluator_payload_sha256": _sha256(
                selection["evaluator_payload_sha256"], f"{path}.selection.evaluator_payload_sha256"
            ),
        },
        "delegation": {
            "asserted_by": _text(delegation["asserted_by"], f"{path}.delegation.asserted_by", maximum=512),
            "operations": operations,
            "path_scope": scope,
            "execution_profiles": profiles,
            "max_parallel_writers": _integer(
                delegation["max_parallel_writers"],
                f"{path}.delegation.max_parallel_writers",
                minimum=0,
                maximum=MAX_PARALLEL_WRITERS,
            ),
            "retry_limits": {key: retries[key] for key in sorted(retries, key=lambda item: item.encode("utf-8"))},
            "stop_before": stops,
        },
        "evidence": {
            "required_receipt": _boolean(evidence["required_receipt"], f"{path}.evidence.required_receipt"),
            "required_paths": evidence_paths,
        },
    }


def _validate_envelope_v2(value: Any, path: str = "$") -> dict[str, Any]:
    root = _object(value, {"schema", "selection", "delegation", "evidence", "authority"}, path)
    if root["schema"] != AUTONOMY_ENVELOPE_V2_SCHEMA:
        _error("AEXCON004", f"{path}.schema", "unsupported autonomy-envelope-v2 schema")
    v1 = _validate_envelope(
        {
            "schema": AUTONOMY_ENVELOPE_SCHEMA,
            "selection": root["selection"],
            "delegation": root["delegation"],
            "evidence": root["evidence"],
        },
        path,
    )
    if v1["delegation"]["max_parallel_writers"] != 1:
        _error("AEXCON012", f"{path}.delegation.max_parallel_writers", "v2 envelope requires one writer")
    authority = _object(
        root["authority"],
        {
            "decision_right",
            "delegate",
            "execution_profile",
            "delegation_sha256",
            "work_order_sha256",
            "expected_repository_state",
            "previous_receipt_sha256",
            "nonce",
            "issued_at",
            "not_after",
            "retry_ordinal",
        },
        f"{path}.authority",
    )
    decision_right = authority["decision_right"]
    if decision_right is not None:
        decision_right = _managed_id(decision_right, f"{path}.authority.decision_right")
    result = {
        "schema": AUTONOMY_ENVELOPE_V2_SCHEMA,
        "selection": v1["selection"],
        "delegation": v1["delegation"],
        "evidence": v1["evidence"],
        "authority": {
            "decision_right": decision_right,
            "delegate": _portable_id(authority["delegate"], f"{path}.authority.delegate"),
            "execution_profile": _profile_name(
                authority["execution_profile"], f"{path}.authority.execution_profile"
            ),
            "delegation_sha256": _sha256(
                authority["delegation_sha256"], f"{path}.authority.delegation_sha256"
            ),
            "work_order_sha256": _sha256(
                authority["work_order_sha256"], f"{path}.authority.work_order_sha256"
            ),
            "expected_repository_state": _sha256(
                authority["expected_repository_state"], f"{path}.authority.expected_repository_state"
            ),
            "previous_receipt_sha256": _nullable_sha256(
                authority["previous_receipt_sha256"], f"{path}.authority.previous_receipt_sha256"
            ),
            "nonce": _nonce(authority["nonce"], f"{path}.authority.nonce"),
            "issued_at": _utc_timestamp(authority["issued_at"], f"{path}.authority.issued_at"),
            "not_after": _utc_timestamp(authority["not_after"], f"{path}.authority.not_after"),
            "retry_ordinal": _integer(
                authority["retry_ordinal"], f"{path}.authority.retry_ordinal", minimum=0, maximum=3
            ),
        },
    }
    if result["selection"]["repository_state"] != result["authority"]["expected_repository_state"]:
        _error("AEXCON011", f"{path}.authority.expected_repository_state", "repository-state identities disagree")
    if result["selection"]["work_order_sha256"] != result["authority"]["work_order_sha256"]:
        _error("AEXCON011", f"{path}.authority.work_order_sha256", "work-order identities disagree")
    if result["authority"]["execution_profile"] not in result["delegation"]["execution_profiles"]:
        _error("AEXCON010", f"{path}.authority.execution_profile", "selected profile is outside delegation")
    if result["authority"]["retry_ordinal"] > min(result["delegation"]["retry_limits"].values()):
        _error("AEXCON010", f"{path}.authority.retry_ordinal", "retry ordinal exceeds delegated limit")
    if result["authority"]["not_after"] <= result["authority"]["issued_at"]:
        _error("AEXCON007", f"{path}.authority.not_after", "expiry must be later than issue time")
    issued = datetime.strptime(
        result["authority"]["issued_at"], "%Y-%m-%dT%H:%M:%SZ"
    ).replace(tzinfo=UTC)
    expiry = datetime.strptime(
        result["authority"]["not_after"], "%Y-%m-%dT%H:%M:%SZ"
    ).replace(tzinfo=UTC)
    if (expiry - issued).total_seconds() > 300:
        _error(
            "AEXCON007",
            f"{path}.authority.not_after",
            "v2 envelope lifetime exceeds five minutes",
        )
    return result


def _validate_evidence_binding(value: Any, path: str) -> dict[str, str]:
    item = _object(value, {"kind", "path", "sha256"}, path)
    return {
        "kind": _portable_id(item["kind"], f"{path}.kind"),
        "path": _path(item["path"], f"{path}.path"),
        "sha256": _sha256(item["sha256"], f"{path}.sha256"),
    }


def _validate_command_response(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict) or value.get("kind") not in {"command", "response"}:
        _error("AEXCON006", path, "value must be a command or response object")
    if value["kind"] == "command":
        item = _object(value, {"kind", "argv"}, path)
        argv = _sequence(item["argv"], f"{path}.argv", lambda part, part_path: _text(part, part_path))
        if not argv:
            _error("AEXCON006", f"{path}.argv", "command requires at least one argument")
        return {"kind": "command", "argv": argv}
    item = _object(value, {"kind", "value"}, path)
    return {"kind": "response", "value": _text(item["value"], f"{path}.value")}


def _validate_preview(value: Any, path: str, *, v1_empty: bool = False) -> dict[str, Any]:
    if v1_empty:
        return _object(value, set(), path)
    item = _object(value, {"kind", "artifact", "from_status", "to_status", "action", "target"}, path)
    kind = _enum(item["kind"], f"{path}.kind", {"none", "lifecycle-transition", "external-action"})
    if kind == "none":
        if any(item[name] is not None for name in ("artifact", "from_status", "to_status", "action", "target")):
            _error("AEXCON007", path, "none preview requires null detail fields")
    elif kind == "lifecycle-transition":
        if item["action"] is not None or item["target"] is not None:
            _error("AEXCON007", path, "lifecycle preview cannot contain external-action fields")
        _artifact_id(item["artifact"], f"{path}.artifact")
        _managed_id(item["from_status"], f"{path}.from_status")
        _managed_id(item["to_status"], f"{path}.to_status")
    else:
        if any(item[name] is not None for name in ("artifact", "from_status", "to_status")):
            _error("AEXCON007", path, "external-action preview cannot contain lifecycle fields")
        _text(item["action"], f"{path}.action", maximum=512)
        _text(item["target"], f"{path}.target", maximum=512)
    return dict(item)


def _validate_alternative(value: Any, path: str) -> dict[str, Any]:
    item = _object(
        value,
        {
            "summary",
            "procedure_id",
            "decision_right",
            "subject",
            "required_accountable_role",
            "recommendation",
            "command_or_suggested_response",
            "effects",
            "non_effects",
        },
        path,
    )
    return {
        "summary": _text(item["summary"], f"{path}.summary", maximum=512),
        "procedure_id": _managed_id(item["procedure_id"], f"{path}.procedure_id"),
        "decision_right": _managed_id(item["decision_right"], f"{path}.decision_right"),
        "subject": _text(item["subject"], f"{path}.subject"),
        "required_accountable_role": _managed_id(
            item["required_accountable_role"], f"{path}.required_accountable_role"
        ),
        "recommendation": _text(item["recommendation"], f"{path}.recommendation", maximum=512),
        "command_or_suggested_response": _validate_command_response(
            item["command_or_suggested_response"], f"{path}.command_or_suggested_response"
        ),
        "effects": _sequence(item["effects"], f"{path}.effects", lambda part, p: _text(part, p, maximum=512)),
        "non_effects": _sequence(
            item["non_effects"], f"{path}.non_effects", lambda part, p: _text(part, p, maximum=512)
        ),
    }


def _validate_packet_context(value: Any, path: str = "$") -> dict[str, Any]:
    root = _object(
        value,
        {
            "schema",
            "repository",
            "candidate_commit",
            "evaluator_payload_sha256",
            "evidence",
            "assumptions",
            "residual_uncertainty",
            "preview",
            "alternatives",
            "safe_to_defer",
        },
        path,
    )
    if root["schema"] != PACKET_CONTEXT_SCHEMA:
        _error("AEXCON004", f"{path}.schema", "unsupported decision-packet context schema")
    return {
        "schema": PACKET_CONTEXT_SCHEMA,
        "repository": _text(root["repository"], f"{path}.repository"),
        "candidate_commit": _nullable_text(root["candidate_commit"], f"{path}.candidate_commit", _git_object_id),
        "evaluator_payload_sha256": _nullable_text(
            root["evaluator_payload_sha256"], f"{path}.evaluator_payload_sha256", _sha256
        ),
        "evidence": _identity_set(root["evidence"], f"{path}.evidence", _validate_evidence_binding, "path"),
        "assumptions": _string_set(
            root["assumptions"], f"{path}.assumptions", lambda item, p: _text(item, p, maximum=512)
        ),
        "residual_uncertainty": _string_set(
            root["residual_uncertainty"],
            f"{path}.residual_uncertainty",
            lambda item, p: _text(item, p, maximum=512),
        ),
        "preview": _validate_preview(root["preview"], f"{path}.preview"),
        "alternatives": _sequence(root["alternatives"], f"{path}.alternatives", _validate_alternative),
        "safe_to_defer": _boolean(root["safe_to_defer"], f"{path}.safe_to_defer"),
    }


def _validate_predicate_evidence(value: Any, path: str) -> dict[str, str]:
    item = _object(value, {"kind", "reference"}, path)
    return {
        "kind": _portable_id(item["kind"], f"{path}.kind"),
        "reference": _text(item["reference"], f"{path}.reference"),
    }


def _validate_predicate(value: Any, path: str) -> dict[str, Any]:
    item = _object(value, {"id", "status", "evidence", "message"}, path)
    return {
        "id": _managed_id(item["id"], f"{path}.id"),
        "status": _enum(item["status"], f"{path}.status", {"pass", "fail", "not_assessable"}),
        "evidence": _sequence(item["evidence"], f"{path}.evidence", _validate_predicate_evidence),
        "message": _text(item["message"], f"{path}.message"),
    }


def _validate_gate(value: Any, path: str) -> dict[str, Any]:
    item = _object(value, {"id", "status", "predicates"}, path)
    return {
        "id": _managed_id(item["id"], f"{path}.id"),
        "status": _enum(item["status"], f"{path}.status", {"pass", "fail", "not_assessable"}),
        "predicates": _sequence(item["predicates"], f"{path}.predicates", _validate_predicate),
    }


def _validate_packet_finding(value: Any, path: str) -> dict[str, Any]:
    item = _object(value, {"scope", "code", "path", "message", "plane"}, path)
    return {
        "scope": _enum(item["scope"], f"{path}.scope", {"selected", "repository"}),
        "code": _diagnostic_id(item["code"], f"{path}.code"),
        "path": None if item["path"] is None else _text(item["path"], f"{path}.path", maximum=512),
        "message": _text(item["message"], f"{path}.message"),
        "plane": None if item["plane"] is None else _text(item["plane"], f"{path}.plane", maximum=512),
    }


def _validate_projection_context(value: Any, path: str) -> dict[str, Any]:
    item = _object(
        value,
        {
            "selected_artifact",
            "lifecycle_state",
            "governing",
            "dependencies",
            "declared_paths",
            "changed_paths",
            "change_set_complete",
            "procedure_id",
            "procedure_step_id",
        },
        path,
    )
    return {
        "selected_artifact": _artifact_id(item["selected_artifact"], f"{path}.selected_artifact"),
        "lifecycle_state": _managed_id(item["lifecycle_state"], f"{path}.lifecycle_state"),
        "governing": _string_set(item["governing"], f"{path}.governing", _artifact_id),
        "dependencies": _string_set(item["dependencies"], f"{path}.dependencies", _artifact_id),
        "declared_paths": _path_scope(item["declared_paths"], f"{path}.declared_paths"),
        "changed_paths": _string_set(item["changed_paths"], f"{path}.changed_paths", _path, paths=True),
        "change_set_complete": _boolean(item["change_set_complete"], f"{path}.change_set_complete"),
        "procedure_id": _managed_id(item["procedure_id"], f"{path}.procedure_id"),
        "procedure_step_id": _managed_id(item["procedure_step_id"], f"{path}.procedure_step_id"),
    }


def _validate_packet(value: Any, path: str = "$") -> dict[str, Any]:
    if not isinstance(value, dict):
        _error("AEXCON006", path, "decision packet must be an object")
    schema = value.get("schema")
    expected = {"schema", "decision", "identity", "assessment", "effect", "handoff"}
    if schema == PACKET_V2_SCHEMA:
        expected.add("context")
    elif schema != PACKET_V1_SCHEMA:
        _error("AEXCON004", f"{path}.schema", "unsupported decision-packet schema")
    root = _object(value, expected, path)
    decision = _object(
        root["decision"],
        {"kind", "subject", "required_accountable_role", "recommendation", "alternatives"},
        f"{path}.decision",
    )
    identity = _object(
        root["identity"], {"repository", "candidate_commit", "evaluator_payload_sha256"}, f"{path}.identity"
    )
    assessment = _object(
        root["assessment"],
        {"gates", "evidence", "findings", "assumptions", "residual_uncertainty"},
        f"{path}.assessment",
    )
    effect = _object(root["effect"], {"preview", "effects", "non_effects"}, f"{path}.effect")
    handoff = _object(root["handoff"], {"command_or_suggested_response", "safe_to_defer"}, f"{path}.handoff")
    result: dict[str, Any] = {"schema": schema}
    if schema == PACKET_V2_SCHEMA:
        result["context"] = _validate_projection_context(root["context"], f"{path}.context")
    result.update(
        {
            "decision": {
                "kind": _managed_id(decision["kind"], f"{path}.decision.kind"),
                "subject": _text(decision["subject"], f"{path}.decision.subject"),
                "required_accountable_role": _managed_id(
                    decision["required_accountable_role"], f"{path}.decision.required_accountable_role"
                ),
                "recommendation": _text(
                    decision["recommendation"], f"{path}.decision.recommendation", maximum=512
                ),
                "alternatives": _sequence(
                    decision["alternatives"], f"{path}.decision.alternatives", _validate_alternative
                ),
            },
            "identity": {
                "repository": _text(identity["repository"], f"{path}.identity.repository"),
                "candidate_commit": _nullable_text(
                    identity["candidate_commit"], f"{path}.identity.candidate_commit", _git_object_id
                ),
                "evaluator_payload_sha256": _nullable_text(
                    identity["evaluator_payload_sha256"], f"{path}.identity.evaluator_payload_sha256", _sha256
                ),
            },
            "assessment": {
                "gates": _sequence(assessment["gates"], f"{path}.assessment.gates", _validate_gate),
                "evidence": _identity_set(
                    assessment["evidence"], f"{path}.assessment.evidence", _validate_evidence_binding, "path"
                ),
                "findings": _sequence(
                    assessment["findings"], f"{path}.assessment.findings", _validate_packet_finding
                ),
                "assumptions": _string_set(
                    assessment["assumptions"],
                    f"{path}.assessment.assumptions",
                    lambda item, p: _text(item, p, maximum=512),
                ),
                "residual_uncertainty": _string_set(
                    assessment["residual_uncertainty"],
                    f"{path}.assessment.residual_uncertainty",
                    lambda item, p: _text(item, p, maximum=512),
                ),
            },
            "effect": {
                "preview": _validate_preview(
                    effect["preview"], f"{path}.effect.preview", v1_empty=schema == PACKET_V1_SCHEMA
                ),
                "effects": _sequence(
                    effect["effects"], f"{path}.effect.effects", lambda item, p: _text(item, p, maximum=512)
                ),
                "non_effects": _sequence(
                    effect["non_effects"],
                    f"{path}.effect.non_effects",
                    lambda item, p: _text(item, p, maximum=512),
                ),
            },
            "handoff": {
                "command_or_suggested_response": _validate_command_response(
                    handoff["command_or_suggested_response"],
                    f"{path}.handoff.command_or_suggested_response",
                ),
                "safe_to_defer": _boolean(handoff["safe_to_defer"], f"{path}.handoff.safe_to_defer"),
            },
        }
    )
    if schema == PACKET_V2_SCHEMA and result["context"]["selected_artifact"] != result["decision"]["subject"]:
        _error("AEXCON014", f"{path}.context.selected_artifact", "packet context and decision subject differ")
    return result


def _validate_receipt_evidence(value: Any, path: str) -> dict[str, str]:
    if not isinstance(value, dict):
        _error("AEXCON006", path, "evidence entry must be an object")
    if set(value) == {"kind", "sha256"}:
        return {
            "kind": _portable_id(value["kind"], f"{path}.kind"),
            "sha256": _sha256(value["sha256"], f"{path}.sha256"),
        }
    item = _object(value, {"kind", "path", "sha256"}, path)
    return {
        "kind": _portable_id(item["kind"], f"{path}.kind"),
        "path": _path(item["path"], f"{path}.path"),
        "sha256": _sha256(item["sha256"], f"{path}.sha256"),
    }


def _validate_skill(value: Any, path: str) -> dict[str, str]:
    item = _object(value, {"name", "version", "portable_core_sha256"}, path)
    return {
        "name": _profile_name(item["name"], f"{path}.name"),
        "version": _semantic_version(item["version"], f"{path}.version"),
        "portable_core_sha256": _sha256(item["portable_core_sha256"], f"{path}.portable_core_sha256"),
    }


def _validate_operation(value: Any, path: str, *, phase1: bool) -> dict[str, Any]:
    if phase1:
        item = _object(value, {"id", "status", "exit_code"}, path)
        status = _enum(item["status"], f"{path}.status", {"passed", "failed"})
        return {
            "id": _managed_id(item["id"], f"{path}.id"),
            "status": status,
            "exit_code": None
            if item["exit_code"] is None
            else _integer(item["exit_code"], f"{path}.exit_code", minimum=-MAX_INTEGER, maximum=MAX_INTEGER),
        }
    item = _object(
        value,
        {"id", "status", "exit_code", "arguments_sha256", "output_sha256", "evidence_path"},
        path,
    )
    return {
        "id": _managed_id(item["id"], f"{path}.id"),
        "status": _enum(
            item["status"],
            f"{path}.status",
            {"passed", "failed", "timed-out", "cancelled", "missing-output", "not-assessable"},
        ),
        "exit_code": None
        if item["exit_code"] is None
        else _integer(item["exit_code"], f"{path}.exit_code", minimum=-MAX_INTEGER, maximum=MAX_INTEGER),
        "arguments_sha256": _nullable_text(item["arguments_sha256"], f"{path}.arguments_sha256", _sha256),
        "output_sha256": _nullable_text(item["output_sha256"], f"{path}.output_sha256", _sha256),
        "evidence_path": None
        if item["evidence_path"] is None
        else _path(item["evidence_path"], f"{path}.evidence_path"),
    }


def _validate_worker(value: Any, path: str) -> dict[str, Any]:
    item = _object(value, {"id", "profile", "status", "operation_ids", "changed_paths", "evidence"}, path)
    return {
        "id": _portable_id(item["id"], f"{path}.id"),
        "profile": _profile_name(item["profile"], f"{path}.profile"),
        "status": _enum(
            item["status"],
            f"{path}.status",
            {"completed", "degraded", "failed", "timed-out", "cancelled", "missing-output"},
        ),
        "operation_ids": _sequence(item["operation_ids"], f"{path}.operation_ids", _managed_id),
        "changed_paths": _string_set(
            item["changed_paths"], f"{path}.changed_paths", _path, paths=True
        ),
        "evidence": sorted(
            _sequence(item["evidence"], f"{path}.evidence", _validate_receipt_evidence),
            key=lambda entry: canonical_json_bytes(entry),
        ),
    }


def _validate_state_entry(value: Any, path: str) -> dict[str, str]:
    item = _object(value, {"kind", "sha256"}, path)
    return {
        "kind": _portable_id(item["kind"], f"{path}.kind"),
        "sha256": _sha256(item["sha256"], f"{path}.sha256"),
    }


def _validate_evaluator(value: Any, path: str, *, outcome: str, envelope_bound: bool) -> dict[str, str]:
    if not isinstance(value, dict):
        _error("AEXCON006", path, "evaluator identity must be an object")
    if not value:
        if outcome != "failed":
            _error("AEXCON015", path, "empty evaluator identity is valid only for failed receipts")
        return {}
    expected = {"identity", "version", "payload_sha256"} if "payload_sha256" in value else {"identity", "version"}
    item = _object(value, expected, path)
    if envelope_bound and "payload_sha256" not in item:
        _error("AEXCON015", path, "envelope-bound receipt requires evaluator payload identity")
    result = {
        "identity": _text(item["identity"], f"{path}.identity"),
        "version": _semantic_version(item["version"], f"{path}.version"),
    }
    if "payload_sha256" in item:
        result["payload_sha256"] = _sha256(item["payload_sha256"], f"{path}.payload_sha256")
    return result


def _validate_deviation(value: Any, path: str, *, phase1: bool) -> dict[str, Any]:
    if not isinstance(value, dict):
        _error("AEXCON006", path, "deviation must be an object")
    full = {"code", "operation", "status", "message", "evidence_path", "details_sha256"}
    if set(value) == full:
        item = _object(value, full, path)
        return {
            "code": _diagnostic_id(item["code"], f"{path}.code"),
            "operation": None if item["operation"] is None else _managed_id(item["operation"], f"{path}.operation"),
            "status": None if item["status"] is None else _managed_id(item["status"], f"{path}.status"),
            "message": None if item["message"] is None else _text(item["message"], f"{path}.message", maximum=512),
            "evidence_path": None
            if item["evidence_path"] is None
            else _path(item["evidence_path"], f"{path}.evidence_path"),
            "details_sha256": _nullable_text(item["details_sha256"], f"{path}.details_sha256", _sha256),
        }
    legacy_sets = (
        {"code", "diagnostics", "operation"},
        {"code", "expected", "observed", "operation"},
        {"code", "message", "operation"},
        {"code", "errors", "operation"},
        {"code", "operation", "status"},
        {"code", "operation", "ready"},
        {"code", "changed_paths"},
        {"code", "message"},
    )
    if not phase1 or set(value) not in legacy_sets:
        _error("AEXCON015", path, "deviation does not match a permitted receipt variant")
    # Legacy fields are compatibility evidence.  Validate all values as bounded
    # JSON and retain their exact field set without inventing a new variant.
    _diagnostic_id(value["code"], f"{path}.code")
    for key, item in value.items():
        if key == "changed_paths":
            _string_set(item, f"{path}.{key}", _path, paths=True)
        elif key == "diagnostics":
            _sequence(item, f"{path}.{key}", lambda part, p: _text(part, p, maximum=512))
        elif key == "ready":
            _boolean(item, f"{path}.{key}")
        elif key != "code":
            _bounded_walk(item, path=f"{path}.{key}")
    return dict(value)


def _validate_receipt(value: Any, path: str = "$") -> dict[str, Any]:
    root = _object(value, {"schema", "selection", "execution", "effects", "validation"}, path)
    if root["schema"] != RECEIPT_SCHEMA:
        _error("AEXCON004", f"{path}.schema", "unsupported execution-receipt schema")
    selection = _object(
        root["selection"], {"repository", "artifact", "autonomy_envelope_sha256"}, f"{path}.selection"
    )
    execution = _object(
        root["execution"], {"profiles", "skills", "operations", "worker_results"}, f"{path}.execution"
    )
    profiles = _string_set(execution["profiles"], f"{path}.execution.profiles", _profile_name, minimum=1)
    envelope_digest = _nullable_text(
        selection["autonomy_envelope_sha256"], f"{path}.selection.autonomy_envelope_sha256", _sha256
    )
    phase1 = profiles == ["single-agent-orientation"] and envelope_digest is None
    operations = _sequence(
        execution["operations"],
        f"{path}.execution.operations",
        lambda item, item_path: _validate_operation(item, item_path, phase1=phase1),
    )
    operation_ids = [item["id"] for item in operations]
    if len(set(operation_ids)) != len(operation_ids):
        _error("AEXCON003", f"{path}.execution.operations", "duplicate operation ID")
    workers = _identity_set(execution["worker_results"], f"{path}.execution.worker_results", _validate_worker, "id")
    for worker in workers:
        if any(item not in operation_ids for item in worker["operation_ids"]):
            _error("AEXCON015", f"{path}.execution.worker_results", "worker references an unknown operation")
    effects = _object(
        root["effects"], {"changed_paths", "evidence", "state_before", "state_after"}, f"{path}.effects"
    )
    before = _sequence(effects["state_before"], f"{path}.effects.state_before", _validate_state_entry)
    after = _sequence(effects["state_after"], f"{path}.effects.state_after", _validate_state_entry)
    if len({item["kind"] for item in before}) != len(before) or len({item["kind"] for item in after}) != len(after):
        _error("AEXCON003", f"{path}.effects", "state chain contains a duplicate kind")
    if [item["kind"] for item in before] != [item["kind"] for item in after]:
        _error("AEXCON015", f"{path}.effects", "before and after state kinds do not form a complete chain")
    validation = _object(
        root["validation"], {"evaluator", "gates", "outcome", "deviations", "residual_uncertainty"}, f"{path}.validation"
    )
    outcome = _enum(validation["outcome"], f"{path}.validation.outcome", {"completed", "degraded", "stopped", "failed"})
    result = {
        "schema": RECEIPT_SCHEMA,
        "selection": {
            "repository": None
            if selection["repository"] is None
            else _text(selection["repository"], f"{path}.selection.repository"),
            "artifact": None
            if selection["artifact"] is None
            else _artifact_id(selection["artifact"], f"{path}.selection.artifact"),
            "autonomy_envelope_sha256": envelope_digest,
        },
        "execution": {
            "profiles": profiles,
            "skills": _identity_set(execution["skills"], f"{path}.execution.skills", _validate_skill, "name"),
            "operations": operations,
            "worker_results": workers,
        },
        "effects": {
            "changed_paths": _string_set(
                effects["changed_paths"], f"{path}.effects.changed_paths", _path, paths=True
            ),
            "evidence": sorted(
                _sequence(effects["evidence"], f"{path}.effects.evidence", _validate_receipt_evidence),
                key=canonical_json_bytes,
            ),
            "state_before": before,
            "state_after": after,
        },
        "validation": {
            "evaluator": _validate_evaluator(
                validation["evaluator"],
                f"{path}.validation.evaluator",
                outcome=outcome,
                envelope_bound=envelope_digest is not None,
            ),
            "gates": _sequence(validation["gates"], f"{path}.validation.gates", _validate_gate),
            "outcome": outcome,
            "deviations": _sequence(
                validation["deviations"],
                f"{path}.validation.deviations",
                lambda item, item_path: _validate_deviation(item, item_path, phase1=phase1),
            ),
            "residual_uncertainty": _string_set(
                validation["residual_uncertainty"],
                f"{path}.validation.residual_uncertainty",
                lambda item, p: _text(item, p, maximum=512),
            ),
        },
    }
    if envelope_digest is not None and any("path" not in item for item in result["effects"]["evidence"]):
        _error("AEXCON015", f"{path}.effects.evidence", "envelope-bound evidence must use retained paths")
    changed_paths = set(result["effects"]["changed_paths"])
    evidence_entries = {canonical_json_bytes(item) for item in result["effects"]["evidence"]}
    for worker in result["execution"]["worker_results"]:
        if not set(worker["changed_paths"]).issubset(changed_paths):
            _error("AEXCON015", f"{path}.execution.worker_results", "worker changed path is absent from aggregate effects")
        if not {canonical_json_bytes(item) for item in worker["evidence"]}.issubset(evidence_entries):
            _error("AEXCON015", f"{path}.execution.worker_results", "worker evidence is absent from aggregate effects")
    operation_statuses = {item["status"] for item in result["execution"]["operations"]}
    worker_statuses = {item["status"] for item in result["execution"]["worker_results"]}
    if outcome == "completed" and (
        not operation_statuses.issubset({"passed"}) or not worker_statuses.issubset({"completed"})
    ):
        _error("AEXCON015", f"{path}.validation.outcome", "completed receipt hides incomplete or unsuccessful work")
    if outcome == "degraded" and (
        operation_statuses & {"failed", "timed-out", "cancelled", "missing-output"}
        or worker_statuses & {"failed", "timed-out", "cancelled", "missing-output"}
    ):
        _error("AEXCON015", f"{path}.validation.outcome", "degraded receipt hides failed or missing work")
    return result


def _validate_profile(value: Any, path: str = "$") -> dict[str, Any]:
    root = _object(
        value,
        {
            "schema",
            "name",
            "purpose",
            "operation_classes",
            "default_mutation_class",
            "prohibited_decisions",
            "prohibited_actions",
            "required_skill_capabilities",
            "input_schemas",
            "result_schemas",
            "runtime_characteristics",
            "single_agent_fallback",
        },
        path,
    )
    if root["schema"] != PROFILE_SCHEMA:
        _error("AEXCON004", f"{path}.schema", "unsupported logical execution profile schema")
    prohibited = _string_set(root["prohibited_decisions"], f"{path}.prohibited_decisions", _managed_id)
    if not MANDATORY_STOPS.issubset(prohibited):
        _error("AEXCON017", f"{path}.prohibited_decisions", "mandatory accountable decisions are not prohibited")
    characteristics = _string_set(
        root["runtime_characteristics"], f"{path}.runtime_characteristics", _portable_id
    )
    for item in characteristics:
        if any(marker in item.split("-") for marker in _PROVIDER_MARKERS):
            _error("AEXCON017", f"{path}.runtime_characteristics", "provider-bound runtime characteristic")
    if _boolean(root["single_agent_fallback"], f"{path}.single_agent_fallback") is not True:
        _error("AEXCON017", f"{path}.single_agent_fallback", "single-agent fallback is required")
    return {
        "schema": PROFILE_SCHEMA,
        "name": _profile_name(root["name"], f"{path}.name"),
        "purpose": _text(root["purpose"], f"{path}.purpose"),
        "operation_classes": _string_set(
            root["operation_classes"], f"{path}.operation_classes", _managed_id, minimum=1
        ),
        "default_mutation_class": _enum(
            root["default_mutation_class"],
            f"{path}.default_mutation_class",
            {"read-only", "draft-writing", "governed-mutation", "external-action"},
        ),
        "prohibited_decisions": prohibited,
        "prohibited_actions": _string_set(
            root["prohibited_actions"], f"{path}.prohibited_actions", _managed_id
        ),
        "required_skill_capabilities": _string_set(
            root["required_skill_capabilities"], f"{path}.required_skill_capabilities", _portable_id
        ),
        "input_schemas": _string_set(root["input_schemas"], f"{path}.input_schemas", _portable_id),
        "result_schemas": _string_set(root["result_schemas"], f"{path}.result_schemas", _portable_id),
        "runtime_characteristics": characteristics,
        "single_agent_fallback": True,
    }


_VALIDATORS = {
    AUTONOMY_ENVELOPE_SCHEMA: _validate_envelope,
    AUTONOMY_ENVELOPE_V2_SCHEMA: _validate_envelope_v2,
    DELEGATION_SCHEMA: _validate_agentic_delegation,
    PACKET_CONTEXT_SCHEMA: _validate_packet_context,
    PACKET_V1_SCHEMA: _validate_packet,
    PACKET_V2_SCHEMA: _validate_packet,
    RECEIPT_SCHEMA: _validate_receipt,
    PROFILE_SCHEMA: _validate_profile,
    REPOSITORY_STATE_SCHEMA: _validate_repository_state,
    REPOSITORY_OBSERVATION_SCHEMA: _validate_repository_observation,
    WORKTREE_STATE_SCHEMA: _validate_worktree_state,
}


def validate_contract(value: Any, *, expected_schema: str | None = None) -> ContractDocument:
    """Strictly validate and canonically encode one supported contract object."""

    if not isinstance(value, dict):
        _error("AEXCON006", "$", "contract root must be an object")
    schema = value.get("schema")
    if expected_schema is not None and schema != expected_schema:
        _error("AEXCON004", "$.schema", "contract schema does not match the expected schema")
    validator = _VALIDATORS.get(schema)
    if validator is None:
        _error("AEXCON004", "$.schema", "unsupported contract schema identifier")
    return _document(validator(value))


def parse_contract_bytes(raw: bytes, *, expected_schema: str | None = None) -> ContractDocument:
    """Parse, validate, normalize, and identify one supported contract document."""

    if expected_schema == WORKTREE_STATE_SCHEMA:
        value = _parse_json_bytes(raw, document_limit=MANIFEST_MAX_BYTES, array_limit=WORKTREE_MAX_ENTRIES)
    else:
        value = parse_json_bytes(raw)
    return validate_contract(value, expected_schema=expected_schema)


_DEFINITION_FIELDS = {
    "name",
    "kind",
    "fields",
    "variants",
    "element",
    "key_type",
    "value_type",
    "enum",
    "pattern",
    "minimum",
    "maximum",
    "collection",
    "identity_field",
    "ordering",
    "max_items",
    "max_bytes",
}


def parse_agent_contract_catalog_bytes(raw: bytes) -> ContractDocument:
    """Validate the closed v1 declarative catalog and return its identity."""

    value = parse_json_bytes(raw)
    root = _object(value, {"schema", "canonical_encoding", "schemas", "definitions", "diagnostics", "bounds"}, "$")
    if root["schema"] != CATALOG_SCHEMA or root["canonical_encoding"] != CANONICAL_JSON_SCHEMA:
        _error("AEXCON004", "$.schema", "unsupported agent contract catalog or canonical encoding")
    schemas = _sequence(
        root["schemas"],
        "$.schemas",
        lambda item, path: _object(item, {"id", "root", "compatibility"}, path),
    )
    expected_schemas = [
        {"id": schema_id, "root": SCHEMA_ROOTS[schema_id], "compatibility": "fail-closed"}
        for schema_id in sorted(SCHEMA_ROOTS, key=lambda item: item.encode("utf-8"))
    ]
    if schemas != expected_schemas:
        _error("AEXCON009", "$.schemas", "schema records differ from the closed ordered v1 catalog")
    definitions = _array(root["definitions"], "$.definitions")
    names: list[str] = []
    for index, definition in enumerate(definitions):
        path = f"$.definitions[{index}]"
        item = _object(definition, _DEFINITION_FIELDS, path)
        names.append(_portable_id(item["name"], f"{path}.name"))
        kind = _enum(
            item["kind"],
            f"{path}.kind",
            {"object", "array", "map", "string", "integer", "boolean", "null", "union"},
        )
        collection = _enum(
            item["collection"], f"{path}.collection", {"scalar", "sequence", "set", "identity-set", "map"}
        )
        ordering = _enum(item["ordering"], f"{path}.ordering", {"none", "source", "utf8", "key-utf8"})
        fields = _array(item["fields"], f"{path}.fields")
        field_names: list[str] = []
        for field_index, field in enumerate(fields):
            field_path = f"{path}.fields[{field_index}]"
            field_item = _object(field, {"name", "type", "required"}, field_path)
            field_names.append(_portable_id(field_item["name"], f"{field_path}.name"))
            _portable_id(field_item["type"], f"{field_path}.type")
            if _boolean(field_item["required"], f"{field_path}.required") is not True:
                _error("AEXCON009", f"{field_path}.required", "all v1 catalog fields are required")
        if field_names != sorted(field_names, key=lambda value: value.encode("utf-8")) or len(field_names) != len(set(field_names)):
            _error("AEXCON009", f"{path}.fields", "object fields must be unique and UTF-8 ordered")
        variants = _string_set(item["variants"], f"{path}.variants", _portable_id)
        enum_values = _string_set(item["enum"], f"{path}.enum", lambda value, value_path: _text(value, value_path))
        for name in ("element", "key_type", "value_type", "identity_field"):
            if item[name] is not None:
                _portable_id(item[name], f"{path}.{name}")
        if item["pattern"] is not None:
            _text(item["pattern"], f"{path}.pattern")
        for name in ("minimum", "maximum", "max_items", "max_bytes"):
            if item[name] is not None:
                _integer(item[name], f"{path}.{name}", minimum=-MAX_INTEGER, maximum=MAX_INTEGER)
        if item["minimum"] is not None and item["maximum"] is not None and item["minimum"] > item["maximum"]:
            _error("AEXCON009", path, "definition minimum exceeds maximum")

        empty_common = not fields and not variants and item["element"] is None and item["key_type"] is None and item["value_type"] is None
        if kind == "object":
            valid_shape = (
                not variants
                and item["element"] is None
                and item["key_type"] is None
                and item["value_type"] is None
                and not enum_values
                and item["pattern"] is None
                and item["minimum"] is None
                and item["maximum"] is None
                and collection == "scalar"
                and item["identity_field"] is None
                and ordering == "none"
                and item["max_items"] is None
                and item["max_bytes"] is None
            )
        elif kind == "array":
            valid_shape = (
                not fields
                and not variants
                and item["element"] is not None
                and item["key_type"] is None
                and item["value_type"] is None
                and not enum_values
                and item["pattern"] is None
                and item["maximum"] is None
                and collection in {"sequence", "set", "identity-set"}
                and ordering == ("source" if collection == "sequence" else "utf8")
                and ((collection == "identity-set") == (item["identity_field"] is not None))
                and item["max_items"] is not None
                and item["max_bytes"] is None
            )
        elif kind == "map":
            valid_shape = (
                not fields
                and not variants
                and item["element"] is None
                and item["key_type"] is not None
                and item["value_type"] is not None
                and not enum_values
                and item["pattern"] is None
                and item["minimum"] is None
                and item["maximum"] is None
                and collection == "map"
                and item["identity_field"] is None
                and ordering == "key-utf8"
                and item["max_items"] is not None
                and item["max_bytes"] is None
            )
        elif kind == "string":
            valid_shape = (
                empty_common
                and collection == "scalar"
                and item["identity_field"] is None
                and ordering == "none"
                and item["minimum"] is None
                and item["maximum"] is None
                and item["max_items"] is None
            )
        elif kind == "integer":
            valid_shape = (
                empty_common
                and not enum_values
                and item["pattern"] is None
                and collection == "scalar"
                and item["identity_field"] is None
                and ordering == "none"
                and item["max_items"] is None
                and item["max_bytes"] is None
            )
        elif kind in {"boolean", "null"}:
            valid_shape = (
                empty_common
                and not enum_values
                and item["pattern"] is None
                and item["minimum"] is None
                and item["maximum"] is None
                and collection == "scalar"
                and item["identity_field"] is None
                and ordering == "none"
                and item["max_items"] is None
                and item["max_bytes"] is None
            )
        else:
            valid_shape = (
                not fields
                and bool(variants)
                and item["element"] is None
                and item["key_type"] is None
                and item["value_type"] is None
                and not enum_values
                and item["pattern"] is None
                and item["minimum"] is None
                and item["maximum"] is None
                and collection == "scalar"
                and item["identity_field"] is None
                and ordering == "none"
                and item["max_items"] is None
                and item["max_bytes"] is None
            )
        if not valid_shape:
            _error("AEXCON009", path, "definition uses properties outside its declared kind")
        _bounded_walk(item, path=path)
    if names != sorted(names, key=lambda item: item.encode("utf-8")) or len(names) != len(set(names)):
        _error("AEXCON009", "$.definitions", "definition names must be unique and UTF-8 ordered")
    references = set(SCHEMA_ROOTS.values())
    for definition in definitions:
        references.update(field["type"] for field in definition["fields"])
        references.update(definition["variants"])
        references.update(
            item
            for item in (definition["element"], definition["key_type"], definition["value_type"])
            if item is not None
        )
    if references != set(names):
        _error("AEXCON007", "$.definitions", "definition references are unresolved or include unused types")
    diagnostics = _sequence(
        root["diagnostics"],
        "$.diagnostics",
        lambda item, path: _object(item, {"code", "class"}, path),
    )
    expected_diagnostics = [{"code": code, "class": description} for code, description in DIAGNOSTICS.items()]
    if diagnostics != expected_diagnostics:
        _error("AEXCON009", "$.diagnostics", "diagnostic table differs from the closed v1 table")
    bounds = _object(
        root["bounds"],
        {
            "max_document_bytes",
            "max_nesting",
            "max_object_members",
            "max_array_entries",
            "max_string_scalars",
            "max_path_bytes",
            "max_collection_entries",
            "max_parallel_writers",
            "max_retry",
            "worktree_max_entries",
            "formal_max_artifacts",
            "file_max_bytes",
            "observation_max_file_bytes",
            "manifest_max_bytes",
        },
        "$.bounds",
    )
    expected_bounds = {
        "max_document_bytes": 1_048_576,
        "max_nesting": 32,
        "max_object_members": 1_024,
        "max_array_entries": 1_024,
        "max_string_scalars": 16_384,
        "max_path_bytes": 1_024,
        "max_collection_entries": 1_024,
        "max_parallel_writers": 32,
        "max_retry": 10,
        "worktree_max_entries": 100_000,
        "formal_max_artifacts": 16_384,
        "file_max_bytes": 1_073_741_824,
        "observation_max_file_bytes": 8_589_934_592,
        "manifest_max_bytes": 67_108_864,
    }
    if bounds != expected_bounds:
        _error("AEXCON009", "$.bounds", "catalog bounds differ from SPEC-AEX-003")
    document = _document(root)
    if document.canonical_bytes != raw:
        _error("AEXCON009", "$", "catalog bytes are not canonical JSON")
    return document


def construct_repository_state_binding(
    worktree_state: Mapping[str, Any], governance: Mapping[str, Any]
) -> ContractDocument:
    """Build a repository-state candidate from complete supplied observations."""

    worktree = validate_contract(worktree_state, expected_schema=WORKTREE_STATE_SCHEMA)
    governance_value = _object(
        governance,
        {"formal_snapshot_sha256", "managed_lock_sha256", "work_order", "work_order_sha256"},
        "$.governance",
    )
    value = {
        "schema": REPOSITORY_STATE_SCHEMA,
        "repository": {
            "git_object_format": worktree.value["git_object_format"],
            "head": worktree.value["head"],
            "tree": worktree.value["tree"],
            "worktree_state_sha256": worktree.sha256,
        },
        "governance": dict(governance_value),
    }
    return validate_contract(value, expected_schema=REPOSITORY_STATE_SCHEMA)


def _scope_intersection(requested: Sequence[str], managed: Sequence[str]) -> list[str]:
    result: set[str] = set()
    for request in requested:
        for maximum in managed:
            if _path_within(request, maximum):
                result.add(request)
            elif _path_within(maximum, request):
                result.add(maximum)
    return sorted(result, key=lambda item: item.encode("utf-8"))


def _assert_narrower(child: Mapping[str, Any], parent: Mapping[str, Any]) -> None:
    if child["selection"] != parent["selection"]:
        _error("AEXCON011", "$.selection", "child selection differs from parent identity")
    child_delegation = child["delegation"]
    parent_delegation = parent["delegation"]
    if child_delegation["asserted_by"] != parent_delegation["asserted_by"]:
        _error("AEXCON012", "$.delegation.asserted_by", "child changed the actor assertion")
    if not set(child_delegation["operations"]).issubset(parent_delegation["operations"]):
        _error("AEXCON010", "$.delegation.operations", "child added an operation")
    if not set(child_delegation["execution_profiles"]).issubset(parent_delegation["execution_profiles"]):
        _error("AEXCON010", "$.delegation.execution_profiles", "child added an execution profile")
    if child_delegation["max_parallel_writers"] > parent_delegation["max_parallel_writers"]:
        _error("AEXCON010", "$.delegation.max_parallel_writers", "child increased the writer limit")
    for item in child_delegation["path_scope"]:
        if not any(_path_within(item, maximum) for maximum in parent_delegation["path_scope"]):
            _error("AEXCON010", "$.delegation.path_scope", "child path is outside parent scope")
    for operation, retry in child_delegation["retry_limits"].items():
        if retry > parent_delegation["retry_limits"].get(operation, -1):
            _error("AEXCON010", "$.delegation.retry_limits", "child increased a retry limit")
    if not set(parent_delegation["stop_before"]).issubset(child_delegation["stop_before"]):
        _error("AEXCON010", "$.delegation.stop_before", "child removed a stop boundary")
    if parent["evidence"]["required_receipt"] and not child["evidence"]["required_receipt"]:
        _error("AEXCON010", "$.evidence.required_receipt", "child removed the receipt obligation")
    if not set(parent["evidence"]["required_paths"]).issubset(child["evidence"]["required_paths"]):
        _error("AEXCON010", "$.evidence.required_paths", "child removed an evidence obligation")


def narrow_autonomy_envelope(parent: Mapping[str, Any], child: Mapping[str, Any]) -> ContractDocument:
    """Validate that a child envelope is equal to or narrower than its parent."""

    parent_doc = validate_contract(parent, expected_schema=AUTONOMY_ENVELOPE_SCHEMA)
    child_doc = validate_contract(child, expected_schema=AUTONOMY_ENVELOPE_SCHEMA)
    _assert_narrower(child_doc.value, parent_doc.value)
    return child_doc


def construct_envelope_candidate(
    *,
    state_binding: Mapping[str, Any],
    evaluator_payload_sha256: str,
    procedure_id: str,
    request: Mapping[str, Any],
    managed_scope: Mapping[str, Any],
    parent: Mapping[str, Any] | None = None,
    parent_sha256: str | None = None,
) -> EnvelopeConstruction:
    """Intersect a requested delegation with supplied maximum managed scope."""

    state = validate_contract(state_binding, expected_schema=REPOSITORY_STATE_SCHEMA)
    request_value = _object(request, {"delegation", "evidence"}, "$.request")
    managed_value = _object(managed_scope, {"delegation", "evidence"}, "$.managed_scope")
    # Validate both scopes by embedding them into complete temporary envelopes.
    selection = {
        "work_order": state.value["governance"]["work_order"],
        "work_order_sha256": state.value["governance"]["work_order_sha256"],
        "repository_state": state.sha256,
        "evaluator_payload_sha256": _sha256(evaluator_payload_sha256, "$.evaluator_payload_sha256"),
    }
    request_doc = validate_contract(
        {"schema": AUTONOMY_ENVELOPE_SCHEMA, "selection": selection, **request_value},
        expected_schema=AUTONOMY_ENVELOPE_SCHEMA,
    )
    managed_doc = validate_contract(
        {"schema": AUTONOMY_ENVELOPE_SCHEMA, "selection": selection, **managed_value},
        expected_schema=AUTONOMY_ENVELOPE_SCHEMA,
    )
    requested = request_doc.value
    maximum = managed_doc.value
    operations = sorted(
        set(requested["delegation"]["operations"]) & set(maximum["delegation"]["operations"]),
        key=lambda item: item.encode("utf-8"),
    )
    profiles = sorted(
        set(requested["delegation"]["execution_profiles"])
        & set(maximum["delegation"]["execution_profiles"]),
        key=lambda item: item.encode("utf-8"),
    )
    paths = _scope_intersection(
        requested["delegation"]["path_scope"], maximum["delegation"]["path_scope"]
    )
    if not operations or not profiles or not paths:
        _error("AEXCON010", "$.request", "request has no admissible operation, profile, or path intersection")
    if requested["delegation"]["asserted_by"] != maximum["delegation"]["asserted_by"]:
        _error("AEXCON012", "$.delegation.asserted_by", "request and managed actor assertions conflict")
    required_paths = sorted(
        set(requested["evidence"]["required_paths"]) | set(maximum["evidence"]["required_paths"]),
        key=lambda item: item.encode("utf-8"),
    )
    for item in required_paths:
        if not any(_path_within(item, delegated) for delegated in paths):
            _error("AEXCON010", "$.evidence.required_paths", "narrowing would remove required evidence scope")
    envelope = {
        "schema": AUTONOMY_ENVELOPE_SCHEMA,
        "selection": selection,
        "delegation": {
            "asserted_by": requested["delegation"]["asserted_by"],
            "operations": operations,
            "path_scope": paths,
            "execution_profiles": profiles,
            "max_parallel_writers": min(
                requested["delegation"]["max_parallel_writers"],
                maximum["delegation"]["max_parallel_writers"],
            ),
            "retry_limits": {
                operation: min(
                    requested["delegation"]["retry_limits"][operation],
                    maximum["delegation"]["retry_limits"][operation],
                )
                for operation in operations
            },
            "stop_before": sorted(
                set(requested["delegation"]["stop_before"])
                | set(maximum["delegation"]["stop_before"])
                | MANDATORY_STOPS,
                key=lambda item: item.encode("utf-8"),
            ),
        },
        "evidence": {
            "required_receipt": bool(
                requested["evidence"]["required_receipt"] or maximum["evidence"]["required_receipt"]
            ),
            "required_paths": required_paths,
        },
    }
    candidate = validate_contract(envelope, expected_schema=AUTONOMY_ENVELOPE_SCHEMA)
    if parent is not None:
        parent_doc = validate_contract(parent, expected_schema=AUTONOMY_ENVELOPE_SCHEMA)
        if parent_sha256 is None or _sha256(parent_sha256, "$.parent_sha256") != parent_doc.sha256:
            _error("AEXCON011", "$.parent_sha256", "parent bytes and digest do not match")
        _assert_narrower(candidate.value, parent_doc.value)
    elif parent_sha256 is not None:
        _error("AEXCON011", "$.parent_sha256", "parent digest was supplied without parent bytes")
    narrowing: list[str] = []
    for name, selected, source in (
        ("operations", operations, requested["delegation"]["operations"]),
        ("path_scope", paths, requested["delegation"]["path_scope"]),
        ("execution_profiles", profiles, requested["delegation"]["execution_profiles"]),
    ):
        if selected != source:
            narrowing.append(name)
    if candidate.value["delegation"]["max_parallel_writers"] != requested["delegation"]["max_parallel_writers"]:
        narrowing.append("max_parallel_writers")
    if candidate.value["delegation"]["retry_limits"] != requested["delegation"]["retry_limits"]:
        narrowing.append("retry_limits")
    return EnvelopeConstruction(
        "constructed",
        state,
        candidate,
        state.value["governance"]["work_order"],
        _managed_id(procedure_id, "$.procedure_id"),
        selection["evaluator_payload_sha256"],
        state.value["governance"]["formal_snapshot_sha256"],
        tuple(narrowing),
    )


def assess_admission(
    envelope: Mapping[str, Any],
    *,
    envelope_sha256: str,
    expected_current_repository_state: str,
    operation: str,
    target_paths: Sequence[str],
    execution_profile: str,
    requested_writers: int,
    retry_ordinal: int,
    evidence_paths: Sequence[str],
    stop_boundary: str,
) -> AdmissionAssessment:
    """Purely assess one operation against a validated envelope."""

    document = validate_contract(envelope, expected_schema=AUTONOMY_ENVELOPE_SCHEMA)
    claimed_digest = _sha256(envelope_sha256, "$.envelope_sha256")
    current = _sha256(expected_current_repository_state, "$.expected_current_repository_state")
    selected_operation = _managed_id(operation, "$.operation")
    selected_profile = _profile_name(execution_profile, "$.execution_profile")
    selected_paths = _string_set(list(target_paths), "$.target_paths", _path, minimum=1, paths=True)
    selected_evidence = _string_set(list(evidence_paths), "$.evidence_paths", _path, paths=True)
    writers = _integer(requested_writers, "$.requested_writers", minimum=0, maximum=MAX_PARALLEL_WRITERS)
    retry = _integer(retry_ordinal, "$.retry_ordinal", minimum=0, maximum=MAX_RETRY)
    boundary = _managed_id(stop_boundary, "$.stop_boundary")
    if claimed_digest != document.sha256 or current != document.value["selection"]["repository_state"]:
        diagnostic = AgentContractError("AEXCON011", "$.selection", "envelope or expected-current identity is stale")
        return AdmissionAssessment(
            "stale", document.sha256, selected_operation, tuple(selected_paths), current, tuple(selected_evidence), (diagnostic.as_dict(),)
        )
    delegation = document.value["delegation"]
    evidence = document.value["evidence"]
    denied: list[Mapping[str, str]] = []
    if selected_operation not in delegation["operations"]:
        denied.append(AgentContractError("AEXCON010", "$.operation", "operation is outside envelope scope").as_dict())
    if selected_profile not in delegation["execution_profiles"]:
        denied.append(AgentContractError("AEXCON010", "$.execution_profile", "profile is outside envelope scope").as_dict())
    if writers > delegation["max_parallel_writers"]:
        denied.append(AgentContractError("AEXCON010", "$.requested_writers", "writer count exceeds envelope scope").as_dict())
    if retry > delegation["retry_limits"].get(selected_operation, -1):
        denied.append(AgentContractError("AEXCON010", "$.retry_ordinal", "retry exceeds envelope scope").as_dict())
    for path in selected_paths:
        if not any(_path_within(path, parent) for parent in delegation["path_scope"]):
            denied.append(AgentContractError("AEXCON010", "$.target_paths", "target path is outside envelope scope").as_dict())
            break
    if boundary in delegation["stop_before"]:
        denied.append(
            AgentContractError(
                "AEXCON012",
                "$.stop_boundary",
                "operation reached a boundary that requires an accountable stop",
            ).as_dict()
        )
    missing_evidence = [
        item
        for item in evidence["required_paths"]
        if not any(_path_within(observed, item) for observed in selected_evidence)
    ]
    if missing_evidence:
        denied.append(AgentContractError("AEXCON010", "$.evidence_paths", "required evidence path is missing").as_dict())
    return AdmissionAssessment(
        "denied" if denied else "admissible",
        document.sha256,
        selected_operation,
        tuple(selected_paths),
        current,
        tuple(evidence["required_paths"]),
        tuple(denied),
    )


def _finding_from_source(value: Any, path: str, scope: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        _error("AEXCON014", path, "workflow finding must be an object")
    allowed = {"code", "path", "message", "plane"}
    if not set(value).issubset(allowed) or not {"code", "message"}.issubset(value):
        _error("AEXCON014", path, "workflow finding cannot be losslessly normalized")
    return _validate_packet_finding(
        {
            "scope": scope,
            "code": value["code"],
            "path": value.get("path"),
            "message": value["message"],
            "plane": value.get("plane"),
        },
        path,
    )


def project_decision_packet(
    workflow_result: Mapping[str, Any], packet_context: Mapping[str, Any]
) -> ContractDocument:
    """Losslessly project one complete workflow-result v2 decision to packet v2."""

    source = _object(
        workflow_result,
        {"schema", "operation", "selection", "scope", "compliance", "procedure", "state", "findings", "mutation", "restitution"},
        "$.workflow_result",
    )
    if source["schema"] != WORKFLOW_RESULT_SCHEMA:
        _error("AEXCON004", "$.workflow_result.schema", "decision source must be workflow-result v2")
    context = validate_contract(packet_context, expected_schema=PACKET_CONTEXT_SCHEMA).value
    selection = _object(source["selection"], {"primary", "artifacts"}, "$.workflow_result.selection")
    primary = _artifact_id(selection["primary"], "$.workflow_result.selection.primary")
    artifacts = _string_set(selection["artifacts"], "$.workflow_result.selection.artifacts", _artifact_id, minimum=1)
    if primary not in artifacts:
        _error("AEXCON014", "$.workflow_result.selection", "primary artifact is absent from selection")
    scope = _object(
        source["scope"],
        {"mode", "governing", "dependencies", "declared_paths", "changed_paths", "change_set_complete"},
        "$.workflow_result.scope",
    )
    if scope["mode"] != "selected":
        _error("AEXCON014", "$.workflow_result.scope.mode", "decision packet requires selected scope")
    compliance = _object(
        source["compliance"],
        {"checkpoint", "workflow_rule_id", "procedure_id", "status", "gates"},
        "$.workflow_result.compliance",
    )
    procedure = _object(source["procedure"], {"id", "current_step", "steps"}, "$.workflow_result.procedure")
    restitution = _object(
        source["restitution"],
        {"outcome", "done", "not_done", "blocked_by", "current_lifecycle_state", "decision_required", "next", "command_or_response", "alternatives"},
        "$.workflow_result.restitution",
    )
    next_step = _object(restitution["next"], {"procedure_id", "step_id", "action"}, "$.workflow_result.restitution.next")
    procedure_id = _managed_id(procedure["id"], "$.workflow_result.procedure.id")
    step_id = _managed_id(procedure["current_step"], "$.workflow_result.procedure.current_step")
    if not (procedure_id == compliance["procedure_id"] == next_step["procedure_id"]):
        _error("AEXCON014", "$.workflow_result.procedure", "procedure identities conflict")
    if step_id != next_step["step_id"]:
        _error("AEXCON014", "$.workflow_result.procedure.current_step", "procedure step identities conflict")
    decision = restitution["decision_required"]
    if decision is None:
        _error("AEXCON014", "$.workflow_result.restitution.decision_required", "source has no complete decision")
    decision = _object(
        decision,
        {"decision_right", "role", "artifact", "decision", "outcomes"},
        "$.workflow_result.restitution.decision_required",
    )
    if decision["artifact"] != primary:
        _error("AEXCON014", "$.workflow_result.restitution.decision_required.artifact", "decision subject differs from selection")
    states = _object(source["state"], {"before", "after"}, "$.workflow_result.state")

    def state_map(values: Any, path: str) -> dict[str, str]:
        result: dict[str, str] = {}
        for index, item in enumerate(_array(values, path)):
            entry = _object(item, {"id", "status"}, f"{path}[{index}]")
            artifact = _artifact_id(entry["id"], f"{path}[{index}].id")
            if artifact in result:
                _error("AEXCON003", path, "duplicate artifact state")
            result[artifact] = _managed_id(entry["status"], f"{path}[{index}].status")
        return result

    before = state_map(states["before"], "$.workflow_result.state.before")
    after = state_map(states["after"], "$.workflow_result.state.after")
    if primary not in before or before.get(primary) != after.get(primary):
        _error("AEXCON014", "$.workflow_result.state", "decision source does not stop before its state effect")
    steps = _array(procedure["steps"], "$.workflow_result.procedure.steps")
    selected_steps = [item for item in steps if isinstance(item, dict) and item.get("id") == step_id]
    if len(selected_steps) != 1:
        _error("AEXCON014", "$.workflow_result.procedure.steps", "selected procedure step is missing or ambiguous")
    step = selected_steps[0]
    if not {"effects", "non_effects"}.issubset(step):
        _error("AEXCON014", "$.workflow_result.procedure.steps", "selected step lacks effect declarations")
    command = _validate_command_response(restitution["command_or_response"], "$.workflow_result.restitution.command_or_response")
    resolved: dict[str, Any] | None = None
    if step.get("kind") == "command" and isinstance(step.get("argv"), list):
        resolved = {"kind": "command", "argv": step["argv"]}
    elif step.get("kind") == "decision" and isinstance(step.get("response"), str):
        resolved = {"kind": "response", "value": step["response"]}
    if resolved is None or _validate_command_response(resolved, "$.workflow_result.procedure.steps.resolved") != command:
        _error("AEXCON014", "$.workflow_result.restitution.command_or_response", "handoff differs from selected procedure step")
    alternative_summaries = _sequence(
        restitution["alternatives"], "$.workflow_result.restitution.alternatives", lambda item, p: _text(item, p, maximum=512)
    )
    if [item["summary"] for item in context["alternatives"]] != alternative_summaries:
        _error("AEXCON014", "$.packet_context.alternatives", "complete alternatives do not match source summaries")
    findings = _object(
        source["findings"], {"scoped_blockers", "repository_blockers", "unrelated_count"}, "$.workflow_result.findings"
    )
    packet = {
        "schema": PACKET_V2_SCHEMA,
        "context": {
            "selected_artifact": primary,
            "lifecycle_state": before[primary],
            "governing": scope["governing"],
            "dependencies": scope["dependencies"],
            "declared_paths": scope["declared_paths"],
            "changed_paths": scope["changed_paths"],
            "change_set_complete": scope["change_set_complete"],
            "procedure_id": procedure_id,
            "procedure_step_id": step_id,
        },
        "decision": {
            "kind": decision["decision_right"],
            "subject": decision["artifact"],
            "required_accountable_role": decision["role"],
            "recommendation": next_step["action"],
            "alternatives": context["alternatives"],
        },
        "identity": {
            "repository": context["repository"],
            "candidate_commit": context["candidate_commit"],
            "evaluator_payload_sha256": context["evaluator_payload_sha256"],
        },
        "assessment": {
            "gates": compliance["gates"],
            "evidence": context["evidence"],
            "findings": [
                *[
                    _finding_from_source(item, f"$.workflow_result.findings.scoped_blockers[{index}]", "selected")
                    for index, item in enumerate(findings["scoped_blockers"])
                ],
                *[
                    _finding_from_source(item, f"$.workflow_result.findings.repository_blockers[{index}]", "repository")
                    for index, item in enumerate(findings["repository_blockers"])
                ],
            ],
            "assumptions": context["assumptions"],
            "residual_uncertainty": context["residual_uncertainty"],
        },
        "effect": {
            "preview": context["preview"],
            "effects": step["effects"],
            "non_effects": step["non_effects"],
        },
        "handoff": {"command_or_suggested_response": command, "safe_to_defer": context["safe_to_defer"]},
    }
    return validate_contract(packet, expected_schema=PACKET_V2_SCHEMA)


def render_decision_packet(packet: Mapping[str, Any]) -> str:
    """Render packet v2 in the deterministic normative heading order."""

    value = validate_contract(packet, expected_schema=PACKET_V2_SCHEMA).value

    def render_items(items: Sequence[Any]) -> str:
        if not items:
            return "none"
        return "\n".join(f"- {json.dumps(item, ensure_ascii=False, sort_keys=True)}" for item in items)

    context = value["context"]
    identity = value["identity"]
    handoff = value["handoff"]["command_or_suggested_response"]
    sections: list[tuple[str, str]] = [
        ("Decision", value["decision"]["kind"]),
        ("Subject", value["decision"]["subject"]),
        ("Accountable role", value["decision"]["required_accountable_role"]),
        ("Current lifecycle state", context["lifecycle_state"]),
        (
            "Scope",
            json.dumps(
                {
                    "governing": context["governing"],
                    "dependencies": context["dependencies"],
                    "declared_paths": context["declared_paths"],
                    "changed_paths": context["changed_paths"],
                    "change_set_complete": context["change_set_complete"],
                },
                ensure_ascii=False,
                sort_keys=True,
            ),
        ),
        ("Procedure", f"{context['procedure_id']} / {context['procedure_step_id']}"),
        ("Recommendation", value["decision"]["recommendation"]),
        ("Alternatives", render_items(value["decision"]["alternatives"])),
        (
            "Identity",
            json.dumps(
                {
                    "repository": identity["repository"],
                    "candidate_commit": identity["candidate_commit"] or "not applicable",
                    "evaluator_payload_sha256": identity["evaluator_payload_sha256"] or "not applicable",
                },
                ensure_ascii=False,
                sort_keys=True,
            ),
        ),
        ("Gates", render_items(value["assessment"]["gates"])),
        ("Evidence", render_items(value["assessment"]["evidence"])),
        ("Findings", render_items(value["assessment"]["findings"])),
        ("Assumptions", render_items(value["assessment"]["assumptions"])),
        ("Residual uncertainty", render_items(value["assessment"]["residual_uncertainty"])),
        ("Preview", json.dumps(value["effect"]["preview"], ensure_ascii=False, sort_keys=True)),
        ("Effects", render_items(value["effect"]["effects"])),
        ("Non-effects", render_items(value["effect"]["non_effects"])),
        ("Safe to defer", "true" if value["handoff"]["safe_to_defer"] else "false"),
        ("Command or response", json.dumps(handoff, ensure_ascii=False, sort_keys=True)),
    ]
    return "\n\n".join(f"{heading}\n{body}" for heading, body in sections) + "\n"


def validate_execution_receipt(
    receipt: Mapping[str, Any], expectations: ReceiptExpectations | None = None
) -> ContractDocument:
    """Validate a receipt and, when supplied, exact independent plan coverage."""

    def reject_prohibited_metadata(value: Any, path: str = "$") -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                normalized = str(key).casefold().replace("-", "_")
                if any(
                    marker in normalized
                    for marker in (
                        "accountable_role",
                        "authority",
                        "credential",
                        "hidden_reasoning",
                        "secret",
                        "token",
                    )
                ):
                    _error("AEXCON016", f"{path}.{key}", "receipt contains prohibited authority or sensitive metadata")
                reject_prohibited_metadata(item, f"{path}.{key}")
        elif isinstance(value, list):
            for index, item in enumerate(value):
                reject_prohibited_metadata(item, f"{path}[{index}]")

    reject_prohibited_metadata(receipt)
    document = validate_contract(receipt, expected_schema=RECEIPT_SCHEMA)
    if expectations is None:
        return document
    value = document.value
    actual_evidence = tuple(
        (item["kind"], item.get("path"), item["sha256"]) for item in value["effects"]["evidence"]
    )
    actual_before = tuple((item["kind"], item["sha256"]) for item in value["effects"]["state_before"])
    actual_after = tuple((item["kind"], item["sha256"]) for item in value["effects"]["state_after"])
    comparisons = (
        (tuple(value["execution"]["profiles"]), expectations.profiles, "$.execution.profiles"),
        (tuple(item["name"] for item in value["execution"]["skills"]), expectations.skill_names, "$.execution.skills"),
        (tuple(item["id"] for item in value["execution"]["operations"]), expectations.operation_ids, "$.execution.operations"),
        (tuple(item["id"] for item in value["execution"]["worker_results"]), expectations.worker_ids, "$.execution.worker_results"),
        (tuple(value["effects"]["changed_paths"]), expectations.changed_paths, "$.effects.changed_paths"),
        (actual_evidence, expectations.evidence, "$.effects.evidence"),
        (actual_before, expectations.state_before, "$.effects.state_before"),
        (actual_after, expectations.state_after, "$.effects.state_after"),
        (
            value["selection"]["autonomy_envelope_sha256"],
            expectations.autonomy_envelope_sha256,
            "$.selection.autonomy_envelope_sha256",
        ),
        (
            value["validation"]["evaluator"].get("payload_sha256"),
            expectations.evaluator_payload_sha256,
            "$.validation.evaluator.payload_sha256",
        ),
    )
    for actual, expected, path in comparisons:
        if actual != expected:
            _error("AEXCON015", path, "receipt coverage differs from the independent execution plan")
    return document


def validate_logical_execution_profile(
    profile: Mapping[str, Any], *, accountable_roles: Iterable[str] = ()
) -> ContractDocument:
    """Validate one provider-neutral, non-authoritative logical profile."""

    document = validate_contract(profile, expected_schema=PROFILE_SCHEMA)
    roles = set(accountable_roles)
    if document.value["name"] in roles:
        _error("AEXCON017", "$.name", "profile name is ambiguous with an accountable role")
    return document


__all__ = [
    "AUTONOMY_ENVELOPE_SCHEMA",
    "AUTONOMY_ENVELOPE_V2_SCHEMA",
    "CANONICAL_JSON_SCHEMA",
    "CATALOG_SCHEMA",
    "DELEGATION_SCHEMA",
    "PACKET_CONTEXT_SCHEMA",
    "PACKET_V1_SCHEMA",
    "PACKET_V2_SCHEMA",
    "PROFILE_SCHEMA",
    "RECEIPT_SCHEMA",
    "REPOSITORY_STATE_SCHEMA",
    "REPOSITORY_OBSERVATION_SCHEMA",
    "WORKTREE_STATE_SCHEMA",
    "AdmissionAssessment",
    "AgentContractError",
    "ContractDocument",
    "EnvelopeConstruction",
    "ReceiptExpectations",
    "assess_admission",
    "canonical_json_bytes",
    "canonical_sha256",
    "construct_envelope_candidate",
    "construct_repository_state_binding",
    "narrow_autonomy_envelope",
    "parse_agent_contract_catalog_bytes",
    "parse_contract_bytes",
    "parse_json_bytes",
    "project_decision_packet",
    "render_decision_packet",
    "validate_contract",
    "validate_execution_receipt",
    "validate_logical_execution_profile",
]
