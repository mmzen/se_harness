+++
id = "WO-RLS-004"
type = "work_order"
title = "Qualify the integrated se-harness 0.2.2 candidate"
status = "implemented"
owners = ["repository-owner", "release-owner", "quality-owner", "engineering-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
implements = ["REQ-DST-006"]
specifications = ["SPEC-DST-001"]
architecture = ["ARCH-DST-001", "ADR-DST-001"]
verification = ["VER-DST-001"]
+++

# Work Order: Qualify the integrated se-harness 0.2.2 candidate

## Authorization

The repository owner explicitly requested a new release contract and a replacement integrated verification record for version 0.2.2 on 2026-08-12. This approves `REL-SEH-003` and this bounded candidate-preparation work. It authorizes implementation, retained evidence, a clean candidate commit, and later preparation of `VREC-SEH-003` as `ready`; it does not authorize its verification transition or any external release action.

## Objective

Produce one clean, fully qualified 0.2.2 candidate containing the four already-implemented instruction-architecture work items, consistent distribution/version metadata, and independent assurance against immutable released version 0.2.1. Then capture a later aggregate ready VREC for the exact five-work-order release set.

## In scope

- Gate exactly `WO-IAR-002`, `WO-IAR-003`, `WO-IAR-004`, `WO-IAR-005`, and this work order under `REL-SEH-003`.
- Preserve `VREC-IAR-002` as verified history for implementation commit `ca2006059eac8d13de9190d3c7b07066f82c5f74`.
- Set package and installed-harness identity to 0.2.2, update public installation guidance for the intended release, and apply the supported self-upgrade.
- Advance the independent external CI baseline from released 0.2.0 to released 0.2.1 using its immutable GitHub wheel and retained SHA-256; keep candidate-source checks distinct.
- Run formal graph validation, both preflight phases as applicable, full tests on Python 3.11 and the local runtime, CLI and doctor checks, deterministic Explorer generation, managed parity, package builds, archive inspection, reproducibility checks, and a fresh Python 3.11 installation.
- Retain qualification evidence, mark this work order `implemented`, commit the clean candidate, and capture `VREC-SEH-003` as `ready` in a later governance change.

## Exact aggregate scope

- Work orders: `WO-IAR-002`, `WO-IAR-003`, `WO-IAR-004`, `WO-IAR-005`, `WO-RLS-004`.
- Verification contracts: `VER-IAR-002`, `VER-IAR-003`, `VER-IAR-004`, `VER-IAR-005`, `VER-DST-001`.
- Evidence: the four existing IAR evidence files plus `docs/engineering/release-0.2.2/evidence/WO-RLS-004-verification.md`.
- Planned aggregate record: `VREC-SEH-003` in the `release-0.2.2` domain.

## Required verification

- Zero formal graph errors; classify every advisory and distinguish legacy compatibility from release-blocking inconsistency.
- Complete supported-runtime regression with only documented platform-conditional skips.
- Version/help, doctor, start and review preflight, deterministic Explorer, workflow parsing, source/canonical parity, lock integrity, and diff hygiene.
- Two independent wheel and raw-sdist builds at one explicit epoch; byte-identical wheels and normalized sdists; identical safe payload manifests and valid wheel RECORD metadata.
- Offline wheel reconstruction from the normalized sdist and clean Python 3.11 installation with initialization, doctor, validation, preflight-capable content, and Explorer smoke checks.
- Exact preservation of immutable captured fields and status in `VREC-IAR-002`.

## Lifecycle and evidence

Move this work order through `in_progress` to `implemented` only after retained evidence passes. The candidate commit must include all authorized source, managed-file, packet, lifecycle, and evidence changes. `VREC-SEH-003` must be created afterward because it identifies that commit.

Retain exact commands, versions, counts, exit codes, hashes, warnings, changed paths, baseline identity, archive results, fresh-install results, deviations, residual risks, and authority boundary in `docs/engineering/release-0.2.2/evidence/WO-RLS-004-verification.md`.

## Out of scope

Editing or superseding a verified historical VREC; transitioning `VREC-SEH-003`; preparing or approving a release record; creating or moving `v0.2.2`; GitHub or PyPI publication; environment approval; deployment; push; pull request; merge; force push; history rewriting; or changing an already-published artifact.

## Stop conditions

Stop on any missing aggregate member, failed check, unclassified diagnostic, changed historical provenance, version disagreement, mutable/unverified baseline, customized managed-file conflict, package mismatch, unsafe archive, non-reproducible eligible artifact, or need for authority outside this work order.
