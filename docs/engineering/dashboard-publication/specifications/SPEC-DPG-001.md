+++
id = "SPEC-DPG-001"
type = "specification"
title = "Release dashboard Pages publication contract"
status = "implemented"
owners = ["technical-owner", "release-owner", "security-owner", "service-owner"]
created = "2026-08-16"
updated = "2026-08-18"

[relations]
specifies = ["REQ-DPG-001", "REQ-DPG-002", "REQ-DPG-003"]
+++

# Specification: Release dashboard Pages publication contract

## Scope

Publish the SE Harness development repository's canonical Explorer to GitHub Pages after a completed release. Normal publication is a main-context stage of the released-record orchestrator; the repository-specific Pages workflow remains an accountable main-only recovery path. Preserve the existing Explorer model, generator, security boundary, and non-authoritative semantics.

This contract does not add a Pages workflow to `templates/repository/standard/`, modify consumer installation or upgrade, create a hosted multi-repository service, or alter formal governance transitions.

## Actors and external systems

- The release owner completes the formal release decision and publishes a GitHub Release.
- A repository maintainer may request a controlled replay.
- GitHub Actions supplies an isolated runner, repository history, event identity, and workflow logs.
- GitHub Pages artifact upload and deployment actions publish the static site through the protected `github-pages` environment.
- Visitors consume a read-only promotional demonstration.
- The exact optional unpkg dependency already accepted by `ADR-DST-008` supplies only the 3D renderer at browser runtime.

## Inputs

Normal publication receives the released-record orchestrator's trusted plan. Manual replay receives a release-record ID and full governance commit and derives the tag from the record. All values are data, not command fragments, and must pass strict format and repository-identity checks.

The resolver may read full default-branch first-parent Git history, formal release records, the selected Git tag, `.engineering-harness.toml`, the released-governor descriptor, and canonical dashboard inputs. It must not use a mutable branch head as the published identity.

## Outputs

- One Pages artifact containing only the reviewed static payload.
- One GitHub Pages deployment for the `github-pages` environment.
- A workflow summary containing release tag, version, release record, candidate commit, governance commit, snapshot SHA-256, dashboard SHA-256, action run, and deployed URL.
- A deterministic `publication-manifest.json` binding the public payload to its release, candidate, governance commit, canonical snapshot hash, generated-dashboard hash, and published-dashboard hash.
- Failed-run diagnostics that do not imply successful publication.

Generated files are deployment artifacts only. They are not committed to any Git branch and are not formal SE Harness evidence or authority.

## State model

```text
requested
  -> release-resolved
  -> governance-commit-resolved
  -> provenance-validated
  -> repository-validated
  -> dashboard-generated
  -> payload-validated
  -> pages-artifact-uploaded
  -> deployed
```

Every transition before `deployed` may fail closed. A failed replacement leaves the previous successful Pages deployment unchanged. Workflow state does not transition any formal artifact.

## Behavioral rules

1. The workflow is repository-specific and is not included in the managed standard template, managed lock, installer, adopter, upgrader, or governor reconciliation surface.
2. Normal publication runs as a main-context job after the orchestrator verifies a final GitHub Release in `mmzen/se_harness`; manual replay uses a separate main-only `workflow_dispatch` with one RLS ID and an explicit governance commit. A tag-ref `release` event is not a Pages deployment trigger.
3. The resolver selects exactly one formal `release_record` whose `status` is `released` and derives the GitHub Release tag from it. Zero or multiple matches fail.
4. The Git tag must resolve, including annotated-tag peeling, to the full candidate commit recorded by the release record using its declared object format. The version and release identity must also agree.
5. The normal governance commit is the unique first-parent commit on the default integration history where the matching release record first appears in `released` state while its first parent does not contain that released state. The result must be immutable, full length, and reachable from the default branch.
6. A manual governance commit must be full length, reachable from the default branch, contain the matching released record, and satisfy the same tag, candidate, version, and validation checks. A replay cannot select arbitrary branch content.
7. Generation occurs in a clean detached checkout of the resolved governance commit. The released independent governor validates the formal graph; the checked-out target-local generator produces the demonstration and grants no authority.
8. `harnessctl dashboard` or the equivalent managed generator writes to a new empty staging directory. Generation failure or nonzero validation exits stop publication.
9. The payload allowlist is exactly `index.html`, `dashboard-data.json`, `generation-summary.json`, and `publication-manifest.json`. Symlinks, traversal paths, hidden credentials, archives, source files, and unexpected files are rejected.
10. The snapshot schema must be `harness-dashboard-snapshot-v1`. The packaging step may add only a constant demonstration notice to `index.html`; it updates the non-canonical generation summary and publication manifest so the generated and published dashboard hashes, canonical snapshot hash, and selected governance provenance remain separately inspectable and consistent.
11. The page identifies itself as the public demonstration of SE Harness governing its own development and states that it is derived, read-only, and non-authoritative.
12. Existing `SPEC-DST-008` semantic, deterministic, hostile-input, CSP, accessibility, bounded-rendering, and optional-CDN fallback obligations remain unchanged.
13. Workflow-wide default permissions are `contents: read`. Only the deployment job receives `pages: write` and `id-token: write`; no job receives contents write, pull-request write, release write, package write, or secrets beyond platform-issued tokens needed for Pages.
14. Official checkout, Python setup, Pages configuration, Pages artifact upload, and Pages deployment actions are pinned to reviewed full commit SHAs. The corresponding upstream release names are documented beside pins and covered by dependency review.
15. Deployments use a repository-specific concurrency group. A later request waits rather than cancelling an in-progress Pages deployment.
16. Upload and deployment use the protected `github-pages` environment and surface the deployment URL through the environment and workflow summary.
17. The workflow never commits, pushes, tags, edits a GitHub Release, changes Pages settings, transitions an artifact, publishes a Python distribution, promotes the self-hosting governor, or deploys consumer repositories.
18. Repeating the same release and governance inputs must reproduce the canonical snapshot hash. A differing hash blocks replay unless the governed source or generator identity differs and a new authorized input explains that change.

