# WO-ECP-001 implementation evidence

artifact: WO-ECP-001
checkpoint: handoff
formal_snapshot_sha256: 9124cd6b08c950e1f4249ec896898e879244d4d89e3f76690e2e9d8304705db6

Retained by the implementation actor on 2026-08-28. This file is evidence. It
does not complete, verify, or release the work order.

## Outcome

`harnessctl next` exists and is a projection of what `focus`, `preflight` and
the procedure's current step already select; `check --from-git BASE` derives
the change set from Git instead of from typed paths; the corrective an agent
receives from a failed operation names `harnessctl next`, never the command
it just ran. No lifecycle state, gate predicate identifier or decision right
changed.

## Evaluators

- Governing: released `se-harness 0.8.0` (the root since `WO-HUP-008`),
  installed outside the checkout, invoked with `-I` — validate, doctor,
  start preflight, the handoff bind. The packet text names 0.7.1, written on
  2026-08-27 before the root advanced; deviation 1 below.
- Candidate: this checkout, branch `wo/ecp-001-next-and-from-git` off `main`
  at `233bc92`; suite and the readings of the new commands run with
  candidate source.

## What changed

| Path | Change |
| --- | --- |
| `se_harness/workflow.py` | `next_step(repository, artifact_id)`: selects the named artifact or the single `in_progress` work order (`WEX-ECP-001` names the candidate count otherwise); takes the `focus` projection; adds `context` = `reading_manifest` (from `run_preflight`, phase `start` for `approved`/`in_progress`, `review` afterwards; a VREC or RLS reads the review manifest of the first work order it verifies or releases), `governing`, `declared_paths`, `state`, `next` (`argv`, `procedure_id`, `step_id` — the argv of the step `focus` selected, `[]` for a decision step), `decision_required`; sets `operation.kind = "next"` and recomputes `result_sha256`. Writes nothing. |
| `se_harness/workflow_compliance.py` | `git_change_set(root, base)`: `git rev-parse --verify BASE^{commit}`, then `git diff -z --name-only --no-renames BASE --` (renames contribute both names) plus `git ls-files -z --others --exclude-standard`, each member through `normalize_path`, deduplicated, `complete = True`, `source = "git"`; any Git failure, a non-checkout or an unresolvable base raises `WEX-ECP-003` naming the base and the exit status. `check_workflow(from_git=…)`: exclusive with the typed options (`WEX-ECP-002`). `CheckpointContext.admitted_scope` = declared scope plus the selected work order's own artifact path (`ECP-CHG-007`); `QGP-G4I-PATHS` evaluates against it; `declared_paths` in the result is unchanged. `remediation_result`: the retry is `harnessctl next . --artifact <ID>` when the artifact is known (`ECP-NXT-008`); "rerun the same command" is gone. |
| `se_harness/workflow_result.py` | `_render_context` renders the `next` context as an ordered `Context` section after `Command or response`; every other section's bytes are unchanged (the `focus` golden digest `d22f5e48…` still reproduces). Scope amendment 2. |
| `se_harness/cli.py` | `next [TARGET] [--artifact ID] [--json]`; `check --from-git BASE`; both refusals; the `WEX-ECP-00x` code of a refusal is carried as the finding code rather than folded under `WEX210`. |
| `se_harness/workflow_contract.json`, template `WORKFLOW.json` | the `QGP-G4I-COMPLETE` corrective of `STEP-WO-IMPLEMENT-CHECK` is `check … --from-git <base>`; the `QGP-G4I-EVIDENCE` response says "rerun the handoff check with --from-git <base>". Byte-identical to each other (asserted by `test_runtime_and_installed_contracts_are_byte_identical`); the root managed copy `docs/engineering/WORKFLOW.json` is released 0.8.0's and is not edited (deviation 2). |
| template `WORKFLOW.md` | step 5 names `harnessctl next`; the failure procedure names the `--from-git` corrective and `next` as the retry. |
| `docs/notes/harnessctl-reference.md` | inventory row, synopsis and two paragraphs for `next` and `--from-git`. |
| `SPEC-ECP-001` | `ECP-CHG-007` by dated amendment (scope amendment 1). |
| `tests/test_workflow_compliance.py` | `GitDerivedChangeSetTests` (5): modified, deleted, renamed (both names), untracked and ignored paths against a real `git init` fixture; scope check and digest binding; own-file admission and a second work order's file refused; exclusivity (`WEX-ECP-002`) and a bad base (`WEX-ECP-003`, no predicate `pass`, retry names `next`); outside a checkout. |
| `tests/test_workflow_execution.py` | `NextCommandTests` (6): selection of the single `in_progress` work order with equality of `next`/`focus`/`check` next step and argv, context member order, differing digest, `Context` after `Command or response`; reading manifest equal to `run_preflight` for both phases; zero and two `in_progress` work orders → `WEX-ECP-001`; VREC projection and refusal of a non-primary type; no writes; the failed-`check` retry is `next`. The corrective test asserts the `--from-git <base>` form. |

