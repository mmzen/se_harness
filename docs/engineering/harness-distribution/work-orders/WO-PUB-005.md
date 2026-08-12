+++
id = "WO-PUB-005"
type = "work_order"
title = "Publish aggregate documentation candidate for review"
status = "implemented"
owners = ["repository-owner", "engineering-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
implements = ["REQ-DST-019", "REQ-DST-020", "REQ-DST-021", "REQ-DST-022", "REQ-DST-023", "REQ-DST-024", "REQ-DST-025", "REQ-DST-026", "REQ-DST-027", "REQ-DST-028"]
specifications = ["SPEC-DST-006", "SPEC-DST-007"]
architecture = ["ARCH-DST-006", "ADR-DST-006", "ARCH-DST-007", "ADR-DST-007"]
verification = ["VER-DST-006", "VER-DST-007"]
+++

# Work Order: Publish aggregate documentation candidate for review

## Lifecycle and authorization

The accountable repository owner explicitly instructed `this becomes the commit candidate, you can commit, create the PR, and create the validation record` on 2026-08-12. That instruction authorizes the aggregate candidate commit, one ready verification record, the later governance commit retaining that record, a normal branch push, and one pull request against `main`.

This governance-only work order reached `implemented` after the branch was pushed and pull request 32 existed. It is not release payload and is not included in the aggregate VREC it authorized.

## Objective

Retain the completed `WO-DOC-007` and `WO-DOC-008` documentation, tests, packets, and evidence as one clean candidate commit; prepare and retain one aggregate ready verification record bound to that commit; publish the branch normally; and open one reviewable pull request declaring this work order.

## In scope

- Audit the complete current branch diff against `origin/main` and protected surfaces.
- Run candidate checks and phase-appropriate preflight for both implementation work orders and this publication work order.
- Create one candidate commit containing the approved documentation implementation, focused tests, packets, honest work-order lifecycle states, and retained evidence.
- From the clean candidate commit, run `harnessctl capture-verification` for `WO-DOC-007` and `WO-DOC-008`, their exact `VER-DST-006` and `VER-DST-007` union, and both work-order evidence paths.
- Use new ID `VREC-DST-005` and retain its `ready` record in a later governance commit.
- Push `docs/update-readme` normally to `origin` with upstream tracking.
- Open one GitHub pull request against `main` whose standalone declaration is `Harness-Work-Order: WO-PUB-005` and whose summary identifies the aggregate work and ready VREC.
- After the pull request exists, retain this work order's `implemented` transition and exact publication evidence in one final governance commit and push it normally to the open branch.

## Out of scope

- At the time of candidate publication, transitioning `VREC-DST-005` to `verified` or any work order to `verified` or `released`. The later, separately accountable approval recorded by `WO-DST-006` extends only the existing PR envelope as described below; it does not retroactively make transition authority part of the original publication decision.
- Preparing or transitioning a release record; changing a version; building a distribution; creating a tag or GitHub Release; publishing to PyPI; deploying; or promoting the self-hosting governor.
- Merging the pull request, force pushing, rewriting history, modifying remote `main`, or changing branch protection and other external configuration.
- Changing implementation content after candidate selection except to correct a blocking verification or publication defect through a new explicitly reported candidate.
- Including this governance-only work order in release-bearing VREC coverage.

## Required verification

- Formal validation has zero errors and only the 38 classified historical warnings.
- `doctor`, review preflight, 27 focused documentation tests, and the 140-test complete suite pass.
- The root remains at 140 lines and nine level-two sections, with protected managed/runtime surfaces unchanged.
- The worktree is clean at verification capture and the VREC records full Git object identity, clean state, both evidence paths, both work orders, both verification contracts, and the deterministic artifact snapshot.
- The ready record validates before its governance commit.
- The normal push and PR creation succeed without rewriting history.

## Evidence and completion

Retain candidate SHA, candidate tree, VREC metadata, governance commit, branch/upstream, pull request URL and number, PR declaration, exact checks, warning classification, and prohibited-action confirmation in `docs/engineering/harness-distribution/evidence/WO-PUB-005-publication.md`.

The branch and ready VREC were retained, and pull request 32 was opened against `main`; exact publication evidence is retained at the path above. The `implemented` state records publication work only and grants no assurance or release authority.

## Later assurance publication extension

After pull request 32 passed its required checks, the accountable repository owner separately instructed `verification record approved` on 2026-08-12. `WO-DST-006` records that assurance authority and the bounded `VREC-DST-005` transition. This later decision also authorizes carrying the four-file assurance governance commit on the already-open `docs/update-readme` branch under this PR-level publication envelope, so the standalone declaration `Harness-Work-Order: WO-PUB-005` remains an honest aggregate scope selector.

This extension does not authorize any other VREC or work-order transition, release preparation or approval, merge, build, tag, publication, deployment, force push, or history rewrite. It does not add `WO-PUB-005` or `WO-DST-006` to the release-bearing verification claim.
