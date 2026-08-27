+++
id = "REQ-ECP-006"
type = "requirement"
title = "The pull-request gate enforces scope unconditionally"
status = "draft"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-27"
updated = "2026-08-27"
statement = "WHEN the managed CI workflow runs on a pull-request event, THE SYSTEM SHALL evaluate `QGP-G4I-PATHS` over the pull request's Git difference against its base and fail the required check on any path outside the selected work order's execution scope."
verification_method = ["test", "demonstration"]
priority = "must"
source = "review section 5, weakness 2"

[relations]
derives_from = ["CAP-ECP-001"]
+++

# Requirement: The pull-request gate enforces scope unconditionally

## Rationale

The template CI checks scope only when a `Harness-Restitution:` trailer is
present (templates/repository/standard/.github/workflows/engineering-
harness.yml:56-89; docs/notes/agentic-execution-review-2026-08.md:111-114).
`transition` never checks scope. Enforcement is therefore opt-in at the only
boundary an agent cannot bypass (docs/notes/agentic-execution-
review-2026-08.md:310). The 2026-08 agentic execution review names a mandatory,
scope-aware gate as the single change that turns scope from honour-based into
enforced for any agent (section 11 item 2), and principle 2 of the target
architecture puts scope enforcement on the diff.

## Behavior

- Trigger: the managed workflow runs for a `pull_request` event whose body
  selects a work order.
- Response: the workflow computes the changed-path set as the Git difference
  between the pull request's base and head, including added files, evaluates
  `QGP-G4I-PATHS` over it against the selected work order's
  `[execution_scope].paths`, and the required check fails when any path is
  outside scope, whether or not a restitution trailer is present.
- On failure: when no work order can be selected from the body, the required
  check fails and names the missing trailer; it never passes by absence of
  input.

## Assumptions and dependencies

- The change set on the runner comes from REQ-ECP-002's `--from-git` reading,
  with the merge base as `<base>`.
- The check is configured as required on `main`; making it required is a
  repository setting the consumer applies, which the template documents.
- A path outside scope that the owner intends is fixed by a scope amendment,
  never by a gate bypass.

## Acceptance examples

Executable scenarios live in `acceptance/REQ-ECP-006.feature` and are named by
the verification contract that covers this requirement.

### Example: normal behavior

**Given** a pull request selecting `WO-X-004` changes only paths inside its
scope and carries no restitution trailer.

**When** the managed workflow runs on the `pull_request` event.

**Then** `QGP-G4I-PATHS` is `pass` and the required check is green.

### Example: failure behavior

**Given** the pull request also adds `docs/other.md`, outside scope.

**When** the workflow runs.

**Then** the required check is red, the log names `docs/other.md` and `WEX201`,
and the pull request cannot merge under the branch rule.

## Open decisions

None.
