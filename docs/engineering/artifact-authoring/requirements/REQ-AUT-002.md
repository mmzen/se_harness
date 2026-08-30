+++
id = "REQ-AUT-002"
type = "requirement"
title = "Offer the five EARS statement shapes and signal non-singular statements"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-25"
updated = "2026-08-25"
statement = "WHEN a requirement is validated, THE SYSTEM SHALL accept a statement that opens with one of the five EARS shapes (ubiquitous, WHEN, WHILE, IF-THEN, WHERE) and contains SHALL, SHALL report a maintenance warning when the opener matches none of them, when the statement contains more than one SHALL, or when it exceeds 300 characters, and the requirement template SHALL show all five shapes."
verification_method = "automated-test"
[relations]
derives_from = ["CAP-AUT-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T18:44:01Z"
decided_by = "requirements-steward"
+++

# Requirement: Offer the five EARS statement shapes and signal non-singular statements

## Rationale

252 of 255 statements use `WHEN` because it is the only shape shown; 64 carry
two or more obligations. EARS exists so that an invariant, a mode, an
unwanted behaviour, and an optional feature each have a shape, and so that a
statement carries one response. Singular statements make verification
contracts map one requirement to one pass condition.

## Preconditions and trigger

Validation of any `requirement` artifact.

## Required response

- Accepted openers: `THE SYSTEM SHALL` (ubiquitous), `WHEN`, `WHILE`,
  `IF … THEN`, `WHERE`; case-sensitive keywords; the subject may be a named
  system instead of `THE SYSTEM`.
- `W-AUT-001` (maintenance): opener matches none of the five.
- `W-AUT-002` (maintenance): more than one `SHALL`.
- `W-AUT-003` (maintenance): statement longer than 300 characters.
- `E005` (existing): no `SHALL` at all remains an error.
- The template shows the five shapes as commented alternatives and states
  "one obligation per requirement".

## Failure and boundary behavior

Warnings never block; the 64 existing multi-`SHALL` statements are flagged,
not invalidated. A later policy may promote `W-AUT-002` for artifacts created
after a stated date.

## Constraints

No change to `E005`.

## Acceptance examples

### Example: normal behavior

**Given** `statement = "WHILE the evaluator is unreachable, THE SYSTEM SHALL refuse a lifecycle decision."`

**When** validated

**Then** no `W-AUT-*` warning.

### Example: failure behavior

**Given** `statement = "WHEN X, THE SYSTEM SHALL do A, and SHALL do B."`

**When** validated

**Then** `W-AUT-002` names the second `SHALL`.

## Open decisions

None.

## Amendment record

**The three statement signals are advisories, proposed 2026-08-30 under
`WO-AUT-004` (`REQ-AUT-007`, `SPEC-AUT-002`).** The required response
names `W-AUT-001`, `W-AUT-002` and `W-AUT-003` as maintenance warnings.
`REQ-AUT-007` makes them advisories: still plane `maintenance`, still
computed and carried in the JSON, but listed and counted apart from
warnings, shown on request, and raised only while the requirement is in
`draft`. The rationale here stands; the class is the only change. The
sentence "a later policy may promote `W-AUT-002`" is unaffected. Nothing
else in this requirement changes.
