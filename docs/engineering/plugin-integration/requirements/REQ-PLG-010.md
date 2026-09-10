+++
id = "REQ-PLG-010"
type = "requirement"
title = "Verified governance context at session start"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-10"
statement = "WHEN a governed session starts, THE SESSION HANDLER SHALL provide the verified managed agent gate and complete harness router before declaring governance context ready."
verification_method = ["test"]
priority = "must"
source = "PR #360 at 9e894e99; plugin implementation request, 2026-09-08"

[relations]
derives_from = ["CAP-IAR-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-10T06:11:30Z"
decided_by = "requirements-steward"
reason = "The operator explicitly approved the reviewed plugin packets in this task: \"i approve the packets, i authorize the work\". On 2026-09-10 they selected \"we will merge later: GO for WO-PLG-007  and then WO-PLG-008\" after deciding DEC-PLG-001 and DEC-PLG-002 for the tested Windows activation routes. Record only the named definitions decision for the D04 governing chain or WO-PLG-007, from reviewed proposal 0b42325b. Sibling work-order states, completion, assurance, release and merge remain separate."
+++

# Requirement: Verified governance context at session start

## In plain words

The agent starts with the repository's real governance instructions. A plugin summary is insufficient: the managed gate and the complete document it routes to must be available.

## Why

Instructions from a damaged installation or the wrong evaluator can describe a different authority boundary. Readiness depends on verified source content, not merely successful hook execution. Existing governance remains authoritative; this requirement adds reliable delivery.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| Governed session starts after runtime setup. | Current verified gate and complete router reach the session before readiness. | Report the failed prerequisite; governance context remains unready. |

## Examples

### Normal

**Given** a ready runtime matching an intact repository installation,

**When** the session-start handler runs,

**Then** the agent receives the managed `AGENTS.md` block and full `ENGINEERING_HARNESS.md`, with their verified identity.

### Failure

**Given** the managed gate has been altered,

**When** the handler checks the repository,

**Then** it reports the mismatch without presenting those bytes as verified governance.
