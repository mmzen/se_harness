+++
id = "VER-ECP-012"
type = "verification"
title = "Independent evidence for the admission of the selected work order's own records"
status = "draft"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[relations]
verifies = ["REQ-ECP-023"]
+++

# Verification Contract: Independent evidence for the admission of the selected work order's own records

## Independence

Expected behaviour derives from `REQ-ECP-023` and the `ECP-ADM-` rules of
`SPEC-ECP-012`. The tests write the records into a fixture repository
themselves, name the selected and another work order explicitly, and drive
`check` through the CLI with a Git-derived and a typed change set; the
hosted reading is this work order's own pull request at its record heads.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-ECP-023` own records admitted | test: `scope` and `handoff` checks over a diff adding the selected work order's ready VREC and its evaluator-evidence file, and a released RLS naming it with its evidence file | `tests/test_workflow_compliance.py` | `QGP-G4I-PATHS` passes; `declared_paths` unchanged |
| `REQ-ECP-023` other records refused | test: the same diff plus a record for another work order | same | `QGP-G4I-PATHS` fails naming that record with `WEX201` |
| `SPEC-ECP-012` every source and checkpoint | test: typed paths with `--changes-complete` and a manifest, at `scope` and `handoff` | same | admitted identically |
| `SPEC-ECP-012` hosted | demonstration: this work order's pull request | the managed lane at the record heads | pass — noting that the lane runs the released 0.10.0 evaluator, so the demonstration is read from the first pull request governed by the release carrying this rule; this work order's own scope lists its records directory for the current root |

## Acceptance scenarios

### Scenario 1: own record, Git-derived

Commit a base; add the selected work order's ready record and evidence
file; run `check --checkpoint scope --from-git BASE`. Assert completed and
`QGP-G4I-PATHS` pass; assert the record path is absent from
`scope.declared_paths`.

### Scenario 2: another work order's record

Add a record for `WO-002` in the same diff. Assert blocked with `WEX201`
naming it.

### Scenario 3: typed paths and manifest

Repeat scenario 1 with `--changed-path` and `--changes-complete`, and with
a change manifest. Assert the same.

### Scenario 4: handoff

Repeat scenario 1 at `--checkpoint handoff`. Assert `QGP-G4I-PATHS` pass.

## Evidence retention

Under `docs/engineering/execution-control-plane/evidence/WO-ECP-016/`.

## Pass criteria

Every deterministic test passes on the Linux lane; the Windows workstation
reading is at its baseline. Graph and integrity readings come from the
exact released evaluator, se-harness 0.10.0, installed outside the
checkout.

## Residual uncertainty

The hosted demonstration under the new rule waits for the next release and
root adoption; until then packets scope their records directory.
