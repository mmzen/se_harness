+++
id = "WO-WLC-003"
type = "work_order"
title = "Approve and publish lifecycle verification"
status = "implemented"
owners = ["repository-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
implements = ["REQ-WLC-001", "REQ-WLC-002", "REQ-WLC-003", "REQ-WLC-004", "REQ-WLC-005", "REQ-WLC-006"]
specifications = ["SPEC-WLC-001"]
architecture = ["ARCH-WLC-001", "ADR-WLC-001"]
verification = ["VER-WLC-001"]
+++

# Work Order: Approve and publish lifecycle verification

## Objective

Record the accountable assurance decision for `VREC-WLC-001`, retain the bounded status transition in one governance commit, and publish that commit through a normal review branch and pull request against `main`.

## Authorization

The accountable repository owner confirmed pull request #15 was merged, reviewed the retained evidence, and explicitly authorized the verification transition, governance commit, normal push, and pull request on 2026-08-11 with the instruction `i merged, then transition and governance commit + PR`.

## In scope

- Confirm pull request #15 merged the candidate and ready record into `main` at merge commit `0236f771d16a3cb4cdd28a95f92d264db002c81f`.
- Confirm `VREC-WLC-001` is a valid `ready` record for `WO-WLC-001` under `VER-WLC-001`.
- Confirm it names candidate `b907860afdb3e4eb387c00588f74e8d29c4ec136` and was retained in governance commit `2db0a1e26c7b92eb34fdc3ea23874da4f3d3a92f`.
- Review the retained evidence at `docs/engineering/work-order-lifecycle/evidence/WO-WLC-001-verification.md`.
- Transition only `VREC-WLC-001` from `ready` to `verified`, retaining the explicit human-decision note without changing captured provenance.
- Create one governance commit containing this work order, its evidence, and the bounded VREC transition.
- Push `governance/verify-vrec-wlc-001` normally and open a pull request targeting `main`.

## Lifecycle

This governance-only work order stops at `implemented`. It records and publishes the decision affecting `VREC-WLC-001`; the target VREC's `verified` status does not recursively verify this work order.

## Out of scope

Changing the candidate commit, object format, captured worktree state, capture timestamp, artifact snapshot, evidence path, or typed relations; changing another VREC or RLS; preparing or transitioning a release; creating or moving a tag; merging the pull request; force push or history rewriting; GitHub release mutation; PyPI workflow dispatch or approval; package upload; publication; and deployment.

## Required verification

The artifact graph, complete Python 3.11 and local-runtime suites, CLI help, doctor, Explorer, candidate and ready-record ancestry, captured-field preservation, and diff hygiene must pass. The final commit must contain exactly the VREC transition, this work order, and its evidence.

## Completion evidence

Retain the reviewed lineage, hashes, commands, outcomes, deviations, and authority boundary in `docs/engineering/work-order-lifecycle/evidence/WO-WLC-003-verification.md`. Commit, branch, PR, and CI results remain externally discoverable after publication rather than being predicted in their own commit.
