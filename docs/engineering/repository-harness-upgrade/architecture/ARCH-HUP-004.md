+++
id = "ARCH-HUP-004"
type = "architecture"
title = "Adopt 0.7.0 through the existing standard-root boundary"
status = "draft"
owners = ["technical-owner", "security-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[relations]
addresses = ["REQ-HUP-012", "REQ-HUP-013"]
conforms_to = ["SPEC-HUP-006"]

[decision_assessment]
outcome = "no_significant_decision"
triggers = []
rationale = "The adoption reuses the boundary ADR-HUP-001 and ARCH-HUP-002 already selected: an external released evaluator, the ordinary standard upgrade, the schema-3 identity lock, the atomic evidence transaction, and separately governed post-publication adoption. No new boundary, trust relationship or policy is introduced."
assessed_by = "technical-owner"
+++

# Architecture: Adopt 0.7.0 through the existing standard-root boundary

## Components and responsibilities

- **External evaluator environment** (`C:\Users\mathi\se-harness-eval-070`
  or equivalent, outside the checkout): the only runtime that plans, applies
  and judges the transaction.
- **Standard upgrade transaction** (`harnessctl upgrade --apply`): writes the
  managed files and the lock atomically under `WO-HUP-006`'s identity table.
- **Repository-owned content**: owner regions of the fragment files and the
  rules outside the managed `.gitattributes` block; untouched by the
  transaction, adjusted by hand only where rule 8 of `SPEC-HUP-006` allows.
- **Qualification**: the same evaluator's `doctor`, `validate`, `inspect`,
  `dashboard`, preflight, plus the repository suites and hosted lanes.

## Control flow

Prove identity → plan and review → apply with evidence → no-op replay →
qualify with the new root → hand the candidate to the work order's
completion, verification and merge as separate acts.

## Trust boundaries

The checkout is untrusted input to the evaluator; the evaluator never imports
from it. The transaction writes only managed paths and the lock. Credentials,
network writes and external state are outside every step.

## Prohibited patterns

Editing managed files by hand; applying from candidate source; adopting from
an index install without the wheel-file digest; waiving a `customized` or
`conflict` result; touching product bytes or release history.

## Decision assessment

No ADR is required: the packet executes the previously decided adoption
mechanism without a new architectural choice.
