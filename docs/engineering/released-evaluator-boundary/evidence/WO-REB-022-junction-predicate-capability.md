# WO-REB-022 Junction-Predicate Capability Evidence

Date: 2026-08-24

Authority: non-authoritative retained implementation evidence. This file does not approve, verify, release, publish, tag, or deploy anything. It records what was measured on one platform at one commit, plus one hosted measurement read from a stored workflow log. Commit-bound assurance for this work order remains a separate `VREC` decision, and this file is not that decision. This file also corrects one measured claim in `WO-REB-021`'s retained evidence; the correction is recorded here, in section 13, rather than by editing that file.

artifact: WO-REB-022
checkpoint: handoff
formal_snapshot_sha256: 10a3f61b7eb6ec4e8424d347f2fe92042a2775d7d7b87a7eacf7e971982bb3c1

## 1. Governing packet and preflight

`WO-REB-022` implements the already approved `REQ-REB-024` under `SPEC-REB-011`, `ARCH-REB-010`, `ADR-REB-010` and `VER-REB-010`. It adds no requirement and no packet artifact. The owner holds the engineering-owner, quality-owner, security-owner, technical-owner, requirements-steward and repository-owner roles in this repository.

Two lifecycle transactions, both through the released 0.6.0 evaluator installed in a virtual environment outside this checkout, because the in-tree CLI refuses these mutations under mutation guard `MG005` on runtime identity:

```text
C:\Users\mathi\se_harness_eval_060\Scripts\python.exe -I -m se_harness transition . \
  --set WO-REB-022=approved --decision WO-REB-022=engineering-owner --reason "..." --apply
Workflow transition: COMPLETED
Applied 1 explicit lifecycle transition(s) atomically.
WO-REB-022 is approved.
```

```text
C:\Users\mathi\se_harness_eval_060\Scripts\python.exe -I -m se_harness transition . \
  --set WO-REB-022=in_progress --decision WO-REB-022=engineering-owner --reason "..." --apply
Workflow transition: COMPLETED
Applied 1 explicit lifecycle transition(s) atomically.
WO-REB-022 is in_progress.
```

The recorded decision timestamps are `2026-08-24T15:11:20Z` for `draft` to `approved` and `2026-08-24T15:13:52Z` for `approved` to `in_progress`. Both transitions are committed as `8f95721`, separately from the implementation.

Preflight from the same released evaluator, at both phases this work order reaches:

```text
C:\Users\mathi\se_harness_eval_060\Scripts\python.exe -I -m se_harness preflight . --work-order WO-REB-022 --phase start
Harness preflight: PASS
Phase: start
Work order: WO-REB-022 (approved)
Assurance classification: commit-bound verification required, decided by engineering-owner
exit code 0
```

```text
C:\Users\mathi\se_harness_eval_060\Scripts\python.exe -I -m se_harness preflight . --work-order WO-REB-022 --phase review
Harness preflight: PASS
Phase: review
Work order: WO-REB-022 (in_progress)
Assurance classification: commit-bound verification required, decided by engineering-owner
exit code 0
```

That evaluator reports `0.6.0` on Python `3.14.6`. Full-graph validation from it, after the transitions:

```text
C:\Users\mathi\se_harness_eval_060\Scripts\python.exe -I -m se_harness validate .
Engineering artifact validation: PASS
Artifacts: 786 | Errors: 0 | Warnings: 50
Planes: structure E0/W0 | governance E0/W0 | policy E0/W0 | maintenance E0/W50
```

All 50 warnings are pre-existing maintenance warnings (`W013` canonical-location, `W014` missing `decision_assessment` on completed legacy architecture, `W015` deprecated `constrains` relation). None names an artifact this work order touches.

## 2. Base commit, branch, and lifecycle position

- Base commit: `2a6bae7230efb894b0737c5e71719100ace22c91`, the tip of `feat/reb-safe-venv-identity`, which is the branch carrying `WO-REB-021`.
- Branch: `fix/reb-junction-predicate-pinned-lane`, stacked on that branch rather than on `main`, so this diff carries this work order alone.
- `4a3cc05` proposes `WO-REB-022` (draft packet, 149 lines, one file).
- `8f95721` records the two lifecycle transitions of section 1 (one file).
- The implementation commit is the next one; it is the commit a `VREC` must bind.

`WO-REB-021` is `implemented` and `docs/engineering/WORKFLOW.json` admits only `verified` and `released` from that state, so this repair cannot be carried under it. That is why this is a separate work order. The two work orders are two commits ranges and two pull requests; they do not share a diff.

## 3. The hosted failure as measured

The defect was measured, not inferred. The hosted workflow ran on the `WO-REB-021` candidate commit `f9225f887d23303be01ba7d73219c53e0fec0f95`, which is the commit `VREC-REB-017` binds.

- Workflow run: `32740492685`
- Failing job: `97473516042`, "Candidate source evidence", step "Run complete candidate-source regression"
- Runner interpreter: `/opt/hostedtoolcache/Python/3.11.16/x64` on `ubuntu`, the lane `.github/workflows` pins as `python-version: "3.11"`
- Other checks on the same head: `validate` SUCCESS, `Governor transition assessment` SUCCESS, every later job SKIPPED behind the failed one

