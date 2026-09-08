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

The hook checks supported actions through the evaluator. It reports coverage gaps explicitly.

## Scope

`check-tool-action.py` only; SPEC-PLG-005/006 own host integration. Existing [workflow rules](../../WORKFLOW.md) retain policy.

## Terms

- **Covered action.** An intercepted action reliably mapped to an applicable evaluator check using its actual inputs and effect.

## Rules

**PLG-HOOK-001.** Each covered action MUST use the existing evaluator with its selected artifact, applicable procedure checkpoint and actual paths.

**PLG-HOOK-002.** The handler MUST obtain the current required check before a covered effect and translate failure into host refusal.

**PLG-HOOK-003.** Malformed or unmappable actions MUST report unavailable coverage and MUST NOT be presented as successfully governance-checked.

**PLG-HOOK-004.** Unenforceable refusal MUST produce an explicit unenforced-route result, without automation readiness for that governed action.

**PLG-HOOK-005.** The adapter MUST preserve required checks and evaluator policy; successful invocation MUST NOT grant action authority.

**PLG-HOOK-006.** For ambiguous, malformed or unmapped governed actions, a refusal-capable host MUST receive refusal before effect, with unavailable coverage reported.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| Covered check fails or cannot complete | Refuse the effect on the supported host route. | Existing finding or check failure |
| Ambiguous, malformed or unmapped governed action | Refuse before effect if supported; otherwise identify the unenforced route. | Explicit coverage blocker |

## Examples

**Given** an ambiguous governed shell action, **when** a host supports refusal, **then** PLG-HOOK-006 refuses before effect; PLG-HOOK-003 reports unavailable coverage.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-PLG-013` | PLG-HOOK-001, PLG-HOOK-002, PLG-HOOK-005 |
| `REQ-PLG-014` | PLG-HOOK-003, PLG-HOOK-004, PLG-HOOK-006 |

## Not decided here

- Independent external authorization enforcement: issue #347.
- Live host coverage: adapter qualification.
