# PyPI Publication Evidence for se-harness 0.2.1

Date: 2026-08-11

## Result

Release `se-harness` 0.2.1 is published on GitHub and production PyPI from the exact verified candidate artifacts. GitHub, PyPI JSON, PyPI Integrity API provenance, workflow deployment, and a clean Python 3.11 installation all agree on version, filenames, sizes, and SHA-256 values.

This evidence completes `WO-RLS-003` at `implemented`. It does not modify the immutable tag, release assets, package files, release record, or candidate identity.

## Governed lineage

- Released candidate: `94e13e31b81333e1f80f5a7dfd86ed5dbfc1e3e5`.
- Verified aggregate record: `VREC-SEH-002`.
- Released record: `RLS-SEH-002`.
- Release-governance PR: `https://github.com/mmzen/se_harness/pull/19`, merge `c542c9291eec95059c2d978a9e8cf0dfb36bf2aa`.
- Immutable annotated tag: `v0.2.1`; remote peeled target `94e13e31b81333e1f80f5a7dfd86ed5dbfc1e3e5`.
- GitHub release: `https://github.com/mmzen/se_harness/releases/tag/v0.2.1`.
- PyPI project/version: `https://pypi.org/project/se-harness/0.2.1/`.

## GitHub release verification

The release is non-draft and non-prerelease. GitHub exposes exactly the three authorized assets:

| Asset | Size | SHA-256 | URL |
|---|---:|---|---|
| `se_harness-0.2.1-py3-none-any.whl` | 92,061 | `533f6f87f5a1060d5d0070702969f643525ca3b91e2ecdbbd029f1530d093454` | `https://github.com/mmzen/se_harness/releases/download/v0.2.1/se_harness-0.2.1-py3-none-any.whl` |
| `se_harness-0.2.1.tar.gz` | 95,569 | `770d40cfe9f65970424acb72f9e235365be61e2e8c73dce58274a0f0eca198e4` | `https://github.com/mmzen/se_harness/releases/download/v0.2.1/se_harness-0.2.1.tar.gz` |
| `SHA256SUMS` | 190 | `b55951ffad4fda16a612e223e0773467c9cf241c92fb9c1ffe484e26367e65fd` | `https://github.com/mmzen/se_harness/releases/download/v0.2.1/SHA256SUMS` |

All three assets were independently downloaded after publication. Names, sizes, hashes, and the exact two-line checksum manifest matched retained release evidence.

## First-run anomaly and correction

Initial protected workflow run `https://github.com/mmzen/se_harness/actions/runs/31514559160` passed exact release download and hash verification but failed before OIDC authentication or upload. The pinned identifier was the signed `v1.14.2` annotated-tag object, so the publisher requested a nonexistent GHCR image tag and received `manifest unknown`. PyPI 0.2.1 remained absent.

`WO-PYP-004` corrected only that identity to the tag's peeled immutable commit `dc37677b2e1c63e2034f94d8a5b11f265b73ba33`. Official upstream metadata and public GHCR manifest digest `sha256:a68d05519f6d7e47372aeaddab80b851b69afa89be179ec41775c72c4e3ab2d5` were verified. Candidate `ce7243a74bd268dcadfde9b6d42f6818913e1795` is bound by verified `VREC-PYP-002`; correction PR `https://github.com/mmzen/se_harness/pull/20` merged at `28fe476ced229bc9f9237848261e1e8139c155b7`.

The failed run remains retained evidence. It was not relabeled, retried unchanged, bypassed, or hidden.

## Successful protected publication

- Workflow run: `https://github.com/mmzen/se_harness/actions/runs/31515473497`.
- Job: `https://github.com/mmzen/se_harness/actions/runs/31515473497/job/93859418663`.
- Workflow source commit: `28fe476ced229bc9f9237848261e1e8139c155b7` on `main`.
- Trigger: manual `workflow_dispatch` with tag `v0.2.1` and the exact two distribution hashes.
- Protected environment: `pypi`, deployment `5854952102`, explicitly owner-approved.
- Result: success at `2026-08-11T17:02:35Z`.

The exact-release download/verification step and Trusted Publishing step both passed. The job used job-scoped `contents: read` and `id-token: write`, no checkout, no build, no token secret, no duplicate skipping, metadata verification, and attestation upload.

## PyPI file verification

PyPI JSON at `https://pypi.org/pypi/se-harness/0.2.1/json` reports project `se-harness`, version `0.2.1`, and exactly two non-yanked files:

| File | Type | Size | SHA-256 | Uploaded | URL |
|---|---|---:|---|---|---|
| `se_harness-0.2.1-py3-none-any.whl` | wheel | 92,061 | `533f6f87f5a1060d5d0070702969f643525ca3b91e2ecdbbd029f1530d093454` | `2026-08-11T17:02:31.639642Z` | `https://files.pythonhosted.org/packages/94/7d/862092f4127e8a8f1da924bdb815a69859e7d89021495990a058f069cb05/se_harness-0.2.1-py3-none-any.whl` |
| `se_harness-0.2.1.tar.gz` | sdist | 95,569 | `770d40cfe9f65970424acb72f9e235365be61e2e8c73dce58274a0f0eca198e4` | `2026-08-11T17:02:32.781993Z` | `https://files.pythonhosted.org/packages/6d/a2/2e0c84a5661c7fcd2aca9d7183dd10618a294def5774a2f87e423dc53814/se_harness-0.2.1.tar.gz` |

## PyPI provenance verification

Both official Integrity API endpoints returned one attestation bundle:

- `https://pypi.org/integrity/se-harness/0.2.1/se_harness-0.2.1-py3-none-any.whl/provenance`;
- `https://pypi.org/integrity/se-harness/0.2.1/se_harness-0.2.1.tar.gz/provenance`.

Each bundle identifies publisher kind `GitHub`, repository `mmzen/se_harness`, workflow `publish-pypi.yml`, and environment `pypi`. Each contains a PyPI publish attestation with predicate `https://docs.pypi.org/attestations/publish/v1`; the subject filename and SHA-256 exactly match the corresponding published file.

## Clean production installation

A new Python `3.11.9` virtual environment installed exactly `se-harness==0.2.1` from `https://pypi.org/simple` using `--no-cache-dir --no-deps --only-binary=:all:`. Package metadata and `harnessctl --version` both returned `0.2.1`.

The installed CLI initialized all `32` standard files into a new repository. Doctor passed every required, distribution, fragment, seed, and managed-integrity check. The installed validator returned zero diagnostics. Explorer generated the empty initial artifact graph successfully with snapshot `f5d3750583c0629f4f2e192f08fa88bb754d76811a0962c2a8817bd88f21c597`.

## Residual observations

- The first failed workflow run is a resolved publication-infrastructure anomaly and did not reach PyPI.
- GitHub Actions reports separate non-blocking Node.js runtime deprecation annotations for other pinned CI actions; these do not affect the PyPI publisher container or released artifacts and remain separately governed.
- GitHub and PyPI are external immutable services. A future defect requires a new version; no tag, release asset, or PyPI file may be replaced.

## Completion boundary

Version 0.2.1 publication is complete. No further dispatch, upload, tag, release mutation, or asset replacement is authorized by this evidence.
