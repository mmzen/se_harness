# Claude recovery qualification: continued observation

The previously authorized native test continued in the retained disposable
session using the same exact candidate wheel, model alias opus and safeguards.
No product implementation or accepted definition changed.

## Results

| Case | Observed result |
| --- | --- |
| Manual compaction | Passed. Claude emitted compact_boundary with trigger manual and delivered the complete expected entry. |
| Ordinary resume after manual compaction | Passed. The acknowledgement returned successfully and the expected entry was complete. |
| First automatic-compaction attempt | The ordinary resumed turn passed, but no automatic compact boundary occurred. This does not pass the automatic criterion. |
| Context-size fixture | Windows first refused the oversized command line before starting Claude. Passing the same synthetic shape rows through stdin reached Claude, which returned reasoning_extraction. |
| Final automatic-compaction attempt | The entry was delivered, but the provider again returned reasoning_extraction. No automatic compact boundary was observed. |

All observed fixture file digests remain unchanged. Exact arguments, temporary
compaction thresholds, hook events, replies and provider errors are retained in
claude-continuation.json. The context-size rows are inert generated data; the
test asked for no tool use or instruction disclosure.

## Current readiness

WO-IAR-030 remains in_progress. The complete candidate assessment and
VREC-IAR-020 remain pending. Native automatic compaction is an explicit criterion
in VER-IAR-021, which VER-IAR-022 requires for the integrated candidate. Earlier
historical passes and successful manual compaction do not turn this run into an
automatic-compaction pass. Codex Windows desktop remains explicitly unverified
under the earlier human instruction.

## Available planning choices

1. Keep the current criterion and candidate pending. Complete the automatic
   compaction observation when the provider session can perform it. No
   requirement change is needed.
2. Prepare a bounded formal deferral proposal for human review. It would name
   the missing automatic-compaction evidence, preserve the unverified label,
   define the effect on support/release claims, and set the follow-up condition.
   A proposal alone changes no requirement or gate and does not authorize
   implementation completion or verification. The applicable formal decision
   and supported lifecycle procedure must be reviewed before applying it.

No deferral, waiver, acceptance, release, push or PR is applied by this report.
