+++
id = "VER-ECP-005"
type = "verification"
title = "Independent evidence for one kernel: schema 2, one selector, one precondition engine"
status = "draft"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[relations]
verifies = ["REQ-ECP-009", "REQ-ECP-010"]
+++

# Verification Contract: Independent evidence for one kernel: schema 2, one selector, one precondition engine

## Independence

Expected behaviour derives from `REQ-ECP-009`, `REQ-ECP-010`, and the
`ECP-KRN-` rules of `SPEC-ECP-005`, read against `ARCH-ECP-001` and the
proposed outcome of `ADR-ECP-004`. The oracle for gate evaluation is the
`transition` checkpoint of `QUALITY_GATES.json` read by the test, and the
oracle for the next step is `select_rule` applied by the test to a context
it builds. Schema conformance is checked against the schema-2 shape the
template CI already consumes, not against candidate output.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-ECP-009` transitions evaluate the contract gates | test: `transition` plan on a work order that `check` blocks; on one `check` passes; with one `transition`-checkpoint predicate added to a copy of the contract | fixture repository where `check` demands content-bound evidence while `transition` today needs only a keyed file (the 2026-08 agentic execution review, section 5, weakness 4) | `transition` and `check` agree on every predicate status for the same artifact and snapshot; a predicate added to the contract's `transition` checkpoint is evaluated without any code change; no command-private precondition set remains reachable |
| `REQ-ECP-010` one schema, one selector | test: `--json` on `focus`, `check`, `transition`, `capture-verification`, `prepare-release` | every state in the state table | each result validates as schema 2 with `result_sha256`; `--result-schema 1` is refused with a coded diagnostic; `next` fields from `_recommend` equal `select_rule` for every state |

## Acceptance scenarios

### Scenario 1: check and transition agree

Build the fixture on which today `check` accepts and `transition` blocks on
`I001 lock-entry:*` (review section 5, weakness 4). Assert equal predicate
statuses from both commands.

### Scenario 2: contract change moves transition

Copy `QUALITY_GATES.json`, add a predicate to the `transition` checkpoint
that fails on the fixture. Assert `transition` blocks naming it.

### Scenario 3: failure path, schema 1 requested

Run each of the five commands with `--result-schema 1`. Assert refusal, one
diagnostic, no side effect (today `transition`, `capture-verification`, and
`prepare-release` default to schema 1; complexity audit P0-6,
`docs/notes/complexity-audit-2026-08.md:224-233`).

### Scenario 4: one selector

For every state, assert the `next` computed by the plan path equals the
`next` computed by `select_rule` over the same context, including
`successor_id` (today the two context builders compute it differently;
audit P0-6).

### Scenario 5: failure path, transition on a blocked gate

Attempt `transition --apply` where a `transition` predicate fails. Assert
refusal with the predicate identifier, not a generic `WEX201`
(`se_harness/cli.py:521` today labels every failure `WEX201`).

## Property and invariant tests

- For random valid contexts, `_recommend(ctx)` equals `select_rule(ctx)`.
- Every result from the five commands round-trips through the canonical
  renderer to the same `result_sha256`.

## Static and architecture checks

- `legacy_to_schema2` and the schema-1 `handoff` renderer are absent from
  `se_harness/`; `grep -n "result_schema" se_harness/cli.py` shows no
  default of `1`.
- `_validate_preconditions` in `se_harness/workflow.py` contains only
  graph-structural checks; no gate predicate name remains in it.
- `check_workflow` in `se_harness/workflow_compliance.py` no longer refuses
  the `transition` checkpoint for the internal caller (today
  `se_harness/workflow_compliance.py:395`).

## Security and privacy checks

- Refusing schema 1 leaks no partial result to stdout.

## Performance and resilience checks

- `transition` plan time is within twice the `check` time at the same
  snapshot, both platforms, recorded.

## Manual assessments

None.

## Evidence retention

Under `docs/engineering/execution-control-plane/evidence/<WO-ID>/`: the
paired `check` and `transition` results per fixture, the mutated contract
copy and its outcome, the refusal diagnostics, and per-platform test
figures.

## Pass criteria

Every deterministic test passes on Linux and on Windows, figures labelled per
platform. The template CI selector continues to consume the schema-2 block
unchanged. Graph and identity readings are taken with the exact released
evaluator, se-harness 0.7.1, installed outside the checkout.

## Residual uncertainty

Consumers pinned to an older evaluator never see this schema change, since
the evaluator is version-pinned; no cross-version JSON contract is claimed.
