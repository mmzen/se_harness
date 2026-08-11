+++
id = "WO-PYP-004"
type = "work_order"
title = "Correct the PyPI publisher immutable commit pin"
status = "implemented"
owners = ["repository-owner", "security-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
implements = ["REQ-PYP-003", "REQ-PYP-004", "REQ-PYP-005"]
specifications = ["SPEC-PYP-001"]
architecture = ["ARCH-PYP-001", "ADR-PYP-001"]
verification = ["VER-PYP-001"]
+++

# Work Order: Correct the PyPI publisher immutable commit pin

## Authorization

The accountable owner authorized completion of the enumerated 0.2.1 release and PyPI steps with `i merged, you can perform the next steps`. The first protected publication run then failed before authentication because the workflow referenced an annotated-tag object rather than the peeled action commit. This work order authorizes the minimum separately governed correction, verification, commits, PR, normal merge after green checks, and one retry with the unchanged release identities.

## Objective

Replace the unusable `v1.14.2` annotated-tag object SHA with the tag's actual immutable commit SHA, prove that the matching public GHCR image exists, prevent regression to the tag-object SHA, and retry exact-asset Trusted Publishing without altering version 0.2.1 or its release assets.

## Root cause and exact correction

- Failed workflow run: `31514559160`.
- Successful pre-upload step: exact GitHub release download and hash verification.
- Failed step: publisher container startup, before OIDC authentication or PyPI upload.
- Incorrect annotated-tag object SHA: `a892a5a61159132606e93a2fa6f4358831b04d26`.
- Official tag: `pypa/gh-action-pypi-publish` `v1.14.2`.
- Peeled immutable commit SHA: `dc37677b2e1c63e2034f94d8a5b11f265b73ba33`.
- Public GHCR manifest for the commit: HTTP 200, digest `sha256:a68d05519f6d7e47372aeaddab80b851b69afa89be179ec41775c72c4e3ab2d5`.

## In scope

- Change only the publisher `uses:` revision from the tag-object SHA to the peeled full commit SHA, retaining the reviewed upstream `v1.14.2` code identity.
- Update static tests to require the peeled commit, reject the known tag-object SHA, retain full-hex immutability, and preserve every publication invariant.
- Correct `ARCH-PYP-001` requirement coverage so deterministic preflight can assess authorized PyPI work orders.
- Retain incident diagnosis and verification evidence.
- Commit the clean candidate, capture `VREC-PYP-002` as `ready`, and record the owner's assurance decision by transitioning only that record to `verified` in later commits.
- Push a normal branch, open a PR declaring this work order, require both CI layers, and merge normally.
- Confirm PyPI 0.2.1 remains absent, then dispatch the same tag and hashes through the corrected workflow and protected `pypi` environment.

## Unchanged publication identities

- Tag: `v0.2.1`.
- Candidate: `94e13e31b81333e1f80f5a7dfd86ed5dbfc1e3e5`.
- Wheel SHA-256: `533f6f87f5a1060d5d0070702969f643525ca3b91e2ecdbbd029f1530d093454`.
- Sdist SHA-256: `770d40cfe9f65970424acb72f9e235365be61e2e8c73dce58274a0f0eca198e4`.
- GitHub release and PyPI project: `mmzen/se_harness` release `v0.2.1`, project `se-harness`.

## Required verification

Official GitHub tag/ref/tag-object APIs must prove the peel. The public GHCR registry must return the commit image manifest. Focused and full suites, formal graph, start/review preflight, workflow security invariants, CLI, doctor, Explorer, diff hygiene, and GitHub CI must pass. The failed run must show no PyPI authentication/upload, and PyPI 0.2.1 must remain absent before retry.

## Stop conditions

Stop if the correction requires a mutable reference, another publisher version, credentials, workflow identity/environment changes, relaxed hashes, rebuild, duplicate tolerance, asset replacement, tag movement, bypassed approval, or any evidence that files reached PyPI.

## Out of scope

Changing released artifacts, package source, version, release record, tag, project, publisher identity, environment, permissions, workflow trigger, hash checks, action inputs, attestation behavior, duplicate behavior, or historical failed-run evidence.

## Completion evidence

Retain exact upstream identities, registry result, failed-run boundary, tests, graph, preflight, and retry authorization in `docs/engineering/pypi-publication/evidence/WO-PYP-004-verification.md`. Final retry and PyPI evidence remains in the release-0.2.1 publication record.