Verbatim tail of that step's log:

```text
----------------------------------------------------------------------
Ran 764 tests in 40.474s

FAILED (failures=33, errors=38, skipped=4)
```

Verbatim first failure block from the same log:

```text
======================================================================
ERROR: test_authority_oracle_rejects_undeclared_and_operational_mutations (test_governance_migration.GovernanceMigrationTests.test_authority_oracle_rejects_undeclared_and_operational_mutations)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/runner/work/se_harness/se_harness/se_harness/governance_migration.py", line 158, in _safe_interpreter
    entry = interpreter_safety.evaluate(python, checkout_root=repository)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/se_harness/se_harness/se_harness/interpreter_safety.py", line 434, in evaluate
    raise InterpreterSafetyRefusal(
se_harness.interpreter_safety.InterpreterSafetyRefusal: EPS011 link_predicate: this runtime cannot classify a directory junction
```

The 71 failures and errors were parsed out of the stored log and tallied by module:

| Module | FAIL + ERROR |
| --- | --- |
| `test_interpreter_safety` | 34 |
| `test_governance_migration` | 15 |
| `test_predecessor_preparation` | 11 |
| `test_release_bootstrap` | 10 |
| `test_predecessor_publication` | 1 |

67 of the 71 blocks carry `EPS011` in their traceback. The remaining 4 are the capability assertions themselves, which fail for the same cause without going through a refusal: `test_at_least_one_route_is_present_on_every_supported_runtime`, `test_both_loaders_report_the_capability_on_this_runtime`, and the two subtests of `test_the_stat_route_alone_reports_the_capability`. `WO-REB-022`'s own Defect section states that every one of the 71 traced to `EPS011` raised in `evaluate`; that is exact for 67 and, for the other 4, the same cause is asserted directly rather than observed through a refusal. The correction is recorded here rather than by editing the approved packet's own statement of the defect.

Cause, measured on this host rather than assumed:

```text
python 3.14.6 on nt
hasattr(Path, 'is_junction')                      : True
hasattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT')     : True
hasattr(stat, 'IO_REPARSE_TAG_MOUNT_POINT')       : True
hasattr(os.stat_result, 'st_file_attributes')     : True
hasattr(os.stat_result, 'st_reparse_tag')         : True
```

`FILE_ATTRIBUTE_REPARSE_POINT` is defined in the cross-platform `Lib/stat.py` and is present on every supported runtime. `IO_REPARSE_TAG_MOUNT_POINT` is published only by the `_stat` C extension and only under `MS_WINDOWS`. `os.stat_result.st_file_attributes` and `st_reparse_tag` are likewise Windows-only members. A Python 3.11 runtime off Windows therefore has no `pathlib.Path.is_junction` and no mount-point reparse tag, which is exactly the combination the hosted lane refused on. The Windows development lane cannot reach the defect, because on Windows every route is present at every supported version.

## 4. Local reproduction and the measured repair

Reproduction is driven by a measurement of the base-commit predicate rather than by an assumption about which route is missing. The base-commit `link_classification_available` was read out of `git show 2a6bae7:<loader>`, evaluated with the three routes withdrawn to the pinned lane's profile, and observed:

```text
2a6bae7:se_harness/interpreter_safety.py       : link_classification_available()=False
2a6bae7:repository_tools/interpreter_safety.py : link_classification_available()=False
```

That measured value was then pinned into both loaders and the boundary modules the hosted lane failed in were run locally. The module set is the five hosted-failing modules other than `test_interpreter_safety`, plus `test_predecessor_assessment_contract`, `test_release_qualification` and `test_evaluator_identity` as controls. `test_interpreter_safety` is excluded because it patches the same module constants the reproduction pins; its own coverage is section 6.

```text
python reb022_control.py
pinned the base-commit predicate value under the pinned lane's profile:
  se_harness.interpreter_safety: link_classification_available=False
  repository_tools.interpreter_safety: link_classification_available=False
Ran 75 tests in 17.863s
FAILED (failures=11, errors=24, skipped=2)
```

114 lines of that output name `EPS011`. Failure names were compared against the hosted set:

- 27 distinct hosted failure names lie in the boundary modules (the 60 hosted names minus the 33 in `test_interpreter_safety`).
- 25 of those 27 reproduce by name locally.
- The 2 that do not are `test_predecessor_preparation.test_external_interpreter_preserves_posix_virtualenv_link` and `test_predecessor_preparation.test_external_interpreter_rejects_linked_environment_parent`. Both are explicitly skipped on this host: "POSIX virtualenv interpreters use terminal links" and "POSIX link rejection coverage". They cannot fail where they do not run.
- Zero local-only failures.

The local traceback is the same frame chain and the same message as the hosted one, on the same test:

