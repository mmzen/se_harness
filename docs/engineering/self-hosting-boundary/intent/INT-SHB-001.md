+++
id = "INT-SHB-001"
type = "intent"
title = "Make self-hosted harness development independently governable"
status = "approved"
owners = ["repository-owner", "quality-owner", "release-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
+++

# Intent: Make self-hosted harness development independently governable

## Problem

`se_harness` is both a product and a repository that uses the product. The current model upgrades the repository's active managed harness to the unreleased candidate, requires candidate templates to equal the operational root copies, and also describes a previously released wheel as an independent baseline. Those identities are not operationally isolated.

The failure is visible in pull request #28: released 0.2.1 runs `doctor` against candidate-managed 0.2.2 files and correctly reports distribution mismatch, while a later `python -c` import can resolve the checkout's `se_harness` package instead of the installed baseline. Candidate and governor evidence can therefore conflict or silently collapse into one runtime.

## Desired outcome

The repository is governed by one exact, immutable released harness. Candidate source is treated as the system under development, and a built candidate package is treated as the deliverable under acceptance. Each identity operates in a distinct runtime and against an explicitly permitted target. An unreleased candidate never overwrites or impersonates the governor merely because the product is self-hosting.

After a version is published and independently retrievable, a separate governed host-upgrade change may promote it to be the governor for the next development cycle.

## Success indicators

- CI reports the exact version, origin, executable, module path, and target role of every harness runtime.
- Released-governor checks cannot import candidate source through current-directory shadowing.
- Same-version installation integrity is checked only against a repository created or managed by that distribution.
- Candidate source and candidate packages are tested without becoming product or release authority.
- The checkout is explicitly candidate source, while governor runtime and same-version managed state remain isolated outside it; candidate distribution parity is proved both in the checkout and disposable package installations.
- Changing a verified or released candidate stops external promotion and requires a new candidate, VREC, and RLS without rewriting history.
- A published version becomes the next governor only through a separate, reviewable post-release upgrade.

## Criticality

Without this boundary, a harness change can either fail for the wrong reason or appear independent while importing the candidate it is meant to challenge. That weakens G3 through G5 precisely where the harness claims independent, commit-bound assurance.

## Authority boundary

Implementation was approved on 2026-08-12 for `WO-SHB-001`. This intent does not invalidate or amend historical records and grants no authority to commit, push, merge, verify, release, tag, publish, or deploy.
