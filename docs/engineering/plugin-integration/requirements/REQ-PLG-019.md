+++
id = "REQ-PLG-019"
type = "requirement"
title = "Retain real evidence through existing procedures"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-10"
statement = "WHEN an operator requests evidence preparation, THE EVIDENCE SKILL SHALL retain observed results through the existing verification or release procedure without treating preparation as an accountable decision."
verification_method = ["test", "inspection"]
priority = "must"
source = "PR #360 and owner plugin-installation feedback, 2026-09-08"

[relations]
derives_from = ["CAP-WEX-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-10T18:16:56Z"
decided_by = "requirements-steward"
reason = "The operator previously stated \"i approve the packets, i authorize the work\" for the reviewed plugin proposal, then on 2026-09-10 explicitly selected \"WO-PLG-010 next, followed by WO-PLG-011 and WO-PLG-012  (delegated route)\". Record only REQ-PLG-019 approval under requirements-steward, from proposal 0b42325b75bc6d1c36897369687c3d3ed578bdb9; reviewed/current draft SHA-256 82b2c144ab5f06a05c58600fa8ee80315a0864f8f871166f846b230c17944bf8. The definition meaning is unchanged from the reviewed packet. Assurance of implementation, release and PR merge remain separate human decisions."
+++

# Requirement: Retain real evidence through existing procedures

## In plain words

The agent records what actually happened and checked. Preparing a record leaves its human decision pending.

## Why

An output without an observed result can mislead reviewers. Recorded facts cannot replace an approval.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| Evidence preparation requested | Retain actual results through the selected procedure | Report missing evidence or authority |

## Examples

### Normal

**Given** authorized preparation and retained checks.

**When** the agent prepares its result.

**Then** the record identifies the real candidate and observations.

### Failure

**Given** a failed check or missing owner decision.

**When** the agent reaches that boundary.

**Then** the result remains incomplete or awaiting that decision.
