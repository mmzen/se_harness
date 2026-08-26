+++
id = "ADR-DLC-002"
type = "adr"
title = "Grandfather pre-contract artifacts by enumerated frozen vector rather than cutover date"
status = "draft"
owners = ["technical-owner", "quality-owner", "repository-owner"]
created = "2026-08-26"
updated = "2026-08-26"

[relations]
decides = ["ARCH-DLC-001"]
+++

# ADR: Grandfather pre-contract artifacts by enumerated frozen vector rather than cutover date

## Status

Proposed.

## Context

`ADR-DLC-001` decides that grandfathering moves from status inference to explicit
declaration. It does not decide the shape of the declaration, and the two
populations are very different sizes:

- 14 architectures predating `decision_assessment`, all in this repository.
- 449 definitions carrying a non-`draft` status with no `lifecycle_events`: 274
  `approved`, 165 `implemented`, 7 `rejected`, and 3 `superseded`.

`SPEC-LRE-001` already established a shape for the small case: a frozen, closed,
named compatibility set of six release identifiers compiled into both
implementations, plus a bounded array in an approved work order for consumers.
The mechanism is approved, implemented, and verified. It has never been exercised
at 449 entries.

An enumerated 449-entry vector is a large committed constant. The obvious
alternative is a frozen cutover instant compared against each artifact's
`created` field: two lines of code instead of 449 lines of data, and it scales to
a consumer with 10,000 pre-contract artifacts without a declaration at all.

That alternative has a specific problem. `created` is an artifact metadata field
that is authored by hand and is not bound to any commit, decision, or evidence.
Nothing in the graph verifies it. A date-based exemption therefore makes the
exemption boundary depend on a field an author controls freely, which means a new
artifact can be exempted from the recorded-decision obligation by writing an
earlier date in it. The obligation being introduced is precisely that a status
must not be self-asserted; grandfathering it by another self-asserted field
reintroduces the defect at one remove.

## Decision drivers

- `HRN-001`: the declaration must be an artifact fact, not a derived guess.
- The exemption must be closed. A grandfathering mechanism that can admit new
  members is not grandfathering; it is a permanent bypass.
- The exemption must be auditable: a reviewer must be able to see exactly which
  artifacts are exempt, from one place, without running anything.
- The mechanism must reuse the approved `SPEC-LRE-001` shape unless there is a
  concrete reason it cannot.
- A consumer repository may hold far more pre-contract artifacts than this one.
- No artifact byte may change, and no decision may be fabricated.
- Diff and review cost of a large committed constant is real but is paid once.

## Considered options

### Option A: enumerated frozen vector for both populations

Compile a frozen 14-identifier set and a frozen 449-identifier set into both the
package module and the self-contained validator script, each with a named
declarer, exactly as `SPEC-LRE-001` does with its six.

The exemption is closed by construction: adding a member is a visible code change
under an approved work order, reviewable line by line. A reviewer reads the
membership from the constant. The mechanism is already approved and verified at
small scale.

The 449-entry constant appears twice, is 449 lines in each copy, and must be
generated once and then frozen. Its correctness at the moment of freezing depends
on the measurement being taken at the right commit.

### Option B: frozen cutover instant over `created`

Store one frozen timestamp. An artifact is exempt when its `created` value
precedes it.

Two lines instead of 898, no per-artifact maintenance, and it scales to any
consumer size without a declaration at all. It is rejected because `created` is
hand-authored and verified by nothing. A new artifact backdated past the cutover
is silently exempt from the very obligation being introduced, and the mechanism
cannot detect it. The exemption would not be closed, only quiet. The
`superseded` and `rejected` artifacts in the population also carry `created`
values that reflect authoring rather than decision, so even the honest reading of
the field is not the reading the exemption needs.

### Option C: frozen commit boundary

Exempt any artifact whose introducing commit is an ancestor of a frozen commit,
resolved through Git history.

This uses a fact no author can forge, which fixes Option B's defect. It is
rejected because it makes the exemption depend on Git state. Every mechanism in
this domain is specified as a pure function of governed artifact content reading
no Git state, and the harness already has hard evidence that Git-derived facts
are fragile: depth-1 checkouts change validator output, and a rebase orphans a
bound commit. Resolution would differ between a shallow CI checkout and a full
clone, which is the exact class of defect the purity constraint exists to
prevent.

### Option D: a per-artifact opt-out field

Add a `pre_contract = true` field to each of the 449 artifacts.

Rejected outright. It changes 449 artifact files, which `REQ-DLC-005` forbids and
which would be a mass edit of historical records including 6 rejected ones. It
also puts the exemption inside the artifact claiming it, so an author could grant
themselves one.

