# WO-CIP-007: the governing readings and the suite

`VER-CIP-003`'s regression row: "suite at its baseline; graph 0 errors under
the released 0.16.0 evaluator; no managed path changed". Every reading below
is the Windows workstation on 2026-09-08, on the branch
`wo/cip-007-pipeline-hygiene` after `main` was merged in at
`560973cf12452d1c91b5a198c6a74d11af383d49` (the merge of #414). The branch
started from `fae52e1b`; `main` moved three times during execution, and every
reading in this file was taken again after the merge. No path this work order
changes moved on `main`: `git diff fae52e1b 560973cf` is empty over
`.github/`, `scripts/`, `repository_tools/release_distribution.py` and the
five test modules.

## The governing evaluator

The governing readings come from the released 0.16.0 evaluator installed
outside the checkout from the wheel file, run isolated:

    C:/Users/mathi/se-harness-eval-0160/Scripts/python -I -m se_harness <command> .

| Command | Result |
| --- | --- |
| `validate .` | `PASS`, 1,431 artifacts, **0 errors**, 44 warnings, 0 advisories; every plane E0 except `maintenance` E0/W44 |
| `doctor .` | exit 0: 97 `PASS` checks, 44 `WARN W013`, no failure |

All 44 warnings are `W013` — an artifact valid outside its canonical location
— and every one of them names a historical release or verification record
under `docs/engineering/release-*/` or a `VREC-DOC-*` at the root of
`docs/engineering/`. None names a path this work order touches. `doctor`
reports every managed path as `matches distribution`, including
`.github/workflows/engineering-harness.yml`: the managed template and its
hash-locked root copy are unchanged, as `WO-CIP-007`'s constraints require.

## The candidate source's own checks

| Command | Result |
| --- | --- |
| `python scripts/validate_release_distributions.py --root .` | `PASS (13 distribution-bearing records)`, exit 0 |
| `python -m se_harness --help` | exit 0 |

## The suite

    python scripts/run_tests.py --workers 4

| Run | Tests | Wall | Verdict |
| --- | ---: | ---: | --- |
| candidate, this branch after the merge | 1,087 | 93 s | 1 failure, 1 error, 23 skips |

The two names are this machine's documented Windows baseline, both recorded
before this work order (`WO-TST-004`, and in the handoffs of `WO-AUT-004`,
`WO-ECP-012` and `WO-CIP-006`):

- `test_instruction_architecture.OwnerInstructionRegionTests.test_owner_region_stays_within_the_size_bound`
  — 6,024 bytes against a 6,000-byte bound. The bound is a byte count and the
  worktree is CRLF: the region is 55 lines, so the committed LF bytes are
  5,969, under the bound, and the hosted Linux lane passes. `AGENTS.md` is not
  in this work order's change set.
- `test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`
  — `shutil.rmtree` of a temporary `.git` fails with `WinError 5` on a
  read-only object file. A Windows temporary-directory effect, not an
  assertion.

The failure set therefore equals the baseline. The suite gained 11 tests,
1,076 to 1,087, counted by loading both trees with `unittest`'s discovery — the
base in a throwaway worktree at `560973cf`, the branch in place:

| Tree | Discovered | `test_ci_pipeline` | `test_release_orchestration` |
| --- | ---: | ---: | ---: |
| base, `560973cf` | 1,076 | 25 | 23 |
| this branch | 1,087 | 35 | 24 |

The 11 are the 10 methods of `PipelineHygieneTests` (`CIP-ONE-016`) and the
manifest-refusal test of `CIP-ONE-013`. No test was deleted, and no other
module's count moved.

Modules that carry a changed assertion, run alone:

| Module | Verdict |
| --- | --- |
| `tests.test_ci_pipeline` | 35 tests, OK |
| `tests.test_release_orchestration` | 24 tests, OK |
| `tests.test_standard_repository_lifecycle` | 29 tests, OK |
| `tests.test_integration_package` | 15 tests, OK |
| `tests.test_pypi_publishing` | 7 tests, OK |

## Changed assertions, and why each moved

| Test | Was | Is |
| --- | --- | --- |
| `test_ci_pipeline.CANDIDATE_EVIDENCE_WORKFLOWS` | key `governor-transition`, which built the expected concurrency-group regex | key `predecessor-evaluator-assessment` (`CIP-ONE-011`) |
| `test_ci_pipeline.OneBuildPerWorkflowTests` | the job `governance-migration`, its artifact, `needs` and outputs | `upgrade-rehearsal` throughout (`CIP-ONE-012`) |
| `test_ci_pipeline.PredecessorDerivationTests` | `jobs["governance-migration"]` | `jobs["upgrade-rehearsal"]` |
| `test_standard_repository_lifecycle` | `^  governance-migration:$`; `assertEqual(3, count("actions/checkout@v4"))` | `^  upgrade-rehearsal:$`; 0 floating and 6 lines naming one digest (`CIP-ONE-006`) |
| `test_integration_package` | the `needs` prerequisite `governance-migration`; `actions/checkout@11bd7190…`; `build==1.2.2.post1 setuptools==75.8.0 wheel==0.45.1` | `upgrade-rehearsal`; `actions/checkout@11d5960a…` (v4.4.0); the three `INTEGRATION_*` env values and the arguments that read them (`CIP-ONE-007`) |
| `test_pypi_publishing` | `identity_args+=(--evaluator-payload-sha256`; the `identity --help` probe; `# v1.14.2 peeled commit` | the unconditional flag, no `identity_args`, no `identity --help`; `# v1.14.2` (`CIP-ONE-006`, `CIP-ONE-009`) |

Every change is a rename of a workflow-level name or a tightening required by
a rule; no assertion was weakened and none removed. `test_release_build.py`
named no retired workflow name, job or artifact and is unchanged.
