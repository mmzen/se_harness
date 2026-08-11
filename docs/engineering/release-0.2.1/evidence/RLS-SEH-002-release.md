# Release Evidence for RLS-SEH-002

Date: 2026-08-11

## Accountable release decision

After merging pull request #18, the repository and release owner explicitly instructed `i merged, you can perform the next steps`. The identified next steps included release-record approval, immutable `v0.2.1` GitHub publication, and protected exact-asset PyPI deployment. This is the human release decision required by `WO-RLS-003` and `REL-SEH-002`; automation records and executes only the exact bounded identities.

## Released lineage

- Version and immutable tag: `0.2.1`, `v0.2.1`.
- Candidate commit: `94e13e31b81333e1f80f5a7dfd86ed5dbfc1e3e5`.
- Candidate timestamp/build epoch: `1786466022`.
- Aggregate verification: `VREC-SEH-002`, status `verified`.
- Verification-governance commit: `da260bf`.
- Ready release-record commit: `ab4c22c040184796bb1827a7edfafe7fc57a15f4`.
- Ready release-record SHA-256 before transition: `0b8bc031163028faf1a6d0a956c0590dd05d1c87ed78855d6e811ad2e8a44c9e`.
- Release contract: `REL-SEH-002`.
- Released work: `WO-IAR-001`, `WO-PYP-001`, `WO-RLS-002`, and `WO-WLC-001`.
- Publication targets: GitHub repository `mmzen/se_harness` and PyPI project `se-harness`.

The release record, verified aggregate VREC, artifact source, version, and planned tag all identify the same candidate commit. Governance commits are later retained decisions and are not tag targets.

## Final artifacts

Two independent exports and builds from the candidate produced byte-identical wheels. Raw setuptools sdists had expected timestamp metadata variance; independent normalization at the candidate epoch produced byte-identical final sdists. Rebuilding the wheel offline from the normalized sdist reproduced the direct wheel exactly.

| Asset | Size | SHA-256 |
|---|---:|---|
| `se_harness-0.2.1-py3-none-any.whl` | 92,061 | `533f6f87f5a1060d5d0070702969f643525ca3b91e2ecdbbd029f1530d093454` |
| `se_harness-0.2.1.tar.gz` | 95,569 | `770d40cfe9f65970424acb72f9e235365be61e2e8c73dce58274a0f0eca198e4` |
| `SHA256SUMS` | 190 | `b55951ffad4fda16a612e223e0773467c9cf241c92fb9c1ffe484e26367e65fd` |

Archive, metadata, RECORD, candidate-payload, Python 3.11 offline installation, init, doctor, validator, and Explorer checks passed. Detailed commands, environment, intermediate hashes, and results are retained in `WO-RLS-003-verification.md`.

## Promotion controls

Before tagging and publication:

1. Merge the released record and this evidence into `main` after green independent-baseline and candidate CI.
2. Confirm remote tag `v0.2.1`, GitHub release `v0.2.1`, and PyPI version 0.2.1 do not exist.
3. Create one annotated tag on candidate `94e13e31b81333e1f80f5a7dfd86ed5dbfc1e3e5` and verify its peeled target before pushing.
4. Publish a non-draft, non-prerelease GitHub release with only the exact wheel, normalized sdist, and checksum manifest above.
5. Download the assets independently and verify names, sizes, and hashes.
6. Dispatch `.github/workflows/publish-pypi.yml` from `main` with tag `v0.2.1` and the exact wheel/sdist hashes; preserve environment protection.
7. Verify workflow success, PyPI files/hashes/attestations, and a clean Python 3.11 installation of exactly `se-harness==0.2.1`.

No artifact may be rebuilt, replaced, or uploaded through another path. Any mismatch stops promotion and requires a separately verified corrective version.

## Release transition

`RLS-SEH-002` changed only from `ready` to `released`, with the decision note above. Its version, candidate, object format, timestamp, authorized owner, tag, release contract, included VREC, and exact released-work set remain unchanged.

## Current external state

At the time this governance evidence was committed, tag, GitHub release, and PyPI publication were intentionally still pending. Their URLs, remote checksums, attestations, workflow run, and installation result cannot truthfully be predicted; they will be retained after publication in `PYPI-SEH-002-publication.md`.

## Authority boundary

This decision authorizes the exact release and publication sequence above. It does not authorize tag movement, asset replacement, another version/project, bypassing the protected environment, credential substitution, force push, history rewriting, or deletion of provenance.
