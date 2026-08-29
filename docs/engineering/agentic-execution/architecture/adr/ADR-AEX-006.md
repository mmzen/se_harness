+++
id = "ADR-AEX-006"
type = "adr"
title = "Formal maximum delegation with evaluator-derived ephemeral authority"
status = "approved"
owners = ["technical-owner", "repository-owner", "security-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
decides = ["ARCH-AEX-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T09:08:48Z"
decided_by = "technical-owner"
+++

# ADR: Formal maximum delegation with evaluator-derived ephemeral authority

## Status

Proposed.

## Context

Phase 4 needs to let one worker perform selected repository and workflow
operations without a human confirmation before every mechanical step. The
maximum authority must be reviewable before execution, while actual effect
admission must depend on state that cannot be known at work-order approval time.

`SPEC-AEX-003` already decides that envelopes are evaluator-derived and in
memory by default, but it intentionally leaves live observation and mutation
integration for a later phase. This ADR closes the source, lifetime, replay, and
state-chain decisions for that integration.

## Decision drivers

- Preserve accountable ownership of decision rights.
- Make maximum delegation reviewable with the selected work.
- Bind each effect to the exact current repository and released evaluator.
- Prevent caller-minted, stale, copied, or replayed authority.
- Allow several sequential effects without widening the original delegation.
- Keep 0.6.0 and nondelegated repositories compatible.
- Keep provider identities and permissions non-authoritative.

## Considered options

### Option A — persist an approved reusable envelope with the work order

The owner approves serialized authority once and the worker presents it for
each effect. This is easy to inspect, but current repository state is not known
at approval, expiry and revocation are awkward, and copied bytes behave like a
bearer token.

### Option B — let the selected skill or agent derive envelopes

The procedure knows the requested paths and can move quickly. It is also the
untrusted requester, cannot prove the exact evaluator or live repository, and
would become a second authority source.

### Option C — record maximum delegation formally and derive one ephemeral
envelope per effect through the exact released evaluator

The approved work order records the maximum rights and scope. At request time,
the evaluator obtains stable live observations, intersects all current inputs,
creates a short-lived nonce-bound envelope, and freshly rechecks state under
the effect lock. A verified receipt anchors the next independently derived
envelope.

### Option D — use provider sessions or operating-system permissions as the
delegation token

Provider and OS controls can reduce reachable effects but do not express
formal decision rights, artifact state, gates, or repository freshness and are
not portable governance records.

## Decision

Choose Option C, subject to approval of `REQ-AEX-010`, `SPEC-AEX-006`,
`VER-AEX-004`, and the applicable implementation work order.

Add an optional formal maximum-delegation declaration to the candidate work-
order template. Its absence means no Phase 4 authority. The declaration is
approved with the work order and cannot be widened during execution.

The exact released evaluator obtains two identical canonical observations
before derivation. It intersects the worker request with the declaration,
work-order scope, current workflow state, gates, profiles, evidence, expiry,
retries, single-writer policy, and mandatory stops. It derives autonomy-envelope
v2 in memory with a unique nonce and at most five-minute lifetime.

Immediately before effect, the evaluator holds the exclusive target-session
lock, freshly observes the repository, requires the state digest to match, and
atomically consumes the nonce. Successful effect receipts bind before and after
state. A next request derives a new envelope from the verified `state_after` and
receipt digest; it never mutates or reuses the previous envelope.

Provider permissions, skill discovery, model output, process identity, and
serialized envelope-shaped input create no authority.

## Consequences

### Positive

- Accountable owners can review the complete maximum delegation in context.
- Actual authority remains narrow, current, short-lived, and single-use.
- Receipt chaining supports useful sequential execution while exposing every
  state transition.
- Skills and providers remain replaceable clients.
- Repositories without delegation preserve the existing human-driven flow.

### Negative

- Work-order schema, validator, workflow contract, envelope schema, and runtime
  state management all need versioned changes.
- Live observation may be expensive on large worktrees.
- A five-minute envelope can expire during slow preparation and require fresh
  derivation.
- Runtime state outside the checkout needs explicit secure configuration,
  retention, and recovery handling.

### Operational

- Initial start requires a clean target; later dirty state must be fully
  explained by the receipt chain.
- Any unexplained edit invalidates the current envelope and stops execution.
- A successor released evaluator must be installed externally before use.
- Operators retain a command-driven fallback when delegation is absent or
  agentic capability is unavailable.

### Security

- Nonces are random, single-use, and persisted only as restricted runtime
  ledger entries or digests.
- Absolute target paths and secret bytes are excluded from portable authority
  and normal evidence.
- Actor assertions retain existing harness semantics and do not become OS or
  provider authentication claims.
- Mandatory accountable and action-time stop classes cannot be removed.

### Migration

- Keep autonomy-envelope v1 valid for pure validation and historical evidence.
- Add v2 for live Phase 4 admission.
- Add the work-order delegation table only in a successor managed template and
  validator release.
- Do not synthesize delegation while upgrading an existing repository.

## Validation

`VER-AEX-004` verifies schema closure, stable observation, evaluator ownership,
least-authority intersection, expiry, revocation, nonce reuse, stale state,
receipt chaining, unexplained dirty state, mandatory stops, and compatibility.

## Amendment record

**The evaluator-derived ephemeral envelope is superseded by the delegation
class of `ADR-ECP-002`, recorded 2026-08-29 under `WO-ECP-006`.** The nonce
ledger, the five-minute lifetime, revocation, the retry ordinal and the
two-observation stability guard defended a token that never left the process
that minted it; `WO-ECP-006` removes them from the product with
`delegated_authority.py`, `runtime_state.py` and `agent_contract.py`
(`SPEC-ECP-006`, `ECP-DLG-008`). What this decision retained as its formal
maximum delegation on the work order continues as the `[delegation]` class
of `REQ-ECP-011`, which unlocks three transitions only while the candidate's
required check is green; that class is implemented under a later work order.
The front matter of this record is unchanged; it is history.
