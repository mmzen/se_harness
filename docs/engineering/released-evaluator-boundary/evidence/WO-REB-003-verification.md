# WO-REB-003 implementation evidence

## Outcome and authority boundary

`WO-REB-003` is implemented. The candidate separates evaluator identity transitions from product releases, emits deterministic non-authoritative conflict observations, and provides a maintainer runbook plus executable disposable recovery rehearsal. This evidence does not grant commit-bound verification, merge, evaluator adoption, incident action, release, publication, tag, deployment, or disposition of any artifact chain.

No operational root upgrade, product release, external publication, credential use, network mutation, tag, release, deployment, or lifecycle transition other than this work order's authorized `in_progress -> implemented` completion occurred.

## Implemented boundary

- `se_harness/upgrade_authorization.py` defines a closed `se-harness-evaluator-upgrade-v1` packet. An identity transition requires one unique `approved` or `in_progress` work order, `scope = "standard-root-only"`, the exact prior lock SHA-256, immutable-publication declaration, exact target version/payload/archive identity, and an accountable authorizer.
- `se_harness.mutation_guard` emits stable `MG007` failures before writes when the separate packet is absent, stale, malformed, ambiguous, or mismatched to the external installed evaluator.
- `apply_changes` keeps same-identity managed repair compatible. For a real identity transition it requires a new work-order-keyed JSON evidence path, rejects overwrite, rechecks target identity after authorization, writes managed changes, schema-3 lock, and canonical transaction evidence under one recoverable snapshot, and requires replay to be a no-op.
- Product release preparation remains a distinct ordinary mutation. Regression coverage proves it leaves `.engineering-harness.lock` byte-identical.
- Candidate portable inspection adds closed rules `W-REB-001` through `W-REB-003` for same-version draft/ready RLS proposals, different-commit overlapping ready VRECs, and structurally provable competing release contracts/proposals. Suggestions identify release or assurance owners and always retain `automatic = false`.
- The active installed 0.5.0 root generator and inspector remain byte-identical to schema-2 lock entries. Only candidate portable templates contain the new rules, so this work does not perform the prohibited root evaluator upgrade.
- `harnessctl rehearse-recovery` creates only a fresh directory outside the operational repository. It refuses mutable selection and recognized publication credential signals, uses a deterministic local archive and simulated publication, rejects candidate contamination and stale identity, stops synthetic competing chains without selection, injects an interrupted transaction, proves exact rollback, restores standard workflows and absence invariants, and records every external action as false.
- `docs/notes/evaluator-recovery-runbook.md` records applicability, decision rights, prerequisites, immutable selection, isolated acquisition/build, credential boundary, public-install proof, bounded root transaction, restoration, verification, rollback, evidence retention, incident follow-up, and prohibitions in the required order.
- Current operator notes use *evaluator* terminology. Historical formal artifacts and negative absence checks remain unchanged.

## Exact changed paths

Implementation and governance:

- `se_harness/upgrade_authorization.py`
- `se_harness/mutation_guard.py`
- `se_harness/installer.py`
- `se_harness/recovery_rehearsal.py`
- `se_harness/cli.py`
- `templates/repository/standard/scripts/generate_harness_dashboard.py`
- `templates/repository/standard/scripts/inspect_engineering_artifacts.py`
- `scripts/check_portable_release_surface.py`
- `docs/notes/evaluator-recovery-runbook.md`
- `docs/notes/harness-installation-and-upgrades.md`
- `docs/notes/harnessctl-reference.md`
- `docs/notes/harness-dashboard-publication.md`
- `docs/notes/developing-se-harness.md`
- `docs/notes/README.md`
- `docs/engineering/released-evaluator-boundary/work-orders/WO-REB-003.md`
- this evidence file

Verification support:

- `tests/mutation_guard_support.py`
- `tests/test_mutation_guard.py`
- `tests/test_recovery_rehearsal.py`
- `tests/test_dashboard_webui.py`
- `tests/test_inspection.py`
- `tests/test_release_orchestration.py`
- `tests/test_revision_provenance.py`

## Requirement results

| Requirement | Evidence | Result |
| --- | --- | --- |
| `REQ-REB-005` | Missing packet, missing evidence path, stale prior lock, mismatched target, evidence collision, and post-authorization identity-change cases fail without retained writes; exact packet succeeds with canonical evidence and no-op replay; release preparation retains the old lock bytes. | PASS |
| `REQ-REB-006` | Synthetic candidate snapshot produces exactly `W-REB-001`, `W-REB-002`, and `W-REB-003`; repeated results are byte-equivalent; source artifact/relations/revision inputs remain unchanged; all three inspection suggestions have `automatic = false`; an explicitly historical/superseded record remains excluded by existing lifecycle projection. | PASS |
| `REQ-REB-007` | The disposable rehearsal passes immutable selection, local build, simulated publication, external-install equivalent, injected interruption, exact rollback, bounded root conversion, normal workflow restoration, and absence invariants; negative cases reject contamination and stale identity and stop competing chains without selection. | PASS |

