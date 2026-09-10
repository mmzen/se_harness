+++
id = "SPEC-PLG-010"
type = "specification"
title = "Change skill with continuous bounded execution"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-10"
contract = "The change skill follows existing artifact and work-order procedures, continuing covered work while stopping affected actions that lack current authority."

[relations]
specifies = ["REQ-PLG-017", "REQ-PLG-018"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-10T18:11:56Z"
decided_by = "technical-owner"
reason = "The operator previously stated \"i approve the packets, i authorize the work\" for the reviewed plugin proposal, then on 2026-09-10 explicitly selected \"WO-PLG-010 next, followed by WO-PLG-011 and WO-PLG-012  (delegated route)\". Record only SPEC-PLG-010 approval under technical-owner, from proposal 0b42325b75bc6d1c36897369687c3d3ed578bdb9; reviewed/current draft SHA-256 2f76c774f1f44a883e0c9d117085b9d74c795ff452c3c41acf09f3031661f079. The definition meaning is unchanged from the reviewed packet. Assurance of implementation, release and PR merge remain separate human decisions."
+++

# Specification: Change skill with continuous bounded execution

## In plain words

Continue work when existing decisions still apply.

## Scope

Follow existing [authoring](../../ARTIFACT_AUTHORING.md), [workflow](../../WORKFLOW.md) and [decision rights](../../DECISION_RIGHTS.md); SPEC-PLG-011 covers evidence.

## Terms

- **Covered continuation.** Actual authority matches reviewed inputs; current gates pass.

## Rules

**PLG-CHANGE-001.** The skill MUST use inspected released commands and installed authoring rules for selected artifact packages and WO procedures.

**PLG-CHANGE-002.** The skill MUST distinguish creation, approval, start and completion, and inspect partial writes or interruptions before retry.

**PLG-CHANGE-003.** The skill MUST continue covered actions without duplicate invocation or approval; ordinary in-scope commits MUST NOT trigger renewed WO approval.

**PLG-CHANGE-004.** Changed or unavailable reviewed inputs, missing authority or failed gates MUST stop the affected action; unrelated authority MUST NOT substitute.

**PLG-CHANGE-005.** The skill MUST preserve DR-015's limited delegation and MUST NOT treat an evaluator next step or `--decision` assertion as authenticated approval.

**PLG-CHANGE-006.** The skill MUST refuse governed writes until current verified governance context is established, and route readiness recovery through setup.

**PLG-CHANGE-007.** Reusing definition authority MUST match artifact IDs, target state, accountable right and SHA-256 of reviewed/current artifact content.

**PLG-CHANGE-008.** Continuing WO execution MUST match WO ID, approved scope and actual start authority, preserving DR-015's limits.

**PLG-CHANGE-009.** Reusing assurance authority MUST match VREC ID, full candidate commit, retained evidence digests and accountable assurance right.

**PLG-CHANGE-010.** Reusing external-action authority MUST match action, full commit/release identity and repository/ref or registry destination, with current gates and independent enforcement.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| Partial write or interrupted transition | Inspect before recovery | Evaluator result |
| Changed input or missing decision | Stop affected action | Changed input or missing right |
| Governance context unestablished | Refuse governed writes; recover through setup | Readiness blocker |

## Examples

**Given** an authorized WO start, **when** in-scope implementation changes code, **then** PLG-CHANGE-003 continues without duplicate approval.

**Given** reviewed content, **when** it changes, **then** PLG-CHANGE-004 stops reusing its approval.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-PLG-017` | PLG-CHANGE-001, PLG-CHANGE-002, PLG-CHANGE-006 |
| `REQ-PLG-018` | PLG-CHANGE-003, PLG-CHANGE-004, PLG-CHANGE-005, PLG-CHANGE-007, PLG-CHANGE-008, PLG-CHANGE-009, PLG-CHANGE-010 |

## Not decided here

- These skill instructions do not provide deterministic enforcement or authenticated decisions.
- No new lifecycle or authority store.
