+++
id = "WO-DPG-001"
type = "work_order"
title = "Publish the SE Harness Explorer demonstration"
status = "implemented"
owners = ["engineering-owner", "quality-owner", "security-owner", "service-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[assurance]
commit_bound_verification = "required"
rationale = "Future public deployment and maintainer replay decisions rely on the correctness of release provenance resolution, executable CI, public-data boundaries, least-privilege policy, and generated demonstration behavior."
decided_by = "repository-owner"

[relations]
implements = ["REQ-DPG-001", "REQ-DPG-002", "REQ-DPG-003"]
specifications = ["SPEC-DPG-001"]
architecture = ["ARCH-DPG-001", "ADR-DPG-001"]
verification = ["VER-DPG-001"]
+++

# Work Order: Publish the SE Harness Explorer demonstration

## Lifecycle

The accountable repository owner approved this packet and instructed `go implement` on 2026-08-16. The bounded implementation and retained evidence are complete. Commit-bound verification is required before future decisions rely on the workflow. An actual GitHub Pages deployment remains a distinct external action and must not be inferred from work-order, VREC, or release state.

## Implementation result

The repository now contains a release-bound, repository-specific Pages workflow, a fail-closed provenance and payload helper, focused regression coverage, and operator documentation. The real v0.4.0 lineage resolves deterministically to candidate `2acc63af8933ee1dfa5ef78b67e2dbe6fb9a4e61` and governance commit `a702d187084ba72d2c8b8b61c66b2a1be5d6f403`. Independent released-governor validation, exact-payload packaging, complete tests, and manual local presentation review passed. Full commands, hashes, action pins, boundaries, and residual risks are retained in `docs/engineering/dashboard-publication/evidence/WO-DPG-001-verification.md`.

## Objective

Implement a repository-specific, release-bound GitHub Pages publication path that demonstrates SE Harness by exposing the canonical Explorer for the project's own completed governance graph, with exact dual provenance, safe static output, least privilege, reproducible replay, and no consumer-distribution impact.

## In scope

- Add one repository-specific GitHub Actions workflow for published-release handling and authorized manual replay.
- Implement a standard-library provenance resolver for released RLS selection, tag/candidate verification, main first-parent governance-commit resolution, and strict manual inputs.
- Validate the selected checkout with the independently released governor and generate the demonstration using the target-local canonical Explorer implementation.
- Add a bounded constant Pages-only demonstration/non-authority notice without introducing a second data model or accepting repository-controlled executable markup.
- Stage and validate an exact static payload, configure Pages, upload one Pages artifact, and deploy through the protected `github-pages` environment.
- Pin official actions to reviewed immutable commits, scope permissions by job, serialize deployment, and report provenance, hashes, run identity, and URL.
- Add deterministic Git-history, workflow-policy, security, payload, regression, and failure tests plus retained work-order evidence.
- Update repository-specific operator documentation or the root README only where a concise demonstration link or replay instruction is required.

## Out of scope

- Adding any Pages workflow, file, setting, or contract to `templates/repository/standard/` or installed consumer repositories.
- Changing `harnessctl dashboard`, `harness-dashboard-snapshot-v1`, the canonical Explorer's artifact semantics, validator rules, VREC/RLS authority, package contents, or self-hosting governor selection solely for publication.
- Creating a hosted API, multi-repository dashboard service, analytics, telemetry, database, custom domain, per-release archive, availability SLA, or runtime dependency beyond the exact existing CDN exception.
- Committing generated output, creating or rewriting `gh-pages`, modifying release tags or GitHub Releases, publishing Python packages, or promoting a governor.
- Actually dispatching a Pages deployment before separate authorization to change public external state.

## Authorized decision envelope

The implementation agent may choose the workflow and helper filenames, bounded history-query implementation, unit-fixture layout, constant notice placement, staging-directory name, and concise job-summary format. It may select current official Pages action releases only when pinned to reviewed full commits and documented in evidence.

The agent may not resolve ambiguity by choosing the newest branch head, use a short or unreachable commit, weaken released-record/tag/candidate checks, run the candidate validator as its own governor, publish unexpected files, broaden permissions or browser network access, alter consumer-managed files, infer formal authority, or perform the public deployment without explicit authorization.

## Constraints

- Preserve Python 3.11+ standard-library repository behavior.
- Keep released-governor validation separate from target-local dashboard generation.
- Treat event data, Git references, repository content, generated paths, action metadata, and environment output as untrusted.
- Preserve all requirements and accepted residual risk in `SPEC-DST-008` and `ADR-DST-008`.
- Keep root and standard-template managed parity unchanged unless an independently governed defect is found.
- Preserve unrelated user changes and historical formal records.
- Do not build or publish a promotable Python distribution under this work order.

## Expected change surface

Repository-specific GitHub workflow configuration; a repository-specific provenance/publication helper; focused tests and fixtures; concise operator or demonstration documentation; the dashboard-publication domain index; and `WO-DPG-001` retained evidence. Standard consumer templates, package manifests, managed locks, CLI modules, and canonical Explorer assets should remain unchanged.

## Required verification

Execute every check in `VER-DPG-001`. At minimum run formal graph validation, start/review preflight, released-governor CI, focused provenance and workflow-policy tests, dashboard determinism and hostile-input regressions, full standard-library tests, exact payload inspection, consumer-template and package-diff checks, YAML/static action-pin review, `harnessctl doctor`, local link checks, and `git diff --check`. Record actual Pages deployment review only after separately authorized execution.

## Evidence to record

Retain exact commands and exit codes, Python and governor identities, changed paths, test counts, synthetic Git histories, automatic and replay inputs, selected RLS/candidate/governance values, snapshot and dashboard hashes, action release-to-pin mapping, permissions, concurrency and environment review, payload inventory, security cases, consumer isolation, manual UI review, deviations, residual risks, and later deployment run/URL if authorized in `docs/engineering/dashboard-publication/evidence/WO-DPG-001-verification.md`.

## Stop and escalate conditions

Stop if a release cannot resolve uniquely; the governance commit is mutable or not main-reachable; the tag and candidate differ; independent governor validation fails; target-local generation is needed for governance authority; public content exceeds the canonical dashboard boundary; a second schema or broader network dependency appears necessary; Pages requires broader permissions or generated Git commits; consumer-managed files would change; action provenance cannot be reviewed; tests fail; or implementation requires release, tag, package, governor-promotion, repository-settings, or public-deployment authority not explicitly granted.

## Completion report format

Report requirement mapping, automatic and replay flow, provenance algorithm, validation/generation separation, public-data and authority boundaries, workflow permissions and action pins, implementation paths, tests and generated hashes, consumer isolation, deployment status, deviations, residual risks, and the exact candidate path set.
