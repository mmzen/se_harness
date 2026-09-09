# WO-AUT-006 verification evidence

Retained under `VER-AUT-004` for the closing of the compatibility windows.
Measurements were taken on Windows 11 on 2026-09-09, on the branch
`wo/aut-006-close-the-windows`, whose base is `main` at `b11ea537` (the merge
of the packet, PR #423). The governing evaluator is released 0.17.0,
installed from the wheel file in `C:/Users/mathi/se-harness-eval-0170`
(`se_harness-0.17.0-py3-none-any.whl`, `sha256:305c7cbc…cced`), run with `-I`
from outside the checkout. The candidate is this checkout's package. The
hosted Linux lane is the record for the suite; the Windows readings are the
local control, labelled as such.

## Authorization

- 2026-09-07: issue #381 owner decision 3, "migrate the corpus, then
  close": the `W014`/`W015` branches close in the candidate after the
  migration, with the `W-ECP-002` grace and the `WEX-ECP-030` v1 hint; the
  `prepared_at` and `execution_scope` gaps stay, documented as permanent.
- 2026-09-08: `WO-AUT-005` merged (`fae52e1b`); `SPEC-AUT-003` `AUT-MIG-012`
  names this work order as the following one.
- 2026-09-09: the owner approved `REQ-AUT-009`, `SPEC-AUT-004`, `VER-AUT-004`
  and `WO-AUT-006` by selecting "Approve all four (Recommended)" on PR #423,
  and kept the managed `TRACEABILITY.md` template out of scope by selecting
  "Keep the template out of scope (Recommended)". Start, completion and
  record preparation are the delegated executor's under
  `[delegation] class = "execution"`, each taken while the required
  `validate` check is `success` for the head, read at the base of PR #431.

## Baseline and candidate, count by count

The released 0.17.0 evaluator and the candidate on the same tree, the
implementation head `bb2e73a4`:

| Reading | Artifacts | Errors | Warnings | Advisories | Per code |
| --- | ---: | ---: | ---: | ---: | --- |
| released 0.17.0, `main` at `b11ea537` (baseline, before the change) | 1,450 | 0 | 46 | 0 | `W013` 46 |
| released 0.17.0, the branch | 1,450 | 0 | 46 | 0 | `W013` 46 |
| candidate, the branch | 1,450 | 0 | 46 | 0 | `W013` 46 |

The released evaluator still carries the windows and reads none of `W014`,
`W015` on this corpus; the candidate, which no longer has them, reads the
same counts. The two readings are equal per code (`AUT-WIN-016`). The 46
`W013` are the historical records outside their canonical locations; the
baseline was 44 before the 0.17.0 release records and the wave 3 records
landed on `main`.

## Code inventory before and after

| Symbol | Before, at `b11ea537` | After |
| --- | --- | --- |
| `codes.W014`, `codes.W015` | declared under "Installed validator: a warning" | gone |
| `codes.W019` | declared with the preflight warnings | gone |
| `codes.W_ECP_002` | declared with the control-plane warnings | gone |
| `validation_architecture.RELATION_TARGET_TYPES[("architecture", "constrains")]` | `{"requirement", "specification"}` | gone |
| `architecture_traceability_state` states | `typed`, `dual_declared`, `legacy_requirement_trace`, `legacy_specification_trace`, `legacy_ambiguous`, `missing_typed_relations`, `invalid`; `legacy_targets` field | `typed`, `missing_typed_relations`, `invalid`; a `constrains` key is the issue "architecture relation 'constrains' is retired; declare addresses and conforms_to" |
| `decision_assessment_state` on a missing table | `legacy_missing` for a completed architecture, else `missing` | `missing` for every architecture |
| `validate_decision_assessments` | `W014` and the legacy `E015` message on `legacy_missing` | gone; `E014` through the `missing` path, `E015` for `adr_required` without a deciding ADR |
| `preflight` relevance and applicability | four-way branch on the traceability state; `W019` on `legacy_missing` without a selected ADR | the `typed` state alone; no `W019` |
| `dashboard_snapshot.TEMPORAL_REASSESSMENT_RELATIONS["architecture"]` | `addresses`, `conforms_to`, `constrains` | `addresses`, `conforms_to` |
| dashboard assessment states | `legacy_adr_covered`, `legacy_adr_missing` among them | gone |
| `workflow_predicates.review_evidence` | header first, then a substring fallback passing with `W-ECP-002` | header only; a packet without one is `not_assessable`, the message names `harnessctl evidence` |
| `workflow_contract.RETIRED_QUALITY_GATES_SCHEMAS` and the v1 re-raise | `{"se-harness-quality-gates-v1"}` and a `WEX-ECP-030` hint | gone; the loader's own schema error |
| `docs/notes/diagnostic-codes.md` | rows for the four codes | regenerated, none of the four; `--check` passes |

`grep -rn` over `se_harness/` after the change finds none of `legacy_missing`,
`legacy_requirement_trace`, `legacy_specification_trace`, `legacy_ambiguous`,
`dual_declared`, `legacy_targets`, `legacy_adr_covered`, `legacy_adr_missing`,
`W_ECP_002`, `RETIRED_QUALITY_GATES_SCHEMAS`, `"W014"`, `"W015"` or `"W019"`;
`test_no_package_module_names_a_closed_branch` keeps it so.

## The two permanent branches

| Branch | Where | Reading at `b11ea537` |
| --- | --- | --- |
| a record decided before preparation existed carries no `prepared_at`; its decision timestamp is read from its last lifecycle event | `se_harness/engine/validation_lifecycle.py`, `legacy_decision_record` | 84 of 230 verification and release records |
| a work order approved before the scope contract carries no `[execution_scope]`; a checkpoint over it is not assessable | `se_harness/engine/validation_decisions.py`, the `table is None` branch | 111 of 261 work orders |

Each branch carries a comment naming `SPEC-AUT-004` `AUT-WIN-012` and the
note; `docs/notes/artifact-authoring.md`, "Permanent branches", holds the
counts. The counts were measured by reading every record and work order's
front matter under `docs/engineering/`.

## Acceptance scenarios

Run on a scratch worktree at the implementation head `bb2e73a4`
(`target/aut006_scenarios.sh`), on this corpus, with the candidate:

| Scenario | Mutation | Reading |
| --- | --- | --- |
| control | none | `1450 artifacts, 0 errors, 46 warnings, 0 advisories` |
| S1 | `constrains = ["REQ-ECP-001"]` added to the approved `ARCH-ECP-001` | 1 error: `[E016] [governance] …/ARCH-ECP-001.md: architecture relation 'constrains' is retired; declare addresses and conforms_to` |
| S2 | the `[decision_assessment]` table removed from `ARCH-AUT-001` | 1 error: `[E014] [governance] …/ARCH-AUT-001.md: architecture decision assessment is required`; the review preflight over `WO-AUT-001` reads `FAIL` with `A-E014` and no `W019` or `W014` |
| S3 | a retained handoff packet's header rewritten into the three substring lines | run at the bound commit, where the packet exists; recorded in the verification decision |
| S4 | `quality_gates_contract.json` with `schema = "se-harness-quality-gates-v1"` | `ContractError: …/quality_gates_contract.json must use schema se-harness-quality-gates-v2`; no `WEX-ECP-030`, no "retired schema" |
| S5 | the `constrains` refusal removed from `validation_architecture.py` (the window restored) | `test_the_retired_constrains_relation_is_refused_for_every_status` fails on every variant, `AssertionError: [] is not true`, naming the missing `E016` |

`ARCH-AUT-001` is `approved`, not `implemented`; the implemented case is the
fixture test `test_completed_architecture_without_assessment_is_refused_like_any_other`
(an implemented architecture without the table reads `E014` and the preflight
prints no `W019`), and the scenario is repeated on an implemented architecture
of this corpus at the bound commit before verification.

## Tests

Nine test files change; the suite goes 1,119 to 1,126 tests (discovered by
loading the base in a throwaway worktree and the branch in place):

| File | Change |
| --- | --- |
| `tests/test_compatibility_windows.py` | new, 7 tests: the registry and the index, the package names, the dashboard sets, the loader without its v1 hint |
| `tests/test_architecture_traceability.py` | the legacy classifier test becomes the refusal for every status and target set; the dual-declared test becomes "constrains beside typed relations is still refused" |
| `tests/test_adr_applicability.py` | the completed-legacy test becomes "refused like any other" (`E014`, no `W019`); no status is exempt, `implemented` added |
| `tests/test_workflow_compliance.py` | the header-less packet is `not_assessable`, nothing retained, the packet untouched; two freshness fixtures bind through the header; `CanonicalSnapshotTests.LF_DIGEST` re-pinned to `3e10adbb…` after the fixture bytes moved |
| `tests/test_workflow_execution.py` | `bind_handoff_evidence` writes a machine header and keeps the body; the retired-schema test expects the loader's own error |
| `tests/test_validation_taxonomy.py` | `W013` in place of `W015` as the rendered sample |
| `tests/test_dashboard_webui.py` | the architecture relation tuple is the typed pair |
| `tests/artifact_support.py` | `ARCH-001` and `ARCH-002` take `addresses`, `conforms_to` and a `[decision_assessment]` decided by the ADR beside each (`FIXTURE_ASSESSMENT`) |

Local control, Windows 11, `python scripts/run_tests.py --workers 4`: 1,126
tests in 99 s, 0 failures, 1 error, 23 skips; the error is this machine's
documented baseline (`test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`,
a `WinError 5` `rmtree` of a temporary `.git`). The owner-region byte-bound
failure of the earlier baseline is gone since `main` rewrote `AGENTS.md` at
the 0.17.0 adoption. Modules run alone after the change: `test_workflow_compliance`
42, `test_workflow_execution` 70, `test_architecture_traceability` 12,
`test_adr_applicability` 8, `test_compatibility_windows` 7, all OK.

## Governing readings

| Command | Result |
| --- | --- |
| `validate . --advisories` (released 0.17.0, `-I`) | PASS, 1,450 artifacts, 0 errors, 46 `W013`, 0 advisories |
| `validate . --advisories` (candidate) | the same |
| `doctor .` (released 0.17.0) | exit 0, 99 `PASS`, no failure |
| `preflight . --work-order WO-AUT-006 --phase review` (released 0.17.0) | PASS |
| `scripts/validate_release_distributions.py --root .` | PASS, 14 records |
| `python -m se_harness --help` | exit 0 |
| `python -m repository_tools.diagnostic_code_index --check` | the page matches the source |

## Scope

`git diff --quiet b11ea537` over the root managed set, `templates/` and
`docs/engineering/templates/` reports no difference; the only files under
`docs/engineering/` in the change set are the four amended specifications
and this domain's work order and evidence. No corpus artifact changes.

## Hosted lane

Recorded in the handoff file beside this one once the pull request's lanes
have run at the implementation head, and in the lifecycle events at
completion and preparation.

## Disclosures

1. The shared fixture corpus `tests/artifact_support.py` still built its two
   architectures in the legacy shape (`constrains`, no assessment), which
   the closed windows refuse; 24 test modules read it. It now builds the
   typed shape, which is why the change touches nine test files where the
   work order named four, and why `CanonicalSnapshotTests.LF_DIGEST` moved.
2. The `not_assessable` message of `QGP-G4I-EVIDENCE` gained a second
   sentence naming `harnessctl evidence`; the first sentence is unchanged,
   so every reader that matched it still does.
3. `parse_evidence_header` returns `None` for a packet without a header
   rather than raising; the first rewrite of the predicate treated that as
   a raise and crashed on every header-less candidate file, which 63 tests
   caught before the fix. The predicate now skips such files.
4. `ARCH-AUT-001`, used for scenario S2, is `approved`; the implemented
   case is covered by the fixture test and is repeated at the bound commit.
5. The message "new or ongoing architecture requires typed addresses and
   conforms_to relations" lost its first three words, since every
   architecture is now held to it.
6. The `TRC-008` sentence of the managed `TRACEABILITY.md` template still
   calls `ARCH.constrains` compatibility-only; the owner kept the template
   out of scope, and the sentence is owed to the next managed-template work
   order (`AUT-WIN-018`).
