+++
id = "VER-LRE-001"
type = "verification"
title = "Legacy release-evidence declaration, fail-closed resolution and pre-apply refusal assurance"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
verifies = ["REQ-LRE-001", "REQ-LRE-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T10:44:00Z"
decided_by = "quality-owner"
+++

# Verification Contract: Legacy release-evidence declaration, fail-closed resolution and pre-apply refusal assurance

## Independence

Assurance builds its own repository fixtures rather than reusing the ones the
implementation was written against, and constructs its own boundary cases for
chronology, status and partial binding. It asserts diagnostics by code, plane and
path as they appear in the report, never by asking the implementation whether it
considers a record exempt.

Equivalence of the two implementations is asserted from a committed vector file
that both are driven against, so a shared misreading is visible as a vector that
neither satisfies rather than as two implementations agreeing with each other.

The end-to-end claim is verified against the real repository that produced issue
#126, at a recorded commit, by running the patched candidate validator over it.
Assurance reads that repository's `RLS-MOK-001` front matter itself and confirms
byte-for-byte that no field of it changed.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-LRE-001` | Acceptance case | `released` record, both fields absent, declared by an `implemented` work order approved after `released_at` | No error for the record; exactly one `W024` on the maintenance plane naming the record and the declarer; report is valid |
| `REQ-LRE-001` | Authority matrix | The same declaration carried by a work order in each of `draft`, `ready`, `approved`, `in_progress`, `implemented`, `verified`, `released`, `rejected`, `superseded` | Exempt in exactly the five authority-granting states; silent and non-exempt in the others |
| `REQ-LRE-001` | Permanence case | Earlier declaring work order plus a later `[evaluator_upgrade]` work order that declares nothing | Exemption still accepted; no error; the later packet is not consulted for revocation |
| `REQ-LRE-001` | Chronology boundary | Approval instant equal to, one second before, and one second after `released_at` | Exempt only when strictly after; the equal case is a defect |
| `REQ-LRE-001` | Partial-binding case | Record with only `evaluator_evidence_path`, and record with only `evaluator_evidence_sha256`, each declared | Existing binding error stands in both; `E012` also reported on the declarer |
| `REQ-LRE-001` | Non-released case | Declaration naming a `ready` record and naming a `rejected` record | `E012` on the declarer; the `ready` record keeps its binding, current-lock and archive checks |
| `REQ-LRE-001` | Unresolved-declaration matrix | Member that is not a well-formed identifier; member matching no record; member matching a non-record artifact; duplicate members; 513 members; value that is a string; value that is a table | Each produces `E012` on the declarer with the reason; duplicates collapse without error; none is silently inert |
| `REQ-LRE-001` | Undated-declarer case | Authority-granting work order with a non-empty declaration and no `draft` to `approved` event | `E012` on the declarer; nothing exempted |
| `REQ-LRE-001` | Absent-declaration case | The same record with no declaration anywhere in the graph | Existing evaluator-evidence error stands; report is invalid |
| `REQ-LRE-001` | Compatibility-set case | The six frozen `RLS-SEH-*` identifiers with both fields absent | Exempt with no declaration; one `W024` each with the declarer rendered as the compatibility set |
| `REQ-LRE-001` | Packet canonicality | `[evaluator_upgrade]` with the nine required fields plus the one optional key, and with one further unknown key | The optional key is accepted; the unknown key is still rejected by `upgrade_authorization` |
| `REQ-LRE-001` | Unchanged-behaviour regression | Full graph validation of this repository with the candidate validator | Error count unchanged from baseline; no new error class; existing warnings unchanged apart from the compatibility-set `W024` entries |
| `REQ-LRE-002` | Refusal case | Repository with one undeclared unbound `released` record, `upgrade --apply` | Command fails; message lists the identifier and names the authorizing work order; no exit-zero path |
| `REQ-LRE-002` | Byte-identity case | The tree before and after the refused invocation | Every tracked path, the lock and the configuration file are byte-identical; no evidence file created |
| `REQ-LRE-002` | Declared-pass case | The same repository with the declaration present | Transaction proceeds exactly as at baseline, including the replay no-op postcondition, and validates afterwards |
| `REQ-LRE-002` | Planning case | The same undeclared repository, planning invocation only | Plan is reported with a notice listing the identifier; no refusal; nothing written |
| `REQ-LRE-002` | No-history case | Repository with no release record, and repository with no artifact tree | No new condition; transaction proceeds unchanged |
| `REQ-LRE-002` | Fail-closed enumeration | Unreadable artifact, oversized artifact, and invalid TOML front matter in the artifact tree during enumeration | Refusal with the reason; never treated as an absence of records |
| Both | Cross-implementation equivalence | Committed canonical vector fixture driven against the validator script and `se_harness/legacy_release_evidence.py` | Identical accepted mapping and identical defect set for every vector |
| Both | End-to-end reproduction | The consumer repository from issue #126 at its recorded commit, upgraded and validated with the patched candidate validator | `validate` passes with zero errors and exactly one `W024`; `RLS-MOK-001` front matter is byte-identical to its pre-upgrade state |

## Acceptance scenarios

1. A repository holding one pre-enforcement `released` record and a declaration in
   its upgrade work order validates clean, with the exemption visible as one
   `W024`.
2. Removing that declaration makes the repository fail with the existing
   evaluator-evidence error and nothing else.
3. Two further upgrades whose work orders declare nothing leave the exemption
   intact.
4. A declaration naming a record released one second after the declaring work
   order's approval is rejected on the work order.
5. Upgrading a repository that holds an undeclared unbound `released` record fails
   before writing, and the repository is byte-identical afterwards.
6. Planning that same upgrade succeeds and reports the identifier as a notice.
7. This repository's own six compatibility-set records remain exempt and produce
   six `W024` entries and no error under the candidate validator.
8. An `[evaluator_upgrade]` packet carrying any key beyond the nine required and
   the one optional is still rejected.
9. The consumer repository from issue #126 upgrades and validates clean without a
   single byte of `RLS-MOK-001` changing.

## Property and invariant tests

- Resolution is deterministic: the same artifact set yields the same accepted
  mapping and the same defect list across repeated runs and across artifact
  iteration orders.
- Resolution is order-insensitive and duplicate-insensitive within a declaration.
- Resolution is monotone in declarations: adding an authority-granting declaration
  never turns an accepted record into a rejected one and never removes an error
  from a different artifact.
- No accepted exemption exists without a corresponding `W024`, and no `W024` exists
  without an accepted exemption. The two counts are equal in every fixture.
- No fixture in which the implementation runs produces a modified artifact byte;
  the fixture tree digest is compared before and after.
- Authority-granting statuses used by both implementations equal the set derived
  from the managed work-order lifecycle registry, asserted rather than hard-coded
  in the test.

## Static and architecture checks

- The validator script imports nothing from `se_harness`, asserted by inspecting
  its import statements.
- `se_harness/legacy_release_evidence.py` imports neither `installer` nor any
  module that reads the lock or the installed evaluator identity.
- Neither implementation reads `os.environ`, parses a command-line flag, or
  consults local configuration during resolution.
- No declaration value reaches a filesystem call, a subprocess, an import or an
  evaluated expression, asserted by inspection and by a fixture whose declaration
  members are hostile strings.
- The compatibility set contains exactly the six documented identifiers in both
  the candidate validator and the dashboard publisher.

## Security and privacy checks

- A declaration in a non-authority-granting work order never exempts, in every one
  of the four non-granting states.
- A declaration can never cover a record released after the declarer's approval,
  including at the exact-equality boundary.
- A declaration can never cover a `ready` record, a `rejected` record, a partially
  bound record, or a verification record.
- Hostile declaration members, including path traversal strings, absolute paths,
  identifiers with embedded newlines, and very long strings, produce a bounded
  diagnostic and no filesystem access.
- The refusal cannot be overridden by any environment variable, flag or
  configuration value, asserted by attempting each.
- Existing evaluator-evidence checks for bound records, including archive identity
  and current-lock matching, are unchanged, asserted by their existing tests
  passing untouched.

## Performance and resilience checks

- Resolution adds no filesystem pass during validation; it consumes artifacts
  already loaded.
- A declaration is bounded at 512 members and a fixture at the bound completes
  within the existing per-test budget.
- The upgrade enumeration respects the existing per-artifact size bound and makes
  no network or subprocess call.
- Full-suite wall time on the reference platforms stays within the recorded
  baseline envelope.

## Manual assessments

- Security owner accepts that repository content may now relax a governance error,
  on the stated bounds of declarer authority, record state and chronology, and
  confirms that no run-time input can substitute for any of them.
- Quality owner accepts the two-implementation design and reviews the shared vector
  fixture for coverage of every rule in `SPEC-LRE-001`.
- Repository owner accepts that the six-member compatibility set survives frozen,
  that six `W024` entries will appear in consumer-facing validation of this
  repository, and that the mechanism reaches consumers only through a later
  released version.
- Release owner confirms that nothing in this packet builds, binds, publishes or
  promotes a distribution.

## Evidence retention

`WO-LRE-001` evidence retains: the baseline error and warning counts of this
repository before and after the change; the full test result before and after,
with platform, Python version and skip counts; the complete diagnostic text of
every negative case; the shared vector fixture and the equivalence result for both
implementations; the refused-upgrade transcript together with the before-and-after
tree digest proving byte identity; the planning-path transcript; the end-to-end
reproduction against the issue #126 repository including its commit, the upgrade
transcript, the passing validation output with its single `W024`, and the
unchanged `RLS-MOK-001` front matter; and the explicit list of actions not
performed, naming at least the absence of any push, pull request, release, tag,
publication and consumer upgrade.

## Residual uncertainty

A repository already frozen by this defect stays frozen until a later harness
version ships, and that release is outside this contract. Whether the
compatibility set is retired, whether this repository's own history migrates onto
the declaration, and whether `W024` later becomes an error after a migration
window are all deliberately unsettled by `SPEC-LRE-001` and remain unverified
here. Consumer repositories that hold release records this repository has never
seen remain outside the observed set; the end-to-end evidence covers one real
consumer, not a population.
