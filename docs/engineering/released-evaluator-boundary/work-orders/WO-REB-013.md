+++
id = "WO-REB-013"
type = "work_order"
title = "Rebuild released bytes on their retained platform"
status = "implemented"
owners = ["engineering-owner", "quality-owner", "release-owner"]
created = "2026-08-22"
updated = "2026-08-22"

[assurance]
commit_bound_verification = "required"
rationale = "The immutable release bytes must be reconstructed in the exact retained Windows/Python producer class before any privileged publication reconciliation."
decided_by = "engineering-owner"

[relations]
implements = ["REQ-REB-015"]
specifications = ["SPEC-REB-007"]
architecture = ["ARCH-REB-006", "ADR-REB-006"]
verification = ["VER-REB-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-22T20:52:27Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-22T20:52:28Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-22T20:57:14Z"
decided_by = "engineering-owner"
+++

# Work Order: Rebuild released bytes on their retained platform

## Lifecycle

This bounded corrective work is implemented with exact qualification retained in `../evidence/WO-REB-013-retained-build-platform.md`. Commit-bound assurance remains required before another publication retry.

## Objective

Run only the credential-free exact-candidate qualification/build job on the retained Windows Python 3.11.9 producer class so its no-isolation build can reproduce the immutable C6 distribution bytes.

## In scope

- Retain publication run `32597819730`, job `97091491671`, and its Ubuntu Python 3.11.16 pre-privilege byte mismatch.
- Move only the `qualify` job from `ubuntu-latest` to `windows-2022`.
- Pin only that job to exact Python `3.11.9`; retain the exact `build`, setuptools, and wheel pins from WO-REB-012.
- Add static regression assertions for the retained runner and runtime.

## Out of scope

- Changing C6, `v0.6.0`, `RLS-SEH-012`, distribution bytes or hashes, build commands, resolver behavior, rejected history, root evaluator, privileged-job runners, credentials, or external policy.
- Treating a newly produced byte identity as releasable.

## Required verification

- Retain the exact local Windows Python 3.11.9 reconstruction of both RLS-bound hashes.
- Run focused workflow policy, complete release-orchestration, complete isolated suite, current/predecessor graph, distribution, portable-surface, whitespace, and clean-checkout checks.
- Prove only the credential-free qualification runner/runtime changed.
- Prepare and verify a later commit-bound VREC before retry.

## Evidence

Retain results in `../evidence/WO-REB-013-retained-build-platform.md`.
