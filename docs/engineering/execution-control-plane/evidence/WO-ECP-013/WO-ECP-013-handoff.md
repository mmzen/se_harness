```toml
artifact = "WO-ECP-013"
checkpoint = "handoff"
formal_snapshot_sha256 = "361ff7b847e71cf3254ca86923a0ba70ac39b544da2eabb3d1d2262be02f801a"
rebound_at = "2026-08-29T08:46:33Z"
```

# WO-ECP-013 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

`harnessctl check` has a fifth public checkpoint, `scope`, at which
`QG-G4-IMPLEMENTATION-EVIDENCE` evaluates only `QGP-G4I-SCOPE`,
`QGP-G4I-COMPLETE` and `QGP-G4I-PATHS` for a work order in any lifecycle
state (`ECP-SCP-001` to `ECP-SCP-005`); the managed workflow runs it on
every pull request and runs the handoff check with the `Harness-Restitution`
comparison only while the work order is `in_progress` (`ECP-SCP-006` to
`ECP-SCP-009`); the five checkpoints are documented (`ECP-SCP-010`);
`SPEC-ECP-003` and `ARCH-ECP-001` carry their amendment records. Issue
#255.

## Evaluators

- Governing: released `se-harness 0.9.0` outside the checkout, `-I`, on
  Windows for `validate`, `doctor` and `preflight`, and the same wheel in an
  isolated Linux environment (WSL Ubuntu 24.04, CPython 3.12.3) for
  `evidence`, `transition --apply` and the handoff check over an LF clone
  (issues #254 and #256 on this root). The released 0.9.0 evaluator does
  not know the `scope` checkpoint: `harnessctl check ... --checkpoint scope`
  is refused by its argument parser, which is expected until a release
  carries this change and a root adopts it.
- Candidate: this checkout, branch `wo/ecp-013-scope-checkpoint` off
  `main` at `1d19d17`; the suite and the demonstrations run candidate
  source.

## Change

- `se_harness/workflow_contract.py`: `CHECKPOINTS` gains `scope`.
- `se_harness/workflow_compliance.py`: `check_workflow` accepts `scope`,
  refuses it for a record (`WEX210: the scope checkpoint applies only to a
  work order`), evaluates `SCOPE_CHECKPOINT_GATE` regardless of the selected
  rule, and supplies the scope predicates' corrective forms when the
  selected step declares none (`SCOPE_CHECKPOINT_CORRECTIVE`); `evidence`
  keeps its four checkpoints.
- `se_harness/workflow_procedures.py`: `select_current_step` treats `scope`
  as `handoff`.
- `se_harness/cli.py`: `check --checkpoint` choices gain `scope`;
  `handoff.json` retention stays bound to `handoff`.
- `QUALITY_GATES.json` (template and packaged copy, byte-identical): the
  gate declares `scope`; `QGP-G4I-SCOPE`, `QGP-G4I-COMPLETE` and
  `QGP-G4I-PATHS` declare `scope`; the other five predicates declare the
  gate's previous three checkpoints explicitly. No identifier or evaluator
  moves. `WORKFLOW.json` is unchanged.
- `QUALITY_GATES.md` (`QG-010`, `QG-011`) and `WORKFLOW.md` name the
  checkpoint; the managed workflow's scope step is rewritten per
  `ECP-SCP-006` to `ECP-SCP-009` with no unguarded exit; the pull-request
  seed states that the check fails whatever the lifecycle state and that a
  declared digest is not recomputed after completion.
- `docs/notes/harnessctl-check.md` and `harnessctl-reference.md` name five
  checkpoints, with `scope` in the checkpoint and gate tables.
- Hash-locked root files of this repository are untouched: `git diff
  --stat 1d19d17 -- docs/engineering/QUALITY_GATES.* docs/engineering/WORKFLOW.*
  .github/ scripts/` is empty.

## Tests

- `tests/test_workflow_compliance.py::ScopeCheckpointTests`: in `draft`,
  `approved`, `in_progress`, `implemented` and `verified` (with a committed
  covering record), an in-scope Git diff completes with exactly the three
  scope predicates and the state echoed; an out-of-scope path blocks with
  `QGP-G4I-PATHS: WEX201` naming it and an escalation to
  `DR-REMEDIATION-SCOPE`; the scope check writes no `handoff.json` while
  the handoff check still does; a verification record is refused with
  `WEX210`; `evidence` rejects `scope`.
- `tests/test_ci_pipeline.py`: the managed step runs `--checkpoint scope`
  before anything else, guards the handoff check and the digest comparison
  on the `in_progress` reading, carries the bound-at-handoff line, has no
  bare exit, reads the change set from Git and never from the body.
- `tests/test_progressive_documentation.py`: the check note's five
  checkpoints and its identifiers against the contracts.
- `tests/test_validation_taxonomy.py`: the root `QUALITY_GATES.md` of a
  release before this change differs from the template in exactly the
  `QG-010` and `QG-011` paragraphs; the divergence is declared, not hidden.
- Every existing handoff assertion is unchanged and passes.

## Suite readings

- Linux (WSL Ubuntu 24.04, CPython 3.12.3, LF clone at `18203d0`):
  `python3 scripts/run_tests.py --scale full` OK, 4 skips.
- Windows 11 workstation (CPython 3.12, CRLF checkout, `18203d0`): 1117
  tests, 2 failing names, both outside this work order and present on
  `main`:
  `test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`
  and
  `test_instruction_architecture.OwnerInstructionRegionTests.test_owner_region_stays_within_the_size_bound`
  (the CRLF-only owner-region reading).

## Demonstration on this repository, candidate source on Windows

- `check . --artifact WO-ECP-013 --checkpoint scope --from-git 1d19d17`:
  Completed; gates `QGP-G4I-SCOPE`, `QGP-G4I-COMPLETE`, `QGP-G4I-PATHS`
  all `pass` (the work order is `in_progress`; the diff is this branch).
- `check . --artifact WO-ECP-012 --checkpoint scope --from-git 1d19d17`:
  Blocked, `QGP-G4I-PATHS` naming this branch's paths, which are outside
  `WO-ECP-012`'s scope (the work order is `implemented` with a verified
  record; under the old gate the check was refused outright).
