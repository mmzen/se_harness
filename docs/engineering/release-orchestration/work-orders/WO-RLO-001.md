+++
id = "WO-RLO-001"
type = "work_order"
title = "Implement deterministic released-record publication"
status = "implemented"
owners = ["engineering-owner", "release-owner", "quality-owner", "security-owner"]
created = "2026-08-18"
updated = "2026-08-18"

[assurance]
commit_bound_verification = "required"
rationale = "Future release, publication, operational, and security decisions will rely on changed release-record schema, trusted workflow identity, executable orchestration, credential boundaries, and recovery semantics."
decided_by = "repository-owner"

[relations]
implements = ["REQ-RLO-001", "REQ-RLO-002", "REQ-RLO-003", "REQ-RLO-004", "REQ-RLO-005", "REQ-RLO-006", "REQ-RLO-007", "REQ-RLO-008", "REQ-PYP-001", "REQ-PYP-002", "REQ-PYP-003", "REQ-PYP-004", "REQ-PYP-005", "REQ-DPG-001", "REQ-DPG-002", "REQ-DPG-003"]
specifications = ["SPEC-RLO-001", "SPEC-PYP-001", "SPEC-DPG-001"]
verification = ["VER-RLO-001", "VER-PYP-001", "VER-DPG-001"]
architecture = ["ARCH-RLO-001", "ADR-RLO-001", "ARCH-PYP-001", "ADR-PYP-001", "ARCH-DPG-001", "ADR-DPG-001"]
+++

# Work Order: Implement deterministic released-record publication

## Lifecycle

On 2026-08-18, after reviewing the complete RLO definition and architecture decision, the accountable repository owner stated `ok, go implement`. `WO-RLO-001` is therefore `in_progress` and authorizes only the bounded implementation below. It does not authorize a commit, push, pull request, VREC transition, RLS preparation or transition, tag, GitHub Release, PyPI upload, Pages deployment, environment approval, external publisher change, or governor promotion.

After bounded implementation and evidence, transition only to `implemented`. Because commit-bound assurance is required, later release or operational reliance requires a separate clean candidate commit, aggregate `VREC-RLO-*` proposal, accountable verification decision, and governance commit.

On 2026-08-18 the bounded implementation and retained evidence completed with both the repository-default and Python 3.11 suites green. `WO-RLO-001` transitioned to `implemented`; this records completed work, not correctness or independent assurance. No commit, push, pull request, VREC, RLS, tag, GitHub Release, PyPI upload, Pages deployment, environment approval, external publisher change, or governor promotion was performed.

## Objective

Replace the manually composed post-RLS release sequence with one repository-specific, main-only, released-record-driven orchestration that preserves deterministic bytes, exact provenance, protected PyPI and Pages boundaries, safe replay, and stage-specific evidence.

## In scope

- Add an optional versioned Python distribution block to release-record validation and templates without invalidating historical records.
- Add deterministic bundle-manifest parsing and `prepare-release --distribution-manifest` capture with exact candidate, version, epoch, filename, checksum, and hash validation.
- Add trusted-main release-plan resolution, exact external-state classification, deterministic result serialization, and bounded GitHub release helpers.
- Evolve `.github/workflows/publish-pypi.yml` in place into the top-level one-input orchestrator while preserving its external PyPI Trusted Publisher filename and protected environment.
- Separate resolve, credential-free qualification, GitHub write, PyPI OIDC, Pages write, and observation jobs with minimal permissions.
- Retain the existing exact PyPI controls, update their requirements/specification/verification wording where the explicit identity moves from manual tag/hash inputs to a manually selected released RLS, and preserve environment approval.
- Move normal Pages publication into the main-context orchestrator; narrow the current Pages workflow to a main-only explicit recovery path and align its governed definitions.
- Implement absent/exact/partial/mismatched reconciliation, draft GitHub staging, exact replay completion, Pages-only replay, and stage-specific failure reporting.
- Add deterministic unit, integration, static workflow, archive, schema, history, security-boundary, result, and failure-injection tests plus acceptance scenarios.
- Update repository-specific release/publication documentation and context only where behavior or commands change.
- Retain work-order-keyed evidence and a completion report.

## Out of scope

