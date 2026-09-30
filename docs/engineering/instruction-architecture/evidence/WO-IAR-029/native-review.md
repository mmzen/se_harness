# Native test review — WO-IAR-029

Native CLI checks passed after correcting one delivery defect. WO-IAR-029
remains `in_progress`. Desktop delivery is unverified. The later
[CLI workflow review](cli-workflow-review.md) completes the new/resumed-work
walkthrough through Codex CLI. No verification record was prepared.

Candidate: `e79368c677541d7092129a853e8b39157865ace9`.
The governing evaluator remains released 0.20.0. The tested 0.21.0 wheel is a
development candidate, not a repository adoption or a published release.

## Defect found and corrected

The native Codex activation returned a delivery gap because its complete entry
and actual paths needed **10,002 UTF-16 units**. The adapter applied Claude's
10,000-unit bound to both hosts. It correctly refused to truncate the policy,
but incorrectly rejected an entry that Codex could deliver.

The adapter now applies a bound for each host: 10,000 units for Claude and
20,000 for Codex. Codex retains its existing 5,000 approximate-token hook setting.
An oversized entry reports its measured size. The instructions themselves are
unchanged. A regression test covers an entry accepted by Codex and refused by
Claude, plus complete-envelope and Unicode boundaries.

The native rerun received the full 10,002-unit Codex context after activation,
manual compaction, automatic compaction and resume. Its entry matches the
independently rendered wheel template, including the final section.

## Results

| Check | Observed result |
| --- | --- |
| Full suite | 1,185 tests; 18 skipped; no failures. |
| Final focused and assembly checks | 45 tests; 2 skipped; no failures. |
| Linux delivery boundaries | 17 tests passed. |
| Installed-wheel walkthrough | All 39 steps passed on Windows and on Linux. |
| Native Claude Code 2.1.273 | Bootstrap, agent-driven clone and activation, manual/automatic compaction, same-session resume, compatible plugin update, two release selections, switching and clearing passed. |
| Native Codex 0.158.0-alpha.2.1 | Bootstrap, agent-driven activation, manual/automatic compaction, resume, switching, clearing and corrupt-record refusal passed. |
| Concurrent Codex sessions | Two sessions from one parent retained distinct 0.20.0 and 0.21.0 selections during simultaneous turns and compactions. |
| Session isolation | Clearing one session preserved the other selection on both hosts. |
| Repository validation | Zero errors; 54 existing warnings. |

These are native CLI/app-server observations. They are not desktop observations.
Automatic compaction used documented temporary thresholds; no manual compact
command was used for those cases. Claude emitted `trigger: auto`. Codex emitted
`contextCompaction` during an ordinary turn with no compact RPC.

The final suite ran after the runtime fix. The only later source changes were
the two README explanations of the host bounds; the final focused/assembly
checks include those edits. All runtime, skill, asset and hook files used in the
native reruns match the candidate. The wheel and entry bytes did not change.

## Remaining qualification

- **Codex Windows desktop:** **unverified**, as requested by human mmzen on 2026-09-30. Continue CLI qualification; this is not a desktop pass. Computer Use identified the installed
  app as ChatGPT. Its [skill](C:/Users/mathi/.codex/plugins/cache/openai-bundled/computer-use/26.924.22138/skills/computer-use/SKILL.md)
  references [guidance](C:/Users/mathi/.codex/plugins/cache/openai-bundled/computer-use/26.924.22138/docs/guidance.md)
  that states: “Do not automate the ChatGPT desktop app UI or Codex CLI or Codex
  extensions within Windows apps.” Shell-based native test drivers do not
  establish desktop delivery.
- **Complete work-to-delivery walkthrough:** passed through Codex CLI on the
  successor and legacy fixtures; see [the retained review](cli-workflow-review.md).
  These results identify exact candidates and delivery authority without publication.

The released evaluator still selects `PROC-WO-IMPLEMENT` /
`STEP-WO-IMPLEMENT-CHECK`, with the bound handoff check for WO-IAR-029. Desktop delivery remains unverified under the user's instruction; no completion is inferred from CLI evidence alone.

## Evidence and limits

[native-tests.json](native-tests.json) contains the assessed matrix, independent
entry identities, actual runtime-file hashes and evaluator result.
[native-traces.json](native-traces.json) retains commands, native events, outputs
and test reports; long text is stored once by its exact SHA-256.

Earlier failures remain recorded: the test-launcher argument separator, Git
fixture ownership, Codex sandbox process launch, the incorrect shared delivery
bound, and the temporary marketplace-source conflict. Exact native command
approvals recovered the Codex process-launch failure without a persistent
permission rule. No hook-trust bypass was used.

Existing authenticated disposable profiles were reused without copying
credentials. The original plugin package was restored in the disposable Codex
profile after testing. Real user settings, production installations and
credentials were not changed. No push, PR, release, adoption or lifecycle
completion was performed.
