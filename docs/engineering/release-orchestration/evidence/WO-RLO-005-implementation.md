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

None of the four is in `tests/test_publication_rehearsal.py`; all four assert on exact bytes and all four are green at the same commit in the `core.autocrlf=false` clone. They are a property of the inherited checkout, not of this work order and not of the publication path. That is why `REQ-RLO-015` was amended to report `line_ending_conversion` on the result and why the human summary states `Inherited checkout: core.autocrlf=true, so the candidate checkout converts line endings`.

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

- The hosted lane has never run. Real `ubuntu-latest` and `windows-2022` runner-image behavior is unproven, which is the same class of gap `RC-060-11` describes — moved from release time to integration time rather than eliminated.
- Step digests catch a change inside a declared step. They do not prove the rehearsal drives its mechanics in the orchestrator's order, or that a mechanic sees the same surrounding state. A step moved between jobs passes every comparison. `ARCH-RLO-005` records this as the accepted weakness and `ADR-RLO-005` records what would reopen the refactor decision.
- Two programs can diverge in ways a seam cannot see. The owner chose the seam over a shared implementation deliberately; `ADR-RLO-005` carries the trade.
- `predecessor-view-qualification` is exercised for real only in `release-record` mode against a record under preparation. No such record exists to rehearse now, so that path is covered by unit tests and not by an end-to-end run.
- Everything was measured on CPython 3.14.6, while the orchestrator and the lane pin 3.11. The candidate unit suite inside the rehearsal ran on the local interpreter, not on 3.11.
- The `core.autocrlf=true` reds are named and attributed, not fixed. Four pre-existing tests assert on exact bytes and fail in a converting checkout; that is a real property of this repository's test suite and is out of this work order's scope.
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

## Actions explicitly not performed

Through the two commits this document measures, no external mutation of any kind was performed. The owner then authorized exactly two on 2026-08-24, by the statement `Push the branch and open a pull request with a Harness-Work-Order: WO-RLO-005 trailer`: pushing `feat/rlo-004-publication-rehearsal` and opening its pull request. That is the first hosted execution of the rehearsal lane on both runner types, and the Linux half is unproven, so the lane may report red.

Everything else remains not performed and not authorized: no tag, branch other than this feature branch, GitHub Release, PyPI publication, Pages deployment, protected-environment approval, workflow dispatch of the release orchestrator, release record, release-record preparation or transition, promotable distribution build, `VREC`, assurance decision, governor adoption, credential acquisition, or hosting or branch-protection change. `WO-RLO-005` transitions only to `implemented`; commit-bound verification remains `required` and unmet, and reliance on this rehearsal in any release decision requires a later ready `VREC` and an accountable assurance decision.