## Scope amendments

1. `SPEC-ECP-001` added for `ECP-CHG-007` (owner: "Admit the selected WO's
   own file by rule"). Measured cause: `check --from-git main` on this branch
   reported `WEX201` for `WO-ECP-001.md`, whose approval and start commits
   are on the branch; with a Git-derived set nothing can omit it.
2. `se_harness/workflow_result.py` added (owner: "Amend scope: add
   workflow_result.py"). Measured cause: the same check reported `WEX201`
   for that file after amendment 1; `ECP-NXT-007` puts the `Context` section
   in the canonical block, which that module renders.

## Readings of the new commands on this branch (candidate source)

- `harnessctl next .` selects `WO-ECP-001` (the one `in_progress` work
  order); `context.next.argv` = `harnessctl check . --artifact WO-ECP-001
  --checkpoint handoff` (`PROC-WO-IMPLEMENT`/`STEP-WO-IMPLEMENT-CHECK`), the
  reading manifest is the 12-file start manifest `preflight` emits.
- `harnessctl check . --artifact WO-ECP-001 --checkpoint handoff --from-git
  main --json`: `change_set_source = "git"`, `change_set_complete = true`,
  the changed paths are this branch's diff; before the amendments the only
  scope refusals were `WO-ECP-001.md` and `workflow_result.py`; after them
  the only blocker is `QGP-G4I-EVIDENCE` until this file is bound.
- `--from-git main --changes-complete` → `WEX-ECP-002`; `--from-git nope` →
  blocked, `WEX-ECP-003: git rev-parse failed for base 'nope' with exit
  status 1`, retry `harnessctl next . --artifact WO-ECP-001`.

## Readings under the 0.8.0 root, isolated mode

- `validate .`: PASS, 0 errors (after both amendments).
- `doctor .`: 0 FAIL.
- Start preflight: Completed over the approval commit `d0de313`.

## Tests

- `tests.test_workflow_execution` + `tests.test_workflow_compliance`: 204
  tests OK (143 before; 11 added, the rest are subtests counted by the
  runner).
- `tests.test_progressive_documentation`: OK after the inventory row.

## Handoff check

Governing 0.8.0 (which predates `--from-git` and `ECP-CHG-007`): `harnessctl check . --artifact WO-ECP-001 --checkpoint handoff --changed-path … --changes-complete` over the 12 paths below, the work order's own file omitted as under every earlier work order: Completed; before this file carried the formal snapshot the only non-pass predicate was QGP-G4I-EVIDENCE.

Candidate source, the new path: `harnessctl check . --artifact WO-ECP-001 --checkpoint handoff --from-git main`: the change set below plus `WO-ECP-001.md`, admitted by `ECP-CHG-007` — result recorded after the bind in the next section.

## Complete changed-path set

Every path this work order changed since `main` at `233bc92`, amendments and evidence included (the work order's own file changes only through its recorded transitions and scope amendments):

```
docs/engineering/execution-control-plane/evidence/WO-ECP-001/WO-ECP-001-verification.md
docs/engineering/execution-control-plane/specifications/SPEC-ECP-001.md
docs/notes/harnessctl-reference.md
se_harness/cli.py
se_harness/workflow_compliance.py
se_harness/workflow_contract.json
se_harness/workflow.py
se_harness/workflow_result.py
templates/repository/standard/docs/engineering/WORKFLOW.json
templates/repository/standard/docs/engineering/WORKFLOW.md
tests/test_workflow_compliance.py
tests/test_workflow_execution.py
```

## Git-derived handoff, candidate source

`check --from-git main` after the bind: completed git 13 95f8f4b8e03e10ac714636f325c7d8740803fd7bcef3673c8290f1e6d4933ef0 — outcome, change_set_source, path count (the typed set plus the work order's own file), result_sha256.

## Suite

`python scripts/run_tests.py --scale full` with candidate source (CPython 3.12, Linux): Ran 1050 tests in 47.845s (118 classes, 4 workers); failures: FAIL: test_release_build.HostIndependentCandidateSourceTests.test_declared_mode_set_is_what_a_posix_export_already_carries; — the workstation file-mode condition that passes hosted, unchanged. The Windows figure is the hosted lane's.
