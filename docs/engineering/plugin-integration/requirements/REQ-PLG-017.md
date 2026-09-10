+++
id = "REQ-PLG-017"
type = "requirement"
title = "Change workflow through existing engine operations"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-10"
statement = "WHEN guiding artifact packages or work orders, THE CHANGE SKILL SHALL use existing evaluator operations and installed authoring rules for the selected change."
verification_method = ["test"]
priority = "must"
source = "PR #360 at 9e894e99; plugin implementation request, 2026-09-08"

[relations]
derives_from = ["CAP-WEX-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-10T18:11:56Z"
decided_by = "requirements-steward"
reason = "The operator previously stated \"i approve the packets, i authorize the work\" for the reviewed plugin proposal, then on 2026-09-10 explicitly selected \"WO-PLG-010 next, followed by WO-PLG-011 and WO-PLG-012  (delegated route)\". Record only REQ-PLG-017 approval under requirements-steward, from proposal 0b42325b75bc6d1c36897369687c3d3ed578bdb9; reviewed/current draft SHA-256 d3eceab43b26eb2cb2230c4c500d8aa2990597f91ef72e8a341e15b0d3f05594. The definition meaning is unchanged from the reviewed packet. Assurance of implementation, release and PR merge remain separate human decisions."
+++

# Requirement: Change workflow through existing engine operations

## In plain words

The change skill explains and performs the existing workflow. It connects drafting, review and bounded implementation without introducing a new lifecycle engine.

## Why

Using familiar names is insufficient if the skill silently changes what an approval or command means. Draft creation must remain distinct from approval, and work-order approval distinct from start. Current evaluator results govern the next applicable operation.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| An authorized request selects artifact drafting, amendment or work-order execution. | Read applicable installed rules and use supported evaluator operations for that stage. | Preserve actual partial results and stop the affected operation on a reported blocker. |

## Examples

### Normal

**Given** a request authorizing preparation of a draft artifact package,

**When** the change skill creates and validates its records,

**Then** new definitions and work orders remain draft; decision records remain open. Creation supplies no approval or disposition.

### Failure

**Given** a requested amendment requires an unsupported transition,

**When** the skill evaluates the next operation,

**Then** it reports the unsupported path instead of inventing a reopen command or changing lifecycle semantics.
