+++
id = "SPEC-RLO-001"
type = "specification"
title = "Deterministic released-record publication contract"
status = "approved"
owners = ["engineering-owner", "release-owner", "security-owner"]
created = "2026-08-18"
updated = "2026-08-18"

[relations]
specifies = ["REQ-RLO-001", "REQ-RLO-002", "REQ-RLO-003", "REQ-RLO-004", "REQ-RLO-005", "REQ-RLO-006", "REQ-RLO-007", "REQ-RLO-008"]
+++

# Specification: Deterministic released-record publication contract

## Scope

Define the repository-specific workflow and supporting control-plane behavior that consume one released RLS from trusted `main`, reconstruct and qualify its exact Python distributions, create or reconcile the immutable tag and GitHub Release, promote exact assets to PyPI, deploy the release-bound Explorer demonstration, and retain post-publication observations.

This specification composes rather than copies the exact-asset controls in `SPEC-PYP-001` and the immutable-governance demonstration controls in `SPEC-DPG-001`. Those artifacts must be amended only where their trigger and orchestration interfaces change; their least-privilege, provenance, and failure guarantees remain normative.

## Actors and external systems

- The release owner selects one released RLS and initiates the workflow.
- The assurance and security owners review the RLS-bound evidence and protected channel configuration.
- GitHub Actions runs trusted-main resolution, unprivileged candidate qualification, GitHub release publication, PyPI promotion, Pages deployment, and observation jobs.
- GitHub Git data and Releases retain the tag and exact release assets.
- The protected `pypi` environment and PyPI Trusted Publisher authorize one OIDC job.
- The protected `github-pages` environment deploys derived demonstration content.
- Public PyPI and Pages endpoints provide post-publication observations.

## Inputs

The normal workflow accepts exactly one required string input, `release_record`, matching `^RLS-[A-Z0-9-]+-[0-9]{3}$`, and is manually dispatched from `refs/heads/main`. It accepts no version, tag, candidate, governance commit, filename, hash, latest-release selector, force, overwrite, or skip input.

A separate recovery entry point may accept the same RLS plus an explicit immutable governance commit only for a Pages-only replay. It cannot tag, create or change a GitHub Release, mint PyPI identity, or change the resolved distribution set.

## Outputs

- A deterministic result document with schema `se-harness-release-result/v1`.
- An immutable annotated tag resolving to the RLS candidate.
- One final GitHub Release containing exactly the wheel, normalized sdist, and `SHA256SUMS`.
- The same wheel and sdist on PyPI with metadata verification and attestations.
- One release-bound demonstration deployed from the immutable governance snapshot.
- A fresh public Python 3.11 installation observation and linked workflow summary.

## State model

1. **Selected:** one RLS ID is supplied on `main`.
2. **Resolved:** trusted main history proves the released record, candidate, VREC, contract, work, distribution block, and governance commit.
3. **Qualified:** two exact-candidate builds and required checks produce the declared bytes without credentials.
4. **GitHub staged:** exact tag and draft release state exist; assets are not yet public as a final release.
5. **GitHub published:** final release metadata and all three assets match.
6. **PyPI awaiting approval:** the least-privilege job waits on the protected environment.
7. **PyPI observed:** both public files and hashes either match or the version is classified partial/mismatched.
8. **Pages observed:** the immutable governance snapshot is deployed or a bounded replayable failure is retained.
9. **Reported:** stage-specific results and authority boundaries are emitted.

No aggregate status converts a partial outcome into success. GitHub package release, PyPI, and Pages stages retain separate results.

## Behavioral rules

