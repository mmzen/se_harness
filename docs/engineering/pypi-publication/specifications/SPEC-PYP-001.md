+++
id = "SPEC-PYP-001"
type = "specification"
title = "Exact-asset PyPI Trusted Publishing contract"
status = "implemented"
owners = ["engineering-owner", "quality-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-18"

[relations]
specifies = ["REQ-PYP-001", "REQ-PYP-002", "REQ-PYP-003", "REQ-PYP-004", "REQ-PYP-005"]
+++

# Specification: Exact-asset PyPI Trusted Publishing contract

## Scope

Define `.github/workflows/publish-pypi.yml`, the GitHub `pypi` environment, deterministic static verification, and the authority/evidence boundary for promoting one final `se-harness` GitHub release to production PyPI.

## Actors and external systems

- A release owner supplies one released RLS ID and approves the protected environment deployment; the workflow derives the tag and expected hashes.
- GitHub Releases supplies public release metadata and files.
- GitHub Actions supplies an ephemeral runner, repository token, protected environment, and OIDC identity.
- PyPI trusts the exact repository/workflow/environment identity and receives distributions.
- The PyPA publishing action validates metadata, exchanges OIDC, uploads, and produces attestations.

## Inputs

- `release_record`: one canonical released `RLS-*` identifier integrated into trusted `main` history.
- Derived from that record: exact tag, candidate, version, wheel/sdist/checksum filenames and lowercase SHA-256 values.
- External configuration: GitHub environment `pypi`; PyPI publisher owner `mmzen`, repository `se_harness`, workflow `publish-pypi.yml`, environment `pypi`.

## Outputs

- On success: the exact wheel and sdist published to the `se-harness` PyPI project with PyPI metadata and attestations.
- On failure: a failed workflow with no fallback credential, rebuild, version substitution, or duplicate suppression.
- Separately retained evidence: run URL, PyPI URLs and hashes, attestation visibility, and installation smoke result.

## State model

1. **Configured:** workflow and environment exist; no publication authority is implied.
2. **Authorized:** a released RLS names the candidate, tag, structured distribution identities, and release scope.
3. **Awaiting approval:** manual workflow dispatch is blocked on the `pypi` environment.
4. **Preflight:** release state, filenames, hashes, and manifest are checked.
5. **Publishing:** the pinned PyPA action alone exchanges OIDC and uploads.
6. **Observed:** success or failure evidence is retained; an existing PyPI filename remains terminal for that file.

## Behavioral rules

1. The top-level workflow exposes only `workflow_dispatch` with one required `release_record` input; it accepts no tag, version, candidate, filename, hash, force, or skip override.
2. Trusted resolution requires the record to be `released` on first-parent `main`, derives a tag matching `^v[0-9]+\.[0-9]+\.[0-9]+$`, and requires the final GitHub Release to be non-draft and non-prerelease before PyPI promotion.
3. `VERSION` is the tag without `v`; exact expected files are `se_harness-${VERSION}-py3-none-any.whl`, `se_harness-${VERSION}.tar.gz`, and `SHA256SUMS`.
4. Both RLS-derived distribution hashes must match `^[0-9a-f]{64}$`; downstream jobs cannot replace them.
5. Download occurs with the job's read-only repository token into an isolated asset directory.
6. SHA-256 verification uses the RLS-derived hashes independently and requires the downloaded manifest to be byte-identical to a deterministic two-line manifest containing those values and filenames.
7. Only the wheel and sdist are copied into a separate `dist/` directory.
8. The publication job runs only when `github.ref` is `refs/heads/main`; the `pypi` environment permits only `main`; the job has job-scoped `contents: read` and `id-token: write`, stores no PyPI secret, checks out no repository content, and executes no repository code.
9. The publisher is `pypa/gh-action-pypi-publish` pinned to reviewed peeled commit `dc37677b2e1c63e2034f94d8a5b11f265b73ba33` (`v1.14.2`). Metadata verification, hash reporting, and attestations are explicit; `skip-existing` is absent.
10. Before the publisher, public PyPI state is classified: no files is eligible, both exact files is replay-complete without upload, and any partial, unexpected, or mismatched state blocks.
11. A failed preflight or upload stops. Correction uses a new verified version and a new authorization; immutable state is not deleted or replaced.
12. Workflow availability, a successful dry static check, or GitHub environment configuration never grants publication authority.

## Error and recovery behavior

All validation errors exit nonzero before the publisher step. External upload errors remain visible in the run. Do not mutate GitHub release assets, move tags, delete PyPI history, introduce token fallback, or enable duplicate skipping. Record partial external state and escalate to release, quality, and security owners.

## Data and interface contracts

The workflow filename and environment name are stable identity inputs to PyPI. Renaming either requires coordinated PyPI configuration and an approved artifact change. Hashes are lowercase hex derived from the released RLS and are never inferred from the colocated checksum file.

## Security and privacy properties

The job has no checkout, package build, arbitrary dependency installation, or stored PyPI credential. The repository token is read-only. OIDC is granted only to the protected publication job. The third-party publisher is pinned by full commit SHA. Workflow logs may expose filenames and hashes but no secret material.

## Performance and capacity

The job downloads and hashes one small wheel and one small sdist. No cache, matrix, concurrency, persistent runner, or background service is required.

## Observability

GitHub retains the RLS dispatch input, derived plan, environment deployment approval, logs, action revision, and outcome. PyPI exposes release files, hashes, metadata, and attestations. The orchestration result connects them to the GitHub release and governing authorization.

## Compatibility and migration

This adds no runtime dependency, installation profile, CLI behavior, or package rebuild. Existing GitHub-only `RLS-SEH-001` remains unchanged. Future platform wheels, prereleases, alternate names, or indices require a specification change.

## Explicitly unspecified decisions

The implementation agent may choose bounded shell diagnostic wording and unit-test organization. It may not weaken hash comparison, environment/OIDC identity, action pinning, no-checkout/no-build boundaries, duplicate failure, or separate publication authorization.
