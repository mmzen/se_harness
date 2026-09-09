+++
id = "SPEC-PLG-003"
type = "specification"
title = "Reproducible Codex compatibility assessment"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-08"
contract = "The compatibility assessment records an observed activation sequence or a specific incompatibility for each assessed host and platform version."

[relations]
specifies = ["REQ-PLG-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-08T21:39:22Z"
decided_by = "technical-owner"
reason = "Operator explicitly approved the Codex probe packet reviewed at be8b4126 in this Codex task. Record the selected specification approval only."
+++

# Specification: Reproducible Codex compatibility assessment

## In plain words

Test the documented Codex shell-guard route before building its production adapter.
An unsuccessful attempt is useful evidence when its exact limitation is recorded.

## Scope

Disposable probes test: shell guard reports setup required when the runtime cannot run; otherwise the Python handler checks readiness. No automatic installation occurs.
SPEC-PLG-005 governs the production adapter after DEC-PLG-001 resolves its supported activation path.

## Terms

- **Activation sequence.** The ordered actions that make plugin components discoverable and their registered events observable.

## Rules

**PLG-CDXP-001.** Each assessment MUST identify the host version, operating system, provided Python, referenced host documentation, and fixture revision.

**PLG-CDXP-002.** Probes MUST use disposable repositories and isolated host configuration, without changing the operator's normal installation.

**PLG-CDXP-003.** Probes MUST assess manifest loading, skill discovery, event registration, trust requirements, and event delivery during new, resumed, and compacted sessions.

**PLG-CDXP-004.** Probes MUST test a host-shell guard before setup, after setup, and after interpreter removal, including paths containing spaces and persistent plugin data.

**PLG-CDXP-005.** Probes MUST record missing-Python and inactive-hook outcomes without silently installing Python or asserting readiness.

**PLG-CDXP-006.** Every assessed host/platform combination MUST retain ordered actions, actual outputs, observed events, and either a reproducible activation sequence or a specific incompatibility.

**PLG-CDXP-007.** The report MUST distinguish tested, unsupported, and unavailable combinations across Windows, Linux, and macOS, without treating an unperformed check as success.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| Host rejects the fixture or omits an event | Retain the rejection or missing event and identify the affected activation step. | Host output or none |
| A platform cannot be assessed | Mark it unavailable and state the missing prerequisite. | None |

## Examples

**Given** an isolated Codex profile, **when** all observed activation steps repeat, **then** the report retains that sequence under PLG-CDXP-006.

**Given** an unavailable compact event, **when** the probe completes, **then** the report records that limitation under PLG-CDXP-003 and PLG-CDXP-007.

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-PLG-006` | PLG-CDXP-001, PLG-CDXP-002, PLG-CDXP-003, PLG-CDXP-004, PLG-CDXP-005, PLG-CDXP-006, PLG-CDXP-007 |

## Not decided here

- Supported production host versions and platforms; DEC-PLG-001 records that choice.
- Shared governance behaviour, which belongs to SPEC-PLG-007 and SPEC-PLG-008.
- Publication or installation into an operator's normal host profile.
