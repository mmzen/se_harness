+++
id = "REQ-ECP-026"
type = "requirement"
title = "The managed lane reads the declarations from the live pull-request body"
status = "draft"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-30"
updated = "2026-08-30"
statement = "WHEN the managed pull-request lane selects a declared Harness-Work-Order or Harness-Restitution field, THE SYSTEM SHALL read the declaration from the pull request's current body fetched from the hosting API during the run, so that a corrected body is honoured by a re-run without a new push."
verification_method = ["test"]
priority = "must"
source = "Issue #280 (functional assessment of 2026-08-30, section 3.3); the no-op push 9126f20 on PR #277"

[relations]
derives_from = ["CAP-ECP-001"]
+++

# Requirement: The managed lane reads the declarations from the live pull-request body

## Rationale

The managed workflow selects the `Harness-Work-Order` and
`Harness-Restitution` declarations with `select-work-order --event`, and it
passes the stored GitHub event payload. That payload is a snapshot from the
moment the run was triggered: when a body is corrected after the pull
request is opened, the stored snapshot still carries the wrong text, so the
check stays red until a new push produces a new event. PR #277 needed the
no-op push `9126f20` for exactly this. The assessment of 2026-08-30 lists
the stored payload among the hidden prerequisites that produce confusing
refusals, and `AGENTS.md` carries it as a trap.

The declarations name repository state; nothing about them depends on the
event snapshot. Reading the body as it is now makes the red check honest
("the body is wrong") instead of sticky ("the body was wrong when you
pushed"), and makes the recovery a re-run instead of a push.

## Behavior

- Trigger: a run of the managed lane on a `pull_request` event reaches a
  step that selects a declared field from the pull-request body.
- Response: the body text handed to the selector is the pull request's
  current body, obtained from the hosting API during the run with the
  workflow's own read token; a body corrected after the trigger is selected
  as corrected when the run is re-run.
- On failure: if the API fetch fails, the lane fails at the fetch step with
  the transport or HTTP error, and no declaration is selected from any
  stored snapshot in its place.

## Assumptions and dependencies

- The selector's own rules are unchanged: exactly one standalone
  `Harness-Work-Order` line, at most one `Harness-Restitution` line, the
  size bound, and the carriage-return diagnosis stay as they are.
- The change-set inputs of the scope and handoff checks are unaffected:
  the base commit and the event-name guards keep coming from the trigger
  context, never from the body.
- The hosting API returns the pull request's current state to its own
  workflow token on both same-repository and fork pull requests.
- The hash-locked root copy of this repository keeps the released stored
  payload behaviour until the next root adoption.

## Acceptance examples

Executable scenarios live in the covering verification contract,
`VER-ECP-017`.

### Example: normal behavior

**Given** a pull request whose body was opened with a wrong
`Harness-Work-Order` line and corrected afterwards without a new push.

**When** the managed lane's failed run is re-run.

**Then** the selection step reads the corrected body from the API and the
work-order selection succeeds.

### Example: failure behavior

**Given** a run in which the API fetch for the pull request fails.

**When** the selection step would otherwise execute.

**Then** the lane fails at the fetch step and does not fall back to the
stored event payload.

## Open decisions

None.
