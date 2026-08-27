+++
id = "REQ-ECP-009"
type = "requirement"
title = "Transitions evaluate the contract's gates"
status = "draft"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-27"
updated = "2026-08-27"
statement = "WHEN `harnessctl transition` plans a lifecycle edge, THE SYSTEM SHALL evaluate the `transition` checkpoint gates declared in `QUALITY_GATES.json` through the same gate evaluator that `check` uses, in place of any command-private precondition set."
verification_method = ["test"]
priority = "must"
source = "se_harness/workflow_compliance.py:395; QUALITY_GATES.md QG-010"

[relations]
derives_from = ["CAP-ECP-002"]
+++

# Requirement: Transitions evaluate the contract's gates

## Rationale

The gate contract's `transition` checkpoint is unreachable: `_gate_results` has
one caller, `check_workflow`, which refuses `transition`
(se_harness/workflow_compliance.py:395, :460; docs/notes/agentic-execution-
review-2026-08.md:117-120). `QUALITY_GATES.md` `QG-010` promises that
transitions recheck contract predicates, but `plan_transition` never loads the
gate table (se_harness/workflow.py:685-750; docs/notes/agentic-execution-
review-2026-08.md:164-166). Three precondition implementations therefore exist,
and `check` and `transition` disagree on the same work order
(docs/notes/complexity-audit-2026-08.md:236-242). One engine is what makes the
promise true.

## Behavior

- Trigger: `harnessctl transition` plans any edge, with or without `--apply`.
- Response: the plan's preconditions are the predicates of the `transition`
  checkpoint in `QUALITY_GATES.json` for the target state, evaluated by the
  evaluator that serves `check`, plus graph-structural checks only; the result
  lists each predicate with its status, and the plan is blocked when any is
  `fail` or `not_assessable`.
- On failure: when the gate contract cannot be loaded or declares no
  `transition` checkpoint, the plan is refused rather than falling back to a
  private list.

## Assumptions and dependencies

- `QUALITY_GATES.json` gains a `transition` checkpoint per target state in the
  managed template; consumers receive it as a managed update.
- `check --checkpoint transition` becomes legal and reads the same predicates.
- Graph-structural checks (edge legality, stale input) stay in Python and are
  reported as predicates too.

## Acceptance examples

Executable scenarios live in `acceptance/REQ-ECP-009.feature` and are named by
the verification contract that covers this requirement.

### Example: normal behavior

**Given** `WO-X-004` satisfies every `transition` predicate for `implemented`.

**When** `harnessctl transition . --artifact WO-X-004 --to implemented` runs.

**Then** the plan lists each contract predicate as `pass`, and `check .
--artifact WO-X-004 --checkpoint transition` reports the identical list.

### Example: failure behavior

**Given** `review_evidence_available` is `fail` for `WO-X-004`.

**When** the same command runs with `--apply`.

**Then** no file changes; the result names `review_evidence_available` as `fail`
with the same corrective form `check` emits, and no private precondition code is
reported.

## Open decisions

None.