```text
ERROR: test_authority_oracle_rejects_undeclared_and_operational_mutations (tests.test_governance_migration.GovernanceMigrationTests.test_authority_oracle_rejects_undeclared_and_operational_mutations)
Traceback (most recent call last):
  File "...\se_harness\governance_migration.py", line 158, in _safe_interpreter
    entry = interpreter_safety.evaluate(python, checkout_root=repository)
  File "...\se_harness\interpreter_safety.py", line 469, in evaluate
    raise InterpreterSafetyRefusal(
        "EPS011", "link_predicate", "this runtime cannot classify a directory junction"
    )
se_harness.interpreter_safety.InterpreterSafetyRefusal: EPS011 link_predicate: this runtime cannot classify a directory junction
```

The repair was then proven against the same simulated profile. All three routes are withdrawn from both loaders by pointing each named constant at a name no runtime carries; nothing inside `stat`, `os` or `pathlib` is patched, so only the capability decision is simulated:

```text
python reb021_lane_sim.py
simulated profile: pathlib route absent, mount-point tag absent, stat members absent
  se_harness.interpreter_safety: reparse_information_observable=False link_classification_available=True
  repository_tools.interpreter_safety: reparse_information_observable=False link_classification_available=True
Ran 75 tests in 36.585s
OK (skipped=2)
```

The same 75 tests that produced 35 failures and errors before the repair all pass after it, under the same profile, and the capability is reported as decided with reparse information unobservable — that is, decided by the third route.

Both scripts are run with the checkout as the working directory. An earlier run from `C:\Users\mathi` produced one extra failure, `test_release_qualification.test_failure_result_bounds_paths_and_retains_no_authority`. That is an artifact of the launching directory and not of the capability: `_bounded_message` in `se_harness/release_qualification.py` substitutes `Path.cwd()` as `<ROOT>` before it substitutes `tempfile.gettempdir()` as `<TEMP>`, and this host's temp directory lies under `C:\Users\mathi`. It is recorded here because the earlier measurement exists, not because it bears on the repair.

## 5. Changed-path manifest

`WO-REB-022`'s execution scope lists ten paths as a maximum allowlist. Nine were changed. Added and removed lines, measured against the base commit:

| Path | Added | Removed |
| --- | --- | --- |
| `docs/engineering/released-evaluator-boundary/README.md` | 3 | 1 |
| `docs/engineering/released-evaluator-boundary/requirements/REQ-REB-024.md` | 25 | 0 |
| `docs/engineering/released-evaluator-boundary/specifications/SPEC-REB-011.md` | 36 | 1 |
| `docs/engineering/released-evaluator-boundary/verification/VER-REB-010.md` | 24 | 2 |
| `docs/engineering/released-evaluator-boundary/work-orders/WO-REB-022.md` | 149 | 0 |
| `repository_tools/interpreter_safety.py` | 45 | 10 |
| `se_harness/interpreter_safety.json` | 2 | 2 |
| `se_harness/interpreter_safety.py` | 45 | 10 |
| `tests/test_interpreter_safety.py` | 225 | 18 |

The tenth listed path is this evidence file. No unlisted path is touched; `git status --porcelain` names no other file.

The two loaders changed identically. Diffing their worktree diffs line by line leaves only two differing lines, both hunk headers (`@@ -44,6 +44,11 @@` against `@@ -45,6 +45,11 @@`, and `@@ -289,23 +294,53 @@` against `@@ -288,23 +293,53 @@`); every added and removed line of content is byte-identical between them.

## 6. The three routes and the capability decision table

The added surface in each loader is one constant and one predicate function, plus one narrowed condition:

```python
#: The ``os.stat_result`` members through which a filesystem reports reparse
#: information. A runtime whose stat result carries neither member observes no
#: reparse point on any path, so the junction predicate answers ``False`` by
#: construction there rather than being unavailable.
REPARSE_STAT_MEMBERS = ("st_file_attributes", "st_reparse_tag")


def reparse_information_observable() -> bool:
    return all(hasattr(os.stat_result, name) for name in REPARSE_STAT_MEMBERS)


def link_classification_available() -> bool:
    if hasattr(Path, JUNCTION_PREDICATE):
        return True
    if all(hasattr(stat, name) for name in REPARSE_CONSTANTS):
        return True
    return not reparse_information_observable()
```

`_is_junction` and `_is_symlink` are unchanged. Their existing `getattr` guards already return `False` on a runtime that carries none of the routes, which is the answer the third route asserts is correct there, so the detection code needed no change — only the capability rule did.

The whole decision table, measured over both loaders by pointing each named constant at a name the running runtime does or does not carry:

| `is_junction` route | `stat` constants route | reparse observable | `se_harness` | `repository_tools` | expected |
| --- | --- | --- | --- | --- | --- |
| present | present | yes | True | True | True |
| present | present | no | True | True | True |
| present | absent | yes | True | True | True |
| present | absent | no | True | True | True |
| absent | present | yes | True | True | True |
| absent | present | no | True | True | True |
| absent | absent | yes | **False** | **False** | **False** |
| absent | absent | no | True | True | True |

Eight combinations, both loaders agreeing with the expectation in all eight. The single `False` row is the one `EPS011` was written for: a runtime that can encounter a reparse point and cannot classify it. The last row is the pinned lane, and it is the row the defect got wrong.

