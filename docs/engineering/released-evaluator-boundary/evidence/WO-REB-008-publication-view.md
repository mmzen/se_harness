# WO-REB-008 publication predecessor-view evidence

## Authority and state

This retained evidence covers pre-candidate review, exact local qualification, and hosted qualification for `WO-REB-008`. It records implementation and qualification observations only; lifecycle, assurance, integration, and publication authority remain separate governance decisions.

Preserved release identities:

- candidate C6: `3b339e9fc70cc634e6dc6bda07ea6a9b1a465798`
- annotated tag object: `03cae3d30ea1e3933a92c9e87683b0144f8ccc77`; peeled target: candidate C6
- released record: `RLS-SEH-012`; Git blob at review base: `090ad5f5b7779748b7a866df913d72aaf9f1372b`; raw SHA-256: `0b0fc3c54968908f6fea0a7d6357c529681ba6a6e75dbce08ca35f4b9fca74af`
- released 0.5.0 wheel SHA-256: `974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f`
- released 0.5.0 installed payload SHA-256: `d247cc48213b49be52345fcadbf2d93355e5ea7ef15b32014d9fc5010458a2bc`
- wheel/sdist/SHA256SUMS identities remain those bound in `RLS-SEH-012`; no distribution file was rebuilt or changed
- root lock/configuration and managed files remain unchanged

## Original closed failure

Authorized publication run `32587383130`, job `97065733491`, failed in `Resolve released authority from main` / `Acquire and prove the released evaluator`. Wheel download, wheel hash, install, runtime identity, and payload identity passed. The direct command

```text
"$RUNNER_TEMP/evaluator-env/bin/harnessctl" validate "$GITHUB_WORKSPACE"
```

then returned the exact retained boundary:

```text
E009 docs/engineering/release-0-6-0/releases/RLS-SEH-009.md: release_record status must be ready or released
E010 docs/engineering/release-0-6-0/releases/RLS-SEH-009.md: duplicate release record version '0.6.0' among RLS-SEH-009, RLS-SEH-012
E010 docs/engineering/release-0-6-0/releases/RLS-SEH-012.md: duplicate release record version '0.6.0' among RLS-SEH-009, RLS-SEH-012
```

All qualification and privileged downstream jobs were skipped. Anonymous reconciliation found no GitHub Release for `v0.6.0`, no PyPI `se-harness==0.6.0`, and no `release/0.6` maintenance ref. No Pages, tag, RLS, distribution, root, or external-policy mutation occurred.

## Start preflight

Released 0.5.0 start preflight passed in an isolated predecessor-compatible projection omitting only the exact rejected pair. The returned schema was `se-harness-preflight-v1`, `ready = true`, work order status `in_progress`, and the complete 15-path reading manifest was read before implementation.

The current candidate validator accepted the approved packet with 653 artifacts, zero errors, and 50 pre-existing maintenance warnings.

## Implemented behavior

`repository_tools/predecessor_publication.py` and `scripts/validate_predecessor_publication_view.py` provide one closed read-only adapter. It:

1. rejects publication credentials, nonempty alternate Git/Python process state, unsafe paths, dirty or non-HEAD source, ambiguous RLS/history, and noncanonical sidecars;
2. validates the complete committed graph with the target checkout's current validator;
3. selects exact released `RLS-SEH-012`, replays its bootstrap contract, evaluator evidence, preparation-view evidence, introduction commit, candidate ancestry, and immutable tag;
4. derives the rejected pair from typed current relations and requires byte/hash equality with the retained sidecar;
5. creates a temporary detached sparse view at exact governance `HEAD` and accepts no caller-supplied omission or diagnostic;
6. proves the exact external wheel/runtime/payload, then requires released 0.5.0 `doctor` and JSON `validate` to pass in that view;
7. proves view cleanup, unchanged tag/history/source, and identical complete validation before and after;
8. optionally writes one exclusive canonical host-normalized JSON observation outside artifact discovery.

The initial release resolver, release-bound Pages build, and standalone Pages recovery now call that same adapter through trusted-main code. No direct full-checkout predecessor `validate` remains at those three points. The initial resolver retains the canonical view and bounded result alongside the release plan; failure retention includes any result produced before the generic refusal.

## Exact local replay

Read-only replay target:

- source commit: `c37ec5af43234ce66c518aa58355ec05c7b8aa21`
- source tree: `eed78d171e32ce862d926a4ad91ed8bf2f95aacf`
- source checkout: disposable clean clone; stopped untracked `RLS-SEH-008` absent
- output: external `WO-REB-008-c37-publication-view.json`
- observation schema: `se-harness-predecessor-publication-view-v1`
- observation SHA-256: `84932d4629e8bbd07b50dd8a0b9c2cb96df093f6e19562ff3f70749450f6dae1`
- complete current validation: 647 artifacts, zero errors, 50 warnings
- predecessor view validation: 645 artifacts, zero errors, 49 warnings
- source/tag/history unchanged: true

