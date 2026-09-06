+++
id = "VER-DST-025"
type = "verification"
title = "Evidence that the installer writes no evaluator script and the evaluator runs its own"
status = "draft"
owners = ["quality-owner"]
created = "2026-09-06"
updated = "2026-09-06"

[relations]
verifies = ["REQ-DST-070"]
+++

# Verification Contract: Evidence that the installer writes no evaluator script and the evaluator runs its own

## Independence

Cases are written from the rule identifiers of `SPEC-DST-025`, not from the
diff. The installation and upgrade cases run against a throwaway target from a
wheel built from the candidate and installed in a virtual environment outside
the checkout, which is how a consumer meets the change. The candidate suite
runs on the hosted Linux lane; the local Windows suite is a control, not the
record.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-DST-070` | test | template manifest (DST-ENG-001, DST-ENG-002) | no manifest target starts with `scripts/`; the template tree has no `scripts/` directory |
| `REQ-DST-070` | test | `init` into an empty directory (DST-ENG-002, DST-ENG-004) | no `scripts/` path on disk, no `scripts/` key in the lock, `validate` and `dashboard` succeed on the result |
| `REQ-DST-070` | test | wheel content (DST-ENG-001, DST-ENG-003) | the five evaluator scripts present once under `se_harness/`, no `share/.../scripts/` member, no `data-files` `scripts` entry |
| `REQ-DST-070` | test | resolver (DST-ENG-004, DST-ENG-005) | the resolved path is inside the package directory for every evaluator script, and a missing script raises before the target is read |
| `REQ-DST-070` | test | invocation and output parity (DST-ENG-006, DST-ENG-007) | the existing validator, generator and inspector tests pass unchanged against the relocated scripts; two generations are byte-identical |
| `REQ-DST-070` | test | upgrade of a fixture lock recording the eight paths with byte-identical copies (DST-ENG-011, DST-ENG-013) | plan shows eight `remove` actions, files gone, lock entries gone, `doctor` passes |
| `REQ-DST-070` | test | same fixture with one edited copy (DST-ENG-011, DST-ENG-012) | plan shows `customized`, apply refuses, tree and lock unchanged |
| `REQ-DST-070` | test | retirement grep (DST-ENG-008, DST-ENG-009, DST-ENG-010) | no file of those names in the wheel or template tree; no `scripts/` path in the evaluator's managed or required lists; no reference outside history notes and this packet |
| `REQ-DST-070` | inspection | `pyproject.toml`, installation note, developing note (DST-ENG-001, DST-ENG-017) | data-files table has no `scripts` entries; the notes describe the package as the only home of the scripts |
| `REQ-DST-070` | inspection | this repository's root (DST-ENG-014) | the work order's diff touches no root `scripts/` file and not the lock |

DST-ENG-015 and DST-ENG-016 bind the later root-adoption work order and are
verified by its contract, not this one.

## Acceptance scenarios

Scenario A, consumer install: build the candidate wheel, install it in a fresh
venv outside the checkout, `init` an empty directory, run `doctor`, `validate`
and `dashboard` on it. Expected: success, no `scripts/` anywhere in the target.

Scenario B, consumer upgrade: take a repository initialized by released 0.15.0,
run the candidate's `upgrade` plan and `upgrade --apply`. Expected: the eight
paths are planned `remove` and are gone afterwards; `doctor` passes.

Scenario C, customized copy: as B, but one retired file was edited. Expected:
refusal naming the path, nothing written.

## Property and invariant tests

For every evaluator script name, the resolver's result is relative to the
package directory. For every template manifest entry, the target does not
start with `scripts/`. Two `dashboard` generations from the relocated
generator are byte-identical, as the existing determinism test already asserts.

## Static and architecture checks

`grep` for the retired names across `se_harness/`, `templates/`, `.github/` and
`docs/notes/` outside `history/` returns nothing but this packet and the
adoption obligations DST-ENG-015 and DST-ENG-016 name.

## Security and privacy checks

The resolver never composes a path from the target root or the working
directory; a test asserts that the resolved path for a target containing a
decoy `scripts/validate_engineering_artifacts.py` is still the package copy.

## Performance and resilience checks

Not applicable; same bytes, same invocation.

## Manual assessments

The owner reviews the installation note's "Two things are installed" section
and the upgrade section for accuracy against Scenario B's plan output.

## Evidence retention

`docs/engineering/harness-distribution/evidence/WO-DST-024-verification.md`
with the scenario outputs, the wheel listing, the upgrade plan, and the test
report of the hosted lane, plus the local control reading labelled as such.

## Residual uncertainty

This repository's own root footprint is not exercised by this contract; the
root-adoption work order that adopts the carrying release verifies the removal
of its eight files and the owner-region and lane changes that follow.
