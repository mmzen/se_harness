+++
id = "WO-ECP-009"
type = "work_order"
title = "One precondition engine: transition evaluates the contract's gates"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-08-28"
updated = "2026-08-28"

[assurance]
commit_bound_verification = "required"
rationale = "The work routes every lifecycle transition through the contract's gate evaluator and deletes two private precondition implementations. A wrong change either applies a transition on a weaker set than check evaluates or blocks every transition; both are trusted engineering state that every later verification and release decision depends on, so commit-bound assurance is required."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/workflow.py",
  "se_harness/workflow_compliance.py",
  "se_harness/workflow_contract.py",
  "se_harness/cli.py",
  "se_harness/quality_gates_contract.json",
  "templates/repository/standard/docs/engineering/QUALITY_GATES.json",
  "templates/repository/standard/docs/engineering/QUALITY_GATES.md",
  "templates/repository/standard/docs/engineering/WORKFLOW.md",
  "tests/",
  "docs/engineering/execution-control-plane/evidence/",
  "docs/notes/harnessctl-reference.md",
  "docs/engineering/workflow-execution/specifications/SPEC-WEX-002.md",
]

[relations]
implements = ["REQ-ECP-009"]
specifications = ["SPEC-ECP-005"]
architecture = ["ARCH-ECP-001", "ADR-ECP-004"]
verification = ["VER-ECP-005"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T12:40:49Z"
decided_by = "engineering-owner"
reason = "Approved on 2026-08-28 by the accountable owner, 'go WO-ECP-009', after #239 merged WO-ECP-005 and VREC-ECP-005. Authorizes only the listed execution scope: plan_transition evaluating the contract's transition bindings through the gate evaluator with one context builder, _validate_preconditions reduced to the graph-structural list reported as QGS- predicates, ensure_governed_checkpoint reduced to its contract-load and integrity refusals, predicate-level checkpoints and the transition bindings in the quality-gates contract and its managed renderings, check --checkpoint transition --target as a public preview, one preflight-diagnostic filter, refusals labelled by predicate, tests and evidence. Start, completion, commit-bound verification and release are separate decisions."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-28T12:40:51Z"
decided_by = "engineering-owner"
reason = "Started on 2026-08-28 by the accountable owner in the same decision as the approval, 'go WO-ECP-009'. Execution is confined to the approved scope."
+++

# Work Order: One precondition engine: transition evaluates the contract's gates

## Lifecycle

Draft. Split out of `WO-ECP-005` on 2026-08-28, on the review of issue #212,
so that the schema deletion and this contract-semantics change are verified
separately. Approval authorizes only the scope below. Start, completion,
commit-bound verification, the assurance-owner decision, integration, and
release are separate decisions. Approval of `REQ-ECP-009`, `SPEC-ECP-005`,
`ARCH-ECP-001`, `ADR-ECP-004`, and `VER-ECP-005` precede approval of this
work order; `WO-ECP-005` precedes it (one result path to render the gate
results into), and `WO-ECP-006` depends on it.

## Objective

End every disagreement between `check` and `transition` on the same state.
Today `plan_transition` hard-codes its preconditions
(`se_harness/workflow.py:685-750`), `ensure_governed_checkpoint`
re-implements two gate predicates by string
(`se_harness/workflow_compliance.py:740`), the gate contract's `transition`
checkpoint is declared on ten of eleven gates and evaluated by nothing
(`check_workflow` refuses it at `:395`), and the two preflight-diagnostic
filters differ, so `check` accepts a work order that `transition` blocks on
`I001 lock-entry:*`. `QUALITY_GATES.md` `QG-010` promises a recheck that does
not happen.

## In scope

- `plan_transition` building one `CheckpointContext` per transitioned
  artifact with `checkpoint = "transition"`, the target state and an empty
  change set, through the same builder `check_workflow` uses, and evaluating
  the `transition` bindings for that edge with `_gate_results`
  (`ECP-KRN-004`).
- `_validate_preconditions` reduced to the closed graph-structural list of
  `SPEC-ECP-005`'s Terms, each reported as a `QGS-` predicate
  (`ECP-KRN-005`); `ensure_governed_checkpoint` reduced to its contract-load
  and repository-integrity refusals.
- Predicate-level `checkpoints` in `se_harness/quality_gates_contract.json`
  and its managed renderings; the `transition` bindings of the
  `ECP-KRN-005` edge table; `QGP-G4I-COMPLETE` and `QGP-G4I-PATHS` bound to
  `pre-action` and `handoff` only; the contract version incremented and
  `WEX-ECP-030` on an unbound edge (`ECP-KRN-009`).
- `check --checkpoint transition --target <state>` as a public read-only
  preview (`ECP-KRN-006`).
- One preflight-diagnostic filter, the compliance module's
  (`ECP-KRN-007`), and the two conformance tests: `transition` planning
  equals `check --checkpoint transition --target` on `compliance.gates` for
  every fixture state; `check --checkpoint handoff` is a superset for
  `-> implemented` (issue #212, criterion 2).
- Transition refusals carrying the refusing predicate's identifier;
  `_repository_workflow_error` classifying by typed exception
  (`ECP-KRN-008`).
- `QG-010` in `QUALITY_GATES.md` restated as what the code does.
- Tests; work-order-keyed evidence.

Amended on 2026-08-28 by the accountable owner during execution, on the
implementer's escalation ("Amend scope, include both"):
`docs/notes/harnessctl-reference.md` and
`docs/engineering/workflow-execution/specifications/SPEC-WEX-002.md` are added
to the execution scope, so the reference describes the
`check --checkpoint transition --target` preview and the specification's
line naming `se-harness-quality-gates-v1` carries a dated amendment to the v2
contract this work order ships. No other scope change.

## Out of scope

- Any new predicate evaluator or gate identifier; any change to a predicate's
  meaning, to lifecycle states or to decision rights; the root managed
  `QUALITY_GATES.*` and `WORKFLOW.md` copies; the schema-1 deletion
  (`WO-ECP-005`); authenticated decisions (`WO-ECP-004`); the delegation
  class (`WO-ECP-006`); folding `focus` into `check` (#225); any lifecycle
  transition of any artifact.

## Authorized decision envelope

The implementation agent may decide the `QGS-` identifiers and wording of the
graph-structural predicates, how the empty change set is represented in the
`transition` context, and test and fixture names. It may not add a predicate
evaluator, weaken any existing predicate, bind a change-set predicate to
`transition`, or write outside the listed paths.

## Constraints

- Python 3.11+ standard library only.
- Use the exact released evaluator, installed outside the checkout, for
  identity, integrity, graph, focus, and preflight readings; exercise the
  candidate `transition` only against temporary repositories.
- Root managed copies are not edited; LF line endings.
- Stage every change before any preflight or check run.

## Expected change surface

`plan_transition` and `_validate_preconditions` in the workflow kernel, the
compliance module's checkpoint entry and context builder, the contract
loader, the CLI error classification, one gate contract and its two template
renderings, `WORKFLOW.md`'s `QG-010` text, tests, evidence.

## Required verification

Execute the `VER-ECP-005` rows and scenarios that name `REQ-ECP-009`, plus
the repository-required checks; run the complete suite on Linux and Windows
with figures labelled per platform.

## Evidence to record

Under `docs/engineering/execution-control-plane/evidence/WO-ECP-009/`:
paired `check --checkpoint transition` and `transition` results per fixture
state, the `handoff`-superset comparison, the mutated contract copy and its
outcome, refusal diagnostics, per-platform test figures, and the complete
changed-path set.

## Stop and escalate conditions

Stop if an edge of the lifecycle registry cannot be bound without a new
predicate evaluator, if a `transition` predicate would need an input the
command does not receive, if the released evaluator refuses the edited gate
contract, or if any path outside scope must change.

## Completion report format

Return the `harnessctl check . --artifact WO-ECP-009 --checkpoint handoff`
schema-2 block verbatim with the complete changed-path set asserted, and
its `result_sha256`.
