# VREC-IAR-020 ready for human review

VREC-IAR-020 is ready and binds candidate `cfbaa994d7af1982bed44bc2e38c60db83602a4e` to nine implemented
work orders and VER-IAR-020, VER-IAR-021 and VER-IAR-022. Released evaluator
0.20.1 captured 56 explicit retained evidence files. Validation and the target
verified gate check pass. No human verification decision has been applied.

## Results

- Full source suite: 1,211 tests, no failures, 20 skips.
- Focused regression suite: 68 tests, no failures, 3 skips; both new regressions
  failed before the fix, with the original results retained.
- Windows and Linux: exact-wheel qualification, installed lifecycle through
  ready VREC and assurance gates, matching bound evidence bytes, migration,
  refusal, rollback and repeat no-op checks passed.
- Native Codex CLI 0.159.2 and Claude Code 2.1.273: selected entry delivery,
  manual and automatic compaction, and resume passed on the corrected wheel.
- Both host packages built; 41 adapter steps and all 20 distribution-bearing
  record checks passed. The disposable Codex profile was restored.

## Explicit limitation

**Codex Windows desktop delivery is unverified.** Native CLI/app-server checks
do not prove desktop delivery. The human previously instructed us to retain
that result as unverified and continue. This record preserves that gap and
does not waive the criterion or claim complete desktop qualification.

## Review material

- [Verification record](../../verification-records/VREC-IAR-020.md)
- [Criterion assessment](../WO-IAR-030/final-integrated-assessment.md)
- [Fresh package and native evidence](qualification.json)
- [Source regression evidence](implementation.json)
- [Capture and gate results](verification-preparation.json)

The tests used implementation commit 3f438bb894e4108fa369a9dc048d69f5e0c2e8ab.
Git comparison confirms that runtime code, templates, adapter code, tests and
build inputs are unchanged in the final candidate. Only evidence and recorded
implementation completion were added afterward. The original E012 failure and
test-driver failures remain retained beside the successful corrections.

The evaluator's next step is PROC-VREC-DECIDE / STEP-VREC-DECIDE: the accountable
human assesses whether the evidence verifies this exact candidate. Its offered
verification response is: "I verify VREC-IAR-020 as assurance owner."
Reject and supersede remain the evaluator's alternative procedures.
No push, PR, release, adoption or publication occurred.
