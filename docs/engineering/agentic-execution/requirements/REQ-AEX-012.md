+++
id = "REQ-AEX-012"
type = "requirement"
title = "Advance delegated execution while preserving accountable stops"
status = "approved"
owners = ["product-owner", "requirements-steward", "technical-owner", "quality-owner"]
created = "2026-08-25"
updated = "2026-08-25"
statement = "WHEN an approved governance record delegates a defined preparatory or execution decision right to a single agent, THE SYSTEM SHALL permit only the corresponding evaluator-governed workflow advancement, produce the required canonical evidence and next-decision packet, and stop before every non-delegated accountable decision or external effect."
verification_method = "inspection-and-automated-test"

[relations]
derives_from = ["CAP-AEX-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T09:08:48Z"
decided_by = "requirements-steward"
+++

# Requirement: Advance delegated execution while preserving accountable stops

## Rationale

Transactional file effects alone do not create useful agentic execution. The
agent must be able to start already-approved work, complete implementation when
objective gates pass, and prepare assurance material without asking for a new
human confirmation at every mechanical boundary. Those rights are safe only
when an accountable owner delegated them in advance and the evaluator can prove
the exact conditions for the requested outcome.

Phase 4 remains single-agent and stops at the assurance decision. Approval,
verification judgment, release judgment, delivery selection, Git mutation, and
external action are not inferred from successful execution.

## Preconditions and trigger

- A valid formal artifact records the accountable owner, delegate identity,
  named decision right, target artifact, allowed outcome, constraints,
  evidence, expiry, state binding, and non-delegable boundaries.
- The selected work order and its governed prerequisites are in the state
  required by the requested workflow operation.
- The target repository's exact released evaluator proves its identity and all
  applicable gates.
- The requested operation is one of the activated Phase 4 rights:
  `DR-WO-START`, `DR-WO-COMPLETE`, or `DR-VREC-PREPARE`.

## Required response

- Resolve the recorded delegation and require an exact match for delegate,
  right, artifact, outcome, state, expiry, and evidence obligation.
- Use evaluator-owned workflow operations for the delegated transition or
  preparation; provider-native files and skills remain non-authoritative.
- Require admitted change-bundle effects and verified receipts for repository
  mutations performed during execution.
- At work-order completion, prove exact changed-path scope, required gates,
  test evidence, receipt-chain continuity, and canonical repository state.
- Prepare a ready verification record or release record only when its approved
  prerequisites and evidence contract are satisfied.
- Produce a canonical decision packet naming outcome, completed and incomplete
  work, current lifecycle state, exact evidence, deviations, uncertainty,
  decision required, one next authorized step, and the exact command or
  response for that step.
- Stop at the first right that is not validly delegated or is explicitly
  non-delegable.

## Failure and boundary behavior

- Missing, ambiguous, expired, stale, mismatched, or overbroad delegation fails
  before lifecycle mutation or preparation.
- A failed gate, incomplete receipt chain, changed path outside scope, missing
  evidence, uncertain rollback, or non-canonical repository state prevents
  completion and assurance preparation.
- The agent cannot approve requirements, architecture, ADRs, specifications,
  verification contracts, or work orders; decide a verification record;
  decide a release record; select delivery; mutate Git; use credentials;
  access the network; publish; deploy; merge; or perform another external
  action under this requirement.
- A runtime prompt, provider permission, skill name, model confidence, or test
  pass cannot substitute for the recorded decision right.

## Constraints

- Initial execution has one worker, one selected work order, one repository,
  and at most one active writer.
- Every delegated workflow operation is independently admitted and recorded;
  delegation is not a standing bearer token.
- Preparation creates a reviewable draft or ready packet, never the owner's
  decision outcome.
- The evaluator restores canonical state and reports one next decision at every
  success, stop, or failure boundary.
- Multi-agent delegation, child delegation, integration coordination, and
  parallel writers remain outside Phase 4.
- `DR-RLS-PREPARE` remains classified as advance-delegable by the approved
  authority model but is not activated by this milestone.
- A successor released evaluator must be installed externally before this
  capability is used to govern a real repository.

## Acceptance examples

### Example: delegated work-order start

**Given** an approved work order delegates `DR-WO-START` to the selected worker
and the start checkpoint passes

**When** the worker requests start

**Then** the evaluator performs the exact managed transition, records the
delegation evidence, and returns the in-progress work-order context.

### Example: assurance preparation and stop

**Given** implementation is complete, receipts and required evidence are
continuous, and `DR-VREC-PREPARE` is delegated

**When** the worker requests assurance preparation

**Then** the evaluator prepares the verification record and decision packet,
then stops for an independent verification decision.

### Example: undelegated release decision

**Given** a release record is ready for decision

**When** the worker requests approval or publication

**Then** the evaluator refuses the request, changes no state, and names the
accountable human decision and exact next action.

## Open decisions

Before approval, specifications and ADRs must close the authoritative
delegation-record location and schema, delegate identity semantics, expiry,
revocation, allowed outcomes, operation-to-right mapping, lifecycle receipts,
decision-packet schema, completion proof, assurance preparation, and exact
Phase 4 terminal boundary.
