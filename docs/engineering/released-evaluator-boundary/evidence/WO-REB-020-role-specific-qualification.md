# WO-REB-020 Role-Specific Qualification Evidence

Date: 2026-08-24

Authority: non-authoritative retained implementation evidence. This file does not approve or verify the work order, authorize a candidate commit, make a release decision, publish, deploy, or upgrade the installed root evaluator.

## Authorization and candidate state

- The approved definition packet is `REQ-REB-020`, `REQ-REB-021`, `REQ-REB-022`, `SPEC-REB-010`, `ARCH-REB-009`, `ADR-REB-009`, and `VER-REB-009`.
- `WO-REB-020` is `in_progress` and requires commit-bound verification.
- The implementation base is `db704964139d6c2d88c9aabbf64848a9cf4eadc8`.
- A status-preserving amendment authorized the exact-public-0.6.0 legacy candidate-verifier bootstrap described below. It did not expand any lifecycle or external-action authority.
- A second status-preserving correction added only `tests/test_instruction_architecture.py` to the work-order execution scope so the existing managed-template contract could be updated with the reviewed assertions.
- Operational candidate commit: `73651505e0850e5c9348bbcf67708765ae61b755` (`Implement role-specific release qualification`).
- The commit contains exactly the reviewed 32-path implementation. This post-candidate evidence update is intentionally uncommitted.
- Exact local source/package qualification and hosted Linux/Windows agreement are recorded below.
- Existing branch `proposal/rca-060-09-role-commands-01a02460` was pushed to origin at the exact candidate commit solely to run hosted qualification.

## Implemented command contracts

| Operation | Fixed evaluator | Fixed target | Independence recorded in canonical output |
| --- | --- | --- | --- |
| `released-root` | released evaluator named by the root lock | installed repository root | `released-evaluator` |
| `predecessor-view` | exact external predecessor selected by the governed release contract | deterministic predecessor-compatible view | `external-predecessor` |
| `complete-candidate` | candidate source at the asserted commit | complete candidate graph | `candidate-controlled` |
| `candidate-package` | exact isolated released verifier | candidate wheel bound to its digest and commit | `released-verifier` |
| `public-install` | exact environment installed from acquired public bytes | released record, wheel, installed payload, resources, and CLI | `public-install-observation` |

The parser exposes exactly these five operations. It has no free-form role, script, validator, or evaluator-wheel selector. Each handler fixes its checks and emits `se-harness-release-qualification-v1`, including evaluator and target identities, ordered check results, the independence class, and the statement `evidence-only; no lifecycle or external action authorized`.

Canonical output is UTF-8 JSON with stable key ordering and LF termination. `--output` accepts only a new path outside the inspected repository and publishes complete bytes without overwriting an existing result. Human output is derived from the same result object. Failure diagnostics are first-line, length-bounded, and scrubbed of workstation, evaluator, and temporary paths.

## Workflow change map

| Workflow surface | Previous release-qualification mechanism | Implemented mechanism |
| --- | --- | --- |
| candidate source | separate source identity plus raw candidate validation/regression | `qualify complete-candidate`, retained as explicitly candidate-controlled evidence, plus regression tests |
| candidate package | package diagnostics without the new typed released-verifier result | exact-public-0.6.0 bootstrap described below; future typed handler is `qualify candidate-package` |
| predecessor assessment after transition | transition assessment only | target evaluator also runs `qualify released-root` when transition is required |
| PyPI preparation and Pages publication | repository script selected the predecessor publication validator and executable inputs | `qualify predecessor-view` delegates to the fixed production service and derives predecessor entry point/wheel provenance itself |
| release candidate checkout | raw `validate` followed by the complete suite | `qualify complete-candidate` followed by the complete suite; the result is retained separately from inert release bytes |
| public package observation | install by version and basic CLI/version smoke | acquire and digest-bind the exact wheel, install those local bytes, and run `qualify public-install` against the released record |
| future managed root health | raw identity, doctor, and validate commands in the candidate template | `qualify released-root` in the candidate template, with the canonical role result retained |

Low-level `doctor`, `validate`, and `identity` remain diagnostic commands. Workflow steps do not treat their standalone output as a role-bound release qualification result.

## Exact-public-0.6.0 bootstrap amendment

Exact public 0.6.0 predates the `qualify` namespace. Direct observation of that immutable package returned exit code 2 with `harnessctl: error: argument command: invalid choice: 'qualify'`. Its existing hardened `accept-candidate` command is therefore retained for the first candidate-package deployment only.

The candidate workflow fixes and verifies all of these values before invoking it:

