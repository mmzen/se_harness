+++
id = "ADR-REB-003"
type = "adr"
title = "Enforce evaluator-evidence LF bytes through versioned Git attributes"
status = "approved"
owners = ["technical-owner", "security-owner", "release-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[relations]
decides = ["ARCH-REB-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-21T17:46:21Z"
decided_by = "technical-owner"
+++

# ADR: Enforce evaluator-evidence LF bytes through versioned Git attributes

## Status

Accepted for bounded local implementation under `WO-REB-005`. Every candidate, hosted, release, publication, maintenance, and root-evaluator action remains separately governed.

## Context

`RLS-SEH-009` was correctly bound to canonical LF evaluator evidence and passed before commit. After the exact two-file preparation commit, a fresh default Windows checkout changed the JSON to CRLF. Candidate validation failed its raw SHA-256 binding, while an otherwise identical `core.autocrlf=false` checkout passed. C2 therefore does not provide portable release-readiness evidence. Attempting the authorized RLS/contract rejection then exposed that the validator requires even a rejected predecessor-bootstrap RLS to retain an approved contract, which prevents a corrected contract from becoming the sole approved bootstrap authority.

## Decision drivers

- Preserve exact-byte evidence rather than reinterpret it.
- Make portability policy repository-owned and reviewable.
- Override platform defaults narrowly without broad line-ending churn.
- Deliver the rule to future standard installations.
- Preserve the released-0.5 root and predecessor trust direction.
- Preserve rejected bootstrap evidence without retaining or reusing its authority.

## Considered options

1. **Require `core.autocrlf=false`.** Rejected because unversioned local configuration cannot be release authority and is not portable.
2. **Normalize CRLF before validator hashing.** Rejected for this correction because it changes the existing raw-byte contract and would accept noncanonical worktree bytes.
3. **Mark evidence JSON binary.** Rejected because JSON is governed text and binary treatment obscures intended canonical LF semantics.
4. **Add a narrow versioned `text eol=lf` rule.** Selected because Git then preserves canonical worktree bytes while validators remain strict.
5. **Abandon 0.6.0.** Retained as a release-owner fallback if the successor candidate cannot pass complete qualification.

## Decision

Add exactly `docs/engineering/**/evidence/*.json text eol=lf` to candidate-root and canonical standard-template Git attributes. Preserve raw evidence hashing and canonical JSON checks. Prove behavior through fresh isolated checkouts across supported configurations.

Also permit one predecessor-bootstrap RLS in `rejected` state to validate only against its exact `rejected` contract and immutable tuple. Exclude rejected contracts from active cardinality and reject them in binder, preparation, release, and publication paths. Ready records continue requiring one exact approved contract.

Because the policy changes trusted candidate and packaged-template state after C2 verification, produce successor candidate C3. `VREC-SEH-009` remains a true historical verification decision for C2 but cannot qualify C3. `RLS-SEH-009` remains stopped until the release owner explicitly rejects it. `REL-SEH-008` must be rejected before a replacement bootstrap contract is approved.

## Consequences

### Positive

- Exact evidence digests survive Windows and non-Windows checkout.
- Validator semantics remain strict and simple.
- Policy is reviewable, testable, and delivered to consumers.
- No local configuration or root-evaluator upgrade is required.
- Failed one-shot bootstrap chains become valid terminal history without blocking a successor.

### Negative and migration cost

- C2 becomes ineligible for release despite unchanged executable behavior.
- Candidate, archive, build, bundle, aggregate VREC, RLS, and hosted identities must be regenerated.
- Candidate/template parity and installation locks may require bounded updates.
- Validator lifecycle logic gains one closed historical state and its negative matrix.

### Operational and security consequences

- Conflicting more-specific attributes must fail qualification.
- Historical stopped records remain retained and cannot be repointed.
- Every lifecycle, commit, branch, credential, and external action remains separately authorized.

## Validation

Execute `VER-REB-003`. Require exact attribute resolution and evidence hashes under isolated checkout matrices, tamper failures, candidate/template/package parity, released and candidate validation, full regression, reproducible builds, hosted lanes, and a new commit-bound aggregate.
