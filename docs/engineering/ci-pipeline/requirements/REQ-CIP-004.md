+++
id = "REQ-CIP-004"
type = "requirement"
title = "Identify a release unit by a candidate commit and derive its work-order census"
status = "draft"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-26"
updated = "2026-08-26"
statement = "WHEN a release contract is drafted, THE SYSTEM SHALL identify the release unit by one candidate commit and derive the gated work-order list from the Harness-Work-Order trailers of the commits between the previous release tag and that commit."
verification_method = "automated-derivation-test-and-template-inspection"
[relations]
derives_from = ["CAP-CIP-001"]
+++

# Requirement: Identify a release unit by a candidate commit and derive its work-order census

## Rationale

`REL-SEH-012` through `REL-SEH-015` were each approved and then rejected on
2026-08-25 for one cause: the contract freezes an allow-list of work orders,
forbids in-place amendment, and a work order reached `implemented` on
`main` after the freeze — once forty-six seconds after approval. Each
re-issue cost a 30–68 KB contract, an entry re-measurement, two owner
decisions and a governance pull request. `publish-pypi.yml` already tags
the candidate commit, not the list; the contract can name that commit from
the start.

## Preconditions and trigger

A release contract is drafted or re-measured.

## Required response

- `RELEASE_CONTRACT.template.md` carries `candidate_commit` (full object
  id) and `previous_release_tag`; `gates` remains the census, now a
  measured value.
- `harnessctl release-unit . --from <tag> --to <commit>` derives the census:
  one row per distinct `Harness-Work-Order` trailer on the first-parent
  history, each row with the work order's status and whether its execution
  scope intersects the packaged surface; output as the canonical JSON block
  and as a TOML `gates` array ready to paste.
- The stop condition becomes: the candidate commit is not an ancestor of
  the ref being released, or the derived census differs from `gates`. A
  merge to `main` after the cut is not a stop condition.
- A late fix is a new candidate commit on a `candidate/X.Y.Z` branch cut from
  the frozen commit, and a new contract names it.

## Failure and boundary behavior

A commit without a trailer on the first-parent path is listed as
`untraced` and fails the derivation unless the contract lists it under an
explicit exemption. The command mutates nothing.

## Constraints

Existing approved and released contracts are not re-shaped. The command
belongs to the candidate CLI; the root's released evaluator does not need it
to validate the template's new fields, which are repository-owned data.

## Acceptance examples

**Given** a fixture history with tag `v1`, four merges carrying three
distinct trailers and one merge without
**When** `release-unit --from v1 --to HEAD` runs
**Then** the census lists the three work orders with statuses and one
`untraced` commit, and exits non-zero.

**Given** a contract naming candidate `C` and a later merge to `main`
**When** the contract is re-measured
**Then** the derived census over `v1..C` is unchanged and no stop condition
fires.

## Open decisions

None.
