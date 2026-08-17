+++
id = "REQ-DST-047"
type = "requirement"
title = "Label artifact semantics without conflation"
status = "approved"
owners = ["product-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"
statement = "WHEN an artifact detail is displayed, THE SYSTEM SHALL label its type, lifecycle state, and derived assurance signal separately without presenting definition coverage as assurance."
verification_method = "automated-test-and-accessibility-review"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Label artifact semantics without conflation

## Rationale

The current header badge says `Definition covered`, `Specification only`, `Definition gap`, or `Not applicable` without naming the dimension. Replacing it with unlabeled colors would remain ambiguous, while treating definition coverage as assurance would be incorrect.

## Preconditions and trigger

This requirement applies to every focused formal artifact detail.

## Required response

- Show three text-bearing semantic labels: exact artifact type, exact lifecycle state, and derived assurance signal.
- Use the assurance vocabulary `assured`, `decision_required`, `attention`, and `not_assessed` so accountable decisions are not collapsed into generic attention.
- Prefix or otherwise programmatically name each dimension so values are understandable without position or color.
- Use stable distinct visual tokens while preserving text and non-color distinction.
- Remove the unnamed definition-coverage badge from the header.
- For requirements only, show specification coverage and verification-contract coverage as separately named Overview metadata fields.
- State that assurance is a derived Explorer signal and never a lifecycle transition or aggregate health score.

## Failure and boundary behavior

Unknown future type, state, or assurance values remain exact readable text with a deterministic fallback token. Missing coverage data is explicit for requirements and omitted for artifact types to which definition coverage does not apply.

## Constraints

- Never rename canonical artifact types or lifecycle states.
- Do not infer `assured` from test output, evidence presence, definition coverage, or color.
- Do not remove the `decision_required` distinction used for ready accountable records.
- Labels must remain readable at narrow widths and by assistive technology.

## Acceptance examples

### Example: implemented work order

**Given** an implemented work order without a verified commit-bound record,

**When** its detail is displayed,

**Then** the labels identify `Type - work_order`, `State - implemented`, and `Assurance - not assessed` without a `Definition covered` badge.

### Example: ready verification record

**Given** a ready verification record,

**When** its detail is displayed,

**Then** its assurance label says `Decision required`, not `Attention` or `Assured`.

## Open decisions

None when approved.
