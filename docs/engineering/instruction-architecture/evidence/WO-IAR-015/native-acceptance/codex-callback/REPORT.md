# Codex compaction callback capture — 2026-09-27

The native event stream confirms execution of the installed Verity Plane
`sessionStart` hook following compaction. The hook completes successfully and
returns the complete matching instruction file before the next probe reply.

Host: `codex-cli 0.155.0-alpha.16.4`, Windows.  
Surface: native app-server over stdio, using the existing isolated demo profile.  
Replay: `01a0e394-d4c0-7852-9618-0e70c05a894d` (ephemeral).  
Source CLI session: `01a0e37f-a778-7b71-a39b-93a898d33f6f`.

| Sequence | Native event | Evidence line |
| --- | --- | --- |
| 1 | `item/completed`, `contextCompaction` | 10 |
| 2 | `hook/started`, `eventName: sessionStart`, source: plugin | 14 |
| 3 | Matching `hook/completed`, status: completed | 15 |
| 4 | Correct post-compaction probe reply | 16 |

The completed hook returns 8,925 context characters. Its instruction-file
SHA-256 is `b55a88ab900a7466b372ec32a4bc80ca47fa26a79ec0f8bc703aba58174bfaab`.
The returned text contains the entire file, not a summary or truncated preview.
The installed hook definition and Python helper match the assembled candidate.
The original CLI rollout and the fixture's root, configuration and lock are unchanged.

The API names the event `sessionStart`; its notification does not include the
input's `source` string. The compact trigger is established by the explicit
compaction request and completion followed by the callback in the same replay,
with no intervening resume or session restart. This follows the documented
[post-compaction SessionStart behavior](https://learn.chatgpt.com/docs/hooks).
The [native event protocol](https://learn.chatgpt.com/docs/app-server) exposes
synchronous hook start and completion notifications.

This is a follow-up native app-server observation. It does not invent a callback
record for the earlier CLI rollout, and it does not establish desktop delivery,
automatic compaction, repository switching or missing/stale-file behavior.
No formal verification acceptance or lifecycle transition was applied.

Evidence:

- [Native event stream](native-events.jsonl)
- [Verified observations and identities](observation.json)
- [Earlier CLI demonstration](../codex-cli/REPORT.md)
