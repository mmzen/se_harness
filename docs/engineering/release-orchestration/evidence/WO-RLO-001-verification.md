# WO-RLO-001 implementation evidence

## Scope and authority

The repository owner approved the complete RLO packet on 2026-08-18 with `ok, go implement`. This evidence covers only the bounded implementation of `REQ-RLO-001` through `REQ-RLO-008` and the selected PYP/DPG control amendments. It records derived checks and does not verify a commit, approve a VREC or RLS, create or move a tag, publish a GitHub Release or package, deploy Pages, approve an environment, change external publisher configuration, promote the governor, commit, push, or open a pull request.

Base `HEAD` during implementation was `cbdb46f9d7077c8812e77663391aae0e3eab4a1f`. The worktree was intentionally dirty with the authorized implementation, so no candidate commit identity or promotable distribution was claimed. Commit-bound source/package/governor acceptance and hosted CI remain review-candidate evidence.

## Implemented controls

- Added optional all-or-none release `[distribution]` schema 1 validation while preserving historical RLS files without the block.
- Added deterministic `se-harness-release-bundle/v1` production from an exact Git tree and wheel/sdist, plus strict `prepare-release --distribution-manifest` capture of version, candidate, object format, commit epoch, filenames, hashes, canonical `SHA256SUMS`, and source-tree manifest identity.
- Added trusted-main RLS resolution, VREC/candidate checks, first-parent governance integration resolution, exact bundle verification, absent/exact/partial/mismatched GitHub and PyPI classification, deterministic notes, and `se-harness-release-result/v1` reporting.
- Preserved `.github/workflows/publish-pypi.yml` as the top-level PyPI Trusted Publisher identity and changed its normal interface to one required `release_record` input.
- Separated resolution, credential-free double-build qualification, GitHub write, protected checkout-free PyPI OIDC, main-context Pages build/deploy, and public observation jobs.
- Removed the Pages `release.published` trigger. `.github/workflows/publish-dashboard-pages.yml` is now main-only recovery with RLS plus explicit governance commit; tag and candidate are derived.
- Added bounded resolution-refusal evidence, exact replay behavior, protected global PyPI concurrency, public exact-version installation, PyPI Integrity API attestation observation, and Pages provenance observation.
- Reconciled only the two expected managed lock digests for the canonical release-record template and validator.

## Structured contracts

The release distribution block contains exactly `schema`, `kind`, `source_date_epoch`, `wheel`, `wheel_sha256`, `sdist`, `sdist_sha256`, `checksums`, `checksums_sha256`, and `source_manifest_sha256`. `kind` is `python-wheel-sdist`; filenames are version-derived safe basenames; all digests are lowercase SHA-256; and checksum bytes are the exact LF-terminated two-line manifest.

The JSON bundle adds `schema = se-harness-release-bundle/v1`, version, full commit, Git object format, and canonical checksum content. The workflow plan is `se-harness-release-plan/v1`; the final observation is `se-harness-release-result/v1` and retains separate resolution, qualification, GitHub, PyPI, Pages, and public-install states. No aggregate score converts a failed or unobserved channel into success.

## Workflow trust matrix

| Job/boundary | Candidate execution | Effective special permission | Environment | Main invariant |
| --- | --- | --- | --- | --- |
| resolve | no candidate execution | `contents: read` | none | one released RLS in trusted first-parent main; released governor validates graph |
| qualify | yes, exact candidate only | `contents: read`; no write/OIDC/Pages | none | two exports/builds, byte equality, RLS hash and source-manifest equality |
| github_release | no candidate execution | `contents: write` only | none | exact immutable tag, draft staging, exactly three release assets |
| pypi | no checkout/build/repository code | `contents: read`, `id-token: write` | `pypi` | exact final GitHub assets; absent or exact PyPI state only; no `skip-existing` |
| pages_build | governance generation only | `contents: read` | none | immutable main-history governance snapshot and released governor |
| pages_deploy | no repository execution | `pages: write`, `id-token: write` | `github-pages` | main-context protected deployment |
| observe | public exact-version install only | `contents: read` | none | channel-specific URLs, hashes, attestations, provenance, and states |

