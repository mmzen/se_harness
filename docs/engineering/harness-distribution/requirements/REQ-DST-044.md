+++
id = "REQ-DST-044"
type = "requirement"
title = "Explain canonical EARS requirement statements"
status = "approved"
owners = ["requirements-steward", "product-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"
statement = "WHEN a focused requirement has a canonical EARS statement, THE SYSTEM SHALL visually distinguish its recognized EARS clauses while preserving the exact statement and avoiding a false validation claim."
verification_method = "automated-test-and-accessibility-review"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Explain canonical EARS requirement statements

## Rationale

Color-assisted clause recognition can make trigger, system, obligation, and response boundaries easier to scan. The referenced Prism demonstration is useful visually but acknowledges ambiguous combined-trigger cases and depends on remote code. Explorer must not turn a presentational tokenizer into a second requirements validator.

## Preconditions and trigger

This requirement applies only to an artifact whose exact canonical type is `requirement` and whose projected `statement` is nonempty.

## Required response

- Present the exact statement as a dedicated EARS block before the artifact body.
- Recognize clause markers case-insensitively, including `WHERE`, `WHILE`, `WHEN`, `IF`, optional `THEN`, the system/subject phrase, `SHALL`, and the response.
- Distinguish recognized clauses with stable color plus text, legend, underline, weight, or another non-color cue.
- Preserve whitespace and punctuation meaning; never rewrite the statement into a preferred form.
- Describe the result as highlighting or clause recognition, never as syntax validation, compliance, approval, or correctness.
- If clause recognition is incomplete or ambiguous, show the complete escaped statement and an explicit `unclassified` indication rather than guessing.

## Failure and boundary behavior

Non-EARS prose and complex combined triggers remain readable. Tokenization is deterministic, bounded, and cannot create markup, selectors, URLs, or executable behavior from statement content.

## Constraints

- No Prism CDN or additional runtime URL is authorized.
- The validator and formal requirement artifact remain the only authorities for required fields and lifecycle consistency.
- The highlighting must remain understandable without color and at narrow widths.

## Acceptance examples

### Example: event-driven requirement

**Given** `WHEN a reader selects an artifact, THE SYSTEM SHALL present its details.`,

**When** the requirement is focused,

**Then** the trigger, subject/obligation, and response are distinguishable while the exact statement remains available to assistive technology.

### Example: ambiguous combined trigger

**Given** a statement combines multiple `WHEN` and `IF` clauses beyond the recognized pattern,

**When** it is focused,

**Then** Explorer preserves the exact statement, marks the uncertain portion unclassified, and does not report a validation error.

## Open decisions

None when approved.
