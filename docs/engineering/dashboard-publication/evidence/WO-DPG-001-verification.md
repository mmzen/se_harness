# Verification Evidence: WO-DPG-001

## Scope and authority

This evidence supports `WO-DPG-001`, `REQ-DPG-001` through `REQ-DPG-003`, and `VER-DPG-001`. The repository owner approved the packet and instructed `go implement` on 2026-08-16. Start and review preflight passed.

This file records implementation evidence only. It does not verify the work, authorize a candidate commit, prepare or approve a VREC, release software, publish a package, change repository settings, or deploy GitHub Pages. The public deployment remains a separate external action.

## Delivered behavior

- Added a repository-specific workflow for a published GitHub Release and for an exact, accountable manual replay.
- Added a standard-library resolver that requires one released RLS, verifies the release tag against its candidate commit, and selects the first main-history governance commit that integrated that released record.
- Kept the two revision identities explicit: the candidate is the released software payload; the later governance commit is the immutable graph snapshot shown by the demonstration.
- Used the checksum-pinned released governor from the selected governance checkout for independent validation, then used that checkout's target-local generator only to render its canonical Explorer.
- Added an exact four-file public payload gate: `index.html`, `dashboard-data.json`, `generation-summary.json`, and `publication-manifest.json`.
- Added a constant visible notice identifying the site as a derived, read-only SE Harness development demonstration with no formal authority.
- Split build and deployment permissions. Only the deployment job receives `pages: write` and `id-token: write`; the protected `github-pages` environment records the deployment URL.
- Serialized deployments without cancelling a run already in progress and retained replay inputs, provenance, and hashes in job summaries.
- Kept the workflow, helper, and documentation out of `templates/repository/standard/`; consumer installation, upgrade, CLI behavior, managed locks, package data, and self-hosting controls are unchanged.
- Retained `OPS-DPG-001` as `draft`: completed implementation alone cannot activate an operating-assurance claim before a verified or released VREC covers the work.

## Real v0.4.0 replay

The resolver ran against the real repository and selected:

| Field | Value |
| --- | --- |
| repository | `mmzen/se_harness` |
| release tag and version | `v0.4.0`, `0.4.0` |
| release record | `RLS-SEH-006` at `docs/engineering/release-0.4.0/releases/RLS-SEH-006.md` |
| candidate commit | `2acc63af8933ee1dfa5ef78b67e2dbe6fb9a4e61` |
| governance commit | `a702d187084ba72d2c8b8b61c66b2a1be5d6f403` |
| Git object format | `sha1` |

The governance checkout was clean and detached. Its released governor descriptor selected SE Harness `0.3.0` with wheel SHA-256 `260e22371b05e5bb6c59143a1f0229855305a6bf7994984be50aa147a02ea516`. The wheel was downloaded from its exact GitHub Release boundary, checksum-verified, installed without dependencies in an isolated virtual environment, and passed the governor identity check. That released governor validated 379 artifacts with zero errors and 42 existing maintenance warnings.

Target-local generation then produced 379 artifacts and 1,401 relations with zero errors and 42 warnings. The exact packaged output contained only four regular files and no symlinks:

| Output | SHA-256 |
| --- | --- |
| canonical snapshot | `bfaf90205a959e36629387813ebe41ae60e1522d6b4e0ea159249021218c2bbd` |
| generated canonical `index.html` | `155c7480bd557145bbf741c1612257491f42b243ce52ed6a4fb943acb78a202a` |
| published notice-bearing `index.html` | `3c4cd5dad3e8de74875ca866a2b23642404ab1e7989915e38d99a245fe8454db` |
| packaged `generation-summary.json` | `131ddc32ea4e63806055123b8ae7a9d1fe3a9becdc0064dfb58ef4bbe60b322e` |

Repeated packaging from identical inputs produced identical files and manifest values. The canonical snapshot was not rewritten by publication packaging.

## Verification results

