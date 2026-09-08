+++
id = "REQ-PLG-019"
type = "requirement"
title = "Retain real evidence through existing procedures"
status = "draft"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "WHEN an operator requests evidence preparation, THE EVIDENCE SKILL SHALL retain observed results through the existing verification or release procedure without treating preparation as an accountable decision."
verification_method = ["test", "inspection"]
priority = "must"
source = "PR #360 and owner plugin-installation feedback, 2026-09-08"

[relations]
derives_from = ["CAP-WEX-001"]
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
