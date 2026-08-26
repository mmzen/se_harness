# The CI pipeline and the release path

Repository-owned note. It records the measured shape of the continuous
integration and release path so that each work order of the `ci-pipeline`
domain can show what it removed. Authority stays with the formal artifacts
under `docs/engineering/ci-pipeline/`.

## Question this note answers

Why does the pipeline feel slow when every run finishes in minutes, and
what does each simplification increment change?

## Baseline, measured 2026-08-26 at `e98b788`

Runner wall-clock, last twelve runs per workflow: every workflow between
under one minute and five minutes. The cost is multiplication, not duration.

| Workflow | Trigger | Jobs | Steps | Role |
| --- | --- | ---: | ---: | --- |
| `engineering-harness.yml` (managed) | push + PR, unfiltered | 1 | 9 | governing evaluator: preflight, doctor, validate, dashboard |
| `candidate-evidence.yml` | push + PR, unfiltered | 7 | 44 | suite, wheel, predecessor acceptance, migration x2 platforms x2 runs, integration package |
| `predecessor-evaluator-assessment.yml` | push + PR, unfiltered | 1 | 9 | governor-transition plan and assessment |
| `publication-rehearsal.yml` | PR + push to `main`, cancelling | 2 | 10 | re-executes the release qualification on two platforms; digest-checks `publish-pypi.yml` |
| `release-candidate-replay.yml` | dispatch | 1 | 6 | hosted replay of the bound recipe |
| `publish-pypi.yml` | dispatch, `main` | 7 | 44 | resolve, qualify, tag and release, PyPI, Pages, observe |
| `publish-dashboard-pages.yml` | dispatch, `main` | 2 | 17 | standalone copy of the Pages jobs |

Totals: 1,963 lines of YAML, 21 jobs, 139 steps. Scripts under
`.github/scripts/`: 6,490 lines (`rehearse_publication.py` 3,187,
`publish_dashboard.py` 1,465, `build_integration_package.py` 1,038,
`publish_release.py` 540, `reconcile_maintenance_branch.py` 260).

Per push to an open pull request, on one commit:

| Work | Times |
| --- | ---: |
| full `unittest discover` | 4 |
| candidate wheel build | about 14 |
| install of the public predecessor evaluator | about 10 |
| nine-stage migration rehearsal | 8 |
| verification of the integration payload | 3 |
| checkout-cleanliness proof (same three lines) | 7 copies |

Release governance for 0.7.0: five release contracts (`REL-SEH-012` to
`REL-SEH-016`), four rejected because a work order reached `implemented`
after the allow-list was frozen; three release work orders; the approved
contract is 68 KB and `WO-RLS-011` is 39 KB. Since `v0.6.0`: 265 commits,
40 merged pull requests, 117 `docs` and `governance` commits against 26
`feat` and `fix`.

## What each increment changes

| Work order | Proposal | Removes | Measured after |
| --- | --- | --- | --- |
| `WO-CIP-001` | P1, P2 | the second run per push; four of five wheel builds; two reconcile-only jobs | pending |
| `WO-CIP-002` | P3, P5 | the Python copy of the qualification, the YAML parser and the digest file; the idle schema leg; the duplicated Pages jobs | pending |
| `WO-CIP-003` | P6 | three hand-edited constants and the silent skip on a version bump | pending |
| `WO-CIP-004` | P4 | the reject-and-re-issue loop on the release contract | pending |

The "Measured after" column is filled by each work order's evidence.

## What stays

The N-1 to N migration rehearsal, the acceptance of the candidate by the
public predecessor evaluator, the byte-identical recipe replay, and the
`pypi` environment decision. They protect a user; they were only run too
often.
