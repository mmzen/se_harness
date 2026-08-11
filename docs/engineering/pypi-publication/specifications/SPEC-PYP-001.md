+++
id = "SPEC-PYP-001"
type = "specification"
title = "Exact-asset PyPI Trusted Publishing contract"
status = "implemented"
owners = ["engineering-owner", "quality-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
specifies = ["REQ-PYP-001", "REQ-PYP-002", "REQ-PYP-003", "REQ-PYP-004", "REQ-PYP-005"]
+++

# Specification: Exact-asset PyPI Trusted Publishing contract

## Scope

Define `.github/workflows/publish-pypi.yml`, the GitHub `pypi` environment, deterministic static verification, and the authority/evidence boundary for promoting one final `se-harness` GitHub release to production PyPI.

## Actors and external systems

- A release owner supplies an authorized tag and expected hashes and approves the protected environment deployment.
- GitHub Releases supplies public release metadata and files.
- GitHub Actions supplies an ephemeral runner, repository token, protected environment, and OIDC identity.
- PyPI trusts the exact repository/workflow/environment identity and receives distributions.
- The PyPA publishing action validates metadata, exchanges OIDC, uploads, and produces attestations.

## Inputs

- `tag`: exact `vMAJOR.MINOR.PATCH` GitHub release tag.
- `wheel_sha256`: lowercase 64-character SHA-256 from retained release evidence.
- `sdist_sha256`: lowercase 64-character SHA-256 from retained release evidence.
- External configuration: GitHub environment `pypi`; PyPI publisher owner `mmzen`, repository `se_harness`, workflow `publish-pypi.yml`, environment `pypi`.

## Outputs

- On success: the exact wheel and sdist published to the `se-harness` PyPI project with PyPI metadata and attestations.
- On failure: a failed workflow with no fallback credential, rebuild, version substitution, or duplicate suppression.
- Separately retained evidence: run URL, PyPI URLs and hashes, attestation visibility, and installation smoke result.

## State model

1. **Configured:** workflow and environment exist; no publication authority is implied.
2. **Authorized:** a separate release-owner record names tag, hashes, and PyPI destination.
3. **Awaiting approval:** manual workflow dispatch is blocked on the `pypi` environment.
4. **Preflight:** release state, filenames, hashes, and manifest are checked.
5. **Publishing:** the pinned PyPA action alone exchanges OIDC and uploads.
6. **Observed:** success or failure evidence is retained; an existing PyPI filename remains terminal for that file.

## Behavioral rules

1. The workflow exposes only `workflow_dispatch` with required tag, wheel hash, and sdist hash inputs.
2. The tag must match `^v[0-9]+\.[0-9]+\.[0-9]+$` and name a non-draft, non-prerelease GitHub release.
3. `VERSION` is the tag without `v`; exact expected files are `se_harness-${VERSION}-py3-none-any.whl`, `se_harness-${VERSION}.tar.gz`, and `SHA256SUMS`.
4. Both supplied hashes must match `^[0-9a-f]{64}$`.
5. Download occurs with the job's read-only repository token into an isolated asset directory.
6. SHA-256 verification uses the supplied hashes independently and requires the downloaded manifest to be byte-identical to a deterministic two-line manifest containing those values and filenames.
7. Only the wheel and sdist are copied into a separate `dist/` directory.
8. The publication job runs only when `github.ref` is `refs/heads/main`; the `pypi` environment permits only `main`; the job has job-scoped `contents: read` and `id-token: write`, stores no PyPI secret, checks out no repository content, and executes no repository code.
9. The publisher is `pypa/gh-action-pypi-publish` pinned to reviewed commit `a892a5a61159132606e93a2fa6f4358831b04d26` (`v1.14.2`). Metadata verification, hash reporting, and attestations are explicit; `skip-existing` is absent.
10. A failed preflight or upload stops. Correction uses a new verified version and a new authorization.
11. Workflow availability, a successful dry static check, or GitHub environment configuration never grants publication authority.

## Error and recovery behavior

All validation errors exit nonzero before the publisher step. External upload errors remain visible in the run. Do not mutate GitHub release assets, move tags, delete PyPI history, introduce token fallback, or enable duplicate skipping. Record partial external state and escalate to release, quality, and security owners.

## Data and interface contracts

The workflow filename and environment name are stable identity inputs to PyPI. Renaming either requires coordinated PyPI configuration and an approved artifact change. Hash inputs are lowercase hex and are never inferred from the colocated checksum file.

## Security and privacy properties

The job has no checkout, package build, arbitrary dependency installation, or stored PyPI credential. The repository token is read-only. OIDC is granted only to the protected publication job. The third-party publisher is pinned by full commit SHA. Workflow logs may expose filenames and hashes but no secret material.

## Performance and capacity

The job downloads and hashes one small wheel and one small sdist. No cache, matrix, concurrency, persistent runner, or background service is required.

## Observability

GitHub retains dispatch inputs, environment deployment approval, logs, action revision, and outcome. PyPI exposes release files, hashes, metadata, and attestations. Repository evidence connects them to the prior GitHub release and governing authorization.

## Compatibility and migration

This adds no runtime dependency, installation profile, CLI behavior, or package rebuild. Existing GitHub-only `RLS-SEH-001` remains unchanged. Future platform wheels, prereleases, alternate names, or indices require a specification change.

## Explicitly unspecified decisions

The implementation agent may choose bounded shell diagnostic wording and unit-test organization. It may not weaken hash comparison, environment/OIDC identity, action pinning, no-checkout/no-build boundaries, duplicate failure, or separate publication authorization.
