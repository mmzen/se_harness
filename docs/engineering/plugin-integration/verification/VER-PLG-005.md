+++
id = "VER-PLG-005"
type = "verification"
title = "Codex adapter conformance to accepted activation evidence"
status = "draft"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-PLG-008"]
+++

# Verification Contract: Codex adapter conformance to accepted activation evidence

## Independence

Use SPEC-PLG-005, DEC-PLG-001, and retained WO-PLG-003 observations for expected host behaviour.
Shared-script expectations come from their selected contracts.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-008 | Test, demonstration, inspection | Accepted activation; malformed event; absent binding; script failure | Shared skills and scripts run through accepted bindings; invalid or incomplete integration never reports readiness. |

## Acceptance scenarios

First establish an approved specification and positively accepted supported route; an exclusion decision cannot satisfy this prerequisite.
Activate the production package in a disposable Codex profile.
Observe supported session and tool-action events, including quoted paths with spaces.
Repeat with malformed fields, an inactive required binding, and a failing shared script.

## Property and invariant tests

Compare passed arguments and returned results against the accepted mapping.
The adapter adds neither policy decisions nor skill invocation requirements.
Check that an exclusion outcome or merely decided decision without an accepted route cannot be reported as supported integration.

## Static and architecture checks

Inspect ARCH-PLG-002 and ADR-PLG-002 conformance.
Check that shared components have one source.

## Security and privacy checks

Unsupported tool coverage remains visible and cannot be presented as authorization enforcement.

## Performance and resilience checks

Record adapter dispatch cost.
Host failures do not silently skip required shared checks.

## Manual assessments

Execute every positively accepted Windows, Linux, or macOS combination recorded through DEC-PLG-001. An empty supported set cannot pass adapter acceptance.
Name exact host, Python, and released-evaluator versions; list unaccepted combinations separately.

## Evidence retention

Retain package identity, event inputs/outputs, observed invocation arguments, and results under `evidence/WO-PLG-005/`.

## Residual uncertainty

Native hooks cover only the accepted host surface.
They do not close the separate deterministic authorization gap tracked by issue #347.
