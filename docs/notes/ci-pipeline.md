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
| `predecessor-evaluator-assessment.yml` | push + PR, unfiltered | 1 | 9 | evaluator-transition plan and assessment |
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
| `WO-CIP-001` | P1, P2 | the second run per push; two of three workflow-level wheel builds; the reconcile-only job | implemented 2026-08-26, see below |
| `WO-CIP-002` | P3, P5 | the Python copy of the qualification, the YAML parser and the digest file; the idle schema leg; the duplicated Pages jobs | pending |
| `WO-CIP-003` | P6 | three hand-edited constants and the silent skip on a version bump | implemented 2026-08-26, see below |
| `WO-CIP-004` | P4 | the reject-and-re-issue loop on the release contract | pending |

The "Measured after" column is filled by each work order's evidence.

### After `WO-CIP-001`

- `candidate-evidence.yml`, `predecessor-evaluator-assessment.yml` and the
  standard template of `engineering-harness.yml`: `push` restricted to
  `main`, `release/**`, `candidate/**`; a cancelling concurrency group per
  workflow and ref. One run per commit on a pull request instead of two.
  The hash-locked root `engineering-harness.yml` follows at the root-evaluator
  upgrade.
- `candidate-evidence.yml`: six jobs instead of seven. The wheel is built
  once in `candidate-source` and handed down as
  `candidate-wheel-non-promotable-<sha>` with `SHA256SUMS`; `candidate-package`
  and both migration legs verify and never rebuild. Workflow-level wheel
  builds of the commit: 3 to 1. The cross-platform migration comparison is a
  step on job outputs, not a job.
- Kept, and why: the two migration runs per platform (`REQ-REB-017`'s
  determinism example); the integration package's own two builds and its
  retention job (`SPEC-IPK-001` rules 1 and 5: a different distribution with a
  local-version overlay, byte-equal across two builds, retained only after
  every matrix member passes).
- Per pull-request push, one commit: full suite 2 (was 4); wheel builds 5
  (was about 14: 1 candidate + 2 integration in `candidate-evidence`, 2 in
  the rehearsal, which `WO-CIP-002` addresses); predecessor installs about 5
  (was about 10); migration rehearsals 4 (was 8).

- Hosted reading, pull request #171 at `ff44da2` (2026-08-26): 13 checks
  pass; the repository-owned workflows ran on `pull_request` only and the
  superseded commit's runs were cancelled by the concurrency group; the root
  0.6.0 managed workflow still ran on `push` as well. The `candidate-evidence`
  log shows one `pip wheel` (in `candidate-source`), `candidate-package`
  verifying `SHA256SUMS: OK`, and the integration build comparing the two
  platforms' migration digests (`1bcca199…`). These are `VER-CIP-001`
  scenarios 1 and 2.

### After `WO-CIP-003`

- `repository_tools/predecessor_facts.py`: `derive` reads the declared root
  and the candidate version and exports the predecessor's version, wheel,
  wheel digest, payload digest, legacy acceptance-contract digest, and the
  migration scenario path and digest; `write-scenario` is the canonical
  scenario writer. Both fail closed with a `PRE0nn` code that names what is
  missing.
- `candidate-evidence.yml`: one derivation step in `candidate-source`, before
  any network access; `candidate-package` and both migration legs take the
  values from job outputs. Literals restating the evaluator in the
  repository-owned workflows: 8 → 0 (the pinned build-tool versions are not
  evaluator facts and stay). A version bump without its scenario fails the
  first job with the expected path instead of skipping four jobs.
- Tests that restated the same literals (`test_release_qualification`,
  `test_governance_migration`, `test_standard_repository_lifecycle`) now
  derive them through the module; the legacy contract digest lives in one
  table in the module.
- Not changed: the managed `engineering-harness.yml` keeps its version
  literal (`{{HARNESS_VERSION}}` in the template) until the root-evaluator
  upgrade; `predecessor-evaluator-assessment.yml` already derived its facts
  through `scripts/validate_governor_transition.py` and carries no literal.

## What stays

The N-1 to N migration rehearsal, the acceptance of the candidate by the
public predecessor evaluator, the byte-identical recipe replay, and the
`pypi` environment decision. They protect a user; they were only run too
often.
