+++
id = "SPEC-REB-014"
type = "specification"
title = "Consumer-installed validator without predecessor-bootstrap rules"
status = "approved"
owners = ["technical-owner", "engineering-owner", "release-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[relations]
specifies = ["REQ-REB-029"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-27T20:11:19Z"
decided_by = "technical-owner"
reason = "Approved on 2026-08-27 by the accountable owner, 'i approve the 3 draft artifacts', on the owner review of pull request #206. Specifies the part of REQ-REB-029 that SPEC-REB-013 excluded in terms: the candidate copy of the hash-locked managed validator. SPEC-REB-013 keeps its full force alongside this specification and is not amended, narrowed or replaced; PV001 and PV002 stay reserved by it. Rule 3's finding that no tolerance shim is required is accepted as measured on the current file. Rule 4 moves the retained-digest guarantee to the repository's own suite. Rule 5 preserves REQ-REB-011 exactly. Rule 6 accepts a template-versus-root divergence as the expected state until the root evaluator next advances. The root copy is not edited under this specification either."
+++

# Specification: Consumer-installed validator without predecessor-bootstrap rules

## Scope

The removal of the predecessor-bootstrap and predecessor-view rules from the
candidate copy of the managed validator, and the state of the six closed 0.6.0
artifacts under a validator that no longer knows those schemas. Completes
`REQ-REB-029`, whose measure `SPEC-REB-013` left unmet by excluding the managed
validator from `WO-REB-028`.

`SPEC-REB-013` continues to bind alongside this specification, and both are
selected by `WO-REB-029`. This specification adds the managed-validator rules
`SPEC-REB-013` excludes; it does not amend, narrow or replace anything
`SPEC-REB-013` states.

## Actors and external systems

The candidate copy at `templates/repository/standard/scripts/`, which is what a
consumer repository installs. The root copy at `scripts/`, which is the exact
released evaluator's file and is not an actor here. The six closed 0.6.0
artifacts, which are read but never written. The repository's own test suite,
which takes over one guarantee the validator gives up.

## Inputs

The candidate validator source; the artifact graph of any repository it is
installed into; the retained `[bootstrap]` tables and `preparation_*` fields of
the six closed artifacts.

## Outputs

A validator with no rule that reads a `[bootstrap]` tuple, resolves a bootstrap
contract for a release record, or verifies preparation-view evidence.

## State model

None. The rules are stateless per-artifact checks; removing them removes no
state.

## Behavioral rules

1. The candidate validator declares none of `se-harness-release-bootstrap-v1`,
   `se-harness-predecessor-bootstrap-v1` or
   `se-harness-predecessor-preparation-view-v1`, and contains no
   `_validated_release_bootstrap`, `_bootstrap_for_release_record` or
   `_validate_predecessor_view_evidence`.
2. No call site references them, including the evaluator-evidence binding's
   bootstrap-contract comparison, the at-most-one-approved-contract rule and
   the release-record branch.
3. The retained fields become inert data. No tolerance shim is required and
   none is added: measured on the current file, the validator enforces a closed
   field set only on nested tables it reads, so removing the reader removes the
   check. A `[bootstrap]` table or a `preparation_schema` marker on a release
   contract or release record is then an unread key, not an unknown-field
   error.
4. The retained-evidence guarantee moves from the validator to the repository's
   own suite. `tests/test_predecessor_bootstrap_retirement.py` already
   recomputes `RLS-SEH-012`'s two digests and `RLS-SEH-009`'s evaluator digest
   from the files themselves; that case is the guarantee after this change and
   is extended, not replaced.
5. `REQ-REB-011`'s rule is preserved exactly. Only the predecessor-schema
   condition that narrowed a rejected-history test to
   `se-harness-predecessor-bootstrap-v1` is removed; the general rule that a
   rejected record does not claim a version against at most one ready or
   released successor stays and keeps its own checks.
6. The root copy is not edited. A template-versus-root divergence is the
   expected state from this change until the root evaluator next advances, and
   every test that pins the two byte-equal declares the exact difference rather
   than being redirected away from the comparison.
7. The full artifact graph of this repository validates with zero errors under
   the candidate validator and under the evaluator installed outside the
   checkout, and the six closed artifacts are among the artifacts validated.

## Error and recovery behavior

No new error code is introduced and none is reused. `PV001` and `PV002` stay
reserved by `SPEC-REB-013`. If any of the six closed artifacts stops
validating, the change is wrong and is reverted rather than accommodated.

## Data and interface contracts

`se_harness/hash_bound_classes.json` keeps binding
`evaluator_evidence_sha256`, `preparation_view_evidence_sha256` and
`from_lock_sha256`. Those digests remain facts; what ends is their mechanical
re-derivation by the validator. `check_portable_release_surface.py` forbids
`predecessor-view` in CLI output only, through `FORBIDDEN_CLI`, so the
identifiers inside the packaged template have never been and are not subject to
that check.

## Compatibility and migration

The change reaches other repositories at the next release of this package and
cannot be withdrawn from the ones that adopt it. A consumer repository that
still carries a `[bootstrap]` table keeps it as unread data; nothing in it
becomes invalid, and nothing about it is re-derived. No migration step, policy
key or opt-out is offered: a gated rule would keep the code and the schema
names alive, which is what `ADR-REB-012` decided against.

## Examples and counterexamples

A release contract with a nine-key `[bootstrap]` table validates and no rule
reads the table. A release record with `preparation_schema` and
`preparation_view_evidence_sha256` validates and no rule recomputes the digest.
A counterexample is a rule kept behind a repository policy key, which
`ADR-REB-012` rejects. A second counterexample is deleting the retained fields
from the six closed artifacts, which `ADR-REB-012` rejects outright.

## Explicitly unspecified decisions

Whether the `superseded` status is later applied to `REQ-REB-008`,
`REQ-REB-010` or any definition retired by amendment. When the root copy
adopts this change. Whether `repository_tools/interpreter_safety.py` is
deleted, which is issue #220's question.
