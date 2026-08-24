+++
id = "REQ-AEX-003"
type = "requirement"
title = "Stop at accountable decision points with a canonical decision packet"
status = "approved"
owners = ["product-owner", "requirements-steward", "assurance-owner"]
created = "2026-08-24"
updated = "2026-08-24"
statement = "WHEN autonomous execution reaches an accountable-decision-required decision, exception, failed gate, unresolved scope conflict, or action-time-authorization-required action, THE SYSTEM SHALL stop before the associated effect and emit one canonical decision packet containing the exact subject, candidate identity, required role, gate results, evidence bindings, recommendation, complete alternatives, unresolved findings, effects, non-effects, and exact transition preview or proposed external action."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-AEX-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T09:03:54Z"
decided_by = "requirements-steward"
+++

# Requirement: Stop at accountable decision points with a canonical decision packet

## Rationale

Human-at-the-decision-point succeeds only when the human receives enough
reliable context to decide without reconstructing agent transcripts, raw logs,
or earlier conversations. A generic request for approval preserves interruption
while shifting the information burden to the decision owner.

## Preconditions and trigger

Execution reaches a managed decision right classified as
`accountable-decision-required`, a proposed exception, a failed or
not-assessable required gate, an authority or scope conflict, or an exact action
classified as `action-time-authorization-required`.

## Required response

- Stop before changing lifecycle state or performing the external effect.
- Identify exactly one primary decision and its required accountable role.
- Bind the packet to the selected artifact, candidate commit or current state,
  evaluator observation, and retained evidence digests as applicable.
- Report applicable gates and distinguish pass, fail, and not-assessable.
- Provide one recommendation and every complete authorized alternative.
- State unresolved findings, assumptions, consequences, effects, and
  non-effects.
- Provide a deterministic transition preview, suggested response, or exact
  external action without executing it.
- Render human and JSON forms from the same semantic result.

## Failure and boundary behavior

- Do not guess an accountable role, decision meaning, artifact, candidate, or
  target when any is absent or ambiguous.
- Do not hide failed gates behind a positive recommendation.
- Do not include secrets, private evidence bodies, raw environment data, or
  unrelated repository prose in the normal packet.
- A packet remains a proposal; elapsed time, packet generation, or silence does
  not count as a decision.

## Constraints

- Existing managed workflow result and restitution semantics remain the
  starting compatibility contract.
- A decision packet may summarize retained evidence but must bind the exact
  evidence paths and digests needed for review.
- The system cannot determine whether an accountable human's substantive
  judgment is correct.

## Acceptance examples

### Example: assurance decision

**Given** a ready VREC with exact candidate and evidence bindings

**When** autonomous preparation completes

**Then** execution stops and the packet asks the assurance owner to verify,
reject, or request remediation without transitioning the VREC.

### Example: required gate fails

**Given** an approved work order whose required verification fails

**When** the worker reaches handoff

**Then** the packet reports the exact failure and unchanged lifecycle state,
recommends bounded remediation, and does not ask the owner to approve a
transition that the gate prohibits.

## Open decisions

Before approval, the specification must decide whether decision packets extend
the existing workflow-result schema or form a separately versioned object with
a lossless mapping to current restitution fields.
