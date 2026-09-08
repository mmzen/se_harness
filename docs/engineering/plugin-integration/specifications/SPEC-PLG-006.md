+++
id = "SPEC-PLG-006"
type = "specification"
title = "Claude Code adapter for shared plugin components"
status = "draft"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-08"
contract = "The host adapter exposes the selected shared skills and connects supported host events to the shared scripts through the approved activation sequence."

[relations]
specifies = ["REQ-PLG-009"]
+++

# Specification: Claude Code adapter for shared plugin components

## In plain words

The host binds shared components without adding governance policy.

## Scope

This contract covers Claude Code bindings after the technical owner selects a supported route through DEC-PLG-002.
SPEC-PLG-004 governs probe evidence.
SPEC-PLG-002 owns runtime identity; SPEC-PLG-007/008 own shared handlers.

## Terms

- **Shell guard.** A host hook command reporting missing runtime before invoking Python.

## Rules

**PLG-CLCA-001.** The adapter MUST use only a positively accepted supported route and host/platform combinations recorded through DEC-PLG-002.

**PLG-CLCA-002.** The adapter MUST expose the packaged shared skills through the host's proven discovery mechanism, preserving each skill's invocation contract.

**PLG-CLCA-003.** A host-shell guard MUST precede `session-context.py` for session events and `check-tool-action.py` for supported tool events, without installing dependencies.

**PLG-CLCA-004.** Bindings MUST translate host event fields and script results without duplicating evaluator rules or granting decision rights.

**PLG-CLCA-005.** Script invocation MUST preserve arguments and absolute paths under the selected interpreter route, including paths containing spaces.

**PLG-CLCA-006.** Missing runtime, required fields, failed scripts, or inactive bindings MUST report unready; interpreter existence MUST NOT establish readiness.

**PLG-CLCA-007.** The adapter MUST report absent coverage; a declared governed effect escaping required refusal MUST remain unqualified under SPEC-PLG-008.

**PLG-CLCA-008.** Unready guards MUST preserve ordinary host permissions and already-authorized setup access without checked-success claims or permission overrides.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| No accepted route | Refuse readiness. | None |
| Unsupported host or platform | Refuse readiness and identify the supported combination. | None |
| Missing runtime | Report setup required in the demonstrated host format. | Setup-required message |
| Malformed event or failed script | Preserve the failure in the host's supported result format. | Shared script or host output |

## Examples

**Given** a missing event field, **when** the adapter receives a tool action, **then** it reports failure under PLG-CLCA-006.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-PLG-009` | PLG-CLCA-001, PLG-CLCA-002, PLG-CLCA-003, PLG-CLCA-004, PLG-CLCA-005, PLG-CLCA-006, PLG-CLCA-007, PLG-CLCA-008 |

## Not decided here

- Setup eligibility is instruction-level; the guard does not authenticate authority or enforce an action classifier.
