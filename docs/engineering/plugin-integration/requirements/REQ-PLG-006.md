+++
id = "REQ-PLG-006"
type = "requirement"
title = "Establish the Codex activation sequence"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "WHEN Codex compatibility is assessed, THE COMPATIBILITY PROBE SHALL retain a reproducible activation sequence or a specific incompatibility for every assessed host and platform version."
verification_method = ["inspection","demonstration"]
priority = "must"
source = "Owner-reviewed plugin proposal, PR #360 at 9e894e99; granular implementation request of 2026-09-08."

[relations]
derives_from = ["CAP-DST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-08T21:39:22Z"
decided_by = "requirements-steward"
reason = "Operator explicitly approved the Codex and Claude probe packets reviewed at be8b4126 in this Codex task: i approve the packets, i authorize the work. Record the selected definition approval only."
+++

# Requirement: Establish the Codex activation sequence

## In plain words

A small trial shows exactly how Codex loads the proposed integration. An unsuccessful trial records what prevents support.

## Why

A written manifest alone does not prove loading, hook activation, or access to the selected interpreter.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| A declared Codex compatibility trial | Record tested versions, actions, observations, and either a working activation sequence or the precise unsupported step. | Record the failed or unavailable step without claiming support. |

## Examples

### Normal

**Given** an available Codex version and a disposable test profile.

**When** the trial exercises discovery and activation.

**Then** the report records the actual sequence and observed events.

### Failure

**Given** the host cannot pass the required event or interpreter input.

**When** the trial reaches that step.

**Then** the report identifies that incompatibility.