The expectation is owned by the test, not by the loader. `test_the_capability_decision_covers_every_route_combination` writes the eight-row table as test data and compares each loader's answer against it, and `test_reparse_observability_is_reported_from_the_stat_result_members` asserts the observability predicate reads the members `REPARSE_STAT_MEMBERS` names rather than something else. Each route is withdrawn or supplied by name, through the `_routes` context manager, so every combination is constructable on either lane and none depends on the running lane's own capabilities.

## 7. `EPS011` reachability before and after

`EPS011` is narrowed, not removed. It remains the second entry of the declared case list in `EVALUATION_ORDER`, remains `refused`, and remains reachable and tested.

| Condition | Before the repair | After the repair |
| --- | --- | --- |
| reparse observable, neither predicate route | `EPS011` | `EPS011` |
| reparse unobservable, neither predicate route | `EPS011` | accepted; predicate answers negative |
| either predicate route present | accepted | accepted |

Proven by four focused tests, all passing:

- `test_withdrawing_both_routes_reports_no_capability` — with reparse observability pinned present and both predicate routes withdrawn, both loaders report no capability.
- `test_withdrawing_both_routes_refuses_a_real_environment` — the same profile refuses a constructed environment with `EPS011`, against a real path rather than against the capability function alone.
- `test_a_runtime_with_no_reparse_surface_accepts_a_real_environment` — with observability withdrawn as well, the same constructed environment is accepted, `refusal_case is None`, and the derived environment root equals `entry.parent.parent`. This is the regression the repair fixes, asserted against a real path.
- `test_an_unobservable_reparse_surface_alone_reports_the_capability` — the third route alone decides the predicate.

Every refusal reachable at the base commit is still reachable: the base and repaired suites produce the identical failure-name set (section 10), the declared case list and outcomes are byte-equal in structure (section 9), and the adversarial corpus tests in `tests/test_interpreter_safety.py` pass unchanged.

## 8. The third route names no platform, proven mechanically

`test_the_capability_rule_names_no_platform` walks the AST of both loader modules and asserts that `os.name`, `sys.platform`, `platform.system`, `platform.platform` and the literal `"nt"` appear in none of `link_classification_available`, `reparse_information_observable`, `_is_junction` or `_is_symlink`. It passes.

A passing absence test proves nothing unless a platform name would fail it, so the test was mutated against:

```text
python reb022_mutation_probe.py
unmutated: exit=0 OK
mutated se_harness/interpreter_safety.py with `os.name == "nt"`: exit=1 FAILED (failures=2)
mutated repository_tools/interpreter_safety.py with `os.name == "nt"`: exit=1 FAILED (failures=2)
restored: exit=0 OK
worktree diffstat for the two loaders after restore:
 repository_tools/interpreter_safety.py | 55 +++++++++++++++++++++++++++-------
 se_harness/interpreter_safety.py       | 55 +++++++++++++++++++++++++++-------
```

Each loader was mutated in turn with an `os.name == "nt"` short-circuit inserted into `link_classification_available`, the test failed, and the file was restored from its captured original in a `finally` block. The post-probe diffstat equals the pre-probe diffstat, and both loaders remain free of carriage returns in the worktree.

This is the constraint `REQ-REB-024` states first — detection shall not depend on the platform name — and the reason the third route reads `os.stat_result`'s own member surface rather than a platform identifier. The prohibition in `WO-REB-021`'s and `WO-REB-022`'s decision envelopes against a platform-name conditional in the capability functions is therefore enforced by a test rather than by review.

## 9. Declared cases, order, registry and corpus are unchanged

The declaration was parsed at the base commit and in the worktree and compared structurally:

| Property | Unchanged |
| --- | --- |
| `schema` | yes |
| case identifiers, in order | yes |
| case outcomes | yes |
| case subjects | yes |
| boundary registry (id, runtime, module, kind) | yes |
| corpus identifiers, in order | yes |
| corpus expected outcomes | yes |
| corpus `constructable_on` | yes |
| `outcomes` | yes |
| `position_classes` | yes |

11 cases in declared evaluation order — `EPS010`, `EPS011`, `EPS001` through `EPS009` — 8 boundaries, 18 corpus entries. Exactly two values differ from the base commit, both of them summary strings:

- `EPS011.summary`, now "the runtime observes reparse information on its filesystem yet exposes no route that classifies a directory junction, so link safety cannot be decided".
- `ISC016.summary`, now describing a runtime that observes reparse information yet exposes neither predicate route, constructed on either platform by withdrawing and supplying the three named routes.

`ISC016.constructable_on` stays `["linux","windows"]`. Its test patches the capability functions rather than building a path, so the case remains constructable on both lanes, and the repair makes that true of every combination rather than only of this one.

Declaration bytes: `04cd0de61eeca6590e8368e6bdd08e2d3adbc697a526ab74b3695f4d6972a378` at the base commit, `83ae1bef77f7d57845964bfa2690a6dad6c614863281eb8236abc653f58f2507` in the worktree. As `WO-REB-021`'s evidence recorded, nothing digests these bytes; the loaders parse the file and the conformance check compares parsed structures, so these two figures are facts of this worktree rather than pinned invariants. `.gitattributes` is unchanged and remains outside scope.

