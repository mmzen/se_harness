+++
id = "REQ-RLO-012"
type = "requirement"
title = "Establish the released maintenance line"
status = "approved"
owners = ["release-owner", "engineering-owner"]
created = "2026-08-19"
updated = "2026-08-19"
statement = "WHEN the repository-specific workflow materializes an authorized SE Harness release, THE SYSTEM SHALL create or verify its derived release/MAJOR.MINOR maintenance branch at a history containing the exact released candidate without moving an existing branch."
verification_method = "automated-workflow-policy-and-state-test"

[relations]
derives_from = ["CAP-RLO-001"]
+++

# Requirement: Establish the released maintenance line

## Rationale

SE Harness documents supported `release/x.y` maintenance lines, but the repository release workflow currently stops after tag, GitHub Release, PyPI, and Pages publication. Maintainers must remember a separate branch operation, which makes the last mile incomplete and can produce an unsupported or incorrectly based release line.

## Preconditions and trigger

One released RLS has resolved from trusted `main`, its candidate and semantic version are exact, the qualified bundle matches, and the GitHub tag and Release have reached their exact authorized state.

## Required response

Derive `release/MAJOR.MINOR` from the released version. If the branch is absent, create it at the exact candidate commit. If it exists, verify that the candidate is the branch tip or an ancestor of it and leave it unchanged. Report the derived branch and whether it was created or already contained the candidate.

## Failure and boundary behavior

An invalid version, conflicting ref type, inaccessible hosting state, or existing branch that does not contain the candidate blocks the transaction visibly. Automation must never force-update, delete, rewind, merge, or otherwise repair an existing branch.

## Constraints

- This is policy of the `mmzen/se_harness` implementation repository only.
- Preserve the single `release_record` workflow input; branch identity is derived, not supplied.
- Use one line branch per `MAJOR.MINOR`, not a separate `release/MAJOR.MINOR.PATCH` branch.
- Do not change `harnessctl`, the packaged `se_harness` namespace, managed consumer templates, consumer CI, or portable graph validation.
- Branch creation grants no formal verification, release, or maintenance-work authority.

## Acceptance examples

### Example: first release in a line

**Given** released version `0.5.0`, candidate `C`, and no `release/0.5` ref

**When** the repository publication workflow reaches exact GitHub release state

**Then** it creates `release/0.5` at `C` and reports `created`.

### Example: replay or later patch

**Given** released version `0.5.1`, candidate `P`, and existing `release/0.5` whose tip is `P` or a descendant of `P`

**When** the workflow reconciles the maintenance line

**Then** it reports `existing` and does not move the ref.

### Example: conflicting line

An existing `release/0.5` that does not contain the selected candidate blocks publication continuation and remains unchanged.

## Open decisions

Whether a future release line is unsupported and therefore should omit a branch is not configurable in this bounded change. This repository currently treats every normal released minor line as maintainable; changing that policy requires later governed work.

## Approval

Approved by the accountable repository owner on 2026-08-19 through the statement `go implement` as part of the complete RLO-003 packet. This approves the requirement definition and the bounded implementation in `WO-RLO-003`; it does not create a branch or authorize a release, publication, deployment, or formal assurance transition.
