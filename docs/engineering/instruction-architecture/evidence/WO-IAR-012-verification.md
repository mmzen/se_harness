# WO-IAR-012 implementation and verification evidence

## Authority and candidate state

The repository owner approved `REQ-IAR-020`, `SPEC-IAR-012`, `VER-IAR-012`, and `WO-IAR-012` on 2026-08-21 together with the `WO-DST-021` packet, and authorized implementation the same day. This file records the `VER-IAR-012` execution.

At evidence finalization the implementation is an uncommitted working-tree candidate. No commit, push, pull request, verification transition, or release was performed, and none is authorized by this approval.

`WO-IAR-012` and `WO-DST-021` were implemented in the same working tree. They are independent by design: rule 3 of `SPEC-IAR-012` states the `REPOSITORY_CONTEXT.md` pointer by content rather than by harness status, so the owner region is correct both before and after the scaffold retirement. Product, template, and readiness figures belong to `WO-DST-021` and are recorded in `WO-DST-021-verification.md` in this directory and in `../../harness-distribution/evidence/WO-DST-021-verification.md`.

## Evaluator identity

```text
../se-harness-eval-1685/Scripts/python -I -m se_harness
se-harness 0.5.0
C:\Users\mathi\se-harness-eval-1685\Lib\site-packages\se_harness
```

Released-evaluator `preflight` for `WO-IAR-012` is `Harness preflight: PASS` with exit 0 for both `start` and `review` while the work order is `approved`. After the closeout transition to `implemented`, `review` still passes and `start` reports the expected `W005` start-ineligibility, which managed `WORKFLOW.md` specifies for completed work.

## The pre-existing owner-region revision and its correction

The work order records that an uncommitted revision of the owner region already existed in the worktree, made before the packet was drafted, that it is not implementation, and that it did not satisfy the revised rule 3. That was the only rule the pre-existing text violated. It described the file as harness-owned:

```text
`docs/engineering/REPOSITORY_CONTEXT.md` carries the same commands plus the release-build,
release-binding, and publication sequences. It is preflight-required and harness-seeded, so it
stays; read it before any build, release, or publication step.
```

Implementation replaced that sentence with a statement by content:

```text
`docs/engineering/REPOSITORY_CONTEXT.md` is repository-owned content carrying the same commands
plus the release-build, release-binding, and publication sequences. Read it before any build,
release, or publication step. Those sequences are not duplicated here.
```

Every rule of `SPEC-IAR-012` was then reviewed against the whole region rather than assumed satisfied; rules 1, 2, and 4 through 13 were already met by the existing text and are asserted by the tests below.

## Managed block digest invariance

Computed with `canonical_sha256(tracked_content("fragment", ...))` against `.engineering-harness.lock`, before and after the edit:

```text
AGENTS.md   computed=bcf46d13ceee8c2606834a897eba153a654f0092c1d41c8737723739a1405f1c
            lock    =bcf46d13ceee8c2606834a897eba153a654f0092c1d41c8737723739a1405f1c   match=True
```

Unchanged in both directions. The two other fragment paths are unchanged as well: `.gitignore` `1b9c8af1917e119817b7160d3afa4e7277226d187b964c318fdbb6072beeaeaa`, `CLAUDE.md` `a5d3b02b3200e5dc147578f81f2b80ca4a0f055a0a4a1c94a535352572ade2cd`. The stop condition on a changed fragment digest was never approached.

`AGENTS.md` uses CRLF line endings in this worktree; `utf8-text-lf-v1` canonicalizes line endings only, which is why the digest holds. The file carries exactly one begin marker and one end marker, in order.

## Region size bound

```text
owner region: 4875 bytes   (bound: 6000)
whole file:   5436 bytes
```

The owner region is the file with the marker block and both markers removed, so the measurement excludes managed content.

## Lock-derived path agreement

The path expectations are derived from `.engineering-harness.lock` at test time, not from prose. The lock has exactly 28 `managed` paths:

| Group | Count |
| --- | --- |
| root and CI (`.engineering-harness.toml`, `ENGINEERING_HARNESS.md`, `.github/workflows/engineering-harness.yml`) | 3 |
| `docs/engineering/*.md` policy modules (`WORKFLOW`, `DECISION_RIGHTS`, `QUALITY_GATES`, `TRACEABILITY`) | 4 |
| `docs/engineering/templates/` | 13 |
| `scripts/` | 8 |

`test_owner_region_identifies_every_managed_path_from_the_lock` asserts the count is 28 and that every path is identified in the region: the thirteen templates by the collective statement `every file in \`docs/engineering/templates/\``, and each other path by its full path or, where the region states a shared directory prefix once, by its basename. The four policy modules are identified on one bullet, `` `docs/engineering/WORKFLOW.md`, `DECISION_RIGHTS.md`, `QUALITY_GATES.md`, `TRACEABILITY.md` ``, which rule 6 permits because all four are identified.

`test_owner_region_separates_owner_editable_scripts_from_managed_ones` asserts the eight managed script paths derived from the lock and the five owner-editable ones named in the region are disjoint, and that no owner-editable script has a lock entry at all:

```text
managed (8):        artifact_layout_registry.py, check_engineering_harness.ps1,
                    check_engineering_harness.sh, generate_harness_dashboard.py,
                    harness_explorer/index.template.html, inspect_engineering_artifacts.py,
                    select_harness_work_order.py, validate_engineering_artifacts.py
owner-editable (5): bind_release_distribution.py, check_portable_release_surface.py,
                    create_release_bundle_manifest.py, normalize_sdist.py,
                    validate_release_distributions.py
```