The bidirectional declaration comparison, the cross-runtime conformance check, the boundary-registry check and the import-barrier check are the existing tests in `tests/test_interpreter_safety.py`. All pass (section 10).

## 10. Focused module, full suite, and the baseline comparison

The baseline was captured independently, in a throwaway detached worktree at the base commit `2a6bae7`, on the same host and interpreter, rather than inferred from an unchanged total.

Focused module:

```text
base   worktree: python -m unittest tests.test_interpreter_safety -v
       Ran 83 tests in 1.045s
       OK (skipped=10)

repair worktree: python -m unittest tests.test_interpreter_safety -v
       Ran 88 tests in 0.806s
       OK (skipped=10)
```

Test names were diffed: five added, none removed.

- `JunctionPredicateTests.test_an_unobservable_reparse_surface_alone_reports_the_capability`
- `JunctionPredicateTests.test_the_capability_decision_covers_every_route_combination`
- `JunctionPredicateTests.test_reparse_observability_is_reported_from_the_stat_result_members`
- `JunctionPredicateTests.test_the_capability_rule_names_no_platform`
- `JunctionPredicateTests.test_a_runtime_with_no_reparse_surface_accepts_a_real_environment`

The skip count is 10 in both runs. The four named skips are the pre-existing Windows symbolic-link privilege skips for `ISC002`, `ISC004`, `ISC006` and `ISC013`. The repair removes a skip rather than adding one: the base commit's `test_the_pathlib_route_alone_reports_the_capability` called `self.skipTest` when `pathlib.Path.is_junction` was absent, and the repaired version pins that route present instead. The removal is invisible in the count on this host, where the route exists and the skip never fired; it is visible on the pinned 3.11 lane, where it did.

Full suite:

```text
base   worktree: Ran 764 tests in 278.425s   FAILED (failures=4, skipped=22)
repair worktree: Ran 769 tests in 281.211s   FAILED (failures=4, skipped=22)
```

The two failure-name sets are identical, and both contain exactly the four known Windows line-ending failures of this host:

- `test_agentic_execution.test_contract_rejects_duplicate_and_unknown_fields`
- `test_agentic_execution.test_manifest_normalizes_line_endings_and_detects_content_changes`
- `test_hash_bound_integrity.test_declaration_is_data_only`
- `test_release_build.test_non_promotable_ephemeral_wheel_carries_and_fresh_installs_one_skill_core`

Delta added: none. Delta removed: none. The test-count delta is exactly `769 - 764 = 5`, the five tests added here. The base commit's own 764 is the same total the hosted lane ran, where those four pass and the interpreter-safety failures do not exist.

Remaining required checks, all from the candidate checkout on Python 3.14.6:

```text
python scripts/validate_engineering_artifacts.py --root .
Engineering artifact validation: PASS
Artifacts: 786 | Errors: 0 | Warnings: 50

python scripts/validate_release_distributions.py --root .
SE Harness release distribution validation: PASS (1 distribution-bearing record)

python scripts/check_portable_release_surface.py --repository .
portable release surface: PASS

python -m se_harness --help
exit code 0
```

## 11. Amendment record

Three artifacts restate the rule this repair changes, and all three were amended in the same act, each in its own `## Amendment record` section:

- **`SPEC-REB-011` rule 4**, amended a second time. The rule now states three routes and narrows `EPS011` to a runtime that observes reparse information and has neither predicate route. The amendment section names the `_stat` / `MS_WINDOWS` cause, the hosted measurement, and the fact that the third route can only answer negative and only where the platform supplies nothing for the other two to classify — so the amendment adds no acceptance beyond the one the defect wrongly refused. Rule 5 of the specification's own "Explicitly unspecified decisions" prohibits adding, removing, renumbering or reordering a declared case; section 9 measures that none of that happened.
- **`VER-REB-010`**, amended a second time: the `REQ-REB-024` junction-predicate method row and refusal scenario 4. Refusal scenario 3 is unchanged, because it concerns a real junction on Windows where both classifying routes exist. The amendment strengthens the obligation — the whole decision table against a test-owned expectation, a real-path assertion for the pinned lane's combination, and a removed skip rather than an added one — and the contract's coverage statement that neither platform alone verifies `REQ-REB-024` stands unchanged.
- **`REQ-REB-024`**, amended once, under the owner's explicit decision to amend the requirement rather than rely on the specification alone. A second constraint states that a runtime observing no reparse information answers the junction question rather than disabling the check, that the observation is a runtime capability read from the stat-result surface rather than a platform identifier, and that the check is disabled only if a runtime that can encounter a reparse point proceeds without classifying it. The `WHEN` statement, the required response, every listed refusal form, the failure and boundary behavior, every acceptance example, and the first constraint are unchanged.

The domain index gained one paragraph recording the defect, the hosted measurement, the third route, the forward-only-lifecycle reason for a separate work order, and the supersession of `VREC-REB-017` rather than a re-pointing of it.

