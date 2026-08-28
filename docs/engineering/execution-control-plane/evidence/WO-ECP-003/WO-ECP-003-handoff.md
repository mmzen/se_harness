```toml
artifact = "WO-ECP-003"
checkpoint = "handoff"
formal_snapshot_sha256 = "93cc27b586da6bca838f247372b1423e333cc330010812fbbe58379ab04ca1f4"
rebound_at = "2026-08-28T22:40:00Z"
```

# WO-ECP-003 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored. This
file is evidence. It does not complete, verify, or release the work order.

## Outcome

The managed template workflow now enforces the work order's scope on every
pull request: the handoff check runs over the diff Git reports, with the
released evaluator from the lock, whether or not a restitution digest is
declared; an out-of-scope path fails the required check naming it. The
canonical block carries the change set and every predicate status, so a
`result_sha256` binds what was changed and what was evaluated, not only the
restitution prose.

## Evaluators

- Governing: released `se-harness 0.8.0` outside the checkout, `-I`:
  validate, doctor, start preflight, the handoff bind (0.8.0 reads evidence
  by substring; the *Legacy binding* section below is for it).
- Candidate: this checkout, branch `wo/ecp-003-mandatory-gate` off `main`
  at `e75fac8`; the demonstration ran the candidate wheel built from this
  branch, installed into a venv outside the checkout, exactly as the
  workflow step installs the released evaluator.

## What changed

