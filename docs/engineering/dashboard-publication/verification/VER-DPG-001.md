+++
id = "VER-DPG-001"
type = "verification"
title = "Verify release-bound Pages demonstration"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
verifies = ["REQ-DPG-001", "REQ-DPG-002", "REQ-DPG-003"]
+++

# Verification Contract: Verify release-bound Pages demonstration

## Independence

Expected provenance comes from formal release-record fields, Git object semantics, main first-parent history, the released-governor boundary, the canonical Explorer contract, and GitHub Pages permission requirements. Tests must not derive correctness from the resolver or workflow implementation being tested. Deployment review is performed by an accountable reviewer who did not infer release authority from a green Actions run.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-DPG-001` | Git-history fixtures, formal validation, generation, and provenance comparison | completed release, annotated tag, later main commits, zero/multiple RLS matches, candidate mismatch, unreachable or abbreviated replay commit | exactly one immutable governance snapshot is selected; released RLS, tag, candidate, version, object format, reachability, validation, and generated provenance agree or publication fails before upload |
| `REQ-DPG-002` | payload inspection, hostile-input regression, semantic review, and consumer-parity checks | canonical output, public demonstration notice, malformed schema, unexpected file, blocked CDN, consumer standard template | output preserves Explorer meaning and fallback, is visibly derived/non-authoritative, contains only allowed public static files, and changes no consumer-managed surface |
| `REQ-DPG-003` | workflow policy tests, pin review, replay test, concurrency inspection, and controlled deployment review | automatic event, manual replay, overlapping requests, upload/deploy failure, protected environment | permissions are least privilege, actions are immutable, deployments serialize without mid-run cancellation, provenance is observable, replay is idempotent, and no Git output branch or formal mutation occurs |

## Acceptance scenarios

- Resolve a synthetic main history where the candidate tag predates a merge commit that first contains the released record; select the merge governance commit, not the tag or current head.
- Resolve `v0.4.0` and `RLS-SEH-006` from the real repository and report candidate `2acc63af8933ee1dfa5ef78b67e2dbe6fb9a4e61` separately from the governance commit.
- Leave unrelated commits after the release integration and prove they do not enter the selected snapshot.
- Reject a ready, draft, superseded, missing, duplicate, malformed, or candidate-mismatched release record.
- Reject a manual short SHA, non-main commit, dirty generation state, invalid graph, unexpected staged file, symlink, or mismatched generated hash.
- Generate twice from identical inputs and compare canonical snapshot hashes.
- Block the optional CDN and confirm the published output retains the non-3D views required by `VER-DST-008`.
- Replay the same approved immutable inputs and compare the selected identities and snapshot hash.

## Property and invariant tests

- Provenance resolution is deterministic for the same Git graph and release tag.
- The selected governance commit is full length, immutable, main-reachable, and contains the exact matching released record.
- Tag peeling produces exactly the release record's candidate object ID.
- No current branch head, timestamp, directory enumeration order, or later unrelated commit changes the selected snapshot.
- The upload manifest is exactly `index.html`, `dashboard-data.json`, `generation-summary.json`, and `publication-manifest.json`, not a prefix or extension heuristic.
- No deployment success can modify or infer an artifact lifecycle state.
- Repeated generation from the same checkout produces identical `dashboard-data.json` bytes and SHA-256.

## Static and architecture checks

- The repository-specific workflow handles `release.published` and bounded `workflow_dispatch` replay.
- Workflow default permissions are read-only; only deployment has `pages: write` and `id-token: write`.
- The deployment uses `github-pages`, declares the resulting URL, and uses a non-cancelling concurrency policy.
- Every third-party action reference is a reviewed full commit SHA with its upstream version documented.
- No push, commit, tag, release edit, package publication, settings mutation, `gh-pages` branch, or consumer-template copy exists.
- The released governor performs validation and target-local code performs only post-release generation.
- The architecture relation includes `ARCH-DPG-001` and `ADR-DPG-001`; `ADR-DST-008` remains unchanged and unbroadened.

## Security and privacy checks

Use malicious release names, tags, manual inputs, artifact titles, paths, and generated-file names to test command-injection resistance, traversal rejection, safe logging, HTML safety, and exact payload allowlisting. Inspect the final tar payload or upload directory for tokens, Git metadata, source files, distributions, retained evidence bodies not present in the canonical snapshot, symlinks, and unexpected hidden files.

Review workflow permission scopes, environment use, immutable action pins, checkout persistence, credential cleanup, and the exact browser CSP/network boundary. Confirm that no event-controlled text is evaluated as shell syntax and that public deployment grants no access to private data or repository mutation.

## Performance and resilience checks

Exercise bounded histories with later commits, merge commits, duplicate candidate references, and a representative repository graph. Confirm timeouts and clear failures for unavailable governor distribution, validation, generation, upload, and deployment. Verify that a failed replacement does not intentionally delete or overwrite the last successful site and that an authorized replay can recover.

## Manual assessments

An accountable reviewer opens the deployed desktop and narrow-width site, confirms that it is recognizably the canonical Explorer, that the demonstration/non-authority notice is visible, and that release, candidate, and governance provenance are understandable. The reviewer checks Overview, Lineage, Readiness, keyboard navigation, non-color meaning, blocked-CDN fallback, Pages URL, Actions summary, and the absence of edit or approval controls.

Actual Pages deployment is an external action distinct from commit-bound verification. Record it only after separately authorized execution; static workflow and local payload verification must remain sufficient to assess the candidate implementation before merge.

## Evidence retention

Retain exact commands, runtimes, fixture histories, selected object IDs, release-record fields, validator identity, test counts, generated file inventory, snapshot and dashboard hashes, workflow permission and action-pin review, hostile inputs, consumer-template diff, browser observations, deployment run and URL when executed, failures, deviations, and residual risks under `docs/engineering/dashboard-publication/evidence/WO-DPG-001-verification.md`.

## Residual uncertainty

Local and fixture tests cannot prove continued GitHub Actions, Pages, or unpkg availability or exclude upstream service compromise. A successful test deployment does not establish an uptime SLO or independent assurance over GitHub. Immutable pins, least privilege, fail-closed provenance, a retained previous deployment, replay, and the existing non-3D fallback bound these risks.
