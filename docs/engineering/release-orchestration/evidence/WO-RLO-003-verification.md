# WO-RLO-003 implementation evidence

## Authority and scope

On 2026-08-19 the accountable repository owner approved the complete RLO-003 packet and authorized `WO-RLO-003` through the statement `go implement`. The same owner explicitly constrained the change to the `se_harness` repository and prohibited modification of the SE Harness governance tool.

This evidence assesses the completed working-tree implementation only. It is retained engineering evidence, not a commit-bound VREC, assurance decision, release decision, branch operation, publication, deployment, or external configuration change.

## Implemented behavior

- Added repository-owned `.github/scripts/reconcile_maintenance_branch.py` using only the Python standard library and the existing job-scoped GitHub token.
- Derived exactly `release/MAJOR.MINOR` from the canonical resolved `MAJOR.MINOR.PATCH` version; no operator-controlled branch input exists.
- Added the reconciliation step after exact tag and non-draft GitHub Release verification in `.github/workflows/publish-pypi.yml`.
- Created an absent ref at the exact released candidate and re-read the postcondition.
- Accepted an existing ref without mutation only when its tip equals or descends from the candidate.
- Re-read and assessed a ref after either GitHub `409` or `422` create conflict, permitting only a compatible concurrent creator.
- Failed closed on behind, diverged, malformed, inaccessible, missing-after-create, or otherwise unknown state. No update, force, delete, merge, rewind, or repair API exists in the helper.
- Exposed the branch and `created`/`existing` state as GitHub-job outputs, the human workflow summary, and fields inside the existing GitHub stage of the machine-readable release result.
- Kept downstream PyPI and Pages jobs dependent on successful `github_release`, so reconciliation refusal blocks promotion and remains replayable after prior exact immutable writes.
- Updated repository context, release-domain index, and contributor guidance to distinguish this local policy from portable SE Harness.

## State and failure matrix

| Observed state | Result | Mutation |
|---|---|---|
| canonical line absent | create at candidate, re-read, report `created` | one create request |
| tip equals candidate | report `existing` | none |
| tip descends from candidate | report `existing` | none |
| create returns `409` or `422`, ref now compatible | refetch, prove containment, report `existing` | only the original create attempt |
| tip behind or diverged | fail with candidate/tip/comparison | none |
| ref malformed or non-commit | fail | none |
| lookup, comparison, create, or postcondition inaccessible/invalid | fail | no update/delete/repair |

The fixture suite validates the full request sequence and rejects every unexpected API call. Existing-ref cases contain only GET requests. Creation payload is structurally generated as `{ref, sha}` and selects the exact candidate.

## Repository/product boundary

The final changed-path audit returned no path under:

- `se_harness/`
- `templates/repository/standard/`
- `.engineering-harness.toml`
- `.engineering-harness.lock`
- `.github/workflows/engineering-harness.yml`

Doctor independently reported every managed portable file unchanged and matching its distribution. No `harnessctl` command, package module, artifact schema, managed validator, standard template, consumer CI behavior, installation, adoption, upgrade, or governor-reconciliation behavior changed. The only executable surfaces are the repository-owned release workflow, one `.github/scripts` helper, and repository tests.

## Verification results

| Check | Result |
|---|---|
| `python -m unittest discover -s tests -p "test_*.py"` on Python 3.14.6 | PASS — 262 tests, 3 expected skips |
| same complete suite on Python 3.11.9 | PASS — 262 tests, 3 expected skips |
| focused maintenance/release/PyPI suite on Python 3.11.9 | PASS — 35 tests |
| `python -m py_compile .github/scripts/reconcile_maintenance_branch.py` | PASS |
| available PyYAML parse of `.github/workflows/publish-pypi.yml` | PASS |
| `python scripts/validate_engineering_artifacts.py --root .` | PASS — 484 artifacts, structure/governance/policy E0/W0; unchanged maintenance E0/W44 |
| `python scripts/validate_release_distributions.py --root .` | PASS — zero currently distribution-bearing records |
| `python -m se_harness doctor .` | PASS — managed files and lock unchanged; existing location warnings only |
| start and review preflight for `WO-RLO-003` | PASS |
| `git diff --check` | PASS; Git reported only normal working-copy LF/CRLF notices |

The full regression suites include installer, managed-integrity, self-hosting, release-resolution, deterministic distribution, GitHub/PyPI/Pages state, CLI, dashboard, preflight, inspection, and artifact-graph tests. The new focused suite covers canonical derivation, repository restriction, absent creation, exact replay, descendant replay, behind/diverged refusal, `409`/`422` concurrent creation, malformed/non-commit/API failures, workflow ordering, one-input preservation, outputs, and promotion dependency.

## External contract review

The implementation was checked against GitHub's official REST documentation for [Git references](https://docs.github.com/en/rest/git/refs) and [commit comparison](https://docs.github.com/en/rest/commits/commits). The documented `200`/`404` reference lookup, `201` creation, `409`/`422` refusal possibilities, contents permission, fully qualified ref body, and `BASE...HEAD` comparison are reflected in the bounded state handling. The helper pins the established GitHub API version header already compatible with this repository's automation and uses a fixed HTTPS API origin.

## Security and resilience observations

- The helper is loaded from trusted `main` by the existing contents-write job; candidate source and distributions are not executed there.
- Version, repository, commit, ref payload, comparison status, response JSON, and response size are validated before use.
- The API token is read only from `GH_TOKEN`, placed only in the Authorization header, and never serialized or logged.
- Responses are bounded to 1 MiB and requests use a 30-second timeout; there is no polling or retry loop.
- A failed reconciliation may follow a successfully published immutable GitHub Release, matching the existing partial-state model. A later workflow replay verifies the immutable state and safely retries reconciliation.
- The workflow still has exactly one required input and no new action, secret, PAT, environment, dependency, or permission scope.

## Residual uncertainty

Local tests do not prove future GitHub availability, repository branch-rule configuration, protected-environment decisions, or external administrator policy. The first separately authorized release after merge provides operational confirmation. Because current historical maintenance branches use per-patch names, the workflow will establish the first canonical `release/MAJOR.MINOR` line on its next authorized run; it deliberately does not rename, delete, or repair legacy refs.

## Actions explicitly not performed

No commit, push, pull request, VREC, assurance transition, release record, production maintenance branch, tag, GitHub Release, PyPI publication, Pages deployment, protected-environment approval, governor promotion, branch-protection change, legacy-ref cleanup, or other external mutation was performed under implementation authority.
