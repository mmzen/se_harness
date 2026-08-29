+++
id = "VER-ECP-009"
type = "verification"
title = "Independent evidence for the scope checkpoint and the state-independent gate"
status = "draft"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[relations]
verifies = ["REQ-ECP-020"]
+++

# Verification Contract: Independent evidence for the scope checkpoint and the state-independent gate

## Independence

Expected behaviour derives from `REQ-ECP-020` and the `ECP-SCP-` rules of
`SPEC-ECP-009`. The checkpoint tests drive `harnessctl check` through the
CLI on fixture repositories whose work orders are placed in each lifecycle
state by the test, not by the code under test; the workflow test reads the
template's step text against the rules; the hosted reading is the pull
request of the work order itself, which carries its own completion and
verification and so is the case that was red before.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-ECP-020` the scope checkpoint | test: `check --checkpoint scope --from-git` on a fixture work order in `draft`, `approved`, `in_progress`, `implemented` (with a ready and with a verified record), `verified` | `tests/test_workflow_execution.py` | every state completes on an in-scope diff and blocks on `QGP-G4I-PATHS` with `WEX201` on an out-of-scope diff; exactly the three scope predicates are reported; a VREC or RLS is refused with `WEX210`; no `handoff.json` is written |
| `REQ-ECP-020` the handoff checkpoint unchanged | test: existing handoff cases | `tests/test_workflow_compliance.py`, `tests/test_workflow_execution.py` | every existing handoff assertion still passes; the eight predicates are still evaluated at handoff |
| `REQ-ECP-020` the managed step | test: the template's step text | `tests/test_ci_pipeline.py` | the step runs the scope check unconditionally, runs the handoff check only when the state reads `in_progress`, compares a declared digest only then, and logs the bound-at-handoff line otherwise |
| `REQ-ECP-020` hosted | demonstration: this work order's own pull request | the managed lane at the completion and verification heads | the required check passes at the head that carries the completion transition and at the head that carries the verified record |
| `SPEC-ECP-009` documentation | inspection and test | `docs/notes/harnessctl-check.md`, managed policy documents | the five checkpoints are named; the check note's tables carry `scope` |

## Acceptance scenarios

### Scenario 1: every state, in scope

For each state above, run the scope check with an in-scope Git diff. Assert
`completed` and exactly `QGP-G4I-SCOPE`, `QGP-G4I-COMPLETE`, `QGP-G4I-PATHS`
in the gate result.

### Scenario 2: every state, out of scope

For each state, run it with one out-of-scope path. Assert `blocked`, the
`QGP-G4I-PATHS` message naming the path with `WEX201`, and the outcome
independent of the state.

### Scenario 3: the checkpoint is a work-order checkpoint

Run the scope check on a verification record. Assert `WEX210`.

### Scenario 4: nothing is written

Run the scope check with `--from-git` on an `in_progress` work order. Assert
no `handoff.json` appears; run the handoff check and assert it does.

### Scenario 5: the step

Parse the template step. Assert the scope check has no state guard, the
handoff check is guarded on `in_progress`, and the digest comparison sits
inside that guard.

### Scenario 6: hosted, this work order

Record the managed lane's conclusion at the pull request heads that carry
`WO-ECP-013`'s completion and its verified record. Assert both pass.

## Static and architecture checks

- `se_harness/workflow_contract.json` and `se_harness/quality_gates_contract.json`
  equal their template copies byte for byte.
- The predicate identifiers and evaluators of `QG-G4-IMPLEMENTATION-EVIDENCE`
  are unchanged.

## Evidence retention

Under `docs/engineering/execution-control-plane/evidence/WO-ECP-013/`: the
handoff packet with the test figures per host and the hosted lane readings
at the completion and verification heads.

## Pass criteria

Every deterministic test passes on the Linux lane. Scenario 6 is read from
the pull request. Graph and integrity readings come from the exact released
evaluator, se-harness 0.9.0, installed outside the checkout.

## Residual uncertainty

Scenario 6 can only be observed once the release carrying this change
governs a repository; on this repository's 0.9.0 root, the managed lane
still runs the old step, so the hosted reading of this work order's own
pull request is the *old* behaviour and is recorded as such. The new step is
demonstrated by the template test and by a consumer rehearsal in the
evidence.
