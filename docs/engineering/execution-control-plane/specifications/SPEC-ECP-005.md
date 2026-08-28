+++
id = "SPEC-ECP-005"
type = "specification"
title = "One kernel: schema 2, one selector, one precondition engine"
status = "draft"
owners = ["technical-owner", "quality-owner", "repository-owner"]
created = "2026-08-27"
updated = "2026-08-28"

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
  artifact graph shape alone and not of any gate predicate. The closed list:
  edge legality from the lifecycle registry; a complete assurance
  classification before a work order is approved; an eligible verification
  record covering a work order before it is verified; an eligible release
  record covering a work order, and verified records under a release record,
  before either is released; supersession successor existence, type,
  eligibility and coverage. Every other precondition `_validate_preconditions`
  carries today has an evaluator in `_evaluate` and moves to the gate table
  (see the edge table under ECP-KRN-005).
- **Predicate checkpoint membership:** a predicate may declare its own
  `checkpoints`; when absent it inherits its gate's. The `transition`
  checkpoint binds only predicates whose inputs `transition` receives.
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
passing it, with either value, is an argument error. `legacy_to_schema2`, the
schema-1 `_result`/`_handoff` builders and `workflow.render_human`/`render_json`
are deleted, and the `handoff` block of every rule, the `failure.handoff` block
and `handoff_fields` are removed from `se_harness/workflow_contract.json` and
its managed rendering `WORKFLOW.json`; `restitution_fields` is the one result
vocabulary. The `harness-orient` skill adds `--result-schema 2` only when
`focus --help` advertises it, so it needs no change.

**ECP-KRN-003:** `_recommend` is deleted and every caller uses `select_rule`
with one context builder; `successor_id` is computed once, in that builder,
and a conformance test asserts `focus`, `check`, `next`, and `transition`
agree on `procedure.rule_id` for every fixture state.

**ECP-KRN-004:** `plan_transition` evaluates, for each transitioned
artifact, the gate ids bound to the `transition` checkpoint for the target
state in `QUALITY_GATES.json` through `_gate_results` with a
`CheckpointContext` built by the same function `check` uses, carrying
`checkpoint = "transition"` and the target state and an empty change set; a
predicate status other than `pass` blocks the plan and is rendered under
`Blocked by` with its corrective form. Predicates that need a declared change
set (`QGP-G4I-COMPLETE`, `QGP-G4I-PATHS`) declare `checkpoints` without
`transition` and are evaluated at `handoff` only, so `check --checkpoint
handoff` evaluates a superset of what `transition -> implemented` evaluates,
never a different set.

**ECP-KRN-005:** `_validate_preconditions` retains only the graph-structural
checks of the Terms section, each reported in the result as a predicate with
a `QGS-` identifier so a refusal always names its check; every other
precondition is a gate predicate that already has an evaluator and is bound
to the `transition` checkpoint for its target state. No new predicate
evaluator is introduced. The binding, by edge:

| Edge | Gate predicates at `transition` | Graph-structural |
| --- | --- | --- |
| definition `draft -> approved` | `QGP-G1-AUTHORING` / `QGP-G2-AUTHORING` (`authoring_ready`) | edge legality |
| release contract `draft -> approved` | `QGP-G5P-RELEASE-UNIT` (`release_unit_ready`) | edge legality |
| work order `draft -> approved` | `QGP-G3-GRAPH`, `QGP-G3-INTEGRITY` | assurance classification complete |
| work order `approved -> in_progress` | `QGP-G3-STATUS`, `-GRAPH`, `-INTEGRITY`, `-SCOPE`, `QGP-G3-PREFLIGHT` (`start_preflight_ready`) | edge legality |
| work order `in_progress -> implemented` | `QGP-G4I-STATUS`, `-GRAPH`, `-INTEGRITY`, `-SCOPE`, `-PREFLIGHT` (`review_preflight_ready`), `-EVIDENCE` (`review_evidence_available`) | edge legality |
| work order `-> verified` / `-> released` | `QGP-G4V-*` / `QGP-G5D-*` graph and integrity | eligible VREC / RLS coverage |
| verification record `ready -> verified` | `QGP-G4A-GRAPH`, `QGP-G4A-INTEGRITY` | edge legality |
| release record `ready -> released` | `QGP-G5D-STATUS`, `-GRAPH`, `-INTEGRITY` | verified VRECs included |
| verification record `-> superseded` | `QGP-G4A-GRAPH`, `QGP-G4A-INTEGRITY` | successor is an eligible VREC preserving coverage |

