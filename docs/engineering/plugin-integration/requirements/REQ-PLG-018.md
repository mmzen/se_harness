+++
id = "REQ-PLG-018"
type = "requirement"
title = "Continue covered work without repeated approval prompts"
status = "draft"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "WHEN a next workflow action remains covered by current authority, THE CHANGE SKILL SHALL continue without requesting a duplicate invocation or decision."
verification_method = ["test"]
priority = "must"
source = "PR #360 at 9e894e99; plugin implementation request, 2026-09-08"

[relations]
derives_from = ["CAP-WEX-001"]
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