Exact omissions:

| Artifact | Path | Git blob | Raw SHA-256 | Bytes |
| --- | --- | --- | --- | ---: |
| `REL-SEH-008` | `docs/engineering/release-0-6-0/release/REL-SEH-008.md` | `d14090b88ff6d1c032333d7a2454ca9a571854e5` | `24e0962f6957e7501159a223913e16ef82b22e5e1ae1a88174b9887b43cb4aec` | 9093 |
| `RLS-SEH-009` | `docs/engineering/release-0-6-0/releases/RLS-SEH-009.md` | `0b9661f570e8a85afa4acb4dd995eda57bfc7f67` | `e0b8952953e8e180c6d572fe5d1236fded7104e623cc336bb9a93cd3b978f9e3` | 1797 |

Canonical sparse-spec SHA-256: `448159eec515975b9e7e946bed2653dbd6811dc4c06fd7b9e9d3a3facbd00332`.

The same replay must be repeated against the eventual clean corrective commit before commit-bound verification; this base replay does not substitute for that later exact-candidate evidence.

## Initial corrective commit-bound replay

Initial local corrective candidate identity:

- source commit: `6eb13f60cc84755190bc69b5ceb09a5e2a37fd7a`
- source tree: `b73550087b55fc7c2baa9a51a30b0af7b2a5c1bd`
- commit diff: exactly the 17 paths listed below
- source checkout: fresh short-path detached clone with canonical-LF checkout; the stopped untracked `RLS-SEH-008` was absent
- output: external `WO-REB-008-6eb13f6-publication-view.json`
- observation schema: `se-harness-predecessor-publication-view-v1`
- observation SHA-256: `522d0ea9e1ae3c8fdaf6d113ff64ee2f27e507632603e5f1a0b0bbd887ecd05d`
- complete current validation: 653 artifacts, zero errors, 50 warnings
- predecessor view validation: 651 artifacts, zero errors, 49 warnings
- source/tag/history unchanged: true
- exact omissions and their Git blob, raw SHA-256, byte count, and status: identical to the two-row table above
- canonical sparse-spec SHA-256: `448159eec515975b9e7e946bed2653dbd6811dc4c06fd7b9e9d3a3facbd00332`

The first exact-suite attempt against superseded local commit `33bd2cedd77b32d5d6cadbb832f8590c9a63661c` found one documentation-retirement allowlist failure: the changed-path inventory in this evidence named the retired owner-context path literally. The inventory was rewritten descriptively inside this already authorized evidence path and the single local candidate commit was amended to the initial identity above. Focused regression and full exact-commit qualification then passed.

## Final hosted-qualification successor

The reviewed workflow correction was committed on top of the initial implementation without changing its adapter, release identities, distribution bytes, rejected history, tag, or root evaluator:

- source commit: `397a7e5ac09109f8836de979157f15b0cf451e28`
- source tree: `dd57ce33d27e783cf9bf38c2180e24005d1c4075`
- parent implementation commit: `6eb13f60cc84755190bc69b5ceb09a5e2a37fd7a`
- successor diff: exactly `.github/workflows/candidate-evidence.yml`, `.github/workflows/predecessor-evaluator-assessment.yml`, `tests/test_predecessor_assessment_contract.py`, and `tests/test_standard_repository_lifecycle.py`
- source checkout: fresh short-path detached clone with canonical-LF checkout; stopped untracked `RLS-SEH-008` absent
- output: external `WO-REB-008-397a7e5-publication-view.json`
- observation schema: `se-harness-predecessor-publication-view-v1`
- observation SHA-256: `be2c310622297c2ae9968e5653aeaea7457652fe6d504760c3afb2345fed4de1`
- complete current validation: 653 artifacts, zero errors, 50 warnings
- predecessor view validation: 651 artifacts, zero errors, 49 warnings
- exact omissions and their Git blob, raw SHA-256, byte count, and status: identical to the two-row table above
- canonical sparse-spec SHA-256: `448159eec515975b9e7e946bed2653dbd6811dc4c06fd7b9e9d3a3facbd00332`
- source/tag/history unchanged: true

Focused workflow and adapter regression passed 28 tests. The full isolated exact-commit suite passed 452 tests with seven declared platform skips in 215.946 seconds. Candidate graph validation passed with 653 artifacts, zero errors, and 50 warnings. Release-distribution validation passed with one record; portable release-surface validation, diff checks, and detached-checkout cleanliness also passed.

