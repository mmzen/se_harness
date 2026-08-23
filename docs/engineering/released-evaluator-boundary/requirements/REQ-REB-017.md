+++
id = "REQ-REB-017"
type = "requirement"
title = "Rehearse the complete governance migration before release"
status = "approved"
owners = ["requirements-steward", "quality-owner", "security-owner", "release-owner"]
created = "2026-08-23"
updated = "2026-08-23"
statement = "WHEN a migration-required successor is qualified for release, THE SYSTEM SHALL execute a deterministic no-credential predecessor-to-successor rehearsal covering preparation, complete validation, rejection, replacement, hosted assessment, release and publication planning, rendering, and separately gated post-publication adoption, and SHALL fail qualification if the rehearsal cannot preserve every declared authority and immutability boundary."
verification_method = "automated-cross-version-migration-rehearsal"

[relations]
derives_from = ["CAP-REB-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T07:56:21Z"
decided_by = "requirements-steward"
+++

# Requirement: Rehearse the complete governance migration before release

## Rationale

The 0.6.0 release exercised each missing transition only after the previous attempt failed. A pre-release rehearsal must execute the complete handover as one sequence, including the failure and successor path that ordinary happy-path CI did not cover.

The rehearsal is evidence, not a real release. Accountable decisions are represented by explicit immutable fixtures and are never inferred by the runner. Publication, deployment, credential use, and operational root adoption are planned or simulated only.

## Preconditions and trigger

- `REQ-REB-016` has classified the successor as migration-required and supplied a valid machine-readable contract.
- Exact predecessor evaluator bytes and an exact successor candidate source or non-promotable package are locally available.
- The rehearsal target is disposable and contains no production credentials or operational repository state.

## Required response

The rehearsal must execute and independently check this ordered sequence:

1. The released predecessor prepares the predecessor-compatible release proposal or equivalent readiness artifact.
2. The successor validates the complete graph using successor semantics without mutating root authority.
3. A fixture-owned accountable rejection is replayed, and the rejected record remains immutable, terminal, visible, and non-authoritative.
4. A corrected successor proposal is created without reopening the rejected record or letting rejected history reserve active authority.
5. Hosted assessment is simulated with the declared evaluator and exact view for each claim.
6. Release and publication inputs are resolved read-only; no tag, release, package upload, maintenance ref, or deployment is created.
7. The governance snapshot is rendered through the declared evaluator/view pair and reconciled to the selected successor proposal.
8. Only after a simulated immutable public successor fact, a distinct upgrade transaction plans and applies adoption in the disposable root; the predecessor remains selected before that explicit step.

The result must bind every input and stage output, record allowed mutations and before/after snapshots, identify decisions as fixture facts rather than automation, and state every external action not performed.

## Failure and boundary behavior

The first failed, missing, reordered, skipped, ambiguous, or undeclared stage stops the rehearsal. Later stages do not run. A failure report identifies the last completed stage and proves that the operational source, root evaluator, lifecycle records outside the disposable fixture, Git refs, credentials, and external services were unchanged.

## Constraints

- Core rehearsal execution is local and receives no network or credential capability. A hosted lane may acquire an already public predecessor package in a separate unprivileged step, verify its declared digest, and then pass only local paths to the runner.
- Candidate and predecessor runtimes execute in separate isolated environments outside the target checkout.
- The fixture may replay human decisions but must not claim that automation made or approved them.
- No diagnostic is converted into success by substring matching or an accepted-error allowlist.
- The exact 0.5.0-to-0.6.0 incident path is a required regression scenario, but the contract and runner must support future N-1-to-N fixtures without embedding those version numbers in the protocol.

## Acceptance examples

### Example: normal behavior

**Given** pinned predecessor N-1 bytes, an exact candidate N, and a disposable migration fixture

**When** the rehearsal runs twice on supported platforms

**Then** both canonical results agree on roles, stages, views, identities, authority effects, and zero external actions, and the disposable root selects N only in the final separately modeled adoption stage.

### Example: failure behavior

**Given** candidate N writes the root lock during validation, a rejection fixture lacks accountable attribution, or publication planning attempts to use a credential

**When** the affected stage runs

**Then** the rehearsal fails at that stage, later stages remain unexecuted, and all non-disposable state is unchanged.

## Open decisions

No product decision remains open after the owners accept the stage catalog and authority model in the accompanying specification and ADR. Fixture filenames, helper names, and temporary-directory layout remain implementation choices.
