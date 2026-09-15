+++
id = "SPEC-PLG-014"
type = "specification"
title = "Optional helpers with enforced read-only boundaries"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-14"
contract = "Optional helpers produce scoped read-only findings under enforced host permissions, with the main workflow retaining implementation and every accountable decision."

[relations]
specifies = ["REQ-PLG-024"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-10T06:11:30Z"
decided_by = "technical-owner"
reason = "The operator explicitly approved the reviewed plugin packets in this task: \"i approve the packets, i authorize the work\". On 2026-09-10 they selected \"we will merge later: GO for WO-PLG-007  and then WO-PLG-008\" after deciding DEC-PLG-001 and DEC-PLG-002 for the tested Windows activation routes. Record only the named definitions decision for the D04 governing chain or WO-PLG-007, from reviewed proposal 0b42325b. Sibling work-order states, completion, assurance, release and merge remain separate."
+++

# Optional helpers only for an identified need

## Current scope

Deferred. No current plugin user task requires this component. The normal executor
can investigate, implement and gather evidence through the accepted single route.
Reconsider only after the owner identifies a concrete task for which a helper adds
useful value beyond the ordinary host tools. Helper use is not a workflow route.

## Conditional behavior

If selected later, use the host's existing helper capability with a named task and
inputs. A helper described as read-only must actually have read-only permissions.
If those controls are unavailable, perform the task in the normal workflow. Do not
build a custom permission layer, credential model or host capability matrix.

Return relevant findings and sources. Findings do not approve scope, verify a record
or authorize external actions; the usual workflow retains those decisions. Existing
orient/brief contracts still apply to those skills. Do not invent a helper-specific
receipt or call-count contract for them. REQ-PLG-024 is the conditional boundary.

## Simpler choice

Do no helper implementation now. A later bounded amendment must name the user need,
chosen existing host facility and exact implementation scope. This replaces the old
prospective five-scenario permission/registration matrix and hook-architecture
dependency. It does not relax a claimed read-only permission boundary.

## Prospective amendment — 2026-09-14

The owner requested that all remaining plugin work comply with the accepted KISS changes.
WO-PLG-022 applies that instruction here. Earlier approval events retain their original
dates and meaning. This amendment governs future helper work; it records no implementation
or host acceptance. See [the current plan](../../../notes/plugin-backlog-kiss-2026-09-14.md).
