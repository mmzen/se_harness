# WO-REB-023 Verification Evidence

Date: 2026-08-26

Authority: non-authoritative retained candidate evidence. This file does not approve an
artifact, authorize a diff, verify work, merge, release, publish, tag, or deploy. It records
what was measured, on which interpreter, on which platform, at which commit, and what the
measurements do not cover, so that an accountable assurance decision can be taken over facts
rather than over a summary. Every rehearsal figure quoted here carries the rehearsal's own
field `authority = "This rehearsal records technical evidence only. It cannot approve,
verify, release, publish, deploy, or adopt an evaluator in the operational repository."`

Work order: `WO-REB-023`, `status = "implemented"`, assurance classification
`commit_bound_verification = "required"` decided by the repository owner with the rationale
that the `governance-migration` gate "is the only proof that released evaluator N-1 governs
the candidate N, and release approval reads it. A scenario that declared the wrong
identities, or a workflow pointed at the wrong scenario, would turn a real refusal into a
green gate, so assurance must bind the exact commit whose scenario and workflow produced the
reading."

Verification contract: `VER-REB-007`, "Predecessor-to-successor migration assurance",
`status = "approved"`, verifying `REQ-REB-016` and `REQ-REB-017`.

## 1. The tree these measurements describe

The work-order branch merged before verification was authorized, so the candidate cannot be
the branch tip: `capture-verification` requires the bound evidence file to be tracked at the
candidate, and this file does not exist on that branch. The candidate is therefore a fresh
commit taken from `main`, carrying only this evidence file, and the verification record sits
in a second commit above it.

- Base: `main` at `c189b58ca6b574c7067032a640e3c2c8a22cf089`, the merge of PR #166.
- `pyproject.toml` `version = "0.7.0"`; `se_harness/__init__.py` `__version__ = "0.7.0"`.
- Working tree clean before and after every measurement below: `git status
  --porcelain=v1 --untracked-files=all` empty, `git diff` exits zero.
- `core.autocrlf = true` in this checkout, so every figure here is a Windows-checkout figure
  unless it is explicitly a blob digest or a hosted reading.
- Formal artifact snapshot over this checkout at this commit:
  `e2e5a2891afda11a890315390800a24a93dcd886d06e6f1749a7e551e6ad84cf`, 890 artifacts. This is
  not the figure `WO-REB-023`'s implementation evidence binds — that one, `dc45e80d…` at 889
  artifacts, describes the candidate commit on the merged branch. The two differ because the
  graph moved, not because either is wrong, and neither may be substituted for the other.

The work order's own execution scope names
`docs/engineering/released-evaluator-boundary/evidence/`, so this file is inside it. The
verification record itself is not: `verification-records/` is outside every declared scope,
which is the ordinary consequence of a record being created after the candidate it names.

## 2. What independence meant here, concretely

`VER-REB-007`'s Independence section allows the implementation actor to build fixtures and
produce reports but not to define accepted diagnostics, omit required stages, decide which
mutations are harmless, or treat a passing candidate result as predecessor or human
authority. The same actor implemented `WO-REB-023` and took these measurements, which is a
disclosed limitation of this record and is stated again in section 10. What was done to make
the measurements independent of the implementation's own reasoning:

- The predecessor distribution was resolved **from the public index in this session**, not
  reused from the implementation's working directory, and its digest compared against the
  workflow pin afterwards rather than copied from it.
- The canonical form of every fixture was checked by a **re-implementation of the canonical
  writer from its specification** — ASCII-escaped, minimal separators, sorted keys, one
  trailing LF, UTF-8 — which does not import `se_harness`. A fixture that was canonical only
  because the repository's own writer produced it would still fail if the writer had drifted.
- The version-divergence refusal was provoked by **four different mechanisms**, none of them
  the mechanism the implementation used, and three of them without editing a tracked byte.
- Every claim about the rehearsal's authority boundary was read out of the report's own
  fields, and the report's retained bytes were independently re-canonicalized and searched
  for host-path leakage.
- The stage results were read field by field from the retained JSON. No figure below is
  taken from a runner's success flag or from the implementation's evidence.

## 3. Fixture identity: worktree bytes against the committed blob

All three fixtures are byte-identical in the worktree and in the commit, LF, zero CR bytes,
under the `.gitattributes` rule `tests/fixtures/governance_migration/*.json text eol=lf`.

