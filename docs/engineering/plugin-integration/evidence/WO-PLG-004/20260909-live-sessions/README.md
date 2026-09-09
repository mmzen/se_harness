# Authenticated session observations

Claude Code **2.1.266**, Windows, existing isolated login profile. No credential
contents or account details were captured. These commands used no tools and
retained ordinary permission mode. The observer restored the existing prepared
evaluator; this preparation is not C07 setup evidence.

| Case | Observed result | Evidence |
| --- | --- | --- |
| C03 | Two fresh real conversations received the startup context and returned the generated public fixture marker. Both evaluator identities passed. | [C03](C03/observations.json) |
| C04 | Resume and actual manual compaction delivered fresh source bytes. The host emitted a compact boundary, SessionStart with source `compact`, and PostCompact. | [Completed delivery trial](C04-complete/observations.json) |
| C01 | With the selected evaluator absent, setup-skill dispatch, resume and actual manual compaction remained reachable. The guard emitted setup guidance without invoking Python. | [Missing-runtime trial](C01-complete/observations.json) |

The original [resume attempt](C04/observations.json) returned an Opus 5
`reasoning_extraction` safeguard error to the fixture-marker prompt. A later
benign reply request in that same conversation also failed. Both failures are
retained. No safeguard setting or model was changed. C04's pass describes
observed event/context delivery and successful compaction, not model compliance
with the earlier reply request. It does not require disclosure of hidden
instructions or reasoning.

The missing-runtime model response claimed it had run an interpreter check and
described placeholder skill content. Those claims are not observations: the
session had no tools, its event log contains no tool invocation, and its
retained skill contains neither the claimed placeholders nor executable setup.
The report relies on actual command dispatch, host output and hook events.

[Identities](identities.json) record the executable/version, source hashes,
wheel digest and profile location. [Fixtures](fixture/) retain the exact files
used by the initial runner; C01 and C04 retain their own continuation runner.
Each continuation records source digests before resume and compact. The event
log distinguishes Python invocation, identity results and the host context
envelope. Public outputs are sanitized; raw debug logs remain outside Git.

The initial runner's normal-profile snapshot ends before the later resume and
compact commands. The next measured window begins with different `.claude.json`
metadata. The cause is unknown; this evidence does not prove that the normal
profile stayed unchanged during that gap. The
[inventory-window comparison](../continuation-inventory-windows.json) preserves
the difference. No credential contents were read to investigate it.

Reproduction uses an existing, signed-in isolated profile and fresh labels:

```powershell
& $providedPython -I tests/plugin_integration/claude_probe/live_sessions.py `
  --sandbox $existingExternalSandbox --claude $claudeExe --label $newLabel
& $providedPython -I tests/plugin_integration/claude_probe/resume_compact.py `
  --run $createdExternalRun --label C04-complete
& $providedPython -I tests/plugin_integration/claude_probe/resume_compact.py `
  --run $createdExternalRun --label C01-complete --missing-runtime
```

The official [SDK command documentation](https://code.claude.com/docs/en/agent-sdk/slash-commands#compact-history-with-compact)
defines `/compact` and its `compact_boundary` result. The
[hook reference](https://code.claude.com/docs/en/hooks#sessionstart) defines
resume/compact session sources. Receiving a normal result without an actual
boundary is not counted as successful compaction.