- Preparing or approving a product release, changing an existing RLS/VREC fact, creating or moving a production tag, publishing a GitHub Release, uploading to PyPI, deploying Pages, or approving an environment during this implementation work.
- Changing PyPI project ownership, package name, environment name, stored credentials, publisher action, attestation policy, or supported package formats.
- Renaming `publish-pypi.yml`, replacing its top-level PyPI identity with a reusable workflow, storing a PAT/GitHub App secret to trigger another workflow, or changing external publisher configuration.
- Creating general release automation for consumer repositories or adding this repository-specific workflow to the standard installation.
- Adding prereleases, platform wheels, alternate indexes, release branches, automatic RLS transitions, automatic merges, automatic evidence commits, or governor promotion.
- Deleting or rewriting historical formal artifacts, tags, releases, PyPI files, workflow runs, or Pages history.

## Authorized decision envelope

The implementation agent may choose helper module boundaries, deterministic JSON serialization mechanics, job and fixture names, safe temporary paths, bounded summary wording, and test decomposition. It may update existing PYP and DPG definition prose only to reflect the approved orchestration while preserving their normative security and provenance obligations.

The agent may not alter the single-input contract, RLS authority precondition, structured identity fields, top-level PyPI workflow filename, protected environments, credential separation, state classifications, immutable-state prohibitions, action pin review, assurance applicability, or production-action exclusions.

## Constraints

- Preserve Python 3.11+ standard-library runtime behavior and one consumer installation.
- Treat paths, TOML/JSON/Markdown, Git history, archives, workflow inputs, artifacts, API responses, and external metadata as untrusted.
- Use the released self-hosting governor independently from candidate source and package evidence.
- Keep candidate code out of every job with write or OIDC privileges.
- Perform no promotable production build except ephemeral deterministic fixtures explicitly bounded to this approved implementation; this work does not create a public release candidate.
- Preserve unrelated changes and existing VREC/RLS facts.
- Fail closed if implementation would require a stored workflow-trigger credential, reusable PyPI publisher, publisher migration, external destructive state change, or weakened environment policy.

## Expected change surface

- Release-record parsing, validation, template guidance, preparation CLI, and structured provenance helpers.
- Repository-specific GitHub scripts and `publish-pypi.yml` orchestration jobs.
- The Pages publication workflow's trigger/recovery surface and shared trusted helpers.
- Existing PyPI and dashboard definition artifacts affected by trigger composition.
- Unit, integration, workflow-policy, acceptance, release-build, provenance, and failure-state tests.
- Repository context and focused publication documentation.

No standard consumer workflow or packaged managed file should change unless a test-only compatibility correction is separately identified and approved.

## Required verification

- Start and review preflight for `WO-RLO-001`.
- Formal graph validation with zero new structure, governance, or policy findings; classify baseline maintenance warnings separately.
- Doctor and managed-integrity checks.
- Every matrix row and invariant in `VER-RLO-001`, plus the existing `VER-PYP-001` and `VER-DPG-001` controls affected by the change.
- Complete Python 3.11 and repository-default unit suites, focused release/PyPI/Pages/security suites, CLI help, `git diff --check`, and strict YAML parsing.
- Two independent non-promotable fixture builds proving deterministic wheel, normalized sdist, checksum, manifest, and exact reconstruction behavior.
- Released-governor candidate-source and candidate-package acceptance with runtime origins recorded.
- Hosted CI on the later review branch. No production external mutation is used as implementation evidence.

## Evidence to record

Retain `docs/engineering/release-orchestration/evidence/WO-RLO-001-verification.md` with approved scope, changed controls, exact commands and results, artifact and test counts, candidate/governor/tool identities, schema and state matrices, build hashes, action pins, permissions and environment analysis, external publisher/environment observations, documentation changes, warnings/deviations, residual risks, and all unperformed production/governance actions.

## Stop and escalate conditions

Stop for an invalid or damaged graph, managed-integrity drift, incomplete governing chain, need to mutate existing released facts, reusable-workflow requirement for PyPI, publisher filename/environment change, stored credential, candidate execution in a privileged job, unreviewed action change, nondeterministic artifact, unsafe archive, partial external test state, consumer-template impact, unclear RLS authority, new package format, or any production publication/deployment required to claim implementation completion.

## Completion report format

Report implemented requirements and existing controls preserved; changed files/components; release-record and manifest schema; workflow job/permission/environment matrix; normal and recovery state transitions; test and acceptance counts; deterministic artifact hashes; governor/source/package origins; documentation updates; warnings/deviations/residual risks; evidence path; candidate commit plan; and every commit, push, PR, verification transition, release action, publication, deployment, or external configuration change not performed.