## 12. Non-change proofs

- Managed hash-locked paths: `.engineering-harness.toml`, `ENGINEERING_HARNESS.md`, `.github/workflows/engineering-harness.yml`, the seven managed documents under `docs/engineering/`, all of `docs/engineering/templates/`, and the eight managed scripts are all absent from `git status --porcelain`, so all are byte-unchanged. No script is touched at all by this work order.
- `.engineering-harness.lock` is unchanged; no fragment digest moved.
- `AGENTS.md`, `CLAUDE.md`, `.gitignore` and `.gitattributes` are unchanged, so no tracked fragment block and no byte-pinning rule was touched.
- `pyproject.toml` is unchanged: the declaration was already package data, and no dependency, version or `requires-python` value moved. `requires-python` remains `>=3.11` and no lane version changed.
- `se_harness/governance_migration_contract.json` is unchanged, so the six `implementation_sha256` values `WO-REB-021` re-measured are untouched and every digest bound to that contract holds.
- The 13 evaluator-evidence sidecars under `docs/engineering/**/evidence/*-evaluator.json` are unchanged, as is the canonical `se-harness-evaluator-evidence-v1` document. The runtime-identity schema identifier remains `se-harness-runtime-identity-v3` and no field was added to either schema.
- The boundary registry, the evaluation order and `EVALUATION_ORDER` itself are unchanged.
- `repository_tools` still imports only the standard library and its own package; `se_harness` does not import `repository_tools`. Neither loader imports the other.
- History: no commit was amended and no history was rewritten. `4a3cc05` and `8f95721` are ordinary commits on a new branch stacked on `2a6bae7`.
- Tags: 9 tags — `v0.2.0`, `v0.2.1`, `v0.2.2`, `v0.3.0`, `v0.4.0`, `v0.4.1`, `v0.5.0`, `v0.5.0a1`, `v0.6.0` — unchanged. No tag was created, moved or deleted. Released bytes and public distributions are untouched.
- The installed root evaluator, the root lock and the root configuration are unchanged. Nothing was adopted.

## 13. Relationship to `WO-REB-021` and to `VREC-REB-017`

This work order edits neither `WO-REB-021` nor its retained evidence, and it changes no lifecycle event either records. `WO-REB-021` stays `implemented` at `2026-08-24T14:43:03Z`. The implementation that transition accepted is exactly the implementation this repair corrects.

`WO-REB-021`'s retained evidence disclosed the gap this defect fell through, in its own words: capability withdrawal proved the fallback logic rather than the 3.11 runtime. That disclosure was accurate. What it did not do is state that the fallback logic itself was wrong for the pinned lane, and its full-suite section reported a green local suite as coverage of the change. This file corrects that claim of coverage: the local Windows suite could not fail on this defect, because on Windows every route is present, so its green result was not evidence about the pinned lane. Section 4 of this file supplies the missing measurement in both directions — the reproduction and the repair — through a simulated route profile that either lane can construct.

`VREC-REB-017` binds `f9225f887d23303be01ba7d73219c53e0fec0f95`, the commit the hosted lane measured 33 failures and 38 errors on. A verification record's provenance cannot be re-pointed at a later commit, and a record that has been verified cannot be corrected, so the record is superseded and a successor is written with every field measured afresh over the post-repair commit. Fresh candidates are prepared for both work orders: one for `WO-REB-022`, and one for `WO-REB-021` over the same post-repair commit, so that the entry-point safety rule's assurance binds a tree on which the pinned lane passes. The supersession and the successors are separate governance commits and separate decisions; this file is not either of them.

## 14. Hosted re-run

Measured. The pinned lane is repaired for the defect this work order names, and the same run exposes two further failures that the defect had been hiding. The lane is not green, so the work order's stop-and-escalate condition is active and this section retains the exact failures rather than absorbing them.

### 14.1 The run

| Fact | Value |
| --- | --- |
| Workflow | `SE Harness Candidate Evidence` |
| Run | `32745833437` — <https://github.com/mmzen/se_harness/actions/runs/32745833437> |
| Job | `97490996661` `Candidate source evidence`, conclusion `failure` |
| Step | `Run complete candidate-source regression` |
| Event | `pull_request` (`PR #140`) |
| Head commit | `def14847951f2837cfde363f9fcb0655230ec95d` |
| Branch | `fix/reb-junction-predicate-pinned-lane` |
| Started | `2026-08-24T15:35:54Z` |
| Runtime observed in the traceback | `/opt/hostedtoolcache/Python/3.11.16/x64` |

Six later jobs are `skipped`, as they are gated on this one.

### 14.2 The measured movement

| Commit | Lane result |
| --- | --- |
| `f9225f887d23303be01ba7d73219c53e0fec0f95` (`WO-REB-021` candidate) | `Ran 764 tests`, `FAILED (failures=33, errors=38, skipped=3)` |
| `def14847951f2837cfde363f9fcb0655230ec95d` (this repair) | `Ran 769 tests in 47.229s`, `FAILED (failures=1, errors=1, skipped=3)` |

