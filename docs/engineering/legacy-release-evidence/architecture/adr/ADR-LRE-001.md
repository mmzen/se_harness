+++
id = "ADR-LRE-001"
type = "adr"
title = "Declare legacy release-evidence exemptions in the upgrade authorization packet"
status = "approved"
owners = ["technical-owner", "security-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
decides = ["ARCH-LRE-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T10:44:00Z"
decided_by = "technical-owner"
+++

# ADR: Declare legacy release-evidence exemptions in the upgrade authorization packet

## Status

Accepted, on the basis recorded in this domain's README. Acceptance authorizes the
implementation described by `WO-LRE-001` and nothing else. It does not authorize a
release, a publication, a governor adoption, a push, a pull request, a deployment,
or any edit to an artifact outside that work order's declared scope.

## Context

`SPEC-REB-001` forbids rewriting historical release records to add evaluator
evidence. Released 0.6.0 requires that evidence on every `released` release
record. Both are correct; together they make any repository with pre-existing
releases unable to adopt 0.6.0.

The existing escape is `LEGACY_RELEASES_WITHOUT_EVALUATOR_EVIDENCE`, a six-member
`frozenset` in the validator naming this repository's own releases. It is
distributed to consumers, who therefore inherit this repository's history as their
only permitted exception. Its only description in the artifact tree is a line in
non-authoritative evidence for `WO-REB-002`.

`REQ-REB-008` closes the nearest-looking alternative explicitly: the
predecessor-bootstrap contract is scoped to exactly one contract-bound bootstrap
release record, is stated not to be a missing-evidence allowlist, cannot fall back
to a generic one, requires a `ready` record, and never waives the binding.

The measured consequence in a consumer repository was a single `E012` that made
`validate` FAIL, the dashboard INVALID and `preflight` FAIL in both phases, on an
upgrade that was otherwise entirely clean. The repository had no forward path and
no clean way back.

What must be decided is where an exemption may be stated, what bounds it, and how
the components that must agree about it are kept in agreement.

## Decision drivers

- An exemption must be attributable to an accountable owner and reviewable in the
  diff that grants it.
- It must be impossible to grant at run time, from an environment value, or by a
  flag.
- It must not require, or tempt, an edit to an immutable record.
- It must not need restating at every subsequent upgrade, or the mechanism becomes
  a recurring tax and a recurring chance to freeze the repository by omission.
- It must be unable to cover a future release.
- The validator script must stay self-contained for consumers.
- A repository must not be able to reach the frozen state at all once this is
  shipped.

## Considered options

**Option 1: declare in the `[evaluator_upgrade]` packet.** Add one optional key
naming the records that predate enforcement. The packet is already the artifact
that authorizes crossing into schema-3 enforcement, already carries an accountable
`authorized_by`, and already lives in a work order whose approval is a dated
lifecycle event, which supplies the date guard for free.

**Option 2: a key in `.engineering-harness.toml`.** Simple and local, but that
file is managed, so a consumer editing it breaks integrity and the required gate.
Making it owner-editable would put a governance waiver in configuration rather
than in a governed artifact, with no accountable actor and no date.

**Option 3: extend the predecessor-bootstrap contract.** Reuses an existing
transition mechanism, but `REQ-REB-008` rules it out in terms, requires a `ready`
record this problem does not have, and is one-shot and version-scoped. Stretching
it would damage a contract that currently says exactly what it means.

**Option 4: a field on each release record.** Something like
`evaluator_evidence = "not-applicable"` on the record itself. This is the most
local and readable option, and it is rejected precisely because it requires editing
the immutable record, which is the thing the specification forbids and the thing
this decision exists to avoid.

**Option 5: broaden the hard-coded set, or make it a pattern.** Cheapest to
implement and the worst outcome: an unbounded, undated, unattributable waiver
compiled into the distribution, which `REQ-REB-008` already names as a non-goal.

**Option 6: downgrade the error to a warning for all unbound released records.**
Unfreezes every repository immediately and destroys the guarantee for records that
should carry a binding, including future ones. It cannot distinguish history from
negligence.

## Decision

Adopt option 1. The exemption is declared as
`legacy_releases_without_evaluator_evidence`, an optional array in the
`[evaluator_upgrade]` table of a work order whose status grants authority, and it
is accepted for a `released` record with both binding fields absent whose
`released_at` precedes the declaring work order's `draft` to `approved` instant.

Acceptance asks whether *some* authority-granting work order declares the record,
never whether the latest one does. A declaration is a historical fact about a
record that was already released; nothing later un-releases it, so nothing later
needs to repeat it.

Every accepted exemption emits `W024` on the maintenance plane, including those
granted by the compatibility set, so the debt is countable rather than absorbed.

The six-member compatibility set is kept, frozen and closed to additions, and is
documented as such in the specification rather than only in evidence. It is not
migrated onto the new mechanism here, because the work order that would have to
carry the declaration is `implemented` and belongs to another domain's in-flight
chain.

Two implementations of one semantics are accepted: the self-contained validator
script, and `se_harness/legacy_release_evidence.py` for the upgrade transaction.
Their equivalence is asserted against a shared committed vector fixture. The
alternatives, making the validator importable or making the installer shell out
to it, were rejected as changes to the self-hosting boundary and as making an
authorization decision depend on a subprocess.

`upgrade --apply` refuses before its first write when an undeclared unbound
`released` record exists, and a planning invocation reports the same as a notice.

## Consequences

### Positive

- A repository with pre-existing releases can adopt enforcement, and the act that
  permits it is a dated, attributable approval visible in a diff.
- No immutable record is edited, so the prohibition in `SPEC-REB-001` stays intact
  and unqualified.
- The exemption cannot reach a future release, cannot reach a `ready` record, and
  cannot reach a partially bound record.
- Declaring once is sufficient forever, so no later upgrade can freeze the
  repository by forgetting to restate it.
- The frozen state in issue #126 becomes unreachable: an upgrade that would cause
  it refuses instead.
- The exemption is countable on the dashboard for as long as it is in force.
- The mechanism, not just this repository's exception list, is finally described by
  an authoritative artifact.

### Negative and migration cost

- The `[evaluator_upgrade]` packet is a hand-written published contract, and this
  adds surface to it. The key is optional, so existing packets are unaffected, but
  once released the semantics can never be narrowed without breaking repositories
  that relied on it.
- The semantics exists twice. Duplication is a real maintenance cost and a real
  drift risk; it is mitigated by a shared vector fixture rather than eliminated.
  The precedent is already in the repository: the bootstrap contract is likewise
  implemented in both `repository_tools/release_bootstrap.py` and the validator.
- The validator now reads `[evaluator_upgrade]`, which it never did before. That
  couples the validation plane to the authorization packet's shape.
- A new warning code, `W024`, appears in consumer output. Repositories using the
  compatibility set will see six of them once they run a validator carrying this
  change.
- Nothing reaches a consumer until a later harness version is released, so a
  repository frozen today stays frozen until then. Its interim remedy is to remain
  on its current harness version.
- The compatibility set survives, so the repository-specific identifiers in
  distributed source are not yet gone. The intent's measure for that stays at six.

### Operational and security consequences

The declaration is the only new path by which repository content can relax a
governance error, and it is bounded on three independent axes simultaneously:
declarer authority, record state, and chronology. Defeating it requires forging a
lifecycle approval in a reviewed artifact, which is the same bar as every other
governance decision in the harness.

Fail-closed behaviour is preserved throughout. An absent declaration is not an
exemption. A malformed declaration is an error on the declarer, not an empty set. An
unreadable artifact during upgrade enumeration refuses rather than passes. The
refusal offers no override, so the recovery path is a governance act rather than a
retry.

No credential, network resource, subprocess or operator environment value
participates. No declaration content is used as a path, an import, a command or an
expression.

## Validation

`VER-LRE-001` carries the contract. The decision is validated when the two
implementations are proven equivalent on the shared vectors, when each fail-closed
case is proven to produce a diagnostic on the declarer, when a refused upgrade is
proven to leave the tree byte-identical, and when the measured freeze from issue
#126 is reproduced against the patched validator and shown to resolve to a pass
with one `W024`.
