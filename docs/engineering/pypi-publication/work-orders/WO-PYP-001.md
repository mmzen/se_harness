+++
id = "WO-PYP-001"
type = "work_order"
title = "Implement governed PyPI Trusted Publishing"
status = "implemented"
owners = ["repository-owner", "engineering-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
implements = ["REQ-PYP-001", "REQ-PYP-002", "REQ-PYP-003", "REQ-PYP-004", "REQ-PYP-005"]
specifications = ["SPEC-PYP-001"]
architecture = ["ARCH-PYP-001", "ADR-PYP-001"]
verification = ["VER-PYP-001"]
+++

# Work Order: Implement governed PyPI Trusted Publishing

## Objective

Add and verify a repository-specific Trusted Publishing workflow that can later promote exact authorized GitHub release assets to the existing `se-harness` PyPI project without rebuilding or storing a PyPI credential.

## Authorization

After reviewing the proposed PyPI Trusted Publishing design and creating the PyPI account and project, the accountable repository owner explicitly authorized the remaining implementation actions on 2026-08-11 with the instruction `i created the PyPI account and project. Can you implement the other actions`.

This authorization covers the workflow, deterministic tests, artifact packet, implementation evidence, and creation/configuration of the GitHub `pypi` environment. It does not authorize a workflow dispatch, PyPI upload, package-index credential entry, commit, push, pull request, verification transition, release record, tag, GitHub release change, merge, or deployment.

After implementation, the accountable repository owner explicitly authorized `mmzen` self-review for the protected environment and confirmed creation of the exact PyPI publisher on 2026-08-11 with the instruction `i authorized self review and created the publisher`. This changes environment review configuration only; it does not authorize a workflow dispatch or package publication.

## In scope

- Add `.github/workflows/publish-pypi.yml` implementing `SPEC-PYP-001`.
- Pin the official PyPA action to reviewed `v1.14.2` commit `a892a5a61159132606e93a2fa6f4358831b04d26`.
- Add deterministic static tests for trigger, inputs, release-state checks, exact filenames, independent hashes, manifest equality, least privilege, environment, OIDC, no checkout/build/secret, publisher options, attestations, and duplicate failure.
- Create the GitHub `pypi` environment, restrict it to `main`, require accountable review, and inspect its resulting API state when repository permissions allow.
- Document the remaining exact PyPI publisher configuration and publication authority boundary.
- Run `VER-PYP-001`, full repository checks, and retain implementation evidence.

## Out of scope

- Running the workflow or uploading `0.2.0` or any other version to PyPI.
- Entering or storing PyPI credentials.
- Rebuilding, renaming, deleting, or replacing any release file.
- Editing `RLS-SEH-001`, moving `v0.2.0`, or changing the GitHub release.
- Automatically triggering from a tag or GitHub release.
- Supporting prereleases, platform-specific wheels, alternate projects, or alternate indexes.
- Committing, pushing, opening a pull request, merging, capturing a VREC, or granting verification/release status without separate authorization.

## Authorized decision envelope

The implementation agent may choose bounded shell diagnostic text and deterministic unit-test structure. It may not weaken manual selection, hash/manifest equality, OIDC/environment identity, job-scoped permissions, immutable action pinning, no-checkout/no-build rules, metadata/attestation defaults, duplicate failure, or separate publication authority.

## Constraints

Preserve the standard-library runtime, one standard installation, current package artifacts, repository history, and all existing governance decisions. Treat workflow inputs and downloaded files as untrusted. Do not expose secrets or execute repository content in the OIDC job.

## Expected change surface

Repository-specific GitHub workflow, PyPI publication artifact packet, one static unit-test module, engineering overview, external GitHub environment configuration, and retained verification evidence.

## Required verification

Run the artifact validator before and after implementation; focused PyPI workflow tests; the complete unit suite; CLI help; source doctor; workflow diff security review; action-pin verification against the official upstream tag; and GitHub environment API inspection. Do not perform the irreversible PyPI upload under this work order.

## Evidence to record

Retain exact commands and results, artifact counts, test counts, workflow invariant matrix, reviewed action version/SHA, GitHub environment state, PyPI configuration still requiring owner confirmation, deviations, and residual risks in `docs/engineering/pypi-publication/evidence/WO-PYP-001-verification.md`.

## Stop and escalate conditions

Stop if implementation requires a PyPI token, repository checkout or code execution in the OIDC job, artifact rebuilding, mutable action reference, automatic publication, relaxed duplicate handling, unavailable exact hashes, a changed release asset, environment protection that cannot be inspected, or actual package publication.

## Completion report format

Report implemented requirements, workflow and external configuration, exact verification results, remaining owner-controlled PyPI publisher step, excluded publication action, deviations, and residual risks.
