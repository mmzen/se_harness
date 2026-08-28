+++
id = "REQ-ECP-011"
type = "requirement"
title = "A delegation class unlocks transitions behind the gate"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-27"
updated = "2026-08-28"
statement = "WHERE a work order declares a delegation class, THE SYSTEM SHALL permit the delegated actor to apply `DR-WO-START`, `DR-WO-COMPLETE`, and `DR-VREC-PREPARE` transitions only while the required pull-request gate for the candidate is passing."
verification_method = ["test", "demonstration"]
priority = "must"
source = "review section 10, principle 5; ADR-AEX-006"

[relations]
derives_from = ["CAP-ECP-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T12:03:40Z"
decided_by = "requirements-steward"
reason = "Approved on 2026-08-28 by the accountable owner, 'I approve the ECP definitions and WO-ECP-005', as part of the execution-control-plane definition packet of #231 with the issue #212 amendments of #238 applied. Approval of a definition authorizes no work; each work order is approved separately."
+++

# Requirement: A delegation class unlocks transitions behind the gate

## Rationale

Phase 4 delegated execution is reachable but no formal work order carries
`[agentic_delegation]`, so `resolve_delegation` raises `AEXAUTH003` on every
real one; it has never run outside tests (docs/notes/agentic-execution-
review-2026-08.md:157-159). Its envelope guards a token that never leaves the
process that minted it, and the gates reaching the broker are caller-asserted
JSON (`gates_passed=True` at se_harness/delegated_workflow.py:399;
docs/notes/agentic-execution-review-2026-08.md:214-222). ADR-AEX-006 chose that
envelope. The 2026-08 agentic execution review's principle 5 replaces it:
delegation is a work-order attribute that unlocks `transition` for start,
completion, and record preparation when the gate is green, with no envelope and
no broker (section 10).

## Behavior

- Trigger: `harnessctl transition --apply` for `DR-WO-START`, `DR-WO-COMPLETE`,
  or `DR-VREC-PREPARE` is invoked by an actor named as delegated on the work
  order.
- Response: the transition is permitted when the work order's front matter
  declares a delegation class covering that right, the actor matches the class,
  and the required pull-request gate for the candidate commit is currently
  `success`; the appended event names the delegation class and the gate run it
  relied on.
- On failure: when the class is absent, the right is outside the class, the
  actor does not match, or the gate is `failure`, `pending`, or unobservable,
  the transition is refused with a coded predicate and no file changes; a human
  decision record remains the only other route.

## Assumptions and dependencies

- The gate state is read from the CI provider at the candidate head, or from
  a signed gate result the CI lane commits; both are fail-closed when absent.
- The delegation class is a small enumeration declared in the work-order
  template and `WORKFLOW.json`; the `[agentic_delegation]` table is retired.
- Human decision rights other than the three named stay human-only.

## Acceptance examples

Executable scenarios live in `acceptance/REQ-ECP-011.feature` and are named by
the verification contract that covers this requirement.

### Example: normal behavior

**Given** `WO-X-004` declares `delegation = "execute"`, the pull request for its
candidate is green on the required check, and the delegated actor is the CI
actor.

**When** `harnessctl transition . --artifact WO-X-004 --to implemented --apply`
runs as that actor.

**Then** `WO-X-004` becomes `implemented` and the event names the delegation
class and the passing gate run.

### Example: failure behavior

**Given** the same work order, and the required check is red.

**When** the same command runs.

**Then** no file changes, and the result names the failing gate run as the
refused predicate.

## Open decisions

None.
