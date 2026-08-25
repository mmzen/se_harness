"""Formal delegation resolution and effect-free Phase 4 admission preparation."""

from __future__ import annotations

import hashlib
import secrets
import tomllib
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any, Callable, Mapping

from se_harness.agent_contract import (
    AUTONOMY_ENVELOPE_V2_SCHEMA,
    DELEGATION_SCHEMA,
    REPOSITORY_OBSERVATION_SCHEMA,
    ContractDocument,
    ReceiptExpectations,
    validate_contract,
    validate_execution_receipt,
)
from se_harness.repository_state import StableRepositoryObservation, require_fresh_observation
from se_harness.runtime_state import RuntimeSession, RuntimeStateStore


MAX_ENVELOPE_LIFETIME = timedelta(minutes=5)


class DelegatedAuthorityError(RuntimeError):
    """A stable, bounded authority-derivation diagnostic."""

    def __init__(self, code: str, message: str) -> None:
        text = "".join(character if character >= " " else "?" for character in str(message))[:512]
        super().__init__(f"{code}: {text or 'delegated authority rejected'}")
        self.code = code
        self.message = text


@dataclass(frozen=True)
class DelegationPolicy:
    """Closed managed catalogs supplied by the exact released evaluator."""

    decision_right_delegators: Mapping[str, frozenset[str]]
    operations: frozenset[str]
    execution_profiles: frozenset[str]
    delegates: frozenset[str]
    operation_statuses: Mapping[str, frozenset[str]]


@dataclass(frozen=True)
class ResolvedDelegation:
    work_order: str
    work_order_status: str
    work_order_sha256: str
    execution_scope: tuple[str, ...]
    document: ContractDocument


@dataclass(frozen=True)
class AuthorityRequest:
    operation: str
    decision_right: str | None
    delegate: str
    execution_profile: str
    paths: tuple[str, ...]
    required_evidence: tuple[tuple[str, str], ...]
    retry_ordinal: int


@dataclass(frozen=True)
class EnvelopeDerivation:
    outcome: str
    envelope: ContractDocument
    observation_sha256: str
    delegation_sha256: str
    narrowing: tuple[str, ...]
    non_effects: tuple[str, ...] = (
        "No target repository, Git, lifecycle, credential, network, or external mutation occurred.",
        "No effect was admitted or invoked; the envelope remains an in-memory candidate.",
    )


@dataclass(frozen=True)
class LiveAdmission:
    outcome: str
    envelope_sha256: str
    repository_state_sha256: str
    nonce_sha256: str
    runtime_record: Mapping[str, Any]
    non_effects: tuple[str, ...] = (
        "The nonce was consumed in external runtime state.",
        "No target effect callback exists in this module and no target effect was invoked.",
    )


def _front_matter(raw: bytes) -> dict[str, Any]:
    if not isinstance(raw, bytes) or len(raw) > 1_048_576:
        raise DelegatedAuthorityError("AEXAUTH001", "work-order bytes exceed their bound")
    if raw.startswith(b"\xef\xbb\xbf"):
        raise DelegatedAuthorityError("AEXAUTH001", "work-order byte-order mark is prohibited")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise DelegatedAuthorityError("AEXAUTH001", "work order is not valid UTF-8") from exc
    if not text.startswith("+++\n"):
        raise DelegatedAuthorityError("AEXAUTH001", "work order has no TOML front matter")
    closing = text.find("\n+++\n", 4)
    if closing < 0:
        raise DelegatedAuthorityError("AEXAUTH001", "work-order front matter is unterminated")
    try:
        value = tomllib.loads(text[4:closing])
    except tomllib.TOMLDecodeError as exc:
        raise DelegatedAuthorityError("AEXAUTH001", "work-order front matter is invalid") from exc
    if not isinstance(value, dict):
        raise DelegatedAuthorityError("AEXAUTH001", "work-order front matter is not a table")
    return value


def _within(child: str, parent: str) -> bool:
    return child.startswith(parent) if parent.endswith("/") else child == parent


def _require_narrower(paths: tuple[str, ...], maximum: tuple[str, ...], label: str) -> None:
    if not paths or any(not any(_within(path, parent) for parent in maximum) for path in paths):
        raise DelegatedAuthorityError("AEXAUTH004", f"{label} is outside the maximum delegation")


