+++
id = "REQ-PLG-024"
type = "requirement"
title = "Bound optional helpers to read-only findings"
status = "draft"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "WHEN an optional helper is used, THE PLUGIN SHALL restrict it to read-only findings within the supplied scope while retaining decisions and implementation with the main workflow."
verification_method = ["test", "inspection"]
priority = "must"
source = "PR #360 and owner plugin-installation feedback, 2026-09-08"

[relations]
derives_from = ["CAP-WEX-001"]
+++

# Requirement: Bound optional helpers to read-only findings

## In plain words

An optional helper inspects a named topic and reports findings. It cannot change files, approve work, or replace the main agent.

## Why

Delegation can hide additional effects or confuse accountability. Actual permissions must match the limited role.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| Optional helper requested | Return scoped read-only findings | Use the main agent if the host cannot enforce restrictions |

## Examples

### Normal

**Given** a host enforcing read-only access.

**When** a helper inspects the supplied scope.

**Then** it returns findings without changing state.

### Failure

**Given** a host unable to restrict helper tools.

**When** assistance is requested.

**Then** the main agent continues without spawning a helper.
