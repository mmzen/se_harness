+++
id = "REQ-ADS-004"
type = "requirement"
title = "Recurring traps become evaluator diagnostics"
status = "draft"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-25"
updated = "2026-08-25"
statement = "WHEN a handoff check or review preflight runs in a Git checkout, THE SYSTEM SHALL warn when a pull-request body under evaluation carries a carriage return inside the `Harness-Work-Order` trailer line, and SHALL warn when a `ready` verification record binds a candidate commit that is not an ancestor of `HEAD`."
verification_method = "automated-test"
[relations]
derives_from = ["CAP-ADS-001"]
+++

# Requirement: Recurring traps become evaluator diagnostics

## Rationale

Four traps are documented in the owner region. Operating the repository from a
coding agent has surfaced more that recur: a CRLF in the pull-request body
breaks the work-order trailer while the local round trip hides it; a `ready`
VREC is silently orphaned when the branch below it in a stack is rebased or
merged. Each was learned by a stopped run. A trap that has bitten twice should
be a diagnostic, not a memory.

## Preconditions and trigger

- `harnessctl check --checkpoint handoff` with `--pull-request-body <file>`, or
  the CI selector reading the stored event payload.
- `harnessctl preflight --phase review` in a Git checkout containing at least
  one `ready` verification record.

## Required response

- `W-ADS-001`: the trailer line contains `\r`; the diagnostic names the byte
  offset and the exact fix (`git config core.autocrlf`, or write the body with
  `newline="\n"`).
- `W-ADS-002`: `VREC-…` is `ready` and its `candidate_commit` is not reachable
  from `HEAD`; the diagnostic names the record, the commit, and the only legal
  routes (`verify`, `reject`, or a successor bound to a fresh commit).

## Failure and boundary behavior

Both are warnings on the `governance` plane; they never change severity of an
existing rule or exit status of a passing run. Outside a Git checkout,
`W-ADS-002` is `not_assessable` and is reported as such.

## Constraints

No new gate. No change to `QUALITY_GATES.json`. Diagnostic identifiers are
reserved in the `ADS` family.

## Acceptance examples

### Example: normal behavior

**Given** a pull-request body file whose trailer line ends `WO-X-001\r\n`

**When** `check --checkpoint handoff --pull-request-body body.md` runs

**Then** `W-ADS-001` is reported with the byte offset.

### Example: failure behavior

**Given** `VREC-X-001` is `ready` bound to commit `abc…` and `HEAD` no longer
contains `abc…`

**When** `preflight --phase review` runs

**Then** `W-ADS-002` names `VREC-X-001`, `abc…`, and the legal routes.

## Open decisions

None.
