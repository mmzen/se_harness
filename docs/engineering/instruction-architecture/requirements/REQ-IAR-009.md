+++
id = "REQ-IAR-009"
type = "requirement"
title = "Keep instructions, evidence, and authority separate"
status = "implemented"
owners = ["requirements-steward", "repository-owner", "quality-owner", "release-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN instructions, preflight, CI, or dashboards report engineering state, THE SYSTEM SHALL treat their outputs as guidance or evidence and SHALL NOT convert them into product, verification, release, or publication authority."
verification_method = "automated-test-and-inspection"

[relations]
derives_from = ["CAP-IAR-001"]
+++

# Requirement: Keep instructions, evidence, and authority separate

## Acceptance criteria

- Product intent and implementation authority remain in approved formal artifacts and one approved work order.
- Preflight and CI never approve a draft artifact, work order, verification record, or release record.
- Dashboard and preflight outputs identify themselves as derived, read-only evidence.
- Automation may prepare only lifecycle states already allowed by the governing workflow and separate explicit authorization.
- No instruction adapter, repository-context file, CI result, source-code observation, or conversation substitutes for an accountable human decision.
- Commit, push, pull-request, verification transition, tag, release, publication, and deployment remain separately authorized actions.
