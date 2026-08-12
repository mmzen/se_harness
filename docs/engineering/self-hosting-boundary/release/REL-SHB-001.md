+++
id = "REL-SHB-001"
type = "release_contract"
title = "Release the corrected self-hosting boundary"
status = "approved"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
gates = ["WO-IAR-002", "WO-IAR-003", "WO-IAR-004", "WO-IAR-005", "WO-RLS-004", "WO-SHB-001"]
+++

# Release Contract: Release the corrected self-hosting boundary

## Release unit

The recovered `se-harness` 0.2.2 wheel and normalized source distribution derived from one exact candidate commit. The candidate contains the five work orders already qualified by `REL-SEH-003` plus the isolated released-governor, candidate-source, and candidate-package model implemented by `WO-SHB-001`.

Version 0.2.2 is deliberately reused because the failed attempt remained on closed, unmerged PR #28 and produced no `v0.2.2` tag, GitHub Release, PyPI file, deployment, or merge to `main`. The recovery does not reuse the failed verification or release record IDs.

## Entry criteria

- `WO-SHB-001` is approved, implemented, and supported by complete `VER-SHB-001` evidence.
- All six gated work orders are `implemented` with distinct retained evidence.
- A clean replacement candidate commit exists on the valid lineage through `9ba0cec3710167ad4568931747ed5f4e48a63532` and excludes the failed governance commits from PR #28.
- All three CI lanes pass with exact runtime identity and permitted-target evidence.
- Governor bootstrap uses a hash-pinned independently published wheel and cannot import the candidate checkout.
- Candidate source and exact candidate package checks pass on Python 3.11 and the local supported runtime.
- Host/governor and candidate/sandbox parity invariants both pass with no ambiguous ownership.
- Closed PR #28 and its branch preserve the failed `VREC-SEH-003` and `RLS-SEH-003` attempt as audit history, while both files are absent from the recovery tree.
- `VREC-SEH-004` binds the exact replacement candidate to all six gated work orders and their applicable verification contracts.
- Any later release approval is recorded as `RLS-SEH-004`; neither failed ID is reused.

## Required evidence

Retain governor version, URL, wheel name and SHA-256; executable, module and template origins for every role; import-adversary results; checkout mutation snapshots; three-lane workflow structure and CI URLs; candidate tests; exact artifact hashes; normalized archive results; fresh-install and upgrade acceptance; migration results; failed-attempt audit location and recovery-tree exclusion; and the accountable version/release decision.

## Compatibility and migration

The public product retains one standard installation and Python 3.11+ standard-library runtime behavior. The host/candidate split applies only when developing the harness implementation. Ordinary consumer targets keep distribution-to-target parity.

The first migration from the mixed model must be transactional, preserve owner-controlled content, expose any host customization, retain prior governor identity and rollback data, and establish the future post-publication governor-promotion cycle.

## Security and provenance

Every installed artifact is verified before execution. Checkout, path, environment, workflow, archive, and lock inputs are untrusted. Identity output is allowlisted and credential-free. The VREC, RLS, eligible artifacts, and any later tag or publication must identify or derive from one exact replacement candidate.

## Promotion policy

Preparation commands may create only reviewable records. Accountable quality and release owners separately approve verification and release. Tagging, GitHub release creation, PyPI promotion, deployment, and governor adoption are separate actions. A failure or candidate change stops promotion and requires new commit-bound records.

`RLS-SEH-003` cannot authorize the corrected payload. No tag or publication may use its candidate identity after `WO-SHB-001` changes source, managed distribution content, or CI behavior. The only eligible record sequence is a new `VREC-SEH-004`, followed after accountable assurance review by a new `RLS-SEH-004`.

## Stop conditions

Stop on ambiguous runtime origin, cross-role import, mutable or unverified governor source, checkout mutation by isolated lanes, required-lane skip, host/candidate ownership confusion, failed migration, reintroduction or reuse of the failed PR records, artifact mismatch, missing replacement VREC, or authority beyond the approved release work.

## Rollback

Before external publication, preserve the failed attempt through its closed PR and branch, correct through a new candidate, and rerun every gate. After publication, never move a tag or replace a package file; issue a separately governed corrective version. Governor promotion retains the prior released governor and lock as rollback provenance and never downgrades through an unverified local build.

## Authority boundary

The repository owner approved the recommended clean-recovery option and selected reuse of version 0.2.2 on 2026-08-12. That decision authorizes recovery-tree preparation, complete local qualification, the replacement candidate commit, push, pull request, and later preparation of `VREC-SEH-004` as `ready` after hosted CI passes. It does not authorize `ready -> verified`, preparation or approval of `RLS-SEH-004`, merge, tag, GitHub Release, PyPI publication, deployment, or governor promotion.