## Error and recovery behavior

Each resolution and validation failure names the failed invariant without exposing tokens or unnecessary file content. Upload and deployment errors remain GitHub workflow failures. Recovery is an authorized replay after correcting platform availability or a new governed repository candidate after correcting source behavior. The workflow does not rewrite history or mutate the failed release to recover.

## Data and interface contracts

The generated interface remains `harness-dashboard-snapshot-v1` plus `generation-summary.json` and the rendered `index.html` defined by `SPEC-DST-008`. `publication-manifest.json` is deployment attestation metadata, not a formal artifact or second dashboard model. Workflow inputs use validated identifiers and full Git object IDs. Workflow outputs use GitHub's job summary and Pages deployment URL; no new formal artifact schema or dashboard schema is introduced.

## Security and privacy properties

- Treat release names, tags, artifact prose, paths, repository data, and manual inputs as untrusted.
- Avoid shell interpolation of event text; pass validated values through bounded arguments or environment variables.
- Publish only data already intended for the public SE Harness repository and present in the canonical Explorer output.
- Keep credentials outside the Pages artifact and redact them from logs.
- Use least-privilege job permissions, immutable action pins, the Pages environment, output allowlisting, safe generation, and the existing narrow CSP.
- Retain the CDN residual risk and exact network exception from `ADR-DST-008`; do not expand it.

## Performance and capacity

One deployment per selected release is expected, with occasional replay. The existing generator's bounded behavior applies. Artifact retention follows GitHub platform policy; the live site holds only the latest successful deployment. No high-frequency trigger, persistent server, database, or paid runtime is introduced.

## Observability

The Actions run, Pages deployment environment, generated summary, hashes, selected commits, selected release record, and deployment URL form the operational observation set. The workflow should emit concise step summaries and preserve platform logs according to repository retention policy.

## Compatibility and migration

The feature is additive to this repository. It does not modify `.engineering-harness.toml`, the self-hosting governor descriptor, standard template manifests, consumer workflows, package contents, CLI behavior, or existing release records. Disabling the repository-specific workflow stops future promotion-site updates without affecting released packages or formal evidence.

## Examples and counterexamples

For `v0.4.0`, the candidate commit is `2acc63af8933ee1dfa5ef78b67e2dbe6fb9a4e61`, while the governance snapshot containing released `RLS-SEH-006` is later in main history. A correct deployment reports and validates both identities.

Checking out only `v0.4.0` is incorrect because it omits the later release decision. Generating from the current moving `main` head is incorrect because it may include work unrelated to 0.4.0. Committing `_site` to `gh-pages` is incorrect because generated demonstration output must remain an external deployment artifact.

## Explicitly unspecified decisions

The implementation agent may choose a standard-library helper layout, test fixtures, staging-directory name, concise workflow/job names, and the exact formatting of the visible demonstration notice. It may not weaken unique provenance resolution, action pinning, permission boundaries, payload allowlisting, non-authoritative labeling, or consumer isolation.
