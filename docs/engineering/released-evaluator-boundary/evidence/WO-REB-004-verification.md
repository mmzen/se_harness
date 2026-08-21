# WO-REB-004 local implementation and qualification evidence

## Outcome and authority boundary

The bounded local C2 implementation for `WO-REB-004` passes its pre-candidate qualification. It provides one contract-bound predecessor-evaluator bootstrap for the first 0.6.0 release record while preserving released 0.5.0 as the operational governor and leaving the normal schema-3 release rule unchanged everywhere else.

The accountable owners approved `REQ-REB-008`, `SPEC-REB-003`, `ARCH-REB-002`, `ADR-REB-002`, `VER-REB-002`, `WO-REB-004`, and `REL-SEH-008`, authorized their `draft -> approved` transitions and the start of `WO-REB-004`, and on 2026-08-21 at `2026-08-21T16:31:42Z` authorized only the canonical-LF correction across those seven records while preserving their statuses and every other scope boundary. The six non-work-order records remain `approved`; after exact local and hosted qualification, `WO-REB-004` separately transitioned from `in_progress` to `implemented` at `2026-08-21T17:09:35Z`.

After separate authorization, one local operational replacement-candidate commit containing exactly the 20 reviewed paths was created as `b033827cc9f8357a7afb1d82f336c6fe2fc16e26`. A later exact-ref authorization used the configured Git credential only to create and push `candidate/0.6.0-c2` at that commit and trigger the successful hosted lanes; historical `candidate/0.6.0` did not move. No other push or credential use, VREC or RLS preparation or transition, tag, publication, deployment, maintenance mutation, external-policy change, or root-evaluator upgrade occurred. The stopped untracked `RLS-SEH-008` proposal was excluded from the commit and every clean-snapshot qualification input and remains unmodified.

## Implemented boundary

- `REL-SEH-008` owns one closed bootstrap tuple for future `RLS-SEH-009`: release 0.6.0, schema-2 predecessor lock, canonical `utf8-text-lf-v1` lock SHA-256 `08441ec0b4825db4c017ce4169f23092162995ff06476004d267f0671c7443b3`, released evaluator 0.5.0, wheel `se_harness-0.5.0-py3-none-any.whl`, and wheel SHA-256 `974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f`.
- `repository_tools/release_bootstrap.py` parses the closed contract, enforces global single-bootstrap cardinality, checks the exact ready-RLS graph, canonical predecessor lock, public wheel, isolated installed 0.5.0 identity, installed payload/wheel parity, and released validation, and emits canonical evaluator evidence.
- `scripts/bind_release_bootstrap.py` exposes a read-only plan by default and an explicit `--apply` mode. Apply may exclusively create only the work-order-scoped evaluator sidecar and atomically add its binding to the named ready RLS; collision, partial state, concurrent change, or replacement failure fails closed with rollback.
- The candidate formal validator accepts schema 2 only for the exact approved bootstrap record and tuple. Ordinary ready release records still require schema 3, reuse is rejected, and a bootstrap record becomes historical after the root reaches schema 3.
- Dashboard publication resolves the bootstrap only from the exact governance commit, reads Git bytes without checkout line-ending smudging, rechecks the same canonical tuple and evidence, and invokes only the independently installed released evaluator.
- PyPI and dashboard workflows pass the exact release record to evaluator resolution and capability-negotiate the released 0.5.0 identity CLI. They always check the wheel digest and pass a payload flag only when the selected released evaluator supports it.
- Candidate templates lead the separately locked root only on this narrowly declared release-format feature. Root managed files and the operational schema-2 lock remain byte-unmodified.

## Canonical-LF correction evidence

The Windows checkout reports `.engineering-harness.lock` as `i/lf w/crlf`. Its platform-smudged working bytes are 5,634 bytes with SHA-256 `c4c4191998cad431620324dba2ad205c190fcf2802847278cabec92e853989af`; canonical `utf8-text-lf-v1` bytes are 5,490 bytes with SHA-256 `08441ec0b4825db4c017ce4169f23092162995ff06476004d267f0671c7443b3`.

Tests prove that UTF-8 LF, CRLF, and CR encodings of otherwise identical lock text have that one canonical identity. Invalid UTF-8, a BOM, field or content drift, wrong version/schema, and every non-line-ending change fail closed. The approved records bind only the canonical digest; their relations, statuses, trust direction, and mutation boundaries are unchanged.

## Exact changed paths

Implementation and publication integration:

