# WO-REB-005 LF-stability and rejected-bootstrap-history evidence

## Outcome and authority boundary

The exact C3 candidate for `WO-REB-005` passes local and hosted exact-candidate qualification. It preserves canonical evaluator-evidence JSON across supported Git checkout settings and lets the candidate validator retain only an exact `rejected` predecessor-bootstrap RLS plus its exact `rejected` declaring contract as terminal history. Ready and released bootstrap records still require their exact `approved` contract, and binder/publication code still refuses every non-approved contract.

The accountable owners approved `REQ-REB-009`, `REQ-REB-010`, `SPEC-REB-004`, `ARCH-REB-003`, `ADR-REB-003`, `VER-REB-003`, and `WO-REB-005`. Their `draft -> approved` events were recorded at `2026-08-21T17:46:21Z`, and `WO-REB-005` entered `in_progress` at `2026-08-21T17:48:51Z` after released-0.5 start preflight passed. After exact local and hosted qualification, the engineering owner transitioned only `WO-REB-005` from `in_progress` to `implemented` at `2026-08-21T21:41:30Z`. `REL-SEH-009` remains `draft`, `RLS-SEH-009` remains `ready`, and `REL-SEH-008` remains `approved`; their dispositions remain deferred pending separately authorized lifecycle actions.

The release owner subsequently amended the draft 0.6.0 successor scope from ten to twelve work orders after verified `WO-IAR-012` and `WO-DST-021` were integrated from main. The future aggregate must therefore cover twelve work orders, thirteen keyed evidence paths, and eleven verification contracts; cross-domain `WO-DST-021` contributes two evidence paths and two contracts. Historical C1/C2 contracts, VRECs, RLS records, and their exact scopes remain unchanged, while `WO-HUP-001`, `WO-RCA-001`, and `WO-VSP-006` retain their prior exclusion from the release-bearing aggregate.

One authorized operational candidate commit and one dedicated candidate-branch push occurred. Existing configured Git credentials were used only for that push, and the resulting hosted qualification was read without external mutation. No VREC/RLS preparation or release transition, tag, publication, deployment, maintenance mutation, external-policy change, or root-evaluator upgrade occurred. The stopped untracked `RLS-SEH-008` proposal remains unmodified and is excluded from clean-snapshot qualification.

## Trigger and retained failure

- Candidate C2 is `b033827cc9f8357a7afb1d82f336c6fe2fc16e26`.
- Canonical `RLS-SEH-009` evaluator evidence has SHA-256 `11a4aec338f1da102a112faca6589d18541e115e139e695e8d66e4d509125404`.
- A default Windows checkout without the corrected policy produced CRLF bytes with SHA-256 `7881148c63f6e8e7edf701dff36b2efe5f8c6dd4caebe3e18e2a4bb8f5ebc4d4`; candidate validation correctly raised `E012` for the bound raw-byte digest mismatch.
- The LF control checkout passed.
- The attempted zero-write disposition transaction exposed the second defect: once the bootstrap contract became rejected, the candidate validator required the rejected RLS to retain an approved contract. The transaction failed atomically and changed no lifecycle state.

The retained `RLS-SEH-009` record, evaluator sidecar, and `REL-SEH-008` currently hash to `543f09879683f39955bb27c3a4586630fc476106a02deb8f81a450a14d775dcd`, `11a4aec338f1da102a112faca6589d18541e115e139e695e8d66e4d509125404`, and `050ca3f793365e005679e00eeaf462efffb1e597f61c9b092d20d72c707d5157`, respectively. They have no working-tree diff.

## Approved preflight and lifecycle mechanics

Released SE Harness 0.5.0 start preflight reported `ready: true` with no diagnostics. Its complete reading manifest was:

- `ENGINEERING_HARNESS.md`
- `docs/engineering/REPOSITORY_CONTEXT.md`
- `docs/engineering/README.md`
- `docs/engineering/WORKFLOW.md`
- `docs/engineering/DECISION_RIGHTS.md`
- `docs/engineering/QUALITY_GATES.md`
- `docs/engineering/TRACEABILITY.md`
- `docs/engineering/released-evaluator-boundary/intent/INT-REB-001.md`
- `docs/engineering/released-evaluator-boundary/capabilities/CAP-REB-001.md`
- the seven approved `REQ-REB-009`, `REQ-REB-010`, `SPEC-REB-004`, `ARCH-REB-003`, `ADR-REB-003`, `VER-REB-003`, and `WO-REB-005` paths.

Released 0.5.0 has no `transition` command. Candidate `transition --apply` correctly refused ordinary mutation against the operational schema-2 lock with `MG002`; it did not write. The authorized events were therefore recorded only after the candidate read-only transition plan and released-governor preflight agreed. This did not change the root evaluator or its lock.

## Implemented behavior

The candidate root contains this single managed attribute rule:

```gitattributes
docs/engineering/**/evidence/*.json text eol=lf
```

The root managed block SHA-256 is `fba4cf22b45939f8c705f2a9c3bd964408b5003d0599993e72735ce865b97e3b`; the canonical installer fragment SHA-256 is `38e401b81d4abf8c36fb055b6a51d174eca713b28cd9ee2f64f8e362428d80e7`. Fresh installs render the exact root block and bind it as lock mode `fragment` with that same managed-block digest.

The candidate/template validator selects the exact declaring contract status from the release record status: `rejected` records require their exact `rejected` contract; all ready/released operational records retain the existing exact `approved` requirement. Status-matched claimant cardinality, tuple validation, ID/version equality, canonical evidence parsing, raw SHA-256, and current-lock matching rules remain intact. Rejected history does not match the current root lock, but its immutable evidence must still match the declaring tuple. No evidence normalization was introduced.

The repository binder already parses only `status = "approved"` contracts. Dashboard publication already resolves only the single exact approved bootstrap contract. New tests explicitly preserve those denials for `rejected` contracts.

## Exact implementation and governance paths

Candidate/package behavior:

- `.gitattributes`
- `templates/repository/standard/gitattributes.fragment`
- `templates/repository/standard/scripts/validate_engineering_artifacts.py`
- `tests/test_context_routing_retirement.py`
- `tests/test_release_bootstrap.py`
- `tests/test_standard_repository_lifecycle.py`
- `docs/notes/developing-se-harness.md`
- `docs/notes/harnessctl-reference.md`

Approved packet and retained evidence:

- `docs/engineering/released-evaluator-boundary/requirements/REQ-REB-009.md`
- `docs/engineering/released-evaluator-boundary/requirements/REQ-REB-010.md`
- `docs/engineering/released-evaluator-boundary/specifications/SPEC-REB-004.md`
- `docs/engineering/released-evaluator-boundary/architecture/ARCH-REB-003.md`
- `docs/engineering/released-evaluator-boundary/architecture/adr/ADR-REB-003.md`
- `docs/engineering/released-evaluator-boundary/verification/VER-REB-003.md`
- `docs/engineering/released-evaluator-boundary/work-orders/WO-REB-005.md`
- this evidence file.

Draft `REL-SEH-009` is retained as a non-authoritative successor proposal and was not approved or transitioned. Untracked stopped `RLS-SEH-008` is outside this path set.

The operational `.engineering-harness.toml`, `.engineering-harness.lock`, root `scripts/validate_engineering_artifacts.py`, released evaluator, and maintenance state have zero diff.

## Local verification

