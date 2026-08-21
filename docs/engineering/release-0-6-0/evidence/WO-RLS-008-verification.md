# WO-RLS-008 preliminary qualification evidence

## Evidence status and authority boundary

This evidence records work performed on 2026-08-21 under the approved bounded implementation envelope for `REL-SEH-007` and `WO-RLS-008`. It is preliminary working-tree and disposable-fixture evidence. It is not a candidate commit, aggregate capture, VREC or RLS proposal or transition, release decision, tag, publication, deployment, maintenance mutation, credential use, external policy change, or root-evaluator upgrade.

`WO-RLS-008` remains `in_progress`. The authorized documentation correction and the separately authorized historical WEX dispositions are complete, and preliminary qualification now passes on Python 3.14.6 and Python 3.11.9. Exact-candidate qualification remains stopped only because the operational candidate commit is deliberately unauthorized.

## Approved aggregate scope

- Work orders: `WO-DST-019`, `WO-DST-020`, `WO-WEX-001`, `WO-WEX-002`, `WO-REB-001`, `WO-REB-002`, `WO-REB-003`, and `WO-RLS-008`.
- Verification contracts: `VER-DST-001`, `VER-DST-019`, `VER-DST-020`, `VER-WEX-001`, `VER-WEX-002`, and `VER-REB-001`.
- Existing keyed evidence: the seven paths named in `WO-RLS-008`; this file is the eighth keyed evidence path.
- Excluded release-bearing work: `WO-HUP-001`, `WO-RCA-001`, emergency publication history, merge-only commits, governance transitions, and every work order not explicitly allowed by `REL-SEH-007`.

## Baseline and preliminary source identity

| Item | Identity |
| --- | --- |
| `v0.5.0` annotated tag object | `b4a1b7956c6d78ea808997eed027800a8b973f4a` |
| `v0.5.0` released candidate commit | `c42bbac20f14268ef162c9628dd1d2b45ea843af` |
| Initial clean `main` / operational working-tree parent | `cd80f0bde9f24a069d15ba461d1257261d744e9c` |
| Initial parent tree | `9dc1d1f9aaf9c2bc2b2c8926772b67d558ba0d85` |
| Preliminary build epoch | `1787316550` (the initial parent commit timestamp; not a final candidate epoch) |
| Disposable qualification-only Git fixture | `6c2c438bfd760bc680ea4cccb34fd69a7018c98c` |

The disposable fixture commit exists only under `work/release-0.6.0-preliminary/export-c`. It supplies Git metadata to tests and black-box acceptance without changing the operational repository. It must not be represented as, captured as, tagged as, or promoted as the release candidate.

## Version and changed-path inventory

The approved working tree currently has candidate identity `0.6.0` in:

- `pyproject.toml`;
- `se_harness/__init__.py`; and
- the exact public install example in `README.md`.
- the current source-candidate statement in `docs/notes/developing-se-harness.md`.

The exact released-root surfaces remain at 0.5.0 and have no Git diff:

- `.engineering-harness.toml`;
- `.engineering-harness.lock`;
- `ENGINEERING_HARNESS.md`; and
- `.github/workflows/engineering-harness.yml`.

Tracked product changes are limited to `README.md`, `pyproject.toml`, and `se_harness/__init__.py`. The only untracked operational path is `docs/engineering/release-0-6-0/`. No candidate commit was created.

## Runtime identities

| Plane | Result | Evidence |
| --- | --- | --- |
| Released evaluator | PASS | Public `se-harness==0.5.0`, Python 3.14.6, isolated Python, user site disabled, distribution/module/templates/entry point under `work/released-evaluator-0.5.0`, no checkout fallback; wheel SHA-256 `974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f`. |
| Candidate source | PASS, preliminary fixture | Version 0.6.0, Python 3.14.6, module/templates/distribution metadata under the disposable `export-c`, bound only to fixture commit `6c2c438bfd760bc680ea4cccb34fd69a7018c98c`. |
| Candidate package | PASS, preliminary fixture | Fresh wheel-only environment, Python 3.14.6 with `-I`, user site disabled, package/templates/entry point outside the checkout, bound only to the disposable fixture commit. |

The initial editable-install identity failure was correctly rejected because editable distribution metadata resolved outside the checkout. Removing that install and executing candidate source directly from a clean checkout/export satisfied the candidate-source role. The globally installed Python was not used as the released evaluator because it resolved an unrelated editable 0.4.1 checkout.

## Root and graph checks

| Check | Result |
| --- | --- |
| Released-0.5.0 start preflight after the complete 15-file reading manifest | PASS |
| Released-0.5.0 review preflight for `WO-RLS-008` | PASS; `ready: true`, status `in_progress`, no diagnostics |
| Released-0.5.0 root doctor | PASS; managed installation unchanged; existing candidate-template W013 advisories retained |
| Candidate artifact validation | PASS: 596 artifacts, 0 errors, 44 existing maintenance warnings, 0 structure/governance/policy warnings |
| Release-distribution validation | PASS: no distribution-bearing records exist yet |
| Released-evaluator inspection | PASS observation: 597 artifacts, 2,140 relations, 44 maintenance findings, zero decisions required, and only `WO-RLS-008` active |
| Released-evaluator Explorer | PASS: manifest `015ee355118335b3f4560dd309a1e7a9d24f21031b13b5a11d49d1e0cd90ca59` |
| Portable release surface, repository and both wheels | PASS |
| `git diff --check` | PASS; Windows LF-to-CRLF notices only |

