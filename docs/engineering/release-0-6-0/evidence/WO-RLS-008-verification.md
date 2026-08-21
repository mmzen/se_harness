# WO-RLS-008 qualification evidence

## Evidence status and authority boundary

This evidence records work performed on 2026-08-21 under the approved bounded implementation envelope for `REL-SEH-007` and `WO-RLS-008`. It now includes the separately authorized operational candidate commit, local exact-candidate replay, dedicated candidate-branch push, and hosted exact-candidate results. The existing Git credential was used only for that one push. This evidence is not aggregate capture, a VREC or RLS proposal or transition, a release decision, tag, publication, deployment, maintenance mutation, external policy change, or root-evaluator upgrade.

`WO-RLS-008` is `implemented`. Candidate commit `827b2709292abaa3458bb3b4cac37b582378c585` passes local exact-candidate qualification on Python 3.14.6 and Python 3.11.9 and all push-triggered hosted qualification lanes. The separately authorized post-candidate governance commit retains only this evidence update and the work-order transition; it does not replace or mutate the candidate.

## Approved aggregate scope

- Work orders: `WO-DST-019`, `WO-DST-020`, `WO-WEX-001`, `WO-WEX-002`, `WO-REB-001`, `WO-REB-002`, `WO-REB-003`, and `WO-RLS-008`.
- Verification contracts: `VER-DST-001`, `VER-DST-019`, `VER-DST-020`, `VER-WEX-001`, `VER-WEX-002`, and `VER-REB-001`.
- Existing keyed evidence: the seven paths named in `WO-RLS-008`; this file is the eighth keyed evidence path.
- Excluded release-bearing work: `WO-HUP-001`, `WO-RCA-001`, emergency publication history, merge-only commits, governance transitions, and every work order not explicitly allowed by `REL-SEH-007`.

## Baseline and exact candidate identity

| Item | Identity |
| --- | --- |
| `v0.5.0` annotated tag object | `b4a1b7956c6d78ea808997eed027800a8b973f4a` |
| `v0.5.0` released candidate commit | `c42bbac20f14268ef162c9628dd1d2b45ea843af` |
| Initial clean `main` / operational working-tree parent | `cd80f0bde9f24a069d15ba461d1257261d744e9c` |
| Initial parent tree | `9dc1d1f9aaf9c2bc2b2c8926772b67d558ba0d85` |
| Operational candidate commit | `827b2709292abaa3458bb3b4cac37b582378c585` |
| Operational candidate tree | `cdeb5f5e0fe512e042dd13d8f8071dc06a1b40e0` |
| Exact candidate build epoch | `1787322471` |
| Exact candidate archive SHA-256 | `6ed1b6e4dcad1e24d042babb773be5e52638cb11a4a6fe458da03178a187aabc` |

The retained exact-candidate replay is under `work/release-0.6.0-exact-827b270`. All source exports came from `git -c core.autocrlf=false archive` of the operational candidate. The two test exports received fixture-only Git metadata so Git-dependent tests could execute; those disposable fixture commits are not represented as the candidate identity. All candidate, bundle, package, and verifier evidence below is explicitly bound to the operational candidate commit.

## Version and changed-path inventory

The candidate commit has candidate identity `0.6.0` in:

- `pyproject.toml`;
- `se_harness/__init__.py`; and
- the exact public install example in `README.md`.
- the current source-candidate statement in `docs/notes/developing-se-harness.md`.

The exact released-root surfaces remain at 0.5.0 and have no candidate-commit diff:

- `.engineering-harness.toml`;
- `.engineering-harness.lock`;
- `ENGINEERING_HARNESS.md`; and
- `.github/workflows/engineering-harness.yml`.

The commit has exactly 13 changed paths: the three product-version files; `docs/notes/developing-se-harness.md`; the four `REL-SEH-007` / `WO-RLS-008` release-domain files; `WO-VSP-006` plus its evidence; and the three explicitly dispositioned WEX verification records. `git diff --check HEAD^ HEAD` passes. No protected released-root path changed.

## Runtime identities

