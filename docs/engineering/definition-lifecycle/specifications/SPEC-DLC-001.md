+++
id = "SPEC-DLC-001"
type = "specification"
title = "Declared architecture-generation exemption"
status = "draft"
owners = ["technical-owner", "quality-owner", "repository-owner"]
created = "2026-08-26"
updated = "2026-08-26"

[relations]
specifies = ["REQ-DLC-001", "REQ-DLC-005"]
+++

# Specification: Declared architecture-generation exemption

## Scope

This specification defines how the harness decides whether an architecture
artifact carrying no `decision_assessment` table is exempt from the
required-assessment error. It replaces the inference from lifecycle status with
a frozen closed self-hosting set plus one bounded declaration inside an approved
work order.

It changes no lifecycle state, decision right, quality gate, relation, artifact
schema, or status vocabulary. It does not touch `W015`, the deprecated
`constrains` finding, which is resolved from relation shape and is independent
of status.

## Actors and external systems

- The released evaluator validating a target repository.
- The self-contained `scripts/validate_engineering_artifacts.py`, which must run
  inside a consumer repository without importing the package.
- The repository owner of a consumer repository holding pre-`decision_assessment`
  architectures.
- The engineering owner of the work order that carries a consumer declaration.
- `se_harness/legacy_release_evidence.py` and `SPEC-LRE-001`, as the approved,
  implemented, and verified precedent whose rules this specification mirrors.

## Inputs

Resolution is a pure function of governed artifact content. It reads:

- every architecture artifact's `id`, `decision_assessment` presence, and
  `relations`;
- every work order's `id`, `lifecycle_events`, and declaration packet; and
- the frozen self-hosting set compiled into both implementations.

It reads no lock, no installed evaluator identity, no environment value, no
command-line flag, and no Git state. It writes nothing and recomputes or
re-points no field.

## Outputs

For each architecture with no `decision_assessment`, one resolution:

- `exempt` with a source of `self-hosting-compatibility-set` or the declaring
  work-order identifier; or
- `not_exempt` with one stable machine-readable reason.

An `exempt` resolution produces one `W014` maintenance diagnostic. A
`not_exempt` resolution produces one `E014` governance error. An architecture
that is exempt still produces `E015` when no active ADR's `decides` relation
targets it, exactly as today.

## State model

The resolution is stateless and has no lifecycle. It is recomputed on every
validation run. The frozen set is closed at compile time and never grows. A
declaration's effect begins when its work order records a `draft -> approved`
lifecycle event and does not end.

## Behavioral rules

**DLC-GEN-001:** The frozen self-hosting compatibility set contains exactly the
fourteen architectures of this repository that predate `decision_assessment`:
`ARCH-AGR-001`, `ARCH-DST-001`, `ARCH-DST-002`, `ARCH-DST-003`, `ARCH-DST-004`,
`ARCH-DST-005`, `ARCH-IAR-001`, `ARCH-IAR-002`, `ARCH-IAR-003`, `ARCH-PMI-001`,
`ARCH-PYP-001`, `ARCH-REV-001`, `ARCH-VSP-001`, `ARCH-WLC-001`. The set is
closed: no identifier is ever added to it, and every new exemption uses a
declaration. Its declarer name is `self-hosting-compatibility-set`.

**DLC-GEN-002:** A consumer declaration is an array of architecture identifiers
under a stable field name inside a work order's declaration packet, bounded at
512 entries, matching the shape and bound `SPEC-LRE-001` already establishes for
`legacy_releases_without_evaluator_evidence`.

**DLC-GEN-003:** A declaration resolves only when its work order carries a
recorded `draft -> approved` lifecycle event. A declaration in a `draft` work
order resolves nothing.

**DLC-GEN-004:** A declared identifier resolves only when it matches the
architecture identifier pattern, names exactly one architecture in the graph,
and that architecture carries no `decision_assessment`. Zero matches, more than
one match, a non-architecture target, and an architecture that already carries
an assessment each resolve to a distinct stable reason.

