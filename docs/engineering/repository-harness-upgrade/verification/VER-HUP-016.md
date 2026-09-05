+++
id = "VER-HUP-016"
type = "verification"
title = "Verify standard-root adoption of exact public 0.15.0"
status = "draft"
owners = ["assurance-owner", "quality-owner"]
created = "2026-09-05"
updated = "2026-09-05"

[relations]
verifies = ["REQ-HUP-031", "REQ-HUP-032"]
+++

# Verification Contract: Verify standard-root adoption of exact public 0.15.0

## Independence

Expected values derive from `REQ-HUP-031`, `REQ-HUP-032` and the rules of
`SPEC-HUP-016`; the plan counts, digests and readings are those the
rehearsal of 2026-09-05 measured on a throwaway clone, and the real
transaction is compared with them, not the other way round. The wheel
digest is read from `RLS-SEH-024`'s distribution table, never from the
installed environment.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-HUP-031` | wheel-file SHA-256 before install; `upgrade .`, `upgrade . --apply --evidence-output ...`, `upgrade .` replay from the isolated 0.15.0 environment | wheel digest equals `RLS-SEH-024`'s; plan 48 files with 19 `update`, 1 `add`, 1 `adopt` and no `customized`/`conflict`/`remove`; the transaction document retained under `docs/engineering/repository-harness-upgrade/evidence/` with prior `tool_version 0.14.0`, prior lock digest equal to the committed 0.14.0 lock, target identity equal to the new lock; replay 48 unchanged; lock `archive_sha256` equals the wheel digest |
| `REQ-HUP-032` | exact 0.15.0 `validate --advisories`, `doctor`, `qualify released-root`, `inspect`, `dashboard` twice, review preflight; `evaluator_facts derive`; `run_tests.py --scale full` on the moved root and on a same-commit control | validate 0 errors, 0 advisories, warnings as the evidence records; doctor 0 FAIL; RR001 to RR004 PASS; inspect exit 0; identical resource digests across two generations; preflight PASS; derive yields 0.15.0 to 0.16.0 after the candidate move and `PRE008` before it; the suite's failure set equals the control's beyond the named edits and the workstation baseline error |
| both | hosted lanes at the pull request head | the governor-transition lane assesses the real 0.14.0 to 0.15.0 move with exactly one transaction document and `RLS-SEH-024` supplying the wheel; the managed lane runs the 0.15.0 gate the transaction installed; the candidate-evidence lanes rehearse 0.15.0 to 0.16.0 on both platforms; the Publication Rehearsal passes in both modes |

## Acceptance scenarios

- Install the published wheel in an isolated environment after comparing
  its digest with `RLS-SEH-024`; plan, apply with the transaction document,
  replay; read the lock.
- Run the complete qualification on the moved root and compare the suite
  with a same-commit control on the 0.14.0 root.
- Raise a decision artifact in a throwaway copy of the moved root and see
  the 0.15.0 gate read it; this is the first root that can.

## Evidence retention

`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-016/` and
`WO-HUP-016-evaluator-upgrade.json`.

## Pass criteria

Every row of the matrix passes; the pull request's lanes are green through
the completion and the record heads; the hash-locked root copies after the
move equal the candidate templates modulo the installer's substitutions.

## Residual uncertainty

The suite runs hosted on Linux only; Windows readings remain workstation
readings. Two Explorer generations are compared by their resource digests
because the bundle's generation block carries a timestamp by design.
