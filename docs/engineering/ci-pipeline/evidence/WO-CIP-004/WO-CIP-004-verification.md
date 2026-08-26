# WO-CIP-004 implementation evidence

artifact: WO-CIP-004
checkpoint: handoff
formal_snapshot_sha256: 4ae17c000b1fa7fb62adec2352e870cf4b3de1218a3a11ed5c9a0f6f5b38885d

Retained by the implementation actor on 2026-08-26. This file is evidence. It
does not complete, verify, or release the work order.

## Evaluators

- Governing: released `se-harness 0.6.0` installed outside the checkout from
  the exact wheel `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`
  (`C:\Users\mathi\se-harness-eval`, invoked with `-I`).
- Candidate: this checkout, `python -m se_harness` from the repository root.
  `release-unit` is a candidate command; the root's released evaluator does
  not have it and does not need it.

## What was built

- **Template (CIP-RLU 1, 4).** `RELEASE_CONTRACT.template.md` (standard
  template) carries `candidate_commit` and `previous_release_tag` with a
  comment naming the derivation command; a "Release unit" section stating
  that `gates` is the measured census, that a merge to `main` after the cut
  changes nothing, and that a fix to the release is a new candidate commit on
  `candidate/<version>` with a new contract; and a stop condition in
  "Rollback criteria and procedure" that names a non-ancestor candidate or an
  `E-CIP-001` difference — not a later `implemented` work order.
- **`harnessctl release-unit` (CIP-RLU 2).** `se_harness/release_unit.py`:
  walks `--first-parent <tag>..<commit>` oldest first; a non-merge commit
  contributes its own `Harness-Work-Order` trailer, a merge the trailers of
  its merged commits (`<merge>^1..<merge>^2`), because forge merges carry no
  trailer; one row per work order with lifecycle status and a
  packaged-surface flag from the catalog (`se_harness/`,
  `templates/repository/standard/`, `pyproject.toml`); `untraced` commits;
  `--exempt <full sha>` repeatable; `--contract REL-…` compares
  `candidate_commit`, `previous_release_tag` and `gates` and reports
  `E-CIP-001`; `--json` (schema `se-harness-release-unit-v1`) and `--toml`
  (the `gates` array). Exit 1 on an untraced commit, a non-`implemented`
  work order, or any finding. Mutates nothing; no network.
- **Stop condition 1 measured.** The 0.6.0 root validator accepts the two
  new fields on an approved contract as unknown keys: with them added to
  `REL-SEH-006`, `validate` reports 913 artifacts, 0 errors, 50 warnings
  (edit reverted).
- **Tests.** `tests/test_release_unit.py` (five): the census on a fixture
  history with a tag, three forge-style merges carrying three distinct
  trailers and one without, and a direct trailed commit — rows, commits,
  statuses, `untraced`, blockers, the `gates` array; exemptions need a full
  commit id and a later merge to `main` does not move the unit; the contract
  comparison reports `E-CIP-001` on each of the three differences; the CLI is
  registered and the template names the unit; the CLI derives against a
  stubbed catalog and prints the human and TOML forms.
