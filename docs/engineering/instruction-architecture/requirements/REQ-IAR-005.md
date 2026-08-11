+++
id = "REQ-IAR-005"
type = "requirement"
title = "Require curated repository context before implementation"
status = "implemented"
owners = ["requirements-steward", "repository-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN implementation readiness is evaluated, THE SYSTEM SHALL require owner-curated repository context while preventing that context from granting product or governance authority."
verification_method = "automated-test-and-inspection"

[relations]
derives_from = ["CAP-IAR-001"]
+++

# Requirement: Require curated repository context before implementation

## Acceptance criteria

- `REPOSITORY_CONTEXT.md` remains repository-owned after installation.
- Preflight fails when required context fields retain the standard unresolved placeholder or are blank.
- The diagnostic identifies every incomplete field without treating arbitrary uses of the word `TODO` elsewhere as incomplete context.
- Context supplies confirmed commands, entry points, ownership, sensitive paths, and repository constraints.
- The file states that product intent, requirements, work authorization, verification, and release authority reside only in formal artifacts and accountable decisions.