- version: `0.6.0`;
- wheel: `se_harness-0.6.0-py3-none-any.whl`;
- wheel SHA-256: `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`;
- installed-payload SHA-256: `c233678548fe742b7a7a5a8bd65de10156ff233edc65b68e2ed0333fbe4dea42`;
- acceptance-contract SHA-256: `a443e93d6da7d0538bdf790a16f4dea49ac7a6ede384c65e40362627d7a84b75`;
- command: isolated exact-public-0.6.0 `python -I -m se_harness accept-candidate`;
- result schema: `se-harness-functional-acceptance-v1`; and
- retained artifact label: `candidate-package-legacy-bootstrap-0.6.0`.

The workflow independently checks the candidate commit, candidate-wheel digest, verifier identity, and contract digest. It also asserts that the legacy result has no `independence` claim. The result is not renamed or converted to `se-harness-release-qualification-v1`.

This bootstrap must be removed as soon as the selected released verifier exposes `qualify candidate-package`. Newly built code keeps `accept-candidate` only as a one-cycle parser alias to the typed handler; that alias is not the immutable 0.6.0 implementation.

## Actual changed-path subset

The implementation changes 32 paths, all present in the maximum execution allowlist:

- four repository-owned workflows: candidate evidence, predecessor assessment, PyPI publication, and dashboard/Pages publication;
- the released-evaluator-boundary README, eight approved packet artifacts, and this keyed evidence file;
- six developer/operator notes, including the new role guide;
- `scripts/check_portable_release_surface.py`;
- `se_harness/cli.py`, `se_harness/evaluator_identity.py`, and new `se_harness/release_qualification.py`;
- the candidate standard managed-workflow template; and
- six adjacent test modules plus new `tests/test_release_qualification.py`.

No other allowlisted production helper required modification. In particular, the existing predecessor production service remains the single implementation of predecessor-view policy, and `candidate_acceptance.py` remains the single hardened candidate-wheel contract implementation.

## Local verification

The following results were obtained from the reviewed working tree:

- focused qualification, identity, workflow, release, package, dashboard, and managed-template tests: PASS, 104 tests;
- complete supported suite: PASS, 500 tests with 9 expected skips;
- scale observations: PASS at 100, 500, and 1000 artifacts;
- engineering graph JSON validation: PASS, 717 artifacts, 0 errors, 50 pre-existing maintenance warnings;
- all five repository workflow YAML files parsed with PyYAML 6.0.3;
- Python compilation of the changed package, script, and tests: PASS;
- portable release-surface check, including installed help for all five operations: PASS;
- `git diff --check`: PASS.

Focused tests cover the closed parser, deterministic/non-authoritative schema, exclusive output, bounded path/privacy failures, evaluator-identity stop gates, fixed predecessor delegation, candidate-controlled labeling, exact candidate-wheel verifier ownership, public wheel/payload/release binding, compatibility-alias parity, exact-public-0.6.0 bootstrap constants/schema/label, workflow role selection, and managed root/template separation.

The complete suite was replayed after the evidence and authorized managed-template assertion correction were present. The changed-path audit reported 32 changed paths and zero paths outside `WO-REB-020.execution_scope`.

## Exact-candidate replay

### Complete candidate

`qualify complete-candidate` passed from a fresh external Python environment against commit `73651505e0850e5c9348bbcf67708765ae61b755` and tree `2de29cfe9e7951d68c7e7799afb257c3c6cef6ae`:

- candidate runtime bound to checkout: PASS;
- clean `HEAD` and tracked tree bound to the candidate commit: PASS;
- complete engineering graph: PASS, 717 artifacts, 0 errors, 50 existing maintenance warnings; and
- repository no-change snapshot: PASS.

The canonical result is `se-harness-release-qualification-v1`, operation `complete-candidate`, independence `candidate-controlled`, evaluator identity SHA-256 `a99dc63609145fe0de4df801e91b67643a08938f07ef32357a1024df4adbf005`, and target identity SHA-256 `0cef2cbc281a57154c5939031998aa9d4730838a381fb3f27eb1c3c5faee903c`.

Retained clean-runtime result SHA-256: `8ab99f67050cb3d435885dd8c238a4bbff495dfe6036b5f17caded1466dba291`.

An initial invocation from the workstation's ordinary Python failed closed with `RID009` and `RID018` because that runtime enabled user site-packages and exposed unrelated installed distribution metadata outside the checkout. The same exact candidate passed from the workflow-equivalent clean external environment. Both results are retained externally; the refusal result SHA-256 is `a59b22f33b9492878600f38cb496b969678bad3cfaf882d6408c6e7ffe6ff7aa`. The refusal demonstrates the intended runtime-contamination gate and was not bypassed or converted into a pass.

### Reproducible candidate distributions

