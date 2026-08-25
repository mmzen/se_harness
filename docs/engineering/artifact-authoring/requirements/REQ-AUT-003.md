+++
id = "REQ-AUT-003"
type = "requirement"
title = "Close the verification-method vocabulary and migrate existing values"
status = "draft"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-25"
updated = "2026-08-25"
statement = "WHEN a requirement is validated, THE SYSTEM SHALL require verification_method to be a non-empty array drawn from test, analysis, inspection, and demonstration, SHALL accept an optional free-text verification_notes field, and SHALL provide one governed migration that maps every existing string value to the vocabulary before the rule becomes an error."
verification_method = "automated-test-and-manual-review"
[relations]
derives_from = ["CAP-AUT-001"]
+++

# Requirement: Close the verification-method vocabulary and migrate existing values

## Rationale

255 requirements carry 110 distinct `verification_method` strings. A closed
vocabulary of the four methods every standard shares (ISO/IEC/IEEE 29148,
INCOSE) makes the attribute queryable and aligns it with the verification
contract's matrix.

## Preconditions and trigger

Validation of any `requirement` artifact; the migration work order.

## Required response

- `verification_method = ["test"]`, an array of one to four distinct values
  from `test`, `analysis`, `inspection`, `demonstration`.
- Optional `verification_notes` string for detail.
- Transition: the validator accepts the legacy string form with maintenance
  warning `W-AUT-004` until the migration lands; after it, a string is `E-AUT-001`.
- The migration maps every existing value by a table retained as evidence:
  values containing "test" map to `test`; "review", "inspection", or
  "walkthrough" add `inspection`; "analysis", "assessment", or "replay" add
  `analysis`; "demonstration", "rehearsal", or "end-to-end" add
  `demonstration`; unmapped values are listed for the steward's decision. The
  original string moves to `verification_notes`.

## Failure and boundary behavior

An unknown value or an empty array is an error once the migration is applied.

## Constraints

Historical `superseded` and `rejected` requirements are migrated like the
rest; their bodies are untouched.

## Acceptance examples

### Example: normal behavior

**Given** `verification_method = ["test", "inspection"]`

**When** validated

**Then** no diagnostic.

### Example: failure behavior

**Given** `verification_method = ["manual-review"]` after the migration

**When** validated

**Then** `E-AUT-001` names the unknown value.

## Open decisions

The mapping of unmatched values is a requirements-steward decision recorded
in the migration evidence.
