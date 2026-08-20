+++
id = "REQ-HUP-003"
type = "requirement"
title = "Preserve evaluator and candidate role separation"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-20"
updated = "2026-08-20"
statement = "WHEN the governor-upgrade candidate is reviewed locally or in hosted CI, THE SYSTEM SHALL prove that released-evaluator, candidate-source, and candidate-package roles remain distinct, fail closed on cross-role execution, and retain sufficient evidence to restore the prior 0.5.0a1 root before merge."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-HUP-001"]
+++

# Requirement: Preserve evaluator and candidate role separation

## Rationale

The managed version update is trustworthy only if CI executes the independently installed final evaluator and candidate checks remain evidence rather than governance authority.

## Preconditions and trigger

The managed upgrade candidate exists in a reviewable worktree or commit and no product/release change is mixed into it.

## Required response

- Run doctor, validation, start/review preflight, inspection, and dashboard through the released 0.5.0 environment.
- Require hosted Engineering Harness CI to install exact `se-harness==0.5.0` from the package index outside the checkout.
- Run candidate-source and candidate-package evidence in their existing non-governing lanes.
- Record module, distribution, Python, entry-point, checkout, commit, and wheel identities for each applicable role.
- Retain the exact pre-upgrade files and candidate diff so the branch can be abandoned or reverted before merge without changing public state.

## Failure and boundary behavior

Wrong evaluator version, checkout import, cross-role module origin, managed drift, invalid graph, failing test, unexpected file, or unexplained warning blocks verification and merge readiness.

## Constraints

Rollback before merge is repository-local abandonment or an ordinary reviewed revert; no force push, history rewrite, public package replacement, or tag movement is allowed.

## Acceptance examples

### Example: green separated lanes

**Given** a clean upgrade candidate

**When** local and hosted checks run

**Then** the evaluator resolves to public 0.5.0 while candidate roles resolve only in their bounded evidence lanes.

### Example: product change mixed into upgrade

**Given** package source, version, release artifacts, or publication controls changed

**When** changed-surface validation runs

**Then** review stops for scope expansion.

## Open decisions

None after accountable owners approve the evidence and rollback boundary.