Under the later separate assurance authorization, governance-only `WO-VSP-006` explicitly superseded `VREC-WEX-001`, `VREC-WEX-002`, and `VREC-WEX-003` with verified, coverage-preserving `VREC-WEX-005`. Released-evaluator inspection now reports zero decision-required items. The governance work order is excluded from the exact eight-work-order release-bearing allow-list.

## Source regression results

The complete Python 3.14.6 suite executed 369 tests in 183.249 seconds with five conditional skips. The first LF-export run reported two failures and one error:

1. The release-manifest test required Git metadata that a plain `git archive` export intentionally lacked.
2. PowerShell's first archive invocation applied Windows CRLF conversion to two Git-normalized JSON contracts.
3. `docs/notes/developing-se-harness.md` does not contain the candidate version `0.6.0`, violating `test_development_note_explains_standard_evaluator_and_candidate_planes`.

The first two are disposable-fixture mechanics, not product failures. Re-exporting with `git -c core.autocrlf=false archive` and initializing a fixture-only Git repository made the exact two targeted tests pass. The documentation assertion still fails alone. Because `docs/notes/developing-se-harness.md` is outside `[execution_scope].paths`, it was not modified.

After the narrow scope amendment and WEX dispositions entered a fresh LF-normalized fixture, the complete suite passed on both supported local runtimes:

- Python 3.14.6: 369 tests in 184.924 seconds, five conditional skips, zero failures or errors.
- Python 3.11.9: 369 tests in 187.069 seconds, the same five conditional skips, zero failures or errors.

The previously failing current-version, Git-metadata, and JSON byte-parity cases all pass in the corrected fixture.

## Preliminary reproducible distributions

Two builds used separate LF-normalized exports, Python 3.14.6, `SOURCE_DATE_EPOCH=1787316550`, and:

```text
python -m build --wheel --sdist --no-isolation --outdir <raw-output> <export>
python scripts/normalize_sdist.py --epoch 1787316550 <raw-sdist> <final-sdist>
```

| File | Build C SHA-256 | Build D SHA-256 | Result |
| --- | --- | --- | --- |
| `se_harness-0.6.0-py3-none-any.whl` | `d10f2f7673b1928613b508678e1b050c120ae87f5a7ff9b6f8a51f4c2f4a5b3c` | `d10f2f7673b1928613b508678e1b050c120ae87f5a7ff9b6f8a51f4c2f4a5b3c` | byte-identical |
| `se_harness-0.6.0.tar.gz` | `cdbca8e84425314010d66987d302f483cfeca2af7c6ef7e96936e00a47d91e00` | `cdbca8e84425314010d66987d302f483cfeca2af7c6ef7e96936e00a47d91e00` | byte-identical after normalization |

Both wheels pass the repository's portable-release-surface policy. The build emitted the existing setuptools notice that the TOML-table form of `project.license` is deprecated after 2027-02-18; it is not a current build failure and changing it is outside this release-integration scope.

These hashes are preliminary and non-promotable. A final exact-candidate replay must use the actual candidate commit timestamp.

The documentation and governance files are intentionally absent from the package manifest, so the amended replay retained the same wheel and normalized-sdist hashes. A wheel rebuilt offline from the normalized sdist at the same epoch is byte-identical to both direct wheels at SHA-256 `d10f2f7673b1928613b508678e1b050c120ae87f5a7ff9b6f8a51f4c2f4a5b3c`.

## Fresh-package and verifier-owned acceptance

The exact preliminary wheel installed offline with no dependencies in a fresh environment and reported version 0.6.0. Candidate-package identity passed. A disposable standard repository passed init, doctor, validate, dashboard, and same-version transactional upgrade behavior. Installed CLI portable-surface policy passed.

The isolated released 0.5.0 evaluator ran verifier-owned black-box acceptance against the amended fixture-bound wheel on Python 3.14.6 and Python 3.11.9. All ten scenarios passed on both runtimes: installed identity, init, adopt, doctor, validate, dashboard, safe upgrade, customized-content refusal, corrupted-integrity refusal, and authority denial.

- Python 3.14.6 acceptance manifest SHA-256: `b487c344f6f77a60bfd460cdffd7553d7421e9e855b469b2b115eef8a97523b7`.
- Python 3.11.9 acceptance manifest SHA-256: `2a39f6bc2a51b5ba5581a9dc9e91b64b8d78fe8426d93b8d7f94efbc83ccbb87`.
- Released verifier contract SHA-256: `a443e93d6da7d0538bdf790a16f4dea49ac7a6ede384c65e40362627d7a84b75`.

The manifest is bound to the disposable fixture commit and is not an operational candidate manifest or assurance decision.

## Required work not yet performed

- No operational candidate commit, exact candidate tree or epoch, exact-source replay, release bundle manifest, source manifest, hosted candidate lanes, or aggregate capture.
- No `VREC-SEH-008` or `RLS-SEH-008` file was prepared and no aggregate VREC or RLS status changed. The only VREC status changes are the three separately authorized WEX supersessions retained under `WO-VSP-006`.
- No merge, tag, GitHub Release, PyPI upload, Pages deployment, maintenance-line mutation, credential use, external policy change, or root-evaluator upgrade occurred.

## Current stop and next accountable decisions

Qualification stops here under the work order's explicit authority boundary. The documentation correction, WEX supersession decisions, dual-runtime suites, reproducibility, offline reconstruction, and fresh-package acceptance now pass. The single next accountable decision is whether to authorize one operational candidate commit containing the reviewed implementation, governance decisions, and retained evidence. Exact candidate epoch builds, bundle/source manifests, hosted lanes, and aggregate capture must occur only after that separately authorized commit; aggregate VREC preparation and transition remain independently unauthorized.
