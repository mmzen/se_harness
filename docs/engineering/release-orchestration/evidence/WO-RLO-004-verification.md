# WO-RLO-004 implementation evidence

> Implementation handoff evidence. This file records implementation observations and the separately authorized work-order completion only. It is not a verification decision, release decision, publication authorization, or external-action authority.

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
- Operational candidate commit: `4fec0d78c1c6a792104506d3fa3c7778bdcd3792`
- Review branch: `proposal/issue-110-build-recipe-01a02460`
- Pull request: `https://github.com/mmzen/se_harness/pull/133`
- Hosted candidate-evidence run: `https://github.com/mmzen/se_harness/actions/runs/32729113623` (`success`, exact head `4fec0d78c1c6a792104506d3fa3c7778bdcd3792`)

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

Exact candidate `4fec0d78c1c6a792104506d3fa3c7778bdcd3792` ran 604 local tests in 372.684 seconds: 586 passed, 12 skipped, 5 failed, and 1 errored. Three failures are existing CRLF-sensitive comparisons in this Windows checkout. The other three results are caused by the sandbox-required `GIT_CONFIG_*` safe-directory environment being intentionally rejected by predecessor-publication isolation tests. The exact candidate's hosted clean-checkout candidate-source regression, package installation, disposable consumer, Linux and Windows governance migration, deterministic integration package, and cross-platform package verification all pass in run `32729113623`; no assertion was weakened.

Hosted run `32729113623` completed successfully with candidate-source job `97437057352`, candidate-package job `97437337806`, Linux migration job `97437486001`, Windows migration job `97437485875`, deterministic-package job `97437803507`, Linux package-verification job `97437862068`, Windows package-verification job `97437861878`, and retained-package job `97438018174`. Each job is bound by the run metadata to exact head `4fec0d78c1c6a792104506d3fa3c7778bdcd3792`.

## Formal handoff binding

```text
artifact: WO-RLO-004
checkpoint: handoff
formal_snapshot_sha256: 479ad9d768933fa9505597cf962bf985b03fec623573a2922f5bd959c72f49aa
```

The declared complete change set contains the 28 paths in operational candidate `4fec0d78c1c6a792104506d3fa3c7778bdcd3792`; the later evidence update changes only the already-declared evidence path. All 28 paths are within the authorized 31-path execution scope. Completeness is an explicit caller assertion rather than trusted proof of absent hidden changes.

## Required bounded scope correction discovered during implementation

The hash-bound integrity feature merged before this work treats every previously unseen `*_sha256` front-matter field as undeclared. A future schema-2 RLS will therefore make `build_recipe_sha256` fail the portable integrity inventory even though repository distribution policy validates the referenced recipe. Omitting or renaming the field would violate `REQ-RLO-013`; teaching portable code to interpret the recipe would violate the repository-policy boundary.

The authorized narrow correction adds only these paths to `WO-RLO-004.execution_scope`:

- `se_harness/hash_bound_classes.json` — declare only the field name `build_recipe_sha256` as a repository-policy-bound digest outside portable hash-class interpretation, matching the existing treatment of `wheel_sha256`, `sdist_sha256`, `checksums_sha256`, and `source_manifest_sha256`; no recipe path, parser, command, or build behavior enters the package;
- `tests/test_hash_bound_integrity.py` — prove that the exact field is inventoried while unknown digest fields still fail; and
- `tests/test_context_routing_retirement.py` — add only `WO-RLO-004.md` to the exact permitted historical/path-reference inventory.

The scope now contains thirty-one paths. The declaration inventories only the exact field name and assigns its interpretation to repository policy; it adds no recipe path, parser, command, or build behavior to the portable package. The retirement inventory names only this work order, and the existing unknown-digest rejection remains intact. All 24 focused correction tests pass.

## Pending exact and hosted evidence

This host has neither Docker nor Podman, so the real digest-pinned Linux producer cannot be launched locally. The interpreter correctly has no native-host fallback. Standard exact-candidate hosted qualification passed, but the new pre-release replay requires a future schema-2 ready RLS and already accepted hashes by design. Consequently these release-stage observations remain pending a separately authorized future release dispatch:

- two real clean producer builds and their wheel/sdist hashes;
- hosted ready-RLS replay URL and result digest;
- schema-2 production-path hosted observation.

The engineering owner explicitly accepted the completed handoff, and the released evaluator atomically transitioned only `WO-RLO-004` from `in_progress` to `implemented`. The future release-stage observations above remain mandatory for the concrete schema-2 RLS they assess; they do not create a release or publication authority here. No verification claim is made by this work-order transition.

## Authority and unchanged state

The authorized operational candidate commit, branch push, pull request, ordinary hosted PR qualification, and explicit `WO-RLO-004` completion transition were performed. No VREC or RLS preparation/transition, release, tag, publication, deployment, maintenance mutation, external-policy change, or root-evaluator upgrade was performed at this stage. `RLS-SEH-012`, v0.6.0 distribution bytes, rejected history, and portable managed files remain unchanged.