| Fixture | Bytes | CR | SHA-256 (worktree = blob) |
| --- | --- | --- | --- |
| `candidate-0.6.0-to-0.7.0.json` | 3862 | 0 | `0b21462cc4e73055b4b701b76392091c4988b65e38860975e3c2f2d7c0d73b4a` |
| `historical-0.5.0-to-0.6.0.json` | 3485 | 0 | `393f639eb06fdec17a31386c5fc94f526cceba2e0efc95cbde6e1077f99b8324` |
| `synthetic-n-minus-1-to-n.json` | 3476 | 0 | `af2101d95784babdd3afaaccad16946ba04abbce866643c7e6cb4413ecb33daf` |

The independent canonical oracle reports all three **canonical**, and reads their declared
version pairs as `0.6.0 -> 0.7.0`, `0.5.0 -> 0.6.0` and `41.2.0 -> 42.0.0`. The historical
fixture's digest is the same value the implementation evidence quotes as unchanged, measured
here from `main` rather than from the branch.

## 4. Contract and adapter provenance

- `se_harness/governance_migration_contract.json` hashes to
  `61f2b658dd6fcf47846a57004425a94c86396e232fac57a52475d0a432c32087`, which is the value the
  rehearsal report carries as `contract.sha256`.
- `se_harness/governance_migration.py` hashes to
  `e8cdadd36e74494d793e98c9c70a718a87fd062a4929d51096da23238279fddc`, which is the value the
  report carries as `contract.implementation_sha256`.
- **All six** adapters named in the contract — `historical-` and `synthetic-` × prepare,
  assess, publish — declare that same `implementation_sha256`. Every
  "predecessor-compatible" adapter is therefore code from the tree under test. Section 9
  states what that bounds.

## 5. Predecessor origin, independently resolved

`pip download --only-binary=:all: --no-deps se-harness==0.6.0` from the public index, hashed
as a file:

- `se_harness-0.6.0-py3-none-any.whl` →
  `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`
- Workflow pin `PREDECESSOR_WHEEL_SHA256` in `.github/workflows/candidate-evidence.yml`:
  the same value. **MATCH.**
- The candidate scenario also declares that archive under
  `runtime_expectations.predecessor`. Guard `MIG229` refuses a rehearsal whose installed
  archive differs from the scenario's declaration, and the rehearsal passed, so the declared
  digest was checked against a wheel actually installed in an isolated environment — not
  merely found to equal the workflow's string.

For section 8's reproduction of the reported defect, `se-harness==0.5.0` was resolved the
same way: `se_harness-0.5.0-py3-none-any.whl` →
`974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f`, which is the value
`tests/test_governance_migration.py` carries in `PUBLIC_PREDECESSOR_ARCHIVES`.

## 6. Successor runtime, and the isolation property

The successor was built from `git archive HEAD` extracted outside the checkout, then
installed into a fresh `venv`. It is an **ephemeral, non-promotable** artifact; its digest is
traceability only.

- `se_harness-0.7.0-py3-none-any.whl` →
  `56f04e32f440ae93b019636575aece32bb1d4d86299761bbe97a4bbda775ade5`. This differs from the
  digest the implementation evidence records for its own successor build; a wheel built by
  `pip wheel` is not byte-reproducible across build directories, and no record binds either.
- Both environments were probed under `-I`: `se_harness.__file__` resolves inside the
  environment's own prefix and **not** inside the checkout, for the predecessor and the
  successor alike.
- The report's own `runtimes` block agrees, per role: `isolated: true`,
  `checkout_excluded: true`, `python_version 3.11.9`, versions `0.6.0` and `0.7.0`,
  `archive_sha256` `2a952eb6…` and `56f04e32…`. Guards `MIG212` (isolation and user-site),
  `MIG213` (package inside its declared environment) and `MIG225` (import search must not
  contain the checkout) each refuse the alternative, and none fired.

## 7. Complete positive rehearsal, twice, and the determinism property

Two consecutive rehearsals of `candidate-0.6.0-to-0.7.0.json`, predecessor `0.6.0`,
successor `0.7.0`, CPython 3.11.9, Windows, no network:

- `overall_result: pass`, `first_failed_stage: None`, both runs.
- `classification: {"affected_operations": [], "missing_capabilities": [], "outcome":
  "compatible"}`.
- `scenario.sha256 0b21462c…`, `scenario.fixture_sha256
  e5c79724f5616db220389fa91b8670e4273701addfb4914b4dda95144ed62f93` — the same
  `fixture_sha256` the hosted Linux run reported, so nothing converted the fixture in
  transit and nothing converts it here either.
- `semantic_sha256:
  f95be1a78223a40d652e40b19ca3c397813738b1d7238d1d5ae870823a52f660`, **identical across both
  runs**.
