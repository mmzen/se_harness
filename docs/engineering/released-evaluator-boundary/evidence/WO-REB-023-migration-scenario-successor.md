# WO-REB-023 Migration Scenario Successor Evidence

Date: 2026-08-26

Authority: non-authoritative retained implementation evidence. This file does not approve an artifact, authorize a diff, verify work, merge, release, publish, tag, or deploy. It records what was measured, on which runtimes, at which commit, and what the measurements do not cover. Commit-bound assurance for this work order is `required` and remains a separate `VREC` decision; this file is not that decision.

Retention under this work order's own key is the engineering owner's reading of `VER-REB-007`, taken at approval on 2026-08-25 when the alternative — a standalone verification packet — was put to them with its cost. It is a decision, not an oversight: the reading is that a scenario replacement inside an existing rehearsal contract is a routine exercise of `VER-REB-007` rather than a new verification obligation.

artifact: WO-REB-023
checkpoint: handoff
formal_snapshot_sha256: dc45e80da7da7f35b4dc23e19553abee4192a9dc1843b92b272d365a899aff85

## 1. Governing packet, preflight, and the owner decisions

`WO-REB-023` implements the already approved `REQ-REB-016` and `REQ-REB-017` under `SPEC-REB-008`, `ARCH-REB-007`, `ADR-REB-007` and `VER-REB-007`. It adds no requirement and no packet artifact, and amends none of those six.

Four decisions were taken by the engineering owner at approval on 2026-08-25, each put with its measured cost:

1. Approve `WO-REB-023`, push the branch, and open a pull request.
2. **Route A** — a version-truthful `compatible` scenario, rather than a fabricated capability gap or a new contract version.
3. Retain the evidence under this work order's own key, as a routine reading of `VER-REB-007`.
4. Drop the historical pair from the lane; the unit suite keeps exercising it.

A fifth was taken on 2026-08-26 and is recorded in section 11: a bounded `[execution_scope]` amendment adding `tests/test_standard_repository_lifecycle.py`.

Governing preflight at the implementation tree, with the released exact public `0.6.0` evaluator from outside the checkout in isolated mode:

```text
Harness preflight: PASS
Work order: WO-REB-023 (in_progress)
```

## 2. The defect as measured

`SE Harness Candidate Evidence` run `32886901131`, event `push`, branch `chore/wo-rls-011-0-7-0-qualification`, head `6fdb23a0911b0e9c0185d73ca55ea74b228398d7`, **failed**:

| Job | Id | Conclusion |
|---|---|---|
| Candidate source evidence | `97929364771` | success |
| Candidate package evidence | `97929972663` | success |
| Governance migration (Windows) | `97930154875` | **failure** |
| Governance migration (Linux) | `97930154913` | **failure** |
| Build deterministic integration package | `97930458774` | skipped |
| Reconcile governance migration platforms | `97930458842` | skipped |
| Verify integration package | `97930459343` | skipped |
| Retain verified integration package | `97930460668` | skipped |

Both migration jobs failed at *Rehearse the exact predecessor-to-successor handover twice* with `harnessctl: MIG211: successor version differs from the scenario`. The failure is at the **first** rehearsal, so the double-replay `semantic_sha256` comparison never ran and four downstream jobs, including the deterministic integration package and its verification, never started.

The cause is exact: the lane ran `historical-0.5.0-to-0.6.0.json`, whose `versions` object is `{"predecessor": "0.5.0", "successor": "0.6.0"}`, against a successor built from `GITHUB_SHA` on a branch whose `pyproject.toml` declares `0.7.0`. `_verify_runtime_identity` refuses that, which is `SPEC-REB-008` rule 4 working as specified. **The refusal is correct; the configuration was wrong.**

## 3. Route A, and exactly what it gives up

The scenario declares `compatible` with an empty missing-capability set and an empty affected-operation set, because that is what the vocabulary can express truthfully: released `0.6.0` genuinely holds all eight capability names the packaged contract declares. A real capability gap does exist — released `0.6.0` exposes no `qualify` — but the closed vocabulary cannot name it, and naming it would require a new contract version, which the owner rejected for this work order.

The `candidate-` prefix is deliberate. It is not `historical-`, because the pair has no historical boundary to preserve, and not `synthetic-`, because both runtimes are real. That prefix costs two guards, and both are replaced by assertions rather than left uncovered:

| Guard given up | Why | Compensating assertion |
|---|---|---|
| `MIG404` on a `candidate-` prefix withdrawing the boundary guard | the prefix is not `historical-` | `test_candidate_prefix_is_what_withdraws_the_boundary_guard` proves the withdrawal is what the prefix does, by measuring `overall_result` `fail` at `first_failed_stage` `validate-complete` with `MIG404` in the diagnostic |
| `MIG179`, the archive pin a `historical-` scenario forces | ditto | the workflow keeps `PREDECESSOR_WHEEL_SHA256` anyway, and `test_lane_predecessor_pin_matches_the_public_archive` compares the lane's two `env` values against the scenario and against the measured public archive |
| the `compatible` outcome could silently drift | route A's premise | `test_candidate_pair_classifies_compatible_over_the_whole_vocabulary` compares the scenario's predecessor capability list against the contract's whole vocabulary |

## 4. The scenario fixture

Generated with the repository's own canonical writer, not hand-authored.

| Fact | Value |
|---|---|
| Path | `tests/fixtures/governance_migration/candidate-0.6.0-to-0.7.0.json` |
| Bytes | 3862, UTF-8, LF, 0 CR bytes |
| Blob and worktree SHA-256 | `0b21462cc4e73055b4b701b76392091c4988b65e38860975e3c2f2d7c0d73b4a` |
| Rehearsal's own `fixture_sha256` | `e5c79724f5616db220389fa91b8670e4273701addfb4914b4dda95144ed62f93` |
| Stages | the closed nine-stage catalog in order, `prepare` → `adopt` |
| Re-canonicalization | `raw == canonical_json(scenario)` is asserted for every fixture in the directory, and the directory glob is compared against the enumerated list so a new fixture cannot escape the assertions |

## 5. Changed-path manifest, and the two `check` readings

Five paths from the branch's base, plus the two the scope amendment authorizes:

```text
.github/workflows/candidate-evidence.yml
docs/engineering/released-evaluator-boundary/README.md
docs/engineering/released-evaluator-boundary/work-orders/WO-REB-023.md
tests/fixtures/governance_migration/candidate-0.6.0-to-0.7.0.json
tests/test_governance_migration.py
tests/test_standard_repository_lifecycle.py
docs/engineering/released-evaluator-boundary/evidence/WO-REB-023-migration-scenario-successor.md
```

Before the amendment, `check` refused the sixth path and named it:

```text
QGP-G4I-PATHS: WEX201: changed path is outside execution scope: tests/test_standard_repository_lifecycle.py
```

`preflight` passed on the same tree, which is why the refusal is the enforcing reading and not a second opinion. After the amendment, the same command with all seven paths reports no path diagnostic. Both readings came from the released `0.6.0` evaluator outside the checkout.

The workflow diff is four lines in one job: `PREDECESSOR_VERSION` `0.5.0` → `0.6.0`, `PREDECESSOR_WHEEL_SHA256` `974ba2de…` → `2a952eb6…`, and the scenario path. No job, matrix dimension, permission, trigger or step was added or removed.

## 6. Qualification at the candidate commit

Measured at `4052143570d3bafc12447292e371f5e3066979dc`, in a checkout detached at that commit, on CPython 3.11.9 — the version the lane pins. The tree carries the `0.7.0` bump through the stacked merge described in section 12, so this is the real configuration the lane will run, not an approximation.

| Fact | Value |
|---|---|
| `pyproject.toml` / `se_harness.__version__` | `0.7.0` / `0.7.0` |
| Predecessor runtime | `0.6.0`, installed from the already-public wheel, SHA-256 `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7` |
| Successor runtime | `0.7.0`, built from `git archive HEAD` into an **explicitly non-promotable** ephemeral wheel outside the checkout, SHA-256 `39b131563638c8ed08a2a791f3536d69d3abb65470c19038d04fe625c89a5d84` |
| Both runtimes | isolated virtual environments outside the checkout, invoked with `-I` |

Two consecutive rehearsals, both `overall_result` `pass`, `first_failed_stage` `None`:

| Field | Run 1 | Run 2 |
|---|---|---|
| `semantic_sha256` | `5b36c2dcfd84914277ed944498a577d4f763478d23b95794eb544bf7f98dd999` | identical |
| `classification` | `{"affected_operations": [], "missing_capabilities": [], "outcome": "compatible"}` | identical |
| Stages | 9, every one `pass` | identical |
| `validate-complete` | `outcome` `valid`, `codes` `[]` | identical |
| `assess` | `predecessor_complete_graph: pass` | identical |
| `operational_state.unchanged` | `true`, `git_head` `4052143570d3…`, `source_sha256` `a7e73c17…` equal before and after | identical |

The double-replay digest comparison — the thing `MIG211` prevented from ever running — passes.

