+++
id = "REL-DST-001"
type = "release_contract"
title = "Release the standard harness distribution"
status = "approved"
owners = ["release-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
gates = ["WO-AGR-001", "WO-DOC-001", "WO-DOC-002", "WO-DST-001", "WO-DST-002", "WO-DST-003", "WO-PMI-001", "WO-REV-001", "WO-RLS-001", "WO-VSP-001"]
+++

# Release Contract: Standard harness distribution

## Release unit

The versioned `se-harness` wheel, source distribution, source tag, canonical standard template, repository documentation, and checksum manifest. A release instance selects an explicit subset of the gated release-bearing work orders and binds the complete selection to one verified candidate commit.

## Gated 0.2.0 payload

- Core distribution and repository documentation: `WO-DST-001`, `WO-DST-002`, `WO-DST-003`, `WO-DOC-001`, and `WO-DOC-002`.
- Commit-bound and aggregate provenance: `WO-REV-001` and `WO-AGR-001`.
- Portable managed-file integrity: `WO-PMI-001`.
- Verification-record supersession: `WO-VSP-001`.
- Release qualification and deterministic source-distribution tooling: `WO-RLS-001`.

Publication and verification-decision work orders are governance history, not software payload, and are not gated by this contract.

## Required evidence

Release requires a valid artifact graph, the complete unit suite, CLI and doctor checks, deterministic dashboard generation, a reproducible package containing the complete standard template, Python 3.11 compatibility, wheel and source-distribution inspection, a clean fresh-environment installation, checksum retention, and one verified aggregate VREC covering the exact selected payload at one candidate commit.

## Promotion policy

The release record, aggregate VREC, tag, wheel, source distribution, and checksum manifest must agree on one candidate commit and version. The release record is prepared as `ready`; release-owner review later authorizes its `released` transition, the immutable `v0.2.0` tag, and GitHub publication.

## Compatibility and rollback

The standard installation remains the only supported profile and keeps its standard-library runtime. Customized target files remain protected. Do not publish if provenance, compatibility, installation, or checksum verification fails. If a published artifact is defective, preserve the tag and release history, mark the release affected, and prepare a separately verified corrective version.

## Authority boundary

Repository creation, implementation verification, package building, VREC capture, and release-record preparation do not themselves authorize a tag or publication. PyPI publication, deployment, and any package-registry credential use remain outside this contract.