| Plane | Result | Evidence |
| --- | --- | --- |
| Released evaluator | PASS | Public `se-harness==0.5.0`, Python 3.14.6, isolated Python, user site disabled, distribution/module/templates/entry point under `work/released-evaluator-0.5.0`, no checkout fallback; wheel SHA-256 `974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f`. |
| Candidate source | PASS, exact candidate | Version 0.6.0, Python 3.14.6, module/templates/distribution metadata under the exact archive export, bound to commit `827b2709292abaa3458bb3b4cac37b582378c585`, no diagnostics. |
| Candidate package | PASS, exact candidate | Fresh wheel-only Python 3.14.6 and Python 3.11.9 environments with `-I`, user site disabled, package/templates/entry point outside the checkout, bound to the operational candidate commit. |

The preliminary editable-install identity failure remains correctly rejected because editable distribution metadata resolved outside the checkout. Exact source identity ran from the archived candidate export; exact package identity ran only from fresh offline wheel installations. The globally installed Python was not used as the released evaluator because it resolves an unrelated editable 0.4.1 checkout.

## Root and graph checks

| Check | Result |
| --- | --- |
| Released-0.5.0 start preflight after the complete 15-file reading manifest | PASS |
| Released-0.5.0 exact-candidate review preflight for `WO-RLS-008` | PASS; `ready: true`, status `in_progress`, no diagnostics |
| Released-0.5.0 post-hosted implementation review preflight for `WO-RLS-008` | PASS; `ready: true`, status `implemented`, no diagnostics |
| Released-0.5.0 review preflight for `WO-VSP-006` | PASS; no diagnostics |
| Released-0.5.0 root doctor | PASS; managed installation unchanged; existing candidate-template W013 advisories retained |
| Candidate artifact validation | PASS: 597 artifacts, 0 errors, 44 existing maintenance warnings, 0 structure/governance/policy warnings |
| Release-distribution validation | PASS: no distribution-bearing records exist yet |
| Released-evaluator exact-candidate inspection | PASS observation: 597 artifacts, 2,140 relations, 44 maintenance findings, zero decisions required, and only `WO-RLS-008` active |
| Released-evaluator post-hosted implementation inspection | PASS observation: zero active work, zero decisions required, and only implemented `WO-RLS-008` in the assurance-pending queue |
| Released-evaluator Explorer | PASS: manifest `72de5c772c3b402be48aca38fabad38d8b680c41766fbeb7b6724abc262a0715` |
| Portable release surface, repository, both wheels, and both installed CLIs | PASS |
| `git diff --check HEAD^ HEAD` | PASS |

Under the later separate assurance authorization, governance-only `WO-VSP-006` explicitly superseded `VREC-WEX-001`, `VREC-WEX-002`, and `VREC-WEX-003` with verified, coverage-preserving `VREC-WEX-005`. Released-evaluator inspection now reports zero decision-required items. The governance work order is excluded from the exact eight-work-order release-bearing allow-list.

## Source regression results

Two independent exact-archive test exports passed the complete suite:

- Python 3.14.6: 369 tests in 199.387 seconds, five conditional skips, zero failures or errors.
- Python 3.11.9: 369 tests in 202.662 seconds, the same five conditional skips, zero failures or errors.

The preliminary current-version, Git-metadata, and JSON byte-parity failures remain resolved by the authorized documentation correction and LF-normalized exact exports. No candidate source byte was changed during the replay.

## Exact reproducible distributions

Two builds used separate untouched exact candidate exports, Python 3.14.6, `SOURCE_DATE_EPOCH=1787322471`, and:

```text
python -m build --wheel --sdist --no-isolation --outdir <raw-output> <export>
python scripts/normalize_sdist.py --epoch 1787322471 <raw-sdist> <final-sdist>
```

| File | Build A SHA-256 | Build B SHA-256 | Result |
| --- | --- | --- | --- |
| `se_harness-0.6.0-py3-none-any.whl` | `9eb550d2fbab2ea8906aadb39ff75271ca9037267d721b8705cad93012b3ed37` | `9eb550d2fbab2ea8906aadb39ff75271ca9037267d721b8705cad93012b3ed37` | byte-identical |
| `se_harness-0.6.0.tar.gz` | `df10d40eeebfcecf5bbd082aba3444bab8fd63146c1f7c5d2a03c0ad313d98f1` | `df10d40eeebfcecf5bbd082aba3444bab8fd63146c1f7c5d2a03c0ad313d98f1` | byte-identical after normalization |

Both wheels pass the repository's portable-release-surface policy. The build emitted the existing setuptools notice that the TOML-table form of `project.license` is deprecated after 2027-02-18; it is not a current build failure and changing it is outside this release-integration scope.