## Verification results

Released 0.5.0 review preflight also passed in the exact two-omission projection with `ready = true`, no diagnostics, work order `in_progress`, and the same 15-path governing manifest.

| Check | Result |
| --- | --- |
| Focused publication, release-workflow, and Pages-workflow tests | 15 passed |
| `VER-REB-004` / `VER-REB-005` predecessor regressions | 17 passed, 2 POSIX-only cases skipped on Windows |
| Full isolated clean-review suite | 451 passed, 7 platform cases skipped |
| Candidate complete graph in stopped-content-free review projection | 653 artifacts, 0 errors, 50 warnings |
| Released 0.5.0 complete-checkout refusal in the same projection | 653 artifacts, exact E009 + two E010 errors, 48 warnings |
| Released 0.5.0 `doctor` | passed |
| Candidate-source `doctor` | expected managed-root/template drift because candidate templates lead the separately locked released root; no managed write |
| Release-distribution validation | passed; 1 distribution-bearing record |
| Portable release surface | passed |
| CLI/help and Python compilation | passed |
| Harness Explorer review | 653 artifacts, 2395 relations, 0 errors; manifest `6a3f95254d1d7a2a687288013b4a64f943155acd3c4756764362d0eff0022ef3` |
| Diff whitespace check | passed |

Exact final-successor qualification:

| Check | Result |
| --- | --- |
| Corrective focused regression, including the documentation-retirement allowlist | 51 passed |
| Full isolated exact-commit suite | 452 passed, 7 platform cases skipped |
| Candidate complete graph | 653 artifacts, 0 errors, 50 warnings |
| Publication predecessor-view adapter | passed; 651 artifacts, 0 errors, 49 warnings; exact rejected pair only |
| Released 0.5.0 complete-checkout observation | expected refusal: 653 artifacts, exact E009 + two E010 errors, 48 warnings |
| Released 0.5.0 `doctor` | passed |
| Release-distribution validation | passed; 1 distribution-bearing record |
| Portable release surface over repository, released wheel, and installed CLI | passed |
| CLI help and Python compilation | passed |
| Commit diff whitespace and detached-checkout cleanliness | passed |

## Hosted corrective-branch assessment

Dedicated branch `candidate/0.6.0-publication-fix` was created and pushed at exact commit `6eb13f60cc84755190bc69b5ceb09a5e2a37fd7a`. The push triggered three read-only workflows; all failed closed before any package or privileged publication job could run:

| Workflow | Run / job | Exact retained boundary |
| --- | --- | --- |
| Predecessor Evaluator Assessment | run `32590627632`, job `97073786412` | `assess_predecessor_evaluator.py` was still called with rejected `REL-SEH-010`; it refused with `bootstrap requires one approved release_contract`. The approved successor is `REL-SEH-011`. |
| Engineering Harness | run `32590627652`, job `97073786491` | released 0.5.0 `doctor` passed, then direct complete-checkout validation retained the known 653-artifact E009/two-E010 refusal with 48 warnings. |
| SE Harness Candidate Evidence | run `32590627675`, source job `97073786505` | the 452-test Linux suite reached one error because default depth-1 checkout did not contain preparation commit `619d6aea8054e802e5c4ac8c8e586a253bb3661b`; package evidence was skipped. |

The first failure identifies stale release-contract selection in the predecessor-assessment workflow. The second is the existing managed released-governor boundary. The third identifies missing full-history checkout for the new retained-history replay test. Correcting any of those workflow surfaces exceeds the reviewed 17-path `WO-REB-008` candidate and therefore requires a separately reviewed scope decision. No rerun or publication workflow dispatch was attempted.

### Authorized two-workflow amendment review

The owner authorized a bounded amendment covering the predecessor-assessment and candidate-evidence workflows plus their two explicit contract-test files. Local review added full-history credential-free checkouts, selected approved `REL-SEH-011`, and updated the tests to enforce those values. Focused tests passed 28/28; the clean four-path projection passed all 452 tests with 7 platform skips, candidate validation with 653 artifacts/zero errors/50 warnings, release-distribution validation with one record, portable-surface validation, and diff checks.

The exact full-history local replay of the amended predecessor command then failed closed with `legacy full-checkout refusal differs from exact E009`. This is a retained contract conflict rather than missing history: `REL-SEH-011` requires the pre-release legacy observation to contain only E009, while the post-release complete checkout now produces E009 plus the two E010 duplicate-version diagnostics bound above. Merely replacing rejected `REL-SEH-010` with `REL-SEH-011` therefore cannot make the post-release assessment lane green. The four-path amendment remains uncommitted and was not pushed or rerun; an alternate predecessor-lane semantic requires separate review.

