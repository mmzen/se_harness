# WO-REB-018 governance migration rehearsal evidence

## Authority and current state

Issue #101 was implemented locally under approved `REQ-REB-016`, `REQ-REB-017`, `SPEC-REB-008`, `ARCH-REB-007`, `ADR-REB-007`, `VER-REB-007`, and `WO-REB-018`.

`WO-REB-018` is now `implemented` after exact local, package, and hosted qualification. This evidence is not a verification decision, release decision, publication authorization, or root-evaluator adoption. Candidate commits, the dedicated branch push, read-only hosted inspection, and bounded Git credential use occurred under the repository owner's authorization. No VREC/RLS transition, tag, publication, deployment, maintenance mutation, external-policy change, or operational root-evaluator upgrade was performed.

The implementation began at `6582ebfd03c773324ea0b0dd86cb975fb19a15ab` on branch `proposal/rca-060-01-governor-migration`. Exact implementation commit `35f7afdbaff9dd9734a1b2e4b6f4147cc8d294a3` contains the reviewed feature plus the hosted-discovered semantic normalization correction. The later local governance commit containing this evidence update and the work-order transition does not alter the runner, contract, scenarios, tests, workflow, or package payload.

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
| `se_harness/governance_migration_contract.json` | `5819dbabeeea7d2dc538e67d2d53eb8290e5a192f499e6250ccbedc9d2a9b167` |
| `se_harness/governance_migration_contract.py` | `bb87c3d7d713ce2da3fa5aea287714a37df5017f43057f1fa17c7d794716e826` |
| `se_harness/governance_migration.py` | `bcdaf2078e4161b4f18749f48560d9f3045a6cbab10363da9c8ca154179c6231` |
| historical scenario | `393f639eb06fdec17a31386c5fc94f526cceba2e0efc95cbde6e1077f99b8324` |
| historical scenario fixture | `daf7ca33b6fe75246d9a14c5e1193f916c4da8ba4a0a100eae2f23a351c2517c` |
| synthetic scenario | `af2101d95784babdd3afaaccad16946ba04abbce866643c7e6cb4413ecb33daf` |
| rejection decision fixture | `e785b11e591610600e8b8077d5a8f82cbd51e7c5067f4f714776fc4b9c81281f` |
| adoption decision fixture | `91b828771b0fc0dd8895aa87a23062efe308acef69f40e8122a31aca16d7d21e` |

All six declared compatibility adapters bind the exact runner hash above. Unknown fields, duplicate JSON keys, noncanonical UTF-8/LF bytes, reordered stages, unregistered roles/views/adapters/decisions, undeclared effects, and changed adapter bytes are refused.

## Exact local package rehearsal

The final disposable build and rehearsal root is outside the operational checkout:

`../work/wo-reb-018-35f7afd-package`

The package inputs and installed runtime identities were:

| Role | Version and archive | Archive SHA-256 | Installed package-tree SHA-256 |
| --- | --- | --- | --- |
| released predecessor | `se_harness-0.5.0-py3-none-any.whl` | `974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f` | `6233a429759c6600d033d947eb72fce4403bd742b57d367ac9c7e2709934b4bc` |
| non-promotable successor | `se_harness-0.6.0-py3-none-any.whl` | `b2848a48093f2c82806b8df66d11aecd7481926f877c447962922e454a505fa8` | `087e0899ee78980fb271b10c4a9c06ec0ad625ae1895220e474aa693d382baaa` |

Both environments used isolated Python 3.14.6 virtual environments outside the checkout. The released predecessor archive was the retained exact public 0.5.0 wheel. The successor wheel was rebuilt from the final reviewed source and template tree. It is disposable qualification input, not a release distribution.

The installed successor contract SHA-256 was exactly `5819dbabeeea7d2dc538e67d2d53eb8290e5a192f499e6250ccbedc9d2a9b167`, equal to the source contract. The successor runtime recorded payload SHA-256 `e23067781d48491d689d28789404888d0ea4a15a73b5b3944b68a7ff56a1f2d3`.

The historical scenario ran twice from the installed packages. Both runs passed and produced the same normalized semantic SHA-256:

`9d879f060f77852f36aa7d1ee653721a6bb203ca661309bd78c665e60a166bb8`

The normalized digest excludes elapsed time, host/interpreter facts, raw checkout bytes, and independently built successor distribution identities, while the retained result still records every exact factual value. It continues to bind the candidate Git identity, scenario, contract/runner, stage reports, decisions, and unchanged-state claim. This proves deterministic local replay; hosted Windows/Linux agreement is recorded below.

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

Both final exact-package rehearsals recorded operational source SHA-256 `e84858ad7e52faa5bdfcc9de178be35ba076ac849929f4ee1bf251cea41041fb` before and after. Git HEAD remained `35f7afdbaff9dd9734a1b2e4b6f4147cc8d294a3`, and Git refs SHA-256 remained `5b723e0b204e3693c6e5f335ce92faacefe30eb9ef224a50baa890413e66b33c`.

The retained result reports `false` for credential use, network, lifecycle transition, tag, release, publication, deployment, maintenance mutation, external-policy change, and operational root-evaluator upgrade. Runtime checks also proved separate environments, checkout exclusion, user-site isolation, and exact predecessor archive identity.

