+++
id = "REQ-PLG-018"
type = "requirement"
title = "Continue covered work without repeated approval prompts"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-10"
statement = "WHEN a next workflow action remains covered by current authority, THE CHANGE SKILL SHALL continue without requesting a duplicate invocation or decision."
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
reason = "The operator previously stated \"i approve the packets, i authorize the work\" for the reviewed plugin proposal, then on 2026-09-10 explicitly selected \"WO-PLG-010 next, followed by WO-PLG-011 and WO-PLG-012  (delegated route)\". Record only REQ-PLG-018 approval under requirements-steward, from proposal 0b42325b75bc6d1c36897369687c3d3ed578bdb9; reviewed/current draft SHA-256 3be75120e7f5f935170b16d88016ddf4ea71d2b2b67b91138d234db0ce54ac0c. The definition meaning is unchanged from the reviewed packet. Assurance of implementation, release and PR merge remain separate human decisions."
+++

# Requirement: Continue covered work without repeated approval prompts

## In plain words

The user should not need to restart the skill or repeat an unchanged decision at every stage. The agent continues while the actual request and authority still cover its next action.

## Why

A useful harness preserves both momentum and accountable decisions. An evaluator next step describes an action; it does not grant permission. Missing authority, changed content or a failed gate remains a real stop, even when earlier work was authorized.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| The evaluator identifies the next applicable action within an existing request. | Reuse actual decisions that still cover the exact action and relevant inputs. | Stop only the affected action when authority is absent, materially changed or blocked. |

## Examples

### Normal

**Given** an authorized work order start has completed and its scope remains unchanged,

**When** the evaluator identifies in-scope implementation,

**Then** the agent proceeds without another skill invocation or redundant approval prompt.

### Failure

**Given** the next edit exceeds the approved work-order scope,

**When** the agent identifies that change,

**Then** it pauses the affected implementation for the missing decision; an actor argument cannot supply approval.