| Command or check | Result |
| --- | --- |
| Focused bootstrap plus checkout suite | PASS: 25 tests in 10.793 seconds |
| Pre-main clean LF projection, Python 3.14.6 | PASS: 393 tests in 179.510 seconds; 5 declared Windows privilege/symlink skips |
| Pre-main clean LF projection, Python 3.11.9 | PASS: 393 tests in 179.743 seconds; same 5 skips |
| Post-main LF Git worktree, Python 3.14.6 | PASS: 427 tests in 195.205 seconds; 5 declared Windows privilege/symlink skips |
| Post-main LF Git worktree, Python 3.11.9 | PASS: 427 tests in 193.840 seconds; same 5 skips |
| Post-main candidate formal validator | PASS: 628 artifacts, 0 errors, 47 pre-existing maintenance warnings |
| Post-main released-0.5 validator | PASS: 628 artifacts, 0 errors, same 47 warnings |
| Released-0.5 start and review preflight | PASS: ready, no diagnostics; work remains `in_progress` pending exact/hosted evidence |
| Released-0.5 inspection | PASS: 615 artifacts, 2,230 relations, 0 error findings; `WO-REB-005` is the sole active work item |
| Released-0.5 doctor | PASS: required, distribution-parity, and managed-integrity checks; pre-existing location warnings only |
| Release-distribution policy | PASS: 0 distribution-bearing records |
| Portable repository and wheel surface | PASS |
| Changed-Python compilation and `git diff --check` | PASS |
| Git checkout matrix | PASS: `core.autocrlf=true`, `input`, and `false`, each with CRLF-oriented checkout defaults, retained identical LF bytes and digest |
| Attribute-conflict negative | PASS: a nested `eol=crlf` override resolves as CRLF and is rejected by the qualification assertion |
| Evidence-byte negatives | PASS: CRLF with the LF digest fails raw hashing; substituting the CRLF digest still fails canonical JSON validation |
| Bootstrap lifecycle matrix | PASS only for `ready + approved` and `rejected + rejected`; missing, wrong, and mixed pairs fail |
| Rejected binder/publication authority | PASS: both refuse before mutation or credential-bearing work |

The initial clean qualification projection was based on local governance HEAD `39302d8ae2e04939c63718a32233c0f937916b14`, tree `f254f2fbbb3bb56f61e87ee7ff501f6cc4d6c009`, and provisional `SOURCE_DATE_EPOCH=1787333439`. After the release-scope amendment, local merge commit `3fa7777` integrated `origin/main` commit `1d32c97`, including verified `WO-IAR-012` and `WO-DST-021`. The post-main replay used a detached LF Git worktree at `3fa7777` with the uncommitted C3 overlay and stopped `RLS-SEH-008` excluded. Both projections are test inputs, not C3 identity. Git is `2.45.1.windows.1`.

## Pre-main provisional package and reproducibility evidence

Two builds from the same uncommitted LF projection produced byte-identical wheels and, after the required normalization, byte-identical sdists:

- wheel `se_harness-0.6.0-py3-none-any.whl`: SHA-256 `c2d443218b1cd8b3518f0a5d62e7fec0ed59c511a647c977672a4cfb6cf86e25`
- normalized `se_harness-0.6.0.tar.gz`: SHA-256 `350eb7dbf2e4c8b9e52921cdc9a3b240ceaafd3ea1eac7c0e980068589c80522`
- offline no-isolation rebuild from the normalized sdist reproduced wheel SHA-256 `c2d443218b1cd8b3518f0a5d62e7fec0ed59c511a647c977672a4cfb6cf86e25`.

The wheel contains the exact attribute fragment and historical-validator branch. Fresh offline wheel installs on Python 3.14.6 and 3.11.9 both passed `init`, installed-template/lock parity, `doctor`, and validation. These identities predate the mainline integration and no longer characterize the amended twelve-work-order candidate. They are retained as preliminary history only; no exact candidate commit, candidate-source/package identity claim, release bundle, checksum declaration, or aggregate record can be created from them.

## Post-main provisional package and reproducibility evidence

Two independent canonical-LF source copies of merge base `3fa77770ae8589fe623872f22345c6c9c076c6c4` plus the same uncommitted C3 overlay were built with provisional `SOURCE_DATE_EPOCH=1787340825`. The stopped `RLS-SEH-008` proposal was excluded. Both builds produced identical artifacts:

