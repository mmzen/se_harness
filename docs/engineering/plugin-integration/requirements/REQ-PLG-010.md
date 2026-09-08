+++
id = "REQ-PLG-010"
type = "requirement"
title = "Verified governance context at session start"
status = "draft"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "WHEN a governed session starts, THE SESSION HANDLER SHALL provide the verified managed agent gate and complete harness router before declaring governance context ready."
verification_method = ["test"]
priority = "must"
source = "PR #360 at 9e894e99; plugin implementation request, 2026-09-08"

[relations]
derives_from = ["CAP-IAR-001"]
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
