+++
id = "REQ-REB-012"
type = "requirement"
title = "Prepare a successor through an exact predecessor-compatible view"
status = "approved"
owners = ["requirements-steward", "repository-owner", "security-owner", "release-owner"]
created = "2026-08-22"
updated = "2026-08-22"
statement = "WHEN the locked predecessor evaluator cannot parse an exact closed rejected-bootstrap pair, THE SYSTEM SHALL let that evaluator prepare the successor record through a deterministic contract-bound view that omits only that pair and proves the complete repository unchanged before and after preparation."
verification_method = "automated-projection-provenance-and-zero-write-negative-test"

[relations]
derives_from = ["CAP-REB-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-21T22:17:21Z"
decided_by = "requirements-steward"
+++

# Requirement: Prepare a successor through an exact predecessor-compatible view

## Rationale

Released evaluator 0.5.0 must remain the runtime that creates the predecessor-format RLS, but its formal validator supports only `ready` and `released` release records. It therefore stops on the exact rejected `RLS-SEH-009` history before it can evaluate `REL-SEH-009` and `VREC-SEH-010`. Editing history or upgrading the root evaluator would reverse the approved trust direction.

A compatibility view can present only syntax understood by 0.5.0 while a candidate-owned adapter proves that the complete repository, omitted history, old lock, evaluator, contract, VREC, work set, and imported output remain exact.

## Preconditions and trigger

- The complete source is one clean committed governance snapshot that passes the candidate validator.
- The omitted artifacts form one exact `rejected RLS + rejected declaring contract` predecessor-bootstrap pair.
- Their paths, IDs, statuses, Git blob IDs, raw SHA-256 values, tuple, and evidence are valid before preparation.
- Exactly one approved successor bootstrap contract identifies the proposed RLS and version.
- The exact external 0.5.0 interpreter, entry point, public wheel, schema-2 lock, and candidate VREC identities agree with that contract.

## Required response

- Construct a temporary sparse preparation worktree at the exact governance commit.
- Omit only the two contract-declared rejected-history paths; do not alter the commit, index, source repository, or historical bytes.
- Emit canonical retained preparation-view evidence binding the source commit, sparse specification, omitted path/blob/raw hashes, evaluator identity, exact command arguments, successor IDs, candidate identity, and output digest.
- Invoke exact external 0.5.0 `prepare-release` in isolation and accept only its generated ready record.
- Import the record without changing predecessor-owned identity, relations, body, or timestamp fields.
- Revalidate the full repository, restore proof of both historical bytes, and apply the existing canonical evaluator binder atomically.
- Fail with no repository write on any ambiguity, drift, extra omission, contaminated runtime, command failure, output mismatch, or incomplete rollback.

## Failure and boundary behavior

The adapter refuses a dirty or unresolved source, missing Git object, non-closed or non-bootstrap history, more or fewer than two omitted artifacts, local/global sparse policy substitution, symbolic-link traversal, unexpected 0.5.0 output, changed full graph, or existing partial destination. Temporary files are removed or retained only as bounded diagnostic evidence; no credentials are consulted.

## Constraints

- The complete repository is never claimed to have been parsed by 0.5.0 after rejected history exists; the observation is explicitly a compatibility-view preparation.
- Candidate validation of the complete graph is mandatory before and after preparation.
- No root configuration, schema-2 lock, released installation, historical artifact, candidate commit, VREC, tag, maintenance ref, or external state may change.
- The adapter cannot approve, verify, release, tag, publish, deploy, or upgrade anything.

## Acceptance examples

### Example: normal behavior

**Given** exact rejected `REL-SEH-008` and `RLS-SEH-009`, approved successor contract, verified successor VREC, and external 0.5.0

**When** the authorized adapter prepares the successor

**Then** 0.5.0 creates the ready RLS in the exact sparse view, the full repository retains both historical files byte-for-byte, and candidate validation plus canonical binding pass.

### Example: failure behavior

**Given** a sparse view that omits any third path or an omitted file whose hash differs

**When** preparation is planned or applied

**Then** it fails before importing an RLS or creating repository evidence.

## Open decisions

No product decision remains open. Temporary-directory names and internal helper decomposition are delegated; the exact view, proof, isolation, and zero-write guarantees are not.
