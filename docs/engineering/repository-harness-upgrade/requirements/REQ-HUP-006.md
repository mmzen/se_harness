+++
id = "REQ-HUP-006"
type = "requirement"
title = "Preserve owner content and evaluator role separation"
status = "approved"
owners = ["quality-owner", "security-owner", "repository-owner"]
created = "2026-08-23"
updated = "2026-08-23"
statement = "WHEN the 0.6.0 root-upgrade candidate is applied or reviewed, THE SYSTEM SHALL preserve owner-controlled bytes and formal history, retire only withdrawn harness ownership, keep released-evaluator, candidate-source, and candidate-package roles distinct, and demonstrate that no product, release, publication, or external state changed."
verification_method = "inspection"

[relations]
derives_from = ["CAP-HUP-002"]
+++

# Requirement: Preserve owner content and evaluator role separation

## Rationale

Version 0.6.0 withdraws the repository-context scaffold and expands managed policy, but it does not own existing repository facts or authorize product/release changes. The transition remains trustworthy only if the released target runtime is distinct from the source and package candidates it evaluates.

## Preconditions and trigger

The reviewed root-upgrade candidate exists in a worktree and the baseline owner-content, formal-history, product, release, and external-action surfaces have recorded hashes or Git identities.

## Required response

- Preserve owner content outside managed marker blocks in `AGENTS.md`, `CLAUDE.md`, and `.gitignore`.
- Leave `docs/engineering/REPOSITORY_CONTEXT.md` byte-identical while omitting it from the new lock and all harness requirements.
- Preserve every existing formal artifact; add only the HUP-002 definition and later keyed evidence authorized by this packet.
- Run released-evaluator doctor, validate, preflight, inspection, dashboard, release-distribution validation, CLI smoke checks, tests, diff checks, and role-origin checks.
- Prove no changes under product source, canonical package templates, package metadata, repository release tooling, release records, publisher, Pages publisher, tags, remotes, or external services.

## Failure and boundary behavior

Owner-byte drift, formal-history rewrite, candidate contamination, product/release mutation, unexpected warning or error, failing required check, generated-output residue, or external-state change blocks completion and later commit-bound verification.

## Acceptance examples

### Example: repository-context retirement

**Given** an existing owner-authored `docs/engineering/REPOSITORY_CONTEXT.md`

**When** the 0.6.0 upgrade applies

**Then** its bytes are unchanged and the schema-3 lock contains neither an entry nor a tombstone for it.

### Example: candidate-governor contamination

**Given** checkout source or a candidate wheel is reachable by the evaluator runtime

**When** identity or verification runs

**Then** the operation fails and no governance claim is accepted.

## Open decisions

Hosted checks and commit-bound verification remain later decisions after a separately authorized candidate commit.