def resolve_delegation(work_order_bytes: bytes, policy: DelegationPolicy) -> ResolvedDelegation:
    """Resolve and cross-check one optional formal delegation table."""

    metadata = _front_matter(work_order_bytes)
    if metadata.get("type") != "work_order":
        raise DelegatedAuthorityError("AEXAUTH002", "selected artifact is not a work order")
    work_order = metadata.get("id")
    status = metadata.get("status")
    if not isinstance(work_order, str) or not work_order.startswith("WO-"):
        raise DelegatedAuthorityError("AEXAUTH002", "work-order ID is invalid")
    if not isinstance(status, str) or not status:
        raise DelegatedAuthorityError("AEXAUTH002", "work-order status is invalid")
    scope_table = metadata.get("execution_scope")
    if (
        not isinstance(scope_table, dict)
        or set(scope_table) != {"paths"}
        or not isinstance(scope_table.get("paths"), list)
    ):
        raise DelegatedAuthorityError("AEXAUTH002", "work order has no exact execution scope")
    declaration = metadata.get("agentic_delegation")
    if declaration is None:
        raise DelegatedAuthorityError("AEXAUTH003", "work order declares no agentic delegation")
    if not isinstance(declaration, dict):
        raise DelegatedAuthorityError("AEXAUTH003", "agentic delegation is not a table")
    try:
        document = validate_contract(
            declaration, expected_schema=DELEGATION_SCHEMA
        )
    except ValueError as exc:
        raise DelegatedAuthorityError("AEXAUTH003", str(exc)) from exc
    value = document.value
    rights = set(value["decision_rights"])
    if not rights.issubset(policy.decision_right_delegators):
        raise DelegatedAuthorityError("AEXAUTH005", "delegation names an unknown decision right")
    if any(
        value["delegated_by"] not in policy.decision_right_delegators[right]
        for right in rights
    ):
        raise DelegatedAuthorityError(
            "AEXAUTH005", "delegator is not accountable for every named decision right"
        )
    if not set(value["operations"]).issubset(policy.operations):
        raise DelegatedAuthorityError("AEXAUTH005", "delegation names an unknown operation")
    if not set(value["execution_profiles"]).issubset(policy.execution_profiles):
        raise DelegatedAuthorityError("AEXAUTH005", "delegation names an unknown execution profile")
    if value["delegate"] not in policy.delegates:
        raise DelegatedAuthorityError("AEXAUTH005", "delegation names an unknown logical delegate")
    scope = tuple(scope_table["paths"])
    _require_narrower(tuple(value["paths"]), scope, "delegated path")
    _require_narrower(
        tuple(item["path"] for item in value["required_evidence"]),
        scope,
        "evidence path",
    )
    return ResolvedDelegation(
        work_order=work_order,
        work_order_status=status,
        work_order_sha256=hashlib.sha256(work_order_bytes).hexdigest(),
        execution_scope=scope,
        document=document,
    )


def _instant(value: str, label: str) -> datetime:
    try:
        instant = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
    except (TypeError, ValueError) as exc:
        raise DelegatedAuthorityError("AEXAUTH006", f"{label} is not a canonical UTC timestamp") from exc
    return instant


