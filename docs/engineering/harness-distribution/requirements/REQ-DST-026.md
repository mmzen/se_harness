+++
id = "REQ-DST-026"
type = "requirement"
title = "Discoverable relocated operational detail"
status = "approved"
owners = ["product-owner", "documentation-owner"]
created = "2026-08-12"
updated = "2026-08-12"
statement = "WHEN detailed setup, command, agent-operation, release, or contributor material is removed from the root README, THE SYSTEM SHALL retain the relevant current information in expertise-labeled and locally linked notes without duplicating managed governance policy."
verification_method = "automated-link-and-content-test"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Discoverable relocated operational detail

## Rationale

Deleting detail would make the README shorter but would reduce practical usability and could hide safety constraints. Relocation must be explicit, navigable, and current.

## Preconditions and trigger

An existing README section or command example is classified as advanced operator, coding-agent, release, or distribution-contributor material.

## Required response

At minimum, the notes set provides:

- `harness-installation-and-upgrades.md` for platform setup, launcher ownership, exact-version installation, and the two-stage package/repository upgrade;
- `harnessctl-reference.md` for every current subcommand, expected actor, mutation class, authority boundary, and link to authoritative procedure;
- `developing-se-harness.md` for source installation, checks, repository structure, self-hosting assurance planes, and contributor release boundaries.

Existing UML, operational-phasing, branching, and practical-example notes continue to own conceptual model, timing, Git mapping, and end-to-end provenance. The notes index exposes a coherent route rather than a flat list of unrelated files.

## Failure and boundary behavior

Notes must not copy complete `WORKFLOW.md`, `DECISION_RIGHTS.md`, `QUALITY_GATES.md`, or `TRACEABILITY.md` sections or claim authority over them. Broken or circular navigation blocks completion.

## Constraints

- Every new note states its target expertise and explains the score.
- Commands and paths match the current CLI and repository.
- Local Markdown links resolve.
- Removed facts are either relocated, intentionally retired as duplication, or recorded as an obsolete claim in evidence.

## Acceptance examples

### Example: advanced command

**Given** a reader needs the complete `capture-verification` form,

**When** they follow the README learning route,

**Then** the command reference and practical example expose its syntax and human-decision boundary.

### Example: contributor

**Given** a contributor needs the three self-hosting assurance planes,

**When** they follow the contributor link,

**Then** the development note explains the identities and routes to authoritative self-hosting material.

## Open decisions

Existing notes may be tightened or cross-linked to avoid repeating content introduced by the three new notes.