Two fresh extractions of `git archive 73651505e0850e5c9348bbcf67708765ae61b755` were built with the workflow-pinned disposable toolchain (`build==1.3.0`, `setuptools==84.0.0`, `wheel==0.48.0`) and `SOURCE_DATE_EPOCH=1787564659`. The repository sdist normalizer used the same epoch. Both output sets were byte-identical:

- `se_harness-0.6.0-py3-none-any.whl`: `70eb7b89b23bdda227273668f18e9837ea04846e4a4c799f4e646eef4a751f09`;
- `se_harness-0.6.0.tar.gz`: `a901f36a4bf041b8c201fb9bc5abf984ed3db45e14adfc9e0f7c6850bdedcccb`.

These are non-promotable local candidate distributions retained outside the checkout. Their hashes do not amend the released 0.6.0 record or public distribution bytes.

### Independent exact-public-0.6.0 candidate-package bootstrap

The immutable public-0.6.0 verifier accepted the exact candidate wheel using its historical command and retained `se-harness-functional-acceptance-v1` without a typed-independence field:

- verifier wheel SHA-256: `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`;
- verifier acceptance-contract SHA-256: `a443e93d6da7d0538bdf790a16f4dea49ac7a6ede384c65e40362627d7a84b75`;
- candidate commit: `73651505e0850e5c9348bbcf67708765ae61b755`;
- candidate wheel SHA-256: `70eb7b89b23bdda227273668f18e9837ea04846e4a4c799f4e646eef4a751f09`; and
- result: PASS, all 10 fixed scenarios.

Retained legacy-bootstrap result SHA-256: `9f9a8849bc6969fd5762306972969f4f33a722ae93b91ccd1f43ae887e640829`.

The separately installed candidate wheel then passed isolated `candidate-package` runtime identity with no diagnostics, the packaged portable-release surface, and a disposable repository `init`, `doctor`, `validate`, `dashboard`, and no-op `upgrade --apply` lifecycle. The disposable root reported 36 managed files unchanged after upgrade. Final candidate-checkout status and diff checks remained clean before this evidence update.

### Hosted exact-candidate qualification

All hosted workflows selected exact commit `73651505e0850e5c9348bbcf67708765ae61b755` on branch `proposal/rca-060-09-role-commands-01a02460`:

- Engineering Harness run `32714254411`: PASS;
- SE Harness Candidate Evidence run `32714254421`: PASS;
- candidate source job `97392038359`: PASS, including typed complete-candidate qualification, portable surface, full regression, retained result, and checkout no-change;
- candidate package job `97392233234`: PASS, including the exact-public-0.6.0 bootstrap verifier, installed identity/surface, disposable repository, retained legacy result, and checkout no-change;
- Linux governance-migration job `97392364977`: PASS;
- Windows governance-migration job `97392365039`: PASS; and
- cross-platform reconciliation job `97392634696`: PASS with one semantic result.

Governor Transition Assessment run `32714254403` also passed at the same commit. The only hosted annotations were informational Node.js-20 deprecation notices emitted by GitHub Actions; no qualification job reported a warning or failure.

## Root/template and no-action proof

At base and after implementation:

- installed root `.github/workflows/engineering-harness.yml` Git blob: `f444ef920d397e220b7b7ea49546dda5d029ae9b`;
- installed root `.engineering-harness.lock` Git blob: `d282bde74a7728a7ac4b4a957ea9212cc80f68c0`;
- candidate template workflow base Git blob: `016e2cdf40d21c390cf6772f5e3f1527b25f46a6`;
- candidate template workflow working-tree Git blob: `7aaa6a5e63715c5903a2e53a0de3ef4f68bdaa3b`.

The root managed workflow and lock are byte-identical to `HEAD`. Template drift is the reviewed future-upgrade change, not an installed root upgrade.

No pull request, lifecycle transition beyond the already authorized packet approval/start, VREC/RLS preparation or transition, release, tag, publication, deployment, maintenance mutation, persistent external-policy change, root-evaluator upgrade, or promotable distribution build occurred. The configured Git credential was used only to push the existing branch at the exact candidate commit and read the resulting run status. Public network access was otherwise used only to install workflow-pinned build dependencies into a disposable external environment.

## Residual risks and next accountable decision

- The immutable public-0.6.0 bootstrap is deliberately legacy-shaped and must not survive availability of a typed released verifier.
- `predecessor-view` intentionally coordinates through the repository-owned production service while the historical evaluator executes externally; future packaging of that coordinator is a separate design decision, not a reason to duplicate view policy here.

Local and hosted qualification now pass. The next accountable decision is whether to transition `WO-REB-020` from `in_progress` to `implemented`, followed by a governance commit, exact replay at that clean governance commit, and ready preparation of `VREC-REB-016` conforming to `VER-REB-009` with this keyed evidence path. `WO-REB-020` remains `in_progress` until that transition is explicitly authorized.