- `.github/scripts/publish_dashboard.py`
- `.github/workflows/publish-dashboard-pages.yml`
- `.github/workflows/publish-pypi.yml`
- `repository_tools/release_bootstrap.py`
- `scripts/bind_release_bootstrap.py`
- `templates/repository/standard/scripts/validate_engineering_artifacts.py`
- `docs/notes/developing-se-harness.md`
- `docs/engineering/release-0-6-0/README.md`

Approved governance packet:

- `docs/engineering/released-evaluator-boundary/requirements/REQ-REB-008.md`
- `docs/engineering/released-evaluator-boundary/specifications/SPEC-REB-003.md`
- `docs/engineering/released-evaluator-boundary/architecture/ARCH-REB-002.md`
- `docs/engineering/released-evaluator-boundary/architecture/adr/ADR-REB-002.md`
- `docs/engineering/released-evaluator-boundary/verification/VER-REB-002.md`
- `docs/engineering/released-evaluator-boundary/work-orders/WO-REB-004.md`
- `docs/engineering/release-0-6-0/release/REL-SEH-008.md`
- this evidence file

Verification support:

- `tests/test_release_bootstrap.py`
- `tests/test_dashboard_publication.py`
- `tests/test_pypi_publishing.py`
- `tests/test_release_orchestration.py`

The untracked `docs/engineering/release-0-6-0/releases/RLS-SEH-008.md` is expressly outside this path set.

## Automated verification

| Command or check | Result |
| --- | --- |
| Focused bootstrap, publication, PyPI, and release-orchestration suite | PASS: 69 tests in 25.342 seconds |
| Full suite, Python 3.14.6, clean canonical-LF snapshot | PASS: 389 tests in 195.457 seconds; 5 expected Windows privilege/symlink skips |
| Full suite, Python 3.11.9, same snapshot | PASS: 389 tests in 190.677 seconds; the same 5 skips |
| Candidate and released-0.5 formal validation | PASS: 605 artifacts, 2,175 relations, 0 errors, 45 pre-existing maintenance warnings |
| Released-0.5 review preflight for `WO-REB-004` | PASS: ready, no diagnostics |
| Release distribution policy | PASS: 0 distribution-bearing records; no released RLS was created |
| Candidate and released inspection | PASS: 605 artifacts, 2,175 relations, 0 error findings; 45 validation warnings |
| Repeated dashboard generation | PASS: identical canonical manifest SHA-256 `ceeeaefea7bde9cb2393371778890ca74fdb8e9c01b54900e667fc1b69c864c6` |
| `git diff --check` and changed-Python compilation | PASS |
| Secret-like material and absolute host-path scans over the bounded path set | PASS: no matches |
| Root managed-surface comparison | PASS: lock, root configuration/guide, root validator, root generator, and root inspector unchanged |

The focused tests include closed-parser key/type/order coverage; single-contract cardinality; LF/CRLF/CR equivalence; invalid UTF-8 and BOM rejection; lock, wheel, installed-payload, identity-origin, RLS, relation, and evidence drift; external identity with `PYTHONPATH` removed; read-only planning; exclusive creation; atomicity, rollback, collision refusal, and idempotent replay; exact candidate schema-2 acceptance; non-reuse and historical behavior; publication commit-byte resolution; tamper/cardinality failure; and workflow compatibility with the released 0.5.0 CLI.

## Disposable exact-source projection

Qualification used a fresh canonical-LF local snapshot that omitted the stopped RLS proposal. Its disposable Git identity is commit `31e92654c04fe150d5c84a057ff1c470da5a3eb3`, tree `be361f948fb7dfe52244ef00c106786e074c96ca`, with `SOURCE_DATE_EPOCH=1787330206`. Candidate-source identities passed on Python 3.14.6 and 3.11.9 with source, distribution, and template origins inside that exact projection, no `PYTHONPATH`, and disabled user site.

This disposable commit is a test fixture only and was never an operational candidate. The later authorized replacement candidate is `b033827cc9f8357a7afb1d82f336c6fe2fc16e26`; candidate `827b2709292abaa3458bb3b4cac37b582378c585` remains unchanged as the prior candidate identity.

## Reproducible distribution evidence

Two independent exports and builds from the disposable projection produced byte-identical artifacts:

