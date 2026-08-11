+++
id = "WO-WLC-002"
type = "work_order"
title = "Commit and publish lifecycle consistency for review"
status = "implemented"
owners = ["repository-owner", "engineering-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
implements = ["REQ-WLC-001", "REQ-WLC-002", "REQ-WLC-003", "REQ-WLC-004", "REQ-WLC-005", "REQ-WLC-006"]
specifications = ["SPEC-WLC-001"]
architecture = ["ARCH-WLC-001", "ADR-WLC-001"]
verification = ["VER-WLC-001"]
+++

# Work Order: Commit and publish lifecycle consistency for review

## Objective

Retain the completed `WO-WLC-001` implementation and evidence in one clean candidate commit, capture a ready commit-bound VREC for that exact candidate, retain the VREC in one later governance commit, push the review branch normally, and open a pull request against `main`.

## Authorization

The accountable repository owner explicitly authorized this sequence on 2026-08-11 with the instruction `commit, capture, commit and push + PR`.

## In scope

- Confirm `feature/work-order-lifecycle` is based on current `origin/main` and contains only the bounded lifecycle packet, implementation, normalization, tests, templates, lock update, and evidence.
- Rerun the required graph, focused/full tests, CLI, doctor, dashboard, parity, provenance-preservation, and diff-hygiene checks.
- Commit the complete `WO-WLC-001` candidate and this governance-only publication authorization.
- From the resulting clean candidate, capture `VREC-WLC-001` for only `WO-WLC-001`, `VER-WLC-001`, and its keyed evidence.
- Retain the ready VREC in one later governance commit.
- Push `feature/work-order-lifecycle` normally with upstream tracking and open a pull request targeting `main`.

## Out of scope

Transitioning `VREC-WLC-001` to `verified`; changing any existing VREC or RLS; preparing or transitioning a release record; merging the pull request; force push or history rewriting; tag creation or movement; GitHub release mutation; workflow dispatch or approval; package upload; publication; and deployment.

## Lifecycle

This is governance-only work and terminates at `implemented`; it is not selected into `VREC-WLC-001`. The commit IDs, ready record, remote branch, PR, and checks are derived results discoverable after execution and do not require recursively verifying this publication work order.

## Required verification

The candidate must be clean and based on current `origin/main`; all `WO-WLC-001` gates must pass; the capture must bind the exact candidate commit with clean worktree state, correct snapshot, evidence, work order, and verification contract; the second commit must not change the candidate identity; and the normal push and PR must target the intended branch and `main`.

## Completion evidence

Retain the preflight, authority boundary, candidate scope, required checks, and derived-result rule in `docs/engineering/work-order-lifecycle/evidence/WO-WLC-002-verification.md`. Resulting commit IDs, remote state, PR URL, and CI remain externally discoverable rather than being predicted inside their own commit.
