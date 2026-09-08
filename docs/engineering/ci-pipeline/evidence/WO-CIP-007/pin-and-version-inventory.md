# WO-CIP-007: pin and version inventory before and after

`SPEC-CIP-003` `CIP-ONE-005`, `CIP-ONE-006` and `CIP-ONE-007`;
`VER-CIP-003`'s "versions and pins" row. The eight repository-owned workflows
only: the managed template `.github/workflows/engineering-harness.yml` is
`SPEC-DST-027`'s and is excluded from every figure here.

## How the figures are read

    git grep -nE "^\s+(- )?uses: " <ref> -- .github/workflows | grep -v engineering-harness
    git grep -nE "python-version|PYTHON_VERSION" <ref> -- .github/workflows | grep -v engineering-harness

Each `uses:` line is classified as

- **local** — `uses: ./.github/workflows/…`, a reusable workflow in this
  repository, which takes no digest;
- **pin form** — `@` a 40-character commit digest followed by `# vX.Y.Z`, the
  exact tag the digest was peeled from (`SPEC-CIP-003`, Terms);
- **digest, inexact comment** — a full digest whose comment is a bare major
  (`# v4`) or carries extra words;
- **floating** — a tag reference such as `@v4`.

## Pins before, at `fae52e1b6c570bf1cdba892728029fa38416c947`

`main` has since moved to `560973cf12452d1c91b5a198c6a74d11af383d49` and this
branch merged it in. The before-figures hold at both refs:
`git diff --stat fae52e1b 560973cf -- .github/` is empty, so no line counted
here moved on `main`.

| Workflow | pin form | digest, inexact comment | floating | local |
| --- | --- | --- | --- | --- |
| `candidate-evidence.yml` | 11 | 0 | 12 | 0 |
| `pages-publication.yml` | 5 | 0 | 0 | 0 |
| `predecessor-evaluator-assessment.yml` | 0 | 0 | 3 | 0 |
| `publication-rehearsal.yml` | 2 | 0 | 0 | 2 |
| `publish-dashboard-pages.yml` | 0 | 0 | 0 | 1 |
| `publish-pypi.yml` | 6 | 6 | 0 | 2 |
| `release-candidate-replay.yml` | 2 | 1 | 0 | 0 |
| `release-qualification.yml` | 2 | 2 | 0 | 0 |
| **total** | **28** | **9** | **15** | **5** |

52 lines name a public action: 28 in the pin form, 24 not. Three generations
are present at once, as `REQ-CIP-009`'s source records.

The floating lines: `actions/checkout@v4` (`candidate-evidence.yml` 44, 128,
291; `predecessor-evaluator-assessment.yml` 32), `actions/setup-python@v5`
(`candidate-evidence.yml` 48, 132, 295; `predecessor-evaluator-assessment.yml`
36), `actions/upload-artifact@v4` (`candidate-evidence.yml` 102, 110, 262, 373;
`predecessor-evaluator-assessment.yml` 151), `actions/download-artifact@v4`
(`candidate-evidence.yml` 136, 316).

The inexact comments: `# v4` on `actions/upload-artifact@ea165f8d…`
(`publish-pypi.yml` 133, 153, 494; `release-candidate-replay.yml` 69;
`release-qualification.yml` 182, 194), `# v5` on
`actions/download-artifact@634f93cb…` (`publish-pypi.yml` 198, 409), and
`# v1.14.2 peeled commit` on `pypa/gh-action-pypi-publish@dc37677b…`
(`publish-pypi.yml` 369).

## Digests chosen, each verified against the action's tag

`SPEC-CIP-003` leaves the digests to the work order: the newest release of the
major each file already uses. Every digest below was resolved from the tag on
2026-09-08 through `GET /repos/{action}/git/ref/tags/{tag}`, peeling the
annotated tag object to its commit.

| Action | Tag | Commit digest | Used by |
| --- | --- | --- | --- |
| `actions/checkout` | v4.4.0 | `11d5960a326750d5838078e36cf38b85af677262` | `candidate-evidence.yml`, `predecessor-evaluator-assessment.yml` |
| `actions/checkout` | v7.0.1 | `3d3c42e5aac5ba805825da76410c181273ba90b1` | the five release-path workflows (unchanged) |
| `actions/setup-python` | v5.6.0 | `a26af69be951a213d495a4c3e4e4022e16d87065` | `candidate-evidence.yml`, `predecessor-evaluator-assessment.yml` |
| `actions/setup-python` | v7.0.0 | `5fda3b95a4ea91299a34e894583c3862153e4b97` | the five release-path workflows (unchanged) |
| `actions/upload-artifact` | v4.6.2 | `ea165f8d65b6e75b540449e92b4886f43607fa02` | five workflows |
| `actions/download-artifact` | v4.3.0 | `d3f86a106a0bac45b974a628896c90dbdf5c8093` | `candidate-evidence.yml` |
| `actions/download-artifact` | v5.0.0 | `634f93cb2916e3fdff6788551b99b062d0335ce0` | `publish-pypi.yml` |
| `actions/cache` | v4.2.3 | `5a3ec84eff668545956fd18022155c47e93e2684` | `candidate-evidence.yml` (already in the pin form; unchanged) |
| `actions/configure-pages` | v6.0.0 | `45bfe0192ca1faeb007ade9deae92b16b8254a0d` | `pages-publication.yml` (unchanged) |
| `actions/upload-pages-artifact` | v5.0.0 | `fc324d3547104276b827a68afc52ff2a11cc49c9` | `pages-publication.yml` (unchanged) |
| `actions/deploy-pages` | v5.0.0 | `cd2ce8fcbc39b97be8ca5fce6e763baed58fa128` | `pages-publication.yml` (unchanged) |
| `pypa/gh-action-pypi-publish` | v1.14.2 | `dc37677b2e1c63e2034f94d8a5b11f265b73ba33` | `publish-pypi.yml` |

