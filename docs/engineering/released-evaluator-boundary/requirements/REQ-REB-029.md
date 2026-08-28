+++
id = "REQ-REB-029"
type = "requirement"
title = "One predecessor-successor handover mechanism, and no compatibility view"
status = "approved"
owners = ["requirements-steward", "repository-owner", "release-owner", "security-owner"]
created = "2026-08-27"
updated = "2026-08-27"
statement = "WHEN a release or publication step needs assurance that a predecessor evaluator and its successor agree, THE SYSTEM SHALL obtain it only from the no-network governance-migration rehearsal, with no contract-declared predecessor evaluator, no compatibility view of the repository, and no release path able to require either."
verification_method = "automated-retired-surface-absence-and-history-retention-test"
priority = "must"
source = "Sweep of 2026-08-27 following issue #190; supersedes REQ-REB-012 and REQ-REB-015"
measure = "zero code paths that read a contract [bootstrap] tuple or construct a predecessor view; the closed 0.6.0 pair still valid and hash-bound"

[relations]
derives_from = ["CAP-REB-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-27T16:43:16Z"
decided_by = "requirements-steward"
reason = "Approved on 2026-08-27 by the accountable owner, 'I approve the artifacts', on the read-only sweep of 2026-08-27 following issue #190: the predecessor-bootstrap release path has no remaining occasion, its three defects of 2026-08-27 all came from leftover assumptions about a single rejected release record, and the general mechanism it should have been already ships as governance_migration. Predecessor-successor assurance comes only from the governance-migration rehearsal. REQ-REB-012 and REQ-REB-015 are superseded under WO-REB-028. REQ-REB-010 and REQ-REB-011 keep their force and retire with the managed validator in a later work order."
+++

# Requirement: One predecessor-successor handover mechanism, and no compatibility view

## Amendment of 2026-08-28

Amended under `WO-ECP-010` (`REQ-ECP-012`) for issue #210. The one mechanism this requirement names as the source of assurance that a predecessor evaluator and its successor agree is no longer the no-network governance-migration rehearsal, which is retired with `REQ-REB-016`, `REQ-REB-017` and `SPEC-REB-008`, but the real upgrade rehearsal of `repository_tools/upgrade_rehearsal.py`: the successor's own `upgrade --apply` against a throwaway export holding the released predecessor's lock, judged by both evaluators' `doctor` and by the resulting lock. The rest of the requirement keeps its force: no contract-declared predecessor evaluator, no compatibility view of the repository, and no release path able to require either.


## Rationale

The predecessor-bootstrap path was authored for one event. Released 0.5.0
emits `E009` on `status = "rejected"`, so retaining the rejected
`REL-SEH-008` / `RLS-SEH-009` pair made the repository unparseable by its own
governor. `REQ-REB-012` and `REQ-REB-015` answered that by letting 0.5.0 read
a sparse view of the repository with the offending pair omitted, and by
binding the evaluator to a nine-key `[bootstrap]` tuple in the release
contract.

`REQ-REB-011` removed the cause in 0.6.0: a rejected record became valid but
inert history. 0.7.0 then proved that no later release needs the view —
`RLS-SEH-014` was rejected and `RLS-SEH-015` released, both under the 0.6.0
governor, with no view and no tuple. `REL-SEH-017` declared no `[bootstrap]`
block at all.

What remained was a mechanism with no remaining occasion, and it kept
failing. Issue #190 recorded three defects in it on 2026-08-27, all from the
same cause: code that assumed the whole repository still contained exactly
one rejected release record, or that a view still applied. The 0.6.0 recovery
had predicted this in writing — "the current compatibility code is strongly
tied to the exact rejected 0.6.0 pair. It solves this release but is not yet
a general version-migration framework."

The general framework exists. `governance_migration.py` is a no-network,
dual-runtime rehearsal of a predecessor-to-successor handover, it ships in
the package, and `check_portable_release_surface.py` already requires its
command in the installed surface. Keeping a second, single-purpose mechanism
beside it is a standing source of the failures #190 recorded.

## Preconditions and trigger

- A release or publication step would benefit from evidence that a
  predecessor and a successor evaluator agree on the same repository.
- The repository contains closed predecessor-bootstrap history: the rejected
  `REL-SEH-008` / `RLS-SEH-009` pair and the released `RLS-SEH-012` that its
  successor contract produced.
- No active release contract declares a `[bootstrap]` tuple, and none may.

## Required response

- Obtain predecessor-successor assurance only from the governance-migration
  rehearsal.
- Retain the closed 0.6.0 bootstrap artifacts unchanged, with their evidence
  digests still bound by the `evaluator-evidence` and `standard-lock`
  hash-bound classes.
- Provide no mechanism that reads a contract-declared predecessor evaluator,
  constructs a sparse or omitting view of the repository, or runs a
  predecessor evaluator inside one.
- Let every publication and Pages step read the complete governance snapshot
  unconditionally, with no branch on whether a view applies.
- Keep the retired diagnostic codes reserved and never reuse them for
  another meaning.

## Failure and boundary behavior

An artifact that declares a `[bootstrap]` tuple gains no authority from it.
A step that cannot obtain assurance without a compatibility view fails
closed rather than constructing one. Retiring the mechanism never changes a
byte, digest, lifecycle fact, or released-governor verdict of the closed
0.6.0 history.

## Constraints

- The closed pair stays present and stays validated by the unchanged root
  validator; `REQ-REB-010` and `REQ-REB-011` keep their force.
- No historical artifact, evidence file, lock, or tag changes.
- The `harness-dashboard-bootstrap-v2` Explorer payload is a different schema
  and is unaffected.
- Nothing in this requirement authorizes a write to a hash-locked managed
  path.

## Acceptance examples

### Example: normal behavior

**Given** a release record whose contract declares no `[bootstrap]` tuple

**When** the authorized last mile and the release-bound Pages build run

**Then** both read the complete governance snapshot, neither selects a
predecessor view, and no step refuses for a missing tuple.

### Example: retained history

**Given** the rejected `REL-SEH-008` and `RLS-SEH-009` and the released
`RLS-SEH-012`, after the mechanism is retired

**When** the exact public 0.6.0 evaluator validates the repository from
outside the checkout

**Then** the artifact count, error count and warning count are unchanged, and
`RLS-SEH-012`'s bound evidence digests still verify.

### Example: boundary

**Given** any repository state

**When** the installed evaluator's qualification operations are enumerated

**Then** no operation constructs a repository view, and the
governance-migration rehearsal is the only predecessor-successor mechanism
present.
