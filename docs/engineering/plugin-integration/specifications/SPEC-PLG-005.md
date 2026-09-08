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

The Codex adapter connects the host to the same plugin components used by the other host.
It translates host inputs and results without creating another governance engine.

## Scope

This contract covers Codex bindings after the technical owner selects a supported route through DEC-PLG-001.
SPEC-PLG-003 governs the required compatibility evidence.
SPEC-PLG-002 owns evaluator selection; SPEC-PLG-007 and SPEC-PLG-008 own shared event behaviour.

## Terms

- **Host adapter.** The host-specific manifest and bindings that connect supported events to shared components.

## Rules

**PLG-CDXA-001.** The adapter MUST use only a positively accepted supported route and host/platform combinations recorded through DEC-PLG-001.

**PLG-CDXA-002.** The adapter MUST expose the packaged shared skills through the host's proven discovery mechanism, preserving each skill's invocation contract.

**PLG-CDXA-003.** Supported session events MUST call `scripts/session-context.py`; supported tool-action events MUST call `scripts/check-tool-action.py`.

**PLG-CDXA-004.** Bindings MUST translate host event fields and script results without duplicating evaluator rules or granting decision rights.

**PLG-CDXA-005.** Script invocation MUST preserve arguments and absolute paths under the selected interpreter route, including paths containing spaces.

**PLG-CDXA-006.** Missing required fields, failed scripts, or inactive required bindings MUST produce a visible failure without reporting the integration ready.

**PLG-CDXA-007.** The adapter MUST identify unsupported event and tool coverage without representing it as enforcement.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| No positively accepted route, including an exclusion decision | Refuse implementation readiness; a decided decision alone grants no support. | None |
| Unsupported host or platform | Refuse readiness and identify the supported combination. | None |
| Malformed event or failed script | Preserve the failure in the host's supported result format. | Shared script or host output |
| Required binding is inactive | Report incomplete activation. | None |

## Examples

**Given** an accepted Codex profile, **when** a session event arrives, **then** its binding invokes the shared script under PLG-CDXA-003.

**Given** a missing event field, **when** the adapter receives a tool action, **then** it reports failure under PLG-CDXA-006.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-PLG-008` | PLG-CDXA-001, PLG-CDXA-002, PLG-CDXA-003, PLG-CDXA-004, PLG-CDXA-005, PLG-CDXA-006, PLG-CDXA-007 |

## Not decided here

- Shared script policy, skill workflows, or additional evaluator APIs.
- Operator approval rights or remote-action authorization.
- Host support beyond the accepted compatibility evidence.