def derive_autonomy_envelope_v2(
    *,
    stable_observation: StableRepositoryObservation,
    delegation: ResolvedDelegation,
    policy: DelegationPolicy,
    request: AuthorityRequest,
    issued_at: datetime,
    gates_passed: bool,
    revoked: bool = False,
    managed_not_after: datetime | None = None,
    nonce_factory: Callable[[], str] = lambda: secrets.token_hex(16),
) -> EnvelopeDerivation:
    """Derive a least-authority v2 envelope without admitting an effect."""

    if stable_observation.captures < 2:
        raise DelegatedAuthorityError("AEXAUTH007", "two stable observations are required")
    observation = validate_contract(
        stable_observation.document.value,
        expected_schema=REPOSITORY_OBSERVATION_SCHEMA,
    )
    observed = observation.value
    declared = delegation.document.value
    if revoked:
        raise DelegatedAuthorityError("AEXAUTH008", "delegation is revoked")
    if not gates_passed:
        raise DelegatedAuthorityError("AEXAUTH009", "required current gates did not pass")
    if request.decision_right == "DR-WO-START" and not stable_observation.clean:
        raise DelegatedAuthorityError("AEXAUTH015", "delegated work-order start requires a clean repository")
    if not stable_observation.clean and observed["previous_receipt_sha256"] is None:
        raise DelegatedAuthorityError(
            "AEXAUTH014", "dirty repository state has no verified preceding receipt"
        )
    if issued_at.tzinfo is None or issued_at.utcoffset() != timedelta(0):
        raise DelegatedAuthorityError("AEXAUTH006", "issue time must be timezone-aware UTC")
    issued_at = issued_at.astimezone(UTC).replace(microsecond=0)
    if (
        observed["governance"]["work_order"] != delegation.work_order
        or observed["governance"]["work_order_sha256"] != delegation.work_order_sha256
        or observed["governance"]["work_order_status"] != delegation.work_order_status
    ):
        raise DelegatedAuthorityError("AEXAUTH010", "live work-order identity differs from delegation")
    allowed_statuses = policy.operation_statuses.get(request.operation)
    if allowed_statuses is None or delegation.work_order_status not in allowed_statuses:
        raise DelegatedAuthorityError("AEXAUTH011", "operation is unavailable in the current lifecycle state")
    if request.operation not in declared["operations"]:
        raise DelegatedAuthorityError("AEXAUTH004", "operation is outside the delegation")
    if request.decision_right is not None and request.decision_right not in declared["decision_rights"]:
        raise DelegatedAuthorityError("AEXAUTH004", "decision right is outside the delegation")
    if request.delegate != declared["delegate"]:
        raise DelegatedAuthorityError("AEXAUTH004", "delegate differs from the formal declaration")
    if request.execution_profile not in declared["execution_profiles"]:
        raise DelegatedAuthorityError("AEXAUTH004", "execution profile is outside the delegation")
    if not 0 <= request.retry_ordinal <= declared["max_retry"]:
        raise DelegatedAuthorityError("AEXAUTH004", "retry ordinal exceeds the delegation")
    _require_narrower(request.paths, tuple(declared["paths"]), "requested path")
    _require_narrower(request.paths, delegation.execution_scope, "requested path")
    evidence = tuple(
        (item["kind"], item["path"]) for item in declared["required_evidence"]
    )
    if tuple(sorted(request.required_evidence)) != tuple(sorted(evidence)):
        raise DelegatedAuthorityError(
            "AEXAUTH004", "requested evidence must retain every formal evidence obligation"
        )
    expiry = _instant(declared["valid_until"], "delegation expiry")
    limits = [issued_at + MAX_ENVELOPE_LIFETIME, expiry]
    if managed_not_after is not None:
        if managed_not_after.tzinfo is None:
            raise DelegatedAuthorityError("AEXAUTH006", "managed expiry must be timezone-aware")
        limits.append(managed_not_after.astimezone(UTC).replace(microsecond=0))
    not_after = min(limits)
    if not_after <= issued_at:
        raise DelegatedAuthorityError("AEXAUTH012", "delegation is expired")
    nonce = nonce_factory()
    if not isinstance(nonce, str):
        raise DelegatedAuthorityError("AEXAUTH013", "nonce source returned a non-string value")
    authority = {
        "decision_right": request.decision_right,
        "delegate": request.delegate,
        "execution_profile": request.execution_profile,
        "delegation_sha256": delegation.document.sha256,
        "work_order_sha256": delegation.work_order_sha256,
        "expected_repository_state": observation.sha256,
        "previous_receipt_sha256": observed["previous_receipt_sha256"],
        "nonce": nonce,
        "issued_at": issued_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "not_after": not_after.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "retry_ordinal": request.retry_ordinal,
    }
    candidate = {
        "schema": AUTONOMY_ENVELOPE_V2_SCHEMA,
        "selection": {
            "work_order": delegation.work_order,
            "work_order_sha256": delegation.work_order_sha256,
            "repository_state": observation.sha256,
            "evaluator_payload_sha256": observed["evaluator"]["payload_sha256"],
        },
        "delegation": {
            "asserted_by": declared["delegated_by"],
            "operations": [request.operation],
            "path_scope": list(request.paths),
            "execution_profiles": [request.execution_profile],
            "max_parallel_writers": 1,
            "retry_limits": {request.operation: declared["max_retry"]},
            "stop_before": list(declared["stop_before"]),
        },
        "evidence": {
            "required_receipt": True,
            "required_paths": [path for _, path in evidence],
        },
        "authority": authority,
    }
    try:
        envelope = validate_contract(
            candidate, expected_schema=AUTONOMY_ENVELOPE_V2_SCHEMA
        )
    except ValueError as exc:
        raise DelegatedAuthorityError("AEXAUTH013", str(exc)) from exc
    narrowing = tuple(
        name
        for name, narrowed in (
            ("operations", len(declared["operations"]) != 1),
            ("paths", tuple(declared["paths"]) != tuple(request.paths)),
            ("execution_profiles", len(declared["execution_profiles"]) != 1),
            ("decision_rights", len(declared["decision_rights"]) != (request.decision_right is not None)),
        )
        if narrowed
    )
    return EnvelopeDerivation(
        outcome="derived",
        envelope=envelope,
        observation_sha256=observation.sha256,
        delegation_sha256=delegation.document.sha256,
        narrowing=narrowing,
    )


