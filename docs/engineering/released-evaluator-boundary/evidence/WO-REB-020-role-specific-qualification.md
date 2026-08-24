# WO-REB-020 Role-Specific Qualification Evidence

Date: 2026-08-24

Authority: non-authoritative retained implementation evidence. This file does not approve or verify the work order, authorize a candidate commit, make a release decision, publish, deploy, or upgrade the installed root evaluator.

## Authorization and candidate state

- The approved definition packet is `REQ-REB-020`, `REQ-REB-021`, `REQ-REB-022`, `SPEC-REB-010`, `ARCH-REB-009`, `ADR-REB-009`, and `VER-REB-009`.
- `WO-REB-020` is `in_progress` and requires commit-bound verification.
- The implementation base is `db704964139d6c2d88c9aabbf64848a9cf4eadc8`.
- A status-preserving amendment authorized the exact-public-0.6.0 legacy candidate-verifier bootstrap described below. It did not expand any lifecycle or external-action authority.
- A second status-preserving correction added only `tests/test_instruction_architecture.py` to the work-order execution scope so the existing managed-template contract could be updated with the reviewed assertions.
- No operational candidate commit exists for this work. Exact-commit, built-package, and hosted Windows/Linux results therefore remain pending a separately authorized candidate stage.

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

## Root/template and no-action proof

At base and after implementation:

- installed root `.github/workflows/engineering-harness.yml` Git blob: `f444ef920d397e220b7b7ea49546dda5d029ae9b`;
- installed root `.engineering-harness.lock` Git blob: `d282bde74a7728a7ac4b4a957ea9212cc80f68c0`;
- candidate template workflow base Git blob: `016e2cdf40d21c390cf6772f5e3f1527b25f46a6`;
- candidate template workflow working-tree Git blob: `7aaa6a5e63715c5903a2e53a0de3ef4f68bdaa3b`.

The root managed workflow and lock are byte-identical to `HEAD`. Template drift is the reviewed future-upgrade change, not an installed root upgrade.

No candidate commit, push, pull request, credential use, hosted dispatch, lifecycle transition beyond the already authorized packet approval/start, VREC/RLS preparation or transition, release, tag, publication, deployment, maintenance mutation, external-policy change, root-evaluator upgrade, or promotable distribution build occurred.

## Residual risks and next accountable decision

- Exact-commit qualification cannot occur before a separately authorized candidate commit exists.
- The exact candidate package and hosted Windows/Linux lanes remain pending; local mocks and workflow contract tests do not replace those results.
- The immutable public-0.6.0 bootstrap is deliberately legacy-shaped and must not survive availability of a typed released verifier.
- `predecessor-view` intentionally coordinates through the repository-owned production service while the historical evaluator executes externally; future packaging of that coordinator is a separate design decision, not a reason to duplicate view policy here.

The next accountable decision is whether to authorize an operational candidate commit for exact-commit qualification. `WO-REB-020` remains `in_progress` until that evidence is available and reviewed.