Focused adversarial tests inject a fault at each of the nine stages and prove the first fault is retained while every later stage is `not-run`. Additional cases cover tampered scenario bytes, reordered stages, role and decision substitution, undeclared authority effects, operational mutation, credential-bearing environments, shared runtimes, checkout imports, output collisions, and exact predecessor mismatch.

## Local verification

The following checks passed on Windows:

- governance-migration and adjacent policy tests: 51 passed;
- complete clean-detached suite: 462 passed with 7 declared skips in 262.339 seconds;
- candidate-template graph: 679 artifacts, 0 errors, 50 maintenance warnings;
- exact released-0.5 predecessor view: 677 artifacts, 0 errors, 49 maintenance warnings;
- exact released-0.5 `doctor`: exit 0 with existing maintenance-location warnings only;
- exact released-0.5 `WO-REB-018` start preflight: ready, 0 diagnostics before implementation;
- released-distribution validation: pass with one distribution-bearing record;
- portable wheel surface: pass;
- installed/source contract parity: pass;
- public CLI parser/help and canonical JSON output: pass; and
- Git whitespace/diff checks: pass after retaining this evidence.

The separately locked managed-root 0.5 validator still reports the already known #103 boundary on the unmodified complete graph: `E009` for rejected `RLS-SEH-009`, plus `E010` for the duplicate 0.6.0 records `RLS-SEH-009` and `RLS-SEH-012`. The candidate validator accepts the complete graph. The exact released-0.5 preparation view removes only that previously governed incompatible pair and passes with zero errors. This evidence does not treat the root failure as a new implementation failure or change the root evaluator.

The candidate-source `doctor` and review preflight also correctly refuse to treat the unadopted 0.6.0 template as the operational root: they report the existing managed-root files and lock as different from the candidate distribution. The released-0.5 `doctor` is the authoritative operational check at this stage and passes on its exact predecessor view. Candidate complete-graph validation remains a separate claim and passes. This is the authority separation the rehearsal is intended to preserve, not a bypass or an inferred root upgrade.

## Hosted qualification and normalization correction

Hosted run `32630458376` at exact implementation commit `35f7afdbaff9dd9734a1b2e4b6f4147cc8d294a3` passed:

- candidate source job `97172344750`;
- candidate package job `97172439538`;
- Linux migration job `97172479304`;
- Windows migration job `97172479387`; and
- cross-platform reconciliation job `97172594101`.

Each platform ran the historical scenario twice and all four results passed with semantic SHA-256 `cb6e1a8d0e50b90535176cf6825566fd3f19d13cf89ab9f719995fa0633aee72`. Both retained the exact public predecessor archive SHA-256 `974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f`, exact commit `35f7afdbaff9dd9734a1b2e4b6f4147cc8d294a3`, equal refs SHA-256 `04c78e3c1e979782bf62eeb74a97b2c8f9916619da8ef6755c3ee309f8bd3769`, and `operational_state.unchanged = true`.

The retained platform-specific facts remain visible rather than being discarded. Linux recorded source SHA-256 `dc2f9ced95d5057c990703baaa6f8abee962b23d9cd76caca352d928d0d588d2`, successor archive `d064f9cd54f81d7a784adad2ba467275b3416c8708ae15eaf72df2206df53f1c`, package tree `6da5346a2b92b8b5d889e83b6d6eff474f0f8566f832a06f17ea8102fd1322d8`, and payload `1bfe32ee26a8a9f2526a4d04c3c20f2d99e4ddfcfd258feca20d05396fc74dc5`. Windows recorded source `2c983103bbdb2c17fe23758ff39184e27aaba3205daf0408d7c42b5e7552bb30`, successor archive `0c263635f7274ac2f7713d2d13832eb712f8a2460d4e3f8b4d655a70e9fc6785`, package tree `087e0899ee78980fb271b10c4a9c06ec0ad625ae1895220e474aa693d382baaa`, and payload `e23067781d48491d689d28789404888d0ea4a15a73b5b3944b68a7ff56a1f2d3`.

Runs `32629590304` and `32630115767` usefully failed only the reconciliation job after both platform rehearsals passed. The first digest still included raw source, executable, and independently built archive facts; the second still included installed successor package-tree and payload facts. The final correction keeps all those values in the evidence but removes them from the cross-platform semantic comparison. A regression test mutates every normalized platform field, proves raw results differ, and proves the semantic digest remains equal. Recomputing the final algorithm over the second run's retained Windows/Linux artifacts produced one digest before the final hosted retry.

Predecessor evaluator assessment run `32630458445` passed. Legacy Engineering Harness run `32630458398` stopped at the released-0.5 full-graph `E009`/`E010` boundary tracked by #103; it did not fail the candidate source, package, migration, or reconciliation work and was not converted to an allowlist.

Commit-bound VREC preparation remains pending until the clean governance commit containing this evidence and the `implemented` transition exists. No VREC has been verified or rejected.

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

Create the clean governance commit containing only this retained evidence update and the `WO-REB-018` `in_progress` to `implemented` transition, qualify that exact commit, and prepare ready `VREC-REB-014`. Assurance review and any `ready` to `verified` transition remain separate decisions.