This is the separation the work order's assurance rationale calls out: an agent told that all of `scripts/` is managed would block the documented release-build path.

## Required content presence

`test_owner_region_carries_the_required_operational_facts` asserts thirteen operational facts are present, including the test, graph-validation, and release-distribution commands, the entry points, the `pyproject.toml` reference, the pointer to the owner-authored `REPOSITORY_CONTEXT.md`, `templates/repository/standard/` as the destination for managed changes, `` `.engineering-harness.lock` is authoritative ``, the `Harness-Work-Order: WO-` pull-request line, `stored event payload`, `RID018`, `docs/engineering/README.md` as the domain index, and the statement that product invariants are governed requirements rather than content of the file. It also asserts the lint-or-format answer is stated as `none is configured` with `Do not invent one as a required gate`, so an agent cannot read the absence as an omission.

`test_owner_region_directs_the_evaluator_outside_the_checkout` asserts the region says `outside the checkout`, pins `se-harness==0.5.0`, and names each of `focus`, `check`, `transition`, and `rehearse-recovery` as candidate-only commands that must not appear in instructions the released gate has to satisfy.

`test_owner_region_keeps_the_retained_agent_constraints` asserts the four retained change-and-verification constraints are present verbatim, including the untrusted-input rule and the release-build prohibition.

## Withdrawn-restatement negatives

`test_owner_region_states_no_withdrawn_or_governed_restatement` asserts the region contains none of `preflight-required`, `harness-seeded`, `so it stays`, or `Python 3.11+`. The first three are the withdrawn rule-3 phrasing; the fourth is a governed product fact that belongs in requirements, not in an instruction file that would then need updating alongside them.

`test_owner_region_claims_no_authority` asserts the lowercased region contains none of `i approve`, `approved by`, `takes precedence`, `overrides \`docs/engineering/\``, or `authorizes release`, which is the rule that owner instructions may constrain but cannot waive.

`test_owner_file_carries_exactly_one_ordered_marker_pair` asserts the marker invariant directly.

## Test placement

The ten focused tests were added as `OwnerInstructionRegionTests` in `tests/test_instruction_architecture.py`, which is the module named in this work order's `execution_scope` and matches the expected change surface, "one test module under `tests/`, extending the existing instruction-architecture coverage". An earlier draft placed them in a new `tests/test_owner_instruction_region.py`; that file was outside the declared execution scope and was removed, with the class moved rather than rewritten.

```text
python -m unittest tests.test_instruction_architecture
Ran 26 tests in 11.972s
OK
```

Sixteen pre-existing instruction-architecture tests plus the ten new ones. The retained existing instruction-route test is among the sixteen and passes unchanged.

## Domain records

`docs/engineering/instruction-architecture/README.md` records the packet under "Implemented owner-region instruction revision" with the four-artifact index, following the established pattern. `acceptance/instruction-architecture.feature` gained one scenario under `WO-DST-021`; this work order added no scenario of its own beyond that shared file, because the routing scenario covers the same owner-region destination from the product side.

## Verification results

| Check | Result |
| --- | --- |
| `python scripts/validate_engineering_artifacts.py --root .` | PASS, 605 artifacts, 0 errors, 44 warnings, matching the recorded baseline |
| `python -m unittest discover -s tests -p "test_*.py"` | 403 tests, 2 known environment conditions, 5 skips |
| released-evaluator `preflight` `--phase start` | PASS |
| released-evaluator `preflight` `--phase review` | PASS |
| released-evaluator `doctor .` | exit 0, 81 PASS, 0 FAIL, 15 pre-existing maintenance warnings |

The two suite failures are the known environment conditions of any Windows clone here and are recorded as such, not as regressions:

- `test_standard_repository_lifecycle.test_candidate_source_identity_is_deterministic_and_bounded` — `RID018 distribution_origin`, because the machine-wide editable `se-harness` install owns the package metadata. The work order requires this be named explicitly, and the region itself documents it.
- `test_workflow_documentation_contract.test_fresh_install_contains_managed_machine_contract` — raw byte comparison of `WORKFLOW.json` against a CRLF worktree.

## Lifecycle transitions at closeout

`REQ-IAR-020`, `SPEC-IAR-012`, and `WO-IAR-012` are set to `implemented`. `VER-IAR-012` stays `approved`, matching the recorded `VER-IAR-011` precedent: a verification contract is not advanced by the implementation it governs, and a verification transition is a separate accountable decision that was not performed.

The `AGENTS.md` fragment digest was re-measured against the lock after the transitions and still equals `bcf46d13ceee8c2606834a897eba153a654f0092c1d41c8737723739a1405f1c`. The validator and the full suite were re-run and match the figures below.

## Change surface

- `AGENTS.md`: one substituted sentence in the owner region. The managed block, both markers, and every other line are unchanged.

Measured against `main` rather than against the worktree, the committed `AGENTS.md` diff is larger — 57 insertions and 10 deletions — because the pre-existing uncommitted owner-region revision recorded above had never been committed and lands in the same commit. Both parts are owner-region content governed by `REQ-IAR-020` and `SPEC-IAR-012`, and the tracked block digest is byte-identical to `main`'s at `bcf46d13ceee8c2606834a897eba153a654f0092c1d41c8737723739a1405f1c`.
- `tests/test_instruction_architecture.py`: one added test class with ten tests and its module constants.
- `docs/engineering/instruction-architecture/evidence/WO-IAR-012-verification.md`: this file.

No managed fragment tracked block, managed policy module, packaged template, `CLAUDE.md`, `.engineering-harness.lock`, seed, or CLI behavior was touched, and no formatter or linter gate was introduced.
