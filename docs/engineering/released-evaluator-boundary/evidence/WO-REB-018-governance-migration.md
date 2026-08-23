# WO-REB-018 governance migration rehearsal evidence

## Authority and current state

Issue #101 was implemented locally under approved `REQ-REB-016`, `REQ-REB-017`, `SPEC-REB-008`, `ARCH-REB-007`, `ADR-REB-007`, `VER-REB-007`, and `WO-REB-018`.

`WO-REB-018` remains `in_progress`. This evidence is not a candidate commit, verification decision, release decision, publication authorization, or root-evaluator adoption. No commit, push, hosted dispatch, VREC/RLS preparation or transition, tag, publication, deployment, maintenance mutation, credential use, external-policy change, or operational root-evaluator upgrade was performed.

The implementation worktree is based on Git commit `6582ebfd03c773324ea0b0dd86cb975fb19a15ab` on local branch `proposal/rca-060-01-governor-migration`. The implementation and this evidence are uncommitted, so there is not yet an exact candidate commit identity.

## Delivered contract and executable surface

The implementation adds:

- packaged contract `se-harness-governance-migration-v1`;
- canonical result `se-harness-governance-migration-result-v1`;
- strict contract/scenario loader and validator;
- no-network, evidence-only `harnessctl rehearse-migration` runner;
- separately installed predecessor and successor runtime probes;
- a closed nine-stage migration catalog with typed roles, views, decisions, adapters, effects, and fail-stop behavior;
- permanent historical `0.5.0` to `0.6.0` and version-neutral synthetic scenarios;
- candidate-source, wheel-surface, CLI, adversarial, determinism, and workflow tests;
- an unprivileged Windows/Linux candidate-evidence matrix and semantic-digest reconciliation job; and
- operator, CLI, developer, and domain documentation.

The source identities used by local qualification are:

| Item | SHA-256 |
| --- | --- |
| `se_harness/governance_migration_contract.json` | `7542dfb3dd495fb78ffd5de62c66e25886f067a00509ad933ad02184820710ff` |
| `se_harness/governance_migration_contract.py` | `bb87c3d7d713ce2da3fa5aea287714a37df5017f43057f1fa17c7d794716e826` |
| `se_harness/governance_migration.py` | `74fc4e2b728a3f8ae69c0b10d008afd508570c5d6e9eddb140dd941fcb2091a4` |
| historical scenario | `393f639eb06fdec17a31386c5fc94f526cceba2e0efc95cbde6e1077f99b8324` |
| historical scenario fixture | `daf7ca33b6fe75246d9a14c5e1193f916c4da8ba4a0a100eae2f23a351c2517c` |
| synthetic scenario | `af2101d95784babdd3afaaccad16946ba04abbce866643c7e6cb4413ecb33daf` |
| rejection decision fixture | `e785b11e591610600e8b8077d5a8f82cbd51e7c5067f4f714776fc4b9c81281f` |
| adoption decision fixture | `91b828771b0fc0dd8895aa87a23062efe308acef69f40e8122a31aca16d7d21e` |

All six declared compatibility adapters bind the exact runner hash above. Unknown fields, duplicate JSON keys, noncanonical UTF-8/LF bytes, reordered stages, unregistered roles/views/adapters/decisions, undeclared effects, and changed adapter bytes are refused.

## Exact local package rehearsal

The final disposable build and rehearsal root is outside the operational checkout:

`../work/wo-reb-018-final-d97670e9898f464a912abd37f92c14b4`

The package inputs and installed runtime identities were:

| Role | Version and archive | Archive SHA-256 | Installed package-tree SHA-256 |
| --- | --- | --- | --- |
| released predecessor | `se_harness-0.5.0-py3-none-any.whl` | `974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f` | `6233a429759c6600d033d947eb72fce4403bd742b57d367ac9c7e2709934b4bc` |
| non-promotable successor | `se_harness-0.6.0-py3-none-any.whl` | `60d555bcf54005859c3b03b1f536857824222c5117ce560272e25575e26b8269` | `b47ce208a81361550e575ffaa1bb4c3a843a9f183c8dff98d192970e94ba6341` |

