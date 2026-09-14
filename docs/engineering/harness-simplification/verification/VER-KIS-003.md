+++
id = "VER-KIS-003"
type = "verification"
title = "Check the single execution procedure and retained boundaries"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-14"
updated = "2026-09-14"

[relations]
verifies = ["REQ-KIS-009"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-14T20:38:27Z"
decided_by = "assurance-owner"
reason = "The owner requested the delegated route as the only route, reviewed the complete proposal and accepted it with \"yes: go\" on 2026-09-14. Record assurance-owner approval of VER-KIS-003 for that bounded scope, including its retained acceptance boundaries and prospective adoption. No completion, verification, merge, release or live adoption result is inferred."
+++

# Check the single execution procedure and retained boundaries

## Independence

Expected outcomes are the owner's accepted proposal and SPEC-KIS-003, not candidate
output. Reuse public CLI fixtures and retained checks; do not mirror every code branch.

## Requirement-to-evidence matrix

| Requirement | Evidence | Pass condition |
| --- | --- | --- |
| REQ-KIS-009 | A: workflow/capture tests; B: policy/skill review; C: required suite/package checks | One local execution path meets KIS-EXE-001 through 007 and preserves acceptance/history. |

## Checks

A: An approved selected WO without a delegation table can start, complete and prepare
required evidence through the existing commands offline. A human and agent follow the
same checks with their supplied actor retained. Missing approval, changed scope or a failed
local gate blocks the affected operation, including use of an owner actor name. Capture
checks every explicitly selected WO rather than imposing an actor-specific single-WO limit.
Old explicit execution grants remain meaningful; an old approval without that grant is not
silently expanded. Preparation leaves VREC ready and related decisions unchanged.

B: Review the template, workflow/policy agreement and common skill route. Walk the ordinary
approved-task request through the returned commands: no separate routine permissions and
no hardcoded obsolete CI authorization. Respect the existing assurance classification and
project role separation. Keep that review in ordinary evidence, not a new receipt.

C: Run focused workflow/provenance tests, the repository source suite, distribution checks,
CLI help, graph validation, doctor and start/review preflight. Use Windows locally and
existing hosted supported-platform checks. Candidate source/non-promotable wheels test
future behavior; released 0.17.0 governs this real work. Retain actual failed attempts and
report unavailable platform evidence honestly. Never change tests to bypass retained rules.
