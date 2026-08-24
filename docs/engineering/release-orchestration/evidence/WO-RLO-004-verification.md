# WO-RLO-004 implementation evidence

> In-progress technical evidence. This file records implementation observations only. It is not a verification decision, release decision, hosted dispatch, publication authorization, or lifecycle transition.

## Bound build identity

- Recipe schema: `se-harness-release-build-recipe/v1`
- Candidate path: `release/build-recipe.json`
- Current canonical recipe SHA-256: `0c3f368c45f8f41177d84f695ec743d56794bb33604b4834ada369d92362acdc`
- Toolchain path: `release/build-toolchain.lock`
- Toolchain SHA-256: `826d70d4ec8710d363861b7604ffb3f82fa8a981c15bfb9d283c9f2b353eaba3`
- Producer: `python@sha256:2856e6af199e8128161abd320575eb9b341f3b76f017b5d0c9cd364f60d8a050`, `linux/amd64`
- Runtime: `CPython 3.11.9`, 64-bit
- Bundle and distribution: `se-harness-release-bundle/v2` and repository distribution schema 2
- Replay result: `se-harness-release-build-replay/v1`

The exact locked inventory is:

| Distribution | Version | Wheel SHA-256 |
|---|---:|---|
| build | 1.3.0 | `7145f0b5061ba90a1500d60bd1b13ca0a8a4cebdd0cc16ed8adf1c0e739f43b4` |
| colorama | 0.4.6 | `4f1d9991f5acc0ca119f9d443620b77f9d6b33703e51011c16baf57afb285fc6` |
| packaging | 26.3 | `d7193f7c8e4e93f444fde0262bf90af30e16fa0ad0ad44cb553c87339b23cd1c` |
| pip | 24.0 | `ba0d021a166865d2265246961bec0152ff124de910c5cc39f1156ce3fa7c69dc` |
| pyproject-hooks | 1.2.0 | `9e5c6bfa8dcc30091c74b0cf803c81fdd29d94f01992a7707bc97babb1141913` |
| setuptools | 84.0.0 | `51a52592b3b99e102b609654876bd65f19f999935166d1352678931132b0c670` |
| wheel | 0.48.0 | `3217dcc807155e45db462d7ef2431f5ddda0d7273b700d05a67b271ceb1287ab` |

The recipe inherits no environment variables. It fixes `HOME`, `LANG`, `LC_ALL`, `PATH`, `PYTHONDONTWRITEBYTECODE`, `PYTHONHASHSEED`, and `TZ`, and derives only `SOURCE_DATE_EPOCH` from the exact candidate commit. The interpreter adds only the isolated toolchain path required to run the declared tools. All three recipe commands are closed argument arrays; recipe text is never evaluated by a shell.

## Baseline defect and corrected identity flow

Before this change, the RLS bound output hashes, the source epoch, and source-tree identity, while `publish-pypi.yml` separately chose Windows 2022, setup-Python 3.11.9, three direct packages, host state, build commands, and normalization commands. No single retained object answered “which complete producer created these accepted bytes?”

The corrected forward path is:

1. the exact candidate tree binds the complete canonical recipe and lock;
2. the repository interpreter exports that candidate twice and uses two fresh digest-pinned producers;
3. bundle schema 2 binds the candidate, source, recipe, output names, and hashes;
4. a ready RLS atomically binds the same schema-2 identity;
5. the read-only hosted lane replays the already accepted hashes before release approval; and
6. schema-2 publication qualification calls the same interpreter before any privileged job.

Already released schema-1 history is unchanged and valid only through the labeled legacy path. A new ready schema-1 record is refused.

## Local verification performed so far

The following focused suites pass in this checkout:

- `python -m unittest tests.test_release_build.BuildRecipeSchemaTests tests.test_release_build.ReplayBuildTests tests.test_release_build.ReplayWorkflowTests -v` — 8 tests passed.
- `python -m unittest tests.test_release_orchestration -v` — 24 tests passed after adding schema-2 binding, mismatch, atomicity, and schema-1-history coverage.
- `python -m unittest tests.test_maintenance_branch tests.test_pypi_publishing tests.test_release_orchestration.ReleaseWorkflowPolicyTests tests.test_instruction_architecture.OwnerInstructionRegionTests -v` — 32 tests passed.
- Both changed workflows parse as YAML.
- The changed Python entry points compile.
- Current and released-0.6.0 graph validation each pass with 760 artifacts, 0 errors, and the same 50 pre-existing maintenance warnings.
- `python scripts/validate_release_distributions.py --root .` passes with the one historical distribution-bearing record.
- Historical `RLS-SEH-012` resolves through release plan schema 2 with `distribution_schema = 1` and null recipe fields, preserving its exact candidate and distribution hashes.
- `python scripts/check_portable_release_surface.py --repository .` passes.
- The combined recipe, distribution, integrity, retired-context, publication, maintenance, and owner-instruction focus run passes 82 tests.
- The bounded scope correction's 24 integrity and retired-context tests pass, including exact `build_recipe_sha256` inventory and continued rejection of an unknown digest field.
- Released-0.6.0 `doctor` exits 0 with only the existing historical-location warnings; released-0.6.0 graph validation passes with 760 artifacts, 0 errors, and the same 50 maintenance warnings.
- Review preflight for `WO-RLO-004` passes under the released-0.6.0 evaluator with commit-bound verification still required.
- Python compilation, both workflow YAML documents, release-distribution validation, and portable-release-surface validation pass after the scope amendment.
- The working diff has 28 changed paths, all contained by the authorized 31-path execution scope; `git diff --check` reports no errors.

