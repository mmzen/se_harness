+++
id = "WO-RLS-001"
type = "work_order"
title = "Qualify and prepare se-harness 0.2.0"
status = "implemented"
owners = ["release-owner", "quality-owner", "engineering-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
implements = ["REQ-AGR-002", "REQ-AGR-003", "REQ-AGR-005", "REQ-AGR-007", "REQ-DST-006"]
specifications = ["SPEC-AGR-001", "SPEC-DST-001"]
architecture = ["ARCH-AGR-001", "ADR-AGR-001", "ARCH-DST-001", "ADR-DST-001"]
verification = ["VER-AGR-001", "VER-DST-001"]
+++

# Work Order: Qualify and prepare se-harness 0.2.0

## Authorization

The accountable repository and release owner confirmed version `0.2.0`, tag `v0.2.0`, the initial nine-work-order release-bearing payload, and GitHub-only publication on 2026-08-11 with the instruction `ok, then let's go`.

During qualification, two raw setuptools sdists contained identical payload bytes but different generated timestamps. After reviewing the blocking result and proposed bounded correction, the accountable owner explicitly authorized the release-build scope extension on 2026-08-11 with the instruction `implement the deterministic sdist fix`. Because that implementation is included in the source distribution, this work order is the tenth release-bearing item and must be covered by the aggregate VREC and release record.

## Objective

Produce one fully qualified candidate and auditable release lineage for the current `se-harness` repository without combining verification records that identify different historical commits.

## In scope

- Expand `REL-DST-001` to gate the ten explicitly selected release-bearing work orders.
- Run the complete graph, unit, CLI, doctor, dashboard, packaging, wheel-content, source-distribution, Python 3.11, and fresh-install qualification matrix.
- Add a repository-only deterministic sdist normalizer that preserves member payloads and modes while normalizing archive order, ownership, timestamps, extended metadata, and the gzip header to an explicit epoch.
- Include that normalizer in the source distribution; reject unsafe, duplicate, or special archive members and refuse to overwrite an existing output.
- Retain commands, results, raw-build deviations, normalized hashes, and residual risks in `evidence/WO-RLS-001-verification.md`.
- Commit the approved release scope and qualification evidence as one clean candidate.
- Capture `VREC-SEH-001` as a later `ready` aggregate record naming that exact candidate and the retained evidence for all ten work orders.
- After separate accountable quality approval, prepare `RLS-SEH-001` as `ready` under `REL-DST-001` for version `0.2.0` and tag `v0.2.0`.
- After separate accountable release approval, build or reproduce the final artifacts from the recorded candidate, transition the release record, create the immutable tag, and publish the GitHub release assets.

## Out of scope

- PyPI or another package-index publication.
- Changing package runtime behavior, version, dependency policy, installation profiles, or the source payload selected by setuptools.
- Treating governance-only publication and decision work orders as released software payload.
- Reusing historical VRECs as if their different commits were one candidate.
- Moving or replacing a published tag, deleting provenance, superseding a concrete VREC, deploying, or using package-registry credentials.

## Exact payload

`WO-AGR-001`, `WO-DOC-001`, `WO-DOC-002`, `WO-DST-001`, `WO-DST-002`, `WO-DST-003`, `WO-PMI-001`, `WO-REV-001`, `WO-RLS-001`, and `WO-VSP-001`.

The applicable verification contracts are `VER-AGR-001`, `VER-DST-001`, `VER-DST-002`, `VER-PMI-001`, `VER-REV-001`, and `VER-VSP-001`.

## Required verification

- Artifact validation: zero errors and zero warnings.
- Complete unit suite on the local supported runtime and a separate Python 3.11 execution path.
- CLI help, doctor, dashboard generation, source/canonical parity, and diff hygiene.
- Two independent raw wheel and sdist builds with recorded SHA-256 hashes and inspected contents.
- Deterministic normalization tests covering metadata variance, input ordering, payload preservation, unsafe and duplicate paths, special members, atomic failure, and non-overwrite.
- Byte-identical normalized sdists from the two raw builds at one explicit candidate-derived epoch; identical member payloads before and after normalization.
- Fresh virtual-environment installation from the wheel, followed by version, init, doctor, validation, and dashboard smoke tests.
- Clean Git state before aggregate VREC capture; candidate availability and ancestry checks afterward.
- GitHub `main` CI green for the final candidate before release authorization.

## Phase gates

Automation may qualify, build locally, commit the candidate when explicitly authorized here, and prepare only `ready` VREC/RLS records. Quality-owner review is required for `VREC-SEH-001 -> verified`. Release-owner review is required for `RLS-SEH-001 -> released`, `v0.2.0`, and GitHub publication. Any failed required check or changed payload stops promotion.