An offline wheel reconstruction from the normalized sdist at the same epoch is byte-identical to both direct wheels. The release-bundle manifest is bound to the operational commit and records source-manifest SHA-256 `1fa0127abddd446a519bab667cd89cfaeff95979775f28d500ea1c993dad1832`, checksum-content SHA-256 `63a0d91bc027447449901c9733e1caee5d32d73c8e60c2eda1ce357f7550459b`, and manifest-file SHA-256 `8b6e3ad52b5e65f50b4dc0ecd98cf12f46fd100d73c23d5864678dc027fdbb89`.

## Fresh-package and verifier-owned acceptance

The exact wheel installed offline with no dependencies into fresh Python 3.14.6 and Python 3.11.9 environments and reported version 0.6.0. Candidate-package identity and installed-CLI portable-surface policy passed on both runtimes.

The isolated released 0.5.0 evaluator ran verifier-owned black-box acceptance against the exact operational-candidate wheel on Python 3.14.6 and Python 3.11.9. All ten scenarios passed on both runtimes: installed identity, init, adopt, doctor, validate, dashboard, safe upgrade, customized-content refusal, corrupted-integrity refusal, and authority denial.

- Python 3.14.6 acceptance manifest SHA-256: `6845459905f7cd27a09ab0fcb6cf18b66a26b2174876169027843adeb6bd5630`.
- Python 3.11.9 acceptance manifest SHA-256: `72446826458a3fa2ad3270c911fb9289fc9e326291ef8c64989c965274ce55c3`.
- Released verifier wheel SHA-256: `974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f`.
- Released verifier contract SHA-256: `a443e93d6da7d0538bdf790a16f4dea49ac7a6ede384c65e40362627d7a84b75`.

Both manifests are bound to operational candidate commit `827b2709292abaa3458bb3b4cac37b582378c585`. They are retained qualification evidence, not an aggregate assurance decision or lifecycle transition.

## Hosted exact-candidate qualification

The separately authorized credential use created `origin/candidate/0.6.0` at exactly `827b2709292abaa3458bb3b4cac37b582378c585`. The push-triggered workflows completed against that same `head_sha` without checkout mutation:

| Workflow / job | Run | Result | Timing (UTC) |
| --- | --- | --- | --- |
| SE Harness Candidate Evidence / Candidate source evidence | [run 97, job 96806587928](https://github.com/mmzen/se_harness/actions/runs/32493552379/job/96806587928) | PASS | 2026-08-21 14:42:10 to 14:42:48 |
| SE Harness Candidate Evidence / Candidate package evidence | [run 97, job 96806785170](https://github.com/mmzen/se_harness/actions/runs/32493552379/job/96806785170) | PASS | 2026-08-21 14:42:51 to 14:43:08 |
| Engineering Harness / validate | [run 397, job 96806588077](https://github.com/mmzen/se_harness/actions/runs/32493552394/job/96806588077) | PASS | 2026-08-21 14:42:10 to 14:42:26 |

The complete [Candidate Evidence run 97](https://github.com/mmzen/se_harness/actions/runs/32493552379) and [Engineering Harness run 397](https://github.com/mmzen/se_harness/actions/runs/32493552394) both concluded `success`. No pull request, merge, tag, release, publication, deployment, maintenance mutation, external policy change, or root-evaluator upgrade accompanied the push.

## Required work not yet performed

- No aggregate capture occurred, no `VREC-SEH-008` or `RLS-SEH-008` file was prepared, and no aggregate VREC or RLS status changed. The only VREC status changes are the three separately authorized WEX supersessions retained under `WO-VSP-006`.
- The post-candidate governance commit is local only and has not been pushed.
- No merge, tag, GitHub Release, PyPI upload, Pages deployment, maintenance-line mutation, credential use beyond the single authorized branch push, external policy change, or root-evaluator upgrade occurred.

## Current stop and next accountable decisions

Implementation stops here under the work order's explicit authority boundary. The candidate commit, documentation correction, WEX supersession decisions, dual-runtime suites, reproducibility, offline reconstruction, runtime identities, bundle/source manifests, verifier-owned acceptance, hosted source/package/root lanes, retained evidence, and `WO-RLS-008` implementation transition now pass. Candidate identity remains `827b2709292abaa3458bb3b4cac37b582378c585`. Aggregate VREC and RLS preparation or transition remain separately unauthorized.
