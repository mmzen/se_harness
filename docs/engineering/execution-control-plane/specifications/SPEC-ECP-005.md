+++
id = "SPEC-ECP-005"
type = "specification"
title = "One kernel: schema 2, one selector, one precondition engine"
status = "draft"
owners = ["technical-owner", "quality-owner", "repository-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[relations]
specifies = ["REQ-ECP-009", "REQ-ECP-010"]
+++

# Specification: One kernel: schema 2, one selector, one precondition engine

## Scope

This specification consolidates the workflow core so that `focus`, `check`,
`transition`, `capture-verification`, and `prepare-release` render one
result schema from one rule selector and evaluate one precondition engine.
Today two result envelopes exist with a lossy projection between them
(`se_harness/workflow.py:99-142`; `se_harness/workflow_result.py:210-285`),
`--result-schema` defaults to 2 on `focus` and to 1 on the three mutators
(`se_harness/cli.py:999`, `:1042`, `:1241`, `:1323`), two rule engines select
the next step (`se_harness/workflow.py:355-399`;
`se_harness/workflow_contract.py:554-595`), and the `transition` checkpoint of
the gate contract is never evaluated because `_gate_results` has one caller
that refuses `transition` (`se_harness/workflow_compliance.py:395`, `:460`)
while `_validate_preconditions` hard-codes its own checks
(`se_harness/workflow.py:685-750`; `docs/notes/complexity-audit-2026-08.md`,
P0-6). `QUALITY_GATES.md` `QG-010` promises the recheck. No lifecycle edge
or decision right changes.

## Actors and external systems

- A coding agent and accountable owners read the results.
- The released evaluator computes them.
- `WORKFLOW.json` and `QUALITY_GATES.json` are the contracts.
- The managed CI workflow consumes `check --json`.

## Terms

- **Kernel:** the functions `select_rule`, `select_current_step`,
  `_gate_results`, `build_result`, and `TransitionPlan`.
- **Graph-structural check:** a precondition that is a property of the
  artifact graph shape alone (edge legality from the lifecycle registry,
  supersession target existence, successor uniqueness) and not of any gate
  predicate.
- **`transition` checkpoint:** the checkpoint of that name declared in
  `QUALITY_GATES.json`.

## Behavioral rules

### One kernel

**ECP-KRN-001:** Every workflow result of `focus`, `check`, `next`,
`transition`, `capture-verification`, and `prepare-release` is built by
`build_result` (`se_harness/workflow_result.py:68`) and carries `schema =
"se-harness-workflow-result-v2"`; no command constructs a result dictionary
elsewhere.

**ECP-KRN-002:** The `--result-schema` option is removed from every command;
passing it is an argument error, and `legacy_to_schema2` and the schema-1
`handoff` builder are deleted.

**ECP-KRN-003:** `_recommend` is deleted and every caller uses `select_rule`
with one context builder; `successor_id` is computed once, in that builder,
and a conformance test asserts `focus`, `check`, `next`, and `transition`
agree on `procedure.rule_id` for every fixture state.

**ECP-KRN-004:** `plan_transition` evaluates, for each transitioned
artifact, the gate ids bound to the `transition` checkpoint in
`QUALITY_GATES.json` through `_gate_results` with the same
`CheckpointContext` that `check` builds; a predicate status other than
`pass` blocks the plan and is rendered under `Blocked by` with its
corrective form.

**ECP-KRN-005:** `_validate_preconditions` retains only graph-structural
checks; every check expressible as a gate predicate (assurance
classification, start preflight, revision provenance, evidence presence,
scope) is declared in `QUALITY_GATES.json` under the `transition` checkpoint
and removed from Python.

**ECP-KRN-006:** `check_workflow` accepts `--checkpoint transition
--target <state>` as a public read-only checkpoint that renders the same
gate results `plan_transition` evaluates, so an agent can preview a
transition's gate outcome without a decision record.

**ECP-KRN-007:** The preflight-diagnostic filters of `workflow.py:668-682`
and `workflow_compliance.py:844-853` are one function, and a conformance
test asserts that `check --checkpoint transition` and `transition` (planning
mode) return identical `compliance.gates` for every fixture.

**ECP-KRN-008:** A transition refusal is rendered with the code of the
predicate or graph check that refused it; the blanket `WEX201` label on
every transition failure (`se_harness/cli.py:521`) is removed and
`_repository_workflow_error` classifies by typed exception, not message
substring.

**ECP-KRN-009:** `QUALITY_GATES.json` declares the `transition` checkpoint
with at least the gates `QG-G3-WORK-AUTHORIZATION` for `-> in_progress`,
`QG-G4-IMPLEMENTATION-EVIDENCE` for `-> implemented`, and the provenance
gate for `-> verified` and `-> released`, each keyed by the target state,
and contract loading fails with `WEX-ECP-030` when an edge in the lifecycle
registry has no `transition` gate binding.

**ECP-KRN-010:** `result_sha256` is defined for every result of
`ECP-KRN-001`, so a `transition` or `prepare-release` block can be quoted in
a pull-request body and recomputed.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-ECP-009 | ECP-KRN-004 to ECP-KRN-009 |
| REQ-ECP-010 | ECP-KRN-001 to ECP-KRN-003, ECP-KRN-007, ECP-KRN-008, ECP-KRN-010 |

## Inputs and outputs

Inputs: the existing command arguments minus `--result-schema`, plus
`check --checkpoint transition --target <state>`. Outputs: schema-2 results
only; `QUALITY_GATES.json` gains the `transition` checkpoint table and
`QUALITY_GATES.md` indexes it.

## Failure behaviour

Every rule fails closed: a missing `transition` binding fails contract
loading; a non-`pass` predicate blocks the plan before any write; a removed
option is an argument error. No rule creates, changes, or infers lifecycle
state.

## Compatibility and migration

Schema 1 is removed without a compatibility window: the released evaluator
is version-pinned, the template CI consumes only schema 2, and
`result_sha256` binds only schema 2 (`docs/notes/complexity-audit-2026-08.md`,
P0-6). `--result-schema 2` is accepted as a no-op for one release with
warning `W-ECP-004`. Installed `QUALITY_GATES.json`, `QUALITY_GATES.md`,
`WORKFLOW.json`, `WORKFLOW.md`, and `OPERATING_CARD.md` regenerate on
upgrade. The quality-gates contract version increments; loading an older
installed copy is `WEX-ECP-030` until the consumer upgrades.

## Explicitly unspecified decisions

- The exact partition of `_validate_preconditions` into graph-structural
  checks beyond the list in the Terms section.
- Whether `focus` remains a separate command or becomes an alias of
  `check --checkpoint focus`; the equality rules hold either way.
- Internal caching of validation between the plan and the apply, provided
  the stale-input check of `TransitionPlan` is kept.
