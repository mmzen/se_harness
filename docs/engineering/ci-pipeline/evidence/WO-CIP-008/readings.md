# WO-CIP-008 readings

Measured on Windows 11 on 2026-09-10 on the branch
`wo/cip-008-definition-repair`, base `main` at `7457a401`. The governing
evaluator is released 0.17.0 in `C:/Users/hok/se-harness-eval-0170`, run
with `-I` from outside the checkout.

## The grep of issue #433, acceptance 2

Command:

    grep -rn governance-migration docs/engineering/ci-pipeline/architecture docs/engineering/ci-pipeline/requirements

Before, at `main` `7457a401`:

    docs/engineering/ci-pipeline/architecture/ARCH-CIP-001.md:43:`governance-migration` (N-1 to N scenario per platform),
    docs/engineering/ci-pipeline/requirements/REQ-CIP-002.md:27:`candidate-package`, once per platform in `governance-migration`, and twice
    docs/engineering/ci-pipeline/requirements/REQ-CIP-002.md:29:`governance-migration-reconcile` and `integration-package-retain`, exist only
    docs/engineering/ci-pipeline/requirements/REQ-CIP-002.md:41:- `candidate-package`, `governance-migration` and the integration-package
    docs/engineering/ci-pipeline/requirements/REQ-CIP-002.md:49:  `governance-migration` matrix, `integration-package` matrix).
    docs/engineering/ci-pipeline/requirements/REQ-CIP-009.md:13:measure = "... named after the retired governor or governance-migration mechanisms ..."
    docs/engineering/ci-pipeline/requirements/REQ-CIP-010.md:12:source = "... still name governance-migration, renamed upgrade-rehearsal by WO-CIP-007 ..."
    docs/engineering/ci-pipeline/requirements/REQ-CIP-010.md:13:measure = "grep governance-migration over ... returns only lines inside an amendment record, and a test pins it"

After, on this branch:

    docs/engineering/ci-pipeline/architecture/ARCH-CIP-001.md:92:component named the job `governance-migration`, its name when this
    docs/engineering/ci-pipeline/requirements/REQ-CIP-002.md:81:rehearsal job was `governance-migration` and `governance-migration-reconcile`
    docs/engineering/ci-pipeline/requirements/REQ-CIP-009.md:13:measure = "..." (unchanged, front matter, names the mechanism as retired)
    docs/engineering/ci-pipeline/requirements/REQ-CIP-010.md:12:source = "..." (unchanged, front matter, locates the finding)
    docs/engineering/ci-pipeline/requirements/REQ-CIP-010.md:13:measure = "..." (unchanged, front matter, states this measure)

Lines 92 of `ARCH-CIP-001` and 81 of `REQ-CIP-002` are inside the two
`## Amendment record` sections. The five body lines of the "before" reading
are gone. The three front-matter lines are disclosure 1 of the handoff.

## Front-matter diff against `main`

`git diff origin/main -- ARCH-CIP-001.md REQ-CIP-002.md`, front matter only:

    -updated = "2026-08-26"
    +updated = "2026-09-10"

once in each file. `id`, `type`, `title`, `status`, `owners`, `created`,
`statement`, `verification_method`, `verification_notes`,
`[decision_assessment]`, `[relations]` and every `[[lifecycle_events]]` entry
are byte-identical.

## Body diff against `main`

`ARCH-CIP-001`: one line changed (43, the Consumers component) and one
amendment record appended. `REQ-CIP-002`: four lines changed (27, 29, 41,
49) and one amendment record appended.

## Evaluator readings

| Command | Reading |
| --- | --- |
| `validate .` | PASS; 1,480 artifacts, 0 errors, 46 warnings (all `W013`), 0 advisories |
| `doctor .` | 99 `PASS`, no `FAIL`; every managed path matches its distribution |
| `preflight . --work-order WO-CIP-008` | PASS, phase `start`, `WO-CIP-008` `in_progress`, commit-bound verification `required` |

## Tests

| Command | Reading |
| --- | --- |
| `python -m unittest tests.test_ci_pipeline.DefinitionNamesTests -v` | 1 test, OK |
| `python -m unittest tests.test_ci_pipeline` | 36 tests, OK |
| `python scripts/run_tests.py` (local control, Windows) | recorded in the completion reason; the hosted Linux lane is the record |

Negative control: reinserting `governance-migration` into the Components
section of a scratch copy of `ARCH-CIP-001` makes `DefinitionNamesTests`
fail with `docs/engineering/ci-pipeline/architecture/ARCH-CIP-001.md:43` as
the offender.