### Final successor semantic and hosted result

The final reviewed successor makes the hosted predecessor lane exercise the same post-release `RLS-SEH-012` publication adapter used by the three publication validation points. Both hosted checkouts use full history with persisted credentials disabled. This preserves the older `REL-SEH-011` observation as immutable pre-release evidence instead of incorrectly replaying it against later released history.

Dedicated branch `candidate/0.6.0-publication-fix` was advanced to exact commit `397a7e5ac09109f8836de979157f15b0cf451e28`. Hosted results were:

| Workflow | Run / job | Result |
| --- | --- | --- |
| SE Harness Candidate Evidence | run `32594275919`; source job `97082695051`; package job `97082780881` | passed exact source and package qualification |
| Predecessor Evaluator Assessment | run `32594275925`; job `97082695071` | passed the complete release and exact predecessor publication view |
| Engineering Harness | run `32594275934`; job `97082695102` | expected-red released-0.5 complete-checkout boundary: 653 artifacts, exact E009 plus two E010 errors, 48 warnings |

The successful predecessor artifact is `predecessor-evaluator-assessment`, artifact ID `9481131901`, size 2,593 bytes, digest `sha256:29d6c6fd5a2bb3015d9f385c720553acf2f97dc2e0cd05d8d48d72e111011565`, retained until 2026-11-20. The candidate workflow uploaded no artifact because both required jobs completed directly. The obsolete managed-root lane remains intentionally diagnostic for the separately locked 0.5 governor; it is not the replacement publication qualification lane and does not invalidate the two successful exact-candidate lanes.

The first full-suite attempt in the operational checkout produced three environmental failures: two dashboard tests observed the stopped untracked `RLS-SEH-008`, and one source-identity test observed an unrelated editable distribution outside this checkout. The exact failed tests passed in the stopped-content-free review projection; the complete isolated suite there passed as recorded above.

Negative coverage includes changed preparation evidence before predecessor execution, credential contamination, nonempty `PYTHONPATH`, alternate Git configuration, closed CLI inputs, output collision/location/canonicalization, exact rejected-pair replay, linked external-path regressions, sparse-omission substitution, payload mismatch, diagnostic drift, TOCTOU rollback, and exclusive-write/cleanup boundaries.

## Changed paths under review

- `.github/workflows/publish-dashboard-pages.yml`
- `.github/workflows/publish-pypi.yml`
- `.github/workflows/candidate-evidence.yml`
- `.github/workflows/predecessor-evaluator-assessment.yml`
- `repository_tools/predecessor_publication.py`
- `scripts/validate_predecessor_publication_view.py`
- `tests/test_predecessor_publication.py`
- `tests/test_predecessor_assessment_contract.py`
- `tests/test_release_orchestration.py`
- `tests/test_dashboard_publication.py`
- `tests/test_standard_repository_lifecycle.py`
- repository owner-context note at the retired repository-context path
- `docs/notes/developing-se-harness.md`
- `docs/notes/harnessctl-reference.md`
- `docs/engineering/released-evaluator-boundary/requirements/REQ-REB-015.md`
- `docs/engineering/released-evaluator-boundary/specifications/SPEC-REB-007.md`
- `docs/engineering/released-evaluator-boundary/architecture/ARCH-REB-006.md`
- `docs/engineering/released-evaluator-boundary/architecture/adr/ADR-REB-006.md`
- `docs/engineering/released-evaluator-boundary/verification/VER-REB-006.md`
- `docs/engineering/released-evaluator-boundary/work-orders/WO-REB-008.md`
- `docs/engineering/released-evaluator-boundary/evidence/WO-REB-008-publication-view.md`

The user-owned stopped file `docs/engineering/release-0-6-0/releases/RLS-SEH-008.md` remains outside scope and unchanged at SHA-256 `eea7a9953767e6b817754a517db72a2484561462fce1c9e440c5e5d1501a75fc`.

## Pending gates and actions not performed

The final corrective successor is exact commit `397a7e5ac09109f8836de979157f15b0cf451e28` on local and remote branch `candidate/0.6.0-publication-fix`. Exact local and replacement hosted qualification passed as recorded above. At evidence closeout, `WO-REB-008` lifecycle completion, commit-bound VREC preparation/review, integration to trusted `main`, and publication retry remain later governance actions. No tag movement, GitHub Release, PyPI publication, Pages deployment, maintenance mutation, root mutation, distribution rebuild, or external-policy change occurred during corrective qualification.
