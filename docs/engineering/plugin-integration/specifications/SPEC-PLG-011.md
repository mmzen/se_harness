+++
id = "SPEC-PLG-011"
type = "specification"
title = "Evidence skill using existing lifecycle procedures"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-10"
contract = "Evidence preparation retains observed results and follows existing verification and release procedures while leaving accountable decisions with their owners."

[relations]
specifies = ["REQ-PLG-019"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-10T18:16:56Z"
decided_by = "technical-owner"
reason = "The operator previously stated \"i approve the packets, i authorize the work\" for the reviewed plugin proposal, then on 2026-09-10 explicitly selected \"WO-PLG-010 next, followed by WO-PLG-011 and WO-PLG-012  (delegated route)\". Record only SPEC-PLG-011 approval under technical-owner, from proposal 0b42325b75bc6d1c36897369687c3d3ed578bdb9; reviewed/current draft SHA-256 de2a163e92a3702141ee4a10108b0ac6dbc7ac3cd783b36da11bf7bf21781bb1. The definition meaning is unchanged from the reviewed packet. Assurance of implementation, release and PR merge remain separate human decisions."
+++

# Specification: Evidence skill using existing lifecycle procedures

## In plain words

Prepare observed evidence and identify the next accountable decision.

## Scope

Existing workflow/provenance rules govern lifecycle decisions; SPEC-PLG-012 covers read-only skills.

## Terms

- **Preparation.** Recording evidence before the separate accountable decision.
- **Applicable authority.** Action inputs match SPEC-PLG-010's applicability rules.

## Rules

**PLG-EVD-001.** The skill MUST follow the selected WORKFLOW.json procedure using the exact verified external evaluator.

**PLG-EVD-002.** Retained evidence MUST identify actual commands, outcomes, candidate identity and relevant files; missing or failed observations MUST remain visible.

**PLG-EVD-003.** The skill MUST classify `check --checkpoint handoff --from-git BASE`, `evidence`, `capture-verification`, and `prepare-release` as writing operations, distinct from read-only preflight.

**PLG-EVD-004.** Record preparation MUST remain separate from the assurance or release decision; the skill MUST NOT supply approval on the owner's behalf.

**PLG-EVD-005.** The skill MUST reuse applicable authority under SPEC-PLG-010; changed inputs, missing authority, failed gates or uncertain effects MUST stop affected actions.

**PLG-EVD-006.** Agent merge or publication MUST require exact action authority and demonstrated independent external enforcement; otherwise the skill MUST report the automation blocker.

**PLG-EVD-007.** When required, capture-verification MUST bind the clean committed candidate; the resulting VREC MUST be retained in a later governance commit, never its own bound candidate.

**PLG-EVD-008.** The skill MUST refuse governed writes until current verified governance context is established, and route readiness recovery through setup.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| Missing check or owner decision | Report the missing fact or decision | Existing refusal or missing right |
| Writing handoff lacks applicable authority | Stop before evidence changes | Missing write authority |
| Candidate changed, dirty or uncommitted | Stop the affected candidate-bound operation | Identity mismatch or capture refusal |
| Governance context unestablished | Refuse governed writes; recover through setup | Readiness blocker |

## Examples

**Given** unestablished context, **when** writing evidence is requested, **then** PLG-EVD-008 refuses the write.

**Given** authority for candidate A, **when** candidate B is selected, **then** PLG-EVD-005 stops reuse of candidate A's decision.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-PLG-019` | PLG-EVD-001, PLG-EVD-002, PLG-EVD-003, PLG-EVD-004, PLG-EVD-005, PLG-EVD-006, PLG-EVD-007, PLG-EVD-008 |

## Not decided here

- Project-specific build and release commands.
- Lifecycle predicates and external authorization; skill instructions are not deterministic enforcement.
