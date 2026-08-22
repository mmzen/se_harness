+++
id = "WO-REB-017"
type = "work_order"
title = "Separate Pages plan output consumption and view setup"
status = "implemented"
owners = ["engineering-owner", "quality-owner", "release-owner"]
created = "2026-08-22"
updated = "2026-08-22"

[assurance]
commit_bound_verification = "required"
rationale = "Hosted Pages recovery must consume release-plan step outputs only after the producing step completes and must create the exact retained-view parent in the job that uses it."
decided_by = "engineering-owner"

[relations]
implements = ["REQ-REB-015"]
specifications = ["SPEC-REB-007"]
architecture = ["ARCH-REB-006", "ADR-REB-006"]
verification = ["VER-REB-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-22T22:03:46Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-22T22:03:47Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-22T22:08:17Z"
decided_by = "engineering-owner"
+++

# Work Order: Separate Pages plan output consumption and view setup

## Lifecycle

This bounded hosted-wiring correction is implemented with exact qualification retained in `../evidence/WO-REB-017-pages-step-output.md`. Commit-bound assurance remains required before retry.

## Objective

Consume `publish_release.py` governance output in a later workflow step and create the release-workflow retained-view parent in the Pages build job that owns it.

## In scope

- Retain failed standalone recovery run `32601295455`, job `97099823204`, and the exact empty same-step output comparison.
- Move the immutable governance-input assertion to its own immediately following unprivileged step.
- Move the release-workflow Pages view-parent creation from initial authority resolution to the Pages build evaluator step.
- Add explicit workflow-policy tests for both boundaries.

## Out of scope

No adapter, evaluator, release identity, RLS/VREC/REL, candidate, tag, distribution, GitHub Release, PyPI file, maintenance line, Pages environment policy, or root evaluator changes are permitted by this correction.

## Required verification

Run focused workflow policy, complete isolated suite, current graph, release-distribution, portable-surface, whitespace, and clean-checkout checks; prepare and verify a commit-bound VREC before trusted-main push and exact standalone recovery retry.

## Evidence

Retain results in `../evidence/WO-REB-017-pages-step-output.md`.
