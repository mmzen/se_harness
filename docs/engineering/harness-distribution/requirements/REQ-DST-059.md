+++
id = "REQ-DST-059"
type = "requirement"
title = "Upgrade consumer CI through the standard transaction"
status = "implemented"
owners = ["engineering-owner", "security-owner", "quality-owner"]
created = "2026-08-17"
updated = "2026-08-17"
statement = "WHEN an operator plans or applies a standard repository upgrade with a newer released SE Harness package, THE SYSTEM SHALL synchronize the managed consumer workflow to that same evaluator version through the existing safe upgrade transaction without a separate CI or governor-reconciliation command."
verification_method = "automated-upgrade-and-migration-test"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Upgrade consumer CI through the standard transaction

## Rationale

Package upgrade and repository upgrade are intentionally separate, but consumer CI must not require a third reconciliation concept. The normal plan/apply transaction already owns the canonical workflow and lock evidence.

## Preconditions and trigger

The operator upgrades the selected local environment to a newer released `se-harness`, then runs `harnessctl upgrade <repository>` with or without `--apply`.

## Required response

- The read-only plan shows the exact managed workflow disposition and new evaluator version.
- Explicit apply updates an unmodified older consumer workflow, configuration identity, other managed distribution files, and lock metadata atomically.
- Re-running plan/apply is idempotent.
- Customized, ambiguous, or protected content blocks all writes and remains unchanged.
- `reconcile-governor` remains applicable only to the explicitly classified SE Harness implementation repository.

## Failure and boundary behavior

Installing a newer Python package alone does not mutate a repository or its hosted CI. Applying a repository upgrade locally does not affect GitHub until the resulting files are reviewed, committed, pushed, and merged. The tool does not configure required checks or deployment ordering.

## Constraints

- There is one public consumer upgrade path: package upgrade, read-only repository plan, explicit apply, and `doctor`.
- No profile, YAML merge engine, automatic self-update, or implicit network mutation is introduced.
- Historical consumer workflows that exactly match their retained managed evidence may migrate; customized workflows require explicit owner resolution.

## Acceptance examples

### Example: ordinary upgrade

**Given** an unmodified SE Harness 0.4.0 consumer installation and a newer installed release,

**When** the operator applies the reviewed upgrade,

**Then** the dedicated workflow names the newer release as its sole evaluator and the managed lock is current.

### Example: package-only upgrade

**Given** the operator updates the local virtual environment,

**When** no repository upgrade is applied,

**Then** the committed workflow and GitHub behavior remain unchanged.

## Open decisions

None when approved.
