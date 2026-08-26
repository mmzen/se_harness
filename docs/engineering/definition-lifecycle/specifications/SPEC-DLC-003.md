+++
id = "SPEC-DLC-003"
type = "specification"
title = "Mandatory recorded decision chain for definition statuses"
status = "approved"
owners = ["technical-owner", "quality-owner", "repository-owner"]
created = "2026-08-26"
updated = "2026-08-26"

[relations]
specifies = ["REQ-DLC-004", "REQ-DLC-005"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-26T09:33:19Z"
decided_by = "technical-owner"
+++

# Specification: Mandatory recorded decision chain for definition statuses

## Scope

This specification closes the permission that lets a definition carry any status
without a recorded decision. It makes `lifecycle_events` mandatory for every
definition whose status is not `draft`, and it defines the declared pre-contract
exemption that keeps the 449 existing such definitions valid and visible.

It changes nothing about how an existing chain is validated. The chain-shape,
ordering, actor, and append-only rules already in `validate_lifecycle_events` are
unchanged; only the `events is None` early exit is replaced.

Out of scope: work orders, verification records, and release records; any edit to
an existing artifact; and any change to the status vocabulary.

## Actors and external systems

- The released evaluator validating a target repository.
- `scripts/validate_engineering_artifacts.py`, which must run standalone inside a
  consumer repository.
- The repository owner of a consumer repository holding hand-authored statuses.
- The engineering owner of the work order carrying a consumer declaration.
- `SPEC-LRE-001` and `se_harness/legacy_release_evidence.py`, the precedent for
  the declaration mechanism.

## Inputs

Resolution is a pure function of governed artifact content. It reads each
definition's `id`, `type`, `status`, and `lifecycle_events`; each work order's
`id`, `lifecycle_events`, and declaration packet; and the frozen pre-contract set
compiled into both implementations. It reads no lock, no installed evaluator
identity, no environment value, no command-line flag, and no Git state. It writes
nothing.

## Outputs

For each definition whose status is not `draft`:

- if a conforming chain is present, no new diagnostic;
- if no chain is present and a pre-contract exemption resolves, one `W025`
  maintenance diagnostic;
- if no chain is present and no exemption resolves, one `E022` governance error;
- if both a chain and a resolved exemption are present, one stale-declaration
  diagnostic and no `W025`.

A chain that is present but malformed continues to produce the existing
chain-consistency diagnostics and is not a candidate for the exemption.

## State model

Stateless; recomputed on every validation run. The frozen pre-contract set is
closed at compile time and never grows. A consumer declaration takes effect when
its work order records a `draft -> approved` lifecycle event and does not expire.

## Behavioral rules

**DLC-EVT-001:** A definition whose `status` is not `draft` requires a
`lifecycle_events` array. The nine definition families are in scope:
`intent`, `capability`, `requirement`, `specification`, `architecture`, `adr`,
`verification`, `release_contract`, `operating_contract`. `work_order`,
`verification_record`, and `release_record` are out of scope and unaffected.

**DLC-EVT-002:** A conforming chain's first event has `from = "draft"`, each
subsequent event's `from` equals the previous event's `to`, and the last event's
`to` equals the artifact's current `status`.

**DLC-EVT-003:** A definition in scope with no `lifecycle_events` key, or with an
empty array, and with no resolving exemption, reports `E022` in the governance
plane.

**DLC-EVT-004:** A chain that is present but skips a state, starts anywhere but
`draft`, or ends anywhere but the current status reports the existing
chain-consistency diagnostics. The exemption covers absence only and never
repairs a malformed chain.

**DLC-EVT-005:** The frozen self-hosting pre-contract set contains exactly the
449 definitions of this repository that carry a non-`draft` status and no
`lifecycle_events` at the candidate commit: 274 `approved`, 165 `implemented`, 7
`rejected`, and 3 `superseded`. The set is closed: no identifier is ever added,
and every later exemption uses a declaration. Its declarer name is
`pre-contract-definition-statuses`.

**DLC-EVT-006:** A consumer declaration is an array of definition identifiers
under a stable field name inside a work order's declaration packet, bounded at
512 entries, matching the shape and bound `SPEC-LRE-001` establishes for
`legacy_releases_without_evaluator_evidence`. A consumer needing more than 512
uses more than one approved declaration; the bound is per declaration.

**DLC-EVT-007:** A declaration resolves only when its work order carries a
recorded `draft -> approved` lifecycle event. A declaration in a `draft` work
order resolves nothing, and every definition it names reports `E022`.

**DLC-EVT-008:** A declared identifier resolves only when it matches the artifact
identifier pattern, names exactly one definition in the graph, that definition's
status is not `draft`, and that definition carries no `lifecycle_events`. Zero
matches, more than one match, a non-definition target, a `draft` target, and a
target that already has a chain each resolve to a distinct stable reason.

**DLC-EVT-009:** Every resolved exemption reports `W025` on every run. The
exemption suppresses the error and never the diagnostic. There is no
configuration, flag, or declaration field that suppresses `W025`.

**DLC-EVT-010:** Resolution is fail-closed. An unreadable, malformed, non-array,
oversized, or duplicate-keyed declaration resolves nothing, and validation of
unrelated artifacts continues.

**DLC-EVT-011:** Both implementations — the package module and the self-contained
validator script — agree on a shared committed vector fixture covering every rule
above and every stable reason.

**DLC-EVT-012:** No chain is fabricated, inferred, defaulted, or backfilled for
any artifact, by this change or by any tool it adds. A definition with no
recorded decision is reported as having none.

**DLC-EVT-013:** The `W025` diagnostic text states that the status predates the
recorded-decision obligation and is declared. It does not assert that the
decision was taken, does not name an actor, and does not name a date.

## Error and recovery behavior

`E022`'s message names the artifact, its status, and the fact that no chain
reaches that status, and states the two recovery routes: apply the transition
through `harnessctl transition` so the event is recorded, or declare the artifact
as pre-contract under an approved work order.

Declaration reasons are stable strings on the `SPEC-LRE-001` model: declaration
shape, declaration size, no approval on the declaring work order, invalid
identifier, unknown artifact, ambiguous artifact, target is not a definition,
target is `draft`, and target already has a chain.

A definition that is exempt is never described as compliant. `W025` is
outstanding work whose remedy is a real recorded decision, or an accepted
permanent record that none exists.

## Data and interface contracts

Declared identifiers are matched against `^[A-Z][A-Z0-9-]*-\d{3}$` and then
resolved against the definition families. Declaration arrays are bounded at 512
entries, reject duplicate object keys, and are compared case-sensitively. The
frozen set is an immutable frozen collection in both implementations. `E022` and
`W025` are reserved here and are the next free codes above the candidate
validator's existing `E021` and `W024`; if either is taken by a concurrent change
before implementation, the next free code is used and this specification is
amended.

## Security and privacy properties

Artifact metadata, work-order text, and declaration arrays are untrusted parser
input. Resolution performs no network operation, no subprocess, no filesystem
write, and no Git operation. Diagnostics contain artifact identifiers, statuses,
work-order identifiers, and stable reasons only.

## Performance and capacity

Resolution is linear in the number of definitions plus the total declared
entries. The frozen set holds 449 entries and is a constant-time membership test.
The added cost over 890 artifacts is not measurably distinguishable from the
existing lifecycle-event validation it extends.

## Observability

Each run reports the number of definitions requiring a chain, the number with a
conforming chain, the number exempt from the frozen set, the number exempt per
declaring work order, and every unresolved declaration with its reason. The run
never reports the exempt population as complete or migrated.

## Compatibility and migration

- This repository stays at 0 errors. The increment adds exactly 449 `W025`
  diagnostics and moves no existing count: 21 `W013`, 14 `W014`, 15 `W015`
  unchanged, and the total becomes 499 warnings.
- No artifact bytes change. In particular no chain is written for any of the 449,
  and the 6 `rejected` and 3 `superseded` ones are not touched, since inventing a
  decision for a rejected artifact would rewrite history.
- A consumer repository with hand-authored statuses must declare them under an
  approved work order before upgrading, or they become `E022`. The upgrade path
  states this, and the governance-migration scenario for the version pair covers
  it.
- This increment lands last of the three. It must not be authorized before
  `REQ-DLC-001` and `REQ-DLC-002`, because the 165 `implemented` statuses it would
  otherwise grandfather are the same ones those requirements are still reasoning
  about, and the frozen set must be measured once, after they settle.

## Examples and counterexamples

A new fixture requirement authored `status = "approved"` with no
`lifecycle_events` and named in no declaration reports `E022`; the same fixture
with a recorded `draft -> approved` event validates cleanly. A consumer
declaration naming 600 definitions in one array exceeds the bound, resolves
nothing, and every named definition reports `E022`.

It is invalid to fabricate a chain, to let an exemption suppress `W025`, to let a
declaration in a draft work order resolve, to add a 450th identifier to the
frozen set, or to extend the obligation to work orders or records under this
specification.

## Explicitly unspecified decisions

The implementation may choose the module layout, function and dataclass names,
the stable reason strings, the fixture organization, and the declaration packet's
table name. It may not weaken the obligation, fabricate a chain, reopen the
frozen set, raise or remove the 512-entry bound, drop the approval precondition,
suppress `W025`, or extend the scope beyond the nine definition families.

The 449 are declared by enumeration in a committed frozen vector, decided
2026-08-26 by the repository owner and recorded in `ADR-DLC-002`. A cutover date
over `created`, a Git-history boundary, and a per-artifact opt-out field are
rejected mechanisms, not implementation alternatives.

`W025` is emitted once per grandfathered definition on every run, decided
2026-08-26 by the repository owner. Aggregating the population into a single count
line, and rendering per-artifact detail only under a verbose flag, are both
forbidden: either would stop an individual missing decision from being visible in
the verdict.
