+++
id = "SPEC-PLG-008"
type = "specification"
title = "Existing checks at supported tool boundaries"
status = "draft"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-08"
contract = "Supported tool actions receive current evaluator checks before their effects, while unsupported routes remain explicit coverage gaps."

[relations]
specifies = ["REQ-PLG-013", "REQ-PLG-014"]
+++

# Specification: Existing checks at supported tool boundaries

## In plain words

The hook must return refusals before the host stops waiting. Missing output proves no protection.

## Scope

`check-tool-action.py`; SPEC-PLG-005/006 own bindings. [Workflow](../../WORKFLOW.md) retains policy.

## Terms

- **Covered action.** An action reliably mapped to its evaluator check.
- **Inner deadline.** One time budget for evaluator work, ending before the host timeout with room for startup, cleanup and response.

## Rules

**PLG-HOOK-001.** Each covered action MUST use the existing evaluator with its selected artifact, applicable checkpoint and actual paths.

**PLG-HOOK-002.** The handler MUST obtain the current required check before a covered effect and translate failure into supported host refusal.

**PLG-HOOK-003.** Malformed or unmappable actions MUST report unavailable coverage without claiming a successful governance check.

**PLG-HOOK-004.** Unavailable refusal MUST be recorded as an unenforced route without governed-automation readiness; missing handler output MUST NOT be treated as refusal.

**PLG-HOOK-005.** The adapter MUST preserve required checks and evaluator policy; successful invocation MUST NOT grant authority.

**PLG-HOOK-006.** Ambiguous, malformed or unmapped governed actions MUST receive refusal before effect on refusal-capable routes, with unavailable coverage reported.

**PLG-HOOK-007.** Each invocation MUST enforce one monotonic inner deadline across evaluator work, reserving measured startup, cleanup and response margins before the configured host timeout.

**PLG-HOOK-008.** On inner expiry or evaluator failure, the running handler MUST stop evaluator process trees, collect exits and emit supported refusal before the host deadline.

**PLG-HOOK-009.** Host timeout, launch failure or missing required denial MUST trigger effect inspection before retry; escaped required refusal MUST remain unqualified.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| Evaluator failure/inner expiry; handler running | Stop children; return timely denial | Evaluator error/inner timeout |
| Ambiguous governed action | Refuse on supported route | Coverage blocker |
| Host cancels hook or guard never starts | Inspect effects; no assumed refusal | Host failure/unenforced route |

## Examples

**Given** stalled evaluation, **when** the inner deadline expires, **then** PLG-HOOK-008 returns denial before the host deadline.

**Given** host cancellation, **when** no decision arrives, **then** PLG-HOOK-009 requires effect inspection.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-PLG-013` | PLG-HOOK-001, PLG-HOOK-002, PLG-HOOK-005, PLG-HOOK-007, PLG-HOOK-008, PLG-HOOK-009 |
| `REQ-PLG-014` | PLG-HOOK-003, PLG-HOOK-004, PLG-HOOK-006, PLG-HOOK-009 |

## Not decided here

- Exact timing values and live host qualification.
- Independent external authorization: issue #347.