- `check . --artifact WO-HUP-009 --checkpoint scope --changes-complete`:
  Completed on an empty change set (the work order is `implemented` with a
  verified record).
- The released 0.9.0 evaluator refuses `--checkpoint scope` in its argument
  parser. This repository's own managed lane keeps the old step until the
  next root adoption, so this pull request is red from its completion
  transition to its merge by the rule this work order removes; `VER-ECP-009`
  scenario 6 is therefore recorded as the old behaviour here and left to
  the first pull request governed by the release that carries the change.

## Readings under the 0.9.0 root

- `validate .`: PASS; maintenance E0/W475.
- `doctor .`: 0 FAIL.
- Review preflight for `WO-ECP-013`: PASS.

## Handoff check

`harnessctl check . --artifact WO-ECP-013 --checkpoint handoff --from-git 1d19d17`
from the Linux 0.9.0 environment over an LF clone, run twice on the
committed packet so the retained `handoff.json` is in the change set it
digests: see that file beside this one.

## Complete changed-path set

Every path this work order changed since `main` at `1d19d17`, packet
included, as Git derived it (26 paths):

```
docs/engineering/execution-control-plane/architecture/adr/ADR-ECP-006.md
docs/engineering/execution-control-plane/architecture/ARCH-ECP-001.md
docs/engineering/execution-control-plane/evidence/WO-ECP-013/handoff.json
docs/engineering/execution-control-plane/evidence/WO-ECP-013/WO-ECP-013-handoff.md
docs/engineering/execution-control-plane/README.md
docs/engineering/execution-control-plane/requirements/REQ-ECP-020.md
docs/engineering/execution-control-plane/specifications/SPEC-ECP-003.md
docs/engineering/execution-control-plane/specifications/SPEC-ECP-009.md
docs/engineering/execution-control-plane/verification/VER-ECP-009.md
docs/engineering/execution-control-plane/work-orders/WO-ECP-013.md
docs/notes/harnessctl-check.md
docs/notes/harnessctl-reference.md
se_harness/cli.py
se_harness/quality_gates_contract.json
se_harness/workflow_compliance.py
se_harness/workflow_contract.py
se_harness/workflow_procedures.py
templates/repository/standard/.github/PULL_REQUEST_TEMPLATE.md.seed
templates/repository/standard/.github/workflows/engineering-harness.yml
templates/repository/standard/docs/engineering/QUALITY_GATES.json
templates/repository/standard/docs/engineering/QUALITY_GATES.md
templates/repository/standard/docs/engineering/WORKFLOW.md
tests/test_ci_pipeline.py
tests/test_progressive_documentation.py
tests/test_validation_taxonomy.py
tests/test_workflow_compliance.py
```

## Hosted lanes

Pull request #258 at `94113de`: every lane passes (13 pass). The managed
Engineering Harness lane (https://github.com/mmzen/se_harness/actions/runs/33243970048/job/99078077948) still runs the 0.9.0 root's old step
(`check --checkpoint handoff`), which completed inside the declared scope
with the declared `Harness-Restitution` `b27e6177…` equal to the recomputed
`result_sha256` while the work order is `in_progress`; the Governor
Transition Assessment (https://github.com/mmzen/se_harness/actions/runs/33243970000/job/99078077807), both candidate-evidence lanes, both migration
legs, both qualification rehearsals and the integration-package build,
verify (Linux, Windows) and retain lanes pass. From the completion
transition on, that old step is expected red on this pull request, by the
rule this work order removes (`VER-ECP-009`, residual uncertainty).
