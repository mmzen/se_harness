# Native lifecycle qualification: trials 361

Both agents completed the synthetic hosted lifecycle. Independent released-evaluator
replay passed for every accepted operation and export. **Qualification remains
incomplete** because each host has a reporting or instruction-use failure.

Implementation candidate: `ee86a842550c19fb6a56913841757b42df9ecaec`.
Review head during both runs: `dfeb5adf1f640dea48a53b7a446e49e93c31004a`.
Client 0.22.2; candidate plugin 0.2.7; released governor 0.22.1.
No candidate package changed between these trials and the preceding diagnostic.

| Observation | Claude 361 | Codex 361 |
| --- | --- | --- |
| Native wall time | 21m 59s | 22m 30s |
| Calls | 188; complete capture | 237 observed tool items; complete count unavailable |
| Reported peak input context | 626,116 | Unavailable |
| Accepted lifecycle operations independently replayed | 12, pass | 12, pass |
| Native exports independently replayed | 2, pass | 4, pass |
| Native MCP comparisons | 8 calls covering all 7 tools, exact | 9 calls covering all 7 tools, exact |
| Refused scope and stale-draft requests | Correct refusal, no receipt/effect | Correct refusal, no receipt/effect |
| Lost reply, lookup, identical retry, changed-key refusal | Pass | Pass |
| Original imported records, staged inputs, monitored repository/settings | Unchanged | Unchanged |
| Remaining qualification failure | Calls supplied implementation candidate C unknown | Direct shell reads of task.md at startup and after compaction |

Claude used Opus 5.5 with pinned CLI 2.1.280. Codex's exact invocation and observed
host identity are retained in its archive. The runs overlapped each other and the
focused clarification cases. Their durations are observations, not an isolated
model comparison. Neither run received a workflow hint or operator mutation.

## Findings and corrections

- **F40-C1:** Claude's original report names C as unknown, although the selected
  inputs contain `qualification_candidate`. Its synthetic candidate P binding is
  correct. Expose the same input through the existing identity command and point
  the evidence guide to that field. Do not repair the agent's original report.
- **F40-X1:** Codex used `Get-Content` outside the task's helper-only shell route.
  The initial pointer did not provide the helper prefix until after task.md was
  read. Expose the bounded reader in the startup pointer and clarify recovery.
  Normal host filesystem protections remained active; no broader write or
  settings change was observed. Codex disclosed its recovery deviation.
- **Observer correction:** Claude did read both host-persisted instruction
  responses completely. The first trace collector missed host-managed paths.
  Native Read calls at events 51 and 188, and their successful returns at 52 and
  189, prove full recovery. The supplemental comparison retains exact saved
  bytes. The preliminary interpretation was corrected; this is not a native
  instruction-reading failure.

Failed commands and recoveries remain in the visible transcripts. Successful
completion does not erase them. The stale selected-draft test here is separate
from the isolated preview-digest guard demonstrated by the earlier 351 trial.

## Evidence

- [Claude visible transcript](claude-361-visible.md), [bounded evidence](claude-361-evidence.zip), [inventory](claude-361-inventory.json).
- [Codex visible transcript](codex-361-visible.md), [bounded evidence](codex-361-evidence.zip), [inventory](codex-361-inventory.json).
- [Setup, package reuse, live comparisons and observer commands](provenance.zip), [inventory](provenance-inventory.json).

Each host archive contains its independent assessment, original report, selected
inputs, exact requests/results, read trace, boundary comparison and replay results.
The Claude archive adds the persisted-instruction recovery supplement. The Codex
archive retains the reader-boundary finding. Private reasoning, credentials and
raw host/system events are excluded; original event digests remain recorded.
Completed test containers are stopped; their private volumes remain available.

WO-HAG-009/010/011 remain in progress. No real verification, release, deployment,
merge or Git-authority change occurred. PR #543 remains an unfinished-work draft.
The next action is the affected unassisted native rerun after the bounded correction.
