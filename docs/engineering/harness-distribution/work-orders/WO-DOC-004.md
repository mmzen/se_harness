+++
id = "WO-DOC-004"
type = "work_order"
title = "Approve and publish PyPI onboarding verification"
status = "implemented"
owners = ["repository-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
implements = ["REQ-DST-013"]
specifications = ["SPEC-DST-003"]
architecture = ["ARCH-DST-003", "ADR-DST-003"]
verification = ["VER-DST-003"]
+++

# Work Order: Approve and publish PyPI onboarding verification

## Objective

Record the accountable assurance decision for `VREC-DOC-003`, retain the bounded transition in one governance commit, and publish that commit through a new review branch and pull request against `main`.

## Authorization

The accountable repository owner confirmed pull request #22 was merged, reviewed the retained implementation and ready verification record, and explicitly authorized the verification transition, governance commit, normal push, and pull request on 2026-08-11 with the instruction `i merged, then transition and governance commit + PR`.

## In scope

- Confirm pull request #22 merged the implementation candidate and ready record into `main` at merge commit `9b8a0e06094cadf2df3871a01ab95e4455c75bfd` with all required checks passing.
- Confirm `VREC-DOC-003` is a valid `ready` record for `WO-DOC-003` under `VER-DST-003`.
- Confirm it names clean candidate commit `37588cbffc4e44797ea4f165ec5730cc48c7294c` and was retained in ready-record governance commit `3750eb0e09b652ba6b619055730f398a5bcd7594`.
- Review `docs/engineering/harness-distribution/evidence/WO-DOC-003-verification.md` and its deferred release-verification boundary.
- Transition only `VREC-DOC-003` from `ready` to `verified` and add the explicit human-decision note while preserving every captured provenance field and relation.
- Create one governance commit containing only this work order, its evidence, and the bounded VREC transition.
- Push `governance/verify-vrec-doc-003` normally to `origin` and open a pull request targeting `main`.

## Out of scope

Changing the candidate commit, Git object format, worktree state, capture timestamp, artifact snapshot, implementation evidence path, work-order relation, or verification-contract relation; changing `WO-DOC-003` or its implementation evidence; building a distribution; changing a version, workflow, CI baseline pin, template, lock, release contract, release record, tag, GitHub release, PyPI project or file, attestation, or external configuration; merging the governance pull request; force pushing; rewriting history; publication; and deployment.

This governance-only work order is audit history and is not automatically release payload or a recursive candidate for commit-bound verification.

## Required verification

The graph must validate with zero diagnostics; the candidate and ready-record governance commits must be locally available ancestors; the implementation evidence and ready-record SHA-256 values must be retained before transition; all captured VREC fields and typed relations must remain unchanged; the focused onboarding tests and complete unit suite must pass on Python 3.11 and the local runtime with only the known conditional Windows symlink skips; CLI help, doctor, review preflight, deterministic dashboard generation, and diff hygiene must pass; and the final governance commit must contain only the three bounded files.

## Completion evidence

Retain reviewed lineage, hashes, commands, results, transition boundaries, deviations, and residual risks in `docs/engineering/harness-distribution/evidence/WO-DOC-004-verification.md`. The resulting remote branch, pull request URL, and CI results remain externally discoverable after the commit and are not predicted inside it.

## Completion boundary

This work order stops after the governance commit, normal push, and pull-request creation authorized by the owner. The VREC transition does not authorize a release build, RLS preparation or transition, tag, GitHub release, PyPI publication, deployment, or pull-request merge.
