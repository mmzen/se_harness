+++
id = "WO-RLS-002"
type = "work_order"
title = "Verify instruction architecture and qualify se-harness 0.2.1"
status = "implemented"
owners = ["release-owner", "quality-owner", "engineering-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
implements = ["REQ-DST-006"]
specifications = ["SPEC-DST-001"]
architecture = ["ARCH-DST-001", "ADR-DST-001"]
verification = ["VER-AGR-001", "VER-DST-001"]
+++

# Work Order: Verify instruction architecture and qualify se-harness 0.2.1

## Authorization

After merging pull request #17, the accountable repository owner instructed `i merged, then transition and governance commit + PR` and selected that work for release `0.2.1`, explicitly including deployment to PyPI. This authorizes the bounded assurance decision, candidate preparation, qualification, commits, normal branch push, and release-candidate pull request. It does not waive the later aggregate verification and release-record gates.

## Objective

Record the assurance decision for `VREC-IAR-001` and produce one clean, fully qualified 0.2.1 candidate whose exact incremental payload can later be verified, released to GitHub, and promoted unchanged to PyPI.

## In scope

- Confirm pull request #17 merged candidate `9b42d3b564eb107b161458c6d750d05680284618` and ready-record commit `39a7e2582ede1e2526fce33fb845ec3dce1ac53a` into `main` at `87b538bef1f7494f0c13860b567572c4271d530c`.
- Review retained `WO-IAR-001` evidence and transition only `VREC-IAR-001` from `ready` to `verified` without changing captured provenance.
- Select exactly `WO-PYP-001`, `WO-WLC-001`, `WO-IAR-001`, and this work order as the incremental 0.2.1 release payload under `REL-SEH-002`.
- Set source and installed-harness version metadata to `0.2.1`, update the self-hosted lock through the supported transactional upgrade, and preserve the immutable 0.2.0 independent-CI bootstrap pin.
- Run the complete graph, tests, CLI, doctor, review preflight, Explorer, package reproducibility, archive inspection, and clean Python 3.11 install matrix.
- Retain release-candidate qualification evidence and preliminary reproducibility hashes; retain final candidate-derived publication hashes only in the later release evidence.
- Commit the clean candidate, then capture a later aggregate `VREC-SEH-002` as `ready` against that exact commit with evidence for all four work orders.
- Push `release/0.2.1` normally and open one pull request against `main` declaring `Harness-Work-Order: WO-RLS-002`.

## Exact payload

`WO-IAR-001`, `WO-PYP-001`, `WO-RLS-002`, and `WO-WLC-001`.

The applicable verification contracts are `VER-AGR-001`, `VER-DST-001`, `VER-IAR-001`, `VER-PYP-001`, and `VER-WLC-001`.

## Required verification

- Formal graph and both preflight phases: zero diagnostics.
- Complete suite on Python 3.11 and the local supported runtime, with only documented platform-conditional skips.
- CLI version/help, self-hosted doctor, source/canonical parity, deterministic Explorer, workflow parsing, and diff hygiene.
- Two independent raw wheel and sdist builds at an explicit qualification epoch, followed by a later final rebuild from the committed candidate at that commit's epoch.
- Byte-identical wheels and normalized sdists, identical payload manifests, safe archive members, correct metadata, and exact source inclusion.
- Offline wheel reconstruction from the normalized sdist and exact wheel equality.
- Clean Python 3.11 wheel install; version, repository initialization, doctor, formal validation, and Explorer smoke tests.
- Immutable lineage and captured-field preservation for `VREC-IAR-001`.

## Lifecycle and promotion

This work order becomes `implemented` when the candidate and evidence are complete. `VREC-SEH-002` is captured later as `ready`. After merge, accountable quality approval is still required to transition that aggregate VREC. A release record can then be prepared against the same candidate; accountable release approval is required before tag, GitHub release, and exact-asset PyPI dispatch.

## Out of scope

Changing historical `RLS-SEH-001`, `VREC-SEH-001`, tag `v0.2.0`, or published assets; moving a tag; replacing a package file; bypassing protected environments; storing a PyPI token; publishing a rebuild; force push; history rewriting; merging the PR; or claiming final 0.2.1 publication before the later verified/released records and external evidence exist.

## Completion evidence

Retain the transition review, qualification commands, results, exact hashes, deviations, residual risks, and authority boundary in `docs/engineering/release-0.2.1/evidence/WO-RLS-002-verification.md`. The final commit, ready VREC, remote branch, PR, CI, release, and publication URLs remain externally discoverable or are retained by their later authorized phases.
