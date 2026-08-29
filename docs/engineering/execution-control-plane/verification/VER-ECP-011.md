+++
id = "VER-ECP-011"
type = "verification"
title = "Independent evidence for the checkpoint-less check projection"
status = "draft"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[relations]
verifies = ["REQ-ECP-022"]
+++

# Verification Contract: Independent evidence for the checkpoint-less check projection

## Independence

Expected behaviour derives from `REQ-ECP-022` and the `ECP-ONE-` rules of
`SPEC-ECP-011`. The identity tests compare two CLI invocations' JSON on
fixture repositories the test places in each lifecycle state; the contract
test parses `WORKFLOW.json` and the reference rather than trusting prose;
the alias test compares the alias's bytes with a fixture captured before
the change.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-ECP-022` the projection | test: `check --artifact` without a checkpoint for a WO in `approved`, `in_progress`, `implemented` (with and without a ready record), `verified`, a VREC `ready` and an RLS `ready` | `tests/test_workflow_execution.py` | `operation.kind` `check`, no gate, no write; every other section byte-identical to `focus`'s |
| `REQ-ECP-022` refusals | test: a requirement id; `--from-git` without a checkpoint | same | `WEX210` naming the cause |
| `REQ-ECP-022` the alias | test: `focus` output against a fixture captured before the change; stderr carries the notice | `tests/test_workflow_execution.py` | bytes identical; exit status unchanged |
| `SPEC-ECP-011` contracts and surface | test: no step argv names `focus`; `WFL-003` names `check`; `orient.py` invokes `check`; the reference names `focus` once | `tests/test_workflow_documentation_contract.py`, `tests/test_agentic_execution.py`, `tests/test_progressive_documentation.py` | as stated |
| `SPEC-ECP-011` no regression | test: every existing `focus`, `next` and `check` assertion | the existing modules | unchanged and passing |

## Acceptance scenarios

### Scenario 1: identity

For each state above, run `check --artifact ID --json` and `focus
--artifact ID --json`; assert equality of every top-level section except
`operation.kind` and `result_sha256`, and assert `compliance.gates == []`.

### Scenario 2: the alias's bytes

Capture `focus` stdout and `--json` on the fixture before the change into a
test fixture; after the change assert equality and assert one stderr line
naming `check`.

### Scenario 3: the contract

Parse `WORKFLOW.json`; assert no `argv` contains `focus`; assert the five
renamed steps keep their identifiers and gate bindings.

### Scenario 4: the shipped skill

Run `orient.py` under a subprocess trace; assert the traced argv invokes
`check` and no `focus`.

## Evidence retention

Under `docs/engineering/execution-control-plane/evidence/WO-ECP-015/`.

## Pass criteria

Every deterministic test passes on the Linux lane; the Windows workstation
reading is at its baseline. Graph and integrity readings come from the
exact released evaluator, se-harness 0.10.0, installed outside the
checkout.

## Residual uncertainty

The alias's removal is a later work order; until then two names remain in
the CLI's help.
