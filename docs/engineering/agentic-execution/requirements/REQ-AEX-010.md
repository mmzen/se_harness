+++
id = "REQ-AEX-010"
type = "requirement"
title = "Derive delegated mutation authority from live repository state"
status = "approved"
owners = ["product-owner", "requirements-steward", "technical-owner", "security-owner"]
created = "2026-08-25"
updated = "2026-08-25"
statement = "WHEN a governed single-agent execution requests a repository mutation under an approved and started work order with recorded advance delegation, THE SYSTEM SHALL have the target repository's exact released evaluator observe a stable current repository state and derive a least-authority, operation-bound, expiring autonomy envelope before any effect is admitted."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-AEX-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T09:08:48Z"
decided_by = "requirements-steward"
+++

# Requirement: Derive delegated mutation authority from live repository state

## Rationale

The approved Phase 2 contracts define autonomy envelopes and deterministic
admission, but the candidate implementation constructs envelopes from caller-
supplied data and deliberately performs no repository effect. Phase 4 needs an
authoritative bridge from an accountable owner's recorded delegation to the
exact repository state on which an effect will operate.

That bridge must belong to the target repository's exact released evaluator.
An agent, skill, provider, candidate checkout, or persisted envelope cannot be
allowed to assert that the repository is current or to mint its own mutation
authority.

## Preconditions and trigger

- The target is a standard repository with a valid managed lock and a provable
  exact released evaluator outside the checkout.
- One work order is approved and started through the managed workflow.
- The work order contains a valid advance-delegation declaration approved with
  the work order and bounded to named decision rights, operations, paths,
  profiles, evidence, expiry, retry, and writer limits.
- Current gates required before the requested operation pass.
- A declared single-agent worker requests one supported governed operation.

## Required response

- Observe all repository inputs that can affect safe admission, including Git
  identity and state, relevant formal-artifact state, managed-lock identity,
  selected-work-order identity and digest, filesystem properties, and exact
  evaluator identity.
- Require two identical canonical observations before deriving an envelope.
- Resolve the requested operation against the recorded delegation, approved
  contracts, current workflow state, current gates, and work-order execution
  scope.
- Derive an in-memory, least-authority envelope containing only the operation,
  paths, decision right, worker profile, evidence obligation, limits, expiry,
  and current-state fingerprint needed for that request.
- Bind the envelope to a unique nonce and the exact evaluator identity and make
  it single-use.
- Perform a fresh observation immediately before effect admission and reject a
  stale, replayed, widened, ambiguous, or unsupported request.
- After each admitted effect, bind the next request to the verified receipt's
  `state_after` without widening the original work-order delegation.
- Persist normalized derivation and admission evidence, not the reusable
  authority-bearing envelope itself.

## Failure and boundary behavior

- A changed observation, dirty or unsupported Git state, invalid lock,
  evaluator mismatch, work-order digest mismatch, undeclared right, path, or
  profile, expired delegation, reused nonce, missing gate, or ambiguous
  filesystem identity fails closed before mutation.
- A failed derivation or admission changes no repository, Git, lifecycle,
  credential, network, or external state.
- Provider tool permission, skill discovery, process identity, a previous
  receipt, or possession of serialized envelope-shaped data supplies no
  authority.
- A post-effect state may advance the state chain only when an evaluator-
  verified receipt proves the exact preceding admitted effect.
- Approval, verification decision, release decision, delivery selection, Git
  mutation, credential use, network use, and external actions remain human
  stops unless separately governed by an approved future contract.

## Constraints

- Initial concurrency is one active writer and one selected work order per
  target repository.
- Envelope derivation is deterministic for the same normalized request,
  delegation, policy, evaluator identity, and observation except for the
  evaluator-generated nonce and bounded timestamps.
- Repository observations and fingerprints contain no secrets or hidden model
  reasoning.
- An envelope cannot outlive its delegation, selected work-order state,
  evaluator identity, repository-state binding, or configured short expiry.
- Published 0.6.0 behavior remains immutable; this capability requires a
  separately governed successor release before it can govern a real target.

## Acceptance examples

### Example: stable delegated request

**Given** a started work order delegates one `change-bundle-apply` operation to
one worker profile for `se_harness/observer.py` and its tests

**When** the exact released evaluator obtains two identical observations and
all current gates pass

**Then** it derives one in-memory envelope bound to that operation, those
paths, that worker, the current fingerprint, and one unique nonce.

### Example: repository changes before effect

**Given** an envelope was derived from a stable observation

**When** another process changes the worktree before effect admission

**Then** the fresh observation differs, admission fails, the nonce cannot be
reused, and no requested bytes are applied.

### Example: chained admitted effects

**Given** one admitted effect produces a verified receipt whose `state_after`
matches the actual repository

**When** the same worker requests a second operation within the original
delegation

**Then** the evaluator may derive a new envelope bound to that verified
`state_after`; the first envelope is not reused and no scope is widened.

## Open decisions

Before approval, specifications and ADRs must close the canonical observation
fields, normalization and hashing rules, dirty-state policy, delegation schema,
envelope expiry and nonce storage, supported operation catalog, state-chain
algorithm, evaluator identity proof, evidence redaction, and crash recovery.
