+++
id = "ADR-IAR-007"
type = "adr"
title = "Classify diagnostics explicitly at emission"
status = "approved"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
decides = ["ARCH-IAR-007"]
+++

# ADR: Classify diagnostics explicitly at emission

## Status

Accepted on 2026-08-15 through the repository owner's instruction `ok i approve`.

## Context

SE Harness needs useful validation categories without splitting the command or inferring assurance from a score. Classification must remain correct when one diagnostic code is shared by rules with different authority.

## Options considered

1. Infer the plane from diagnostic-code ranges. Simple, but incorrectly couples public meaning to historical numbering and cannot classify reused codes accurately.
2. Apply one post-processing map from code to plane. Centralized, but still loses rule-level authority and permits ambiguous codes.
3. Split structure, governance, and policy into separate validators. Clear boundaries, but duplicates discovery and reporting and is disproportionate for the first increment.
4. Require each diagnostic emission to declare a plane from one closed vocabulary. Slightly more explicit code, but preserves rule-level meaning and supports one validator.

## Decision

Choose option 4. The diagnostic model carries an explicit plane. One centralized vocabulary validates values, while each rule owns its classification. Report renderers summarize existing error and warning collections by plane; they do not infer or change severity.

The public JSON change is additive and versioned. Human output remains recognizable and retains individual diagnostic details. Baseline tests compare pre-taxonomy and post-taxonomy results after removing only the newly added plane metadata and summary.

## Consequences

- Every new validation rule must deliberately choose a plane.
- Tests can reject unclassified rules.
- A shared diagnostic code may legitimately appear in more than one plane.
- Future profiles or inspection features may use the taxonomy, but this decision does not authorize them.
- The initial change touches many diagnostic construction sites mechanically, so regression comparison is mandatory.

## Rejected implications

This decision does not create separate validators, make maintenance warnings blocking, redesign repository policy, add orphan or aging heuristics, establish evaluator independence, or change accountable authority.
