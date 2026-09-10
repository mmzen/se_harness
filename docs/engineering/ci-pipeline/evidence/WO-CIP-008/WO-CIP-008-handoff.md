```toml
artifact = "WO-CIP-008"
checkpoint = "handoff"
formal_snapshot_sha256 = "ebd371153526b6623a9ccd584f8505ad2494bc3c87c075acdafbc63cf6ac4eec"
rebound_at = "2026-09-10T11:11:02Z"
```

# WO-CIP-008 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

`ARCH-CIP-001` and `REQ-CIP-002` name the rehearsal job `upgrade-rehearsal`,
the name `WO-CIP-007` gave it on 2026-09-08. Each carries an amendment record
dated 2026-09-10 under this work order: the architecture's names the former
name, the renaming work order and its verification record; the requirement's
also names the reconcile job's removal under `WO-CIP-001`. The Rationale of
`REQ-CIP-002` now describes the reconcile job without its retired name. In
both files only `updated` changed in the front matter; the statement, the
relations, the lifecycle events and the decision assessment are byte-identical
to `main`. `tests/test_ci_pipeline.py` gains `DefinitionNamesTests`, which
reads the body of every artifact under the domain's `architecture/` and
`requirements/` and fails, naming file and line, on any occurrence of the old
name outside an `## Amendment record` section. No workflow, script, module,
managed template or hash-locked root file changed. The domain index names
the repair. Rules `CIP-AMD-001` to `CIP-AMD-005` of `SPEC-CIP-004` are mapped
to their evidence below.

## Evaluators

- Governing: released `se-harness 0.17.0` installed from the wheel file
  outside the checkout (`C:/Users/hok/se-harness-eval-0170`), run `-I`, for
  `validate`, `doctor`, `preflight`, `evidence` and the handoff check.
- Candidate: this checkout, branch `wo/cip-008-definition-repair`, off
  `main` at `7457a401` (the merge of #438, this work order's packet). The
  start event was taken by the `delegated-executor` role at `be6c6fc8` under
  the `validate` check that was `success` for the base.

## Rule-to-evidence map

| Rule | Evidence | Reading |
| --- | --- | --- |
| `CIP-AMD-001` | `ARCH-CIP-001` line 43 and its amendment record | Components names `upgrade-rehearsal`; the record names `governance-migration`, `WO-CIP-007`, `VREC-CIP-007` and 2026-09-08 |
| `CIP-AMD-002` | `REQ-CIP-002` lines 27, 29, 41, 49 and its amendment record | the rehearsal job is `upgrade-rehearsal` in the Required response and the job count; the Rationale says "the upgrade rehearsal" and "the rehearsal's reconcile job"; the record dates the rename and names the removal under `WO-CIP-001` |
| `CIP-AMD-003` | `readings.md`, front-matter diff | `updated` 2026-08-26 to 2026-09-10 in both; no other front-matter line differs |
| `CIP-AMD-004` | `readings.md`, the grep before and after; `DefinitionNamesTests` | in the two artifact bodies the old name occurs only inside the two amendment records; the test passes and pins it |
| `CIP-AMD-005` | the domain index bullet; the change set | the index names the repair and this branch; the change set holds five paths, all inside `[execution_scope]`, none under `.github/`, `scripts/`, `repository_tools/` or a managed path |

## Readings

- Released 0.17.0 `validate`: PASS, 1,480 artifacts, 0 errors, 46 warnings
  (all `W013`), 0 advisories.
- Released 0.17.0 `doctor`: 99 `PASS`, no `FAIL`.
- Released 0.17.0 `preflight --work-order WO-CIP-008`: PASS at phase `start`,
  the work order `in_progress`.
- `python -m unittest tests.test_ci_pipeline`: 36 tests, OK, on Windows 11
  with Python 3.13; the local full suite is the control recorded in the
  completion reason, the hosted Linux lane is the record.
- Managed lane at `be6c6fc8` (the start commit): blocked on
  `QGP-G4I-EVIDENCE` only, before this packet existed; every other lane
  `success`.

## Disclosures

1. Rule `CIP-AMD-004` says the old name occurs under the two directories
   "only inside an amendment record". Read over whole files, the acceptance
   grep of issue #433 also returns three front-matter lines: the `measure` of
   `REQ-CIP-009` ("named after the retired governor or governance-migration
   mechanisms", approved 2026-09-08 under `WO-CIP-007`'s packet and outside
   this scope) and the `source` and `measure` of `REQ-CIP-010` itself, which
   locate the finding and state this measure. Each names the retired name as
   retired; none describes the job. The test therefore reads artifact bodies
   for the rule and pins those two front-matter mentions as the known set, so
   a new one fails the test. The rule's wording is left to the owner's
   reading at verification.
2. The Rationale of `REQ-CIP-002` describes the pipeline as it was when the
   requirement was written. It now says "the upgrade rehearsal" and "the
   rehearsal's reconcile job" for the two jobs, which is the reading
   `SPEC-CIP-004` leaves undecided; the amendment record gives both former
   names.
3. Historical evidence packets and verification records under the domain
   (`WO-CIP-001` to `WO-CIP-007`) keep the old name as a statement of what
   was true when written; they are outside `[execution_scope]` and the grep
   of acceptance 2 does not cover them.

## Changed paths

- `docs/engineering/ci-pipeline/architecture/ARCH-CIP-001.md`
- `docs/engineering/ci-pipeline/requirements/REQ-CIP-002.md`
- `docs/engineering/ci-pipeline/README.md`
- `docs/engineering/ci-pipeline/evidence/WO-CIP-008/` (this packet,
  `readings.md`, `handoff.json`)
- `docs/engineering/ci-pipeline/work-orders/WO-CIP-008.md` (lifecycle
  events only)
- `tests/test_ci_pipeline.py`
