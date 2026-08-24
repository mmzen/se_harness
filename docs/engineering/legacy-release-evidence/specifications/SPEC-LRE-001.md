+++
id = "SPEC-LRE-001"
type = "specification"
title = "Declared legacy release-evidence exemptions and pre-apply upgrade refusal"
status = "approved"
owners = ["technical-owner", "quality-owner", "security-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
specifies = ["REQ-LRE-001", "REQ-LRE-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T10:44:00Z"
decided_by = "technical-owner"
+++

# Specification: Declared legacy release-evidence exemptions and pre-apply upgrade refusal

## Scope

Define one optional declaration inside the `[evaluator_upgrade]` authorization
packet, one resolution rule from that declaration to an accepted exemption, one
maintenance diagnostic per accepted exemption, one governance error class for
declarations that do not resolve, and one pre-apply refusal in the upgrade
transaction.

Out of scope: the capture, canonical form and hashing of evaluator evidence; the
`ready` record binding written by `prepare-release`; the predecessor-bootstrap
contract; verification-record bindings; the retirement or migration of the
six-identifier self-hosting compatibility set; any release, publication or
governor adoption.

## Actors and external systems

- Artifact validation consumes the artifact graph, resolves exemptions, and
  reports errors and warnings.
- The upgrade transaction consumes the same declaration semantics before writing,
  and refuses or notices.
- Dashboard publication consumes the same semantics so its release view agrees
  with validation.
- Repository owners declare, and are named as the accountable actor of the
  declaring work order's approval.
- No external service, credential, network resource or operator environment value
  participates.

## Inputs

- Work-order artifacts carrying an `[evaluator_upgrade]` table, including the
  optional key `legacy_releases_without_evaluator_evidence`.
- Work-order `status` and `[[lifecycle_events]]`.
- Release-record artifacts, their `status`, `released_at`, and their
  `evaluator_evidence_path` and `evaluator_evidence_sha256` fields.
- The managed work-order lifecycle registry, for the authority-granting states.
- The frozen six-identifier self-hosting compatibility set.

All inputs are untrusted repository content and are validated before use.

## Outputs

- Zero or more `E012` governance diagnostics attributed to a declaring work order.
- Zero or more `W024` maintenance diagnostics attributed to an exempt release
  record.
- A deterministic mapping from exempt release-record identifier to the identifier
  of the artifact that exempted it, consumed by validation, by dashboard
  publication and by the upgrade refusal.
- A refusal or a notice from the upgrade transaction.

## State model

A `released` release record is in exactly one of four states with respect to the
evaluator-evidence binding: `bound`, when both fields are present and valid;
`partially-bound`, when exactly one is present; `legacy-declared`, when both are
absent and an accepted declaration covers it; and `legacy-undeclared`, when both
are absent and no accepted declaration covers it. Only `legacy-declared` is
accepted without the binding. `legacy-undeclared` keeps its existing error, and
`partially-bound` keeps its existing error and can never become
`legacy-declared`.

A record never leaves `legacy-declared` by later repository activity, because the
declaration that placed it there is a lifecycle fact of an artifact that is itself
never rewritten.

## Behavioral rules

1. **Declaration location and shape.** The declaration is the optional key
   `legacy_releases_without_evaluator_evidence` inside a work order's
   `[evaluator_upgrade]` table. Its value is an array of strings. Absence means an
   empty declaration. A value that is not a list, a member that is not a string,
   or more than 512 members is a defect.
2. **Canonical field set.** `[evaluator_upgrade]` still requires exactly the nine
   fields `schema`, `scope`, `prior_lock_sha256`, `target_version`,
   `target_payload_sha256`, `target_archive_name`, `target_archive_sha256`,
   `publication` and `authorized_by`.
   `legacy_releases_without_evaluator_evidence` is the only permitted optional
   key. Any further key remains rejected.
3. **Authoritative declarers.** A declaration is read only from an artifact whose
   `type` is `work_order`, whose `status` grants authority under the managed
   work-order lifecycle, and whose `[evaluator_upgrade]` table declares
   `schema = "se-harness-evaluator-upgrade-v1"` and
   `scope = "standard-root-only"`. A `draft`, `ready`, `rejected` or `superseded`
   work order declares nothing, and its declaration is neither honoured nor
   reported as a defect.
4. **Approval instant.** The declaring work order's approval instant is the
   `decided_at` of its last `draft` to `approved` lifecycle event, in
   `YYYY-MM-DDTHH:MM:SSZ` form. An authoritative work order carrying a non-empty
   declaration and no such event is a defect and declares nothing.
5. **Accepted exemption.** A release record is `legacy-declared` when all hold:
   its `status` is `released`; both `evaluator_evidence_path` and
   `evaluator_evidence_sha256` are absent; and at least one authoritative
   declaring work order names its identifier and has an approval instant strictly
   greater than the record's `released_at` under lexicographic comparison of the
   canonical timestamp form.
6. **Declarations are permanent facts.** Acceptance asks whether some
   authoritative work order declares the record. It never asks whether the most
   recent one does. A later upgrade work order that carries a packet and declares
   nothing revokes nothing, and no declaration is restated to remain in force.
7. **Partial bindings.** A record with exactly one of the two fields is never
   exempt. Its existing diagnostic is unchanged, and a declaration naming it is a
   defect.
8. **Non-released records.** A declaration naming a record whose status is not
   `released` is a defect. `ready` records keep the binding, current-lock matching
   and archive checks they have today.
9. **Fail closed on unresolved declarations.** Each declared member that does not
   match the release-record identifier pattern, matches no release record, matches
   more than one, matches a record that is not `released`, matches a record
   carrying either binding field, or whose record has an absent, malformed, or not
   strictly earlier `released_at`, produces one `E012` governance diagnostic on the
   declaring work order naming that member and the reason. A declaration is never
   silently inert.
10. **Visible debt.** Each `legacy-declared` record produces exactly one `W024`
    maintenance diagnostic on the record, naming the record and the declaring
    work order. Where more than one authoritative work order declares the same
    record, the lexicographically smallest declaring identifier is named, so the
    diagnostic is stable.
11. **Self-hosting compatibility set.** The six identifiers `RLS-SEH-001`,
    `RLS-SEH-002`, `RLS-SEH-004`, `RLS-SEH-005`, `RLS-SEH-006` and `RLS-SEH-007`
    remain exempt with no declaration, under the same both-fields-absent and
    `released` conditions. The set is frozen: no identifier is added to it, and
    the mechanism for any new exemption is rule 5. An exemption granted by the set
    produces the same `W024` with the declarer rendered as
    `self-hosting-compatibility-set`.
12. **Pre-apply refusal.** An upgrade that will write a schema-3 lock enumerates
    `released` records with both fields absent, subtracts those accepted under
    rule 5 and rule 11, and refuses before its first write when the remainder is
    non-empty. The refusal message lists the remaining identifiers in sorted
    order and names the authorizing work order as the artifact whose
    `[evaluator_upgrade]` table must declare them. A planning invocation reports
    the same list as a notice and does not refuse.
13. **Byte-identical refusal.** A refused upgrade writes nothing: no managed file,
    no lock, no configuration file and no evidence file.
14. **One semantics, two implementations.** The validator script resolves
    declarations from the artifact graph with no import from the harness package,
    and the upgrade transaction resolves them through the harness package. The two
    implementations agree on every case of a shared canonical vector fixture, and
    that agreement is asserted by test.
15. **No rewriting.** Nothing in this contract writes, recomputes or repoints any
    field of any release record, verification record, work order or lock. No
    lifecycle transition, credential use, publication, deployment or governor
    adoption follows.
16. **Declarations are data.** No import path, expression, shell command, path or
    repository-provided executable appears in a declaration. The array is read as
    data and never evaluated.

## Error and recovery behavior

A defect under rules 1, 4, 7, 8 or 9 is a governance-plane `E012` on the declaring
work order. The record it names keeps whatever diagnostic it already had; a defect
in the declaration never removes an error from a record.

An unreadable or malformed artifact encountered while enumerating for rule 12
refuses the upgrade with that reason rather than being treated as an absence. A
missing artifact tree yields an empty enumeration and no refusal.

Recovery from a refusal is a governance act, not a retry: the owner adds the
identifier to the authorizing work order's declaration, or explains why the record
is not legacy. The command offers no override.

## Data and interface contracts

`legacy_releases_without_evaluator_evidence` is an array of release-record
identifiers matching `^[A-Z][A-Z0-9-]*-\d{3}$` with the `RLS-` prefix. Order is
insignificant to acceptance; duplicates are collapsed. The resolution result is a
mapping from record identifier to declarer identifier, where the declarer is a
work-order identifier or the literal `self-hosting-compatibility-set`.

`W024` messages state the record identifier, the declarer, and that the record
predates evaluator-evidence enforcement.

## Security and privacy properties

The declaration widens what validates, so it is bounded on three axes at once:
the declarer must be an authority-granting work order carrying a valid
`standard-root-only` packet, the record must already be `released` with both
fields absent, and the record must have been released before the declaration was
approved. No run-time input can substitute for any of the three. A declaration
cannot cover a future release, cannot cover a `ready` record, cannot cover a
partially bound record, and cannot be supplied outside a reviewed artifact diff.

Exact-byte trust for records that do carry a binding is untouched. No content of a
declaration reaches a filesystem path, a subprocess or an evaluated expression. No
secret, credential or personal datum is read or emitted.

## Performance and capacity

Resolution is a single pass over already-loaded artifacts and is linear in their
count. Declarations are bounded at 512 members each. The upgrade enumeration
reads artifact front matter only, under the existing per-artifact size bound, and
adds no network or subprocess work.

## Observability

Every exemption in force is countable from `validate --json` and from the
dashboard by its `W024` code and `maintenance` plane. A defective declaration is
countable by its `E012` on a work-order path. A refused upgrade prints the
complete list of undeclared identifiers, not a sample.

## Compatibility and migration

Existing repositories are unaffected: an absent optional key is an empty
declaration, and the six-identifier set continues to behave exactly as it does
today. No existing artifact requires an edit.

A repository frozen by the defect in issue #126 migrates by adding the
declaration to the work order that authorized its upgrade, which is an ordinary
work-order edit under that work order's own scope, and then re-running
validation. If the repository has not yet upgraded, rule 12 stops it before it
freezes.

The mechanism reaches consumers only through a later released harness version.
Until that release exists this repository's own gate runs the frozen managed
evaluator recorded in `.engineering-harness.toml`, so the candidate change alters
no gate here.

## Examples and counterexamples

Accepted: a record released at `2026-08-19T17:53:05Z` with both fields absent,
declared by an `implemented` work order approved at `2026-08-24T09:00:00Z`. One
`W024`, no error.

Accepted: the same repository after two further upgrades whose work orders declare
nothing. Unchanged, by rule 6.

Rejected: the same record with no declaration anywhere. The existing binding error
stands.

Rejected: a declaration naming a record released at `2026-08-24T09:00:01Z` by a
work order approved at `2026-08-24T09:00:00Z`. `E012` on the work order, by rule
9, and the record still fails the binding.

Rejected: a declaration naming a `ready` record, by rule 8. Rejected: a
declaration naming a record with only `evaluator_evidence_path`, by rule 7.
Rejected: a declaration inside a `draft` work order, which by rule 3 declares
nothing and is silent.

Rejected: an upgrade against a repository holding one undeclared unbound
`released` record. Refused before any write, by rule 12, with the repository
byte-identical.

## Explicitly unspecified decisions

Whether the six-identifier compatibility set is eventually retired, and whether
this repository's own history is migrated onto rule 5, are deliberately left
open; both require a separate chain and would touch an implemented work order in
another domain. Whether a future harness version reports `W024` as an error once
consumers have had a migration window is likewise left open. Neither question is
answered here, and neither is prejudged by this contract.
