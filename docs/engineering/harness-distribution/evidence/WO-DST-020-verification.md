# WO-DST-020 implementation evidence

## Scope and authority

The repository owner approved `REQ-DST-062` through `REQ-DST-064`, `SPEC-DST-020`, `ARCH-DST-013` including its `no_significant_decision` assessment, `VER-DST-020`, and `WO-DST-020` for implementation on 2026-08-20. The same instruction requires the RCV and 0.5.1 release artifacts to remain draft.

This evidence covers bounded local implementation only. It does not authorize or record a candidate commit, VREC, push, pull request, merge, release build, release record, version change, tag, publication, deployment, root upgrade, or issue action.

## Released-evaluator preflight

- Evaluator: externally installed public `se-harness 0.5.0`.
- Installed module origin: the dedicated `public-0.5.0` environment outside the checkout.
- Public wheel SHA-256 retained by the approved HUP chain: `974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f`.
- `harnessctl preflight . --work-order WO-DST-020`: PASS in `start` phase with `WO-DST-020` approved and commit-bound verification required.
- Every returned manifest file was read before product implementation: the managed router, repository context and index, workflow, decision rights, quality gates, traceability, `INT-DST-001`, `CAP-DST-001`, the three new requirements, specification, architecture, verification contract, and work order.
- Public `harnessctl doctor .`: PASS before implementation; the public distribution, schema-2 lock, every managed path, and required repository paths matched.

## Baseline and selected target

| Observation | Value |
| --- | ---: |
| Baseline main commit | `af0eaa0ff0b44f887a01278de821c9be5b7fc086` |
| Baseline graph | 539 artifacts, 1,944 relations |
| Baseline topology | 525,689 UTF-8 bytes |
| Old repository target | 524,288 bytes |
| Baseline excess | 1,401 bytes |
| Approved target | 2,097,152 bytes |
| Increase | exactly 4x |

The old failure was reproduced by the merged PR integration history and is retained as problem evidence. It is not treated as a waived gate.

## Implemented change

- Changed the canonical candidate standard-template generator to `TOPOLOGY_ACCEPTANCE_BYTES = 2_097_152`.
- Added one small `topology_target_exceeded` predicate so exact below/equal/above boundary behavior can be tested without constructing multi-mebibyte fixtures.
- Changed `tests/test_dashboard_webui.py` to load the canonical candidate generator instead of the independently managed root generator.
- Added explicit assertions that the candidate target is 2 MiB while the active root remains 512 KiB.
- Preserved the strict predicate: values below or equal to the target do not exceed it; target plus one byte does.
- Aligned only the obsolete capacity wording in `REQ-DST-055`, `SPEC-DST-013`, `VER-DST-013`, `SPEC-DST-017`, and `VER-DST-017`. Their statuses, relations, dates, architecture decisions, and noncapacity meaning remain unchanged.
- Added and approved the complete `REQ-DST-062..064`, `SPEC-DST-020`, `ARCH-DST-013`, `VER-DST-020`, and `WO-DST-020` packet.

## Product/governor separation

| Surface | Observed target | Result |
| --- | ---: | --- |
| Canonical candidate template | 2,097,152 | changed as authorized |
| Active root `scripts/generate_harness_dashboard.py` | 524,288 | unchanged |
| Candidate-initialized disposable repository | 2,097,152 | package content confirmed |
| `.engineering-harness.lock` and managed configuration | public 0.5.0 | unchanged; public doctor passes |

The active root generator, lock, config, managed router, Engineering Harness workflow, package version, release artifacts, and RCV artifacts were not edited. Candidate bytes were never used as the released evaluator.

## Exact limits

The candidate generator declares:

| Limit | Bytes |
| --- | ---: |
| `MAX_INDEX_BYTES` | 262,144 |
| `MAX_SUMMARY_BYTES` | 262,144 |
| `MAX_CONTENT_DOCUMENT_BYTES` | 262,144 |
| `MAX_CONTENT_TOTAL_BYTES` | 16,777,216 |
| `TOPOLOGY_ACCEPTANCE_BYTES` | 2,097,152 |

No other limit, bundle schema, serialized field, relation, finding, provenance observation, manifest descriptor, path, browser origin, dependency, permission, persistence, network behavior, or publication behavior changed.

## Focused and complete tests

| Check | Result |
| --- | --- |
| Candidate dashboard/WebUI module, Python 3.14.6 | PASS: 23 tests, 1 environment-dependent symlink skip |
| Complete suite, Python 3.14.6 | PASS: 277 tests, 4 environment-dependent skips |
| Complete suite, Python 3.11.9 | PASS: 277 tests, 4 environment-dependent skips |
| Exact boundary cases | PASS: target minus one, target, target plus one |
| Candidate/root separation assertions | PASS |
| Release-distribution policy validator | PASS: 0 distribution-bearing records |
| Candidate and public CLI help | PASS |
| `git diff --check` before evidence | PASS; only Git line-ending notices |