- wheel `se_harness-0.6.0-py3-none-any.whl`: SHA-256 `b097bd287b3a9e63cec79f0e5363a44f72cb3fea1ebcca71b2f73cc039050392`;
- normalized `se_harness-0.6.0.tar.gz`: SHA-256 `41392561328f435ebdf955787bc0358808256781d626a26ed77e3b739bfab10c`; and
- offline no-isolation reconstruction from that normalized sdist reproduced wheel SHA-256 `b097bd287b3a9e63cec79f0e5363a44f72cb3fea1ebcca71b2f73cc039050392`.

The wheel passed the portable-release-surface check. Fresh isolated installs on Python 3.14.6 and Python 3.11.9 both installed version `0.6.0`, initialized a disposable standard repository with the retired repository-context seed absent, matched every packaged managed file including `.gitattributes`, passed `doctor`, and passed artifact validation. These artifacts remain non-promotable provisional evidence because they were produced before the exact C3 candidate commit existed.

## Exact C3 candidate and retained local replay

The authorized operational C3 candidate is commit `2ab1c1fffd2c0a2f462e7affcb9ea6f426b202e5`, with parent `3fa77770ae8589fe623872f22345c6c9c076c6c4`, tree `c3f1585a2b42f25398bf5a5057097dfd21c4c76d`, and commit epoch `1787342263`. Its commit contains exactly the reviewed seventeen-path C3 set. The root operational evaluator/configuration and maintenance state remain untouched, and the stopped untracked `RLS-SEH-008` is absent from the tree. Two independent ZIP exports of the exact commit were byte-identical with SHA-256 `a5e0b3ea46253b257d4688e76b149cfa5b3d0a4133315c7477b4976892c0f15f`. Their extracted canonical `RLS-SEH-009` evaluator evidence retained SHA-256 `11a4aec338f1da102a112faca6589d18541e115e139e695e8d66e4d509125404` under the LF attribute policy.

Candidate-source identity passed for version `0.6.0`, the exact commit, the detached checkout root, and source/template/distribution origins wholly inside that checkout. Released evaluator 0.5.0 identity and doctor passed, with only the pre-existing location warnings. Its validator passed 628 artifacts with 0 errors and 47 pre-existing maintenance warnings; its `WO-REB-005` review preflight remained ready with no diagnostics and did not change the work order from `in_progress`. The candidate validator independently passed the same 628 artifacts with 0 errors and 47 warnings. Release-distribution policy passed with 0 distribution-bearing records, and the portable source surface passed.

The full exact-source suite passed on both supported runtimes:

- Python 3.14.6: 427 tests in 203.806 seconds, with 5 declared Windows privilege/symlink skips.
- Python 3.11.9: 427 tests in 198.407 seconds, with the same 5 skips.

Two independent exact-export builds produced byte-identical release files:

- wheel `se_harness-0.6.0-py3-none-any.whl`: SHA-256 `2a8daa2eca4a04fd62c93443f74a9d8cafbd358219ba0d99315c9fe9c81c3dfb`;
- normalized sdist `se_harness-0.6.0.tar.gz`: SHA-256 `a9136c61937d6b2738e214fc2e4006906f50e531a288b6ab024b7b249fc4513f`; and
- an offline no-isolation reconstruction from the normalized sdist reproduced the exact wheel SHA-256 `2a8daa2eca4a04fd62c93443f74a9d8cafbd358219ba0d99315c9fe9c81c3dfb`.

The exact bundle manifest passed canonical parsing and bound the candidate commit, epoch, wheel, sdist, checksum bytes, and Git source manifest. Its SHA-256 is `a29718bb2f10689039c6121f15f2d04772f1d36df5e3f63efaac37e4da87519d`; the canonical `SHA256SUMS` content has SHA-256 `cde97da846b18676047ddde704cb80606c5c1aa963d07ebfc467b6d993d4acc6`; and the exact Git source manifest has SHA-256 `916e372022b0824d81ab3944e3826207bcfcba8b2d69f67d83a5a20e6d4bded9`.

