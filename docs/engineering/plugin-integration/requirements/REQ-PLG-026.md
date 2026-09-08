+++
id = "REQ-PLG-026"
type = "requirement"
title = "Report timing and prompt measurements"
status = "draft"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "WHEN plugin qualification measures workflow overhead, THE QUALIFICATION PROCESS SHALL report startup, tool-check and total-operation durations, together with operator-prompt counts and their measurement conditions."
verification_method = ["test", "inspection"]
priority = "must"
source = "PR #360 and owner plugin-installation feedback, 2026-09-08"
measure = "Milliseconds for durations; operator prompts per operation; every sample identifies its conditions."

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Report timing and prompt measurements

## In plain words

The report separates time spent starting, checking tools, and completing work. It also counts interruptions requiring operator input.

## Why

A demonstration can hide repeated startup costs or prompts. Measurements expose the tradeoff under visible conditions.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| Workflow overhead measured | Report durations and prompt counts with conditions | Retain missing samples without presenting them as zero |

## Examples

### Normal

**Given** a repeatable qualification scenario.

**When** timing and prompts are measured.

**Then** the report separates startup, checks, total duration, and prompts.

### Failure

**Given** a sample is interrupted.

**When** the report is prepared.

**Then** the missing sample is identified rather than assigned zero.
