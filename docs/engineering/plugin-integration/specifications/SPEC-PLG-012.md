+++
id = "SPEC-PLG-012"
type = "specification"
title = "Retained orientation and explicit operator briefing"
status = "draft"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-08"
contract = "The plugin preserves existing read-only orientation and explicit briefing contracts while adapting their installation paths and verified evaluator invocation."

[relations]
specifies = ["REQ-PLG-020", "REQ-PLG-021"]
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
