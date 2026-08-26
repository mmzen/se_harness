# WO-CIP-005 implementation evidence

artifact: WO-CIP-005
checkpoint: handoff
formal_snapshot_sha256: 76cdb82d323af15043913e7b9a36678c866d2777f6ae16d4e8299f222506d725

Retained by the implementation actor on 2026-08-26. This file is evidence. It
does not complete, verify, or release the work order.

## Evaluators

- Governing: released `se-harness 0.6.0` installed outside the checkout from
  the exact wheel `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`
  (`C:\Users\mathi\se-harness-eval`, invoked with `-I`).
- Candidate: this checkout. The predicate is candidate behaviour; the root's
  0.6.0 gate contract does not carry it and follows at the upgrade.

## What was built

- **Evaluator `release_unit_ready`** (`se_harness/workflow_compliance.py`,
  added to `workflow_contract.EVALUATORS`): for a release contract that
  names `candidate_commit`, derives the census with
  `se_harness.release_unit.derive_release_unit` from `previous_release_tag`
  to that commit, with exemptions from the contract's
  `[release_unit] untraced_exemptions` array, and fails with every
  `E-CIP-001` finding of `compare_with_contract`; `pass` for a contract
  without a candidate commit (the retained allow-list form is not
  re-measured); `not_assessable` when the history cannot be derived (no
  git, no tag); `fail` when a candidate commit is named without a previous
  release tag or the exemptions are malformed.
- **Predicate `QGP-G5P-RELEASE-UNIT`** on `QG-G5-RELEASE-PREPARATION` in
  `se_harness/quality_gates_contract.json` and the byte-identical standard
  `QUALITY_GATES.json` (`cmp` identical); `QUALITY_GATES.md` evaluator row
  and binding row; the declared candidate exception in
  `tests/test_validation_taxonomy.py`.
- **Hook** in `ensure_governed_checkpoint`: a `release_contract` moving
  `draft -> approved` that fails the evaluator is refused with the
  predicate identifier and the findings, and no state changes.
- **`se_harness/release_unit.py`**: the work-order id pattern accepts the
  two-segment form (`WO-001`) as well as `WO-CIP-001`; the catalog admits
  both, and the fixture uses the former.
- **Tests** (`tests/test_release_unit.py::ApprovalPredicateTests`, four):
  on a cached standard repository with the base chain, `WO-001` and
  `WO-002`, a git history tagged `v1` and one trailed commit, approval
  through `transition --apply` is refused with `QGP-G5P-RELEASE-UNIT` and
  `E-CIP-001` naming `WO-002` when `gates` over-declare, and succeeds when
  `gates` equal the census; the allow-list form is approved unmeasured; an
  untraced commit is refused until it is exempted in the contract; the
  evaluator and the predicate are in the loaded contracts.
- **Documentation.** `docs/notes/developing-se-harness.md` ("Release
  sequences": the approval refusal and the exemption form),
  `docs/notes/ci-pipeline.md` ("After WO-CIP-005").

## Commands and results

| Command | Evaluator | Result |
| --- | --- | --- |
| `harnessctl preflight . --work-order WO-CIP-005 --phase review` | released 0.6.0 | `PASS` |
| `harnessctl validate .` | released 0.6.0 | PASS, 949 artifacts, 0 errors, 50 warnings |
| `harnessctl doctor .` | released 0.6.0 | 0 FAIL |
| `python scripts/check_portable_release_surface.py --repository .` | candidate | PASS |
| `cmp se_harness/quality_gates_contract.json templates/…/QUALITY_GATES.json` | — | identical |
| `git diff --check` | git | clean |
| `harnessctl check . --artifact WO-CIP-005 --checkpoint handoff --changed-path … --changes-complete --json` (complete set below) | released 0.6.0 and candidate | before this file existed: blocked only by `QGP-G4I-EVIDENCE`; both report formal snapshot `76cdb82d323af15043913e7b9a36678c866d2777f6ae16d4e8299f222506d725` |
| `python -m unittest` over `test_release_unit`, `test_validation_taxonomy`, `test_workflow_documentation_contract`, `test_artifact_authoring_policy`, `test_ci_pipeline` | candidate | OK |
| `python scripts/run_tests.py --workers 8 --scale full` | candidate, Windows 11, CPython 3.14 | `Ran 995 tests in 111.242s (117 classes, 8 workers)` — `OK (skipped=24)` (`main` gained tests since the packet's figures; the four new approval tests each build a git history) |

## Deviations from the specification, recorded for the completion decision

1. **The predicate binds to `QG-G5-RELEASE-PREPARATION`.** No gate in
   `QUALITY_GATES.json` names a release contract's own approval; the
   release-preparation gate is where the contract's coverage is already
   judged, and the hook applies the evaluator at the contract's
   `draft -> approved` transition regardless of gate. Chosen within the
   decision envelope.
2. **The exemption field is `[release_unit] untraced_exemptions`**, an array
   of full commit ids in the contract's front matter (the envelope left the
   name open). The 0.6.0 root validator accepts it as an unknown table.
3. **`release_unit.py` changed beyond the predicate's needs**: the id
   pattern now admits two-segment work-order ids, which the catalog admits
   too and the fixture uses. Same behaviour for every three-segment id.

## Complete changed-path set

```
docs/engineering/ci-pipeline/evidence/WO-CIP-005/WO-CIP-005-verification.md
docs/notes/ci-pipeline.md
docs/notes/developing-se-harness.md
se_harness/quality_gates_contract.json
se_harness/release_unit.py
se_harness/workflow_compliance.py
se_harness/workflow_contract.py
templates/repository/standard/docs/engineering/QUALITY_GATES.json
templates/repository/standard/docs/engineering/QUALITY_GATES.md
tests/test_release_unit.py
tests/test_validation_taxonomy.py
```

## Deviation acceptances

Recorded on 2026-08-26 from the owner's interactive answers, before the
completion decision. These are the owner's statements; the assurance decision
on `VREC-CIP-005` remains separate.

| Deviation | Owner answer |
| --- | --- |
| 1 - bound to `QG-G5-RELEASE-PREPARATION` | Accept. |
| 2 - exemptions in `[release_unit] untraced_exemptions` | Accept. |
| 3 - two-segment work-order ids admitted | Accept: the catalog already allows them. |

## Not done

- The completion transition; `VREC-CIP-005`. No hosted reading is needed:
  the predicate runs in the evaluator, not in a workflow.
