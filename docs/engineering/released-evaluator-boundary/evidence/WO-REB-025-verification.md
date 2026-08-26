# WO-REB-025 implementation evidence

artifact: WO-REB-025
checkpoint: handoff
formal_snapshot_sha256: c394d159831f4e646c8cbded6934ed3ea7637ab689618d171c0815d41a1e5ac2

Retained by the implementation actor on 2026-08-27. This file is evidence. It
does not complete, verify, or release the work order.

## Evaluators

- Governing: released `se-harness 0.6.0` installed outside the checkout from
  the exact wheel `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`
  (`C:\Users\mathi\se-harness-eval`, invoked with `-I`).
- Candidate: this checkout, branch `fix/reb-025-publication-view-condition`
  off `main` at `088b08befbce5874289fd5877510000048f24226`.

## What was built

Both workflow steps that realise `REQ-REB-015` — *Acquire and prove the
released evaluator* in `.github/workflows/publish-pypi.yml` (resolve job) and
*Validate with the released evaluator* in
`.github/workflows/pages-publication.yml` (build job) — now decide before
running `harnessctl qualify predecessor-view` whether the requirement's
condition holds. The decision is an inline `python -` over the front matter
with `tomllib` (CPython 3.11 on the runners): the named record must resolve
to exactly one file under `docs/engineering/**/releases/`, must satisfy
exactly one release contract, and that contract must resolve to exactly one
file in a `release/` directory; the step then reads `declared` when the
contract carries a `[bootstrap]` table and `absent` otherwise, and fails
closed on any other cardinality.

- `declared`: the previous command line runs unchanged, its `--output` now
  spelled through `view_output`, which holds the same path.
- `absent`: the step writes, at that same path, an `excluded` observation —
  schema `se-harness-predecessor-view-exclusion/v1`, `operation`
  `predecessor-view`, `outcome` `excluded`, the record id, the resolved
  evaluator version and archive digest, the reason, and the standard
  evidence-only authority line — so the retained plan artifact keeps its file
  set and no later step is skipped silently.

The Pages step gains an `env` block for `EVALUATOR_VERSION` and
`EVALUATOR_WHEEL_SHA256` from the same `steps.evaluator` outputs the step
before it already reads. The evaluator download, hash proof and identity
proof are unconditional as before. No script, `se_harness/`, `tests/`,
`repository_tools/` or `templates/` byte changed; `permissions` and action
pins did not move.

## Why

The dispatched last mile for `RLS-SEH-015` (run `33019109414`, `main` at
`088b08b`) stopped in its first job on `PV001: bootstrap field set is
invalid (missing evaluator_archive_name, …)`. `RLS-SEH-015` satisfies
`REL-SEH-017`, which declares no `[bootstrap]` table by design (first
ordinary schema-3 release, governed by the same 0.6.0 evaluator that
validates the complete graph), so `REQ-REB-015`'s *WHEN* clause does not
hold and `SPEC-REB-007`'s two-omission view has no subject. The release
qualification was never the problem: `main`'s push-event rehearsal ran the
`release-record` mode for `RLS-SEH-015` and passed (run `33019036450`).

## Commands and results

| Command | Evaluator | Result |
| --- | --- | --- |
| `harnessctl preflight . --work-order WO-REB-025 --phase start` | released 0.6.0 | `PASS` (recorded in the start transition) |
| `harnessctl preflight . --work-order WO-REB-025 --phase review` | released 0.6.0 | `PASS` |
| `harnessctl validate .` | released 0.6.0 | PASS, 958 artifacts, 0 errors, 53 warnings |
| `harnessctl doctor .` | released 0.6.0 | 0 FAIL |
| `python scripts/check_portable_release_surface.py --repository .` | candidate | PASS |
| `git diff --check` | git | clean; both workflows carry zero CR bytes |
| PyYAML `safe_load` of both workflows | workstation | both parse; `publish-pypi.yml` jobs `resolve, qualify, github_release, pypi, pages, observe`; `pages-publication.yml` jobs `build, deploy` |
| Pinned-string counts | workstation | `predecessor-view-qualification.json` 3 in `publish-pypi.yml` and 1 in `pages-publication.yml` (unchanged); exactly one `mkdir "$RUNNER_TEMP/predecessor-view"` |
| Decision over the real catalog | workstation | `RLS-SEH-015` → `REL-SEH-017` → `absent`; `RLS-SEH-012` → `REL-SEH-011` → `declared` |
| Both patched `run` blocks extracted from the YAML and executed with `bash` (the `qualify` invocation stubbed) | workstation | `RLS-SEH-015`: the `absent` branch writes the excluded observation shown below and echoes the exclusion, in both steps; `RLS-SEH-012`: the `declared` branch reaches the `qualify predecessor-view` command line, in both steps |
| `python -m unittest tests.test_ci_pipeline tests.test_release_orchestration tests.test_dashboard_publication` | candidate | OK |
| `python scripts/run_tests.py --workers 8 --scale full` | candidate, Windows 11, CPython 3.14 | `Ran 995 tests in 81.860s (117 classes, 8 workers)` — `OK (skipped=24)` |
| `harnessctl check . --artifact WO-REB-025 --checkpoint handoff --changed-path … --changes-complete --json` | released 0.6.0 and candidate | before this file existed: blocked only by `QGP-G4I-EVIDENCE`; formal snapshot above |
| Hosted | the pull request's lanes | pending the pull request; the decisive reading is the release owner's re-dispatch of `publish-pypi.yml` for `RLS-SEH-015` after merge |

Excluded observation written for `RLS-SEH-015` in the local execution:

```json
{
  "authority": "derived operational evidence; no formal lifecycle transition",
  "evaluator": {"archive_sha256": "2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7", "version": "0.6.0"},
  "operation": "predecessor-view",
  "outcome": "excluded",
  "reason": "the record's contract declares no bootstrap tuple; REQ-REB-015's condition does not hold",
  "release_record": "RLS-SEH-015",
  "schema": "se-harness-predecessor-view-exclusion/v1"
}
```

## Deviations from the specification, recorded for the completion decision

1. **No new test**, for the reason `WO-REB-024` recorded: `tests/` ships in
   the source distribution and `REL-SEH-017`'s allow-list is frozen. The
   proof is the local execution of both extracted `run` blocks against the
   real catalog for one ordinary and one bootstrap record, plus the unchanged
   workflow suites. A fixture-based case for the exclusion branch can follow
   under a later work order.
2. **`SPEC-RLO-005` rule 37 is not amended.** Its `release-record` clause
   ("never exclude it") presumes a bootstrap-bound record, the only kind that
   existed when it was written; this work order exercises the view only when
   `REQ-REB-015`'s condition holds and leaves the rule's text to a later
   specification change. Recorded rather than silently reconciled.

## Complete changed-path set

```
.github/workflows/pages-publication.yml
.github/workflows/publish-pypi.yml
docs/engineering/released-evaluator-boundary/README.md
docs/engineering/released-evaluator-boundary/evidence/WO-REB-025-verification.md
docs/engineering/released-evaluator-boundary/work-orders/WO-REB-025.md
```

## Not done

- The hosted reading (needs the pull request); the completion transition;
  the verification record; the re-dispatch of the last mile (the release
  owner's act).
