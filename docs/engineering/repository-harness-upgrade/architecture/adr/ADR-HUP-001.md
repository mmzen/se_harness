+++
id = "ADR-HUP-001"
type = "adr"
title = "Version-independent governor succession assessment"
status = "approved"
owners = ["technical-owner", "repository-owner", "security-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[relations]
decides = ["ARCH-HUP-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T20:22:49Z"
decided_by = "technical-owner"
+++

# ADR: Version-independent governor succession assessment

## Status

Proposed.

## Context

The root upgrade made 0.6.0 the current governor, but an always-on workflow
still installed exact 0.5.0 and required the current checkout to satisfy the
historical 0.5.0 bootstrap contract. Replacing 0.5.0 constants with 0.6.0 would
make CI green only until the next upgrade.

## Decision drivers

- Support future governor versions without per-version workflow rewrites.
- Keep ordinary current-governor validation simple and authoritative.
- Never let untrusted PR content choose an executable without independent
  identity and approval checks.
- Preserve a visible hosted check and bounded evidence during migration.
- Avoid permanent predecessor-compatible views of current governance.

## Considered options

1. Hard-code 0.6.0 in the old workflow. Smallest immediate edit, but repeats
   the defect at 0.7.0.
2. Delete the old workflow. Removes the failure, but silently removes the
   transition observation and may conflict with required-check policy.
3. Continue evaluating current governance through a permanent predecessor
   compatibility view. Preserves the historical tool but retains the complexity
   and split-authority failure mode that root adoption was intended to end.
4. Separate steady-state managed validation from a version-independent,
   identity-bound transition assessment.

## Decision

Choose option 4. The transition workflow compares one trusted base with target
`HEAD`. Equal governor identities produce a deterministic not-applicable
observation. Changed identities require one approved upgrade declaration,
matching canonical transaction evidence, independently verified exact target
evaluator, complete target-root qualification, and checkout immutability.

Historical compatibility remains available only as immutable evidence or an
explicit fixture/manual rehearsal. It is not part of ordinary current-root CI.

## Consequences

- Positive: later upgrades change governed identity/evidence data rather than
  workflow control logic; N never validates N+1; Linux and Windows agree.
- Negative: event-derived base selection and identity consistency require a
  small security-sensitive resolver with exhaustive negative tests.
- Operational: the workflow file and check remain during the correction, but
  their purpose changes from one historical version to generic succession.
- Security: target evaluator execution is permitted only after archive,
  payload, origin, approval, and evidence agreement; no credentials persist.
- Migration: the failed candidate and ready VREC remain immutable; a successor
  candidate and aggregate VREC are required.

## Validation

Use `VER-HUP-004`, including future-version synthetic fixtures, exact 0.5.0 to
0.6.0 hosted reproduction, tampered identity/evidence cases, LF/CRLF cases,
complete tests, and checkout-clean proof.
