+++
id = "REQ-AUT-007"
type = "requirement"
title = "Authoring advisories are reported apart from errors and warnings"
status = "draft"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-30"
updated = "2026-08-30"
statement = "WHEN a repository is validated, THE SYSTEM SHALL report the authoring-style signals as advisories, counted and listed apart from errors and warnings, shown on request, and raised only for artifacts still in draft, so that the warning count reads zero when nothing needs an operator's attention."
verification_method = ["test"]
priority = "must"
source = "functional assessment of 2026-08-30 (issue #283): 485 warnings on a clean tree, 416 of them W-AUT-*"

[relations]
derives_from = ["CAP-AUT-001"]
+++

# Requirement: Authoring advisories are reported apart from errors and warnings

## Rationale

`REQ-AUT-002` and `REQ-AUT-003` made the validator signal statement style
(`W-AUT-001` to `W-AUT-003`) and the old free-text `verification_method`
(`W-AUT-004`) as maintenance warnings. They were written as advice for the
author of a draft. On this repository they now fire on 416 approved
artifacts whose text is frozen by governance, and `validate .` reads
`0 errors, 485 warnings` on a tree nothing is wrong with. A warning that
nobody can act on and nobody reads is not a signal; a real new warning
disappears inside the count. The fix is a third class, *advisory*: still
computed, still in the JSON, shown when asked for, but not in the number an
operator or a lane looks at first, and not raised at all once an artifact
has left `draft`.

## Preconditions and trigger

Validation of a repository by the validator script, `harnessctl validate`,
or any command that reads the validation report (`inspect`, `doctor`,
`check`).

## Required response

- The `W-AUT-*` family is the advisory class. An advisory is not an error
  and not a warning: it does not appear in the warning list, the warning
  count or the per-plane warning counts.
- The human summary gains a fourth number: `Artifacts | Errors | Warnings
  | Advisories`. Advisories are listed only when `--advisories` is given.
- The JSON report always carries `advisories` and `advisory_count`.
- An advisory is raised only for an artifact whose status is `draft`. An
  artifact past `draft` raises none.
- `inspect` and `check` read the report, so their warning-derived counts
  exclude advisories without further change. `doctor` is unchanged.

## Failure and boundary behavior

An advisory never blocks. The authoring checklist that `create-artifact`
prints is unchanged; it already names the statement rules. `E005` (no
`SHALL`) and `E-AUT-001` (unknown vocabulary after the migration) stay
errors.

## Constraints

No change to any error code or to the plane taxonomy.

## Acceptance examples

### Example: normal behavior

**Given** this repository at a commit where `validate .` reads
`0 errors, 485 warnings`, 416 of them `W-AUT-*`, all on approved artifacts.

**When** validated after this change.

**Then** the summary reads `Errors: 0 | Warnings: 69 | Advisories: 0`, and
`--json` carries `advisories: []`.

### Example: failure behavior

**Given** a draft requirement whose statement carries two `SHALL`s.

**When** `validate --advisories` runs.

**Then** the summary reads `Advisories: 1`, `W-AUT-002` is listed under
`Advisories:`, and the warning count is unchanged.

## Open decisions

None.
