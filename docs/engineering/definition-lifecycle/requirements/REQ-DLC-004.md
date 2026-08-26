+++
id = "REQ-DLC-004"
type = "requirement"
title = "Require a recorded decision for every definition state past draft"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-26"
updated = "2026-08-26"
statement = "WHEN a definition artifact carries any status other than draft, THE SYSTEM SHALL require an append-only lifecycle_events chain that starts at draft and reaches that status, SHALL report a definition without such a chain as an error unless a declared pre-contract exemption resolves for it, and SHALL report every resolved pre-contract exemption as an outstanding maintenance diagnostic."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-DLC-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-26T09:33:19Z"
decided_by = "requirements-steward"
+++

# Requirement: Require a recorded decision for every definition state past draft

## Rationale

449 of 630 definitions — 71% — carry no `lifecycle_events` at all: 274
`approved`, 165 `implemented`, 7 `rejected`, and 3 `superseded`. For the
majority of the governing graph there is no recorded answer to who approved this
artifact and when.

`HRN-005` and `WFL-004` say only an explicit actor decision and an applied
transition change lifecycle state. The validator nonetheless accepts a
hand-authored status in silence: `validate_lifecycle_events` begins `events =
artifact.metadata.get("lifecycle_events"); if events is None: continue`.

That single permission is the reason the other two defects in this domain grew
undetected behind a clean zero-error verdict. 165 definitions were authored
straight into a terminal state that no decision right grants and no procedure
step performs, and nothing objected. Closing the permission is what stops the
next such divergence from being invisible.

Once an event chain exists the validator already checks it thoroughly. This
requirement makes the chain mandatory rather than optional; it changes nothing
about how an existing chain is validated.

## Preconditions and trigger

- The formal graph is being validated.
- A definition artifact's status is not `draft`.

## Required response

- Require an append-only `lifecycle_events` array whose first event has `from =
  "draft"` and whose last event's `to` equals the artifact's current status,
  with each event's `from` equal to the previous event's `to`.
- Report a definition without such a chain as an error, in the governance plane,
  under the reserved code `E022`.
- Resolve a pre-contract exemption from two sources only, on the
  `SPEC-LRE-001` pattern: a frozen self-hosting declaration for this
  repository's own 449 pre-contract definitions, and a bounded explicit
  declaration inside an approved work order for a consumer repository's own.
- Report every resolved pre-contract exemption as a maintenance diagnostic under
  the reserved code `W025`, so an exempted definition stays visible as
  outstanding work rather than becoming permanently invisible.
- Apply the obligation to the nine definition families only. Work orders,
  verification records, and release records are out of scope for this
  requirement.

## Failure and boundary behavior

- A chain that skips a state, starts anywhere but `draft`, or ends anywhere but
  the current status is an error under the existing chain-consistency rules, not
  a candidate for the pre-contract exemption. The exemption covers absence
  only.
- A definition with both a chain and a resolved exemption reports the exemption
  as stale and does not report `W025`.
- A declaration in an unapproved work order does not resolve, and the named
  definitions report `E022`.
- The exemption is fail-closed. An unreadable, malformed, oversized, or
  ambiguous declaration resolves nothing.
- This requirement introduces no route by which a status may be authored without
  either a decision or an explicit, approved, visible declaration that it
  predates the obligation.

## Constraints

- No artifact bytes change. In particular, no `lifecycle_events` chain is
  fabricated for any of the 449. Inventing a decision that was never taken would
  be worse than recording its absence, and for the 6 already-`rejected` and 3
  `superseded` ones it would rewrite history.
- The self-hosting exemption is frozen at exactly the 449 definitions present at
  the candidate commit. It is closed: no identifier is ever added, and every
  later exemption uses a declaration.
- Both implementations — package module and self-contained validator script —
  agree on a shared committed vector fixture, as `SPEC-LRE-001` already
  requires for its own declaration.
- This requirement lands last of the three. It must not be authorized before
  `REQ-DLC-001` and `REQ-DLC-002`, because the 165 statuses it would otherwise
  have to grandfather are the same ones those two requirements are still
  reasoning about.

## Acceptance examples

### Example: normal behavior

**Given** this repository at the candidate commit

**When** the graph is validated

**Then** the verdict has 0 errors, `E022` is emitted for no artifact, and `W025`
is emitted for exactly the 449 declared pre-contract definitions.

### Example: the permission is closed

**Given** a new fixture requirement authored with `status = "approved"` and no
`lifecycle_events`, named in no declaration

**When** the graph is validated

**Then** `E022` is reported for it, and the same fixture with a recorded
`draft -> approved` event validates cleanly.

### Example: failure behavior

**Given** a consumer-repository declaration naming 600 pre-contract definitions

**When** the graph is validated and the declaration exceeds the bounded entry
count

**Then** the declaration resolves nothing, every named definition reports
`E022`, and the diagnostic names the bound that was exceeded.

## Recorded decisions

Decided 2026-08-26 by the repository owner: the 449 pre-contract definitions are
declared by enumeration in a committed frozen vector. A frozen cutover date over
`created`, a Git-history boundary, and a per-artifact opt-out field were all
considered and declined; `ADR-DLC-002` records why.

Decided 2026-08-26 by the repository owner: `E022` and `W025` are reserved, with a
next-free fallback. If a concurrent change takes either code before
implementation, the implementation uses the next free code and reports that
`SPEC-DLC-003` needs amending rather than blocking on a number.

Decided 2026-08-26 by the repository owner: `W025` is emitted once per
grandfathered definition, on every run. Aggregating the 449 into a single count
line was considered and declined, because an individual artifact's missing
decision would stop being visible and no one could see progress as chains are
added. The accepted cost is that the verdict grows from 50 warnings to 499, and
that reviewers must be told a large count here records honesty rather than new
breakage.
