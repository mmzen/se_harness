+++
id = "WO-PYP-002"
type = "work_order"
title = "Commit and publish PyPI automation for review"
status = "approved"
owners = ["repository-owner", "engineering-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
implements = ["REQ-PYP-005"]
specifications = ["SPEC-PYP-001"]
architecture = ["ARCH-PYP-001", "ADR-PYP-001"]
verification = ["VER-PYP-001"]
+++

# Work Order: Commit and publish PyPI automation for review

## Objective

Retain the completed `WO-PYP-001` implementation and evidence in one clean candidate commit, capture `VREC-PYP-001` against that exact candidate, retain the ready record in a later governance commit, push the review branch normally, and open a pull request against `main`.

## Authorization

The accountable repository owner explicitly authorized this sequence on 2026-08-11 with the instruction `commit, capture, commit and push + PR`.

## In scope

- Confirm `feature/pypi-trusted-publishing` is based on current `origin/main` and contains only the bounded PyPI publication implementation, governance packet, tests, and evidence.
- Run the required graph, focused/full test, CLI, doctor, workflow-syntax, dashboard, and diff-hygiene checks.
- Commit the complete `WO-PYP-001` candidate and this publication authorization.
- From the resulting clean candidate, run `harnessctl capture-verification` for `WO-PYP-001`, `VER-PYP-001`, and its retained evidence, producing `VREC-PYP-001` with status `ready` and the exact candidate commit.
- Commit only the ready verification record in a later governance commit.
- Push `feature/pypi-trusted-publishing` normally to `origin` with upstream tracking.
- Open a GitHub pull request targeting `main` with implementation, security-boundary, environment, and verification summaries.

## Out of scope

- Transitioning `VREC-PYP-001` to `verified` or changing its captured provenance.
- Preparing or transitioning a release record.
- Merging the pull request or modifying remote `main` directly.
- Dispatching the PyPI workflow, approving a deployment, or uploading a package.
- Moving or replacing `v0.2.0`, changing GitHub release assets, or editing historical `RLS-SEH-001`.
- Force pushing, deleting branches, rewriting history, or storing a PyPI credential.

## Authorized decision envelope

The implementation agent may choose concise commit and pull-request wording. It may not change the verified scope after candidate commit, include unrelated files, alter ready-record facts, weaken the publication controls, or broaden the external actions.

## Constraints

The candidate must be clean before capture. `VREC-PYP-001` must name the first commit rather than its own later governance commit. The push is a normal new-branch push. The PR targets `main`. Publication remains a later separately authorized action after merge and verification transition.

## Expected change surface

Two Git commits on `feature/pypi-trusted-publishing`, one new `VREC-PYP-001` file in the PyPI packet, one remote review branch, and one pull request.

## Required verification

Validate the artifact graph with zero errors/warnings; run all 60 tests on Python 3.11 and 3.14 with only the two known Windows symlink skips; run focused PyPI tests, CLI help, source doctor, dashboard, YAML and Bash syntax checks, and `git diff --check`; verify the candidate is clean and based on current `origin/main`; inspect the ready record after capture; and confirm GitHub CI starts on the PR.

## Evidence to record

Pre-commit verification is retained in `WO-PYP-001-verification.md` and `WO-PYP-002-verification.md`. Candidate/governance commits, remote branch state, PR URL, and CI results remain externally discoverable after creation rather than being predicted inside the candidate.

## Stop and escalate conditions

Stop if `origin/main` changed incompatibly, the tree includes unrelated changes, a required check fails, capture selects the wrong commit/scope/evidence, the remote branch already diverges, GitHub authentication fails, the PR target is not `main`, or any step would dispatch or publish the package.

## Completion report format

Report candidate and governance commit IDs, captured VREC facts, remote branch and PR URL, check status, excluded publication action, deviations, and residual risks.
