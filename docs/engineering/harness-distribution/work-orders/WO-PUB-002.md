+++
id = "WO-PUB-002"
type = "work_order"
title = "Publish cross-agent harness changes for review"
status = "approved"
owners = ["repository-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
implements = ["REQ-DST-007", "REQ-DST-008"]
specifications = ["SPEC-DST-002"]
architecture = ["ARCH-DST-002", "ADR-DST-002"]
verification = ["VER-DST-002"]
+++

# Work Order: Publish cross-agent harness changes for review

## Objective

Commit the completed `WO-DST-003` implementation and evidence on a new review branch, push that branch normally to the configured `origin`, and open a pull request against `main`.

## Authorization

The accountable repository owner explicitly authorized this work on 2026-08-11 with the instruction `commit, push and PR`.

## In scope

- Create `feature/cross-agent-repository-context` from the current local `main` base.
- Commit the bounded implementation, governance artifacts, self-installation updates, documentation, tests, and retained evidence.
- Push the new branch to `origin` with upstream tracking.
- Open a GitHub pull request targeting `main` with a concise implementation and verification summary.

## Out of scope

Force push, history rewriting, direct modification of remote `main`, tag creation, GitHub release creation, verification or release approval, package publication, deployment, and merging the pull request are not authorized.

## Required preflight

The artifact graph, complete test suite, CLI help, installed-harness doctor, and diff hygiene must pass before the commit. The remote URL and branch base must be inspected before publication.

## Completion evidence

The commit SHA, remote branch, and pull request are discoverable through Git history and the configured repository host rather than self-recorded in the commit that creates them.