Fresh isolated installs of the exact wheel on Python 3.14.6 and Python 3.11.9 both passed candidate-package identity bound to the exact commit, the portable installed surface, fresh standard-repository `init`, `doctor`, `validate`, Explorer dashboard generation, safe `upgrade --apply`, and retired-command absence. Released evaluator 0.5.0 wheel SHA-256 `974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f`, contract SHA-256 `a443e93d6da7d0538bdf790a16f4dea49ac7a6ede384c65e40362627d7a84b75`, accepted the exact candidate wheel and commit in all 10 verifier-owned scenarios on both runtimes. The Python 3.14.6 acceptance manifest has SHA-256 `3da02187b548f4b5ea08606bb4d57a2771573148f0c13092667534dc86ee79bb`; the Python 3.11.9 manifest has SHA-256 `dd135f728ad7c6f6aa04c160c0a029a100e50f37e995198f7140cc48ee7dffcb`.

The detached exact checkout remained clean after source, package, verifier, distribution, and bundle replay. Candidate identity remains unchanged.

## Hosted C3 qualification and completion

Dedicated branch `candidate/0.6.0-c3` was created and pushed at exact commit `2ab1c1fffd2c0a2f462e7affcb9ea6f426b202e5`; a subsequent read-only remote-ref check returned the same full object ID. The push triggered exactly the expected workflows:

- [SE Harness Candidate Evidence run 32529057484](https://github.com/mmzen/se_harness/actions/runs/32529057484) completed successfully. Candidate source evidence job `96917222445` passed in 1 minute 7 seconds, and candidate package evidence job `96917488942` passed in 19 seconds.
- [Engineering Harness run 32529057501](https://github.com/mmzen/se_harness/actions/runs/32529057501) completed successfully. Released-evaluator validation job `96917222630` passed in 14 seconds against the same exact branch and commit.

GitHub emitted only its platform deprecation notice for Node.js 20-based `actions/checkout@v4` and `actions/setup-python@v5`; it reported no candidate failure. The engineering-owner completion decision then changed only `WO-REB-005` from `in_progress` to `implemented`. A clean candidate-plus-governance projection excluded stopped `RLS-SEH-008`, passed both candidate and released-0.5 formal validation at 628 artifacts, 0 errors, and the same 47 pre-existing maintenance warnings, passed release-distribution policy with 0 selected records, and passed released-0.5 review preflight with status `implemented` and no diagnostics. That completion records finished implementation and retained evidence; it does not verify the work or transition a VREC or RLS.

## Deviations and remaining qualification

- The first full run in the operational checkout produced four environmental failures: two dashboard tests saw the intentionally retained untracked `RLS-SEH-008`, candidate-source identity saw unrelated globally installed distribution metadata, and one machine-contract byte comparison saw the checkout's pre-existing CRLF representation. The same final source replayed in an LF projection without the stopped proposal and with uninstalled interpreters passed all 393 tests on both runtimes.
- The first post-main archive projection produced four non-product failures: it lacked Git metadata, exposed globally installed distribution metadata, retained one CRLF managed JSON representation, and correctly identified this evidence file as one additional recorded mention of the retired repository-context path. A real detached LF Git worktree with isolated Python environments and the bounded retirement-test allowance passed all 427 tests on both runtimes.
- The first offline-rebuild invocation supplied an empty `SOURCE_DATE_EPOCH` because Git was queried from the parent work directory. It failed before producing a wheel. Repeating it with the projection selected produced the exact expected wheel digest.
- Five skips on each runtime require unavailable Windows symlink/privilege facilities. Explicit path/link refusal and all ordinary supported paths pass.
- Candidate workflow annotations are limited to GitHub's non-blocking Node.js action-runtime deprecation notice; no product qualification failure remains open.

## Next accountable action

Review and separately authorize or withhold the deferred `RLS-SEH-009`/`REL-SEH-008` dispositions and successor-contract decision. Aggregate `VREC-SEH-010` and successor RLS preparation remain later, separately governed actions.
