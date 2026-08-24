# WO-RLO-005 implementation evidence

## Authority and scope

On 2026-08-24 the accountable repository owner stated `OK go for #111` and, in the same turn, selected `Parallel lane + drift check` over refactoring the release orchestrator and `Fourth release-orchestration packet` as the governance home under the existing `INT-RLO-001`. That statement approved the complete `RLO-005` definition packet and authorized `WO-RLO-005`.

This document assesses the implementation as committed on the branch. It is retained engineering evidence. It is not a commit-bound `VREC`, an assurance decision, a release decision, a branch operation, a publication, a deployment, or an external configuration change. Neither is a rehearsal result: every rehearsal output quoted here carries the field `authority = "derived operational evidence; no formal lifecycle transition"`.

Issue [#111](https://github.com/mmzen/se_harness/issues/111) records `RC-060-11` from the immutable `0.6.0` release-recovery analysis, together with incidents `I-15` (Git Bash path conversion) and `I-16` (a Windows 8.3 short-name alias for the temporary directory). Both surfaced during a live release because the orchestrator's credential-free work is split so that `resolve` runs only on `ubuntu-latest` and `qualify` only on `windows-2022`.

## Candidate under measurement

| Fact | Value |
|---|---|
| Candidate commit | `cfca2f350bd9aede69c336605d2b68fc50ffc29c` |
| Branch | `feat/rlo-004-publication-rehearsal` |
| Merge base | `1431df591a654202ab1a3a6647d9657905bbd26c` (merge of pull request #132) |
| Diff against merge base | 20 files changed, 6227 insertions, 0 deletions |
| Worktree state | clean at `cfca2f3`; the later changes are this document with the `WO-RLO-005` transition, committed together, and then the owner's amendment and exclusion rulings recorded in the artifacts |
| Local interpreter | CPython 3.14.6 on Windows 11 |
| Orchestrator and lane interpreter | pinned 3.11 |

Every measurement in the tables below was taken at `cfca2f3`. The failing shakedown runs quoted under *Two defects the end-to-end run found* were taken at earlier, amended predecessors of this commit and are labelled as history rather than as results.

## Changed surfaces

Executable, repository-owned:

- `.github/scripts/rehearse_publication.py` — 2754 lines, standard library only, two subcommands `rehearse` and `check-divergence`.
- `.github/scripts/publication_rehearsal_mechanics.json` — data only: 22 mechanics, 9 declared orchestrator steps, 17 trivia commands, 4 infrastructure actions, 4 external-state actions, required platforms `Linux` and `Windows`.
- `.github/workflows/publication-rehearsal.yml` — `contents: read` at workflow and job level, no environment, no secret, no token; triggers `pull_request`, `push` to `main`, and `workflow_dispatch` with one optional `release_record` input.
- `tests/test_publication_rehearsal.py` — 101 tests, and four fixtures under `tests/fixtures/publication_rehearsal/`.

Formal artifacts: `CAP-RLO-003`, `REQ-RLO-015`, `REQ-RLO-016`, `SPEC-RLO-005`, `ARCH-RLO-005`, `ADR-RLO-005`, `VER-RLO-005`, `WO-RLO-005`, the acceptance feature, and the release-orchestration domain index. Repository-owned prose: `docs/notes/release-publication-rehearsal.md` and one row in `docs/notes/README.md`.

## The release orchestrator is byte-unchanged

`REQ-RLO-015` and `WO-RLO-005` both require `.github/workflows/publish-pypi.yml` to be byte-identical to its merge-base content. Proven three independent ways:

| Proof | Result |
|---|---|
| `git diff --stat 1431df5 HEAD -- .github/workflows/publish-pypi.yml` | empty |
| Path absent from `git diff --name-only 1431df5 HEAD` | confirmed |
| SHA-256 over LF-normalized bytes: worktree file, `HEAD` blob, `1431df5` blob | `d7313d16db7f013e4f8b961840eb60af31c27633a1366f95362e5befab9d51a2`, 34896 bytes, all three identical |

The third proof normalizes line endings because this checkout has `core.autocrlf=true`, so the worktree file and the blob differ in bytes as stored while being the same content. The repository test `test_the_release_orchestrator_is_byte_unchanged` asserts the same property in the suite.

The figures in this section are the pre-merge measurement and are kept as measured. `main` later changed the orchestrator itself, so the merge-base form of the proof no longer holds and the claim narrows to byte-unchanged *by this packet*; the section “The orchestrator is still byte-unchanged by this packet” below records the re-derived digest and why.

## Mechanic inventory and per-platform outcomes

Two complete local rehearsals were run, both on Windows, at the candidate commit. They differ only in the inherited `core.autocrlf` setting, which the candidate checkout inherits because the rehearsal creates it with `git worktree add` exactly as the orchestrator does.

The `realized_by` column reproduces the declaration verbatim; it is a closed vocabulary and a mechanic naming anything outside it is refused before any comparison runs.

| # | Mechanic | `realized_by` | `core.autocrlf=false` | `core.autocrlf=true` |
|---|---|---|---|---|
| 1 | `temporary-path-identity` | `platform-toolchain` | executed | executed |
| 2 | `release-record-format-validation` | `shell-composition` | executed | executed |
| 3 | `evaluator-resolution` | `repository-program` | executed | executed |
| 4 | `evaluator-acquisition-and-hash-proof` | `platform-toolchain` | executed | executed |
| 5 | `evaluator-identity-proof` | `released-evaluator` | executed | executed |
| 6 | `predecessor-view-qualification` | `candidate-cli` | **excluded** | **excluded** |
| 7 | `distribution-policy-validation` | `repository-program` | executed | executed |
| 8 | `plan-resolution` | `repository-program` | executed | executed |
| 9 | `resolution-refusal-document` | `platform-toolchain` | executed | executed |
| 10 | `candidate-export` | `platform-toolchain` | executed | executed |
| 11 | `pinned-build-tool-installation` | `platform-toolchain` | executed | executed |
| 12 | `complete-candidate-qualification` | `candidate-cli` | executed | executed |
| 13 | `candidate-unit-suite` | `candidate-cli` | executed — 753 tests passed | **failed** — 4 byte-exact assertions |
| 14 | `cli-smoke-check` | `candidate-cli` | executed | executed |
| 15 | `deterministic-build` | `platform-toolchain` | executed | executed |
| 16 | `sdist-normalization` | `repository-program` | executed | executed |
| 17 | `build-determinism-comparison` | `platform-toolchain` | executed — byte-identical | executed — byte-identical |
| 18 | `bundle-assembly` | `shell-composition` | executed | executed |
| 19 | `bundle-manifest-creation` | `repository-program` | executed | executed |
| 20 | `build-manifest-verification` | `repository-program` | executed | executed |
| 21 | `bundle-verification` | `repository-program` | executed | executed |
| 22 | `teardown` | `rehearsal-program` | executed — 6209 paths | executed — 6209 paths |

The complete per-mechanic result of both runs is reproduced in this table and in the reason text quoted below; the machine-readable `se-harness-publication-rehearsal-result/v1` documents, each with its 26-entry command transcript, are retained outside the repository, because `WO-RLO-005`'s execution scope declares no path for them and a rehearsal result carries no formal authority that would justify committing one.

Overall state: `rehearsed`, exit 0 with `core.autocrlf=false`; `failed`, exit 1 with `core.autocrlf=true`. `unreported_mechanics` is empty in both, so no mechanic was silently skipped. Both runs report `verification_compares_against_authorized_release_identity = false` and `verification_plan_source = derivation-from-the-first-distribution-set`, because candidate mode derives its plan from its own first build rather than from an authorized release identity.

The `core.autocrlf=false` run was measured in a throwaway clone at the same commit, since removed; the `core.autocrlf=true` run was measured in the working checkout. Both report `source_date_epoch = 1787580552` and both tore down 6209 derived paths, so the epoch and the derived-tree shape are reproducible across the two.

### The four `core.autocrlf=true` failures

`test_contract_rejects_duplicate_and_unknown_fields` and `test_manifest_normalizes_line_endings_and_detects_content_changes` (`tests/test_agentic_execution.py`), `test_declaration_is_data_only` (`tests/test_hash_bound_integrity.py`), and `test_non_promotable_ephemeral_wheel_carries_and_fresh_installs_one_skill_core` (`tests/test_release_build.py`). The rehearsal names all four in its own failure text: `candidate unit suite exited 1 with 4 failing tests: …`.

There were four at this commit. `main` later added six more byte-exact assertions, so the same condition now reports ten; the section “Re-measured after the merge” below names them and the control that proves they are inherited. None of the four is in `tests/test_publication_rehearsal.py`; all four assert on exact bytes and all four are green at the same commit in the `core.autocrlf=false` clone. They are a property of the inherited checkout, not of this work order and not of the publication path. That is why `REQ-RLO-015` was amended to report `line_ending_conversion` on the result and why the human summary states `Inherited checkout: core.autocrlf=true, so the candidate checkout converts line endings`.

## Measured versus injected platform coverage

`WO-RLO-005` constrains the implementer to one directly executable platform and requires the other to be reported as injected rather than claimed as measured.

| Coverage | Status |
|---|---|
| Windows runner family, all 22 mechanics, end to end, twice | **measured** on this machine |
| POSIX `bin/python` and `bin/harnessctl` layout | **derived, not measured** — `venv_scripts_directory` asks `sysconfig` for the platform scheme; `test_source_hardcodes_neither_layout_name` asserts the source contains neither `"Scripts"` nor `/ "bin"` as a literal |
| `ubuntu-latest` → `Linux` runner-label mapping | **injected** — `test_runner_labels_map_to_families_and_refuse_the_unknown` |
| Linux job classification, declared platform claims, lane platform set | **injected** through the four fixtures under `tests/fixtures/publication_rehearsal/` |
| Link teardown | **measured in the Windows link shape** — symlink creation is privileged on Windows, so `try_directory_symlink` falls back to a junction, which is the link shape a virtual environment or build tool actually leaves there; the POSIX symlink shape is exercised by the same tests only on Linux, so it is not measured here |
| Real `ubuntu-latest` runner-image behavior | **not measured** — first proven by the hosted lane, which is not dispatched under this work order |

The hosted lane has not run. No push or pull request is authorized, so the Linux half of `REQ-RLO-015` is satisfied by design, derivation, and injected state locally, and awaits its first hosted execution. `docs/notes/release-publication-rehearsal.md` states this limitation for human readers, and `VER-RLO-005` carries it as residual uncertainty.

## The excluded mechanic, and why exclusion is not suppression

`predecessor-view-qualification` reports `excluded` in candidate mode with this measured evidence, identical in both runs:

```json
{
  "release_record": "RLS-SEH-012",
  "resolved_evaluator_version": "0.6.0",
  "resolved_evaluator_sha256": "2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7",
  "record_predecessor_evaluator_version": "0.5.0",
  "record_predecessor_evaluator_sha256": "974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f"
}
```

The cause is structural. `publish_dashboard.read_evaluator` ignores `--release-record` when `.engineering-harness.lock` is schema 3 and returns the lock's evaluator, so the orchestrator installs the lock evaluator — here `0.6.0` — while `qualify predecessor-view --release-record X` compares it against `X`'s own predecessor bootstrap contract. Those two agree only while a record is being prepared. Afterwards they differ by exactly one release, because a released record names the evaluator that qualified it and the lock names the evaluator that release advanced to.

The mechanic is therefore excluded with both identities named, not passed and not suppressed:

- `release-record` mode never excludes. `_predecessor_view_exclusion` returns `None` immediately when `self.mode == "release-record"`, so a mismatch there is a defect in the record and fails. `test_release_record_mode_never_excludes` asserts this.
- Candidate mode excludes only on a measured mismatch. If a committed `RLS-*` record ever binds the resolved evaluator as its predecessor, the mechanic runs. `test_a_record_binding_the_resolved_evaluator_is_a_valid_subject` asserts that.
- `test_the_governing_lock_and_the_newest_released_record_disagree_here` measures the real repository and asserts that no released record currently binds the governing evaluator. Its failure message tells a future reader that the expectation, not the code, has gone stale.
- The exclusion is reported in the machine result, in the human summary, and in the acceptance feature scenario *A mechanic with no valid subject is excluded rather than failed*.

## Two defects the end-to-end run found

Both were found by running the rehearsal for real rather than by reading it, and both are fixed in the candidate.

**The teardown post-audit was unsatisfiable.** The audit walked `self.deleted_paths` and rejected any path not contained in the rehearsal root. The root is the last path teardown removes and its parent lies outside the root by construction, so the audit refused its own correct behavior. Two runs failed this way, quoting `teardown deleted a path outside the rehearsal root: C:/Users/mathi/rehearsal-inplace-1`. The fix audits every deleted path by its parent and accepts exactly one exception, the root's own real path compared under `os.path.normcase`, so a link's own target cannot make it look contained. `TeardownAuditTests` covers the root's removal, an outside path, a sibling sharing the root's name prefix, residue the rehearsal did not inherit, and inherited uncommitted entries not read as residue.

**`PV001` was two unrelated causes under one identifier.** The first shakedown, run while the packet was still uncommitted, produced this — recovered from that run's own `se-harness-release-qualification-v1` result before its residue was deleted, and retained outside the repository:

```json
{"id": "PV001", "message": "predecessor preparation requires a clean Git worktree",
 "passed": false, "subject": "predecessor-view"}
```

After the packet was committed the same `PV001` identifier returned with an entirely different message, `evaluator wheel differs from the released RLS contract`. One identifier covering both a dirty worktree and a subject mismatch is why the two were initially conflated. The result now reports the inherited checkout condition next to the outcomes so the first cause is attributable to the checkout, and rule 37 of `SPEC-RLO-005` governs the second.

## Divergence verdicts

| Run | Verdict | Exit |
|---|---|---|
| `check-divergence --repository .` | `EXACT` | 0 |
| `check-divergence --repository . --cross-check-yaml` (PyYAML 6.0.3) | `EXACT` | 0 |

Rehearsed jobs: `qualify`, `resolve`, on `Linux` and `Windows`. Lane platforms: `Linux`, `Windows`. `No uncovered or stale mechanic.` Five of the orchestrator's seven jobs are excluded, each reporting the attribute that excluded it:

```text
- github_release: contents: write permission; step 'Create or verify the immutable annotated tag' env names GH_TOKEN; step 'Stage, verify, and publish the exact GitHub Release' env names GH_TOKEN; step 'Record final GitHub state' env names GH_TOKEN; step 'Create or verify the maintenance line' env names GH_TOKEN
- observe: depends on the excluded job github_release
- pages_build: uses the external-state action actions/configure-pages; uses the external-state action actions/upload-pages-artifact
- pages_deploy: pages: write permission; id-token: write permission; declares a protected environment; uses the external-state action actions/deploy-pages
- pypi: id-token: write permission; declares a protected environment; step 'Download and verify exact final GitHub assets' env names GH_TOKEN; uses the external-state action pypa/gh-action-pypi-publish
```

`observe` is the case that shows classification is fail-closed and transitive: it holds only `contents: read`, but it `needs: github_release`, so it runs after a credential has been used and is excluded on its dependency rather than on a permission of its own.

PyYAML is installed locally and in the lane but is **not** a repository dependency — `pyproject.toml` declares none. `--cross-check-yaml` fails outright when PyYAML is absent rather than falling back silently; the bounded reader is what runs when it is not there.

## Negative-case matrix

Every condition below is exercised by a test that asserts the finding's `kind` against a mutated fixture pair. The `detail` texts quoted are the exact strings the program emits; `<…>` marks a value interpolated at the point of failure.

Divergence findings, `kind | direction | detail`:

| Condition | Finding |
|---|---|
| Credential-free step absent from the declaration | `undeclared_step \| uncovered \| a credential-free orchestrator step is absent from the declaration; its mechanics are not rehearsed` |
| Declared step's script changed at all | `changed_step \| uncovered \| a credential-free orchestrator step changed; its rehearsal coverage must be re-derived and the declaration updated` |
| Credential-free step with a script but no name | `unnamed_step \| uncovered \| a credential-free step with a script has no name to declare` |
| Command matching no declared mechanic and no trivia | `unclassified_command \| uncovered \| a credential-free orchestrator command matches no declared mechanic and is not declared shell trivia` |
| Declared step the orchestrator no longer performs | `stale_step \| stale \| the declaration names a step the orchestrator no longer performs` |
| Declared step of a job no longer rehearsed | `stale_step \| stale \| the declaration names a step of a job that is no longer rehearsed` |
| Declared command the orchestrator no longer invokes | `stale_mechanic \| stale \| the orchestrator no longer invokes this declared command` |
| Declared mechanic of a job no longer rehearsed | `stale_mechanic \| stale \| the declaration names a mechanic of a job that is no longer rehearsed` |
| Declared platform differs from the job's runner | `platform_claim \| stale \| the declared orchestrator platform differs from the job's runner type` |
| Action neither declared infrastructure nor declared external state | `unclassified_action \| uncovered \| a rehearsed job uses an action that is neither declared infrastructure nor a declared external-state action` |
| Action not pinned to a full 40-character commit | `unpinned_action \| uncovered \| a rehearsed job uses an action that is not pinned to a full commit` |
| Rehearsal lane absent | `missing_lane \| uncovered \| the rehearsal lane is absent: <name>` |
| Lane missing a required platform | `missing_platform \| uncovered \| the rehearsal lane does not declare <platforms>` |
| Lane job not `contents: read` only | `lane_permissions \| uncovered \| a rehearsal lane job does not declare contents: read only` |
| Lane job declares an environment | `lane_environment \| uncovered \| a rehearsal lane job declares an environment` |
| Lane job references a credential | `lane_secret \| uncovered \| a rehearsal lane job references a credential: <name>` |
| Lane job uses an external-state action | `lane_external_state \| uncovered \| a rehearsal lane job uses the external-state action <action>` |

Findings are deduplicated by exact content, so a repeated condition reports once (`test_one_finding_is_reported_per_condition`).

Refusals — conditions the program refuses outright rather than reporting as a finding:

| Condition | Refusal |
|---|---|
| Job cannot be classified | `job <name> is not a mapping and cannot be classified`, `job <name> has unclassifiable permissions`, `job <name> declares no step list and cannot be classified` |
| Job needs an unknown job | `job <name> needs an unknown job <dependency>` |
| No credential-free job remains | `no credential-free orchestrator job remains to rehearse` |
| Declaration is not strict JSON data | `mechanic declaration is not strict JSON data: <error>`, `mechanic declaration must be a mapping`, `mechanic declaration must be JSON data: <path>` |
| Declaration repeats a key or a mechanic identifier | `declaration repeats the key <key>`, `mechanic declaration repeats a mechanic identifier` |
| Declaration key is executable-shaped | `declaration key at <path> is executable-shaped: <key>` |
| Declaration value is not data | `declaration value at <path> is not data: <type>` |
| Mechanic claims an undeclared realization surface | `mechanic <id> names an undeclared realization surface: <surface>` |
| Workflow outside the modelled Actions subset | `<file> has no job mapping`, `<file>: job <name> is not a mapping`, unbalanced quote, untokenizable script |
| Bounded reader and PyYAML disagree | `<file>: the bounded reader and PyYAML disagree about <jobs>` |
| Cross-check requested without PyYAML | `cross-checking <file> was requested but PyYAML is not installed` |
| Runner label has no known family | `runs-on label has no known platform family: <label>`, `runs-on must be a single label; found <value>` |
| Virtual-environment layout absent | `virtual-environment layout is absent on <platform>: expected <scripts>/<interpreter> under <root>` |
| Temporary path the tools observe differs from the one set | `temporary-path identity divergence: the rehearsal set <expected> and a child process reported <observed>` |
| Two builds differ | `the two independent builds of <name> differ at byte offset <offset>: set A sha256 <a>, set B sha256 <b>` |
| Teardown asked to leave the root | `teardown refused a path outside the rehearsal root: <path>`, `teardown refused a linked rehearsal root: <root>` |
| Teardown left the root or residue behind | `teardown left the rehearsal root behind: <root>`, `teardown deleted a path outside the rehearsal root: <path>`, `teardown left <n> untracked or modified entries: <sample>` |
| Mode arguments crossed | `release-record mode requires --release-record`, `candidate mode takes no --release-record` |

`test_a_refusal_exits_one_without_writing_a_result` asserts that a refusal exits 1 and writes no result file, so a refusal can never be mistaken for a verdict.

## Verification results

| Check | Result |
|---|---|
| `python -m unittest discover -s tests -p "test_*.py"`, `core.autocrlf=false` clone at `cfca2f3` | PASS — 753 tests, 12 skips, 292.212s |
| same suite, `core.autocrlf=true` worktree at `cfca2f3` | 753 tests, 12 skips, 4 failures — the four byte-exact tests named above, all green in the LF clone |
| same suite at merge base `1431df5`, measured in a separate clean worktree with `core.autocrlf=true` | 652 tests, 12 skips, the **same 4 failures by name** — so `+101` tests and no regression |
| `tests/test_publication_rehearsal.py` alone | PASS — 101 tests |
| `python scripts/validate_engineering_artifacts.py --root .` | PASS — 782 artifacts, 0 errors, 50 warnings (774/0/50 at merge base) |
| candidate validator `templates/repository/standard/scripts/validate_engineering_artifacts.py --root .` | PASS — 782 artifacts, 0 errors, 56 warnings (774/0/56 at merge base) |
| `python scripts/validate_release_distributions.py --root .` | PASS — 1 distribution-bearing record |
| `python scripts/check_portable_release_surface.py --repository .` | PASS |
| `python -m se_harness --help` | exit 0 |
| `check-divergence`, both with and without `--cross-check-yaml` | `EXACT`, exit 0 |
| Full local rehearsal, `core.autocrlf=false` | `rehearsed`, exit 0, 21 executed and 1 declared exclusion |
| Full local rehearsal, `core.autocrlf=true` | `failed`, exit 1, the single failure attributable to the inherited checkout |
| Governing released `0.6.0` evaluator `doctor`, run from outside the checkout | PASS — 87 PASS, 21 WARN, 0 FAIL, exit 0 |
| Governing released `0.6.0` evaluator `preflight … --work-order WO-RLO-005 --phase start` | PASS while the work order was `in_progress`; after the transition it correctly reports `[W005] status 'implemented' is not eligible for start` |
| Governing released `0.6.0` evaluator `preflight … --work-order WO-RLO-005 --phase review` | PASS — `WO-RLO-005 (implemented)`, commit-bound verification `required`, exit 0 |
| In-tree `python -m se_harness doctor .` | 84 PASS, 21 WARN, 9 FAIL — the identical 9 measured in a clean worktree at merge base `1431df5`, so pre-existing |
| `git diff --check 1431df5 HEAD` | exit 0 |
| Changed-path audit against `se_harness/`, `templates/`, `scripts/`, `.engineering-harness.*`, managed policy documents, `docs/engineering/templates/`, `.github/workflows/engineering-harness.yml`, `.github/workflows/publish-pypi.yml` | no match |

The in-tree `doctor` FAIL set is candidate-versus-released skew, not damage: six `distribution:` items (`.gitattributes`, `.github/workflows/engineering-harness.yml`, `docs/engineering/WORKFLOW.json`, `docs/engineering/WORKFLOW.md`, `docs/engineering/templates/VERIFICATION_RECORD.template.md`, `scripts/validate_engineering_artifacts.py`) and three missing `.agents/skills/harness-orient/*` lock entries. The governing evaluator run from outside the checkout reports 0 FAIL, which is the verdict that governs.

`+8` artifacts and unchanged warning counts on both validators mean the eight new `RLO-005` artifacts introduce no new warning of any class.

## The hosted lane's first run did not happen on pull-request opening

The owner authorized the push and the pull request on 2026-08-24, expecting them to produce the lane's first hosted execution on both runner types. They did not, and the reason lies outside this packet.

| Fact | Value |
|---|---|
| Branch pushed | `61d8cae` at 14:47:06 UTC, tracking `origin/feat/rlo-004-publication-rehearsal` |
| Pull request | [#138](https://github.com/mmzen/se_harness/pull/138), opened 14:47:41 UTC, `Harness-Work-Order: WO-RLO-005` present in the fetched-back body with no CR characters |
| Push-triggered checks on that commit | all green — `validate`, candidate source and package evidence, governance migration on Linux and Windows, the platform reconcile, and the governor transition assessment |
| `pull_request`-event workflow runs for #138 | **none created**, including after a close and reopen |
| Publication Rehearsal runs | none; the workflow is not yet registered under `/actions/workflows` because it has never run |

The lane triggers on `pull_request` and on `push` to `main`, so a feature-branch push is not supposed to run it. The missing part is the `pull_request` event itself, and it is not a property of this lane: pull request [#137](https://github.com/mmzen/se_harness/pull/137), which does not contain the lane, was opened three minutes earlier and likewise has no `pull_request`-event run for any of the three pre-existing workflows, while pull request #136 was opened at 13:42:14 UTC and had all three within three seconds. Repository-wide `pull_request` run creation therefore stopped between those two times, and both open pull requests are affected identically.

The consequence for this work order is unchanged from the section above: the Linux half of `REQ-RLO-015` remains unproven on a hosted runner. The lane's first hosted execution now awaits either a later push to the open pull request once `pull_request` delivery recovers, or the merge to `main`, both of which are inside the approved trigger set. Nothing here justifies widening that set to every branch push, which would run two hosted rehearsals for every push in the repository; that is an owner decision and is not taken here.

## The hosted lane's first run, and what it found

`pull_request` delivery recovered, and pushing the merge produced the lane's first
hosted execution: run
[32749064795](https://github.com/mmzen/se_harness/actions/runs/32749064795), event
`pull_request`, created 2026-08-24T16:08:16Z over head `c4bc9cf`, candidate
`e77d3dd7d11408a16aa095b2ec05e5a5e44bbdcc` — the pull request's merge commit, which
is the subject a `pull_request` run resolves.

| Job | Conclusion | Wall clock | Result |
|---|---|---|---|
| Refuse orchestrator and rehearsal divergence | success | 9s | `Publication rehearsal divergence: EXACT`, `Rehearsed jobs: qualify, resolve on Linux, Windows` |
| Rehearse the credential-free path on Linux | success | 1m28s | `REHEARSED`, 21 executed, 2 excluded, `candidate unit suite passed (831 tests)`, 7611 derived paths removed |
| Rehearse the credential-free path on Windows | failure | 2m42s | `FAILED`, 20 executed, 2 excluded, one failed mechanic, 7168 derived paths removed |

Pushing this document's own commit produced a second hosted run,
[32756344464](https://github.com/mmzen/se_harness/actions/runs/32756344464) over
candidate `42649e954a94bd5aa64f893c8ed64d6d0f525f3c`, with the same three
conclusions and the same eleven failing test names. The observation below is
therefore reproducible across two merge commits rather than seen once.

Three things this establishes, all of them the lane's purpose:

First, `REQ-RLO-015`'s Linux half is no longer unproven. It ran on a hosted
`ubuntu-latest` runner against injected nothing: real Git, a real evaluator wheel
resolved and hash-proved, two real builds compared byte for byte, and a real
teardown. The section above recorded that as the packet's principal residual gap,
and it is closed by measurement rather than by argument.

Second, the two exclusions reported identically on both runner types, with the
measured reasons the owner already ruled on. `predecessor-view-qualification` named
both evaluator identities — resolved `0.6.0` against `RLS-SEH-012`'s predecessor
`0.5.0` — and `recipe-bound-build-replay` named its subject obstacle, `the 1
committed records declare distribution schema 1`. Neither is silent, and neither
differs by platform.

Third, the Windows leg failed one mechanic, and the failure is the orchestrator's
rather than the rehearsal's:

```text
Inherited checkout: core.autocrlf=true, so the candidate checkout converts line endings
- failed   candidate-unit-suite: Windows: RehearsalError - candidate unit suite exited 1
  with 11 failing tests: test_canonical_recipe_binds_complete_identity, …
```

`.github/workflows/publish-pypi.yml:209` creates the checkout its qualification
reads with `git worktree add --detach`, and a `git worktree` inherits the checkout's
`core.autocrlf`, which is `true` on `windows-2022`. Rule 5 makes the rehearsal build
that checkout the same way, so this is the orchestrator's own outcome observed
early: the release orchestrator would fail candidate qualification on its Windows
leg, whose steps are gated on `distribution_schema == '1'`, and `RLS-SEH-012`
declares schema 1. That is precisely `RC-060-11` — a real hosted platform detail
found before publication day rather than during it — and it is the first thing this
lane has caught.

Ten of the eleven names are exactly the ten a `core.autocrlf=true` workstation
reproduces at `main`'s `fc97103`. The eleventh,
`test_manifest_rejects_missing_required_invalid_utf8_and_reserved_paths`, exists at
`fc97103` and passes there locally, so the extra red is not a difference in the test
inventory and is not locally reproduced; a `pull_request` run tests the merge commit,
whose `tests/test_agentic_execution.py` is an automatic merge of two divergent
copies, and the hosted interpreter is 3.11.9 rather than 3.14.6. That is recorded as
unexplained rather than attributed. The fix is outside this work
order's subject: the owner routed it to a separate work order and a separate pull
request, `WO-HBI-003`, so that this packet's diff stays exactly the rehearsal lane.
Nothing in this packet changes as a result, and no rule is amended: the rehearsal is
faithful to the orchestrator here, and the condition belongs to the checkout, which
the section on the `core.autocrlf=true` failures already stated. This branch's
Windows job stays red, correctly, until `WO-HBI-003` merges and `main` is merged in
again.

## Repository/product boundary

No changed path lies under `se_harness/`, `templates/`, the eight managed `scripts/` files, `.engineering-harness.toml`, `.engineering-harness.lock`, `.github/workflows/engineering-harness.yml`, the managed policy documents, or `docs/engineering/templates/`. `harnessctl` gains no rehearsal command or option. `check_portable_release_surface.py` passes, though it proves the absence of the *governor and self-hosting* surface and knows nothing of the rehearsal; the rehearsal's portable boundary is proven instead by `test_no_packaged_module_or_template_mentions_the_rehearsal` and `test_the_rehearsal_lives_only_in_repository_owned_locations`, which assert the rehearsal exists only in `.github/`, `tests/`, and `docs/`.

## Security and resilience observations

- The lane declares `contents: read` at workflow and job level, no environment, no secret, no token, and `persist-credentials: false` on both checkouts. Every action is pinned to a full 40-character commit, and the divergence check fails closed on an unpinned or undeclared action in a rehearsed job.
- The rehearsal makes exactly one network request: an HTTPS GET of the released evaluator wheel from its release asset URL. The URL scheme is asserted (`evaluator wheel URL is not https`) and the downloaded bytes are digest-proven against the resolved contract *before* installation (`evaluator wheel digest differs before installation: expected …, read …`). It uploads nothing.
- Orchestrator YAML, declaration data, downloaded bytes, subprocess output, filesystem state, and link targets are all treated as untrusted. The workflow reader refuses a tab, a duplicate key, and any construct outside the modelled subset rather than guessing.
- Teardown unlinks links instead of following them, refuses a linked root, and post-audits every reported deletion by its parent. It then compares `git status --porcelain` against the pre-run snapshot, so residue is detected as a difference and inherited uncommitted entries are not misread as residue. It also removes and prunes the `git worktree add` registration: after both runs `git worktree list` names only the checkout itself, and neither rehearsal root exists on disk.
- Candidate code executes with no credential present, which preserves the property `INT-RLO-001` requires of publication. The rehearsal runs candidate tests and a candidate CLI, and it runs them in an environment where there is nothing to steal.
- The rehearsal builds distributions. They are ephemeral, built under the rehearsal root outside the checkout, never promoted, and removed by teardown; both runs tore down 6209 derived paths and left the worktree clean.

## Residual uncertainty

- The hosted lane has now run once, on both runner types, and the section on that run records it. What remains unproven there is narrower: `release-record` mode has never run hosted, the lane has never run on a `push` to `main`, and one hosted run on each image is not a claim about runner-image stability over time.
- Step digests catch a change inside a declared step. They do not prove the rehearsal drives its mechanics in the orchestrator's order, or that a mechanic sees the same surrounding state. A step moved between jobs passes every comparison. `ARCH-RLO-005` records this as the accepted weakness and `ADR-RLO-005` records what would reopen the refactor decision.
- Two programs can diverge in ways a seam cannot see. The owner chose the seam over a shared implementation deliberately; `ADR-RLO-005` carries the trade.
- `predecessor-view-qualification` is exercised for real only in `release-record` mode against a record under preparation. No such record exists to rehearse now, so that path is covered by unit tests and not by an end-to-end run.
- Everything was measured on CPython 3.14.6, while the orchestrator and the lane pin 3.11. The candidate unit suite inside the rehearsal ran on the local interpreter, not on 3.11.
- The `core.autocrlf=true` reds are named and attributed, not fixed here. Four pre-existing tests asserted on exact bytes when this was first measured and eleven do at the hosted merge commit, because `main` added more such surfaces while the branch was open. That is a real property of this repository, it is out of this work order's scope, and the owner routed it to `WO-HBI-003`, which this branch does not contain.
- `docs/notes/release-publication-rehearsal.md` is repository-owned prose. If it and the formal artifacts disagree, the artifacts govern.

## Amendments, and the owner's decision on them

Seven amendments to approved artifacts were made during implementation. None relaxes a required response; each adds to one. No `statement` field changed.

The accountable repository owner accepted all seven on 2026-08-24 through the statement `Accept all seven`, and the acceptance is recorded in each amended artifact's own amendments section rather than only here. In the same turn the owner ruled on the excluded mechanic: *"On ordinary integration there is no valid subject, so reporting `excluded` with both measured identities is honest. `release-record` mode still fails on a real mismatch, which is where the comparison is meaningful."* `SPEC-RLO-005` rule 37 now carries that ruling and `VER-RLO-005` makes reporting the mechanic `executed`, or omitting it, a failure of the contract. Neither decision authorizes a release, publication, deployment, or governor adoption.

- `SPEC-RLO-005` A7 and rule 37: the resolution subject a mechanic needs, and what happens when none exists.
- `SPEC-RLO-005`: the state model admits an `excluded` outcome with a reason; two error/recovery rows; one valid and one invalid example; the closing facts extended from two to three.
- `REQ-RLO-015`: the required response reports the inherited checkout condition.
- `REQ-RLO-015`: that condition includes line-ending conversion, not only worktree cleanliness.
- `VER-RLO-005`: the `REQ-RLO-015` matrix row admits `excluded` with a reason; two new property tests; residual uncertainty extended.
- `acceptance/publication-rehearsal.feature`: three scenarios — a mechanic with no valid subject, teardown's audit accepting the root, and an inherited converting checkout.
- `docs/notes/release-publication-rehearsal.md`: three things to know instead of two.

Two further amendments, `A8` and `A9`, were forced later and by a different cause: `main` advanced under the open branch and changed the orchestrator, rather than a mismeasurement here. They are not covered by the `Accept all seven` acceptance, so they were put separately, and the accountable repository owner accepted both on 2026-08-24 through the statement `Accept A8 and A9`. `SPEC-RLO-005`'s amendment section records that decision and the framing it was taken over. Neither changes an approved `statement` field, relaxes a pass condition, or widens the authority boundary.

- `SPEC-RLO-005` A8, rules 38 and 39: matrix combination enumeration, per-step gate resolution, step and mechanic platform claims, and declaration schema `v2` with four load-time refusals.
- `SPEC-RLO-005` A9, rule 1 and rule 40: twenty-two mechanics instead of twenty-one, and the recipe-bound build replay always reported `excluded` with a measured reason in both modes.
- `SPEC-RLO-005`: nine error and recovery rows, five examples, and the data-contract paragraph.
- `REQ-RLO-015`: a third amendment recording that one credential-free mechanic cannot be executed on either runner type by this control.
- `REQ-RLO-016`: the required response derives platforms from the matrix and holds the claim per step; two acceptance examples.
- `VER-RLO-005`: the `REQ-RLO-016` row gains the matrix cases; five property tests; the static orchestrator check names the content inherited from `main`; residual uncertainty extended with the second excluded mechanic and the adjacent replay lane.
- `WO-RLO-005`: a lifecycle paragraph for the renumbering, the merge, and the conflict resolution, and a constraint restated as byte-unchanged by this packet.
- `acceptance/publication-rehearsal.feature`: four scenarios — a gated matrix job, a step that loses its gate, an unmodelled matrix or gate refused rather than guessed, and a mechanic no platform can rehearse; the orchestrator scenario now compares against the content inherited from `main`.
- `docs/notes/release-publication-rehearsal.md`: four things to know instead of three, a platform-claims row in the drift-layer table, the per-step claim explained, and the split-by-platform paragraph corrected for the matrix.

## The merge with `main`, and what it changed

`main` advanced to `cda8a10` while this branch was open. Two independent things followed: an identifier collision, and a semantic break in the divergence seam.

### The identifier collision and the renumbering

Pull request #133 (issue #110, the complete build-recipe packet) merged first and bound `CAP-RLO-004` through `WO-RLO-004` to verified `VREC-RLO-004`. This packet had claimed the same identifiers. A verified record is immutable and cannot be re-pointed, so this packet is the side that moved: commit `c7f2e48` renumbered it to `RLO-005` throughout, and `docs/engineering/release-orchestration/README.md` discloses the renumbering in the packet's own section rather than presenting `RLO-005` as the original numbering.

### `main` was merged in, not rebased onto

Commit `29c0db0` is a merge of `cda8a10` into `c7f2e48`. A rebase would have rewritten commits this branch had already published, orphaning any record bound to them; the doctrine is to merge `main` in. One content conflict occurred, in `docs/engineering/release-orchestration/README.md`, where both sides added a packet section at the same place. It was resolved by keeping both sections. That resolution is content no test covered before the merge, which is why it is disclosed here rather than left to the diff. Every other incoming path is `main`'s content taken verbatim; no incoming file was edited to make anything pass.

### The orchestrator changed, and the check refused it

`main` gave the orchestrator's `qualify` job a two-mode matrix, with `mode: legacy-schema-1` on `windows-2022` and `mode: recipe-schema-2` on `ubuntu-latest` declared through `strategy.matrix.include`, and `runs-on` set to the `matrix.os` expression. The divergence check refused the merged file outright, exit 1:

```
publication rehearsal: runs-on label has no known platform family: ${{ matrix.os }}
```

That is `REQ-RLO-016` working as specified — the checker will not guess a platform — and it is not a repairable state, because the orchestrator is out of scope and the claim it refused was genuinely no longer expressible. Five consequences were measured and are recorded in `SPEC-RLO-005` amendments `A8` and `A9`:

1. A job can now run on more than one runner type, so a job's platforms are the union over its enumerated matrix combinations.
2. Every credential-free step of `qualify` now carries a mode gate, so the platform claim had to move from the job to the step. A per-job claim would have stated that the Windows-only build half of `qualify` runs on Linux too — the overstatement of platform coverage that `RC-060-11` is about.
3. Six mechanics measurably run on both platforms now, four of them newly: candidate export, complete-candidate qualification, the unit suite, the CLI smoke check, build-manifest verification, and bundle verification. Six remain Windows-only: temporary-path identity, pinned build-tool installation, the deterministic build, sdist normalization, build-determinism comparison, and bundle assembly.
4. Four `qualify` step titles changed and two steps are new, so four declared `run` digests were re-derived and two step entries added. The declaration schema advanced to `se-harness-publication-rehearsal-mechanics/v2` with a required per-step platform claim; the previously documentary `steps[].mechanics` link now carries a mechanic's platform claim, and a mechanic realized by no declared step of its own job is refused at load time.
5. The step `Replay the exact bound recipe twice` added a twenty-second credential-free mechanic, reported `uncovered` against the approved inventory.

### The twenty-second mechanic cannot be rehearsed here

`repository_tools/release_build.replay_build` pulls and runs an immutable producer image with `docker pull --platform linux/amd64` and `docker run`. Three measurements, in the precedence rule 40 fixes:

| Measurement | Result |
|---|---|
| Committed release records that are released distribution-schema-2 subjects with a bound recipe | none; the one distribution-bearing record, `RLS-SEH-012`, declares distribution schema 1 |
| `docker` on the measuring host's `PATH` | absent |
| `linux/amd64` container execution on `windows-2022` | impossible by runner type, not by configuration |

So the mechanic is declared and always reported `excluded` with the first reason that holds, in both modes. This differs from rule 37's exclusion, which applies to `candidate` mode only, because the platform obstacle is not a property of the subject. The measured run reports the first precedence step: "no committed release record is a released distribution-schema-2 subject with a bound build recipe; the 1 committed records declare distribution schema 1, so this mechanic has no subject to replay".

`main` also added `.github/workflows/release-candidate-replay.yml`, a `workflow_dispatch`-only lane with an empty top-level `permissions` map and one `ubuntu-latest` job under `contents: read`, which replays the exact candidate twice without credentials. That is the honest home of the replay, and the declaration names it in the exclusion reason. It is **not** the declared orchestrator, so this packet's divergence check does not read it and a change to it is invisible here. Widening the check to a second workflow would exceed `SPEC-RLO-005`, which names one orchestrator, so it is disclosed as an adjacent uncovered surface rather than silently absorbed.

### The orchestrator is still byte-unchanged by this packet

The merge-base proof above no longer applies, because `main` changed the file itself. What this packet can honestly claim is that it contributes no byte:

| Proof | Result |
|---|---|
| `git diff --stat cda8a10 29c0db0 -- .github/workflows/publish-pypi.yml` | empty |
| Pinned LF digest in `tests/test_publication_rehearsal.py` | re-derived from `d7313d16db7f…` to `2d3c3b775946d7667d9a175b0bb85446ff90db029d021e155a9b12105ff1f51e` |
| Meaning of the assertion | restated in the test's own comment as byte-unchanged *by this packet*, with the incoming change named |

A pinned digest that is re-derived is only as good as the disclosure of why, which is this row and the merge commit's own message. The digest is re-derived only for an incoming change from `main` and never to accommodate a change made here.

### Re-measured after the merge

| Measurement | Result |
|---|---|
| `check-divergence --repository .` | `EXACT`, exit 0, `Rehearsed jobs: qualify, resolve on Linux, Windows`, five excluded jobs each with its attribute, no uncovered or stale mechanic |
| `tests/test_publication_rehearsal.py` | 121 tests, OK — the 101 that existed before the merge plus 20 new for the matrix layers and the replay exclusion |
| Full suite at `29c0db0` | 825 tests, 5 failures and 5 errors, 12 skipped |
| Control worktree at `cda8a10` | 704 tests, the same ten failure names, 12 skipped |
| Delta | this branch adds 121 tests, all passing, and introduces no new failing test |
| Root frozen validator | PASS, 795 artifacts, 0 errors, 50 warnings |
| Candidate validator | PASS, 795 artifacts, 0 errors, 56 warnings |
| `validate_release_distributions.py --root .` | PASS, 1 distribution-bearing record |
| `git diff --check` | clean for every path this packet touches; three trailing-whitespace reports are in `VALUE_PROPOSAL_EXEC.md`, incoming from `main` as markdown hard line breaks |
| Governing review preflight, released `0.6.0` evaluator run from outside the checkout | `Harness preflight: PASS`, phase `review`, `WO-RLO-005` (`implemented`), no diagnostic |
| Governing `doctor`, same evaluator | PASS, 0 `FAIL` |
| In-tree `doctor` | 9 `FAIL`, the same count as the control at `cda8a10`: six candidate-versus-released template deltas and three `harness-orient` skill lock entries absent from the released distribution. Candidate boundary skew inherited from `main`, not caused by this packet |

The ten reds are the inherited `core.autocrlf=true` condition, now ten rather than the four recorded above, because `main` added byte-exact assertions in `tests/test_agent_contract.py`, `tests/test_hash_bound_integrity.py`, and `tests/test_release_build.py`. Their names are identical in the branch and in the control at `cda8a10`, so none is caused by this packet. None is in `tests/test_publication_rehearsal.py`.

### The full rehearsal at the merge commit

Run on Windows in `candidate` mode at `29c0db0` with a clean worktree: twenty mechanics `executed`, two `excluded` with measured reasons, one `failed`, `unreported_mechanics` empty, `source_date_epoch = 1787586665`, both distribution sets byte-identical — the normalized sdist is `39e9b9eb…` from both trees — `verify-build-manifest` and `verify-bundle` both `exact`, and teardown removing 6289 derived paths without following a link and leaving the worktree clean.

The one failure is `candidate-unit-suite`, and it is the inherited checkout again: the rehearsal names all ten tests in its own failure text, and they are the same ten the control at `cda8a10` reports. The two exclusions are the predecessor-view qualification under rule 37 and the recipe-bound build replay under rule 40, each carrying both measured identities or the measured obstacle in its reason.

The same rehearsal was then run at the same commit in a `core.autocrlf=false` clone, which settles the one failure: state `rehearsed`, exit 0, twenty-one mechanics `executed` including the unit suite at 825 tests passed, the same two exclusions with the same reasons, the same `source_date_epoch = 1787586665`, and the same 6289 derived paths torn down. The same clone reports `check-divergence` `EXACT` at exit 0 and 121 passing rehearsal tests. So every mechanic this control can execute is proven executed at `29c0db0` on the one platform the implementer can run, and the Windows run's single failure is the checkout and nothing else.

| Run at `29c0db0` | State | Unit suite | Exclusions |
|---|---|---|---|
| Working checkout, `core.autocrlf=true` | `failed`, exit 1 | 10 byte-exact tests fail, all ten also failing in the control at `cda8a10` | predecessor-view qualification, recipe-bound build replay |
| Throwaway clone, `core.autocrlf=false` | `rehearsed`, exit 0 | 825 tests passed | the same two, with the same reasons |

## The second merge with `main`, after `WO-HBI-003` landed

`main` advanced from `cda8a10` to `52e3702` while this branch stayed open. Commit `6e16272` merges it in, with parents `4bf05d5` and `52e3702`. Nothing was rebased, so no commit this branch has published is rewritten and no record that binds one is orphaned. The merge is taken under the owner's decision of 2026-08-24: "After you merge #141, I merge main into feat/rlo-004-publication-rehearsal (never rebase), re-derive the pinned digest only if the orchestrator itself moved, disclose any conflict resolution in the evidence, push, and report the hosted rehearsal outcome on both runner types."

### No conflict, and the one auto-merged path

Git reported no conflict. One path was auto-merged: `docs/notes/README.md`, where `main` added two agentic-execution rows and this branch had added the publication-rehearsal row in a different table section. All three rows are present after the merge, each in its own section, and no other row moved. Every other incoming path is `main`'s content taken verbatim; no incoming file was edited to make anything pass. There is therefore no conflict resolution to disclose for this merge, and the previous merge's resolution in `docs/engineering/release-orchestration/README.md` stands unchanged.

### The orchestrator did not move, so the pinned digest is re-verified and not re-derived

The owner's decision made re-derivation conditional on the orchestrator itself moving. It did not.

| Proof | Result |
|---|---|
| `.github/workflows/publish-pypi.yml` blob at `cda8a10`, at `4bf05d5`, at `52e3702` and at `6e16272` | `902bb1978181b74918ad57370f77317e15c7bde3` in all four |
| `git diff --stat cda8a10 52e3702 -- .github/workflows/publish-pypi.yml` | empty |
| SHA-256 of that blob's bytes | `2d3c3b775946d7667d9a175b0bb85446ff90db029d021e155a9b12105ff1f51e`, unchanged |
| Pinned digest in `tests/test_publication_rehearsal.py` | untouched; re-verified, not re-derived |
| `check-divergence --repository . --cross-check-yaml` | `EXACT`, exit 0 |

So the divergence seam is unchanged by this merge, and the assertion still means what the previous section says it means: byte-unchanged *by this packet*.

### `WO-HBI-003` landed, and what that measures here

`main` now carries pull request #141, `WO-HBI-003`, verified by `VREC-HBI-003` against commit `c8fbadd`. That work order exists because this packet's hosted rehearsal measured the release orchestrator failing candidate qualification on `windows-2022`, and it declares seven byte rules in the owner-controlled region of `.gitattributes` so that a `core.autocrlf=true` checkout presents the committed bytes.

Its own evidence discloses the limit that this long-lived checkout then demonstrated: Git rewrites a path on checkout only when its blob changes, so a tree that materialized a path under CRLF before the rule existed keeps the converted bytes. Seven paths were in exactly that state here after the merge, reported by `git ls-files --eol` as `i/lf w/crlf attr/text eol=lf`: `release/build-recipe.json`, `release/build-toolchain.lock`, `se_harness/agent_contract.json`, `se_harness/hash_bound_classes.json`, and the three `harness-orient` skill files under `templates/repository/standard/.agents/skills/`. The nine paths `main` added new to this tree materialized as LF, because their blobs were new here and the rule was already present.

They were re-materialized with `rm` followed by `git checkout --` on those seven paths, which changes worktree bytes and no blob, index entry or recorded digest. The suite was run on both sides of that step:

| Full suite at `6e16272`, `core.autocrlf=true` | Result |
|---|---|
| Before re-materialization, seven paths still CRLF | 926 tests, 15 failures and 5 errors, 22 skipped |
| After re-materialization | 926 tests, 3 failures, 22 skipped |
| Control worktree at plain `52e3702`, freshly materialized by `git worktree add` | 805 tests, the same 3 failure names, 22 skipped |
| Delta | this branch adds 121 tests, all passing, and introduces no failing test |

Seventeen of the twenty reds this packet inherited are gone, which is `WO-HBI-003` working. The control is created with `git worktree add`, which is the orchestrator's own construction and inherits `core.autocrlf=true`, so it materializes from empty exactly as the orchestrator's candidate checkout does.

### An eighth byte-exact surface that no rule covers

Three reds survive, identical in this branch and in the control at plain `main`, so they are `main`'s state and not this packet's:

```
FAIL: test_closed_phase3_contracts_and_manifests_validate
      (test_agentic_execution.SkillContractTests) (skill='harness-draft-change')
      (skill='harness-execute-work-order') (skill='harness-prepare-assurance')
AssertionError: b'policy:\n  allow_implicit_invocation: false\n'
             != b'policy:\r\n  allow_implicit_invocation: false\r\n'
```

`tests/test_agentic_execution.py` line 143 compares the exact bytes of `templates/repository/standard/.agents/skills/<skill>/agents/openai.yaml` for three skills. `WO-HBI-003` declares rules for `*.json`, `*.md` and `*.py` under that directory and no rule for `*.yaml`, so `git ls-files --eol` reports these three as `i/lf w/crlf attr/` — converted, with no attribute resolved — in the freshly materialized control at `52e3702`.

The sequence explains why the fix missed them, and it is a timing fact rather than an omission in the work order:

| Event | Commit | Time, local |
|---|---|---|
| `WO-HBI-003` branched from `main` | `fc97103` | 2026-08-24 17:16:36 +0200 |
| The three `agents/openai.yaml` files and their byte-exact assertion were added | `284b842`, merged as `5fb6a0c` for pull request #143 | 2026-08-24 20:19:53 +0200 |
| `WO-HBI-003` merged | `888d2b6` for pull request #141 | 2026-08-24 20:42:13 +0200 |

The two pull requests touch disjoint paths, so nothing conflicted and nothing warned. `WO-HBI-003`'s guard cannot see it either: `ByteExactSurfaceTests` derives its inventory from the declared patterns and asserts that each selects a tracked file and resolves `text eol=lf`, so it detects a rule that has gone stale, not an assertion that has no rule. Closing that gap means deriving the inventory from the suite's byte-exact assertions instead, which is a change to `WO-HBI-003`'s guard and outside this packet.

The consequence for this packet is exact and is not softened: on `windows-2022` the release orchestrator's candidate qualification fails again, on three tests instead of ten, for the same reason as before. This rehearsal is the lane that measures it, and the Windows leg is expected to report `candidate-unit-suite` failed with these three names. Nothing here changes `.gitattributes`, `tests/test_agentic_execution.py` or any file outside this packet's execution scope; the finding is recorded and routed to an owner decision rather than fixed inside a merge.

### Re-measured after the second merge

| Measurement | Result |
|---|---|
| `check-divergence --repository . --cross-check-yaml` | `EXACT`, exit 0, `Rehearsed jobs: qualify, resolve on Linux, Windows`, five excluded jobs each with its attribute, no uncovered or stale mechanic |
| `tests/test_publication_rehearsal.py` | 121 tests, OK |
| Full suite at `6e16272`, re-materialized worktree | 926 tests, 3 failures, 22 skipped, all three inherited from `main` |
| Control at `52e3702` | 805 tests, the same 3 failure names, 22 skipped |
| Governing validator, released `0.6.0` evaluator run from outside the checkout | PASS, 822 artifacts, 0 errors, 50 warnings, all maintenance |
| Candidate validator | PASS, 822 artifacts, 0 errors, 50 warnings; the six-warning gap recorded at the previous merge closed with `main`'s own changes |
| Governing review preflight, same evaluator | `Harness preflight: PASS`, phase `review`, `WO-RLO-005` (`implemented`), no diagnostic |
| Governing `doctor`, same evaluator | exit 0, 87 checks, 0 `FAIL` |
| In-tree `doctor` | 84 `PASS`, 25 `FAIL`; the control at `52e3702` reports the same 84 and the same 25 with identical names, so the skew is inherited candidate-versus-released boundary state and not caused by this packet |
| `validate_release_distributions.py --root .` | PASS, 1 distribution-bearing record |
| `git diff --check` | clean |

The in-tree `doctor` count moved from 9 `FAIL` to 25 with `main`'s content, entirely in two families: six candidate-versus-released template deltas, and nineteen `.agents/skills/**` lock entries absent from the released `0.6.0` distribution. Both are the released-evaluator boundary and both are present in the control.

## The hosted run after the second merge, on both runner types

Run [32766680271](https://github.com/mmzen/se_harness/actions/runs/32766680271), `pull_request` event, branch head `3768cd4`, candidate commit `29b5e3fed14c`:

| Job | Conclusion | Result |
|---|---|---|
| Refuse orchestrator and rehearsal divergence | success | `EXACT`, `Rehearsed jobs: qualify, resolve on Linux, Windows`, `Rehearsal lane platforms: Linux, Windows`, no uncovered or stale mechanic |
| Rehearse the credential-free path on Linux | success | `REHEARSED`, 21 mechanics executed, 2 excluded, `candidate unit suite passed (928 tests)`, `source_date_epoch = 1787598655`, 7741 derived paths removed without following a link |
| Rehearse the credential-free path on Windows | failure | `FAILED`, 20 executed, 2 excluded, one failed mechanic, the same `source_date_epoch = 1787598655`, 7298 derived paths removed |

Both legs report the same two exclusions with identical reasons, `unreported_mechanics` empty, and both distribution sets byte-identical on their own platform. Every other check on the pull request passes, including `Governance migration` on both platforms and `Reconcile governance migration platforms` on both event runs, which did not exhibit the known digest flake this time.

`REQ-RLO-015`'s Linux half remains proven by measurement rather than by argument: a hosted `ubuntu-latest` runner executed all twenty-one rehearsable mechanics with nothing injected, including a 928-test candidate suite, two builds compared byte for byte, and a real teardown.

### The Windows leg, exactly

```
Inherited checkout: core.autocrlf=true, so the candidate checkout converts line endings
- failed   candidate-unit-suite: Windows: RehearsalError - candidate unit suite exited 1
  with 2 failing tests: test_closed_phase3_contracts_and_manifests_validate,
  test_manifest_rejects_missing_required_invalid_utf8_and_reserved_paths
```

The retained result artifact records `Ran 928 tests` and `FAILED (failures=4, skipped=10)`. Four failures, which the rehearsal reports as two distinct test names.

**Three are the eighth uncovered surface recorded above.** They are the `agents/openai.yaml` sub-cases of `test_closed_phase3_contracts_and_manifests_validate`, and the retained stderr tail carries the assertion verbatim:

```
AssertionError: b'policy:\n  allow_implicit_invocation: false\n'
             != b'policy:\r\n  allow_implicit_invocation: false\r\n'
```

The section above predicted that the Windows leg would report "these three names". That was imprecise in one way and is corrected here rather than edited there: the rehearsal reports distinct test names, and the three skill sub-cases collapse into one name.

**One is not a line-ending failure at all, and it is the red `WO-HBI-003`'s evidence recorded as unexplained.** `test_manifest_rejects_missing_required_invalid_utf8_and_reserved_paths` passes in every local control, at `52e3702` and at `6e16272`, and fails on `windows-2022`.

What is measured: at `tests/test_agentic_execution.py:389` the test copies a skill tree, writes `NUL.txt`, and accepts either an `OSError` — in which case it takes a skip branch — or `SKM003` from `build_skill_manifest`. On the measuring workstation, Windows 11 build 26200 with CPython 3.14.6, `Path("NUL.txt").write_text(...)` succeeds *and* the file is enumerable, so `SKM003` is raised and the test passes. The test's other two branches, a missing `SKILL.md` and an invalid-UTF-8 file, are not platform-dependent. On `windows-2022` with CPython 3.11 a reserved device basename with an extension resolves to the device, so the write succeeds and no file exists to enumerate; nothing is raised and the assertion fails.

What is not measured: the rehearsal retains a 600-character stderr tail, which the `openai.yaml` traceback fills, so this test's own assertion text is absent from retained evidence and only its name is recorded. The reserved-name branch is the only branch whose behaviour is image- and interpreter-dependent, so the cause above is stated as attribution supported by a local measurement, not as proof from the runner. Settling it needs a run that retains more output, which no work order authorizes here.

Both failures would fail the release orchestrator's Windows candidate qualification, whose steps are gated on `distribution_schema == '1'` and whose subject `RLS-SEH-012` declares schema 1. Finding them at integration time rather than on publication day is what `RC-060-11` asks for and what this lane is for; it has now caught three distinct conditions. Neither is fixed here: both are outside `WO-RLO-005`'s execution scope and neither has an authorizing work order.

The hosted Windows leg reports 10 skips where this workstation reports 22 over the same suite. That difference is noted and not investigated, because a skip count is not a pass condition anywhere in this packet; it does mean the platform-guarded coverage claim in this evidence is measured per platform and should not be read as identical on both.

## The third merge with `main`, after `WO-HBI-004` landed

`main` advanced from `52e3702` to `1d459cf` while this branch stayed open, carrying pull
request #144 (`WO-WEX-003`, semantic lifecycle handoffs, with `VREC-WEX-006`) and pull
request #145 (`WO-HBI-004`, the fix for the eighth byte-exact surface this packet's
hosted run found, together with the reserved-name test-portability defect). Commit
`7918a1b` merges it in, with parents `935a9d6` and `1d459cf`. Nothing was rebased, so no
commit this branch has published is rewritten and no record that binds one is orphaned.

The merge is taken under the owner's decision of 2026-08-24, selected over two
alternatives: "Same pattern as #141: the fix merges first, then I merge main into the
RLO-005 branch again and re-run the rehearsal, so #138 goes green before you decide on
it. One extra merge-and-re-measure cycle on my side, no extra review of #138."

### No conflict and no auto-merge, because the two sides are disjoint

Git reported no conflict, and this time it had nothing to reconcile at all. The merge
base is `52e3702`; `comm -12` over the two changed-path sets, `52e3702..935a9d6` and
`52e3702..1d459cf`, is empty, so not one path was touched by both sides. Every incoming
path is `main`'s content taken verbatim and no incoming file was edited to make anything
pass. There is no conflict resolution to disclose for this merge, and the resolutions
recorded for the first two merges stand unchanged.

### The orchestrator did not move again, so the pinned digest is re-verified

| Proof | Result |
|---|---|
| `.github/workflows/publish-pypi.yml` blob at `935a9d6`, at `1d459cf` and at `7918a1b` | `902bb1978181b74918ad57370f77317e15c7bde3` in all three |
| Path absent from `git diff --name-only 935a9d6...origin/main` | confirmed; the incoming delta touches no `.github/` path |
| SHA-256 of that blob's bytes | `2d3c3b775946d7667d9a175b0bb85446ff90db029d021e155a9b12105ff1f51e`, 38213 bytes, unchanged |
| `ORCHESTRATOR_LF_SHA256` in `tests/test_publication_rehearsal.py` | untouched; re-verified, not re-derived |
| `check-divergence --repository . --cross-check-yaml` | `EXACT`, exit 0 |

### `WO-HBI-004` landed, and what that measures here

`WO-HBI-004` replaces `WO-HBI-003`'s three per-extension rules under the closed phase-3
skill templates with one tree rule,
`templates/repository/standard/.agents/skills/** text eol=lf`, and changes
`ByteExactSurfaceTests` to derive its inventory from the tracked set rather than from the
declared patterns.

The same limit this packet demonstrated at the previous merge applied again, for the same
reason: Git re-materializes a path on checkout only when its blob changes, so this
long-lived worktree kept the converted bytes of files whose blobs the merge did not move.
Exactly three paths were in that state after the merge, and they are precisely the three
the previous merge left uncovered:

```
i/lf w/crlf attr/text eol=lf   templates/repository/standard/.agents/skills/harness-draft-change/agents/openai.yaml
i/lf w/crlf attr/text eol=lf   templates/repository/standard/.agents/skills/harness-execute-work-order/agents/openai.yaml
i/lf w/crlf attr/text eol=lf   templates/repository/standard/.agents/skills/harness-prepare-assurance/agents/openai.yaml
```

They now resolve the rule, which is the difference from the previous merge, where the
same command reported `attr/` and no attribute at all. They were re-materialized with
`rm` followed by `git checkout --` on those three paths, which changes worktree bytes and
no blob, index entry or recorded digest; `git status --porcelain` is empty afterwards. All
fifteen tracked files under that tree then report `i/lf w/lf attr/text eol=lf`.

The control worktree at plain `1d459cf`, created with `git worktree add` — the
orchestrator's own construction, inheriting `core.autocrlf=true` — materializes all
fifteen as `w/lf` on the first checkout with no intervention. That is the property the
release orchestrator's candidate checkout depends on, measured rather than argued.

### Re-measured after the third merge

| Measurement | Result |
|---|---|
| Full suite at `7918a1b`, re-materialized worktree, `core.autocrlf=true` | **932 tests, OK, 22 skipped — no failure and no error** |
| Control at plain `1d459cf`, freshly materialized by `git worktree add` | 811 tests, OK, 22 skipped |
| Delta | this branch adds 121 tests, all passing, and no failing test remains in either checkout |
| `tests/test_publication_rehearsal.py` | 121 tests, OK |
| `check-divergence --repository . --cross-check-yaml` | `EXACT`, exit 0, `Rehearsed jobs: qualify, resolve on Linux, Windows`, `Rehearsal lane platforms: Linux, Windows`, five excluded jobs each with its attribute, no uncovered or stale mechanic |
| Governing validator, released `0.6.0` evaluator run from outside the checkout | PASS, 830 artifacts, 0 errors, 50 warnings, all maintenance |
| Candidate validator | PASS, the same 830 / 0 / 50 |
| Governing review preflight, same evaluator | `Harness preflight: PASS`, phase `review`, `WO-RLO-005` (`implemented`), no diagnostic |
| Governing `doctor`, same evaluator | exit 0, 87 checks, 0 `FAIL`, including `PASS managed:.gitattributes: unchanged` and `PASS distribution:.gitattributes: matches distribution` |
| In-tree `doctor` | 81 `PASS`, 28 `FAIL`; `diff` against the control at `1d459cf` is empty, so the skew is inherited candidate-versus-released boundary state — nine `distribution:` and nineteen `lock-entry:` — and none of it is caused by this packet |
| `validate_release_distributions.py --root .` | PASS, 1 distribution-bearing record |
| `git diff --check` | clean |

The three reds this packet inherited at the previous merge and the reserved-name red
beside them are both gone, in the branch and in the control. This is the first
measurement in this packet's history where a `core.autocrlf=true` checkout at the branch
head has no failing test, and it is `WO-HBI-004` working rather than anything this packet
changed: the packet's own 121 tests were already passing at every previous merge, and the
figures that moved are `main`'s.

What this does not measure is the hosted lane. The prediction is that the `windows-2022`
leg now reports `REHEARSED`, and it is stated as a prediction until the run exists. The
rehearsal's candidate suite runs inside its own derived checkout of the candidate commit
and reported 928 tests where this workstation reports 932 over the branch tip, and the
hosted legs report 10 skips against 22 here, so no count from this section should be
carried across to the run recorded below.

## Actions explicitly not performed

Through the two commits this document measures, no external mutation of any kind was performed. The owner then authorized exactly two on 2026-08-24, by the statement `Push the branch and open a pull request with a Harness-Work-Order: WO-RLO-005 trailer`: pushing `feat/rlo-004-publication-rehearsal` and opening its pull request. That is the first hosted execution of the rehearsal lane on both runner types, and the Linux half is unproven, so the lane may report red.

After that, `main` was merged into the branch as `29c0db0` and the branch was pushed again to the same pull request. A merge into a feature branch and a push to a branch the owner already authorized pushing are within that authorization; nothing else was extended by it. That push is what produced the hosted first run recorded above. Amendments `A8` and `A9` were accepted on 2026-08-24 through the statement `Accept A8 and A9`, and the same turn routed the Windows finding into `WO-HBI-003` rather than into this packet; neither decision authorizes anything further.

The same owner turn on 2026-08-24 took the decision this second merge executes: "After you merge #141, I merge main into feat/rlo-004-publication-rehearsal (never rebase), re-derive the pinned digest only if the orchestrator itself moved, disclose any conflict resolution in the evidence, push, and report the hosted rehearsal outcome on both runner types." Commit `6e16272` is that merge and the branch is pushed again to the same pull request; both acts are inside the merge-and-push authorization already recorded above and neither extends it. The eighth byte-exact surface the merge measured, the three `agents/openai.yaml` files, is recorded above and reported to the owner. No fix for it was attempted here: it needs a change to `WO-HBI-003`'s guard and to `.gitattributes`, both outside this work order's execution scope, and no work order authorizes it yet.

The same class of act was taken a third time on 2026-08-24 under the owner's sequencing
decision quoted above, after they merged pull request #145: `main` was merged in as
`7918a1b` and the branch pushed again to the same pull request, which is what re-runs the
hosted rehearsal. Both acts are inside the merge-and-push authorization already recorded
here and neither extends it. The eighth byte-exact surface and the reserved-name defect
this packet's hosted run found were fixed in `WO-HBI-004` under its own work order, on its
own branch and in its own pull request; nothing in this packet was changed to accommodate
them, and this packet's own `.gitattributes`, guard and tests are untouched by that work.

Everything else remains not performed and not authorized: no tag, branch other than this feature branch, GitHub Release, PyPI publication, Pages deployment, protected-environment approval, workflow dispatch of the release orchestrator, release record, release-record preparation or transition, promotable distribution build, `VREC`, assurance decision, governor adoption, credential acquisition, or hosting or branch-protection change. `WO-RLO-005` transitions only to `implemented`; commit-bound verification remains `required` and unmet, and reliance on this rehearsal in any release decision requires a later ready `VREC` and an accountable assurance decision.