`ensure_governed_checkpoint` keeps only its contract-load and
repository-integrity refusals; its re-implementation of `QGP-G1/G2-AUTHORING`
and `QGP-G5P-RELEASE-UNIT` is deleted because the table above evaluates them.

**ECP-KRN-006:** `check_workflow` accepts `--checkpoint transition
--target <state>` as a public read-only checkpoint that renders the same
gate results `plan_transition` evaluates, so an agent can preview a
transition's gate outcome without a decision record.

**ECP-KRN-007:** The preflight-diagnostic filters of `workflow.py:668-682`
and `workflow_compliance.py:844-853` are one function, the one
`workflow_compliance.py` uses today (it is what the managed CI already
enforces); a conformance test asserts that `check --checkpoint transition
--target <state>` and `transition` (planning mode) return identical
`compliance.gates` for every fixture state, and that `check --checkpoint
handoff` returns a superset for `-> implemented`.

**ECP-KRN-008:** A transition refusal is rendered with the code of the
predicate or graph check that refused it; the blanket `WEX201` label on
every transition failure (`se_harness/cli.py:521`) is removed and
`_repository_workflow_error` classifies by typed exception, not message
substring.

**ECP-KRN-009:** `QUALITY_GATES.json` declares the `transition` checkpoint
bindings of the ECP-KRN-005 table, keyed by artifact type and target state,
and contract loading fails with `WEX-ECP-030` when an edge in the lifecycle
registry has no `transition` binding and no graph-structural check. Per-gate
`checkpoints` stays; `QGP-G4I-COMPLETE` and `QGP-G4I-PATHS` gain a
predicate-level `checkpoints` of `["pre-action", "handoff"]`.

**ECP-KRN-010:** `result_sha256` is defined for every result of
`ECP-KRN-001`, so a `transition` or `prepare-release` block can be quoted in
a pull-request body and recomputed.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-ECP-009 | ECP-KRN-004 to ECP-KRN-009 (`WO-ECP-009`) |
| REQ-ECP-010 | ECP-KRN-001 to ECP-KRN-003, ECP-KRN-008, ECP-KRN-010 (`WO-ECP-005`) |

## Inputs and outputs

Inputs: the existing command arguments minus `--result-schema`, plus
`check --checkpoint transition --target <state>`. Outputs: schema-2 results
only; `QUALITY_GATES.json` gains the `transition` bindings and
`QUALITY_GATES.md` indexes them; `WORKFLOW.json` loses its `handoff` blocks.

## Failure behaviour

Every rule fails closed: a missing `transition` binding fails contract
loading; a non-`pass` predicate blocks the plan before any write; a removed
option is an argument error. No rule creates, changes, or infers lifecycle
state.

## Compatibility and migration

Schema 1 is removed without a compatibility window and without a no-op
flag: the released evaluator is version-pinned, the template CI consumes only
schema 2, `result_sha256` binds only schema 2
(`docs/notes/complexity-audit-2026-08.md`, P0-6), and the one skill that
passes `--result-schema 2` guards on `focus --help`. Installed
`QUALITY_GATES.json`, `QUALITY_GATES.md`, `WORKFLOW.json`, `WORKFLOW.md`, and
`OPERATING_CARD.md` regenerate on upgrade. The quality-gates contract version
increments; loading an older installed copy is `WEX-ECP-030` until the
consumer upgrades.

Three approved artifacts govern schema 1 today and are retired by dated
amendment in the form `WO-REB-028` used, under `WO-ECP-005`:
`SPEC-ADS-001` `ADS-NXT-002` (the `--result-schema 1` rendering and its
`WEX-ADS-002` warning), `REQ-ADS-002` (its schema-1 acceptance example), and
`SPEC-WEX-002` (the compatibility window and "schema-1 behaviour remains
governed"). `SPEC-CIP-001` line 96 mentions `[--result-schema 2]` on
`release-unit`, which has no such option; the amendment corrects it.

## Explicitly unspecified decisions

- The `QGS-` identifiers and wording of the graph-structural predicates.
- Whether `focus` remains a separate command or becomes an alias of
  `check --checkpoint focus`; the equality rules hold either way.
- Internal caching of validation between the plan and the apply, provided
  the stale-input check of `TransitionPlan` is kept.