**The `semantic_sha256` is not a cross-commit constant.** `operational_state` includes `git_head` and `git_refs_sha256`, so the same scenario over the same runtimes gave `02dd3ef721d7…` in the pre-amendment merge preview and `5b36c2dc…` here. It is a determinism check between replays at one commit, and quoting it as a fixed expectation would be wrong.

## 7. The coupling assertions, demonstrated red

The point of this work order is that the next bump breaks a local test rather than a hosted gate. That was measured by repointing the workflow at the historical pair on this same tree and running the two assertions, then restoring the file:

| Test | With the candidate scenario | With the historical pair |
|---|---|---|
| `test_lane_scenario_declares_the_version_the_candidate_builds` | pass | **FAILED (failures=1)** |
| `test_candidate_evidence_is_repository_owned_and_non_authoritative` | pass | **FAILED (failures=1)** |

`git status --porcelain=v1 --untracked-files=all` was empty after the restore. The second row is the amended assertion from section 11 doing its job: it now fails if the historical scenario name comes back, so the owner's decision 4 has to be reversed on purpose rather than by accident.

## 8. Non-change proofs

| Claim | How it was proven |
|---|---|
| `historical-0.5.0-to-0.6.0.json` is byte-identical | its blob at `HEAD` and at `origin/main` both hash to `393f639eb06fdec17a31386c5fc94f526cceba2e0efc95cbde6e1077f99b8324` |
| It is still exercised end to end | `test_historical_pair_left_the_lane_and_is_still_exercised_here` rehearses it and asserts `pass` with classification `migration-required` |
| `synthetic-n-minus-1-to-n.json` untouched | `af2101d95784babdd3afaaccad16946ba04abbce866643c7e6cb4413ecb33daf` |
| The runner and contract are untouched | `se_harness/governance_migration.py`, `governance_migration_contract.py` and `governance_migration_contract.json` are absent from the branch diff |
| The rehearsal mutates nothing | `git diff --exit-code` clean and `git status --porcelain=v1 --untracked-files=all` empty after both runs |
| The byte-rule guard covers the new fixture without an edit | `tests.test_hash_bound_integrity`: 102 tests, `OK (skipped=1)`, with no change to that module. Its inventory is the declared patterns, and `tests/fixtures/governance_migration/*.json` is one, so a new file matching an existing pattern is covered — confirmed by running it, not by reading it |

## 9. Gate results at the candidate

Governing verdicts from the released exact public `0.6.0` evaluator, run from outside the checkout in isolated mode. The in-tree CLI is refused for mutations by guard `MG005` on runtime identity, so nothing here relies on it.

| Gate | Result |
|---|---|
| Governing `validate` | 889 artifacts, 0 errors, 50 warnings, all `maintenance` |
| Candidate `scripts/validate_engineering_artifacts.py --root .` | the same 889 / 0 / 50 |
| `python scripts/validate_release_distributions.py --root .` | `PASS (1 distribution-bearing record)` |
| Governing `doctor` | 87 PASS, 0 FAIL |
| Governing `preflight --work-order WO-REB-023 --phase review` | PASS |
| Full suite, CPython 3.11.9 | `Ran 1021 tests`, `OK (skipped=24)` |
| `tests.test_governance_migration` | `Ran 16 tests`, `OK` |

Before the amendment the same suite reported 1021 tests with exactly one failure, `test_candidate_evidence_is_repository_owned_and_non_authoritative`, and no other. The five new tests are the difference between 1016 and 1021.

## 10. The formal snapshot, and its checkout convention

`formal_snapshot_digest` hashes worktree bytes, so the figure depends on how the checkout was made. Both readings were taken at `4052143` with the released `0.6.0` evaluator's own `se_harness.workflow._validation` and `se_harness.workflow_compliance.formal_snapshot_digest` — the exact pair `check` calls — and both report 889 artifacts and 0 errors:

| Checkout | `WO-REB-023.md` CR bytes | Digest |
|---|---|---|
| this working checkout, `core.autocrlf=true` | 513 | `dc45e80da7da7f35b4dc23e19553abee4192a9dc1843b92b272d365a899aff85` |
| `git -c core.autocrlf=false worktree add --detach 4052143` (what a Linux lane reads) | 0 | `81cb0c8b513a5e65a098257f0fa6851156130cebe0f580b2764980340b5ad6f5` |

The block at the head of this file binds the first, because that is the value `check` itself returned on the tree where the handoff was evaluated. A reader recomputing it in an LF checkout will get the second; that is the convention, not a discrepancy.

## 11. The scope amendment of 2026-08-26