- **Documentation (CIP-DOC).** `docs/notes/harnessctl-reference.md`
  (inventory row and a "Release unit derivation" section),
  `docs/notes/developing-se-harness.md` ("Release sequences": the contract
  step and the late-fix route), `docs/notes/ci-pipeline.md` ("After
  WO-CIP-004").

## Commands and results

| Command | Evaluator | Result |
| --- | --- | --- |
| `harnessctl preflight . --work-order WO-CIP-004 --phase review` | released 0.6.0 | `PASS` |
| `harnessctl validate .` | released 0.6.0 | PASS, 913 artifacts, 0 errors, 50 warnings on the stacked branch; 930 artifacts, 0 errors, 50 warnings on `main` after the re-base |
| `harnessctl doctor .` | released 0.6.0 | 0 FAIL |
| `python scripts/validate_release_distributions.py --root .` | candidate | PASS (1 distribution-bearing record) |
| `python scripts/check_portable_release_surface.py --repository .` | candidate | PASS |
| `git diff --check` | git | clean |
| `harnessctl check . --artifact WO-CIP-004 --checkpoint handoff --changed-path … --changes-complete --json` (complete set below) | released 0.6.0 and candidate | before this file existed: blocked only by `QGP-G4I-EVIDENCE`; both reported formal snapshot `b0962ede…` on the stacked branch; after the stack merged the two unbound commits were re-based onto `main` (`98edd14`) and both evaluators report `4ae17c000b1fa7fb62adec2352e870cf4b3de1218a3a11ed5c9a0f6f5b38885d` there |
| `python -m unittest` over `test_release_unit`, `test_harnessctl`, `test_progressive_documentation`, `test_artifact_catalog`, `test_instruction_architecture`, `test_validation_taxonomy` | candidate | OK, 1 skip |
| `python -m unittest discover -s tests -p "test_*.py"` | candidate, Windows 11, CPython 3.14 | on the stacked branch `Ran 916 tests` — `OK (skipped=23)`; on the `main`-based branch before deviation 7 `Ran 958 tests` — 1 failure, the pre-existing one; after it `Ran 958 tests in 356.949s` — `OK (skipped=24)` |
| `python -m se_harness release-unit . --from v0.6.0 --to e98b7885… --contract REL-SEH-015 --json` (`VER-CIP-001` scenario 4; retained as `release-unit-v0.6.0-e98b788.json`) | candidate | see below |

## Scenario 4: the 0.7.0 unit measured from commit trailers

Over `v0.6.0..e98b788` (the `main` on which the 0.7.0 contracts were
drafted): 90 first-parent commits, 39 of them merges. The census traces
eight work orders — `WO-ADS-001`, `WO-ADS-002`, `WO-HBI-003`, `WO-REB-018`,
`WO-REB-019`, `WO-REB-023`, `WO-RLO-006`, `WO-VSP-007` — and reports **80
untraced commits**: 51 direct commits on `main` and 29 merges whose merged
commits carry no trailer either. `REL-SEH-015` names 36 gates; the
comparison reports four `E-CIP-001` findings (no `candidate_commit`, no
`previous_release_tag`, 30 gates the commits do not trace and two the
contract does not list — `WO-REB-023` and `WO-RLO-006`, which reached
`implemented` after its freeze — and the incomplete derivation).

Reading: the trailer discipline on *commits* is recent (the managed CI reads
the trailer from the pull-request body, and until this month many governance
commits landed directly on `main` without one). A commit-trailer census
therefore cannot reproduce the 0.7.0 unit, and the 0.7.0 release keeps its
allow-list contract. The measurement is exact for history written under the
discipline — every commit of this packet carries the trailer — so the first
unit the command freezes cleanly is the one after 0.7.0.

## Deviations from the specification, recorded for the completion decision

1. **`E-CIP-001` is emitted by the command, not by the validator.**
   `CIP-RLU` 3 placed it in the candidate validator. The managed validator
   script is git-free by design and runs on depth-1 checkouts in the managed
   lane, where the derivation is impossible; putting `git log` into it would
   change its character and produce a warning on every hosted run. The
   comparison lives in `release-unit --contract` and fails the command. The
   approval-time gate (a predicate in `QUALITY_GATES.json`, as
   `authoring_ready` is) is the right home and is outside this work order's
   scope; it is a follow-up.
2. **The 0.7.0 unit cannot be reproduced from commit trailers.** Scenario 4
   above: 80 of 90 first-parent commits are untraced. The command reports
   this honestly; it does not fall back to pull-request bodies (network, a
   forge dependency) — that would be a separate decision.
3. **The template changes land in the standard template only.** The root's
   0.6.0 template and validator follow at the root-evaluator upgrade; the
   fields validate as unknown keys today (stop condition 1 measured).
4. **The packaged-surface prefixes are declared in the module.** They mirror
   `pyproject.toml`'s packages, package-data and data-files; a packaging
   change must update them. A derivation from `pyproject.toml` at run time
   was judged not worth the coupling for a flag that informs, not decides.
5. **The template validator is in scope and unchanged** (deviation 1).
6. **The two implementation commits were re-based onto `main` after the
   stack merged.** PRs #171–#174 were merged from rebased copies of their
   branches, so this work order's branch base was no longer in `main`'s
   history. The start and implementation commits carry no record and were
   cherry-picked onto `main` (`0c02aec`, `3906eb6`); the formal snapshot and
   the suite were re-measured there. This is not a rebase of a bound commit.
7. **A pre-existing failure on `main` fixed here.** The clean suite on the
   `main`-based branch reported one failure, present on `main` itself:
   `tests/test_artifact_authoring_policy.py::test_repository_dry_run_report_is_retained_and_matches_a_fresh_run`
   compared the retained WO-AUT-002 dry-run report (248 mapped) with a fresh
   run over the 254 requirements `main` now has. Owner decision 2026-08-26:
   fix it under this work order (`tests/` is in scope). The test now compares
   the `skipped` count and the set of `unmatched` requirements, and requires
   the fresh `mapped` total to be at least the retained one.

## Complete changed-path set

```
docs/engineering/ci-pipeline/evidence/WO-CIP-004/WO-CIP-004-verification.md
docs/engineering/ci-pipeline/evidence/WO-CIP-004/release-unit-v0.6.0-e98b788.json
docs/notes/ci-pipeline.md
docs/notes/developing-se-harness.md
docs/notes/harnessctl-reference.md
se_harness/cli.py
se_harness/release_unit.py
templates/repository/standard/docs/engineering/templates/RELEASE_CONTRACT.template.md
tests/test_artifact_authoring_policy.py
tests/test_release_unit.py
```

## Deviation acceptances

Recorded on 2026-08-26 from the owner's interactive answers, before the
completion decision. These are the owner's statements; the assurance decision
on `VREC-CIP-004` remains separate.

| Deviation | Owner answer |
| --- | --- |
| 1 - `E-CIP-001` emitted by the command, not the validator | Accept: the approval-time predicate is a follow-up work order. |
| 2 - the 0.7.0 unit cannot be reproduced from commit trailers | Accept: 0.7.0 keeps its allow-list contract; the first unit frozen by candidate commit is the one after 0.7.0. |
| 3 - template changes in the standard template only | Accept. |
| 4 - packaged-surface prefixes declared in the module | Accept. |
| 5 - template validator unchanged | Accept. |
| 6 - re-based onto `main` after the stack merged | Owner instruction 2026-08-26: "previous PR have been merged"; unbound commits only. |
| 7 - pre-existing brittle test on `main` fixed here | Owner decision 2026-08-26: fix it under WO-CIP-004. |

## Not done

- The completion transition; `VREC-CIP-004`.
- The approval-time predicate for `E-CIP-001` (deviation 1) and a
  pull-request-body derivation (deviation 2): follow-ups, not started.