### Option E: enumerated vector here, cutover date offered to consumers

Use Option A for this repository's two sets, and let a consumer declare a cutover
date instead of enumerating.

Rejected as the worst of both. It ships the forgeable boundary as a supported
public surface while this repository declines to rely on it, and it means the two
implementations must support two resolution modes. If the boundary is not good
enough here, it is not good enough to publish.

## Decision

Select Option A.

Grandfather both populations by enumerated frozen vector. Compile a 14-identifier
architecture set with declarer name `self-hosting-compatibility-set` and a
449-identifier definition set with declarer name
`pre-contract-definition-statuses`, into both the package module and the
self-contained validator script, and hold both closed: no identifier is ever
added to either, and every later exemption uses a work-order declaration.

Keep the consumer surface identical to `SPEC-LRE-001`'s: a bounded array of
identifiers inside an approved work order's declaration packet, 512 entries per
declaration, resolving only after a recorded `draft -> approved` event,
fail-closed, and reported when it resolves nothing. A consumer needing more than
512 uses more than one approved declaration. No date mode and no Git mode is
offered.

Measure the 449-identifier set once, at the candidate commit of increment 3,
after increments 1 and 2 have settled — the population includes the 165
`implemented` definitions those increments are still reasoning about, and a set
frozen before they settle would be frozen around a moving target.

Accept the diff cost. Both constants are generated by a committed, re-runnable
measurement whose output is compared against the constant in the test suite, so
the freezing step is itself verifiable rather than a manual transcription.

## Consequences

### Positive

- The exemption is closed by construction. Admitting a new member requires a
  visible code change under an approved work order.
- A reviewer can read the exact exempt population from one constant without
  running anything or consulting Git.
- Resolution stays a pure function of governed artifact content, identical in a
  depth-1 CI checkout and a full clone.
- No self-asserted field can grant an exemption, which is the whole point of the
  obligation being introduced.
- One mechanism, already approved and verified, covers both new obligations and
  the existing release-evidence case.
- No artifact byte changes and no decision is fabricated.

### Negative

- A 449-line constant appears in two files and must stay byte-consistent between
  them. It is the largest committed constant in the project.
- A consumer with thousands of pre-contract artifacts must author multiple
  approved declarations of 512 entries each. That is deliberate friction, and it
  will be experienced as friction.
- Generating the set correctly depends on measuring at the right commit, which is
  a sequencing obligation on increment 3 rather than a property the mechanism
  enforces.
- Reviewing the increment-3 diff requires trusting the measurement script rather
  than reading 449 identifiers individually, so the script and its comparison
  test carry real review weight.
- The set can never be trimmed. An artifact that later gains a real
  `lifecycle_events` chain remains in the constant, is reported as a stale
  declaration, and stays there — visible, correct, and slightly untidy forever.

### Operational and security

- Declared identifiers, declaration arrays, and work-order text are untrusted
  parser input; arrays are bounded, duplicate-key rejecting, and fail-closed.
- Both constants are compile-time immutable and are not configurable,
  overridable, or extendable at runtime by any flag or environment value.
- No network, subprocess, filesystem write, Git operation, or lock read.
- Diagnostics contain identifiers, statuses, work-order identifiers, and stable
  reasons only.

### Migration

- The 14-identifier set is measured at increment 1's candidate and asserted equal
  to the 14 architectures currently reporting `W014`.
- The 449-identifier set is measured at increment 3's candidate and asserted
  equal to the definitions then carrying a non-`draft` status with no chain.
- A consumer upgrading across either boundary declares its own population under
  an approved work order first, or the affected artifacts become `E014` or
  `E022`. Each increment ships a governance-migration scenario stating this.
- Neither set is ever extended for a consumer. Consumers use declarations.

## Validation

- Assert both constants are frozen immutable collections in both implementations
  and that the two copies agree.
- Re-run the generating measurement in the test suite and assert its output
  equals the committed constant exactly.
- Assert the 14-identifier set equals the `W014` identifier set at increment 1's
  merge base.
- Fixture-remove each frozen identifier and assert the artifact becomes `E014` or
  `E022` accordingly.
- Assert no code path admits a date, a Git reference, an environment value, a
  flag, or an artifact-supplied field as an exemption input.
- Assert a declaration of 513 entries resolves nothing and names the bound, and
  that two approved 512-entry declarations resolve together.
- Assert a declaration in a `draft` work order resolves nothing.
- Assert a stale declaration — a named artifact that has since gained an
  assessment or a chain — is reported and does not resolve.
- Assert both implementations agree on the shared committed vector fixtures for
  every stable reason.
