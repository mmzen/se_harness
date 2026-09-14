+++
id = "ARCH-KIS-002"
type = "architecture"
title = "Use one local execution authorization path"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-14"
updated = "2026-09-14"

[decision_assessment]
outcome = "adr_required"
triggers = ["responsibility-or-dependency-direction", "cross-cutting-policy"]
rationale = "The approval meaning and executor responsibility change across workflow and evidence preparation."
assessed_by = "implementation-planner"

[relations]
addresses = ["REQ-KIS-009"]
conforms_to = ["SPEC-KIS-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-14T20:38:27Z"
decided_by = "technical-owner"
reason = "The owner requested the delegated route as the only route, reviewed the complete proposal and accepted it with \"yes: go\" on 2026-09-14. Record technical-owner approval of ARCH-KIS-002 for that bounded scope, including its retained acceptance boundaries and prospective adoption. No completion, verification, merge, release or live adoption result is inferred."
+++

# Use one local execution authorization path

## Components and dependencies

The existing workflow contract defines operations. Workflow transitions and verification
capture call the same local approval/scope check. Recommendations read the procedure
directly. Skills read installed policy and commands; they do not implement authorization.
CI consumes results at integration and publication, outside local execution permission.

## Responsibility and trust boundary

The owner approves the work and accepts its result. The executor records actual work
under its own identity. Approval grants a named bounded sequence, not self-verification,
merge or publication. Preserve existing relevant gates and project-required separation.
Use the existing approval event and existing commands; ADR-KIS-002 explains why no mode
switch or separate delegation record is needed.
