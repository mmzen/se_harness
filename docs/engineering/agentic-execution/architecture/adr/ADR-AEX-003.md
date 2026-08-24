+++
id = "ADR-AEX-003"
type = "adr"
title = "Evaluator-derived autonomy envelopes with evidence-only persistence"
status = "approved"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
decides = ["ARCH-AEX-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T11:49:36Z"
decided_by = "technical-owner"
+++

# ADR: Evaluator-derived autonomy envelopes with evidence-only persistence

## Status

Option C was accepted during accountable technical-owner review. The
authoritative lifecycle state is recorded in the front-matter `status` and
lifecycle events.

## Context

`SPEC-AEX-001` defines an autonomy envelope as a non-transferable, bounded
grant for governed execution, but deliberately defers the exact
repository-state representation and the mechanism that derives or stores an
authoritative envelope. Those choices must be closed before an implementation
can assess an envelope for later governed mutation.

Skills, agents, models, runtime profiles, and provider configuration are
execution machinery. Allowing any of them to author their own authority would
let a prompt, copied file, stale observation, or runtime permission bypass the
harness-owned authority plane. Conversely, treating every envelope as a formal
lifecycle artifact would add approval and storage overhead to short-lived,
scope-narrowed grants and would make freshness difficult to reason about.

Phase 2 needs a runtime-neutral contract boundary that can be fully tested
without connecting it to a real mutation. `SPEC-AEX-003` defines the exact
contract catalog and repository-state binding for that boundary.

## Decision drivers

- Keep accountable authority and derivation policy in the harness.
- Reject stale, replayed, copied, caller-modified, or scope-expanded grants.
- Remain portable across agent, model, IDE, CI, and hosted runtimes.
- Avoid a new service, credential system, or formal-artifact lifecycle per
  short-lived envelope.
- Retain enough deterministic evidence to reconstruct what was admitted.
- Preserve the Phase 1 single-agent, read-only skill identity and boundary.
- Make Phase 2 independently testable before any real effect integration.

## Considered options

### Option A — caller- or skill-authored envelopes

The caller constructs an envelope and the harness accepts it when its fields
are syntactically valid or accompanied by runtime-specific proof.

Rejected. Syntax, a prompt, a sandbox permission, a runtime identity, or a
signature over caller-selected data cannot establish that the grant reflects
the current managed repository, selected work order, evaluator, and accountable
decision. It also places authority semantics in replaceable execution layers.

### Option B — persist each envelope as a formal repository artifact

Every envelope is stored, reviewed, and transitioned through the formal
artifact lifecycle before use.

Rejected. This creates lifecycle and repository churn for ephemeral narrowing,
introduces self-reference when repository state includes the stored envelope,
and does not by itself solve freshness between approval and use.

### Option C — evaluator-derived envelopes with evidence-only persistence

The exact released evaluator derives the canonical repository-state binding and
envelope from current managed state and an already-authorized work order. A
caller may request only a narrower subset. The envelope is passed in memory by
default; declared evidence retains its digest and state chain.

Selected. This keeps derivation in the harness-owned authority plane, makes
freshness and narrowing explicit, and avoids turning ephemeral grants into a
new lifecycle class.

### Option D — hosted orchestration authority service

A remote orchestration service issues authoritative envelopes and coordinates
their use.

Rejected for this phase. It introduces provider, network, credential,
availability, and trust dependencies that conflict with the runtime-neutral
contract boundary. A future integration may consume the same contracts, but it
may not replace harness-owned authority without a separate architecture
decision.

## Decision

Choose Option C, subject to approval of this ADR and `SPEC-AEX-003`.

The exact released evaluator is the sole component that may derive an
authoritative `se-harness-autonomy-envelope-v1` for governed repository work.
It does so only after applying the existing integrity, formal-artifact,
procedure, quality-gate, actor, and work-order checks. A skill, agent, model,
adapter, runtime, or caller may request an equal or narrower operation set,
path set, profile set, writer count, retry limit, stop boundary, or evidence
obligation; it may not supply authoritative bytes or widen the result.

The evaluator derives the canonical
`se-harness-repository-state-binding-v1` defined by `SPEC-AEX-003`, binds its
digest and the selected work-order identity into the envelope, and computes the
canonical envelope digest. A copied, caller-modified, differently bound, or
stale envelope has no authority and must fail admission.

This authority step is deliberately not part of Phase 2. `WO-AEX-002`
implements pure functions that validate explicitly supplied typed observations,
construct canonical binding and envelope candidates, narrow candidates, and
return `admissible` or a fail-closed result. `constructed` and `admissible` are
non-authoritative assessments. Only a later separately authorized evaluator
integration may collect live Git/filesystem/governance observations and label
the exact candidate bytes `derived` or an operation `admitted`.

The canonical envelope normally remains in memory. Persistence is allowed only
at a path and for an evidence purpose already declared by an approved work
order. Persistence creates neither a formal lifecycle artifact nor a new
authority source. The execution receipt records the envelope digest,
independently observed before and after state, required evidence digests, and
all requested operation or worker outcomes. Later grants may use a prior
receipt's `state_after` only as the explicitly expected current state; the
evaluator must still observe and compare current repository state.

`WO-AEX-002` may implement only strict parsing, canonical encoding, candidate
construction from supplied observations, narrowing, and pure admission
assessment. Its tests use an injected caller-side effect sentinel to prove
denied input returns before an effect boundary. It may
not connect the contract to `mutation_guard`, a workflow command, a lifecycle
transition, Git, credentials, a network call, or any real write. The first real
mutation integration requires a separate approved work order and use of the
released evaluator.

## Consequences

### Positive

- Authority is derived from current managed repository facts instead of agent
  or runtime assertions.
- Scope narrowing has one canonical, runtime-neutral implementation boundary.
- Short-lived envelopes do not create lifecycle clutter or become durable
  authority tokens.
- Deterministic binding and receipt digests support independent verification,
  replay detection, and audit reconstruction.
- Contract behavior can be tested exhaustively before any write path exists.

### Negative

- Envelope derivation requires access to the exact released evaluator and a
  stable observation of managed repository state.
- A repository change can invalidate a previously derived envelope and require
  re-derivation, even when the intended operation is otherwise unchanged.
- Evidence consumers must retain and compare canonical digests and state chains
  rather than rely on a self-contained caller-issued token.

### Operational

- In a future integration, derive the state binding and envelope immediately
  before admission and compare expected state again at the effect boundary.
- In Phase 2, use only verifier-owned typed observation fixtures and label
  successful construction and assessment `constructed` and `admissible`.
- Record evaluator identity, envelope digest, state-before, state-after, gates,
  deviations, and evidence digests in the declared receipt or verification
  evidence.
- Treat unknown schemas, missing observations, state drift, incomplete work,
  and widening requests as stop conditions.
- Keep the Phase 1 `harness-orient` skill byte and semantic identity unchanged.

### Security

- Treat catalogs, envelopes, paths, repository observations, receipts, runtime
  metadata, and workflow results as untrusted input.
- Do not treat a signature, runtime permission, model identity, receipt,
  persistence location, or successful execution as accountable approval.
- Exclude credentials, secrets, hidden reasoning, and unbounded host metadata
  from envelopes and receipts.
- Future write integrations must compare the admitted binding to a fresh
  observation before an effect; validation alone is not a lock.

### Migration

- Phase 2 introduces the catalog and pure contract module without migrating any
  existing mutation path.
- Existing `harness-orient` contracts and receipts remain compatible and
  unchanged.
- Any later skill, adapter, orchestration layer, or mutation guard must consume
  this approved contract through a separately approved work order.

## Validation

Architecture conformance is checked through the applicable `VER-AEX-001`
methods for `REQ-AEX-001` through `REQ-AEX-005`. Verification must use
verifier-owned canonical vectors and adversarial fixtures to demonstrate:

- pure functions cannot emit `derived` or `admitted`, while only a separately
  authorized released-evaluator integration may apply those labels;
- repository-state, packet-context, and catalog fixtures follow every exact
  field, ordering, compatibility, and digest rule in `SPEC-AEX-003`;
- equal and narrower grants pass while every expanded dimension fails;
- malformed, ambiguous, copied, stale, replayed, or mismatched inputs fail;
- denied cases make zero effect-sentinel calls;
- canonical bytes and digests are deterministic across ordering and environment
  variations;
- receipts completely and non-authoritatively record success, failure,
  cancellation, timeout, and missing required work; and
- Phase 1 skill identity and read-only behavior remain unchanged.

Commit-bound independent verification remains required by `WO-AEX-002` before
this contract layer can support a later mutation integration.
