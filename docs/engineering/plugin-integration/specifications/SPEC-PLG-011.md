+++
id = "SPEC-PLG-011"
type = "specification"
title = "Evidence skill using existing lifecycle procedures"
status = "draft"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-08"
contract = "Evidence preparation retains observed results and follows existing verification and release procedures while leaving accountable decisions with their owners."

[relations]
specifies = ["REQ-PLG-019"]
+++

# Specification: Evidence skill using existing lifecycle procedures

## In plain words

The agent prepares evidence for selected work. It reports facts and the next real decision without inventing approval.

## Scope

This contract governs the evidence skill. Existing workflow and provenance contracts retain lifecycle authority; SPEC-PLG-012 covers the separate read-only skills.

## Terms

- **Preparation.** Recording evidence before the separate accountable decision.

## Rules

**PLG-EVD-001.** The evidence skill MUST follow the selected procedure from WORKFLOW.json using the exact verified external evaluator.

**PLG-EVD-002.** Retained evidence MUST identify actual commands, outcomes, candidate identity and relevant files; missing or failed observations MUST remain visible.

**PLG-EVD-003.** The skill MUST classify `check --checkpoint handoff --from-git BASE`, `evidence`, `capture-verification`, and `prepare-release` as writing operations, distinct from read-only preflight.

**PLG-EVD-004.** Record preparation MUST remain separate from the assurance or release decision; the skill MUST NOT supply approval on the owner's behalf.

**PLG-EVD-005.** The skill MUST retain unchanged valid authority and stop at missing decisions, failed prerequisites, changed scope, or uncertain effects.

**PLG-EVD-006.** Agent merge or publication MUST require exact action authority and demonstrated independent external enforcement; otherwise the skill MUST report the automation blocker.

**PLG-EVD-007.** When required, capture-verification MUST bind the clean committed candidate; the resulting VREC MUST be retained in a later governance commit, never its own bound candidate.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| Missing check or owner decision | Report the missing fact or decision; do not invent success. | existing evaluator refusal or missing decision |
| Handoff check has writing effects | Require covered write authority and retain the resulting evidence changes. | actual operation result |
| Dirty or uncommitted verification candidate | Stop capture; preserve results for the required candidate commit. | existing capture refusal |

## Examples

**Given** a failed check, **when** evidence is prepared, **then** that failure remains visible and assurance remains undecided (PLG-EVD-002, PLG-EVD-004).

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-PLG-019` | PLG-EVD-001, PLG-EVD-002, PLG-EVD-003, PLG-EVD-004, PLG-EVD-005, PLG-EVD-006, PLG-EVD-007 |

## Not decided here

- Project-specific build and release commands.
- Lifecycle predicates and external authorization.
