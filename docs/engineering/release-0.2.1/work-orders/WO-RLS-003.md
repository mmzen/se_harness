+++
id = "WO-RLS-003"
type = "work_order"
title = "Approve and publish se-harness 0.2.1"
status = "implemented"
owners = ["repository-owner", "quality-owner", "release-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
implements = ["REQ-DST-006"]
specifications = ["SPEC-DST-001"]
architecture = ["ARCH-DST-001", "ADR-DST-001"]
verification = ["VER-AGR-001", "VER-DST-001", "VER-PYP-001"]
+++

# Work Order: Approve and publish se-harness 0.2.1

## Authorization

After merging pull request #18, the accountable repository, quality, and release owner instructed `i merged, you can perform the next steps` on 2026-08-11. The referenced next steps were explicitly enumerated as aggregate verification transition, release-record preparation and approval, immutable `v0.2.1` GitHub release publication, exact-hash protected PyPI dispatch, publication verification, and final evidence retention. This is the human assurance, release, and publication authorization for the bounded identities below.

## Objective

Promote the already qualified candidate `94e13e31b81333e1f80f5a7dfd86ed5dbfc1e3e5` through accountable aggregate verification, release governance, immutable GitHub assets, and unchanged PyPI publication while retaining complete before-and-after evidence.

## Exact authorized identities

- Candidate commit: `94e13e31b81333e1f80f5a7dfd86ed5dbfc1e3e5`.
- Aggregate verification: `VREC-SEH-002`.
- Release contract and record: `REL-SEH-002`, `RLS-SEH-002`.
- Version and tag: `0.2.1`, `v0.2.1`.
- Released work: `WO-IAR-001`, `WO-PYP-001`, `WO-RLS-002`, `WO-WLC-001`.
- GitHub repository: `mmzen/se_harness`.
- PyPI project: `se-harness` through workflow `.github/workflows/publish-pypi.yml`, environment `pypi`, and Trusted Publishing.
- Wheel SHA-256: `533f6f87f5a1060d5d0070702969f643525ca3b91e2ecdbbd029f1530d093454`.
- Normalized sdist SHA-256: `770d40cfe9f65970424acb72f9e235365be61e2e8c73dce58274a0f0eca198e4`.

## In scope

- Confirm pull request #18 merged the candidate and ready aggregate record into `main` at `c3e0e417cfa422f3cab732d863e16a552675629e`.
- Review all four evidence paths and immutable captured fields in `VREC-SEH-002`; transition it only from `ready` to `verified`.
- Export the exact candidate twice, build with the candidate commit epoch, normalize both source distributions, inspect all content and metadata, and retain final hashes.
- Prepare `RLS-SEH-002` as `ready` against verified `VREC-SEH-002`, then record the release-owner decision by transitioning it to `released` without changing its candidate identity or scope.
- Retain separate commits for the verified VREC, ready RLS, and released RLS decision.
- Push a normal governance branch, open a pull request declaring this work order, require green independent-baseline and candidate CI, and merge it normally without rewriting history.
- Confirm tag and release absence, create annotated tag `v0.2.1` on the candidate commit, push it once, and publish exactly the retained wheel, normalized sdist, and `SHA256SUMS` as a non-draft, non-prerelease GitHub release.
- Verify the remote tag target, release state, asset names, sizes, and downloaded hashes.
- Dispatch the protected PyPI workflow from `main` with the exact tag and two hashes; do not bypass environment protection.
- Verify the completed workflow, PyPI version/files/hashes/attestations, and a clean exact-version Python 3.11 installation; then retain final publication evidence and mark this governance work order `implemented` in a final review commit.

## Required verification

Formal validation and both preflight phases must pass with zero diagnostics. Complete tests must pass on Python 3.11 and the local runtime with only known conditional symlink skips. Doctor, CLI, Explorer, diff hygiene, candidate/record ancestry, captured-field preservation, archive safety, wheel RECORD, exact source payloads, reproducibility, offline installation, GitHub release verification, PyPI workflow outcome, and exact-version installation must pass.

## Stop conditions

Stop without publication on any changed candidate or payload, non-verified aggregate VREC, release-record inconsistency, existing or mismatched tag/release/version, artifact hash difference, draft/prerelease state, missing asset, publisher/environment mismatch, failed protection approval, upload anomaly, or post-publication hash/install disagreement.

## Out of scope

Changing candidate source, rebuilding after GitHub publication, replacing an asset or PyPI file, moving a tag, altering historical 0.2.0 records, using a long-lived PyPI credential, bypassing environment protection, publishing another project/version, force pushing, deleting history, or treating governance-only work as release payload.

## Completion evidence

Retain the assurance and release decision in `docs/engineering/release-0.2.1/evidence/WO-RLS-003-verification.md`, final GitHub artifact evidence in `docs/engineering/release-0.2.1/evidence/RLS-SEH-002-release.md`, and post-publication results in `docs/engineering/release-0.2.1/evidence/PYPI-SEH-002-publication.md`.
