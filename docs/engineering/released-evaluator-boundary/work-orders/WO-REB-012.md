+++
id = "WO-REB-012"
type = "work_order"
title = "Pin the released distribution build backend"
status = "in_progress"
owners = ["engineering-owner", "quality-owner", "release-owner"]
created = "2026-08-22"
updated = "2026-08-22"

[assurance]
commit_bound_verification = "required"
rationale = "Publication must rebuild the already released C6 distribution bytes with the exact retained backend toolchain before any privileged reconciliation job can run."
decided_by = "engineering-owner"

[relations]
implements = ["REQ-REB-015"]
specifications = ["SPEC-REB-007"]
architecture = ["ARCH-REB-006", "ADR-REB-006"]
verification = ["VER-REB-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-22T20:29:30Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-22T20:29:31Z"
decided_by = "engineering-owner"
+++

# Work Order: Pin the released distribution build backend

## Lifecycle

This bounded corrective work is in progress under the repository owner's explicit authority to finalize release 0.6.0. Commit-bound assurance remains required before publication resumes.

## Objective

Make the credential-free publication rebuild reproduce the immutable C6 distribution bytes by installing the exact retained `build`, `setuptools`, and `wheel` versions before the existing no-isolation build.

## In scope

- Retain failed publication run `32596492345`, job `97088259463`, and the pre-privilege distribution-manifest mismatch.
- Pin `build==1.3.0`, `setuptools==84.0.0`, and `wheel==0.48.0` in the existing qualification environment.
- Add a static regression assertion that the full three-version toolchain is present and the frontend-only installation is absent.
- Prove locally that exact C6 rebuilds retain the wheel and normalized-sdist hashes bound by released `RLS-SEH-012`.

## Out of scope

- Changing C6, `v0.6.0`, `RLS-SEH-012`, any distribution hash or byte, rejected history, the root evaluator, release semantics, privilege boundaries, or external policy.
- Rebuilding from current `main`, retagging, or accepting newly produced distribution identities.

## Required verification

- Rebuild exact C6 with the retained Python 3.11.9 toolchain and compare both artifact hashes to `RLS-SEH-012`.
- Run focused workflow policy tests, the complete release-orchestration module, the complete suite, graph validation, release-distribution validation, and portable-surface checks.
- Prove the resolver, candidate identity, two-build comparison, bundle validation, and privilege dependencies remain unchanged.
- Prepare and verify a later commit-bound VREC before publication retry.

## Evidence

Retain results in `../evidence/WO-REB-012-build-toolchain.md`.