- wheel `se_harness-0.6.0-py3-none-any.whl`: SHA-256 `2b7441b4b186a29ca67eec3bb699cd10378d1e198a784508a41fbfa372668814`
- normalized sdist `se_harness-0.6.0.tar.gz`: SHA-256 `e5735d987e6b92811c0d363629f0d7101a7ae23acc63c112abd7de95aee3f3cc`
- `SHA256SUMS`: SHA-256 `052d3d77256a315ab060f14fdb92f093c69be2b03bf3a897e3148a9df1dafbc8`
- source manifest: SHA-256 `668f9a18e41dcae88566bdcd32d9308e7774432c040e6e124ea31f8c5cb6f76a`
- bundle JSON: SHA-256 `ed0a772fcaa73e20f7b35067a49a2a70534bf6c005752b7d6ec2e50852cd55d6`

An offline, no-isolation wheel build from the normalized sdist reproduced wheel SHA-256 `2b7441b4b186a29ca67eec3bb699cd10378d1e198a784508a41fbfa372668814` exactly. Repository and installed-CLI portable-surface scans passed.

Fresh external candidate-package environments on Python 3.14.6 and 3.11.9 installed that wheel with `--no-deps --no-index`. Both passed isolated `candidate-package` identity with version 0.6.0, the disposable source identity, checkout separation, required launcher, no `PYTHONPATH`, disabled user site, and no diagnostics.

These distribution identities are retained pre-candidate qualification results, not release artifact declarations. They were not reused as exact-candidate evidence; the separately authorized candidate and its replay are recorded below.

## Released-evaluator acceptance

The exact external released evaluator is SE Harness 0.5.0 from public wheel SHA-256 `974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f`. Its independently reconciled installed payload SHA-256 is `d247cc48213b49be52345fcadbf2d93355e5ea7ef15b32014d9fc5010458a2bc`, and verifier contract SHA-256 is `a443e93d6da7d0538bdf790a16f4dea49ac7a6ede384c65e40362627d7a84b75`.

Released identity and doctor checks passed from external environments. Doctor passed required, distribution-parity, and managed-integrity checks; its 16 `W013` location observations are pre-existing non-failing diagnostics.

Released 0.5.0 accepted the exact disposable wheel on both supported test runtimes. Each run passed all 10 scenarios: installed identity, init, adopt, doctor, validate, dashboard, safe upgrade, customized-content refusal, corrupted-integrity refusal, and authority denial.

- Python 3.14.6 acceptance manifest SHA-256: `1e2fc9025c9ff7a2a85176525e28437fa705d1ead496a6a983cf5afa736832b7`
- Python 3.11.9 acceptance manifest SHA-256: `0c5f3b074ad55af1f4fc776fafc407ed34e9ee0e42ff2035509e3dae64616b8c`

## Operational replacement-candidate exact replay

The separately authorized local candidate commit is `b033827cc9f8357a7afb1d82f336c6fe2fc16e26`, tree `0587bfbd364cb7c9423a12bab4c5b23bbd4a3df4`, with `SOURCE_DATE_EPOCH=1787331267`. Its clean LF checkout reported `.engineering-harness.lock` as `i/lf w/lf`, contained the retained pre-candidate evidence, omitted the stopped `RLS-SEH-008`, and had no working-tree changes before qualification.

Exact-candidate qualification results:

| Command or check | Result |
| --- | --- |
| Full suite, Python 3.14.6 | PASS: 389 tests in 201.106 seconds; 5 expected Windows privilege/symlink skips |
| Full suite, Python 3.11.9 | PASS: 389 tests in 205.427 seconds; the same 5 skips |
| Candidate and released-0.5 formal validation | PASS: 605 artifacts, 2,175 relations, 0 errors, 45 pre-existing maintenance warnings |
| Released-0.5 review preflight for `WO-REB-004` | PASS: ready, no diagnostics |
| Release distribution policy | PASS: 0 distribution-bearing records |
| Candidate-source identity, Python 3.14.6 and 3.11.9 | PASS: exact commit and source/template origins, no `PYTHONPATH`, disabled user site, no diagnostics |
| Candidate-package identity, Python 3.14.6 and 3.11.9 | PASS: fresh offline installs, exact commit, isolated Python, required launcher, no diagnostics |
| Released-evaluator identity, Python 3.14.6 and 3.11.9 | PASS: external 0.5.0, exact public wheel, isolated Python, no diagnostics |
| Released-evaluator doctor | PASS: required, distribution-parity, and managed-integrity checks; 16 pre-existing non-failing `W013` observations |
| Candidate and released inspection | PASS: 605 artifacts, 2,175 relations, 0 error findings, 45 warnings |
| Repeated dashboard generation | PASS: identical manifest SHA-256 `933b959f6430cab24914352d26a4e148ef357810a912e36cfa9180d5768a9948` |

Two independent exact-commit exports and builds were byte-identical:

