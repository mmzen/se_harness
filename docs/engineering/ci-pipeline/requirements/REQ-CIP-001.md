+++
id = "REQ-CIP-001"
type = "requirement"
title = "Run each candidate-evidence workflow once per commit"
status = "draft"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-26"
updated = "2026-08-26"
statement = "WHEN a commit is pushed to a branch that has an open pull request, THE SYSTEM SHALL run each candidate-evidence workflow once for that commit and cancel any in-progress run of the same workflow for a superseded commit on the same ref."
verification_method = "automated-workflow-inspection-and-run-observation"
[relations]
derives_from = ["CAP-CIP-001"]
+++

# Requirement: Run each candidate-evidence workflow once per commit

## Rationale

`engineering-harness.yml`, `candidate-evidence.yml` and
`predecessor-evaluator-assessment.yml` declare bare `push:` and
`pull_request:` triggers and no `concurrency:` block. One push to an open
pull request runs all three twice to completion, and a second push does
not cancel the first. `publication-rehearsal.yml` already has the right
shape: `push` restricted to `main` and a cancelling concurrency group.

## Preconditions and trigger

A push to any branch; a pull request opened or synchronized.

## Required response

- `push:` restricted to `main`, `release/**` and `candidate/**`;
  `pull_request:` unchanged.
- A `concurrency` group per workflow and ref with `cancel-in-progress: true`
  on the three candidate-evidence workflows; the release and replay workflows
  keep `cancel-in-progress: false`.
- The change to `engineering-harness.yml` is made in
  `templates/repository/standard/.github/workflows/`; the hash-locked root
  copy is not edited.

## Failure and boundary behavior

A push to a branch without a pull request runs nothing except
`engineering-harness.yml`'s managed copy until the governor upgrade; this is
disclosed in the notes. A direct push to `main` still runs every workflow.

## Constraints

No check is removed. The integration-package jobs, which only pass on the
pull-request run, are unaffected.

## Acceptance examples

**Given** a pull request with two pushes ten seconds apart
**When** the runs are listed
**Then** each workflow has one completed run for the second commit and one
cancelled run for the first, and no `push`-event run for either.

**Given** a push to `main`
**When** the runs are listed
**Then** every workflow with a `push` trigger has one run.

## Open decisions

None.