Seventy-one failures and errors became two. Every `EPS011 link_predicate` occurrence is gone from the log: the capability is decided on the pinned lane by the third route, exactly as section 4's simulated profile predicted, and the test count is `+5` there as it is locally.

### 14.3 The two remaining failures, verbatim

Both are retained here in full rather than summarized, because the work order requires the exact failure and because neither is repairable inside this work order's execution scope.

The first, an error:

```
ERROR: test_a_link_cycle_is_refused_rather_than_looping (test_interpreter_safety.RuleEvaluationTests.test_a_link_cycle_is_refused_rather_than_looping)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/pathlib.py", line 993, in resolve
    s = os.path.realpath(self, strict=strict)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen posixpath>", line 413, in realpath
  File "<frozen posixpath>", line 480, in _joinrealpath
  File "<frozen posixpath>", line 480, in _joinrealpath
  File "<frozen posixpath>", line 475, in _joinrealpath
OSError: [Errno 40] Too many levels of symbolic links: '/tmp/tmpl8pc1f53/venv/bin/python'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/runner/work/se_harness/se_harness/tests/test_interpreter_safety.py", line 541, in test_a_link_cycle_is_refused_rather_than_looping
    self.assertEqual("EPS003", self._both(first))
                               ^^^^^^^^^^^^^^^^^
  File "/home/runner/work/se_harness/se_harness/tests/test_interpreter_safety.py", line 369, in _both
    first = interpreter_safety.refusal_case(path, **kwargs)  # type: ignore[arg-type]
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/se_harness/se_harness/se_harness/interpreter_safety.py", line 568, in refusal_case
    evaluate(
  File "/home/runner/work/se_harness/se_harness/se_harness/interpreter_safety.py", line 486, in evaluate
    target = lexical.resolve(strict=True)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/pathlib.py", line 995, in resolve
    check_eloop(e)
  File "/opt/hostedtoolcache/Python/3.11.16/x64/lib/python3.11/pathlib.py", line 990, in check_eloop
    raise RuntimeError("Symlink loop from %r" % e.filename)
RuntimeError: Symlink loop from '/tmp/tmpl8pc1f53/venv/bin/python'
```

The second, a failure:

```
FAIL: test_external_interpreter_rejects_linked_environment_parent (test_predecessor_preparation.PredecessorPreparationTests.test_external_interpreter_rejects_linked_environment_parent)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/runner/work/se_harness/se_harness/repository_tools/predecessor_preparation.py", line 214, in _safe_interpreter
    return interpreter_safety.evaluate(path, checkout_root=root)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/se_harness/se_harness/repository_tools/interpreter_safety.py", line 476, in evaluate
    raise InterpreterSafetyRefusal(
repository_tools.interpreter_safety.InterpreterSafetyRefusal: EPS001 parent: an enclosing directory is a symbolic link

The above exception was the direct cause of the following exception:

repository_tools.predecessor_preparation.PredecessorPreparationError: evaluator interpreter is refused by EPS001: an enclosing directory is a symbolic link

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/runner/work/se_harness/se_harness/tests/test_predecessor_preparation.py", line 211, in test_external_interpreter_rejects_linked_environment_parent
    with self.assertRaisesRegex(
AssertionError: "environment must not traverse a link" does not match "evaluator interpreter is refused by EPS001: an enclosing directory is a symbolic link"
```

### 14.4 Neither failure is a regression of this repair

Both test names appear in the pre-repair hosted failure list for `f9225f88`, where each carried `EPS011 link_predicate` instead. The blanket capability refusal fired before either rule could be reached, so both tests failed for the defect this work order repairs and neither could report its own cause. The measured list is the evidence: `test_a_link_cycle_is_refused_rather_than_looping` and `test_external_interpreter_rejects_linked_environment_parent` were both already failing before this branch existed.

Each is therefore a second, unrelated defect in the implementation `WO-REB-021` accepted, unmasked by this repair rather than introduced by it. Neither is reachable on the Windows development lane: the first needs a symbolic-link privilege that lane lacks, and the second is skipped there by `unittest.skipIf(os.name == "nt", "POSIX link rejection coverage")`.

### 14.5 The two causes, as measured on this host

Both were reproduced here without a 3.11 POSIX interpreter, by supplying the report the pinned lane produces rather than the platform that produces it, and both candidate repairs were then measured against the same probe. The probe is `reb022_amend_probe.py`, run from the branch tip and from a throwaway worktree at `def1484` carrying the candidate repairs.

**Cause one — a resolution failure the rule does not catch.** `evaluate` rule 5 calls `Path.resolve(strict=True)` inside `except OSError`. Below Python 3.13 `pathlib` catches the underlying `ELOOP` itself and re-raises `RuntimeError("Symlink loop from ...")`, which that clause does not catch, so the refusal escapes as a `RuntimeError` instead of `EPS003`. The same hole exists in `_resolved_within`, whose `except (OSError, ValueError)` guards a second `resolve(strict=True)`. Measured, branch tip against candidate:

| Observation | Branch tip `def1484` | With the candidate repair |
| --- | --- | --- |
| `se_harness` loader, resolution reporting a cycle | `escaped as RuntimeError: Symlink loop from ...` | `EPS003 interpreter: the interpreter path does not resolve` |
| `repository_tools` loader, same | `escaped as RuntimeError: Symlink loop from ...` | `EPS003 interpreter: the interpreter path does not resolve` |

Both files are inside this work order's execution scope. A lane-independent conformance test is constructable in the in-scope focused module: added and measured, the module goes 88 to 89 tests, `OK (skipped=10)`, and with the loader repair reverted that single test fails with the `RuntimeError` above, so it bites.

**Cause two — a changed observable message at a boundary whose behaviour is frozen.** `WO-REB-021` re-pointed `predecessor_preparation._safe_interpreter` at the declared rule and, in doing so, replaced the base commit's `f"{label} environment must not traverse a link"` with `f"{label} is refused by {refusal.case}: {refusal.detail}"`. `SPEC-REB-011` rule 22 states that this module's "current observable behavior is the reference for the rule and shall not change", and `WO-REB-021`'s own stop-and-escalate list names "Correcting a boundary would change the observable behavior of `predecessor_preparation`". The change went unobserved because the only test that reads the message is skipped on Windows and was masked by `EPS011` on the pinned lane. Measured, branch tip against a candidate that retains the frozen wording ahead of the case identifier for the two enclosing-link cases:

| Refusal supplied to `_ordinary_external_interpreter` | Branch tip matches the frozen wording | Candidate matches |
| --- | --- | --- |
| `EPS001` enclosing directory is a symbolic link | no | yes |
| `EPS002` enclosing directory is a directory junction | no | yes |
| `EPS003` (control, not an enclosing-link case) | no | no |

`repository_tools/predecessor_preparation.py` is **not** inside this work order's execution scope, and neither is `tests/test_predecessor_preparation.py`.

### 14.6 Stop and escalate

Two of this work order's stop-and-escalate conditions are met: "The hosted lane still fails after the repair, or fails for a second unrelated cause", and "Another file, lifecycle policy change, historical mutation, released-byte change, or external action is required". Its instruction is "Retain the exact failure and request a bounded amendment. Do not absorb another defect and do not create a bypass."

Accordingly:

- The exact failures are retained above, verbatim, with their causes measured rather than inferred.
- No repair for either cause is committed under this work order's current scope. The candidates exist only in a throwaway worktree and are recorded here as measurements, not as changes.
- No test was weakened, skipped, marked expected-failure, or bounded by a platform name to make the lane green. No bypass was created.
- `WO-REB-022` stays `in_progress`. It is not transitioned to `implemented`, because its own required verification is "Confirm on the hosted lane that the previously failing job passes", and the job does not pass.
- No verification record binds this work order or `WO-REB-021`, and `VREC-REB-017` is not superseded, until a bounded amendment is decided and the lane is measured green.

The requested amendment and its alternatives are an owner decision recorded where that decision is taken, not here. This section records only what was measured.

## 15. Coverage gaps and residual risks

- **The pinned lane is simulated here, not run here.** Section 4's profile withdraws the three routes by name on a Windows host. It reproduces the hosted failure by name for 25 of the 27 boundary-module failures and repairs all of them, but it is not a 3.11 POSIX interpreter. Only section 14's hosted re-run closes this, and it is the reason the work order requires it.
- **The two POSIX-only preparation tests are still skipped on this host.** Both are skipped for lack of the Windows symbolic-link privilege, so this lane cannot observe them directly. Section 14 measures both of their causes here anyway, by supplying the report the pinned lane produces instead of the platform that produces it; that closes the diagnosis, not the platform coverage, and the hosted lane remains the only place their repair is observable end to end.
- **The junction half of the corpus is still Windows-only and the symbolic-link half still POSIX-only.** `VER-REB-010`'s coverage statement that neither platform alone verifies `REQ-REB-024` is unchanged by this repair.
- **The third route is an inference about the filesystem from the runtime's stat-result surface.** A hypothetical runtime whose stat result omits both members while its filesystem does carry reparse points would be accepted where it should refuse. No supported runtime is in that position: the members and the reparse constants come from the same `_stat` extension under the same platform condition. The risk is recorded rather than dismissed, and the mechanical route table of section 6 is where a future runtime that breaks the assumption would have to be handled.
- **This file records one platform at one commit.** Nothing here is a verification decision.

## 16. Actions not performed

No release, no tag, no publication, no deployment, no version change, no dependency change. No promotable or non-promotable distribution was built. No credential was used and no package index was contacted. No maintenance mutation, no root-evaluator adoption, no lock or root managed file change, no external policy change, no history rewrite, no amended commit, no force push. No lifecycle transition other than the two in section 1. No verification record was written, superseded, or bound by this file. No change to `WO-REB-021`, to its evidence, or to `VREC-REB-017`. No hosted workflow was dispatched manually. `PR #137`'s unresolved conflict against `main` was not touched: it remains a separate owner decision, and this branch is stacked on that branch rather than rebased onto `main`, so nothing here moves the commit `VREC-REB-017` binds.
