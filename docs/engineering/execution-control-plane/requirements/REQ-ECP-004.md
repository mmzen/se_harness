+++
id = "REQ-ECP-004"
type = "requirement"
title = "Identifiers are allocated across every local ref"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-27"
updated = "2026-08-28"
statement = "WHEN `harnessctl create-artifact` is invoked without an explicit identifier, THE SYSTEM SHALL allocate the lowest identifier for the requested domain and type that no artifact reachable from any local Git ref already uses."
verification_method = ["test"]
priority = "must"
source = "AGENTS.md traps; OPERATING_CARD.md"

[relations]
derives_from = ["CAP-ECP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T12:03:40Z"
decided_by = "requirements-steward"
reason = "Approved on 2026-08-28 by the accountable owner, 'I approve the ECP definitions and WO-ECP-005', as part of the execution-control-plane definition packet of #231 with the issue #212 amendments of #238 applied. Approval of a definition authorizes no work; each work order is approved separately."
+++

# Requirement: Identifiers are allocated across every local ref

## Rationale

Identifiers are hand-typed and checked only in the current tree
(docs/notes/agentic-execution-review-2026-08.md:149-151), while the identifier
space is shared across branches. Choosing "new identifiers across every ref" is
one of the decisions the agent makes alone (docs/notes/agentic-execution-
review-2026-08.md:282), and the owner region of `AGENTS.md` and
`OPERATING_CARD.md` carry it as a documented trap because collisions recurred. A
trap that recurs belongs in the harness as an allocation, not in prose as a
reminder.

## Behavior

- Trigger: `harnessctl create-artifact REPO --type TYPE --domain PREFIX`
  runs without `--id`.
- Response: the allocated identifier is `TYPE-PREFIX-NNN` with the lowest
  `NNN` such that no artifact carrying that `id` is reachable from any local
  branch, tag, or `HEAD` of the repository; the result reports the identifier
  and the refs consulted.
- On failure: when the repository is not a Git checkout or a ref cannot be read,
  the command fails closed and allocates nothing; it never falls back to the
  working tree alone.

## Assumptions and dependencies

- Local refs are the authority; remote-only refs are not consulted, which the
  result states.
- Artifact identifiers keep the `TYPE-PREFIX-NNN` shape validated today.
- `--id` remains available for an explicit identifier and is rejected when it
  is already used on any local ref.

## Acceptance examples

Executable scenarios live in `acceptance/REQ-ECP-004.feature` and are named by
the verification contract that covers this requirement.

### Example: normal behavior

**Given** `REQ-X-001` to `REQ-X-006` exist on `main`; `REQ-X-007` exists only on
branch `feature/other`.

**When** `harnessctl create-artifact . --type requirement --domain X` runs on a
branch off `main`.

**Then** the allocated identifier is `REQ-X-008` and the result lists
`feature/other` among the refs consulted.

### Example: failure behavior

**Given** the same repository, and the actor passes `--id REQ-X-007`.

**When** the command runs.

**Then** nothing is written, and the result names `REQ-X-007` as used on
`feature/other`.

## Open decisions

None.
