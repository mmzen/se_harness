+++
id = "REQ-ECP-001"
type = "requirement"
title = "One call returns the complete execution context"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-27"
updated = "2026-08-28"
statement = "WHEN an actor runs `harnessctl next` for a repository, THE SYSTEM SHALL return in one schema-2 result the selected artifact and its state, the governing chain, the declared execution scope, the phase reading manifest, the exact next command, and any decision required."
verification_method = ["test"]
priority = "must"
source = "the 2026-08 agentic execution review, section 6"

[relations]
derives_from = ["CAP-ECP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T12:03:40Z"
decided_by = "requirements-steward"
reason = "Approved on 2026-08-28 by the accountable owner, 'I approve the ECP definitions and WO-ECP-005', as part of the execution-control-plane definition packet of #231 with the issue #212 amendments of #238 applied. Approval of a definition authorizes no work; each work order is approved separately."
+++

# Requirement: One call returns the complete execution context

## Rationale

Today the agent is the state machine's memory. The next step is emitted only
after an operation (`restitution.next`), `focus` gives the decision step rather
than the `check` command, and no `next` or session command exists
(docs/notes/agentic-execution-review-2026-08.md:306). Reaching the third human
decision on WO-REB-027 took seventeen commands, and the agent alone chose the
checkpoint, the procedure, and which `check` invocation fit the state
(docs/notes/agentic-execution-review-2026-08.md:283-286). The wrong choice
reproduces live: `check --checkpoint start` on an implemented work order returns
`WEX210` with a corrective that names its own command, while the correct call is
nowhere suggested (docs/notes/agentic-execution-review-2026-08.md:143-148). The
2026-08 agentic execution review ranks one `next` call as the change with the
most leverage on agent load (section 6, and section 11 item 1). The obligation
is that the harness, not the agent, holds selection, scope, reading set, and
next command.

## Behavior

- Trigger: `harnessctl next REPO` runs, with or without `--artifact ID`.
- Response: one schema-2 result whose block carries the selected artifact and
  its `status`, the governing chain, the `[execution_scope].paths` declared on
  the selected work order, the reading manifest for the current phase, the exact
  next `harnessctl` argv, and, when a human decision is the next step, the
  decision right and role that must decide.
- On failure: when no artifact can be selected or the repository does not
  validate, the result is still schema 2, names the reason as a coded predicate,
  and its corrective is not `harnessctl next` itself.

## Assumptions and dependencies

- The existing kernel already computes each piece separately: `focus_schema2`,
  `run_preflight`, and `select_current_step`
  (docs/notes/agentic-execution-review-2026-08.md:405-409).
- Result schema 2 and `result_sha256` remain the canonical envelope
  (REQ-ECP-010).
- The reading manifest is the trimmed form required by REQ-ECP-015.

## Acceptance examples

Executable scenarios live in `acceptance/REQ-ECP-001.feature` and are named by
the verification contract that covers this requirement.

### Example: normal behavior

**Given** `WO-X-004` is `in_progress`, its scope declares three paths, and the
repository validates.

**When** the actor runs `harnessctl next . --artifact WO-X-004`.

**Then** one schema-2 result names `WO-X-004`, `in_progress`, its chain up to
the intent, the three paths, the `execute` phase manifest, and the argv
`harnessctl check . --artifact WO-X-004 --checkpoint handoff --from-git BASE`;
`decision_required` is empty.

### Example: failure behavior

**Given** `WO-X-004` is `implemented` and its verification record is `ready`.

**When** the actor runs `harnessctl next . --artifact WO-X-004`.

**Then** the result's next command is empty, `decision_required` names `DR-VREC-
DECIDE` and `assurance-owner`, and no corrective repeats `harnessctl next`.

## Open decisions

None.
