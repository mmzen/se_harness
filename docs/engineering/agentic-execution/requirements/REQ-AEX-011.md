+++
id = "REQ-AEX-011"
type = "requirement"
title = "Apply admitted single-agent repository changes transactionally"
status = "approved"
owners = ["product-owner", "requirements-steward", "technical-owner", "security-owner", "quality-owner"]
created = "2026-08-25"
updated = "2026-08-25"
statement = "WHEN a governed single-agent execution submits a deterministic change bundle admitted by a current evaluator-derived autonomy envelope, THE SYSTEM SHALL validate and apply the complete bundle through an evaluator-owned transactional effect broker and either produce a state-bound receipt for the exact result, restore the proven prior repository state, or enter an explicit recovery-required stop that permits no further governed advancement."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-AEX-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T09:08:48Z"
decided_by = "requirements-steward"
+++

# Requirement: Apply admitted single-agent repository changes transactionally

## Rationale

A cooperative skill can ask an agent to stay within scope, but it cannot prove
which bytes were written or prevent a direct tool from bypassing the request.
Phase 4 therefore needs one evaluator-owned repository effect boundary. The
worker proposes content; the evaluator validates authority and performs the
effect.

The change bundle is a deterministic transport manifest for proposed byte
deltas. It references the work order and envelope but does not copy their
authority-bearing scope, status, ownership, gates, or decision semantics.

## Preconditions and trigger

- `REQ-AEX-010` has produced a current, unused envelope for the exact effect.
- The worker has materialized proposed regular-file changes in an isolated
  staging area outside the target repository effect path.
- A canonical change bundle identifies every intended create, replace, or
  delete operation, its expected prior state, and its proposed resulting state.
- Required pre-effect gates and path-scope checks pass.

## Required response

- Parse a versioned, canonical change-bundle document and reject unknown,
  duplicate, non-canonical, escaping, case-colliding, or unsupported entries.
- Resolve every target path against the selected work order, current envelope,
  managed-file policy, repository root, and filesystem identity.
- Verify each expected prior absence or content digest against the freshly
  observed target state and each staged source digest against the bundle.
- Admit only regular-file create, replace, and delete operations in the initial
  version; reject links, reparse points, submodules, special files, mode
  changes, `.git`, evaluator-owned policy surfaces, and undeclared paths.
- Preflight the complete bundle before changing the first target byte.
- Apply the admitted set with complete preflight, per-path atomic replacement,
  durable journaling, and deterministic rollback on ordinary write, validation,
  race, or receipt failure.
- Re-observe and verify the resulting repository, then issue an immutable
  receipt binding bundle digest, envelope nonce, exact operations, `state_before`,
  `state_after`, evaluator identity, timestamps, and normalized result.
- Consume the envelope nonce exactly once whether the attempted effect succeeds
  or fails after admission.

## Failure and boundary behavior

- A malformed bundle, changed target, missing staged content, digest mismatch,
  case ambiguity, path escape, managed-policy conflict, unsupported object,
  stale envelope, or concurrent write fails before target change. An ordinary
  apply failure must restore and prove the prior state.
- Process or machine interruption may expose an intermediate multi-file state;
  the durable journal marks it recovery-required and blocks all continuation
  until the evaluator proves complete rollback or complete intended result.
- Rollback failure is a critical stop: preserve recovery material, report every
  uncertain path, prohibit further delegated effects, and require accountable
  human recovery.
- The broker does not approve work, select a design, infer additional paths,
  stage or commit Git changes, use credentials, access the network, or perform
  external actions.
- Bundle possession, bundle signing by a provider, or a matching work-order ID
  does not replace current evaluator admission.

## Constraints

- Change-bundle v1 contains references and byte-level deltas, not duplicated
  work-order prose or mutable lifecycle facts.
- All target and staging paths are normalized repository-relative portable
  paths; the broker performs handle-aware containment and link/reparse checks.
- Bundle ordering and digest are canonical and platform-independent.
- The broker writes only paths admitted by both the work order and the current
  envelope, and never edits installed released evaluator files from inside the
  governed repository.
- One broker transaction runs at a time for the target repository.
- Evidence excludes secrets and full content unless the work order explicitly
  requires and safely stores it; cryptographic digests are preferred.

## Acceptance examples

### Example: regular-file create and replace

**Given** a current envelope admits two paths and a bundle declares one create
and one replace with correct prior and staged digests

**When** the broker preflights and applies the bundle

**Then** both resulting bytes match the bundle, neither path is partially
applied, and the receipt's `state_after` matches a fresh observation.

### Example: stale expected prior digest

**Given** a bundle expects one prior digest

**When** the target file changed before broker preflight

**Then** the complete bundle is rejected and every target path retains its
pre-attempt bytes.

### Example: forbidden object

**Given** a staged path is a symbolic link or Windows reparse point

**When** the worker submits it as a file create

**Then** the broker rejects the complete bundle before any target write.

## Open decisions

Before approval, specifications and ADRs must close the bundle schema and
canonicalization, digest algorithm, staging layout, transaction and rollback
algorithm, directory creation policy, lock strategy, race detection, managed-
surface denylist, receipt schema, recovery evidence, size limits, and
cross-platform semantics.