Failure coverage currently includes non-canonical and duplicate JSON, mutable image, environment inheritance, free-form commands, lock-hash and inventory drift, unsafe bundle identity, recipe hash drift, partial RLS state, atomic replacement failure, new-ready schema 1, expected-output mismatch, workflow credential/permission drift, and privileged-job candidate-execution separation.

The complete historical `tests.test_release_build` suite was restored and extended rather than replaced. Its ephemeral-wheel byte comparison fails in this Windows worktree because an existing managed template is checked out as CRLF while `harnessctl init` writes canonical LF (`git ls-files --eol` reports `i/lf w/crlf` for that pre-existing path). That path is outside `WO-RLO-004` scope and is unchanged. The same test is expected to run with LF in hosted Linux qualification; no assertion was weakened.

The complete local discovery ran 598 tests in 336.956 seconds: 560 passed, 11 skipped, 8 failed, and 19 errored. Twenty-six failures/errors are explained by the sandbox-owned worktree's pre-existing CRLF checkout and Git dubious-ownership refusal; focused runs with the required Git safe-directory context pass the changed behavior. The remaining failure exposed a real scope-inventory effect: the approved `WO-RLO-004` front matter necessarily names the retired repository-context path, while `tests/test_context_routing_retirement.py` keeps an exact list of records allowed to name it. The subsequent bounded scope amendment authorized the exact inventory correction.

## Required bounded scope correction discovered during implementation

The hash-bound integrity feature merged before this work treats every previously unseen `*_sha256` front-matter field as undeclared. A future schema-2 RLS will therefore make `build_recipe_sha256` fail the portable integrity inventory even though repository distribution policy validates the referenced recipe. Omitting or renaming the field would violate `REQ-RLO-013`; teaching portable code to interpret the recipe would violate the repository-policy boundary.

The authorized narrow correction adds only these paths to `WO-RLO-004.execution_scope`:

- `se_harness/hash_bound_classes.json` — declare only the field name `build_recipe_sha256` as a repository-policy-bound digest outside portable hash-class interpretation, matching the existing treatment of `wheel_sha256`, `sdist_sha256`, `checksums_sha256`, and `source_manifest_sha256`; no recipe path, parser, command, or build behavior enters the package;
- `tests/test_hash_bound_integrity.py` — prove that the exact field is inventoried while unknown digest fields still fail; and
- `tests/test_context_routing_retirement.py` — add only `WO-RLO-004.md` to the exact permitted historical/path-reference inventory.

The scope now contains thirty-one paths. The declaration inventories only the exact field name and assigns its interpretation to repository policy; it adds no recipe path, parser, command, or build behavior to the portable package. The retirement inventory names only this work order, and the existing unknown-digest rejection remains intact. All 24 focused correction tests pass.

## Pending exact and hosted evidence

This host has neither Docker nor Podman, so the real digest-pinned Linux producer cannot be launched locally. The interpreter correctly has no native-host fallback. Consequently these required observations remain pending an exact candidate commit and separately authorized hosted dispatch:

- two real clean producer builds and their wheel/sdist hashes;
- exact-commit complete-candidate qualification;
- hosted ready-RLS replay URL and result digest;
- schema-2 production-path hosted observation; and
- final exact-commit complete unit and package/consumer replay results.

`WO-RLO-004` therefore remains `in_progress`. No implementation-completion transition or verification claim is made.

## Authority and unchanged state

No candidate commit, push, pull request, hosted dispatch, VREC or RLS preparation/transition, release, tag, publication, deployment, maintenance mutation, credential use, external-policy change, or root-evaluator upgrade was performed while creating this in-progress evidence. `RLS-SEH-012`, v0.6.0 distribution bytes, rejected history, and portable managed files remain unchanged.
