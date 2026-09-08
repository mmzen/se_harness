+++
id = "SPEC-PLG-005"
type = "specification"
title = "Codex adapter for shared plugin components"
status = "draft"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-08"
contract = "The host adapter exposes the selected shared skills and connects supported host events to the shared scripts through the approved activation sequence."

[relations]
specifies = ["REQ-PLG-008"]
+++

# Specification: Codex adapter for shared plugin components

## In plain words

The host connects shared components. A failed or missing hook does not prove an action was blocked.

## Scope

Codex bindings after DEC-PLG-001; SPEC-PLG-003 owns probe evidence, SPEC-PLG-002 identity, and SPEC-PLG-007/008 shared handlers.

## Terms

- **Shell guard.** A host command checking runtime availability before Python.
- **Host timeout.** The configured time limit for the entire hook command.

## Rules

**PLG-CDXA-001.** The adapter MUST use only positively accepted routes and profiles recorded through DEC-PLG-001.

**PLG-CDXA-002.** Packaged shared skills MUST use proven host discovery and preserve their invocation contracts.

**PLG-CDXA-003.** Host-shell guards MUST precede `session-context.py` for sessions and `check-tool-action.py` for supported tool events, without installing dependencies.

**PLG-CDXA-004.** Bindings MUST translate host fields and results without duplicating evaluator rules or granting authority.

**PLG-CDXA-005.** Invocation MUST preserve arguments and absolute interpreter/script paths, including paths containing spaces.

**PLG-CDXA-006.** Missing runtime or required fields, failed scripts, or inactive bindings MUST report unready; interpreter existence alone MUST NOT establish readiness.

**PLG-CDXA-007.** The adapter MUST report absent coverage; effects escaping required refusal MUST remain unqualified under SPEC-PLG-008.

**PLG-CDXA-008.** Unready guards MUST preserve ordinary host permissions and already-authorized setup access without checked-success claims or permission overrides.

**PLG-CDXA-009.** Before-tool bindings MUST run synchronously with explicit host timeouts exceeding SPEC-PLG-008's inner deadline plus measured startup, cancellation and response margins.

**PLG-CDXA-010.** Qualification MUST observe guard startup and accepted denial on each claimed profile; host timeout, launch failure or missing output MUST NOT imply prevented effects.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| Unsupported route/profile | Refuse readiness | Unsupported combination |
| Runnable guard; missing Python | Keep setup accessible, governance unready | Setup required |
| Handler returns a valid refusal | Observe host rejection before effect | Host-accepted denial |
| Host timeout, launch failure or invalid output | Inspect effects; record missing enforcement | Host failure/coverage gap |

## Examples

**Given** a stopped hook, **when** output is absent, **then** PLG-CDXA-010 requires observing effects rather than assuming refusal.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-PLG-008` | PLG-CDXA-001, PLG-CDXA-002, PLG-CDXA-003, PLG-CDXA-004, PLG-CDXA-005, PLG-CDXA-006, PLG-CDXA-007, PLG-CDXA-008, PLG-CDXA-009, PLG-CDXA-010 |

## Not decided here

- Setup eligibility remains instruction-level, without an authority classifier.
- Host responses follow the assessed [official reference](https://learn.chatgpt.com/docs/hooks#pretooluse); qualification establishes actual behavior, not future availability.