Owner decision 4 removed the `0.5.0` predecessor wheel digest from the workflow, and `test_candidate_evidence_is_repository_owned_and_non_authoritative` asserted that digest was present in the workflow text. So the decision turned that test red by construction — a correct assertion about a lane the owner then changed. The file sat outside the six declared execution-scope paths, `check` refused it as `QGP-G4I-PATHS: WEX201`, and a scope amendment is an owner decision, so it was measured, put, and decided rather than taken locally.

The amendment authorized exactly one edit: replacing that one stale assertion with `PREDECESSOR_VERSION: "0.6.0"`, the `candidate-0.6.0-to-0.7.0.json` scenario name, and two negative assertions — that neither the `0.5.0` digest nor the `historical-` scenario name is present. Nothing else in that file changed, and the `0.6.0` predecessor wheel digest it already asserted was left where it was.

Two consequences a reviewer should hold:

- **The pre-amendment snapshot is stale.** `02c04f26f31c25b8bd9eb931a3e9e8c0a48838fbe5018efc5f39ec301fb68bd0` described a tree that no longer exists and must not be quoted. Section 10 is the live pair.
- **The amendment is recorded in the work order as a dated section**, with the six-path list it replaced, rather than by silently editing the array. `updated` moved to `2026-08-26`.

## 12. The stacked merge and the merge order

The route-A scenario declares successor `0.7.0`, and the lane builds its successor from `GITHUB_SHA`. The scenario and `pyproject.toml` are therefore one fact measured twice, and this repair is only complete in a tree that also carries the bump. That tree is `WO-RLS-011`'s, and relaxing the comparison to make a `0.6.0` tree green is what `SPEC-REB-008` rule 15 forbids.

The owner decided the order on 2026-08-26: open the bump's pull request first and stack this one on it. Accordingly this branch merged `origin/chore/wo-rls-011-0-7-0-qualification` at `5963fed`, **with no conflict and no hand-resolved line**, and this pull request's base is that branch rather than `main`. Every figure in this file was measured after that merge, at `4052143`.

The consequence for a reviewer: if the bump's pull request is closed or rebased instead of merged first, this branch's base disappears and the lane goes red again on the same `MIG211`. The two land together, in that order, or neither does.

## 13. Coverage gaps and residual risks

1. **No hosted reading of the repaired lane exists yet.** Every figure here is local, on one Windows 11 workstation, on CPython 3.11.9 and 3.14.6. The hosted `governance-migration` job runs on `windows-latest` and `ubuntu-latest`, and neither has executed the new scenario. The first hosted reading will be this pull request's own run, and it is not in evidence.
2. **The successor wheel measured here is not the wheel CI builds.** It is an ephemeral non-promotable wheel built from `git archive HEAD` on this workstation. Its digest `39b13156…` is recorded for traceability, not as an expectation; the deterministic-build comparison that would make a wheel digest meaningful is a different lane.
3. **The real capability gap is unnamed.** Released `0.6.0` exposes no `qualify`, and the closed contract vocabulary cannot say so. The scenario is truthful about what it declares and silent about that gap. Naming it needs a new contract version, which `SPEC-REB-008` reserves for accountable review.
4. **`compatible` with an empty affected-operation set is a weaker gate than `migration-required`.** The historical pair's `migration-required` classification exercised more of the runner. That coverage now lives only in the unit suite, which is precisely what decision 4 traded away, and `test_historical_pair_left_the_lane_and_is_still_exercised_here` is what keeps it honest.
5. **No Linux figure is local**, and no local run used the hosted runner images.
6. **The `semantic_sha256` moves with the commit** (section 6). Any future evidence quoting it must name the commit it was measured at.
7. **The missing release-sequence step is not fixed here.** `docs/notes/developing-se-harness.md#release-sequences` still does not list "add a migration scenario for the new version" as a bump step, which is why this gap reached CI. That file is ungoverned under `AGENTS.md` and belongs to a separate pull request with no work-order trailer; this work order must not smuggle it in.

## 14. Actions not performed

No promotable distribution was built. No verification record, release record, tag, GitHub Release, PyPI publication, Pages deployment, protected-environment approval, maintenance-line change, credential use, or root-evaluator change. The root evaluator stays pinned at the released `0.6.0`.

No governing artifact was amended: `REQ-REB-016`, `REQ-REB-017`, `SPEC-REB-008`, `ARCH-REB-007`, `ADR-REB-007` and `VER-REB-007` are untouched. No contract version was added. No existing scenario, no migration runner module, and no managed file was edited. No assertion was relaxed to turn a red reading green, and no `historical-` fixture byte moved.

No pull request was merged. The lifecycle transition out of `in_progress` is the owner's separate act and has not been taken.