- Field-by-field comparison of the two whole reports: the **only** difference is
  `duration_ms` on each of the nine stages. Nothing else moved.
- The two retained report files are 9620 bytes each with **different** file digests
  (`9f0ec77b…`, `22ec672f…`) precisely because of those timings. The reproducible quantity is
  `semantic_sha256`; the file digest is not one, and must not be quoted as an expectation.

The nine stages, in contract order, all `pass`, with the mutation and authority fields read
from the report:

| Stage | Evaluator role | Target view | Observed mutations | Permitted | Authority effect |
| --- | --- | --- | --- | --- | --- |
| `prepare` | predecessor-compatible-adapter | predecessor-preparation-view-v1 | disposable-graph, disposable-root | identical | none |
| `validate-complete` | successor | complete | none | none | none |
| `reject` | lifecycle-simulator | fixture | disposable-graph | identical | proposal-status-rejected |
| `replace` | predecessor-compatible-adapter | predecessor-preparation-view-v1 | disposable-graph | identical | none |
| `assess` | compatibility-adapter | predecessor-assessment-view-v1 | none | none | none |
| `release-plan` | release-planner | selected-release | disposable-release-plan | identical | none |
| `publish-plan` | publication-planner | predecessor-publication-view-v1 | disposable-publication-plan | identical | none |
| `render` | renderer | predecessor-publication-view-v1 | disposable-render | identical | none |
| `adopt` | upgrade-adapter | standard-root | disposable-root, simulated-publication | identical | disposable-root-evaluator-selected |

`observed_mutations` equals `permitted_mutations` at every stage — nine for nine — and no
`authority_effect` names an operational effect. The two decision-bearing stages consume
fixtures rather than repository decisions: `reject` consumes
`DEC-MIG-CANDIDATE-REJECT` (`1d1599de…`) and `adopt` consumes `DEC-MIG-CANDIDATE-ADOPT`
(`bec660e7…`).

**The evaluator-selection invariant `VER-REB-007` names** is satisfied and was read out of
the report, not inferred: `state.evaluator_before = "predecessor"`,
`state.evaluator_after = "successor"`, `final_selected_evaluator = "successor"`, and the flip
occurs at `adopt`, the last stage, whose permitted effect is confined to a disposable root.

**The operational repository was not touched.** `operational_state.unchanged: true`, with
`git_head`, `git_refs_sha256` and `source_sha256` identical before and after
(`c189b58ca6…`, `0c5c6f7e…`, `0ea9f84e…`). Independently: `git diff` exits zero and porcelain
is empty after all seven rehearsals in this session.

**Authority boundary, from the report's own fields.** All ten entries of
`external_actions` are `false`: `credential-use`, `deployment`,
`external-policy-change`, `lifecycle-transition`, `maintenance-mutation`, `network`,
`publication`, `release`, `root-evaluator-upgrade`, `tag`.

**Privacy.** Each retained report's bytes are canonical under the independent oracle, carry
zero CR bytes, and contain no occurrence of the host user name, the work directory path in
either separator form, or any absolute path outside the declared views.

## 8. The refusal, provoked four ways

`VER-REB-007` requires that a wrong configuration be refused rather than reported green.
Four independent provocations, in increasing fidelity to the reported defect:

1. **Mutate only `versions.successor`** in the lane's scenario to `0.7.1`, re-emitted
   canonically so no formatting guard could fire first. Refused: `MIG176: successor runtime
   expectation version differs`. The scenario's own `runtime_expectations` still said
   `0.7.0`, so the inconsistency was caught at contract load, before any runtime ran.
2. **Mutate `versions.successor` and `runtime_expectations.successor.version` together.**
   Refused: `MIG156: both proposals must target the declared successor version` — the
   embedded decision fixtures name the successor too. The declared successor version occurs
   six times in the fixture text and is guarded at three separate layers before the runtime
   comparison is reached at all. No output directory was created for either mutation.
3. **Give the repaired scenario a successor interpreter that reports the wrong version** by
   passing the `0.6.0` environment as `--successor-python`. Refused earlier, by `MIG223:
   predecessor and successor interpreters must be distinct`.
4. **The reported CI defect itself, with no tracked byte edited.** The lane's former
   scenario `historical-0.5.0-to-0.6.0.json`, a genuine public `0.5.0` predecessor matching
   its declaration, and the `0.7.0` successor built from this commit. Refused:
   **`MIG211: successor version differs from the scenario`** — the exact diagnostic and the
   exact shape that turned the lane red when `0.7.0` was bumped, reproduced here from real
   released distributions.