| Path | Change |
| --- | --- |
| `templates/repository/standard/.github/workflows/engineering-harness.yml` | the guarded "Verify a declared restitution digest" step (early `exit 0` without a line; `--changed-path` loop) is replaced by "Enforce the work-order scope on the pull request's diff": on every `pull_request` event, fetch the base, run `check . --artifact WO --checkpoint handoff --from-git BASE --json` with the venv's `python -I -m se_harness`, fail on any `QGP-G4I-PATHS` predicate that is not `pass` (naming the first `WEX201` path), fail on a non-`completed` outcome (naming the blockers), then compare a declared `Harness-Restitution` digest when present. The only `if:` is the event type. The job count is unchanged. |
| `se_harness/workflow_result.py` | `render_human` gains `Change set` (each changed path, then `complete: true|false`) and `Gates` (`PREDICATE-ID: STATUS` per predicate in the evaluator's gate order) after `Command or response`, before `Context` and `Alternatives`; `result_sha256` stays the SHA-256 of the block. |
| `templates/repository/standard/.github/PULL_REQUEST_TEMPLATE.md.seed` | "reviewers remain accountable for confirming that the diff stays within its scope" becomes "fails on any path of the diff outside the work order's declared scope" (`ECP-GTE-007`). |
| `se_harness/github_ci.py`, template `scripts/select_harness_work_order.py` | unchanged: the block is consumed by the evaluator's own `check`; the selector only selects fields. Recorded as the decision on the packet's "consuming the new block" wording. |
| tests | `DigestCoverageTests` (2: block content and order for `check`, `next`, `focus`; digest sensitivity to one path, the completeness flag and one predicate status; LF/CRLF equality), `test_the_managed_workflow_enforces_scope_on_every_pull_request` (YAML and seed assertions), `test_root_managed_copy_is_untouched` made identity-aware (the root copy equals its lock digest; equals the template only while the root is the release that shipped it), the 0.7.1 golden re-pinned to `b8ccd288…` with the dated note (pre-start amendment 3). |

## Demonstration (VER-ECP-003 as amended: local, the hosted form deferred)

The template step's shell was extracted verbatim and run from two
throwaway branches of this repository (`demo/ecp-003-out-of-scope`,
`demo/ecp-003-in-scope`, forked from the work-order branch) in Git
worktrees, with `HARNESS_BASE_SHA` = `main` `e75fac8`, a synthesised
pull-request event carrying only `Harness-Work-Order: WO-ECP-003`, and the
candidate evaluator installed into `$RUNNER_TEMP/se-harness-env`. Logs and
the in-scope canonical block are retained under `demonstration/`.

| Run | Body | Result |
| --- | --- | --- |
| out-of-scope, run 1 | no restitution line | exit 1; stderr `scope: WEX201: changed path is outside execution scope: README-outside.md`; "The pull request's diff leaves the work order's declared scope." |
| in-scope, run 1 | no restitution line | exit 1; not a scope failure: `blocked: QGP-G4I-EVIDENCE …` — no packet was bound yet, so the outcome was not `completed`; the step fails closed as `ECP-GTE-002` requires |
| in-scope, run 2 | no restitution line, after `harnessctl evidence` bound the packet on the branch | exit 0; "inside the declared scope; no restitution digest was declared"; `change_set_source = git`, 4 paths, `QGP-G4I-PATHS: pass` |
| in-scope, declared mismatching digest | `Harness-Restitution: 0000…` | exit 1; "does not match the recomputed result_sha256 cfd5ce78…" |
| in-scope, declared matching digest | `Harness-Restitution: cfd5ce78…` | exit 0; "and the declared restitution digest matches" — the same digest `pr-body` emits on that branch |

One finding from the demonstration, recorded for operators: a completed
Git-derived handoff retains `handoff.json` in the packet directory
(`WO-ECP-002`), and that file is part of the next diff, so the digest of
run 1 (`d2d20b8b…`) differs from the digest once the file exists
(`cfd5ce78…`) — `ECP-DIG-003` working as specified. `pr-body` must be run
after the last check, and the retained file committed with the branch.

The throwaway branches and worktrees were deleted afterwards (`git worktree
remove`, `git branch -D`); nothing was pushed.

## Readings under the 0.8.0 root, isolated mode

- `validate .`: PASS, 0 errors. `doctor .`: 0 FAIL. Start preflight:
  Completed over the approval commit `0f31f1d`.

## Suite

`python scripts/run_tests.py --scale full` with candidate source (CPython
3.12, Linux): 1117 tests, 1 failure, 4 skips — the failure is
`test_release_build…test_declared_mode_set_is_what_a_posix_export_already_carries`,
the workstation file-mode condition that passes hosted, unchanged. The
Windows figure is the hosted lane's; the hosted lanes run the root 0.8.0
workflow, not the template.

## Deviations

1. Readings under 0.8.0, not the 0.7.1 the packet text names.
2. The root managed workflow and selector stay 0.8.0's; this repository's
   own pull-request gate remains the guarded 0.8.0 step until its next root
   adoption; the template carries the mandatory gate to consumers first.
3. `Gates` lines follow the order in which the evaluator emits predicates
   (gate order, then predicate order in the contract); `QG-009` names the
   aggregation order of statuses, not a rendering order, and this is the
   reading taken.

## Handoff check

Governing 0.8.0: `harnessctl check . --artifact WO-ECP-003 --checkpoint handoff --changed-path … --changes-complete` over the 16 paths below, the work order's own file omitted as 0.8.0 predates `ECP-CHG-007`: Completed once the legacy lines below were retained; before them the only non-pass predicate was QGP-G4I-EVIDENCE.

## Complete changed-path set

```
docs/engineering/execution-control-plane/evidence/WO-ECP-003/demonstration/in-scope-canonical-block.txt
docs/engineering/execution-control-plane/evidence/WO-ECP-003/demonstration/in-scope-declared-mismatch-stderr.txt
docs/engineering/execution-control-plane/evidence/WO-ECP-003/demonstration/in-scope-result.json
docs/engineering/execution-control-plane/evidence/WO-ECP-003/demonstration/in-scope-run1-stderr.txt
docs/engineering/execution-control-plane/evidence/WO-ECP-003/demonstration/in-scope-run1-stdout.txt
docs/engineering/execution-control-plane/evidence/WO-ECP-003/demonstration/in-scope-run2-stdout.txt
docs/engineering/execution-control-plane/evidence/WO-ECP-003/demonstration/in-scope-run3-declared-match-stdout.txt
docs/engineering/execution-control-plane/evidence/WO-ECP-003/demonstration/out-of-scope-run1-stderr.txt
docs/engineering/execution-control-plane/evidence/WO-ECP-003/demonstration/out-of-scope-run1-stdout.txt
docs/engineering/execution-control-plane/evidence/WO-ECP-003/WO-ECP-003-handoff.md
docs/engineering/execution-control-plane/verification/VER-ECP-003.md
se_harness/workflow_result.py
templates/repository/standard/.github/PULL_REQUEST_TEMPLATE.md.seed
templates/repository/standard/.github/workflows/engineering-harness.yml
tests/test_ci_pipeline.py
tests/test_workflow_execution.py
```

## Legacy binding

For the governing 0.8.0 evaluator, which reads evidence by substring:

artifact: WO-ECP-003
checkpoint: handoff
formal_snapshot_sha256: 93cc27b586da6bca838f247372b1423e333cc330010812fbbe58379ab04ca1f4

## Hosted lanes

Pull request #251 at `c80c1bf`: all 13 lanes pass, both platform legs of the suite included (the digest-coverage and YAML tests on Windows and Linux). These lanes are the root 0.8.0 workflow; the template's mandatory gate is exercised by the local demonstration above and, hosted, by the release condition recorded in the amendment.
