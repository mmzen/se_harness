+++
id = "ADR-ECP-004"
type = "adr"
title = "One result schema, one rule selector, one precondition engine"
status = "draft"
owners = ["technical-owner", "repository-owner"]
created = "2026-08-27"
updated = "2026-08-28"

[relations]
decides = ["ARCH-ECP-001"]
+++

# ADR: One result schema, one rule selector, one precondition engine

## Status

Proposed.

## Context

The workflow core carries two result envelopes with a lossy projection
(`se_harness/workflow.py:99-142`; `se_harness/workflow_result.py:210-285`),
inconsistent `--result-schema` defaults (`se_harness/cli.py:999`, `:1042`,
`:1241`, `:1323`), two rule engines that compute `successor_id` differently
(`se_harness/workflow.py:355-399`; `se_harness/workflow_contract.py:554-595`),
and three precondition implementations: `_validate_preconditions`
(`se_harness/workflow.py:685-750`), the never-evaluated `transition`
checkpoint (`se_harness/workflow_compliance.py:395`, `:460`), and
`ensure_governed_checkpoint` matching predicate ids as strings
(`docs/notes/complexity-audit-2026-08.md`, P0-6). `check` accepts a work
order that `transition` blocks on `I001 lock-entry:*`; the CLI labels every
transition failure `WEX201` (`se_harness/cli.py:521`); `QG-010` promises a
recheck that does not happen (`docs/engineering/QUALITY_GATES.md:26-29`).

## Decision drivers

- `check` and `transition` must be unable to disagree on the same state.
- `result_sha256` must be defined for every result an agent can quote.
- `QG-010` must be true of the code.
- Gate predicates belong in `QUALITY_GATES.json`, where the installed
  contract and `WORKFLOW.md` can index them (`ADR-ADS-001`).
- Delete rather than adapt: schema 1 has no consumer.

## Considered options

### Option A: keep both schemas and both engines, add cross-checks

Add tests asserting agreement between `_recommend` and `select_rule` and
between `_validate_preconditions` and the gate table. Consequences: the
divergence is measured, not removed; every contract edit is two edits; the
schema-1 projection keeps fabricating `PROC-COMPATIBILITY`.

### Option B: schema 2 only, `select_rule` only, gates evaluated by `plan_transition`

Delete the schema-1 builder and projection and the `--result-schema`
option; `_recommend` delegates to `select_rule`; `plan_transition` calls
`_gate_results` for the `transition` checkpoint and keeps only
graph-structural checks in Python; `check --checkpoint transition` becomes a
public read-only preview. Consequences: one evaluation path; a
quality-gates contract version bump; installed contracts regenerate; every
transition refusal gets the predicate's own code.

### Option C: move transition preconditions into `WORKFLOW.json` steps

Express preconditions as step gates on the `STEP-*-APPLY` rows. Consequences:
keeps predicates in the procedure contract rather than the gate contract,
duplicating the gate table's binding, and leaves `_validate_preconditions`
for edges with no procedure.

## Decision

Select Option B (`SPEC-ECP-005`, `ECP-KRN-001` to `ECP-KRN-010`). The kernel
is `select_rule`, `select_current_step`, `_gate_results`, `build_result`,
and `TransitionPlan`; every command is a rendering of it; no command holds a
private precondition set.

## Consequences

- Positive: every `check` and `transition` disagreement of the audit closes;
  `QG-010` becomes a tested property; refusals carry real codes.
- Negative: schema-1 consumers, if any exist outside this repository, break
  at the upgrade; the review found none.
- Operational: `QUALITY_GATES.json` gains the `transition` checkpoint and
  its version increments; `QUALITY_GATES.md`, `WORKFLOW.json`, `WORKFLOW.md`,
  and `OPERATING_CARD.md` regenerate on upgrade; `--result-schema` is removed
  outright (amended 2026-08-28, see Migration).
- Security: a transition can no longer apply on a weaker precondition set
  than `check` evaluates.
- Migration: two work orders. `WO-ECP-005` removes schema 1 and the second
  selector (REQ-ECP-010) and retires by dated amendment the three approved
  artifacts that govern schema 1 — `SPEC-ADS-001` `ADS-NXT-002`,
  `REQ-ADS-002`, `SPEC-WEX-002` — so the earlier statement that no approved
  artifact needs an amendment is withdrawn on 2026-08-28. `WO-ECP-009` routes
  `transition` through the gate evaluator (REQ-ECP-009) and is what
  `WO-ECP-006` depends on. Splitting them keeps a mechanical deletion apart
  from a contract-semantics change under commit-bound verification.
- Amended on 2026-08-28: no `--result-schema 2` no-op and no `W-ECP-004`;
  the option is removed outright. Checkpoint membership becomes declarable
  per predicate so `transition` never evaluates a predicate whose input it
  does not receive.

## Validation

`ECP-KRN-003` and `ECP-KRN-007` equality tests across commands for every
fixture state; `ECP-KRN-009` contract-loading failure on an unbound edge; a
grep test that `legacy_to_schema2` and `--result-schema` are absent from
the wheel; the installed-contract byte-identity test for the regenerated
files on Linux and Windows.