## Disposable rehearsal

Command:

```text
py -3.11 -m se_harness rehearse-recovery <disposable-output> --repository <operational-clone> --candidate-commit aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa --target-version 999.0.0
```

Result: PASS. The canonical report SHA-256 is `87c7550ed78ba7e0eca16cf88dea5029f5296d34e0cffa02f5b8ffb4b991c7c6`. It records `credentials = false`, `network = false`, `publication = false`, `release = false`, `tag = false`, and `deployment = false`. The operational clone was unchanged by the rehearsal.

## Automated verification

| Command or check | Result |
| --- | --- |
| `py -3.11 -m unittest discover -s tests` | PASS: 303 tests in 126.960 seconds; 4 Windows privilege/platform skips; 0 failures or errors |
| Focused authorization/rehearsal/conflict/release tests | PASS, including exact rollback, no-write snapshots, evidence collision, target-identity TOCTOU rejection, deterministic R1-R3 results, non-automatic suggestions, and product-release lock preservation |
| Candidate formal validator | PASS: 566 artifacts, 0 errors, 44 pre-existing maintenance warnings |
| `scripts/validate_release_distributions.py --root .` | PASS: 0 distribution-bearing records |
| `scripts/check_portable_release_surface.py --repository .` | PASS, including current operator terminology |
| `git diff --check` | PASS |

## Released-evaluator verification

The exact external released evaluator is SE Harness `0.5.0`, installed outside the checkout from wheel SHA-256 `974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f`.

- Isolated identity invocation passed with Python 3.14.6, exact version/root/wheel digest, resolved launcher, disabled user site, absent `PYTHONPATH`, checkout exclusion, and no diagnostics.
- `doctor` passed every required, distribution-parity, managed-integrity, owner-seed, and script check. The active root schema-2 lock remained unchanged at SHA-256 `c4c4191998cad431620324dba2ad205c190fcf2802847278cabec92e853989af`.
- Formal validation passed with 566 artifacts, 0 errors, and the same 44 pre-existing maintenance warnings.
- Review preflight for `WO-REB-003` passed with assurance classification `required`.
- Inspection produced schema `se-harness-inspection-v2`, 99 derived findings, and 3 suggestions without mutation.
- Dashboard generation passed with 566 artifacts, 2,028 relations, 0 validation errors, and 44 maintenance warnings. No generated dashboard was committed.

## Candidate package verification

The non-promotable candidate wheel was built locally with the bundled Python 3.12/setuptools environment through `pip wheel --no-deps --no-build-isolation`. The final wheel is `se_harness-0.5.0-py3-none-any.whl`, SHA-256 `5c525a36f0d02d8fa12ec5fc89e2b3dcd7dfae1a2827b0675bc036a34189ce22`.

- Wheel portable-surface scan: PASS.
- Fresh external Python 3.11 environment installation: PASS.
- Installed `harnessctl` portable CLI scan: PASS.
- Installed candidate wheel recovery rehearsal in isolated Python mode: PASS with every external action false.
- Installed `upgrade --help` exposes the bounded `--work-order` and `--evidence-output` contract.
- Installed `rehearse-recovery --help` exposes only disposable output, operational-repository observation, full synthetic commit, and synthetic version inputs.
- Candidate inspection of the operational graph returned 99 findings, no current `W-REB-*` instance, and zero `automatic = true` suggestions. Closed synthetic fixtures prove the new conflict cases without claiming that the current graph has one.

## Deviations and residual risks

- The host Python 3.11 environment lacked a usable local build backend, so the non-promotable wheel was built without network access using the already-bundled Python 3.12/setuptools runtime. The wheel then installed and passed public-surface checks in a fresh Python 3.11 environment.
- An initial direct launcher identity check correctly reported that Python isolated mode was absent. Re-running the exact released evaluator through `python -I -m se_harness identity` passed. No identity rule was weakened.
- Structural conflict rules cannot infer semantic intent beyond declared artifact fields and relations. They intentionally stop at non-authoritative observations.
- The synthetic rehearsal proves the local transaction and authority boundaries; it does not prove a future package index, hosting service, OIDC provider, protected environment, or human decision.
- Four full-suite skips require host symlink privileges or platform facilities unavailable in this Windows session; the supported non-symlink paths passed.

## Next accountable action

Retain this implementation in one clean candidate commit, then prepare a separate ready commit-bound VREC covering `WO-REB-003` only after explicit authorization. Do not perform an evaluator upgrade, release, publication, or conflict disposition as part of that action.
