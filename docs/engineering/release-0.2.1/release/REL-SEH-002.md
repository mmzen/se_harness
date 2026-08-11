+++
id = "REL-SEH-002"
type = "release_contract"
title = "Release and publish se-harness 0.2.1"
status = "approved"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
gates = ["WO-IAR-001", "WO-PYP-001", "WO-RLS-002", "WO-WLC-001"]
+++

# Release Contract: Release and publish se-harness 0.2.1

## Release unit

The incremental `se-harness` 0.2.1 wheel, normalized source distribution, immutable `v0.2.1` tag, GitHub release, checksum manifest, and promotion of those exact GitHub assets to the `se-harness` PyPI project.

The release-bearing work since 0.2.0 is exactly:

- `WO-PYP-001`: governed PyPI Trusted Publishing automation;
- `WO-WLC-001`: explicit work-order lifecycle consistency;
- `WO-IAR-001`: rationalized instruction architecture, ownership, preflight, and independent CI enforcement;
- `WO-RLS-002`: versioning and final integrated release qualification.

Governance-only verification decisions, publication mechanics, ready-record capture, and release transitions remain audit history rather than released-work entries.

## Required evidence

Release requires one clean final candidate commit, one verified aggregate VREC covering the exact four-work-order set at that commit, zero formal-graph diagnostics, the complete supported-runtime suite, CLI and doctor checks, deterministic Explorer generation, source/canonical parity, two independent wheel and raw-sdist builds, byte-identical normalized sdists, wheel/sdist inspection, an offline Python 3.11 install and initialized-repository smoke test, and retained final SHA-256 values.

PyPI promotion additionally requires a released `RLS-SEH-002`, immutable non-draft/non-prerelease GitHub release `v0.2.1`, an exact `SHA256SUMS`, explicit release-owner authorization naming the hashes and target project, successful protected-environment Trusted Publishing, retained workflow and PyPI URLs, attestations, and a clean `se-harness==0.2.1` installation from PyPI.

## Compatibility and migration

Python 3.11+ and standard-library runtime behavior remain unchanged. There is one standard installation. Existing owner-controlled seed files and content outside managed fragments remain preserved. Customized or ambiguous upgrades remain fail-closed and transactional.

The independent CI baseline remains pinned to immutable release 0.2.0 during this candidate's bootstrap. Candidate-source verification covers the new 0.2.1 behavior. A later separately governed template update may advance the external baseline only after 0.2.1 is immutable and independently available.

## Security and provenance

The aggregate VREC, release record, tag, wheel, source distribution, checksum manifest, GitHub release, and PyPI files must identify or derive from one exact candidate commit. Publication uses only GitHub OIDC Trusted Publishing through the protected `pypi` environment; no long-lived PyPI credential or candidate rebuild is permitted.

## Promotion policy

Preparation commands may create only `ready` review records. The quality owner separately transitions aggregate verification. The release owner separately transitions the release record and authorizes the immutable tag, GitHub release, exact hashes, target PyPI project, and workflow dispatch. Any failed gate, changed payload, checksum disagreement, duplicate version, or external-configuration drift stops promotion.

## Human approval triggers

Quality-owner approval is required for `VREC-SEH-002 -> verified`. Release-owner approval is required for `RLS-SEH-002 -> released`, tag `v0.2.1`, GitHub publication, and the exact PyPI dispatch. Security-owner review is required if the Trusted Publisher identity, protected environment, permissions, action pin, or publication workflow changes.

## Rollback criteria and procedure

Never move or replace a published tag or package file. Before publication, stop and correct the candidate through new verification. After publication, preserve all evidence, identify the release as affected where supported, disable the publisher if trust configuration is suspect, and issue a separately verified corrective version.

## Post-release observation window

After the first PyPI publication, confirm the GitHub and PyPI hashes and attestations, install exact version 0.2.1 from PyPI into a clean Python 3.11 environment, initialize a new repository, and run doctor, formal validation, preflight, and Explorer generation. Retain all results before considering publication complete.

## Authority

The repository owner explicitly selected version `0.2.1`, requested the verification transition and governance PR, and stated that this release includes PyPI deployment on 2026-08-11. This approves the bounded contract and candidate work. It does not bypass the commit-bound aggregate verification and release-record sequence described above.