1. Preserve `.github/workflows/publish-pypi.yml` as the top-level PyPI-trusted workflow identity and evolve its display name and jobs into the complete release orchestrator. PyPI does not currently accept a reusable workflow as the configured Trusted Publisher, so no reusable OIDC indirection is permitted.
2. The workflow exposes only `workflow_dispatch` for normal operation, runs only from `main`, uses full-SHA-pinned actions, and serializes by resolved version plus a global PyPI concurrency boundary without cancelling an active run.
3. Trusted resolution checks out full `main` history with persisted credentials disabled and uses main-owned code plus the selected independently released governor to validate the governance snapshot.
4. Resolution finds exactly one artifact ID, requires `type = "release_record"` and `status = "released"`, verifies it is present in first-parent main history, and derives the immutable governance commit that first integrated the released form.
5. The RLS candidate, object format, version, tag, release contract, included VRECs, and released work must satisfy the existing graph invariants. Each included VREC is verified or released and names the same candidate.
6. A distributable RLS contains a `[distribution]` block with `schema = 1`, `kind = "python-wheel-sdist"`, `source_date_epoch`, `wheel`, `wheel_sha256`, `sdist`, `sdist_sha256`, `checksums`, `checksums_sha256`, and `source_manifest_sha256`.
7. The wheel and sdist names are exact safe basenames derived from RLS version. The epoch equals the candidate commit timestamp. Every digest is 64 lowercase hexadecimal characters. `checksums` is exactly `SHA256SUMS`, whose LF-terminated two-line bytes are derived from the distribution hashes.
8. Candidate qualification produces a JSON manifest with schema `se-harness-release-bundle/v1`. `harnessctl prepare-release --distribution-manifest PATH` validates its version, commit, epoch, names, hashes, checksum bytes, and manifest digest before copying the distribution block into a ready RLS proposal. The transaction is all-or-none.
9. Historical RLS files without `[distribution]` remain valid. The new fields are optional at graph-schema level but mandatory for this orchestrator and for future SE Harness Python release work that declares public distribution.
10. Candidate source is exported by exact commit. Two independent no-isolation builds use the recorded epoch; both wheels and normalized sdists must be byte-identical, archive-safe, metadata-valid, and equal to the RLS hashes. The job runs the approved release verification matrix and emits one bounded artifact bundle.
11. The qualification job has no publication environment or write/OIDC/Pages permission. Subsequent credential-bearing jobs never checkout or execute candidate content; they consume transferred bytes only after independent hash checks.
12. GitHub publication creates an annotated tag only when absent. Its target, tag name, fixed message, tagger identity, and tagger timestamp derived from `released_at` are deterministic. An existing tag is accepted only when its peeled target equals the candidate.
13. The GitHub Release is first staged as draft, receives exactly the declared three assets, and is downloaded and verified before becoming a final non-prerelease release. Final exact state is replay-complete; any extra, partial, or mismatched state fails without replacement or deletion.
14. Release notes are deterministic and identify version, candidate commit, aggregate VREC, RLS, released work, and installation command. Generated latest-range notes are not authority and are not required for correctness.
15. The PyPI job remains in the top-level trusted workflow, runs under the `pypi` environment from `main`, has only `contents: read` and `id-token: write`, performs no checkout or build, and preserves every exact-asset control of `SPEC-PYP-001`.
16. Before invoking the publisher, query PyPI. No files means eligible; both exact expected files with exact hashes means replay-complete and the publisher is not invoked; one file, unexpected files, or any mismatch is blocking. This preflight reconciliation is not publisher-side `skip-existing`, which remains prohibited.
17. Pages generation and deployment run in the main-context orchestrator after final GitHub publication, preserving `SPEC-DPG-001` provenance and least privilege. The separate Pages workflow loses its automatic `release` trigger and remains a main-only explicit recovery path, preventing tag-ref environment rejection.
18. GitHub, PyPI, and Pages jobs have separate minimal permissions and stage results. Package publication may be complete while Pages is failed; Pages failure does not mutate or revoke the software release.
19. Post-publication checks compare remote GitHub and PyPI hashes, confirm attestations are exposed, create a fresh Python 3.11 environment, install the exact public version, run `harnessctl --version`, and verify the deployed Pages provenance manifest.
20. Every exit path writes as much bounded result state as is safely known and states that automation did not approve, verify, release, merge, or change any formal lifecycle state.