Two further readings bound what `MIG211` says. Running the historical scenario with the
`0.6.0` predecessor produced `MIG211: predecessor version differs from the scenario`: the
code is role-parameterized and names whichever role disagrees first, so a `MIG211` line must
be read for its role and not treated as a successor finding. Running the synthetic
`41.2.0 -> 42.0.0` pair against this commit's runtime produced the same code for the same
reason, which is exactly why that fixture cannot be the lane's scenario.

After each provocation the fixture was restored and re-hashed to `0b21462c…`, and porcelain
was empty.

**Corrected succession, on the same runtimes.** The historical pair rehearsed with a matching
`0.6.0` successor passes end to end: `overall_result pass`, `first_failed_stage None`,
`outcome migration-required`, all nine operations affected, six missing capabilities
(`evaluator-evidence-v1`, `predecessor-compatible-assessment-view`,
`predecessor-compatible-preparation-view`, `predecessor-compatible-publication-view`,
`rejected-record-terminal-state`, `separate-root-adoption`), `semantic_sha256
76b36a31c8c43a3704bfa44413bcfd63860bd7d8e6fab4c875d7dd373297ba05`, runtimes `0.5.0 -> 0.6.0`.

This is a load-bearing result for the owner's decision 4. The implementation evidence
disclosed that `compatible` with an empty affected-operation set is a weaker gate than the
historical pair's `migration-required`, and that the stronger coverage now lives only in the
unit suite. That disclosure is confirmed here by running the historical pair against **real
released wheels**, which the unit suite does not do — see section 9. The stronger
classification is real, it still holds, and it is now measured outside the suite that asserts
it.

## 9. What the rehearsal does not establish

These are properties of the migration protocol as specified, not defects introduced by
`WO-REB-023`. They bound what an assurance decision may conclude from a green
`governance-migration` gate, and they were found by reading the implementation rather than by
trusting its summary.

- **Released predecessor code does not execute the stages.** The predecessor interpreter is
  consulted exactly once, for `RUNTIME_PROBE`, an identity report of eleven fields — version,
  isolation, archive identity, module origin, prefix, import search paths, user-site. Every
  stage's adapter logic then runs in the caller's own process, from the tree under test; all
  six contract adapters declare that tree's module digest (section 4). A green rehearsal
  therefore establishes that *the candidate's model of* the predecessor-compatible views
  behaves as the scenario declares, together with the predecessor's installed identity. It
  does not establish that released `0.6.0` behaves that way.
- **The unit suite's runtimes are stubs, not distributions.** `_create_runtime` builds a
  pip-less `venv` and creates an empty `se_harness` package in its purelib; `_versions` then
  writes a one-line `__init__.py` carrying the version the scenario declares, plus a small
  `evaluator_identity` stub for known predecessors. Because the test forces the reported
  version to match the declared one, the suite structurally cannot exercise the divergence
  the lane exists to catch — which is why the coupling assertions
  `WO-REB-023` added compare workflow text and `pyproject.toml` instead, and why section 8's
  provocations were run against real installs.
- **The synthetic future pair can only ever be exercised with stubs.** `41.2.0 -> 42.0.0`
  names no released distribution, so `VER-REB-007`'s requirement of "one synthetic future
  N-1-to-N scenario" is met by `test_synthetic_rehearsal_is_complete_disposable_private_and_deterministic`
  under stub runtimes, on every platform including CI. No hosted lane rehearses it against
  installed packages, and none can.
- **The stage failure matrix is stub-only and test-private.** `_fault_stage` is a private
  keyword on `run_governance_migration`, not a CLI option, so
  `test_every_stage_fails_closed_and_later_stages_do_not_run` — nine subtests, each asserting
  the faulted stage fails, all later stages read `not-run`, and
  `operational_state.unchanged` holds — is the only exercise of that matrix. It could not be
  reproduced here against real distributions.
- **`semantic_sha256` is commit-dependent.** It normalizes host and build facts but retains
  `operational_state`, which includes `git_head`. The figure measured here,
  `f95be1a78223…`, differs from the implementation's `5b36c2dc…` and from both hosted
  figures for that reason alone. It is a determinism check between replays at one commit,
  never a fixed expectation. This is now measured from three independent commits.
- **Every local figure here is single-platform**, one Windows workstation, CPython 3.11.9 for
  the rehearsals. Cross-platform agreement rests on the hosted readings the implementation
  evidence records, which were taken on an ephemeral pull-request merge commit and cannot be
  reproduced at any commit that exists on `main`.

