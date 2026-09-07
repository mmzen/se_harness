+++
id = "VER-HUP-017"
type = "verification"
title = "Verify standard-root adoption of exact public 0.16.0"
status = "draft"
owners = ["assurance-owner", "quality-owner"]
created = "2026-09-07"
updated = "2026-09-07"

[relations]
verifies = ["REQ-HUP-033", "REQ-HUP-034"]
+++

# Verification Contract: Verify standard-root adoption of exact public 0.16.0

## Independence

Expected values derive from `REQ-HUP-033`, `REQ-HUP-034` and the rules of
`SPEC-HUP-017`; the plan counts, digests and readings are those the
rehearsal of 2026-09-07 measured on a throwaway clone, and the real
transaction is compared with them, not the other way round. The wheel
digest is read from `RLS-SEH-025`'s distribution table, never from the
installed environment.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-HUP-033` | wheel-file SHA-256 before install; `upgrade .`, `upgrade . --apply --evidence-output ...`, `upgrade .` replay from the isolated 0.16.0 environment | wheel digest equals `RLS-SEH-025`'s; plan 48 files with 6 `update`, 8 `remove` of exactly the eight retired copies and no `add`/`adopt`/`customized`/`conflict`; the transaction document retained under `docs/engineering/repository-harness-upgrade/evidence/` with prior `tool_version 0.15.0`, prior lock digest equal to the committed 0.15.0 lock, target identity equal to the new lock; replay 40 unchanged; lock `archive_sha256` equals the wheel digest and no lock entry is under `scripts/` |
| `REQ-HUP-034` | exact 0.16.0 `validate --advisories`, `doctor`, `qualify released-root`, `inspect`, `dashboard` twice, review preflight; `evaluator_facts derive`; `run_tests.py --scale full` on the moved root and on a same-commit control; reading of the three workflows, the owner region and `SPEC-IAR-012` | validate 0 errors, 0 advisories, warnings as the evidence records; doctor 0 FAIL; RR001 to RR004 PASS; inspect exit 0; identical resource digests across two generations; preflight PASS; derive yields 0.16.0 to 0.17.0 after the candidate move and `PRE008` before it; no workflow, owner sentence or test names a root script copy as a file to run or read unconditionally; the suite's failure set equals the control's beyond the named edits and the workstation baseline error |
| both | hosted lanes at the pull request head | the governor-transition lane assesses the real 0.15.0 to 0.16.0 move with exactly one transaction document and `RLS-SEH-025` supplying the wheel; the managed lane runs the 0.16.0 gate the transaction installed; the candidate-evidence lanes rehearse 0.16.0 to 0.17.0 on both platforms; the Publication Rehearsal passes in both modes, its release-record leg exercising the switched `release-qualification.yml` |

## Acceptance scenarios

- Install the published wheel in an isolated environment after comparing
  its digest with `RLS-SEH-025`; plan, apply with the transaction document,
  replay; read the lock and confirm the eight copies are gone from the tree
  and the lock.
- Run the complete qualification on the moved root and compare the suite
  with a same-commit control on the 0.15.0 root.
- Run the in-tree `doctor` after the move and see no `lock-extra` finding;
  run `harnessctl check --artifact WO-TCM-011` and see the start it waited
  for become the next step, without taking it.

## Evidence retention

`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-017/` and
`WO-HUP-017-evaluator-upgrade.json`.

## Pass criteria

Every row of the matrix passes; the pull request's lanes are green through
the completion and the record heads; the hash-locked root copies after the
move equal the candidate templates modulo the installer's substitutions;
the three workflows carry the evaluator commands and their tests read them.

## Residual uncertainty

The suite runs hosted on Linux only; Windows readings remain workstation
readings. Two Explorer generations are compared by their resource digests
because the bundle's generation block carries a timestamp by design. The
switched `pages-publication.yml` is exercised end to end only by the next
release's publication; its unit tests and the unchanged
`publish_dashboard.py` steps are the evidence available before then.