| Check | Result |
| --- | --- |
| focused publication tests | PASS; 16 tests |
| complete Python suite | PASS; 217 tests with 3 expected platform-dependent skips |
| formal graph validation after implementation completion | PASS; 390 artifacts, zero errors, 42 pre-existing maintenance warnings |
| `python -m se_harness doctor .` | PASS; required files, managed parity, lock, and self-hosting governor checks passed |
| review preflight | PASS for approved `WO-DPG-001`, with commit-bound verification required |
| real v0.4.0 provenance resolution | PASS; exact values reported above |
| independent released-governor validation | PASS; version, root, isolation, entry point, checkout, and wheel digest proved |
| exact payload and security gate | PASS; four regular files, no symlink, path escape, mismatch, hidden file, or unexpected file accepted |
| deterministic generation and packaging | PASS; byte-stable snapshot and manifest for identical inputs |
| consumer and package isolation | PASS; no diff under `templates/repository/standard/`, `pyproject.toml`, `.engineering-harness.toml`, or `.github/workflows/engineering-harness.yml` |
| documentation link coverage | PASS as part of the complete `test_public_onboarding` suite |
| diff hygiene | PASS; no whitespace errors, with only Git's existing LF-to-CRLF notices |

Synthetic Git fixtures cover annotated tags, candidate mismatch, missing and duplicate released records, later unrelated main commits, full versus abbreviated replay commits, record relocation in later history, and deterministic first-parent integration selection. Payload tests cover an altered generated hash, unexpected files, repeated packaging, the visible constant notice, and GitHub Release draft/prerelease/tag rejection. Workflow policy tests cover both triggers, repository and main guards, immutable pins, least privilege, non-cancelling concurrency, protected environment use, released-governor separation, and absence from the consumer template.

## Workflow supply-chain and authority review

The workflow pins reviewed official releases to full commits:

- `actions/checkout` v7.0.1: `3d3c42e5aac5ba805825da76410c181273ba90b1`
- `actions/setup-python` v7.0.0: `5fda3b95a4ea91299a34e894583c3862153e4b97`
- `actions/configure-pages` v6.0.0: `45bfe0192ca1faeb007ade9deae92b16b8254a0d`
- `actions/upload-pages-artifact` v5.0.0: `fc324d3547104276b827a68afc52ff2a11cc49c9`
- `actions/deploy-pages` v5.0.0: `cd2ce8fcbc39b97be8ca5fce6e763baed58fa128`

The build job has only `contents: read`. The deploy job has `contents: read`, `pages: write`, and `id-token: write`. Checkout credentials are not persisted. Event and manual inputs are passed through environment variables and argument arrays, validated as bounded identifiers, and never evaluated as shell syntax. No step commits, pushes, creates a tag or release, edits formal artifacts, publishes a Python distribution, or creates a `gh-pages` branch.

## Manual presentation review

The packaged site was served locally and reviewed at desktop and 390-by-844 narrow width. Overview, Lineage, and Readiness navigation rendered correctly; the demonstration/non-authority notice remained visible; release, candidate, and governance provenance were understandable; the narrow layout had no horizontal overflow; and browser inspection reported no errors. The notice did not overlap the main content. The canonical keyboard and non-color behavior remain covered by the existing Explorer tests.

An actual GitHub Pages run was deliberately not performed. Consequently, the deployed URL, protected-environment approval behavior, GitHub-hosted artifact transfer, and blocked-unpkg behavior remain deployment-time manual checks.

## Changed paths attributable to DPG-001

- `.github/scripts/publish_dashboard.py`
- `.github/workflows/publish-dashboard-pages.yml`
- `tests/test_dashboard_publication.py`
- the DPG-001 engineering packet and this retained evidence
- `docs/notes/harness-dashboard-publication.md`
- the concise documentation indexes and root README demonstration link

## Deviations and residual risks

- No action YAML parser was installed locally. Focused static policy tests and manual semantic review passed; GitHub Actions remains the final platform parser after merge.
- Local and fixture tests cannot prove continued GitHub Actions, Pages, GitHub Release API, GitHub-hosted runner, or unpkg availability, nor exclude an upstream service compromise.
- The optional pinned unpkg 3D runtime remains the already accepted `ADR-DST-008` risk. Non-3D views and the underlying public JSON remain available without it.
- The workflow becomes operational only after the candidate is reviewed, committed, verified, merged to the default branch, and separately dispatched for the already-published v0.4.0 demonstration or triggered by a later published release.
- A green deployment is operational evidence only. It cannot verify a VREC, release an RLS, or grant assurance authority.
