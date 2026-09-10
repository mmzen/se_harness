+++
id = "REQ-PLG-020"
type = "requirement"
title = "Preserve read-only project orientation"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-10"
statement = "WHEN project orientation is requested, THE ORIENTATION SKILL SHALL preserve its existing read-only procedure while resolving its evaluator and helper paths through the plugin installation."
verification_method = ["test", "inspection"]
priority = "must"
source = "PR #360 and owner plugin-installation feedback, 2026-09-08"

[relations]
derives_from = ["CAP-WEX-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-10T18:19:50Z"
decided_by = "requirements-steward"
reason = "The operator previously stated \"i approve the packets, i authorize the work\" for the reviewed plugin proposal, then on 2026-09-10 explicitly selected \"WO-PLG-010 next, followed by WO-PLG-011 and WO-PLG-012  (delegated route)\". Record only REQ-PLG-020 approval under requirements-steward, from proposal 0b42325b75bc6d1c36897369687c3d3ed578bdb9; reviewed/current draft SHA-256 c1212dba5660c81dd86c9bb26d1d368ca6cbeb4d09a99cb959bf3b5691cf12da. The definition meaning is unchanged from the reviewed packet. Assurance of implementation, release and PR merge remain separate human decisions."
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
