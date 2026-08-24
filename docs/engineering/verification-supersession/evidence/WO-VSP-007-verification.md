# WO-VSP-007 verification evidence

artifact: WO-VSP-007
checkpoint: handoff
formal_snapshot_sha256: 5b629005ccf508b8d668c8cefb5626fb3efebd91aed11dca4ce55e62c8cfc6d9

Date: 2026-08-24

## Scope and authority

This pre-candidate evidence covers the approved issue #123 implementation under `WO-VSP-007`: align current prepared verification-record supersession with lifecycle validation while preserving immutable legacy history. Qualification was performed on the reviewed working tree based on `2b78f4257a55ebcb8777144b7dcca623e5b2b05c`; the operational candidate identity is established only by the later authorized commit containing these exact bytes. The implementation changes no concrete repository VREC, lifecycle edge, decision right, root managed file, package version, release record, credential, or external system.

The existing `se_harness/workflow.py` transition mutator was reviewed and left unchanged. Its target-specific write set was already conformant; the defect was confined to the packaged candidate validator rule.

## Reproduction and root cause

The focused end-to-end command test initially failed while applying a supported `ready -> superseded` transition to a current VREC containing `prepared_at` and `prepared_by`:

```text
python -m unittest tests.test_workflow_execution.WorkflowExecutionTests.test_ready_prepared_vrec_can_be_superseded_without_verification_decision_fields -v

WEX201: proposed final graph is invalid [E002]: field 'verified_at' must be a non-empty string
Ran 1 test in 1.179s
FAILED (failures=1)
```

The transition plan itself did not add verification fields. The candidate validator grouped `superseded` with `verified` and `released`, so it demanded a verification decision after the mutually exclusive supersession decision.

## Corrected invariant

- Current-format records are identified by the presence of either preparation field and must contain valid `prepared_at` and `prepared_by` together.
- Current `verified` and `released` VRECs require `verified_at` and `verified_by`.
- Current prepared VRECs superseded directly from `ready` preserve their preparation facts, require the existing supersession fields and successor relation, and must omit `verified_at` and `verified_by`.
- Legacy superseded VRECs without preparation fields retain their historical required `verified_at` capture timestamp and remain valid without a fabricated `verified_by` or migration.
- Rejection, successor eligibility, coverage, cycle, active-release reference, event consistency, and atomicity rules are unchanged.

Candidate source hashes at this checkpoint are:

| File | SHA-256 |
| --- | --- |
| `templates/repository/standard/scripts/validate_engineering_artifacts.py` | `275071efee52aefeb9c3af9bf68b240920a78448efcb666de154726f7669f9c6` |
| `templates/repository/standard/docs/engineering/templates/VERIFICATION_RECORD.template.md` | `e6ed155673cf86189609c15cf3c1e9c8b6135c9027db9d40666f14d967d7f0e8` |

## Focused and compatibility verification

- The corrected command test, prepared-record validator matrix, legacy supersession projection, and ready-field rejection test passed: 4 tests in 1.380 seconds.
- The complete workflow-execution and revision-provenance modules passed: 74 tests in 79.440 seconds, with 2 conditional skips.
- Revision-provenance full-discovery replay passed after binding the new test explicitly to the packaged candidate validator: 37 tests in 35.694 seconds, with 1 conditional skip.
- The end-to-end fixture proves retained `prepared_at` and `prepared_by`, absence of both verification fields, exact supersession metadata/relation/event, successful final-graph validation, and no write on failed planning through the existing rollback coverage.
- Existing legacy fixtures continue to require and retain historical `verified_at` while omitting current preparation metadata.

## Complete suite and checkout portability

The first full Windows-worktree run executed 570 tests and exposed two findings. The new test's import-order dependency was corrected and its full-discovery replay passed. The remaining finding was the pre-existing LF-only assertion for `se_harness/hash_bound_classes.json`: Git reported `i/lf w/crlf` on this worktree even though the implementation does not touch that path.

To separate product behavior from checkout conversion, all six tracked implementation diffs were applied to a disposable local clone created with `core.autocrlf=false`. Git reported `i/lf w/lf` for the declaration, and the complete suite passed:

```text
Ran 570 tests in 308.989s
OK (skipped=10)
```

The original worktree also passed the other 569 tests when exactly the unrelated declaration byte-shape assertion was excluded: 569 tests in 303.065 seconds, with 10 conditional skips. No file outside the work-order scope was altered to obtain either result.

## Isolated installed-wheel verification

An offline, non-promotable wheel was built from the uncommitted candidate with bundled `setuptools 84.0.0` and `wheel 0.48.0`, then installed without dependencies or index access into a fresh Python 3.12.13 environment. Its SHA-256 was `5c3f2dcca6976a11987d13637fa05f01b38252d0182945017fca83153667ae87`.

The installed wheel initialized a fresh repository, transitioned `VREC-002` from `ready` to `verified`, then transitioned prepared `VREC-001` from `ready` to `superseded` by that coverage-preserving successor. The installed transition reported exactly these source fields:

```text
lifecycle_events
relations.superseded_by
status
superseded_at
supersession_authorized_by
updated
```

The resulting source retained `prepared_at` and `prepared_by`, contained no `verified_at` or `verified_by`, left all active/assurance/decision queues, and passed installed validation with 12 artifacts and zero errors. The two fixture-only maintenance warnings were unchanged legacy architecture warnings. The temporary wheel is evidence only: it is not a candidate identity, retained distribution, publication artifact, or release authorization.

## Repository-level qualification

- Candidate-template direct validation: PASS, 735 artifacts, 0 errors, 50 pre-existing maintenance warnings.
- Released-root formal validation: PASS, 735 artifacts, 0 errors, the same 50 warnings.
- Exact external public 0.6.0 `doctor`: PASS; all released root managed files remain unchanged.
- Exact external public 0.6.0 JSON validation: `valid = true`, 735 artifacts, 0 errors, 50 warnings.
- Release-distribution validation: PASS for 1 distribution-bearing record.
- CLI help: PASS and exposes the governed command surface.
- Inspection: `WO-VSP-007` is the only active work item; unrelated draft `WO-HBI-002` remains untouched; no assurance or decision queue was changed.
- `git diff --check`: PASS.

Candidate-source `doctor` continues to report root/template drift because candidate templates intentionally lead the separately locked released root copy. Exact released-root `doctor` passes, and this work does not authorize or perform a root upgrade.

## Changed-path and authority boundary

The implementation uses thirteen of the fourteen authorized paths: six definition/work-order records, the VSP index, command reference, candidate VREC template, candidate validator, two test modules, and this evidence file. Authorized `se_harness/workflow.py` is unchanged because its existing behavior passed the exact installed transition write-set test.

After the handoff gate passed, the engineering owner explicitly directed `WO-VSP-007` to become `implemented`; the transition changed only status, update date, and lifecycle event. At the time this pre-candidate evidence was sealed, no candidate commit, VREC preparation or decision, push, pull request, release, tag, publication, deployment, maintenance mutation, credential use, external-policy change, or root-evaluator upgrade had occurred.

## Residual risk

The historical/current discriminator is field presence because old records have no explicit schema-generation marker. The compatibility matrix prevents that discriminator from weakening current prepared records. Exact commit-bound replay remains required after the separately authorized candidate commit; hosted qualification remains a later external action.
