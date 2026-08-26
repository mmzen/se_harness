# WO-REB-024 implementation evidence

artifact: WO-REB-024
checkpoint: handoff
formal_snapshot_sha256: b5426b638be48334a55f94df5d5a95752a22a26da9b3960bc53ea4954bdcd71b

Retained by the implementation actor on 2026-08-26. This file is evidence. It
does not complete, verify, or release the work order.

## Evaluators

- Governing: released `se-harness 0.6.0` installed outside the checkout from
  the exact wheel `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`
  (`C:\Users\mathi\se-harness-eval`, invoked with `-I`).
- Candidate: this checkout, branch `fix/reb-024-rejected-record-scope` off
  `main` at `be2f0cfec18b86d273400466cdf1c8c691d92f75`.

## What was built

`repository_tools/predecessor_preparation.py::_derive_history` now filters
the rejected release records it considers to those whose `preparation_schema`
equals `release_bootstrap.PREPARATION_SCHEMA`
(`se-harness-predecessor-bootstrap-v1`) before the "exactly one, for the
successor version" cardinality check — the rule `SPEC-REB-005` rule 3 states.
Three lines; no new name; the version match, contract and tuple checks that
follow are unchanged. Ordinary rejected release records are invisible to the
selection, as `REQ-REB-019` describes them.

## Why

The first ordinary rejected release record in this repository,
`RLS-SEH-014` (0.7.0, rejected 2026-08-26 on the branch of pull request
#183), made every predecessor-view derivation fail:
`compatibility view requires exactly one rejected release record, for the
successor version`. Measured on that branch at `a3bf411`: the candidate-mode
publication rehearsal (run `33016587678`) and the candidate-evidence lane
(run `33016587475`) both red on
`tests/test_predecessor_publication.py::test_retained_rls_replays_one_exact_rejected_pair`,
which derives the 0.6.0 history over the real catalog.

## Commands and results

| Command | Evaluator | Result |
| --- | --- | --- |
| `harnessctl preflight . --work-order WO-REB-024 --phase start` | released 0.6.0 | `PASS` (recorded in the start transition) |
| `harnessctl preflight . --work-order WO-REB-024 --phase review` | released 0.6.0 | `PASS` |
| `harnessctl validate .` | released 0.6.0 | PASS, 951 artifacts, 0 errors, 50 warnings |
| `harnessctl doctor .` | released 0.6.0 | 0 FAIL |
| `python scripts/check_portable_release_surface.py --repository .` | candidate | PASS |
| `python scripts/validate_release_distributions.py --root .` | candidate | PASS |
| `git diff --check` | git | clean |
| `python -m unittest tests.test_predecessor_publication tests.test_predecessor_preparation` | candidate | OK, 20 tests, 2 skips |
| `python scripts/run_tests.py --workers 8 --scale full` | candidate, Windows 11, CPython 3.14 | `Ran 995 tests in 81.975s (117 classes, 8 workers)` — `OK (skipped=24)` |
| Regression proof on the release catalog: a detached worktree at `a3bf411` (pull request #183, catalog holding `RLS-SEH-009` bootstrap-rejected and `RLS-SEH-014` ordinary-rejected) | candidate | `tests.test_predecessor_publication` **FAILED (errors=1)** without the change; **OK** for both predecessor suites with this file's `predecessor_preparation.py` copied in |
| `harnessctl check . --artifact WO-REB-024 --checkpoint handoff --changed-path … --changes-complete --json` | released 0.6.0 and candidate | before this file existed: blocked only by `QGP-G4I-EVIDENCE`; formal snapshot below |
| Hosted | the pull request's `candidate`-mode rehearsal | pending the pull request |

## Deviations from the specification, recorded for the completion decision

1. **No new test.** The repository's change constraints ask for
   deterministic boundary tests for release behaviour; this work order adds
   none, because `tests/` ships in the source distribution and
   `REL-SEH-017`'s approved allow-list is frozen — a `tests/` byte would
   reopen it. The regression proof is the existing real-catalog test, which
   fails on the release branch without the change and passes with it; the
   fixture-based negative cases in `test_predecessor_preparation.py` still
   pass. A dedicated fixture case can follow under a later work order after
   0.7.0 is published.

## Complete changed-path set

```
docs/engineering/released-evaluator-boundary/README.md
docs/engineering/released-evaluator-boundary/evidence/WO-REB-024-verification.md
docs/engineering/released-evaluator-boundary/work-orders/WO-REB-024.md
repository_tools/predecessor_preparation.py
```

## Not done

- The hosted reading (needs the pull request); the completion transition;
  the verification record.
