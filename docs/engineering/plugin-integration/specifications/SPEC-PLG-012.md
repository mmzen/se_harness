+++
id = "SPEC-PLG-012"
type = "specification"
title = "Retained orientation and explicit operator briefing"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-10"
contract = "The plugin preserves existing read-only orientation and explicit briefing contracts while adapting their installation paths and verified evaluator invocation."

[relations]
specifies = ["REQ-PLG-020", "REQ-PLG-021"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-10T18:19:50Z"
decided_by = "technical-owner"
reason = "The operator previously stated \"i approve the packets, i authorize the work\" for the reviewed plugin proposal, then on 2026-09-10 explicitly selected \"WO-PLG-010 next, followed by WO-PLG-011 and WO-PLG-012  (delegated route)\". Record only SPEC-PLG-012 approval under technical-owner, from proposal 0b42325b75bc6d1c36897369687c3d3ed578bdb9; reviewed/current draft SHA-256 6c1b3287986bc23393deebed63cd87934e5a2a91fcab367de86c233ed9d17ea8. The definition meaning is unchanged from the reviewed packet. Assurance of implementation, release and PR merge remain separate human decisions."
+++

# Specification: Retained orientation and explicit operator briefing

## In plain words

Existing inspection and briefing retain their limits. The plugin supplies their location and verified command inputs.

## Scope

This contract covers the retained read-only skills. Their existing skill contracts remain authoritative; SPEC-PLG-011 owns evidence preparation.

## Terms

- **Retained contract.** The existing skill procedure, input bounds, output schema, and prohibited effects.

## Rules

**PLG-RO-001.** The plugin MUST preserve harness-orient's existing identity, doctor, validation, inspection and optional selected-projection procedure.

**PLG-RO-002.** Orientation MUST remain single-agent and read-only; its receipt stays inline and MUST NOT become repository evidence automatically.

**PLG-RO-003.** The plugin MUST activate harness-operator-brief only when explicitly named, using its existing bounded supplied-source contract.

**PLG-RO-004.** Briefing MUST preserve protected bytes, decision meaning, output schemas and zero-change evidence through the existing check_brief helper.

**PLG-RO-005.** Both skills MUST receive absolute verified evaluator arguments and trusted plugin helper paths without ambient command lookup.

**PLG-RO-006.** Path adaptation MUST NOT restore retired writing skills, execution brokers, or authority envelopes.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| Invalid identity, source mismatch, or implicit briefing | Stop without mutation or automatic repair. | existing skill diagnostic |

## Examples

**Given** a source digest mismatch, **when** an explicit brief is checked, **then** it is refused without rewriting the source (PLG-RO-003, PLG-RO-004).

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-PLG-020` | PLG-RO-001, PLG-RO-002, PLG-RO-005, PLG-RO-006 |
| `REQ-PLG-021` | PLG-RO-003, PLG-RO-004, PLG-RO-005, PLG-RO-006 |

## Not decided here

- Existing skill input/output schemas.
- No automatic briefing stage.
