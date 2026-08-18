+++
id = "VER-RLO-001"
type = "verification"
title = "Verify deterministic last-mile release orchestration"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-18"
updated = "2026-08-18"

[relations]
verifies = ["REQ-RLO-001", "REQ-RLO-002", "REQ-RLO-003", "REQ-RLO-004", "REQ-RLO-005", "REQ-RLO-006", "REQ-RLO-007", "REQ-RLO-008"]
+++

# Verification Contract: Verify deterministic last-mile release orchestration

## Independence

Tests consume workflows, formal artifacts, manifests, archives, Git histories, and external-state responses as data. Expected state is generated independently from fixtures rather than by the implementation helper under test. Candidate build jobs and credential-bound workflow policy are assessed separately. Production mutation is excluded from this implementation work order and remains a later release-owner action.

The released self-hosting governor assesses the candidate repository independently from candidate source and candidate package tests. Existing `VER-PYP-001` and `VER-DPG-001` remain selected for their underlying channels.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| REQ-RLO-001 | resolver unit/integration tests | released, ready, branch-only, ambiguous, mismatched VREC/tag histories | only one released main-history RLS resolves; one input supplies all identities |
| REQ-RLO-002 | schema, CLI, template, and compatibility tests | exact, partial, unsafe, wrong-version, wrong-commit, wrong-epoch manifests; historical RLS | exact block is captured atomically; malformed input fails; historical records remain valid |
| REQ-RLO-003 | reproducible-build and policy tests | two exports/builds, normalized archives, changed byte, candidate checkout placement | both builds and RLS hashes agree; no credential exists in qualification |
| REQ-RLO-004 | Git fixture/API-response tests | absent, exact tag, mismatched tag, draft, exact final, extra/mismatched assets | only absent or exact state progresses; final asset set is exactly three |
| REQ-RLO-005 | static workflow and PyPI-state tests | publisher identity, environment, permissions, absent/exact/partial/mismatched versions | top-level OIDC job is least privilege; no checkout/build/secret/skip; state rules hold |
| REQ-RLO-006 | workflow policy and provenance fixtures | main orchestration, tag-ref attempt, manual replay, deploy failure | normal Pages job uses main context and exact governance; recovery remains bounded |
| REQ-RLO-007 | state-machine and failure injection | interruption after tag, draft assets, final release, PyPI partial, Pages failure | exact replay continues or completes; partial/mismatch stops without destructive mutation |
| REQ-RLO-008 | result-schema and smoke fixtures | full success, preflight failure, package success plus Pages failure | JSON and summary agree, retain stage-specific facts, and never imply lifecycle authority |

## Acceptance scenarios

Executable scenarios are retained in `acceptance/release-orchestration.feature`. Unit tests must implement each scenario or name equivalent fixture coverage in the evidence.

## Property and invariant tests

- The normal trigger exposes exactly one required release-record input and requires `main`.
- All derived commits and digests are full lowercase values of the configured object/hash formats.
- The distribution block is absent or complete; an orchestrated release requires it.
- Identical candidate, epoch, and toolchain inputs yield byte-identical wheel, normalized sdist, checksum manifest, and manifest JSON.
- Candidate code cannot execute in jobs with `contents: write`, `id-token: write`, or `pages: write`.
- Existing immutable state is either exact, partial, or mismatched; only exact is replay-complete.
- A result cannot report an unobserved stage as satisfied.

## Static and architecture checks

- Parse all modified YAML with a strict YAML parser and let GitHub validate it on the pull request.
- Assert top-level triggers, input count, concurrency, `if` conditions, job permissions, environment names, action SHAs, checkout placement, and absence of PAT/secret-based workflow triggering.
- Assert `publish-pypi.yml` remains the direct OIDC workflow and no publisher step appears in a reusable workflow.
- Validate typed architecture/specification/work-order overlap and decision coverage.

## Security and privacy checks

Review expression-to-shell transport, path and archive handling, artifact-download identity, GitHub API mutations, release body construction, JSON/TOML parsing, and every external response. Confirm no candidate-controlled shell, filename, release note, archive member, or metadata field reaches a credential boundary without strict validation. Inspect the live `pypi` and `github-pages` environment policies and the PyPI publisher filename/environment before any authorized production use.

## Performance and resilience checks

Measure one full credential-free qualification and keep bounded artifacts below GitHub limits. Inject network/API failures before and after each modeled external state. Prove retries do not cancel active immutable publication, change identity, or spin indefinitely.

## Manual assessments

- The technical and security owners confirm `ADR-RLO-001` still matches PyPI's current reusable-workflow limitation.
- The release owner confirms a released RLS plus dispatch and protected environment review is the intended authority sequence.
- The service owner confirms Pages-only replay and partial publication escalation procedures.
- A later real release, under its own release authority, confirms GitHub, PyPI attestations, public Python 3.11 installation, and Pages provenance.

## Evidence retention

Retain implementation evidence at `docs/engineering/release-orchestration/evidence/WO-RLO-001-verification.md`. Record exact commands and counts, candidate and governor identities, changed workflow and schema invariants, fixture matrices, two-build hashes, result schemas, hosted CI URLs, external configuration observations, deviations, and every production action not performed.

## Residual uncertainty

Fixture tests cannot prove future GitHub, PyPI, or Pages service behavior or live administrator configuration. The first separately authorized orchestrated release remains an operational validation. PyPI may later support reusable workflow identities; this implementation intentionally follows the current externally documented limitation.
