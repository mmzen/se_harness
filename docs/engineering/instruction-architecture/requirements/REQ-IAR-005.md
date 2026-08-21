+++
id = "REQ-IAR-005"
type = "requirement"
title = "Require curated repository context before implementation"
status = "superseded"
owners = ["requirements-steward", "repository-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-21"
statement = "WHEN implementation readiness is evaluated, THE SYSTEM SHALL require owner-curated repository context while preventing that context from granting product or governance authority."
verification_method = "automated-test-and-inspection"

[relations]
derives_from = ["CAP-IAR-001"]
+++

# Requirement: Require curated repository context before implementation

## Supersession

Superseded on 2026-08-21 by `REQ-IAR-021` and `REQ-DST-065` under `WO-DST-021`,
authorized by the repository owner. The repository-context scaffold and its
readiness gate are withdrawn: repository-local operational facts belong in the
owner-controlled region of `AGENTS.md`, which the harness neither scaffolds,
tracks, nor gates. The acceptance criteria below record what the shipped product
did while this requirement was active and are retained unchanged as history. They
are no longer obligations, and no automated check enforces them.

## Acceptance criteria

- `REPOSITORY_CONTEXT.md` remains repository-owned after installation.
- Preflight fails when required context fields retain the standard unresolved placeholder or are blank.
- The diagnostic identifies every incomplete field without treating arbitrary uses of the word `TODO` elsewhere as incomplete context.
- Context supplies confirmed commands, entry points, ownership, sensitive paths, and repository constraints.
- The file states that product intent, requirements, work authorization, verification, and release authority reside only in formal artifacts and accountable decisions.
