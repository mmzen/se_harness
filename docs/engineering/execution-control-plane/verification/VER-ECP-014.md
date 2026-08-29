+++
id = "VER-ECP-014"
type = "verification"
title = "Independent evidence for the Phase 4 removal and the retained journaled apply"
status = "draft"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[relations]
verifies = ["REQ-ECP-018"]
+++

# Verification Contract: Independent evidence for the Phase 4 removal and the retained journaled apply

## Independence

Expected behaviour derives from `REQ-ECP-018`, `ECP-DLG-008` of
`SPEC-ECP-006`, and the retention decision of `ADR-ECP-002`. `VER-ECP-006`
remains the contract for the whole of `SPEC-ECP-006`; this contract is the
subset a removal-only work order can execute — its scenario 7 and the
fault matrix of its scenarios 5 and 6 re-pointed at retained code — so
that the record binding the removal covers exactly what the removal did.
The wheel check installs a built wheel into a disposable environment and
walks it; the symbol census greps the package tree; the fault matrix injects
faults at each stage of the retained apply.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-ECP-018` no envelope in the CLI | test: recursive `harnessctl --help` walk | `tests/test_workflow_execution.py` or `tests/test_public_onboarding.py` | no `delegated-workflow`; `harnessctl delegated-workflow` is an argument error |
| `REQ-ECP-018` no envelope in the package | test: the wheel's `RECORD` and an import of every public submodule | `tests/test_release_build.py` | none of `delegated_workflow`, `delegated_authority`, `change_bundle`, `repository_state`, `runtime_state`, `agent_contract`, `skill_contract`, `effect_broker`, `agent_contract.json`, `effect_contract.json` present |
| `REQ-ECP-018` no envelope vocabulary | static: `grep -rnE "nonce\|MAX_ENVELOPE_LIFETIME\|retry_ordinal\|revoked=\|agentic_delegation" se_harness templates/repository/standard/scripts` | evidence | empty |
| `ADR-ECP-002` the journal survives | test: the eleven-stage fault matrix of `tests/test_effect_broker.py:308-344` re-pointed at `journaled_apply` | `tests/test_journaled_apply.py` | for every stage: all-before or all-after, never mixed; a corrupt journal stops at `human-recovery-stop` |
| `ADR-ECP-002` Windows held-open case | test on Windows: one target held open during the apply | same | rollback or stop; no partial write |

## Acceptance scenarios

### Scenario 1: the wheel carries no envelope

Build the wheel outside the checkout (non-promotable), install it into a
disposable environment, import `se_harness` and every public submodule,
read `RECORD`, and walk `harnessctl --help` recursively. Assert none of the
listed names appears.

### Scenario 2: crashed journaled apply, retry recovers or stops

For each injected fault stage, crash a three-target apply, assert the
pre-commit stages leave every target byte-equal to before, then run the
recovery. Assert either completion with all three targets at their
post-image, or a `human-recovery-stop` naming the journal, and never a
mixed state.

### Scenario 3: Windows mid-apply replace failure

On Windows, hold one target open during the write. Assert the apply rolls
back or stops, and that no target is partially written.

### Scenario 4: retained history

Assert the phase-1, phase-3, phase-4 and phase-5 vector fixtures are
byte-unchanged against `main` at the candidate.

## Property and invariant tests

For any sequence of interleaved crashes and recoveries, the set of target
states observed is a subset of {all-before, all-after}.

## Evidence retention

Under `docs/engineering/execution-control-plane/evidence/WO-ECP-006/`.

## Pass criteria

Every deterministic test passes on the Linux lane and the Windows
workstation reading is at its baseline with the held-open case run, not
skipped; the wheel walk and the vocabulary grep are empty. Graph and
integrity readings come from the exact released evaluator, se-harness
0.10.0, installed outside the checkout.

## Residual uncertainty

The journal is retained but not yet the write path of any command; that is
`REQ-ECP-017`'s and `VER-ECP-006`'s scenario 5 over `transition --apply`,
under a later work order.
