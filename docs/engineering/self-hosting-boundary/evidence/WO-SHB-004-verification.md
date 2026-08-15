# WO-SHB-004 implementation evidence

Date: 2026-08-15  
Lifecycle: retained implementation evidence; not a VREC, assurance decision, merge decision, or release action

## Authority and scope

The repository owner reviewed `WO-SHB-004` and explicitly stated `i approve`. This evidence covers the bounded bootstrap promotion candidate from released governor 0.2.1 to exact published governor 0.3.0, the necessary repository-specific self-hosting assertions, and local verification. It does not claim that 0.3.0 approved itself. It does not authorize a VREC transition, merge, tag, release, publication, or deployment.

The accepted `main` branch remains governed by 0.2.1 until this candidate is committed, independently reviewed, verified, and merged. The working-tree descriptor and workflow select 0.3.0 only as the proposed next governor state.

## Immutable identities

| Subject | Result |
| --- | --- |
| Prior governor | 0.2.1, `RLS-SEH-002`, candidate `94e13e31b81333e1f80f5a7dfd86ed5dbfc1e3e5` |
| Prior wheel | `se_harness-0.2.1-py3-none-any.whl`, SHA-256 `533f6f87f5a1060d5d0070702969f643525ca3b91e2ecdbbd029f1530d093454` |
| Target governor | 0.3.0, `RLS-SEH-005`, candidate `dd06660a94f06d934adb1df0352b81e709f2ffd3` |
| Target wheel | `se_harness-0.3.0-py3-none-any.whl`, SHA-256 `260e22371b05e5bb6c59143a1f0229855305a6bf7994984be50aa147a02ea516` |
| Target GitHub release | `v0.3.0`, published 2026-08-15T10:36:31Z, non-draft, non-prerelease |
| Local tag resolution | `v0.3.0^{commit}` resolves exactly to `dd06660a94f06d934adb1df0352b81e709f2ffd3` |
| Released record | `RLS-SEH-005` is `released`, version 0.3.0, commit `dd06660a94f06d934adb1df0352b81e709f2ffd3`, tag `v0.3.0` |

Both release wheels were downloaded from their GitHub releases and independently hashed. The target GitHub asset API digest and local file digest agree. The 0.3.0 wheel was inspected as a ZIP archive without importing target code. It contains protocol-1 `governor-migration.toml`, schema-2 field ownership, `engineering-harness.yml.tpl`, and `self-hosting-governor.yml` under the published self-hosting data directory.

## Bootstrap plan and transaction

The released workflow template was read from commit `dd06660a94f06d934adb1df0352b81e709f2ffd3`, rendered with the exact target descriptor, and compared byte-for-byte under LF normalization with the planned root wrapper. The referenced reusable workflow exists at `.github/workflows/self-hosting-governor.yml` in that exact commit.

| Path | Disposition | Canonical SHA-256 before | Canonical SHA-256 after |
| --- | --- | --- | --- |
| `.self-hosting/governor.toml` | update | `bd9868802b8faaf646cdcb43d19e9c8b53a287c9678ae466ba3a084e7280a06a` | `5927b8c2b6c9681f21c3bc4f44a9e39328dc84c3097fdc47b0b9437dd26d4d0b` |
| `.engineering-harness.toml` | unchanged | `5f18b041620d378fb9cd1b9d8f69eeeda6ee04ae8f0cf61e99b77bb5b5bc8804` | same |
| `.github/workflows/engineering-harness.yml` | update | `60ea04e290629b197cb3b78591df348c18980e6210551bf148221867747d8f4a` | `d63208334f4ce3e648116442bc31c238d5bc4e1f50ff2c0fb685c754e2022e59` |
| `.engineering-harness.lock` | matching integrity update | `68eb60aefea8f816a9da64a19a4934397ca4a5f897d2fff17fee5d7bec14c895` | `b170231a7685b4f31229d06d554ea66524bb69bfde3b24cd74f92914b16becf0` |

The target configuration preserves every repository identity and policy value. The root workflow now delegates to the released reusable three-plane workflow pinned to full commit `dd06660a94f06d934adb1df0352b81e709f2ffd3`, with `contents: read`, exact governor release inputs, and candidate version 0.3.0. The lock changes only the accepted workflow digest.

Before the real write, exact prior bytes were retained outside the checkout. The real write copied only the four planned paths, verified every resulting canonical hash, and would restore all four prior files on an exception. A separate disposable fault-injection fixture raised a failure after the second write and proved that all four prior files were restored byte-for-byte.

