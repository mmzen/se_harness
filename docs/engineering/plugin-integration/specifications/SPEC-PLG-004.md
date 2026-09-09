+++
id = "SPEC-PLG-004"
type = "specification"
title = "Reproducible Claude Code compatibility assessment"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-08"
contract = "The compatibility assessment records an observed activation sequence or a specific incompatibility for each assessed host and platform version."

[relations]
specifies = ["REQ-PLG-007"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-08T21:43:01Z"
decided_by = "technical-owner"
reason = "Operator explicitly approved the Claude Code probe packet reviewed at be8b4126. Record the selected specification approval only."
+++

# Specification: Reproducible Claude Code compatibility assessment

## In plain words

Test the documented Claude Code shell-guard route before building its production adapter.
An unsuccessful attempt is useful evidence when its exact limitation is recorded.

## Scope

Disposable probes test: shell guard reports setup required when the runtime cannot run; otherwise the Python handler checks readiness. No automatic installation occurs.
SPEC-PLG-006 governs the production adapter after DEC-PLG-002 resolves its supported activation path.

## Terms

- **Activation sequence.** The ordered actions that make plugin components discoverable and their registered events observable.

## Rules

**PLG-CLCP-001.** Each assessment MUST identify the host version, operating system, provided Python, referenced host documentation, and fixture revision.

**PLG-CLCP-002.** Probes MUST use disposable repositories and isolated host configuration, without changing the operator's normal installation.

**PLG-CLCP-003.** Probes MUST assess manifest loading, skill discovery, event registration, trust requirements, and event delivery during new, resumed, and compacted sessions.

**PLG-CLCP-004.** Probes MUST test a host-shell guard before setup, after setup, and after interpreter removal, including paths containing spaces and persistent plugin data.

**PLG-CLCP-005.** Probes MUST record missing-Python and inactive-hook outcomes without silently installing Python or asserting readiness.

**PLG-CLCP-006.** Every assessed host/platform combination MUST retain ordered actions, actual outputs, observed events, and either a reproducible activation sequence or a specific incompatibility.

**PLG-CLCP-007.** The report MUST distinguish tested, unsupported, and unavailable combinations across Windows, Linux, and macOS, without treating an unperformed check as success.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| Host rejects the fixture or omits an event | Retain the rejection or missing event and identify the affected activation step. | Host output or none |
| A platform cannot be assessed | Mark it unavailable and state the missing prerequisite. | None |

## Examples

**Given** an isolated Claude Code profile, **when** all observed activation steps repeat, **then** the report retains that sequence under PLG-CLCP-006.

**Given** an unavailable compact event, **when** the probe completes, **then** the report records that limitation under PLG-CLCP-003 and PLG-CLCP-007.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-PLG-007` | PLG-CLCP-001, PLG-CLCP-002, PLG-CLCP-003, PLG-CLCP-004, PLG-CLCP-005, PLG-CLCP-006, PLG-CLCP-007 |

## Not decided here

- Supported production host versions and platforms; DEC-PLG-002 records that choice.
- Shared governance behaviour, which belongs to SPEC-PLG-007 and SPEC-PLG-008.
- Publication or installation into an operator's normal host profile.