Both environments used isolated Python 3.14.6 virtual environments outside the checkout. The released predecessor archive was the retained exact public 0.5.0 wheel. The successor wheel was rebuilt from the final reviewed source and template tree. It is disposable qualification input, not a release distribution.

The installed successor contract SHA-256 was exactly `7542dfb3dd495fb78ffd5de62c66e25886f067a00509ad933ad02184820710ff`, equal to the source contract. The successor runtime recorded payload SHA-256 `9e775944035774f6e62613e0a93e40b9a9c4ce255309d8cadf65b7f04e77e1c1`.

The historical scenario ran twice from the installed packages. Both runs passed and produced the same normalized semantic SHA-256:

`34f478dba98fe29873ffa8b3e64afecd9d6517abd48fef506657d487d4d5e9c0`

The normalized digest excludes elapsed time and platform-specific interpreter facts, while the retained result still records those factual values. This proves deterministic local replay; Windows/Linux agreement still requires the hosted matrix described below.

## Nine-stage result

| Stage | Technical actor and view | Attributed authority effect | Result |
| --- | --- | --- | --- |
| `prepare` | predecessor-compatible adapter / preparation view | none | pass |
| `validate-complete` | successor / complete graph | none | pass |
| `reject` | lifecycle simulator / exact rejection fixture | `RLS-MIG-001` becomes rejected only in the disposable graph | pass |
| `replace` | predecessor-compatible adapter / preparation view | none; creates distinct `RLS-MIG-002` | pass |
| `assess` | compatibility adapter / assessment view | none | pass |
| `release-plan` | release planner / selected corrected release | none; plan only | pass |
| `publish-plan` | publication planner / predecessor publication view | none; plan only | pass |
| `render` | renderer / predecessor publication view | none; disposable rendering only | pass |
| `adopt` | upgrade adapter / standard root | selects the successor only in the disposable root after the exact adoption fixture | pass |

The initial complete-successor validation reports `migration-required` with structured `missing-evaluator-evidence` and `unsupported-release-record-schema` codes. The exact rejection fixture then rejects `RLS-MIG-001`. Replacement creates distinct `RLS-MIG-002` and preserves rejected-history SHA-256 `7e0684b950ee5b277512cbf8d38a4c3ac5a23c6e3ec58c180da18bd92e6b9c10` unchanged.

Assessment reports two different facts instead of treating a compatibility pass as a complete pass:

- the corrected complete successor graph passes with graph SHA-256 `c836461c73f4f7e3bd449ce073e7ddfcd3301a7fdb0b65f6fcfcb7740823a8c1`;
- the predecessor-compatible assessment view passes with view SHA-256 `b3a1516c575aa3787a4a75c82e59bad9f1558aee14d00745d1d35cb2d4d4bc52`; and
- predecessor validation of the unmodified complete graph is explicitly recorded as `refused-unsupported-rejected-state`.

Release and publication stages produced plans only. Render selected the corrected proposal. Disposable adoption proved exact rollback and no-op replay after a simulated immutable publication. No stage let the successor decide its own authority.

## Mutation and security evidence

Both exact-package rehearsals recorded operational source SHA-256 `00e5f5fee4cef46c7bc04dcb3f204a0f5a5313be16537dc52727fc31f0d0f29d` before and after. Git HEAD remained `6582ebfd03c773324ea0b0dd86cb975fb19a15ab`, and Git refs SHA-256 remained `5890d13817f8d1e6d3bf658e4c9bea25d15517c58dd28e9fc0012f6445b970d4`.

The retained result reports `false` for credential use, network, lifecycle transition, tag, release, publication, deployment, maintenance mutation, external-policy change, and operational root-evaluator upgrade. Runtime checks also proved separate environments, checkout exclusion, user-site isolation, and exact predecessor archive identity.

Focused adversarial tests inject a fault at each of the nine stages and prove the first fault is retained while every later stage is `not-run`. Additional cases cover tampered scenario bytes, reordered stages, role and decision substitution, undeclared authority effects, operational mutation, credential-bearing environments, shared runtimes, checkout imports, output collisions, and exact predecessor mismatch.

## Local verification

The following checks passed on Windows:

- governance-migration focused tests: 9 passed;
- release-orchestration focused tests: 22 passed;
- release build, PyPI, recovery, and standard-lifecycle focused tests: 31 passed;
- complete suite: 461 passed with 7 declared skips in 282.888 seconds;
- candidate-template graph: 679 artifacts, 0 errors, 50 maintenance warnings;
- exact released-0.5 predecessor view: 677 artifacts, 0 errors, 49 maintenance warnings;
- exact released-0.5 `doctor`: exit 0 with existing maintenance-location warnings only;
- exact released-0.5 `WO-REB-018` start preflight: ready, 0 diagnostics, status `in_progress`;
- released-distribution validation: pass with one distribution-bearing record;
- portable wheel surface: pass;
- installed/source contract parity: pass;
- public CLI parser/help and canonical JSON output: pass; and
- Git whitespace/diff checks: pass after retaining this evidence.

The separately locked managed-root 0.5 validator still reports the already known #103 boundary on the unmodified complete graph: `E009` for rejected `RLS-SEH-009`, plus `E010` for the duplicate 0.6.0 records `RLS-SEH-009` and `RLS-SEH-012`. The candidate validator accepts the complete graph. The exact released-0.5 preparation view removes only that previously governed incompatible pair and passes with zero errors. This evidence does not treat the root failure as a new implementation failure or change the root evaluator.

The candidate-source `doctor` and review preflight also correctly refuse to treat the unadopted 0.6.0 template as the operational root: they report the existing managed-root files and lock as different from the candidate distribution. The released-0.5 `doctor` is the authoritative operational check at this stage and passes on its exact predecessor view. Candidate complete-graph validation remains a separate claim and passes. This is the authority separation the rehearsal is intended to preserve, not a bypass or an inferred root upgrade.

## Hosted and commit-bound evidence still pending

The candidate workflow now defines an unprivileged Windows/Linux matrix that downloads and verifies the exact 0.5.0 public wheel, builds a non-promotable exact-successor wheel, runs the historical rehearsal twice, uploads results even on failure, and reconciles one cross-platform semantic digest. It has not been dispatched because push, credentials, and hosted execution are outside the current authorization.

Commit-bound verification is also pending because no candidate commit is authorized or present. Therefore:

- Windows local source/package qualification is complete;
- hosted Windows/Linux execution and cross-platform reconciliation are pending;
- an exact candidate commit identity is pending;
- `WO-REB-018` remains `in_progress`; and
- no VREC/RLS work has been prepared or transitioned.

## Changed paths under review

- `.gitattributes`
- `.github/workflows/candidate-evidence.yml`
- `docs/engineering/released-evaluator-boundary/README.md`
- `docs/engineering/released-evaluator-boundary/architecture/ARCH-REB-007.md`
- `docs/engineering/released-evaluator-boundary/architecture/adr/ADR-REB-007.md`
- `docs/engineering/released-evaluator-boundary/evidence/WO-REB-018-governance-migration.md`
- `docs/engineering/released-evaluator-boundary/requirements/REQ-REB-016.md`
- `docs/engineering/released-evaluator-boundary/requirements/REQ-REB-017.md`
- `docs/engineering/released-evaluator-boundary/specifications/SPEC-REB-008.md`
- `docs/engineering/released-evaluator-boundary/verification/VER-REB-007.md`
- `docs/engineering/released-evaluator-boundary/work-orders/WO-REB-018.md`
- `docs/notes/developing-se-harness.md`
- `docs/notes/evaluator-migration-rehearsal.md`
- `docs/notes/harnessctl-reference.md`
- `pyproject.toml`
- `scripts/check_portable_release_surface.py`
- `se_harness/cli.py`
- `se_harness/governance_migration.py`
- `se_harness/governance_migration_contract.json`
- `se_harness/governance_migration_contract.py`
- `templates/repository/standard/gitattributes.fragment`
- `tests/fixtures/governance_migration/historical-0.5.0-to-0.6.0.json`
- `tests/fixtures/governance_migration/synthetic-n-minus-1-to-n.json`
- `tests/test_governance_migration.py`
- `tests/test_release_orchestration.py`
- `tests/test_standard_repository_lifecycle.py`

## Next accountable decision

Review the 26-path local implementation and retained evidence. If accepted, a separate authorization can create one exact candidate commit; only after that identity exists can commit-bound local replay, push, hosted Windows/Linux reconciliation, and the later `WO-REB-018` completion decision occur.
