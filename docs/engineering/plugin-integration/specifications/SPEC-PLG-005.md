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

The host binds shared components without adding governance policy.

## Scope

This contract covers Codex bindings after the technical owner selects a supported route through DEC-PLG-001.
SPEC-PLG-003 governs probe evidence.
SPEC-PLG-002 owns runtime identity; SPEC-PLG-007/008 own shared handlers.

## Terms

- **Shell guard.** A host hook command reporting missing runtime before invoking Python.

## Rules

**PLG-CDXA-001.** The adapter MUST use only a positively accepted supported route and host/platform combinations recorded through DEC-PLG-001.

**PLG-CDXA-002.** The adapter MUST expose the packaged shared skills through the host's proven discovery mechanism, preserving each skill's invocation contract.

**PLG-CDXA-003.** A host-shell guard MUST precede `session-context.py` for session events and `check-tool-action.py` for supported tool events, without installing dependencies.

**PLG-CDXA-004.** Bindings MUST translate host event fields and script results without duplicating evaluator rules or granting decision rights.

**PLG-CDXA-005.** Script invocation MUST preserve arguments and absolute paths under the selected interpreter route, including paths containing spaces.

**PLG-CDXA-006.** Missing runtime, required fields, failed scripts, or inactive bindings MUST report unready; interpreter existence MUST NOT establish readiness.

**PLG-CDXA-007.** The adapter MUST report absent coverage; a declared governed effect escaping required refusal MUST remain unqualified under SPEC-PLG-008.

**PLG-CDXA-008.** Unready guards MUST preserve ordinary host permissions and already-authorized setup access without checked-success claims or permission overrides.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| No accepted route | Refuse readiness. | None |
| Unsupported host or platform | Refuse readiness and identify the supported combination. | None |
| Missing runtime | Report setup required in the demonstrated host format. | Setup-required message |
| Malformed event or failed script | Preserve the failure in the host's supported result format. | Shared script or host output |

## Examples

**Given** a missing event field, **when** the adapter receives a tool action, **then** it reports failure under PLG-CDXA-006.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-PLG-008` | PLG-CDXA-001, PLG-CDXA-002, PLG-CDXA-003, PLG-CDXA-004, PLG-CDXA-005, PLG-CDXA-006, PLG-CDXA-007, PLG-CDXA-008 |

## Not decided here

- Setup eligibility is instruction-level; the guard does not authenticate authority or enforce an action classifier.
