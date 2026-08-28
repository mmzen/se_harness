+++
id = "SPEC-CIP-001"
type = "specification"
title = "Triggers, artifact handoff, the reusable qualification, release-unit derivation, predecessor derivation, and the documentation each increment owes"
status = "approved"
owners = ["technical-owner", "release-owner"]
created = "2026-08-26"
updated = "2026-08-26"

[relations]
specifies = ["REQ-CIP-001", "REQ-CIP-002", "REQ-CIP-003", "REQ-CIP-004", "REQ-CIP-005", "REQ-CIP-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-26T15:17:28Z"
decided_by = "technical-owner"
+++

# Specification: Triggers, artifact handoff, the reusable qualification, release-unit derivation, predecessor derivation, and the documentation each increment owes

## Scope

Binds the four work orders of this domain. Rule identifiers `CIP-xxx-nnn`
are referenced by the verification contract and the evidence.

## Triggers and concurrency (CIP-TRG)

1. `candidate-evidence.yml`, `predecessor-evaluator-assessment.yml` and the
   template `engineering-harness.yml` declare
   `push: branches: [main, "release/**", "candidate/**"]` and
   `pull_request:` with no filter.
2. Each declares `concurrency: {group: "<workflow>-${{ github.ref }}",
   cancel-in-progress: true}`. `publish-pypi.yml`,
   `release-candidate-replay.yml` and `publish-dashboard-pages.yml` keep
   `cancel-in-progress: false`.
3. Jobs whose result only counts on the pull-request event keep their
   condition; the notes say which.

## Artifact handoff (CIP-ART)

1. `candidate-source` produces `candidate-wheel-<sha>` containing the wheel
   and `SHA256SUMS`, built from `git archive` with `build==1.2.2.post1`,
   `setuptools==75.8.0`, `wheel==0.45.1`, `SOURCE_DATE_EPOCH` = commit time.
2. Every consumer downloads it and runs `sha256sum -c SHA256SUMS` (or the
   pwsh equivalent) before use. No consumer contains `pip wheel` or
   `python -m build`.
3. `governance-migration` runs the scenario once per platform and outputs
   `semantic_sha256`; a final step of the matrix's dependent job compares
   the two outputs. `governance-migration-reconcile` is removed.
4. `integration-package-retain` is removed; the verify job uploads the
   retention artifact after a successful verify on both platforms.
5. Target job list: `candidate-source`, `candidate-package`,
   `governance-migration[Linux,Windows]`, `integration-package[build,
   verify Linux, verify Windows]` with the retention upload in verify.

## Reusable qualification (CIP-QLF)

1. `.github/workflows/release-qualification.yml` with `on: workflow_call`,
   inputs `mode` (`candidate` | `release-record`), `release_record`
   (string, optional), `platform` (`Linux` | `Windows`); `permissions:
   contents: read`; no secrets input.
2. Steps, in order: checkout at the resolved candidate; pinned build tools;
   export; `qualify complete-candidate`; `unittest discover`; CLI smoke;
   `python -m build` twice; `normalize_sdist.py`; byte comparison; bundle
   assembly; `create_release_bundle_manifest.py`; `publish_release.py
   verify-build-manifest`; `publish_release.py verify-bundle`; upload
   `release-bundle-<id>`.
3. `publication-rehearsal.yml` calls it in both modes on both platforms;
   `publish-pypi.yml`'s `qualify` job calls it with `mode: release-record`
   on the platform the schema requires.
4. Removed: `rehearse_publication.py`, `publication_rehearsal_mechanics.json`,
   the `divergence` job, the PyYAML install.
5. Scripts: `build_integration_package.py`, `publish_release.py`,
   `publish_dashboard.py`, `reconcile_maintenance_branch.py` import
   `se_harness.workflow_contract.canonical_json_bytes`, the package's
   duplicate-key JSON loader and `sha256_file` helper (added to
   `repository_tools` if absent). `reconcile_maintenance_branch.py` calls
   `gh api`. `classify-pypi` is called by the `pypi` job or deleted.

## Schema leg and Pages (CIP-LEG)

1. `qualify` has no matrix; the platform is `needs.resolve.outputs.
   distribution_schema == '2' && 'ubuntu-latest'`; the schema-1 leg is
   deleted with a note in the release sequences.
2. `.github/workflows/pages-publication.yml` (`workflow_call`) holds
   `pages_build` and `pages_deploy`; `publish-pypi.yml` and
   `publish-dashboard-pages.yml` call it.

## Release unit (CIP-RLU)

1. `RELEASE_CONTRACT.template.md` adds `candidate_commit = "<40 or 64 hex>"`
   and `previous_release_tag = "v<version>"` in the front matter, and a
   "Release unit" section that states the census is derived.
2. `harnessctl release-unit <root> --from <tag> --to <commit> [--json]`
   (the `[--result-schema 2]` once written here named an option
   `release-unit` never had; corrected 2026-08-28 under `WO-ECP-005`): walks `--first-parent <tag>..<commit>`, reads the
   `Harness-Work-Order:` trailer of each commit, resolves each work order
   in the catalog, reports `{id, status, packaged_surface: bool,
   commits: [..]}` per work order and `untraced: [sha..]`; exit 1 when
   `untraced` is non-empty or any listed work order is not `implemented`.
3. The 0.6.0 root validator does not know the new fields; they are
   repository-owned data on a repository-owned artifact type and validate
   as unknown keys today. The candidate validator gains `E-CIP-001`: a
   contract in `approved` whose `gates` differs from the derivation.
4. The stop-condition prose in the template replaces "a work order
   reaching implemented after this timestamp" with "the candidate commit
   is not an ancestor of the released ref, or the derived census differs
   from `gates`".

## Predecessor derivation (CIP-PRE)

1. Step `derive-predecessor` reads `.engineering-harness.toml` (version),
   `.engineering-harness.lock` (source wheel digest) and resolves
   `tests/fixtures/governance_migration/candidate-<pred>-to-<cand>.json`;
   exports `version`, `wheel_sha256`, `scenario`.
2. `python -m repository_tools.governance_migration write-scenario
   --predecessor <v> --successor <v>` writes the fixture with the canonical
   writer.
3. Grep gate in tests: no `0\.[0-9]+\.[0-9]+` literal and no 64-hex literal
   in the repository-owned workflows outside the derivation step.

## Documentation (CIP-DOC)

Each work order updates, in the same change:

1. `docs/notes/ci-pipeline.md`: the baseline table and the "after" figures
   for the increment.
2. `docs/notes/developing-se-harness.md`: "Ordinary development checks",
   "Evaluator and candidate evidence", "Release sequences" and "Advancing
   the root evaluator" as affected.
3. `docs/notes/harnessctl-reference.md` for `release-unit` and the scenario
   writer; `docs/notes/README.md` when a note is added.
4. Every workflow's header comment names its purpose, its trigger policy,
   and the note section that describes it.

## Failure behaviour

A work order that leaves a duplicated build, a digest declaration, a
version literal or an idle matrix leg in its scope fails its own
acceptance; the evidence lists the grep commands that prove absence.
