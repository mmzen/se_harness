+++
id = "REQ-PLG-020"
type = "requirement"
title = "Preserve read-only project orientation"
status = "draft"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "WHEN project orientation is requested, THE ORIENTATION SKILL SHALL preserve its existing read-only procedure while resolving its evaluator and helper paths through the plugin installation."
verification_method = ["test", "inspection"]
priority = "must"
source = "PR #360 and owner plugin-installation feedback, 2026-09-08"

[relations]
derives_from = ["CAP-WEX-001"]
+++

# Requirement: Preserve read-only project orientation

## In plain words

The existing project explanation stays read-only. Installing it through the plugin changes its location, not its permissions.

## Why

Operators rely on the existing inspection contract. New installation cannot turn inspection into setup, implementation, or approval.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| Project orientation requested | Return observations under the retained contract | Report failure without repair or mutation |

## Examples

### Normal

**Given** a valid installed evaluator and selected project.

**When** orientation runs.

**Then** the result describes current state with no changed files.

### Failure

**Given** an invalid evaluator identity.

**When** orientation is requested.

**Then** inspection stops before any helper runs.
