+++
id = "REQ-LRE-001"
type = "requirement"
title = "Accept a declared pre-enforcement released record as unbound and report it as debt"
status = "approved"
owners = ["repository-owner", "quality-owner", "security-owner"]
created = "2026-08-24"
updated = "2026-08-24"
statement = "WHEN a released release record carries neither evaluator-evidence field, THE SYSTEM SHALL accept it as unbound only if an authority-granting upgrade work order declares its identifier and was approved after the record was released, SHALL report every accepted record as an outstanding maintenance diagnostic, and SHALL reject a declaration that does not resolve to such a record."
verification_method = "automated-validator-and-cross-implementation-test"

[relations]
derives_from = ["CAP-LRE-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T10:44:00Z"
decided_by = "repository-owner"
+++

# Requirement: Accept a declared pre-enforcement released record as unbound and report it as debt

## Rationale

The prohibition on rewriting released records and the obligation to bind
evaluator evidence to them are both correct. What is missing is the third thing:
a way to state that a specific record was written before the obligation existed.
Without it the harness ships a rule that a repository's own history can make
permanently unsatisfiable, and the only escape is a hard-coded set naming this
repository's releases.

A declaration is the right shape because it is a fact rather than a
configuration. It lives in the artifact that authorized the transition, it is
attributable to the owner who approved that work order, and it is visible in the
diff that introduces it. Being a fact, it does not need to be restated: a later
upgrade does not un-release a record that was already released.

The date guard is what keeps it from becoming a general waiver. A declaration can
only reach records that were already released when it was approved, so it can
never pre-authorize an unbound future release.

## Preconditions and trigger

- Artifact validation loads the artifact graph of a repository.
- A release record with status `released` is examined for the evaluator-evidence
  binding.
- The graph may contain zero or more work orders carrying an
  `[evaluator_upgrade]` table.

## Required response

- Read the optional key `legacy_releases_without_evaluator_evidence` from the
  `[evaluator_upgrade]` table of every work order whose status grants authority
  under the managed work-order lifecycle. Treat its absence as an empty
  declaration.
- Accept a `released` release record as unbound when, and only when, both
  evaluator-evidence fields are absent and at least one such work order names its
  identifier and has a `draft` to `approved` decision instant strictly later than
  the record's `released_at`.
- Continue to require the binding for every other release record, including a
  `ready` record and a record carrying exactly one of the two fields.
- Emit one maintenance-plane warning for each accepted record, naming the record
  and the declaring work order, for as long as the exemption is in force.
- Reject, as a governance error attributed to the declaring work order, a
  declared identifier that is not a well-formed release-record identifier, that
  resolves to no release record, that resolves to a record whose status is not
  `released`, that resolves to a record carrying either evaluator-evidence field,
  or whose record has no usable `released_at` earlier than the declaring work
  order's approval instant.
- Reject, as a governance error attributed to the declaring work order, a
  declaration that is not an array of strings, that exceeds the declared bound, or
  that appears in a work order with no `draft` to `approved` lifecycle event.
- Keep the existing six-identifier self-hosting compatibility set accepted without
  a declaration, subject to the same maintenance warning, and closed to further
  identifiers.
- Leave every other evaluator-evidence check, including current-lock matching for
  `ready` records and archive-identity checks, exactly as it is.

## Failure and boundary behavior

An absent declaration is not an exemption; the record fails with the existing
error. A declaration that does not resolve fails closed on the work order rather
than silently covering nothing, so an identifier typed wrongly is visible instead
of inert. A record whose `released_at` is missing, malformed, or not strictly
earlier than the approval instant is never exempt. A partially bound record is
never exempt and its existing error is unchanged.

Ordering of identifiers within a declaration is irrelevant to acceptance;
duplicates are collapsed; diagnostic output is deterministic. Declarations are
data only: no path, expression, command or executable appears in one. Nothing in
this requirement writes, recomputes or repoints any record field, performs a
lifecycle transition, uses a credential, publishes, deploys, or adopts a
governor.

## Constraints

The validator script must remain self-contained, so it resolves declarations from
the artifact graph alone with no import from the harness package. Identifier
matching uses the existing release-record identifier pattern. Timestamp
comparison uses the existing `YYYY-MM-DDTHH:MM:SSZ` form and its lexicographic
ordering. The declaration array is bounded so that a hostile artifact cannot make
validation expensive.

## Acceptance examples

### Example: normal behavior

**Given** a repository holding `RLS-XYZ-001` with status `released`,
`released_at = "2026-08-19T17:53:05Z"` and no evaluator-evidence fields, and an
`implemented` work order whose `[evaluator_upgrade]` table declares
`legacy_releases_without_evaluator_evidence = ["RLS-XYZ-001"]` and whose `draft`
to `approved` event is `2026-08-24T09:00:00Z`,

**When** artifact validation runs,

**Then** no error is reported for `RLS-XYZ-001`, exactly one maintenance warning
names `RLS-XYZ-001` and the declaring work order, and validation passes.

**Given** the same repository after a later upgrade work order that carries an
`[evaluator_upgrade]` packet and declares nothing,

**When** artifact validation runs,

**Then** the outcome is unchanged, because the earlier declaration remains an
authoritative fact.

### Example: failure behavior

**Given** the same record but no work order declaring it,

**When** artifact validation runs,

**Then** the record fails with the existing evaluator-evidence error and
validation fails.

**Given** a declaration naming `RLS-XYZ-002`, a record released at
`2026-08-24T11:00:00Z`, later than the declaring work order's approval instant,

**When** artifact validation runs,

**Then** a governance error is reported on the declaring work order naming
`RLS-XYZ-002`, and the record itself still fails the binding.

**Given** a record carrying `evaluator_evidence_path` but no
`evaluator_evidence_sha256`, and a declaration naming it,

**When** artifact validation runs,

**Then** the record's existing error stands and a governance error is reported on
the declaring work order, because a partially bound record is never exempt.

## Open decisions

None.