## Repository-specific test alignment

The first complete suite correctly exposed three assertions that represented the pre-promotion root state rather than stable harness behavior:

- the selected descriptor was hard-coded to 0.2.1 and `RLS-SEH-002`;
- the invalid-digest test attempted to replace only the 0.2.1 digest;
- the root workflow test required three jobs inline even though 0.3.0 deliberately moves them to an exact-commit reusable workflow.

`tests/test_self_hosting_boundary.py` now checks the exact 0.3.0 descriptor, release record, candidate commit, wrapper inputs, immutable reusable-workflow pin, and the same non-substitutable three-plane, isolation, permissions, and dependency invariants inside the released reusable workflow. No runtime implementation or consumer-template behavior changed.

## Verification results

| Check | Result |
| --- | --- |
| 0.2.1 wheel origin | isolated external installation reported version 0.2.1 and module origin outside the checkout |
| 0.2.1 semantic assessment | predictably unable to interpret post-0.2.1 distribution/schema facts; retained as the reason the documented bootstrap path is required, not presented as 0.3.0 semantic evidence |
| Formal artifact validation | PASS, 301 artifacts, 0 errors, 40 pre-existing migration/location warnings |
| Candidate-source doctor | PASS; all managed integrity checks pass; governor identity is 0.3.0 with the exact wheel digest |
| Candidate-source start preflight | PASS for `WO-SHB-004` |
| Exact published 0.3.0 doctor | PASS from an external wheel installation |
| Exact published 0.3.0 start preflight | PASS for `WO-SHB-004` from outside the checkout |
| Published runtime identity | PASS on Python 3.11.9; isolated interpreter, version 0.3.0, exact wheel digest, module/distribution/template roots outside checkout, no `PYTHONPATH` or user-site substitution |
| Focused self-hosting suite | PASS, 24 tests |
| Complete Python 3.11 suite | PASS, 160 tests, 3 skips |
| Published black-box acceptance | PASS, all 11 required scenarios |
| Deterministic repository Explorer | PASS twice, 301 artifacts, 1,111 relations, 0 errors, snapshot `2b60a99461a01579d60c4d123c9d2010dcf6a197197ad48736af9699becae9d1` |
| Acceptance contract | `se-harness-functional-acceptance-v1`, contract SHA-256 `48fc055e5123d61b6484656f9d53135188b2432f4d6976f3efef80742cee4349` |
| Acceptance manifest | raw SHA-256 `a94a79bf5b76c5ccc7a96115f9bca8741740c0e5017bda5d4e3ad8efa52aa185` |
| Rollback fault fixture | PASS; injected mid-transaction failure restored all four prior files byte-for-byte |

The 11 published acceptance scenarios were `installed-identity`, `init`, `adopt`, `doctor`, `validate`, `dashboard`, `safe-upgrade`, `customized-content-refusal`, `corrupted-integrity-refusal`, `protected-self-hosting-upgrade`, and `authority-denial`.

## Deviations and corrections

- The first published identity invocation omitted the required `--governor-wheel-sha256` argument and failed with `RID013`; the corrected command supplied the exact digest and passed. No repository file changed.
- A first acceptance run overlapped the complete source suite. The source process changed checkout cache state during the acceptance snapshot, so the runner correctly rejected checkout instability. The rerun was isolated and passed all 11 scenarios.
- The first complete suite failed only the three pre-promotion assertions described above. After their bounded repository-specific update, the focused and complete suites passed.
- A first disposable rollback-fixture command used an invalid multi-source backup copy and failed before reaching the repository. The corrected explicit-copy fixture passed. The real repository transaction had already retained independent backups and completed with all post-write hashes verified.
- Explorer attempts using the repository-default output directory could not complete because this execution session has read-only sandbox access to the repository outside the writable workspace. Those processes were stopped without modifying governed files. Two isolated runs with explicit writable external outputs each completed in 1.1 seconds and produced the same repository snapshot hash.

## Residual risks and remaining gates

- Local checks cannot substitute for hosted GitHub Actions. The pull request must run the pinned 0.3.0 reusable workflow and all governor, candidate-source, and candidate-package jobs successfully.
- Until a candidate commit exists, no commit-bound VREC can be prepared. `implemented` will record completed local work and evidence only.
- The bootstrap process is intentionally one-time. After this change is independently accepted and merged, later compatible promotions should be performed by the selected released 0.3.0 `reconcile-governor` implementation.
- No tag, release, publication, deployment, merge, or history rewrite was performed.
