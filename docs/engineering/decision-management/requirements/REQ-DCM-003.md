+++
id = "REQ-DCM-003"
type = "requirement"
title = "An accepted deviation stays visible until the rule changes"
status = "draft"
owners = ["technical-owner", "quality-owner", "product-owner"]
created = "2026-09-03"
updated = "2026-09-03"
statement = "WHEN a decision of kind deviation is disposed with the option accept, THE SYSTEM SHALL keep it visible as a standing deviation on the departed specification, on the work order, and on every verification or release record covering that work, until a later decision amends or supersedes the departed rule."
verification_method = ["test", "inspection"]
priority = "must"
source = "docs/notes/decision-artifact-proposal-2026-09-03.md, section 4.2; the Lineage prefetch deviation accepted under WO-DST-023 and recorded only in SPEC-DST-023 prose"
measure = "every accepted deviation appears in the Explorer on its specification, work order and records, in the record's evidence, and raises a maintenance warning once its revisit trigger has passed"

[relations]
derives_from = ["CAP-DCM-001"]
+++

# Requirement: An accepted deviation stays visible until the rule changes

## Rationale

A deviation has two halves: the fact that an implementation cannot meet a
rule, and the decision about what to do. Amending or superseding the rule
closes the gap. Accepting the gap does not: after `accept`, the
specification no longer describes the shipped behaviour, and every reader
of that rule, every reviewer of the work and every consumer of the release
must be able to see it. An acceptance that disappears into a reason field
is a silent amendment. An acceptance without a revisit trigger is a
permanent one.

## Behavior

- Trigger: a decision with `kind = "deviation"`, an `against` reference to
  one rule of one specification, and an `observed` fact is disposed with
  the option `accept` and a `revisit` trigger.
- Response: the decision is projected as a standing deviation on the
  departed specification, on the work order it concerns, and on every
  verification or release record whose covered work includes that work
  order; the record's evidence discloses it; the Explorer shows it on each
  of those artifacts with its revisit trigger.
- On failure: `accept` without `revisit` is refused. When the revisit
  trigger has passed and no later decision has amended or superseded the
  rule, the validator raises a maintenance warning on the specification. A
  second accepted deviation against the same rule raises a second warning.

## Assumptions and dependencies

- The decider is the owner of the specification in `against`
  (`REQ-DCM-002`).
- The options `amend` and `supersede` produce an amendment record or a
  successor under the same work order; the decision names what it produced.
- The Explorer's record panel and proof block already render lifecycle
  events and can carry the projection (`SPEC-DST-023`).

## Acceptance examples

### Example: an accepted deviation is visible everywhere it matters

**Given** `DEC-X-002` (deviation, against `SPEC-X-001` rule 7, concerning
`WO-X-002`) is disposed `accept` with revisit "the next design round",

**When** `WO-X-002` completes and `VREC-X-003` is captured and verified,

**Then** the Explorer shows the standing deviation on `SPEC-X-001`,
`WO-X-002` and `VREC-X-003`, and the record's evidence names `DEC-X-002`.

### Example: acceptance is time-bounded

**Given** the same deviation with no `revisit`,

**When** the technical owner applies `decide DEC-X-002 --option accept`,

**Then** the command is refused and the decision stays `open`.

## Open decisions

None.
