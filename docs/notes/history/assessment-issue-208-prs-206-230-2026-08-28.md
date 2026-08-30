# Assessment of issue #208 against pull requests #206 and #230

> Historical record from 2026-08-28, at `42d820a`. Kept for the decision trail; it describes the tool as it was then.

<!-- Target expertise: 7/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

Repository-owned note. It records an independent, read-only assessment made on
2026-08-28 of whether pull requests #206 (`WO-REB-028`) and #230 (`WO-REB-029`),
taken together as a stacked change, correctly and sufficiently resolve issue
#208 (P0-2 of the [2026-08 complexity audit](../complexity-audit-2026-08.md):
remove the 0.5.0→0.6.0 predecessor-bootstrap bridge). It grants no approval,
verification, or release authority and changes no lifecycle state. Every
reading below was reproduced on the combined head `a9f3118` (the tip of #230,
which contains all of #206) rather than taken from the pull-request bodies.

## Verdict

**FIXED WITH MINOR ISSUES.** #206 and #230 together resolve #208. The
remaining items are one deliberate, separately tracked deferral (step 5,
issue #220) and three stale explanatory notes. Neither should block closure.

## Why

- **The bridge is gone from the product.** `repository_tools/` retains only
  `interpreter_safety.py`, `json_bytes.py`, `predecessor_facts.py`,
  `release_build.py` and `release_distribution.py`; the four adapters, four
  scripts and four test modules are deleted. `se_harness/` has no import of
  `repository_tools` (the only textual hits are a docstring and the `RUNTIMES`
  string tuple in `se_harness/interpreter_safety.py`). `qualify
  predecessor-view` is absent from `OPERATIONS`, `INDEPENDENCE` and the CLI,
  and `scripts/check_portable_release_surface.py` lists `predecessor-view`
  under `FORBIDDEN_ACTIVE_CONTENT`, so the surface checker can no longer
  freeze the feature back in.
- **The consumer-installed validator is fixed by #230.** The template copy
  falls from 3,679 to 3,094 lines. The ten deleted blocks are pinned
  individually against the root copy in
  `tests/test_predecessor_bootstrap_retirement.py`. Both validator copies run
  on the full graph at `a9f3118` give **1,001 artifacts, 0 errors, 471
  warnings, with byte-identical diagnostic sets**, so `RLS-SEH-012`, `-014`,
  `-015`, `-016` and the six closed 0.6.0 artifacts still validate as history.
  Their `[bootstrap]` tables and `preparation_schema` markers become inert
  data; the retained digests are recomputed by test from the files they bind.
- **Workflows.** Zero occurrences of `bootstrap` remain in
  `publish-pypi.yml`, `release-qualification.yml` and `pages-publication.yml`.
  #230 also renamed the `$RUNNER_TEMP/predecessor-view` temporary directory
  that #206 had kept.
- **Governance.** `ADR-REB-012` records the retirement decision, and #230's
  dated amendment of `ADR-REB-009` and `ARCH-REB-009` to four typed `qualify`
  operations removes the contradiction the #206 review flagged.
  `REQ-REB-008/010/012/015` and `SPEC-REB-003/005/007` are retired by dated
  amendment because `WORKFLOW.json` has no `approved → superseded` edge; both
  pull requests disclose this.
- **Stacking.** #230 is 7 commits ahead of and 0 behind #206. #206 is 8
  commits behind `main`, all of them docs or the execution-control-plane
  packet; GitHub reports both pull requests `mergeable: clean`.
- **Architectural properties.** The root `scripts/validate_engineering_artifacts.py`
  is untouched, being the hash-locked file of the released 0.7.1 evaluator.
  The retirement reaches this repository's own verdicts only when the root
  evaluator next advances. The evaluator/candidate boundary is respected
  rather than bypassed, and the divergence between the two copies is pinned
  by test instead of being left implicit.

## Requirement coverage

| Requirement (#208) | Implementation | Test or evidence | Result |
| --- | --- | --- | --- |
| Step 1: delete the four adapters, four scripts and their tests; keep retained evidence | #206 deletes 12 paths; the 0.6.0 artifacts are untouched | `test_every_deleted_path_is_absent`, `test_every_retained_evidence_digest_still_verifies` | PASS |
| Step 2: remove the bootstrap/exclusion branches from `publish-pypi.yml` and `pages-publication.yml` | #206 (581 lines removed, including `publish_dashboard.py`); #230 renames the temporary directory | `test_the_publication_path_has_no_predecessor_view_adapter`; grep finds no `bootstrap` in the three workflows | PASS |
| Step 3: remove `predecessor-view` from `OPERATIONS`, `_external_evaluator_files`, the `--help` expectation and the surface checker | #206; the checker now forbids the string | `test_the_retired_operation_is_absent_from_the_published_surface`; ephemeral-wheel reading in the evidence document | PASS |
| Step 4: delete `_validate_predecessor_view_evidence` from the template validator, tolerate historical fields, keep `RLS-SEH-012/014/015` valid | #230 (585 lines removed) | `test_every_deleted_name_is_absent_from_the_candidate_copy`, `test_the_closed_release_artifacts_are_inert_data`; 0 errors and identical diagnostics under both copies | PASS |
| Step 5: drop `repository_tools/interpreter_safety.py` | Not done; the issue itself cross-references P1-8; tracked in #220 | Disclosure 3 of #206 | PASS as an explicit, tracked deferral |
| Step 6: repair work order and superseding ADR for `ADR-REB-009` | `WO-REB-028`, `WO-REB-029`, `ADR-REB-012`, amended `ADR-REB-009` | Graph validates | PASS |
| Acceptance 1: grep returns only historical artifacts | Remaining hits outside `docs/engineering/` are the hash-locked root validator, the forbid entry, and negative tests | grep on `a9f3118` | PASS, with the unavoidable root-copy exception |
| Acceptance 2: no `repository_tools` import in `se_harness/` | — | grep | PASS |
| Acceptance 3: full graph reports 0 errors | — | 1,001 / 0 / 471 under both copies | PASS |
| Acceptance 4: no bootstrap-tuple branch in release-qualification or publish-pypi | — | grep | PASS |
| Guarantee at risk: 0.6.0 evidence stays tracked and hash-bound | Untouched | `test_the_predecessor_lock_digest_of_the_closed_contract_is_unchanged` | PASS |

## Blocking findings

None.

## Non-blocking findings

- **IMPORTANT — three notes still describe the removed feature as live.**
  `harness-dashboard-publication.md` (lines 35 and 88),
  `release-qualification-roles.md` (lines 25 and 40) and
  `evaluator-migration-rehearsal.md` (line 67) still say the Pages workflow
  runs `qualify predecessor-view` or list it as a qualification role. #206
  disclosed this (disclosure 5); #230 did not pick it up. These paths are
  ungoverned under `AGENTS.md`, so an ordinary pull request corrects them
  without a work order.
- **IMPORTANT, process rather than correctness — the `workflow_dispatch`
  rehearsal that `VER-REB-012` requires** for the two edited workflows is
  still outstanding, as both pull requests state. It is an input to the
  `VREC-REB-026` verification decision, not to whether the acceptance criteria
  of #208 are met.
- **MINOR — `CANDIDATE_VALIDATOR_DELETIONS` pins root-copy line numbers**
  (58, 791, 1133, and so on). This is intentional as a divergence tripwire,
  but it will fail the moment the root evaluator advances to a release that
  carries the deletion and must be removed in that same change.

## Recommendation

Merge #206 and then #230 (or #230 into #206, then #206 into `main`) once the
accountable verifiers have decided `VREC-REB-026` and `VREC-REB-027`. Close
#208 with a note that step 5 is tracked in #220, and follow with a notes-only
pull request correcting the three stale references listed above.

## Method

Readings were taken on a Linux host from the tree at `a9f3118` and from
`main` at `290f2fb`: the acceptance-criteria greps from #208, both validator
copies run with `--root .`, the retirement, release-orchestration, dashboard
and interpreter-safety unit suites (153 tests; the single error is a
`git rev-parse` failure of a host without Git at the time of the run, not a
defect of either pull request), and the GitHub compare and mergeability views
of both branches.
