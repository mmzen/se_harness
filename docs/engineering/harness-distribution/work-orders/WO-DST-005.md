+++
id = "WO-DST-005"
type = "work_order"
title = "Approve canonical artifact-layout verification"
status = "implemented"
owners = ["repository-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
implements = ["REQ-DST-015", "REQ-DST-016", "REQ-DST-017", "REQ-DST-018"]
specifications = ["SPEC-DST-005"]
architecture = ["ARCH-DST-005", "ADR-DST-005"]
verification = ["VER-DST-005"]
+++

# Work Order: Approve canonical artifact-layout verification

## Objective

Record the accountable assurance decision for `VREC-DST-004`, retain the bounded transition in one governance commit, and publish that commit through a new review branch and pull request against `main`.

## Authorization

The accountable repository owner confirmed pull request #26 was merged, reviewed the retained canonical artifact-layout implementation evidence and ready verification record, and explicitly authorized the verification transition, governance commit, normal push, and pull request on 2026-08-11 with the instruction `i merged, then transition and governance commit + PR`.

## In scope

- Confirm pull request #26 merged the implementation candidate and ready record into `main` at merge commit `a960382630efaaaf4b14c3e2b5cb2fd18c1c51c8` with all candidate and independent-baseline checks passing.
- Confirm `VREC-DST-004` is a valid `ready` record for `WO-DST-004` under `VER-DST-005`.
- Confirm it names clean candidate commit `fd0a6af2bcbe95ddac2440d101640c4053a83e12` and was retained in ready-record governance commit `100ae73735cdcbe4ea8efb89520db6b36a3c3943`.
- Review `docs/engineering/harness-distribution/evidence/WO-DST-004-verification.md`, including its path-authority boundary, legacy compatibility, safe-write checks, and residual filesystem uncertainty.
- Transition only `VREC-DST-004` from `ready` to `verified` and add the explicit human-decision note while preserving every captured provenance field and relation.
- Create one governance commit containing only this work order, its evidence, and the bounded VREC transition.
- Push `governance/verify-vrec-dst-004` normally to `origin` and open a pull request targeting `main`.

## Out of scope

Changing the candidate commit, Git object format, worktree state, capture timestamp, artifact snapshot, implementation evidence path, work-order relation, or verification-contract relation; changing `WO-DST-004` or its implementation evidence; moving any historical artifact; changing runtime behavior, tests, templates, package metadata, version, lock, workflow, CI baseline pin, release contract, release record, tag, GitHub release, PyPI project or file, attestation, or external configuration; building a distribution; merging the governance pull request; force pushing; rewriting history; publication; and deployment.

This governance-only work order is audit history and is not automatically release payload or a recursive candidate for commit-bound verification.

## Required verification

The graph must validate with zero errors and only the seven expected nonblocking `W013` historical-layout advisories; the candidate and ready-record governance commits must be locally available ancestors; the implementation evidence and ready-record SHA-256 values must be retained before transition; all captured VREC fields and typed relations must remain unchanged; the focused artifact-authoring tests and complete unit suite must pass with only the known conditional skips; CLI help, doctor, review preflight, deterministic dashboard generation, and diff hygiene must pass; and the final governance commit must contain only the three bounded files.

## Completion evidence

Retain reviewed lineage, hashes, commands, results, transition boundaries, deviations, and residual risks in `docs/engineering/harness-distribution/evidence/WO-DST-005-verification.md`. The resulting remote branch, pull request URL, and CI results remain externally discoverable after the commit and are not predicted inside it.

## Completion boundary

This work order stops after the governance commit, normal push, and pull-request creation authorized by the owner. The VREC transition does not authorize a release build, RLS preparation or transition, tag, GitHub release, PyPI publication, deployment, or pull-request merge.

## Implementation result

The owner-authorized assurance transition is complete: `VREC-DST-004` is `verified`, every captured provenance field and relation remains unchanged, and the transition note names the merged pull request, accountable instruction, and this governance-only work order. Candidate and ready-record ancestry, retained hashes, focused and complete tests, formal validation, doctor, CLI help, deterministic Explorer generation, review preflight, and diff hygiene are retained in `docs/engineering/harness-distribution/evidence/WO-DST-005-verification.md`.
