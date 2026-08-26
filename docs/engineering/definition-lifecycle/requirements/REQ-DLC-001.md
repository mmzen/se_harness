+++
id = "REQ-DLC-001"
type = "requirement"
title = "Resolve architecture generation from a declaration, not from lifecycle status"
status = "draft"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-26"
updated = "2026-08-26"
statement = "WHEN the harness assesses an architecture artifact that carries no decision_assessment table, THE SYSTEM SHALL resolve the required-assessment exemption only from a frozen self-hosting compatibility set of exact architecture identifiers and from an explicit declaration in an approved work order, SHALL NOT read the architecture's lifecycle status when resolving that exemption, and SHALL continue to report every resolved exemption as an outstanding maintenance diagnostic."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-DLC-001"]
+++

# Requirement: Resolve architecture generation from a declaration, not from lifecycle status

## Rationale

`LEGACY_ARCHITECTURE_STATUSES = {"implemented", "verified", "released"}` in
`scripts/validate_engineering_artifacts.py` is the only place a definition's
lifecycle status changes a validation outcome. An architecture in one of those
states with no `decision_assessment` is grandfathered to a `W014` maintenance
warning, with `E015` only when no active ADR decides it. The same gap on an
`approved` architecture is a hard `E014`.

Status is a poor proxy for the fact it stands in for. Measured at `c189b58`:

| Architecture cohort | `decision_assessment` | `constrains` | n |
|---|---|---|---:|
| `approved` | present | absent | 36 |
| `implemented` | absent | present | 14 |
| `implemented` | present | absent | 13 |
| `implemented` | present | present | 1 |

The 14 grandfathered architectures are exactly the second row, and exactly the
14 that raise `W014`. The other 14 `implemented` architectures are
modern-shaped and gain nothing from the proxy, so status is a 50%-accurate
signal for generation. Worse, the proxy is bidirectional: promoting a modern
`approved` architecture to `implemented` would silently move it into the legacy
path, and demoting a legacy one to `approved` would convert its warning into an
error.

The repository has already solved this exact class of problem once.
`SPEC-LRE-001` and `se_harness/legacy_release_evidence.py` replace an inferred
pre-contract exemption with a frozen closed self-hosting set of six
`RLS-SEH-*` identifiers plus a bounded declaration inside an approved work
order's packet, resolved as a pure function of governed artifact content. That
pattern is approved, implemented, and verified. This requirement applies it to
architecture generation.

## Preconditions and trigger

- The formal graph is being validated by the released evaluator or by the
  repository validator script.
- An architecture artifact carries no `decision_assessment` table.
- Any declaring work order and its `lifecycle_events` are readable from
  governed artifact content alone.

## Required response

- Resolve the exemption from two sources only: a frozen closed set of exact
  architecture identifiers naming this repository's own pre-contract
  architectures, and a bounded declaration array inside an approved work
  order.
- Resolve it as a pure function of governed artifact content. Read no lock, no
  installed evaluator identity, no environment value, and no command-line flag.
- Require the declaring work order to carry a recorded `draft -> approved`
  lifecycle event, on the `SPEC-LRE-001` rule.
- Emit one maintenance diagnostic for every architecture whose exemption
  resolves, so an accepted exemption is never silent.
- Emit `E014` for an architecture with no `decision_assessment` whose exemption
  does not resolve, whatever its lifecycle status.
- Keep the existing `E015` obligation: an exempted architecture still requires
  an active ADR whose `decides` relation targets it.
- Stop consulting the architecture's lifecycle status in this assessment.

## Failure and boundary behavior

- A declaration that is not an array of strings, exceeds its bounded entry
  count, names an unknown or ambiguous identifier, names a non-architecture
  artifact, or sits in a work order with no recorded approval does not resolve.
  The named architecture falls back to `E014`.
- A declaration that names an architecture which already carries a
  `decision_assessment` does not resolve and is reported as a stale
  declaration.
- The frozen set is closed. No identifier is ever added to it; every new
  exemption uses a declaration.
- Both implementations — the package module and the self-contained validator
  script that must run inside a consumer repository without importing the
  package — agree on a shared committed vector fixture.

## Constraints

- The change is outcome-neutral on this repository. Before and after, the
  released `0.6.0`-lineage verdict is 0 errors and 50 warnings: 21 `W013`, 14
  `W014`, 15 `W015`.
- No architecture artifact's bytes, status, relations, or events change.
- `W015`, which reports the deprecated `constrains` relation, is independent of
  status and is not in scope. Its count stays at 15, including `ARCH-IAR-004`,
  which raises `W015` but not `W014`.
- The frozen set contains exactly the 14 identifiers measured at `c189b58`:
  `ARCH-AGR-001`, `ARCH-DST-001`, `ARCH-DST-002`, `ARCH-DST-003`,
  `ARCH-DST-004`, `ARCH-DST-005`, `ARCH-IAR-001`, `ARCH-IAR-002`,
  `ARCH-IAR-003`, `ARCH-PMI-001`, `ARCH-PYP-001`, `ARCH-REV-001`,
  `ARCH-VSP-001`, `ARCH-WLC-001`.
- No new role, gate, relation, artifact type, or lifecycle state is introduced.

## Acceptance examples

### Example: normal behavior

**Given** this repository at the candidate commit

**When** the released-lineage evaluator validates the graph

**Then** the verdict is 0 errors and 50 warnings, the 14 maintenance warnings
for missing architecture assessments are emitted for exactly the 14 frozen
identifiers, and no diagnostic cites a lifecycle status as its cause.

### Example: status no longer decides

**Given** a fixture architecture with no `decision_assessment`

**When** its status is set to `implemented`, `verified`, or `released` and it
appears in neither the frozen set nor any declaration

**Then** validation reports `E014` for each status, identically to `approved`.

### Example: failure behavior

**Given** a work order declaring an exemption for a fixture architecture

**When** that work order has no recorded `draft -> approved` lifecycle event

**Then** the exemption does not resolve, the architecture reports `E014`, and
the diagnostic names the unapproved declaring work order.

## Open decisions

Before approval, the technical and repository owners must accept the frozen set
as closed at exactly those 14 identifiers, the declaration's location and field
name inside a work-order packet, and the bounded entry count.
