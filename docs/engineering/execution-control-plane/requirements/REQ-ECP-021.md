+++
id = "REQ-ECP-021"
type = "requirement"
title = "The formal snapshot is independent of the checkout's line endings"
status = "draft"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-29"
updated = "2026-08-29"
statement = "WHEN the evaluator computes a formal snapshot digest over the artifact graph, THE SYSTEM SHALL compute it over each artifact's line-ending-canonical bytes, so that the same committed tree yields the same digest on every checkout."
verification_method = ["test"]
priority = "must"
source = "issue #256; pull request #253 at 61840f3, 2026-08-29"

[relations]
derives_from = ["CAP-ECP-001"]
+++

# Requirement: The formal snapshot is independent of the checkout's line endings

## Rationale

`formal_snapshot_digest` hashes each formal artifact's raw bytes
(`se_harness/workflow_compliance.py`, `read_bytes()`). The evidence packet
header binds that digest and `QGP-G4I-EVIDENCE` compares it with the value
recomputed at check time; a verification record's `artifact_snapshot_sha256`
is the same digest. A Windows checkout under `core.autocrlf=true` therefore
computes a different snapshot from the LF checkout the managed workflow
makes: on `se_harness` at `61840f3`, 1096 artifacts, `a1bd35eb…` on the
CRLF worktree against `eb25d023…` on a fresh clone of the same commit, all
1096 differing and every difference a line ending. The managed lane blocked
pull request #253 on `QGP-G4I-EVIDENCE` until the packet was rebound from an
LF clone. The lock already canonicalizes managed files with
`utf8-text-lf-v1`; the snapshot should not disagree with it.

## Behavior

- Trigger: `harnessctl evidence`, `check`, `transition`, or
  `capture-verification` computes a formal snapshot digest.
- Response: each artifact's bytes are canonicalized as `utf8-text-lf-v1`
  before hashing, so a CRLF checkout and an LF checkout of the same commit
  yield the same digest; on an LF checkout the digest is unchanged from the
  raw rule.
- On failure: an artifact that is not valid UTF-8 text is hashed as its raw
  bytes, exactly as the lock treats such content; nothing is refused that was
  accepted before.

## Assumptions and dependencies

- Every packet header and verification record on `main` was bound from an
  LF tree, so no stored digest moves under the canonical rule.
- The chain-scoped digest of `REQ-ECP-016` (`ECP-SNP-001`), when
  implemented, is computed by the same function and inherits the rule.

## Acceptance examples

### Example: normal behavior

**Given** one committed tree checked out twice, once with LF and once with
CRLF line endings in every artifact.

**When** the formal snapshot is computed on each.

**Then** the two digests are equal, and equal to the raw-byte digest of the
LF checkout.

### Example: failure behavior

**Given** the same tree with one artifact's content changed by one
character.

**When** the snapshot is computed.

**Then** the digest differs from the unchanged tree's.

## Open decisions

None.
