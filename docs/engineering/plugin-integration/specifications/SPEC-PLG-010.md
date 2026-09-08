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

One skill guides drafting, review and implementation. The agent keeps moving when the existing request and decisions still cover the next action.

## Scope

Governs `skills/change/` instructions. Existing [authoring](../../ARTIFACT_AUTHORING.md), [workflow](../../WORKFLOW.md) and [decision-rights rules](../../DECISION_RIGHTS.md) define lifecycle behavior; evidence preparation belongs to SPEC-PLG-011.

## Terms

- **Covered continuation.** A next action still permitted by the current request, actual decisions, relevant inputs and applicable evaluator gates.

## Rules

**PLG-CHANGE-001.** The skill MUST use inspected released evaluator commands and installed authoring rules for selected artifact packages and work-order procedures.

**PLG-CHANGE-002.** The skill MUST preserve draft, approval, start and completion distinctions and report actual partial writes or interrupted outcomes before retry.

**PLG-CHANGE-003.** The skill MUST continue a covered next action without requiring another invocation or repeating an unchanged owner decision.

**PLG-CHANGE-004.** The skill MUST stop affected actions when scope, content, candidate, destination, gates or required authority invalidate the previously covered continuation.

**PLG-CHANGE-005.** The skill MUST preserve DR-015's limited delegation and MUST NOT treat an evaluator next step or `--decision` assertion as authenticated approval.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| Partial creation or interrupted transition | Inspect actual records before recovery. | Actual evaluator result |
| Changed scope or missing decision | Pause the affected action for the required owner. | Applicable blocker or decision right |

## Examples

**Given** an authorized WO start, **when** implementation remains covered, **then** PLG-CHANGE-003 continues without another prompt; an out-of-scope edit invokes PLG-CHANGE-004.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-PLG-017` | PLG-CHANGE-001, PLG-CHANGE-002 |
| `REQ-PLG-018` | PLG-CHANGE-003, PLG-CHANGE-004, PLG-CHANGE-005 |

## Not decided here

- Independent external effect controls remain outside the skill.
- This specification adds neither lifecycle transitions nor a new authority store.