Reviewed immutable action identities include checkout `3d3c42e5aac5ba805825da76410c181273ba90b1`, setup-python `5fda3b95a4ea91299a34e894583c3862153e4b97`, upload-artifact `ea165f8d65b6e75b540449e92b4886f43607fa02`, download-artifact `634f93cb2916e3fdff6788551b99b062d0335ce0`, PyPI publisher `dc37677b2e1c63e2034f94d8a5b11f265b73ba33`, configure-pages `45bfe0192ca1faeb007ade9deae92b16b8254a0d`, upload-pages-artifact `fc324d3547104276b827a68afc52ff2a11cc49c9`, and deploy-pages `cd2ce8fcbc39b97be8ca5fce6e763baed58fa128`.

## Verification results

| Command/check | Result |
| --- | --- |
| start preflight for `WO-RLO-001` | PASS after accountable approval |
| candidate graph validation | PASS: 463 artifacts; structure E0/W0, governance E0/W0, policy E0/W0; unchanged maintenance W44 |
| focused release/provenance/PyPI/Pages suite | PASS: 64 tests, one existing skip after final hardening |
| expanded focused implementation/documentation suite | PASS: 95 tests, one existing skip |
| full default suite on Python 3.14.6 | PASS: 243 tests, three existing skips |
| full minimum-runtime suite using `py -3.11` | PASS: 243 tests, three existing skips |
| candidate CLI `prepare-release --help` | PASS; `--distribution-manifest` exposed |
| managed validator and release-template copy hashes | PASS; each pair byte-identical |
| PyYAML 6.0.3 parse of both changed workflows | PASS: two files |
| Python compilation of new/changed helpers | PASS |
| `git diff --check` | PASS; only host CRLF conversion notices |

Unit fixtures cover complete, partial, unsafe, wrong-version, wrong-candidate/epoch, noncanonical-checksum, exact/extra bundle, PyPI absent/exact/partial/mismatched, GitHub absent/exact draft/empty partial/mismatched, result-stage non-inference, one-input policy, credential separation, and historical RLS compatibility. The bundle producer independently hashes exact bytes and the NUL-delimited full candidate tree listing. No production artifact hashes exist because the approved work explicitly prohibited a promotable release build before a clean candidate commit.

## Runtime and external boundaries

The candidate source reports version `0.4.1`. The independent self-hosting descriptor remains released governor `0.3.0` with wheel SHA-256 `260e22371b05e5bb6c59143a1f0229855305a6bf7994984be50aa147a02ea516`; this implementation did not promote it. The default local suite used Python 3.14.6 and the minimum-runtime suite used the installed Python 3.11 runtime.

PyPI's authoritative Integrity API documents `GET /integrity/<project>/<version>/<filename>/provenance`; the observer requires a non-empty attestation bundle for both distributions. PyPI's documented limitation on reusable workflows motivated preserving the top-level `publish-pypi.yml` identity. Live `pypi` and `github-pages` administrator configuration was not mutated or used as implementation evidence.

## Documentation and residual risk

Updated repository context, contributor release instructions, Pages operations, and the selected PyPI/Pages requirements, specifications, architecture, decisions, verification contracts, and operating contracts. Historical work orders and evidence were not rewritten.

Residual uncertainty remains in future GitHub API/CLI behavior, PyPI/Pages availability and administrator drift, environment reviewers, runner tool availability, and the first irreversible end-to-end release. Fixture and static checks cannot prove those external systems. A later clean candidate commit, candidate-source/package acceptance, released-governor review, hosted CI, accountable VREC decision, and separately authorized real release must confirm the operational path. Exact prior state is replayable; partial or mismatched immutable state intentionally stops for human disposition.
