+++
id = "REQ-PLG-007"
type = "requirement"
title = "Establish the Claude Code activation sequence"
status = "draft"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "WHEN Claude Code compatibility is assessed, THE COMPATIBILITY PROBE SHALL retain a reproducible activation sequence or a specific incompatibility for every assessed host and platform version."
verification_method = ["inspection","demonstration"]
priority = "must"
source = "Owner-reviewed plugin proposal, PR #360 at 9e894e99; granular implementation request of 2026-09-08."

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Establish the Claude Code activation sequence

## In plain words

A small trial shows exactly how Claude Code loads the proposed integration. An unsuccessful trial records what prevents support.

## Why

Documentation and discovery output cannot prove that session events and tool checks reach the intended code.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| A declared Claude Code compatibility trial | Record tested versions, actions, observations, and either a working activation sequence or the precise unsupported step. | Record the failed or unavailable step without claiming support. |

## Examples

### Normal

**Given** an available Claude Code version and a disposable test profile.

**When** the trial exercises discovery and activation.

**Then** the report records the actual sequence and observed events.

### Failure

**Given** the host cannot pass the required event or interpreter input.

**When** the trial reaches that step.

**Then** the report identifies that incompatibility.
