# WO-ECP-039 diagnosis and draft review

Current PR #487 head is 7268011f19753bf7d5a42b9bc829c3ea33f682aa. Both upgrade
rehearsals fail only after the six real handover steps meet their expected
outcomes. Both resulting locks have schema 4, evaluator/tool version 0.19.0,
and canonical SHA-256 62882e246417e780120ddf5c706e0c5a5d41d6425270707e9276cfac92f756f3.
The graph has zero errors. The predecessor assessor and ordinary CI validation
pass. The integration-package jobs are skipped because the rehearsals failed.

- [Linux failure](https://github.com/mmzen/se_harness/actions/runs/35118827011/job/104871608237)
- [Windows failure](https://github.com/mmzen/se_harness/actions/runs/35118827011/job/104871608085)
- Prior run 35101599343 at 0dadc352 has the same rehearsal failures.

Source: repository_tools/upgrade_rehearsal.py:395 requires schema == 3.
The existing test fake defaults to schema 3, and the positive test asserts 3;
there is no valid plugin-owned schema-4 success fixture. That explains why
the full local suite passed while the real CI handover exposed this assumption.
The earlier assessor diagnosis should have covered the other failed jobs.

## Review

This correction belongs to the existing real-handover contract, not the
separate assessor. The proposal changes one existing ownership assertion and
its tests; no workflow, dependency or general lock parser is needed. A bare
schema-in-(3,4) acceptance would miss unintended provider changes, so the
specification also checks preservation. Full integrity remains with the real
evaluators. No architecture addresses REQ-ECP-012, matching original WO-ECP-010.

The proposed aggregate verification explicitly resolves earlier record-location
constraints without rewriting historical records. All three new artifacts
remain drafts. No implementation, lifecycle approval, commit or push is claimed.
Raw current and prior failure logs and both platform result JSON files are
retained beside this note. The Git-ref scan before allocation covered 63 refs.
