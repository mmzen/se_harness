+++
id = "REQ-PLG-024"
type = "requirement"
title = "Bound optional helpers to read-only findings"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-10"
statement = "WHEN an optional helper is used, THE PLUGIN SHALL restrict it to read-only findings within the supplied scope while retaining decisions and implementation with the main workflow."
verification_method = ["test", "inspection"]
priority = "must"
source = "PR #360 and owner plugin-installation feedback, 2026-09-08"

[relations]
derives_from = ["CAP-WEX-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-10T06:11:30Z"
decided_by = "requirements-steward"
reason = "The operator explicitly approved the reviewed plugin packets in this task: \"i approve the packets, i authorize the work\". On 2026-09-10 they selected \"we will merge later: GO for WO-PLG-007  and then WO-PLG-008\" after deciding DEC-PLG-001 and DEC-PLG-002 for the tested Windows activation routes. Record only the named definitions decision for the D04 governing chain or WO-PLG-007, from reviewed proposal 0b42325b. Sibling work-order states, completion, assurance, release and merge remain separate."
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