def admit_fresh_envelope(
    *,
    envelope: ContractDocument,
    fresh_observation: ContractDocument,
    current_delegation_sha256: str,
    now: datetime,
    runtime_store: RuntimeStateStore,
    session: RuntimeSession,
    gates_passed: bool,
    revoked: bool = False,
) -> LiveAdmission:
    """Freshly assess and consume one nonce; this function has no target effect."""

    document = validate_contract(
        envelope.value, expected_schema=AUTONOMY_ENVELOPE_V2_SCHEMA
    )
    value = document.value
    fresh = require_fresh_observation(
        value["authority"]["expected_repository_state"], fresh_observation
    )
    if revoked or value["authority"]["delegation_sha256"] != current_delegation_sha256:
        raise DelegatedAuthorityError("AEXAUTH008", "delegation is revoked or changed")
    if not gates_passed:
        raise DelegatedAuthorityError("AEXAUTH009", "required current gates did not pass")
    if (
        fresh.value["evaluator"]["payload_sha256"]
        != value["selection"]["evaluator_payload_sha256"]
        or fresh.value["governance"]["work_order_sha256"]
        != value["selection"]["work_order_sha256"]
        or fresh.value["previous_receipt_sha256"]
        != value["authority"]["previous_receipt_sha256"]
    ):
        raise DelegatedAuthorityError("AEXAUTH010", "fresh evaluator or governance identity differs")
    if now.tzinfo is None:
        raise DelegatedAuthorityError("AEXAUTH006", "admission time must be timezone-aware")
    instant = now.astimezone(UTC).replace(microsecond=0)
    issued = _instant(value["authority"]["issued_at"], "issue time")
    expiry = _instant(value["authority"]["not_after"], "expiry")
    if instant < issued or instant >= expiry:
        raise DelegatedAuthorityError("AEXAUTH012", "envelope is not currently valid")
    record = runtime_store.consume_nonce(
        session,
        nonce=value["authority"]["nonce"],
        envelope_sha256=document.sha256,
        repository_state_sha256=fresh.sha256,
        admitted_at=instant.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    return LiveAdmission(
        outcome="admitted",
        envelope_sha256=document.sha256,
        repository_state_sha256=fresh.sha256,
        nonce_sha256=hashlib.sha256(value["authority"]["nonce"].encode("ascii")).hexdigest(),
        runtime_record=record,
    )


def verify_receipt_state_chain(
    *,
    receipt: Mapping[str, Any],
    expectations: ReceiptExpectations,
    admitted_repository_state: str,
    fresh_after: ContractDocument,
) -> ContractDocument:
    """Validate a receipt and bind its state transition to fresh live state."""

    document = validate_execution_receipt(receipt, expectations)
    fresh = validate_contract(
        fresh_after.value, expected_schema=REPOSITORY_OBSERVATION_SCHEMA
    )
    before = [
        item["sha256"]
        for item in document.value["effects"]["state_before"]
        if item["kind"] == "repository-state"
    ]
    after = [
        item["sha256"]
        for item in document.value["effects"]["state_after"]
        if item["kind"] == "repository-state"
    ]
    if before != [admitted_repository_state]:
        raise DelegatedAuthorityError("AEXAUTH014", "receipt has no exact admitted state_before")
    if after != [fresh.sha256]:
        raise DelegatedAuthorityError("AEXAUTH014", "receipt state_after differs from fresh live state")
    return document


__all__ = [
    "AuthorityRequest",
    "DelegatedAuthorityError",
    "DelegationPolicy",
    "EnvelopeDerivation",
    "LiveAdmission",
    "ResolvedDelegation",
    "admit_fresh_envelope",
    "derive_autonomy_envelope_v2",
    "resolve_delegation",
    "verify_receipt_state_chain",
]