Every digest already present in a pin-form line verified against the tag its
comment claims. One existing pin moves: `actions/checkout` in
`candidate-evidence.yml` was `11bd71901bbe…` (v4.2.2) on three lines and
floating `@v4` on three others; all six now name v4.4.0, the newest release of
the major that file uses, so the file states one digest for one action.

## Python versions before

| Workflow | `python-version` values |
| --- | --- |
| `candidate-evidence.yml` | `"3.11"` ×6 |
| `pages-publication.yml` | `"3.11"` |
| `predecessor-evaluator-assessment.yml` | `"3.11"` |
| `publication-rehearsal.yml` | `"3.11"` |
| `publish-pypi.yml` | `PYTHON_VERSION: "3.11"` once, `${{ env.PYTHON_VERSION }}` ×3 |
| `release-candidate-replay.yml` | `"3.11.9"` |
| `release-qualification.yml` | `"3.11.9"` |

Two distinct strings, `"3.11"` and `"3.11.9"`. `CIP-ONE-005` requires one.

## Integration build-tool versions before

`candidate-evidence.yml`, job `integration-package-build`: `build==1.2.2.post1
setuptools==75.8.0 wheel==0.45.1` in the install step (line 423) and
`--expect-build-version 1.2.2.post1`, `--expect-setuptools-version 75.8.0`,
`--expect-wheel-version 0.45.1` in the build step (lines 439 to 441). Each
version is written twice; `CIP-ONE-007` requires one `env` block read by both.

## After, on the branch `wo/cip-007-pipeline-hygiene`

| Workflow | pin form | digest, inexact comment | floating | local |
| --- | --- | --- | --- | --- |
| `candidate-evidence.yml` | 23 | 0 | 0 | 0 |
| `pages-publication.yml` | 5 | 0 | 0 | 0 |
| `predecessor-evaluator-assessment.yml` | 3 | 0 | 0 | 0 |
| `publication-rehearsal.yml` | 2 | 0 | 0 | 2 |
| `publish-dashboard-pages.yml` | 0 | 0 | 0 | 1 |
| `publish-pypi.yml` | 12 | 0 | 0 | 2 |
| `release-candidate-replay.yml` | 3 | 0 | 0 | 0 |
| `release-qualification.yml` | 4 | 0 | 0 | 0 |
| **total** | **52** | **0** | **0** | **5** |

52 of 52, from 28. The inexact-comment column and the floating column are
empty, and the five local `uses:` lines are unchanged. The managed
`engineering-harness.yml` still carries three floating lines; it is
`SPEC-DST-027`'s and no rule of `SPEC-CIP-003` reads it.

Within one file, one action names one digest — asserted by
`test_every_public_action_takes_the_pin_form`. Across files the majors still
differ by design: the two candidate lanes are on `actions/checkout` v4.4.0 and
`actions/setup-python` v5.6.0, the release-path files on v7.0.1 and v7.0.0,
which is what `SPEC-CIP-003`'s "Not decided here" leaves to this work order
("the newest release of the major each file already uses").

### Python versions after

| Workflow | `python-version` values |
| --- | --- |
| `candidate-evidence.yml` | `"3.11"` ×6 |
| `pages-publication.yml` | `"3.11"` |
| `predecessor-evaluator-assessment.yml` | `"3.11"` |
| `publication-rehearsal.yml` | `"3.11"` |
| `publish-pypi.yml` | `PYTHON_VERSION: "3.11"` once, `${{ env.PYTHON_VERSION }}` ×3 |
| `release-candidate-replay.yml` | `"3.11"` |
| `release-qualification.yml` | `"3.11"` |

One string. `"3.11.9"` is gone from both files that carried it; the only
other spelling is `publish-pypi.yml`'s `PYTHON_VERSION`, which `CIP-ONE-005`
permits and `test_one_python_version_string` confirms is the same string.
Nothing else in the repository pins a patch-level CPython for these lanes:
the recipe's own toolchain is `release/build-toolchain.lock`, which is not a
workflow and is out of scope.

### Integration build-tool versions after

`candidate-evidence.yml`, job `integration-package-build`, one `env` block:

    INTEGRATION_BUILD_VERSION: 1.2.2.post1
    INTEGRATION_SETUPTOOLS_VERSION: 75.8.0
    INTEGRATION_WHEEL_VERSION: 0.45.1

The install step reads `"build==$INTEGRATION_BUILD_VERSION"`,
`"setuptools==$INTEGRATION_SETUPTOOLS_VERSION"` and
`"wheel==$INTEGRATION_WHEEL_VERSION"` (it gained `shell: bash` so the
expansion is defined on both runners; the job runs on Linux only), and the
three `--expect-*-version` arguments read the same variables. Each literal
appears once in the job, asserted by
`test_the_integration_build_toolchain_is_stated_once` (three occurrences of
each variable name: the declaration, the install, the expectation).

`0.45.1` is a `wheel` version, not an evaluator version: `CIP-PRE` 3's grep
gate refuses the se_harness version set, and
`test_no_predecessor_literal_remains_in_the_repository_owned_workflows`
still passes with these three lines present.
