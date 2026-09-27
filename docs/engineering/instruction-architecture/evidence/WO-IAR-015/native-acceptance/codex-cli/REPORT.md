# Codex instruction demonstration — 2026-09-27

Session: `01a0e37f-a778-7b71-a39b-93a898d33f6f`  
Host: Codex CLI `0.155.0-alpha.16.4`, Windows.

| Observation | Native transcript evidence |
| --- | --- |
| Startup delivery | Line 9: complete root in a developer message before the first probe. |
| Progressive reading | Lines 34–35: successful commands reading COMMUNICATION.md and DEFINE_CHANGE.md. |
| Compaction completed | Line 48: ContextCompaction completion. |
| Context after compaction | Line 58: complete root in a new developer message before the next probe. |
| Root identity | Both delivered roots match SHA-256 `b55a88ab900a7466b372ec32a4bc80ca47fa26a79ec0f8bc703aba58174bfaab`. |

The visible demonstration is supported by native context records, not only
by the agent's JSON replies. The source transcript records the full root
again after compaction.

The inspected logs do not separately record the `SessionStart:compact`
callback. Its fresh execution and disk revalidation are not independently
proven by these observations. Desktop delivery, Claude post-compaction,
missing/stale roots and repository switching are not assessed here.

This is transient observation material outside the repository. It changes no
formal artifact or lifecycle state.

See [structured observations](observation.json) and
[retained native messages](native-context-extract.jsonl).

## Follow-up native callback capture

A later ephemeral replay captured the explicit native `hook/started` and
`hook/completed` events after compaction, with the complete matching context.
See the [follow-up capture](../codex-callback/REPORT.md).
The original CLI transcript and its earlier observations remain unchanged.
