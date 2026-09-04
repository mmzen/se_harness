+++
id = "REQ-TCM-010"
type = "requirement"
title = "A success measure outlives the work order"
status = "draft"
owners = ["product-owner", "quality-owner"]
created = "2026-09-04"
updated = "2026-09-04"
statement = "WHEN an intent draft's success-measure row names a CI run, test, validator, verification or implementation review as its observation, THE VALIDATOR SHALL report the row as an acceptance check."
verification_method = ["test"]
priority = "must"
source = "docs/notes/assessment-intent-readability-2026-09-04.md: 12 intents without a table; 47 of 101 rows targeting 0; observation windows such as every CI run, packet verification and implementation review"

[relations]
derives_from = ["CAP-TCM-001"]
+++

# Requirement: A success measure outlives the work order

## In plain words

A success measure is something an operator can count or time after
delivery, without reading the code. A row that is proved once by a test or
a CI run is an acceptance check, and it belongs in the verification
contract. The validator says so on the draft.

## Why

The authoring checklist asks for a measure observable after delivery and
the guidance asks that a reader can tell, years later, whether the outcome
was reached. The corpus's tables say otherwise: their windows are `every
CI run`, `packet verification` and `implementation review`, and forty-seven
targets are `0`. Such a row is true the day the work order closes and tells
the future reader nothing. Nothing mechanical distinguishes the two kinds.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| A success-measure row of an intent draft has an `Observed` cell naming a CI run, test, validator run, verification or implementation review | One advisory names the file and the row's measure | Not applicable; an advisory never fails validation |
| A success-measure table of an intent draft has no row | One advisory says the intent states no measure | Not applicable |
| A row's `Today` cell reads `not measured` | No advisory; the honest baseline is accepted | Not applicable |

## Examples

### Normal

**Given** an intent draft whose rows are observed in the Explorer overview
at each release review and in pull-request threads counted per release,

**When** the repository is validated,

**Then** no advisory names the table.

### Failure

**Given** an intent draft with the row "validator blocks violations, 0,
0, every CI run",

**When** the repository is validated,

**Then** one advisory names the row as an acceptance check that belongs in
the verification contract, and validation passes.