## Error and recovery behavior

| Observed state | Required behavior |
|---|---|
| No tag or release | create after qualification |
| Exact tag, no release | continue with draft staging |
| Exact draft and exact assets | verify and publish |
| Exact final GitHub Release | treat GitHub stage as complete |
| Mismatched tag or final asset | stop; no mutation |
| PyPI version absent | request protected promotion |
| Both PyPI files exact | treat PyPI stage as complete |
| PyPI partial or mismatched | stop and escalate |
| Pages failed or stale for the same identities | permit Pages-only replay |

Transient network or service failure may be retried only before an irreversible call or by rerunning the state reconciliation. Do not add unbounded retry loops, force flags, delete-and-recreate behavior, tag movement, final asset replacement, PyPI duplicate suppression, or candidate substitution.

## Data and interface contracts

The distribution block and bundle/result JSON schemas use UTF-8, deterministic key ordering when serialized, safe repository-relative or basename fields as specified, integer epochs, full lowercase object IDs and SHA-256 values, and no secret material. Job outputs transport resolved scalar identities; uploaded workflow artifacts transport bounded byte bundles and JSON results.

The current PyPI external identity remains repository `mmzen/se_harness`, workflow filename `publish-pypi.yml`, and environment `pypi`. Renaming or reusable-workflow substitution is outside this work because it requires a coordinated external publisher migration.

## Security and privacy properties

- Workflow and repository content, RLS text, Git objects, transferred artifacts, GitHub metadata, PyPI responses, and Pages files are untrusted inputs.
- Expression values enter shell only through environment variables and strict validation.
- Only the GitHub publication job receives `contents: write`; only the PyPI job receives OIDC; only the Pages deploy job receives Pages write/OIDC.
- Candidate code executes only before every credential boundary.
- Full action pins, protected environments, exact hashes, no stored PyPI secret, and no persistent checkout credential are mandatory.

## Performance and capacity

One release performs two builds and the repository's release verification matrix, then transfers one small wheel, sdist, checksum file, and result manifest. No cache is required for authority, and concurrency permits only one production PyPI transaction at a time.

## Observability

GitHub retains dispatch identity, job graph, environment review, release/tag/asset metadata, Pages deployment, logs, summaries, and result artifacts. PyPI exposes file hashes, metadata, attestations, and timestamps. The final result connects these observations to the RLS, VREC, candidate, and governance commit without becoming a formal record.

## Compatibility and migration

- Historical RLS files remain valid but cannot feed the new pipeline without the new structured block.
- Existing manual release and PyPI workflows remain usable until the orchestrator is verified; retirement or narrowing of a recovery path requires explicit evidence and review.
- Existing `pypi` and `github-pages` environment protections remain. The Pages automatic trigger changes to main-context orchestration plus manual recovery.
- No consumer template, runtime API, Python minimum, or installation behavior changes.

## Examples and counterexamples

- Valid: `release_record=RLS-SEH-008` on `main`, all other identities derived, exact prior tag accepted, missing final release completed.
- Invalid: dispatching a tag plus copied hashes, selecting the latest RLS, building from main instead of candidate, permitting a different output hash, or allowing a tag-ref Pages deployment.
- Valid replay: both PyPI files already exist with exact hashes, so public verification runs and no publisher upload is attempted.
- Invalid replay: only the wheel exists on PyPI, so the pipeline stops and retains partial-state diagnostics.

## Explicitly unspecified decisions

The implementation agent may choose bounded helper-module organization, JSON field ordering implementation, job and test names, release-summary wording, and temporary-directory layout. It may not change workflow identity, authority boundaries, required fields, exact state classifications, credential separation, immutable-state rules, or protected environment requirements.
