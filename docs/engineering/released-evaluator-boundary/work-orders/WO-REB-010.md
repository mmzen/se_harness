+++
id = "WO-REB-010"
type = "work_order"
title = "Provide exact Git context to release-candidate tests"
status = "implemented"
owners = ["engineering-owner", "quality-owner", "release-owner"]
created = "2026-08-22"
updated = "2026-08-22"

[assurance]
commit_bound_verification = "required"
rationale = "The trusted publication workflow must execute the complete immutable-candidate test suite with the Git provenance those tests verify before privileged jobs."
decided_by = "engineering-owner"

[relations]
implements = ["REQ-REB-015"]
specifications = ["SPEC-REB-007"]
architecture = ["ARCH-REB-006", "ADR-REB-006"]
verification = ["VER-REB-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-22T20:06:00Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-22T20:06:01Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-22T20:10:59Z"
decided_by = "engineering-owner"
+++

# Work Order: Provide exact Git context to release-candidate tests

## Lifecycle

This bounded corrective work is implemented with exact qualification retained in `../evidence/WO-REB-010-git-aware-candidate.md`. Commit-bound assurance remains required before another publication retry; implementation status does not itself grant assurance or publication authority.

## Objective

Run the complete C6 qualification suite in an exact detached Git worktree while preserving the two byte-deterministic archive exports as the only distribution build inputs.

## In scope

- Retain failed run `32595552589`, job `97085818853`, and its two missing-Git errors.
- Add one detached worktree at the already resolved exact candidate commit in the credential-free qualification job.
- Run candidate validation, tests, help, and doctor in that worktree.
- Continue building and comparing only the unchanged `git archive` exports.
- Add static workflow assertions and qualify the exact correction.

## Out of scope

- Changing C6, tag, RLS, distributions, rejected history, root state, adapter behavior, build inputs, privileged jobs, permissions, policy, or external release state.
- Copying main governance into C6, fabricating Git identity, weakening tests, or skipping failures.

## Required verification

- Reproduce both errors in a plain archive and prove both tests pass in exact detached C6 with Git history.
- Run focused workflow tests, complete suite, graph, release-distribution, and portable-surface checks.
- Prove archive build commands and privileged job dependencies/permissions are unchanged.
- Prepare and verify a later commit-bound VREC before retry.

## Evidence

Retain results in `../evidence/WO-REB-010-git-aware-candidate.md`.
