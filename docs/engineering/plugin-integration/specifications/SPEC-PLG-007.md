+++
id = "SPEC-PLG-007"
type = "specification"
title = "Verified session governance delivery"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-10"
contract = "Session governance is ready only after current installation verification and complete delivery of its managed gate and harness router."

[relations]
specifies = ["REQ-PLG-010", "REQ-PLG-011", "REQ-PLG-012"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-10T06:11:30Z"
decided_by = "technical-owner"
reason = "The operator explicitly approved the reviewed plugin packets in this task: \"i approve the packets, i authorize the work\". On 2026-09-10 they selected \"we will merge later: GO for WO-PLG-007  and then WO-PLG-008\" after deciding DEC-PLG-001 and DEC-PLG-002 for the tested Windows activation routes. Record only the named definitions decision for the D04 governing chain or WO-PLG-007, from reviewed proposal 0b42325b. Sibling work-order states, completion, assurance, release and merge remain separate."
+++

# Specification: Verified session governance delivery

## In plain words

Startup, resume and compaction recovery deliver the repository's verified rules.

## Scope

`session-context.py` only; SPEC-PLG-001/002 own runtime, SPEC-PLG-005/006 host registration.

## Terms

- **Governance context.** The verified managed gate and complete harness router.

## Rules

**PLG-CTX-001.** The handler MUST verify current runtime identity and repository integrity through the released evaluator before delivery.

**PLG-CTX-002.** The handler MUST deliver the complete managed `AGENTS.md` gate and `ENGINEERING_HARNESS.md` router before readiness.

**PLG-CTX-003.** Supported resume and compaction-restoration events MUST repeat verification and delivery using current inputs.

**PLG-CTX-004.** Incomplete delivery MUST require a supported complete read of the verified content before readiness.

**PLG-CTX-005.** The handler MUST remain read-only; prior readiness, summaries and successful hook execution MUST NOT establish complete delivery.

**PLG-CTX-006.** Content returned directly or through fallback MUST match the verified bytes; changed content MUST be rejected and verified again before readiness.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| Identity or integrity fails | Keep context unready; return the existing evaluator finding. | Existing evaluator diagnostic |
| Output limit or unavailable fallback | Require complete verified reading, or report delivery blocked. | Explicit delivery blocker |
| Content changes after verification | Reject changed content; reverify before returning it or declaring readiness. | Verification-to-delivery mismatch |

## Examples

**Given** incomplete restored context, **when** delivery resumes, **then** PLG-CTX-003, PLG-CTX-004 and PLG-CTX-006 require current verification and a complete matching read before readiness.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-PLG-010` | PLG-CTX-001, PLG-CTX-002, PLG-CTX-005, PLG-CTX-006 |
| `REQ-PLG-011` | PLG-CTX-003, PLG-CTX-006 |
| `REQ-PLG-012` | PLG-CTX-004, PLG-CTX-005, PLG-CTX-006 |

## Not decided here

- Host transport and activation.
- Existing governance rules and authority.
