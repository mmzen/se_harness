# CI correction for PR 489

Prepared locally on 2026-09-27. No lifecycle transition, commit, push or PR-body
update was applied during this correction. WO-IAR-013 remains in_progress;
WO-IAR-018 remains draft. VREC-IAR-009 remains verified at its original candidate.

## Line-ending regression: corrected under WO-IAR-013

The Linux CI job failed `test_review_source_is_the_accepted_input` because the
test compared raw LF Git bytes with a hash of the reviewed CRLF input.
The content is identical after replacing only CRLF with LF.

- Historical reviewed CRLF SHA-256: `9811b1770fa81e20f19890cb45de6d991aa463cf60a4338b39251d9d4c978a28`.
- Canonical LF Git SHA-256: `4c210e7e0bb975c3b67cc673bf1986792a2ee46fc37eb5e6722769666d6ff300`.
- Code change: `tests/test_progressive_instruction_discovery.py`, one test.
- The source files, sources.json and the historical source-map digest are unchanged.
  Their old digest records the reviewed CRLF bytes; it is not relabeled as a Git hash.

The assertion now hashes bytes after CRLF-to-LF conversion only. It does not
strip whitespace, decode/rewrite Unicode, ignore content or accept any digest
computed from the current candidate as its expected value. The fixed expected
digest was checked against Git and the preserved reviewed input.

The retained probe invokes the actual test with temporary files. Before the
fix, LF failed and CRLF passed. After the fix, both pass; a changed instruction,
an added space and a bare CR are still rejected. This is a byte-representation
check on Windows, not a claimed native Linux CI rerun.

## Verification performed

- Focused content module: 9 tests passed.
- Full-scale Windows regression:

```text
Ran 1118 tests in 153.659s (175 classes, 6 workers)

OK (skipped=16)
```

- Release distribution validation: passed for 15 distribution-bearing records.
- Candidate CLI help: passed.
- Released 0.18.0 doctor and graph validation: passed.
- WO-IAR-013 review preflight and the correction's initial scope check: passed.
- Original failed probe and unsuccessful draft preflight/CLI preview attempts
  remain retained separately from successful results; no failed result is a pass.

The draft review preflight refused WO-IAR-018 because draft is not a review-stage
state (W005). The subsequent correct read-only approval preview passed. A preview
proposes approved; readback confirms that the record is still draft.

## Governance scope: prepared for review

[WO-IAR-018](../../../work-orders/WO-IAR-018.md) proposes exact coverage of the
19 governance files already present in PR #489. Its body records every path
and baseline Git-blob SHA-256. The only new writable paths are its own record
and evidence directory. It does not permit changing those preserved records.

Proposed assurance classification: `not_required`, solely for transporting
the already authorized VREC-IAR-009 decision and preserved governing package.
The line-ending test correction stays under WO-IAR-013's existing `required`
classification. Changed definitions, evidence or product behavior are excluded.
The human approval of this draft must cover both its scope and classification.

Draft SHA-256: `3348f21f62cf52abcc5f5b0b051723551d20dd265c482f56ba2484de27bc5313`.

Inspection of the complete diff plus untracked preparation files found no
uncovered paths if this proposed scope is added. That is not a passing released
check-pr result: the new work order is not yet approved. Do not add it to the
live PR declaration as though approval had occurred.

## Remaining work

Obtain the engineering owner's decision on WO-IAR-018. After approval, apply
only its supported lifecycle steps, retain transport evidence and rerun the
combined PR check. Existing WO-IAR-013–016 handoffs, native host delivery and
Linux migration qualification remain required. The change does not waive them.

After the prepared changes are committed and pushed under applicable authority,
GitHub must rerun the candidate-source and managed PR checks. The existing remote
results remain failures; a local pass is not a CI success claim.

## Observed CI failures

- [PR scope failure](https://github.com/mmzen/se_harness/actions/runs/36308812399/job/108590618006).
- [Linux source-identity failure](https://github.com/mmzen/se_harness/actions/runs/36308812406/job/108590617948).