The four complete-suite skips were identical across runtimes and environment-dependent; no topology or governance test was skipped because of the change.

## Deterministic current-repository generation

Two independent candidate-template output directories were generated concurrently from the same repository bytes and Git history.

| Observation | Value |
| --- | ---: |
| Formal graph | 546 artifacts, 1,966 relations |
| Canonical output files excluding noncanonical timing summary | 642 |
| Canonical file/hash differences | 0 |
| Manifest SHA-256, both runs | `8ec98ad791e1d9b6589be727d4f3833d4f0102a2dec10e96bb2dfc6d2869fc6a` |
| Topology bytes | 532,710 |
| Target | 2,097,152 |
| Remaining headroom | 1,564,442 bytes |
| Target exceeded | false |

The two generation summaries had identical resource-role counts and bytes. Their documented noncanonical timestamp and elapsed-time values were not compared byte-for-byte.

After the evidence file and `implemented` lifecycle state were present, the review projection was repeated. It contained 643 canonical files, retained the same 532,710-byte topology and 1,564,442-byte candidate headroom, and had zero canonical file/hash differences across two runs. The candidate summary reported target 2,097,152 and `topology_target_exceeded = false`; the public-0.5.0 dashboard over the identical manifest reported its unchanged 524,288 target and `topology_target_exceeded = true`. This is the intended product/governor separation.

## Nonpromotable candidate-package lane

- Built an ephemeral `se_harness-0.5.0-py3-none-any.whl` outside the checkout using `pip wheel --no-cache-dir --no-deps --no-build-isolation`.
- Final candidate wheel size: 195,812 bytes.
- Final candidate wheel SHA-256: `7acddafb72d672938ebd0ac14b38081493ad97abbe249365ce233f681e1d5f34`.
- Installed the exact wheel with `--no-index --no-deps` into a fresh Python 3.11 environment outside the checkout.
- Confirmed installed identity `se-harness 0.5.0` from that disposable environment.
- Initialized a disposable standard repository and confirmed its installed generator uses 2,097,152 while all four other limits remain exact.
- Candidate-package `doctor`: PASS on every installed and managed path.
- Candidate-package dashboard: PASS; reported target 2,097,152 and `topology_target_exceeded = false`.

The wheel is explicitly nonpromotable: it has no candidate commit binding, was not copied into release storage, and will be removed with the disposable environment and repository after local qualification.

### Build deviations

1. The first Python 3.11 `pip wheel --no-build-isolation` attempt stopped before artifact creation because that interpreter lacked `setuptools`.
2. The existing isolated build-capable environment then stopped because pip attempted to write its user cache outside the workspace and received access denied.
3. Retrying with `--no-cache-dir` used the already installed backend, downloaded nothing, and built the retained ephemeral wheel successfully.

Neither failed attempt changed the checkout or produced a release artifact.

## Formal and security checks

- Public-0.5.0 formal validation: PASS with 546 artifacts, zero errors, zero structure/governance/policy warnings, and the same 44 pre-existing maintenance warnings.
- Public-0.5.0 review preflight: PASS with `WO-DST-020` implemented and commit-bound verification required.
- Final public-0.5.0 doctor: PASS; every managed file and schema-2 lock entry remains unchanged.
- Final inspection: zero pending definitions, zero active work, and `WO-DST-020` correctly listed as awaiting commit-bound assurance. The unrelated ready `VREC-DST-016` decision remains untouched.
- The temporary date-only alignment was removed after inspection showed two new temporal reassessment observations; final historical definition dates and `ARCH-DST-010`/`ADR-DST-010` remain unchanged.
- Static changed-surface review found no credential, private repository path, new origin, dependency, workflow permission, persistence, or network addition.
- No artifact, relation, finding, provenance item, or evidence reference was removed to reduce topology size.
- Historical evidence and released records containing the old target remain immutable historical observations.

## Checks requiring later authority

Hosted branch-push and pull-request merge-ref evidence cannot exist before an authorized candidate commit, guarded push, and pull request. The local implementation intentionally stops before those actions. They remain mandatory before a ready VREC can be assessed and must record both branch and integration-history topology sizes against the same 2 MiB target.

The released evaluator's `accept-candidate` command also requires the exact candidate commit. Running it against this uncommitted wheel would record false provenance, so it is deferred to the separately authorized candidate-commit stage.

## Unperformed actions

No candidate commit, VREC preparation or transition, push, pull request, merge, package-version change, promotable release build, RCV or 0.5.1 artifact edit, release record, tag, GitHub Release, PyPI publication, Pages deployment, installed-root upgrade, issue edit, or other external action was performed.

## Residual risks

- Repository topology continues to grow; 2 MiB is substantial headroom, not an unlimited guarantee.
- Pull-request merge history can add valid provenance and must still be observed in hosted CI after separate authority.
- Topology remains one deferred resource. Approaching 2 MiB requires a separately governed sharding decision rather than another implicit increase.
- Commit-bound assurance remains required. Local implementation evidence does not verify or release the candidate.