- wheel `se_harness-0.6.0-py3-none-any.whl`: SHA-256 `770d9b43f61ff32e7a4eaa203115610d870491e50291d31f1ac8eb5893a3ccb9`
- normalized sdist `se_harness-0.6.0.tar.gz`: SHA-256 `552e68871ccc23713253b16f5026a42b8245d3b0353ec5a4d69fdc5d037e8a53`
- canonical `SHA256SUMS`: SHA-256 `b4665592ed7a288f43f5cc40457bc3b74f442d1fb27fff3f35861ebd08f24282`
- exact source manifest: SHA-256 `c8f9a85d01da38f68203f4aefd94b728eff01a71ea108502639f316ec1a1b260`
- bundle JSON: SHA-256 `e6debd62af98deadae8e2fc918392392ce31aee17cbe261df58b1537a9ee515b`

An offline no-isolation build from the normalized exact-candidate sdist reproduced wheel SHA-256 `770d9b43f61ff32e7a4eaa203115610d870491e50291d31f1ac8eb5893a3ccb9` exactly. Repository-wheel and installed-CLI portable-surface scans passed.

Released 0.5.0 accepted that exact wheel on Python 3.14.6 and 3.11.9. Both runs passed all 10 functional and refusal scenarios. The exact acceptance manifest SHA-256 values are:

- Python 3.14.6: `dc61992779a6ce3811d5da70426f3897ece74a9455827cfc6a75baa12ee708e5`
- Python 3.11.9: `d7a08bd4cc30c91fe9a32c3b06d2ed4032381523af85467414ad74f0a1ed324a`

## Hosted C2 qualification

The separately authorized branch `candidate/0.6.0-c2` was created and pushed at exact candidate `b033827cc9f8357a7afb1d82f336c6fe2fc16e26`. Historical branch `candidate/0.6.0` remained at `827b2709292abaa3458bb3b4cac37b582378c585`. Only the exact new branch ref was pushed.

All push-triggered hosted lanes completed successfully on attempt 1:

| Workflow / job | Public identity | Result |
| --- | --- | --- |
| SE Harness Candidate Evidence | workflow `338167728`, run `32506378635`, number `102` | PASS |
| Candidate source evidence | job `96847357364`, 2026-08-21T17:06:07Z to 17:07:11Z | PASS |
| Candidate package evidence | job `96847664197`, 2026-08-21T17:07:14Z to 17:07:30Z | PASS |
| Engineering Harness released-0.5 lane | workflow `331720860`, run `32506378834`, number `402` | PASS |
| Engineering Harness `validate` | job `96847357765`, 2026-08-21T17:06:08Z to 17:06:23Z | PASS |

Both workflow runs record event `push`, branch `candidate/0.6.0-c2`, and exact head `b033827cc9f8357a7afb1d82f336c6fe2fc16e26`. Public run URLs are `https://github.com/mmzen/se_harness/actions/runs/32506378635` and `https://github.com/mmzen/se_harness/actions/runs/32506378834`.

This exact-replay and hosted-evidence section is a post-candidate update. It remains uncommitted so that candidate identity `b033827cc9f8357a7afb1d82f336c6fe2fc16e26` is preserved pending a separate retention and work-order completion decision.

## Deviations and residual risks

- The platform checkout smudges LF to CRLF. Initial worktree-based source qualification therefore observed platform-dependent raw bytes. The authorized correction made the intended content identity explicit, and the clean LF projection plus cross-line-ending tests now prove the canonical rule without altering the operational lock.
- Five full-suite skips on each runtime require Windows privileges or symlink/platform facilities unavailable in this session. Supported non-symlink paths and explicit link/traversal refusal tests passed.
- The disposable pre-candidate build and acceptance identities remain historical and were not reused. Exact-candidate identities are separately retained above.
- Hosted candidate-source, candidate-package, and released-0.5 evaluator lanes passed. They do not exercise release publication, OIDC, protected release environments, Pages deployment, or post-publication behavior, so none of those outcomes is claimed.
- The binder cannot be exercised against a real `RLS-SEH-009` until released 0.5.0 is separately authorized to prepare that record. Closed synthetic graph and external-evaluator tests cover plan/apply behavior without creating or transitioning an RLS here.

## Next accountable action

Separately authorize bounded preparation of aggregate `VREC-SEH-009` for exact candidate `b033827cc9f8357a7afb1d82f336c6fe2fc16e26`, the exact nine-work-order set, the original six verification contracts, and `VER-REB-002`. Any further push, VREC transition, RLS preparation or transition, tag, publication, deployment, maintenance mutation, credential use, external-policy change, or root-evaluator action requires separate authority.