**DLC-GEN-005:** The architecture's lifecycle status is not an input. The
constant `LEGACY_ARCHITECTURE_STATUSES` is removed from
`scripts/validate_engineering_artifacts.py` and from its canonical template, and
no replacement reads `artifact.status` in this assessment.

**DLC-GEN-006:** An exempt architecture is reported, every run, as a `W014`
maintenance diagnostic. Exemption suppresses the error and never the
diagnostic. There is no configuration, flag, or declaration field that
suppresses `W014`.

**DLC-GEN-007:** A declaration that resolves nothing produces one diagnostic
naming the declaration, its work order, and the exact reason, in addition to the
`E014` on each named architecture. A stale declaration — one naming an
architecture that has since gained an assessment — is reported and does not
resolve.

**DLC-GEN-008:** Resolution is fail-closed. An unreadable, malformed,
non-array, oversized, or duplicate-keyed declaration resolves nothing and does
not abort validation of unrelated artifacts.

**DLC-GEN-009:** The package module and the self-contained validator script
carry equivalent implementations and agree on a shared committed vector fixture
covering every rule above and every stable reason.

**DLC-GEN-010:** The diagnostic text for `W014` states that generation is
declared. It does not mention a lifecycle status, a compatibility window keyed
to status, or a migration that changes a status.

## Error and recovery behavior

Reasons are stable strings on the `SPEC-LRE-001` model: declaration shape,
declaration size, no approval on the declaring work order, invalid identifier,
unknown architecture, ambiguous architecture, target is not an architecture, and
architecture already assessed. Recovery is to add a `decision_assessment` table
to the architecture under governed work, or to correct and re-approve the
declaration. Recovery is never to change the architecture's lifecycle status,
which no longer has any effect here.

## Data and interface contracts

Declared identifiers are matched against `^ARCH-[A-Z][A-Z0-9-]*-\d{3}$`. The
declaration array is bounded at 512 entries, rejects duplicate object keys, and
is compared case-sensitively. The frozen set is an immutable frozen collection
in both implementations. No path, host value, or credential is an input.

## Security and privacy properties

Repository content, work-order text, and declaration arrays are untrusted parser
input. Resolution performs no network operation, no subprocess, no filesystem
write, and no Git operation. Diagnostics contain artifact identifiers, work-order
identifiers, and stable reasons only; they reproduce no file body, host path, or
environment value.

## Performance and capacity

Resolution is linear in the number of architectures plus the total number of
declared entries, bounded by 512 entries per declaration. It adds no measurable
cost to a validation run over 890 artifacts.

## Observability

Each validation run reports the total number of exempt architectures, the number
resolved from the frozen set, the number resolved from each declaring work
order, and every unresolved declaration with its reason. The run does not claim
that an exempt architecture is compliant, complete, or migrated.

## Compatibility and migration

- This repository's outcome is unchanged: 890 artifacts, 0 errors, 50 warnings —
  21 `W013`, 14 `W014`, 15 `W015` — with the `W014` identifier set identical
  before and after.
- A consumer repository holding pre-`decision_assessment` architectures must add
  a declaration under an approved work order before upgrading, or those
  architectures become `E014`. The upgrade path states this explicitly, and the
  governance-migration scenario for the version pair covers it.
- The status vocabulary is untouched. An architecture that is `implemented`
  remains valid and authority-granting; it simply no longer gains an exemption
  from being so.
- No architecture artifact is edited by this change.

## Examples and counterexamples

`ARCH-WLC-001` is exempt because it is named in the frozen set. It reports
`W014` and, because `ADR-WLC-001` decides it, no `E015`.

It is invalid for an architecture to become exempt by being transitioned to
`implemented`, for a declaration in a draft work order to resolve, for an
exemption to suppress `W014`, or for the frozen set to gain a fifteenth
identifier.

## Explicitly unspecified decisions

The implementation may choose the module layout, function and dataclass names,
the exact stable reason strings, the fixture file organization, and the
declaration packet's table name. It may not change the frozen set's membership
or closure, the 512-entry bound, the approval precondition, the fail-closed
behavior, the removal of the status input, or the rule that exemption never
suppresses `W014`.
