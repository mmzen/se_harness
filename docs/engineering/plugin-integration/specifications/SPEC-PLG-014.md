+++
id = "SPEC-PLG-014"
type = "specification"
title = "Optional helpers with enforced read-only boundaries"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-10"
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

# Specification: Optional helpers with enforced read-only boundaries

## In plain words

A helper inspects a bounded question. If the host cannot restrict it, the main agent handles the work.

## Scope

This contract governs optional investigator and evidence-reviewer roles under ARCH-PLG-002. SPEC-PLG-012 retains the separate single-agent orientation contract.

## Terms

- **Helper finding.** An observation returned without execution or decision authority.

## Rules

**PLG-HLP-001.** Each helper request MUST identify selected scope, allowed inputs, expected findings and prohibited effects.

**PLG-HLP-002.** Host registration MUST enforce read-only filesystem access and deny mutation-capable tools, credentials and external actions.

**PLG-HLP-003.** Helpers MUST return scoped observations, sources and uncertainty without approving artifacts, completing work, or claiming independent human assurance.

**PLG-HLP-004.** When the host cannot enforce required restrictions, the main agent MUST continue without spawning that helper.

**PLG-HLP-005.** The main workflow MUST retain implementation, evaluator-driven next steps and accountable decision handoffs.

**PLG-HLP-006.** Helper registration MUST NOT weaken harness-orient or harness-operator-brief's single-agent contracts.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| Host cannot enforce helper restrictions | Continue with the main agent without delegation. | helper unavailable: boundary not enforced |

## Examples

**Given** a host without enforceable read-only helper tools, **when** investigation is requested, **then** the main agent continues without delegation (PLG-HLP-004).

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-PLG-024` | PLG-HLP-001, PLG-HLP-002, PLG-HLP-003, PLG-HLP-004, PLG-HLP-005, PLG-HLP-006 |

## Not decided here

- Helper model choice and task wording within scope.
- No mandatory delegation or assurance claim.