## 10. Departures from `VER-REB-007`, disclosed not softened

1. **The four Manual assessments do not exist.** `VER-REB-007` requires manual assessment by
   the product and requirements owners, the technical and security owners, the assurance
   owner, and the release owner. No such judgment has been recorded for this change. This
   record cannot create them and does not claim them. It is the same shape as the gap
   `VREC-TCM-002` discloses for `VER-TCM-001`, and it means `WO-REB-023` cannot cleanly
   conform to its verification contract on evidence alone.
2. **The evidence-retention key differs from the contract's.** `VER-REB-007`'s
   Evidence-retention clause says to retain under the `WO-REB-018` key. The engineering owner
   decided on 2026-08-26 to retain this reading under `WO-REB-023` instead, on the ground
   that the evidence describes `WO-REB-023`'s candidate. This file therefore sits at
   `evidence/WO-REB-023-verification.md`, which is a knowing departure from the contract's
   text rather than an oversight, and the contract was not edited to match.
3. **The "complete positive rehearsal" row is only partly satisfiable in the lane.** That row
   requires "Exact historical 0.5.0-to-0.6.0-style scenario and one synthetic future
   N-1-to-N scenario". Owner decision 4 removed the historical pair from the hosted lane, and
   the synthetic pair was never in it. The lane now rehearses the candidate pair only. Both
   named scenarios remain in the unit suite, and section 8 rehearses the historical one
   against real releases here; neither fact makes the hosted lane cover the row as written.
4. **Verification was performed by the implementation actor.** The independence measures in
   section 2 are real but they are not a second person. `VER-REB-007`'s Independence section
   is satisfied in its specific prohibitions — no accepted diagnostic was defined here, no
   stage omitted, no mutation judged harmless, no candidate result treated as human
   authority — and unsatisfied in its spirit.
5. **The candidate commit is not the work order's implementing commit.** It is a fresh commit
   off `main` carrying this file, for the reason in section 1. Its pull request must be
   merged as a **true merge**: a squash or a rebase orphans the bound commit, and a bound
   commit cannot afterwards be re-pointed — the record would have to be superseded and
   re-measured in full.

## 11. Governing gates at this commit

Measured with the released exact public `0.6.0` evaluator installed **outside** this
checkout and invoked in isolated mode, which is the only configuration that yields a
governing verdict:

- `validate`: `Engineering artifact validation: PASS` — 890 artifacts, 0 errors, 50 warnings,
  all `[maintenance]` and all pre-existing (`W013` canonical-location, `W014` legacy
  architecture without `decision_assessment`, `W015` deprecated `constrains` relation).
- `doctor`: 87 `PASS`, 0 `FAIL`.
- `preflight --work-order WO-REB-023 --phase review`: `Harness preflight: PASS`.
- Full suite, `python -m unittest discover -s tests -p "test_*.py"`: `Ran 1021 tests`,
  `OK (skipped=24)` on CPython 3.11.9 and `OK (skipped=23)` on CPython 3.14.6. The skip
  difference is the standing Windows-only guard set, not a coverage change.
- `tests.test_governance_migration`: 16 tests `OK`.
  `tests.test_standard_repository_lifecycle`: 23 tests `OK`.

Adding this file changes no artifact and no test. The figures above were taken over `main`'s
merge commit before this file was written, so no figure here describes a tree that does not
exist; the record commit above the candidate adds one artifact and its evaluator sidecar,
which moves the artifact count and the snapshot digest and is expected to.

## 12. Actions not performed

No lifecycle transition was taken here. `WO-REB-023` was already `implemented` before this
reading and is untouched. No promotable distribution was built — the `0.7.0` wheel measured
in section 6 is ephemeral, non-promotable, bound by nothing, and was discarded. No release
record was prepared, no tag created or moved, nothing published to GitHub or PyPI, no Pages
deployment, no maintenance-line mutation, no credential used, no external policy changed, and
the root evaluator remains the pinned released `0.6.0`. `VREC-SEH-013` and `RLS-SEH-013`
remain unprepared. The assurance decision on the record this evidence supports belongs to an
accountable assurance owner and has not been taken.

## 13. Next accountable action

An accountable assurance owner reviews this evidence and either transitions the resulting
`ready` verification record to `verified` or rejects it. Section 10 lists what they are being
asked to accept: four owner assessments that do not exist, a retention key that departs from
the contract, a hosted lane that covers one of the two scenarios the contract names, and a
verification performed by the implementation actor. Whether those are acceptable for a
`0.7.0` release is their judgment, not this file's.
