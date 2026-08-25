+++
id = "REQ-AUT-005"
type = "requirement"
title = "Refuse approval of an artifact with leftover placeholders or open decisions"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-25"
updated = "2026-08-25"
statement = "WHEN a definition artifact is evaluated for approval under QG-G1-DEFINITION or QG-G2-ARCHITECTURE, THE SYSTEM SHALL fail the gate when the artifact still contains a template placeholder of the form <...>, or when its Open decisions section is present and states anything other than None."
verification_method = "automated-test"
[relations]
derives_from = ["CAP-AUT-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T18:44:01Z"
decided_by = "requirements-steward"
+++

# Requirement: Refuse approval of an artifact with leftover placeholders or open decisions

## Rationale

Thirteen approved requirements still carry angle-bracket placeholders, and
the sentence "there must be no unresolved product decision when status
becomes approved" has never been read by the validator. Both are exactly the
kind of rule the harness makes a predicate.

## Preconditions and trigger

`check`, `transition`, and preparation commands evaluating
`QG-G1-DEFINITION` or `QG-G2-ARCHITECTURE` for a selected definition, or a
transition packet approving definitions.

## Required response

- Predicates `QGP-G1-AUTHORING` and `QGP-G2-AUTHORING`, evaluator
  `authoring_ready`: fail when the file contains `<` followed by a word and
  `>` outside code spans, or when a `## Open decisions` section exists and
  its first non-empty line is not `None` or `None.`.
- Corrective form: a response naming the offending placeholder or line.

## Failure and boundary behavior

Already-approved artifacts are not re-evaluated; the predicate applies to
transitions out of `draft`.

## Constraints

Evaluator key added to the closed set; no new gate.

## Acceptance examples

### Example: normal behavior

**Given** a complete draft with `## Open decisions` reading `None.`

**When** approval is planned

**Then** `QGP-G1-AUTHORING` passes.

### Example: failure behavior

**Given** a draft whose title is still `<Observable obligation>`

**When** approval is planned

**Then** the gate fails naming the placeholder.

## Open decisions

None.
