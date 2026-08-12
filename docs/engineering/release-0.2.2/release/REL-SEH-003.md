+++
id = "REL-SEH-003"
type = "release_contract"
title = "Qualify and release se-harness 0.2.2"
status = "approved"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
gates = ["WO-IAR-002", "WO-IAR-003", "WO-IAR-004", "WO-IAR-005", "WO-RLS-004"]
+++

# Release Contract: Qualify and release se-harness 0.2.2

## Release unit

The incremental `se-harness` 0.2.2 wheel and normalized source distribution derived from one exact candidate commit. A later release record may authorize immutable tag `v0.2.2`, GitHub release assets, checksums, and unchanged promotion to the `se-harness` PyPI project.

The exact release-bearing work is:

- `WO-IAR-002`: concise routing from the managed contract to the authoritative verification and release workflow;
- `WO-IAR-003`: single ownership of review procedure with concise routing from the managed contract;
- `WO-IAR-004`: mandatory, explicit architecture-decision assessment with conditional ADR coverage;
- `WO-IAR-005`: typed architecture-to-requirement and architecture-to-specification traceability;
- `WO-RLS-004`: 0.2.2 versioning, immutable-baseline advancement, and integrated qualification.

The earlier `VREC-IAR-002` remains immutable historical assurance for the IAR implementation commit. It is not edited or invalidated. A new aggregate record must verify the exact integrated 0.2.2 candidate and the five-work-order release set.

## Entry criteria

- All five gated work orders are `implemented` with retained evidence.
- Source version, package metadata, self-hosted harness identity, and managed lock agree on 0.2.2.
- Independent CI uses an immutable released 0.2.1 wheel and verified SHA-256; candidate CI uses the reviewed 0.2.2 source tree.
- Formal validation has zero errors. Any warning is classified, retained, and shown not to weaken the release payload.
- Full supported-runtime tests, CLI, doctor, preflight, Explorer, managed parity, packaging, reproducibility, archive inspection, and fresh-install checks pass.
- A clean candidate commit exists before `VREC-SEH-003` is captured as `ready` in a later governance change.

## Required aggregate verification

`VREC-SEH-003` must bind one clean 0.2.2 candidate commit to exactly `WO-IAR-002`, `WO-IAR-003`, `WO-IAR-004`, `WO-IAR-005`, and `WO-RLS-004`; the applicable contracts are `VER-IAR-002`, `VER-IAR-003`, `VER-IAR-004`, `VER-IAR-005`, and `VER-DST-001`. Each work order must have a distinct retained evidence path.

The record is a later integrated successor, not a rewrite of `VREC-IAR-002`. Human quality-owner review is required for `ready -> verified`.

## Compatibility and migration

Python 3.11+ and the single standard installation remain unchanged. Existing repository-owned content and completed legacy architecture artifacts remain preserved. New and active architecture artifacts use typed relations and explicit decision assessment. Managed upgrades remain transactional and fail closed on customized or ambiguous content.

## Security and provenance

The VREC, any later release record, tag, wheel, normalized source distribution, checksum manifest, GitHub release, and PyPI files must identify or derive from the same candidate commit. Repository content is untrusted input. No artifact value may be executed or interpolated into a shell command.

## Promotion policy and authority

This contract and `WO-RLS-004` authorize reversible 0.2.2 candidate preparation, local verification, the candidate commit, and preparation of a `ready` VREC. They do not authorize quality approval, a release record, tag creation, GitHub publication, PyPI publication, deployment, push, pull-request creation, or merge.

The repository owner selected a new release contract, a replacement integrated verification record, and version 0.2.2 on 2026-08-12. Separate explicit decisions remain required for verification transition and every later release or external action.

## Stop conditions

Stop on a changed candidate identity, missing work-order coverage, graph error, unexplained warning, failed required check, managed-integrity mismatch, package-version mismatch, non-reproducible eligible artifact, unsafe archive member, stale or mutable independent baseline, evidence disagreement, or authority beyond this contract.

## Rollback policy

Before publication, correct failures through a new candidate and a newly captured verification record. Never move a published tag or replace a published package file. After publication, preserve evidence and issue a separately governed corrective version.
