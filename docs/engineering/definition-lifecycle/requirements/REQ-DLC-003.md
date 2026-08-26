+++
id = "REQ-DLC-003"
type = "requirement"
title = "Derive definition realization from work-order and verification coverage"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-26"
updated = "2026-08-26"
statement = "WHEN the harness reports repository-wide attention or renders the artifact graph, THE SYSTEM SHALL derive each requirement's, specification's, and architecture's realization from the lifecycle state of every work order that names it and from the verification records bound to those work orders, SHALL name the exact commit of the covering verification records when every such work order is verified or released, SHALL report the definition as partially covered while any naming work order is not, and SHALL NOT store, write, or infer the derived result into any artifact field."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-DLC-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-26T09:33:19Z"
decided_by = "requirements-steward"
+++

# Requirement: Derive definition realization from work-order and verification coverage

## Rationale

Retiring the `implemented` state for definitions removes an answer to a real
question: which requirements have actually been built. The answer must be
restored, but in the one place where it can be correct.

A stored answer cannot be correct. 49 of the 104 requirements currently marked
`implemented` are named by more than one work order, and `REQ-DST-006` is named
by 16. A stored flag set when the first work order completes is falsified by the
second and, because the state is terminal, can never be corrected. A derived
answer recomputes on every read, so a sixteenth work order reopens coverage
automatically.

A derived answer is also strictly more informative. The graph already binds
`WO implemented -> VREC verified at an exact commit -> RLS released`, so
derivation can name the commit at which coverage holds. A status field never
can.

This is the shape the harness already uses for related judgments. The dashboard
and `inspect` share a finding vocabulary — `W-HEX-001` through `W-HEX-006`,
`W-REB-001` through `W-REB-003`, `W-REV-002` through `W-REV-004`, `I-REV-001` —
computed from the graph on every run and stored in no artifact.

## Preconditions and trigger

- `harnessctl inspect` runs against a valid graph.
- One or more work orders declare an `implements`, `specifications`, or
  `architecture` relation to the definition.

## Required response

- For each requirement, specification, and architecture, collect every work
  order naming it through the relevant relation.
- Classify the definition as covered when every collected work order is
  `verified` or `released` and at least one exists; as partially covered when at
  least one collected work order is `approved`, `in_progress`, or `implemented`;
  and as uncovered when no work order names it.
- For a covered definition, name the covering verification records and the exact
  commit each binds.
- Emit one informational finding for a covered definition and one warning-class
  finding for a partially covered one, in the existing shared code family, using
  reserved codes `I-DLC-001` and `W-DLC-001`.
- State in the rendered output that the derived result is a report: it grants no
  authority, approves nothing, and transitions nothing.
- Recompute on every run. Persist nothing.

## Failure and boundary behavior

- A definition named by no work order is uncovered, not a defect. Reporting it
  as an error would condemn every intent, capability, and verification contract.
- A definition named only by rejected or superseded work orders is uncovered.
- A work order whose verification record is `rejected` or `superseded` does not
  contribute coverage.
- The derivation reads governed artifact content only. It reads no lock, no
  installed evaluator identity, no environment value, and no Git state beyond
  the commits the records already bind.
- Adding a work order that names an already-covered definition moves it back to
  partially covered on the next run, with no transition, no edit, and no
  diagnostic about the earlier state.
- The derivation never writes an artifact and never proposes a transition. A
  code path that would do either is rejected by an independent write sentinel.

## Constraints

- No new artifact field, relation, artifact type, role, or gate.
- `HRN-006` holds: derivation is a report, and it never synchronizes a
  definition's state to its work orders'.
- The finding codes join the existing shared finding vocabulary and follow its
  existing rendering, ordering, and suggestion rules.
- The first increment renders the derivation in `inspect` only. The dashboard and
  explorer surfaces are deliberately deferred to separately approved work,
  decided 2026-08-26 by the repository owner. Until that work lands, this
  finding family appears in one reader and not the other — a known divergence
  from how `W-HEX-*`, `W-REB-*`, and `W-REV-*` behave, disclosed rather than
  resolved. The derivation itself must be surface-independent so the deferred
  work adds a renderer and no logic.
- Coverage must not be reported as verification. The accountable statement about
  a commit remains the verification record, and the derived finding cites it
  rather than restating it.
- The 165 existing `implemented` definitions are inputs to nothing here. Their
  status is not read by the derivation.

## Acceptance examples

### Example: normal behavior

**Given** a requirement named by three work orders, all `verified`

**When** `inspect` runs

**Then** the requirement is reported as covered, `I-DLC-001` is emitted, the
three verification records are named, and each bound commit is shown.

### Example: coverage reopens

**Given** that same covered requirement

**When** a fourth work order naming it is created and approved

**Then** the next run reports it as partially covered with `W-DLC-001`, names
the fourth work order as the outstanding one, and changes no artifact.

### Example: failure behavior

**Given** a requirement whose only naming work order is `implemented` with a
`rejected` verification record

**When** `inspect` runs

**Then** the requirement is partially covered, the rejected record is not
counted as coverage, and no commit is claimed.

## Recorded decisions

Decided 2026-08-26 by the repository owner: realization is a derived report that
grants no authority and is recorded in no artifact field. Making coverage an
approvable, stored fact under a new decision right was considered and declined,
because it would recreate the falsifiable stored claim that `REQ-DLC-002`
removes. The accepted consequence is that no artifact will ever again state that
a requirement is built — the answer exists only while a reader is running.

Decided 2026-08-26 by the repository owner: the classification is three-way.
`uncovered` is correct and permanent for every intent, capability, and
verification contract, and is never an error. A two-way covered / not-covered
split was declined because it collapses "no work order has ever named this" with
"three of four naming work orders are verified", and the second is the state that
needs attention.

Decided 2026-08-26 by the repository owner: `inspect` only in the first
increment; the dashboard surface is deferred.
