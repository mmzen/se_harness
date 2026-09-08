+++
id = "SPEC-PLG-010"
type = "specification"
title = "Change skill with continuous bounded execution"
status = "draft"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-08"
contract = "The change skill follows existing artifact and work-order procedures, continuing covered work while stopping affected actions that lack current authority."

[relations]
specifies = ["REQ-PLG-017", "REQ-PLG-018"]
+++

# Specification: Change skill with continuous bounded execution

## In plain words

Reuse decisions for the same actions and reviewed inputs.

## Scope

`skills/change/` follows existing [authoring](../../ARTIFACT_AUTHORING.md), [workflow](../../WORKFLOW.md) and [decision rights](../../DECISION_RIGHTS.md). SPEC-PLG-011 covers evidence.

## Terms

- **Covered continuation.** Actual authority matches reviewed inputs; current gates pass.

Comparisons establish applicability, never authentication or new authority records.

| Action | Compare against actual reviewed decision inputs |
| --- | --- |
| Definition decision | Match artifact IDs, target state, accountable right and SHA-256 of reviewed/current artifact content. |
| WO execution | Match WO ID, approved scope and actual start authority; only eligible DR-015 delegation applies. |
| Assurance | Match VREC ID, full candidate commit, retained evidence digests and assurance right. |
| External action | Match action, full commit/release identity, repository/ref or registry destination and authority; require current gates and independent enforcement. |

Ordinary in-scope code commits need no renewed WO approval. Candidate-bound decisions retain identity checks. Missing reviewed inputs stop affected reuse.


## Rules

**PLG-CHANGE-001.** The skill MUST use inspected released evaluator commands and installed authoring rules for selected artifact packages and work-order procedures.

**PLG-CHANGE-002.** The skill MUST preserve draft, approval, start and completion distinctions and report partial writes or interruptions before retry.

**PLG-CHANGE-003.** The skill MUST continue covered actions without another invocation or duplicate decision, using the action-specific applicability table.

**PLG-CHANGE-004.** Changed governing inputs, missing authority or failed gates MUST stop the affected action; unrelated authority MUST NOT substitute.

**PLG-CHANGE-005.** The skill MUST preserve DR-015's limited delegation and MUST NOT treat an evaluator next step or `--decision` assertion as authenticated approval.


## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| Partial write or interrupted transition | Inspect before recovery | Evaluator result |
| Changed input or missing decision | Stop affected action | Changed input or missing right |

## Examples

**Given** an authorized WO start, **when** in-scope implementation changes code, **then** PLG-CHANGE-003 continues without duplicate approval.

**Given** reviewed content, **when** it changes, **then** PLG-CHANGE-004 stops reusing its approval.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-PLG-017` | PLG-CHANGE-001, PLG-CHANGE-002 |
| `REQ-PLG-018` | PLG-CHANGE-003, PLG-CHANGE-004, PLG-CHANGE-005 |

## Not decided here

- External enforcement and authenticated decisions.
- No new lifecycle transitions, policy engine or authority store.
