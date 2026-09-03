+++
id = "REQ-DCM-001"
type = "requirement"
title = "An open decision blocks the transitions it names"
status = "approved"
owners = ["product-owner", "technical-owner", "quality-owner"]
created = "2026-09-03"
updated = "2026-09-03"
statement = "WHEN a decision artifact in status open names an artifact in its blocks relation, THE SYSTEM SHALL refuse every lifecycle transition of that artifact until the decision is decided, withdrawn, or deferred with a scope that admits the transition."
verification_method = ["test"]
priority = "must"
source = "docs/notes/decision-artifact-proposal-2026-09-03.md; the Lineage prefetch deviation under WO-DST-023 (2026-09-01), recorded only as prose"
measure = "zero transitions applied to a blocked artifact while its decision is open, on every fixture and on the repository"

[relations]
derives_from = ["CAP-DCM-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-03T19:10:33Z"
decided_by = "product-owner"
reason = "Approved by the accountable repository owner on 2026-09-03 with the instruction 'i approve with execution delegation', after reviewing the decision-artifact proposal and the drafted packet. WO-DCM-001 carries the delegation class: this approval delegates DR-WO-START, DR-WO-COMPLETE and DR-VREC-PREPARE to the delegated-executor role under the required validate check, with the class read from the pull request's base."
+++

# Requirement: An open decision blocks the transitions it names

## Rationale

A pending decision that does not block is a note. The owner's instruction
is that an unresolved decision stops the work it concerns, and that only an
explicit act by the accountable role lets the work continue. Today the only
mechanical check is that the `## Open decisions` section of one artifact
reads `None` at its own approval; a decision met during execution stops
nothing, and a decision that spans artifacts cannot be expressed.

Fail-closed is the harness's standing rule (`HRN-008`): a warning is not
acceptance. A decision therefore blocks by being `open`, and nothing but a
decision moves it.

## Behavior

- Trigger: a lifecycle transition is requested for an artifact named in the
  `blocks` relation of a decision whose status is `open`, or `deferred`
  with a scope that does not admit the requested transition.
- Response: the transition is refused before any state changes. The refusal
  names the decision, its question, its options and the role that must
  decide, and prints the disposing command as the corrective step.
- On failure: a decision that cannot be read, or whose `blocks` target does
  not exist, is a graph error; the transition is refused with that error.

## Assumptions and dependencies

- The workflow contract evaluates gates at every checkpoint of every
  artifact family; the decision gate joins those predicates.
- A deferral carries a scope of admitted transitions and a revisit trigger
  (`SPEC-DCM-001`).
- Decisions below the authoring threshold are not artifacts and do not
  block; the threshold is stated in `ARTIFACT_AUTHORING.md`.

## Acceptance examples

### Example: an open question blocks approval

**Given** `DEC-X-001` is `open` and blocks `REQ-X-004` and `WO-X-002`,

**When** the actor requests `REQ-X-004=approved`,

**Then** the transition is refused, no state changes, and the result names
`DEC-X-001`, its options and the disposing command.

### Example: a scoped deferral admits one transition

**Given** `DEC-X-001` is `deferred` with a scope that admits
`WO-X-002: approved -> in_progress` and a revisit trigger,

**When** the actor requests `WO-X-002=in_progress`,

**Then** the transition proceeds; a later request for
`WO-X-002=implemented` is refused until the decision is decided.

## Open decisions

None.
