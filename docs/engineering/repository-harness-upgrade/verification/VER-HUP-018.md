+++
id = "VER-HUP-018"
type = "verification"
title = "Verify standard-root adoption of exact public 0.17.0"
status = "draft"
owners = ["assurance-owner", "quality-owner"]
created = "2026-09-09"
updated = "2026-09-09"

[relations]
verifies = ["REQ-HUP-035", "REQ-HUP-036"]
+++

# Verification Contract: Verify standard-root adoption of exact public 0.17.0

## Independence

Expected values derive from `REQ-HUP-035`, `REQ-HUP-036` and the rules of
`SPEC-HUP-018`; the plan counts, digests and readings are those the
rehearsal of 2026-09-09 measured on a throwaway clone, and the real
transaction is compared with them, not the other way round. The wheel
digest is read from `RLS-SEH-026`'s distribution table, never from the
installed environment.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-HUP-035` | wheel-file SHA-256 before install; `upgrade .`, `upgrade . --apply --evidence-output ...`, `upgrade .` replay from the isolated 0.17.0 environment | wheel digest equals `RLS-SEH-026`'s; plan 41 files with 10 `update` and 1 `add` (`RISK.template.md`) and no `remove`/`adopt`/`customized`/`conflict`; the transaction document retained under `docs/engineering/repository-harness-upgrade/evidence/` with prior `tool_version 0.16.0`, prior lock digest equal to the committed 0.16.0 lock, target identity equal to the new lock; replay 41 unchanged; lock `archive_sha256` equals the wheel digest and the lock names forty-one files |
| `REQ-HUP-036` | exact 0.17.0 `validate --advisories`, `doctor`, `qualify released-root`, `inspect`, `dashboard` twice, review preflight; `evaluator_facts derive`; `run_tests.py --scale full` on the moved root and on a same-commit control; reading of the root configuration, the root workflow, the ignore block, the owner region and `SPEC-IAR-012` | validate 0 errors, 0 advisories, warnings as the evidence records; doctor 0 FAIL; RR001 to RR004 PASS; inspect exit 0; identical resource digests across two generations; preflight PASS; derive yields 0.17.0 to 0.18.0 after the candidate move and `PRE008` before it; the configuration holds the five read keys; the workflow equals the release's template with the version substituted; the ignore block sits between hash markers; the owner region reads `se-harness==0.17.0`; the suite's failure set equals the control's beyond the named edits and the workstation baseline error |
| both | hosted lanes at the pull request head | the governor-transition lane assesses the real 0.16.0 to 0.17.0 move with exactly one transaction document and `RLS-SEH-026` supplying the wheel; the managed lane runs the 0.17.0 gate the transaction installed, its check steps surfacing the evaluator's refusal; the candidate-evidence lane rehearses 0.17.0 to 0.18.0 on both platforms; the Publication Rehearsal passes in both modes |

## Acceptance scenarios

- Install the published wheel in an isolated environment after comparing
  its digest with `RLS-SEH-026`; plan, apply with the transaction document,
  replay; read the lock and confirm the forty-one entries and the added
  risk template.
- Run the complete qualification on the moved root and compare the suite
  with a same-commit control on the 0.16.0 root.
- Read the root configuration and the root ignore file after the move: five
  keys, hash markers; run the in-tree `doctor` and see every managed path
  match the distribution.

## Evidence retention

`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-018/` and
`WO-HUP-018-evaluator-upgrade.json`.

## Pass criteria

Every row of the matrix passes; the pull request's lanes are green through
the completion and the record heads; the hash-locked root copies after the
move equal the candidate templates modulo the installer's substitutions.

## Residual uncertainty

The suite runs hosted on Linux only; Windows readings remain workstation
readings. Two Explorer generations are compared by their resource digests
because the bundle's generation block carries a timestamp by design. The
hardened managed workflow's refusal surface is exercised by its unit tests
and by the managed lane's ordinary pass; a real evaluator refusal on this
repository is not staged.
