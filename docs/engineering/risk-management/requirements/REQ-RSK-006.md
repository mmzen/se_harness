+++
id = "REQ-RSK-006"
type = "requirement"
title = "Let anyone identify a risk at any stage without widening scope"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-25"
updated = "2026-08-25"
statement = "WHEN an actor runs harnessctl raise-risk with a domain, identifier, stage, category, likelihood, impact, title, and at least one threatened artifact, THE SYSTEM SHALL create the risk at its canonical path with the computed score and status, SHALL admit that new file as a changed path within any work order's execution scope while its status is identified or raised, and SHALL offer a reading step in every stage procedure that lists the risks threatening the selected artifact's chain."
verification_method = "automated-test"
[relations]
derives_from = ["CAP-RSK-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T13:25:29Z"
decided_by = "requirements-steward"
+++

# Requirement: Let anyone identify a risk at any stage without widening scope

## Rationale

Risks are found by whoever is there — often an agent whose work order does
not admit a `risks/` directory. Identification is preparation (`HRN-005`),
so it must be legal from inside any bounded scope without a scope decision.
A reading step at each checkpoint makes "someone looked" a recorded fact.

## Preconditions and trigger

`harnessctl raise-risk`; `changed_paths_within_scope`; procedure resolution.

## Required response

- `raise-risk` is a preparation command under the same mutation guard as
  `create-artifact`; it validates the destination, checks identifier
  uniqueness against the catalog, writes the draft, and returns a schema-2
  block whose `Done` names the risk, score, level, and threatened artifacts.
- Scope exception: a path matching `docs/engineering/*/risks/RISK-*.md`
  whose artifact status is `identified` or `raised` is admitted by
  `changed_paths_within_scope` for any work order.
- Each stage procedure gains one reading command step
  `harnessctl risks . --artifact {artifact_id}`, which cannot fail and
  exercises nothing.
- `harness-draft-change` and `harness-execute-work-order` may call
  `raise-risk`; `harness-prepare-assurance` includes the register in its
  packet; no skill disposes.

## Failure and boundary behavior

A disposed risk file is not covered by the exception; editing it is a
transition, not a path change. An identifier collision or a threatened
artifact that does not exist refuses the write.

## Constraints

Raising creates one file and changes no other.

## Acceptance examples

### Example: normal behavior

**Given** `WO-X-001` in progress with scope `src/`

**When** an agent raises `RISK-X-001` threatening `WO-X-001` and runs the
handoff check with both `src/main.py` and the risk path as changed paths

**Then** `QGP-G4I-PATHS` passes and `QGP-G4I-RISK` fails.

### Example: failure behavior

**Given** the same work order

**When** the changed set includes `docs/engineering/x/risks/RISK-X-001.md`
already `accepted`

**Then** `QGP-G4I-PATHS` fails as an out-of-scope path.

## Open decisions

None.
