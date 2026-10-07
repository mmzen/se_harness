# Native Codex and Claude qualification — in progress

WO-HAG-009 and VER-HAG-007 were approved by mmzen. The work is in progress.
**Neither host is qualified yet.** No verification record has been prepared.

## First observations

| Host | Observed | Limitation |
| --- | --- | --- |
| Codex CLI 0.159.2 | Live provider request passed; candidate resources and configuration read; exact local greeting assertion passed | Archived wheel read denied; source Git access refused for ownership; service status rejected the wrong project-key binding |
| Claude Code 2.1.273 / Haiku 4.5 | Live provider request passed; candidate plugin 0.2.7 loaded session-locally; seven MCP tools discovered | Non-interactive tool permissions denied needed reads, commands, writes and the attempted MCP invocation |

The configured default Claude model returned HTTP 404. The successful probe used
the explicit session-only `claude-haiku-4-5-20251001` selection. It changed no
account or saved model settings. The exact responses and token usage are retained.

Both native processes exited zero after reporting blockers. Those exits are not
test passes. NQ-01 is partial; NQ-02 through NQ-05 remain blocked or unperformed.
No lifecycle mutation reached either project and no reply fault was triggered.
Operator inspection found both stores at version zero before setup correction.

## Findings and corrections

1. **Operator setup defect:** new project UUIDs were not propagated to the fresh
   sandbox keys' allowed-project lists. The lists now name only their respective
   approved test projects. Roles, accounts, provider policies and real artifacts
   are unchanged. Original observations are preserved. Independent installed-client status
   now confirms both corrected projects are ready at version zero; see
   [the exact commands and responses](corrected-project-status.json).
   A follow-up readiness probe also exposed a stale deployment digest after the
   project ID changed. Each disposable configuration now has its actual digest;
   see [the binding correction](deployment-binding-correction.json). No component
   compatibility check or historical package was changed.
2. **Native permission gap:** inputs were outside the native working directory,
   and Claude had no way to approve its first tool request. The proposed retry
   stages exact selected inputs and supplies explicit, bounded session permissions.
   These permissions have not been applied or used to retry the refused actions.
3. **Assessment correction:** Claude's final prose labels an MCP permission denial
   as an out-of-scope handoff demonstration. The actual tool result does not
   establish that scenario. Its transcript also repeats a denied directory action.
   These observations are retained; no pass or model-wide capability conclusion
   is inferred from this failed setup.

## Prepared retry

Read the [permission review](retry-review.md) and
[exact Claude rules](claude-permissions-proposed.json). A small one-call helper
permits a narrow command-prefix grant. It does not select workflow operations,
supply artifact text or perform recovery for the agent. Three focused tests pass:
path escape/existing destination refusal, external endpoint refusal, and preserving
the operator's exact endpoint/project in a requested call.

Git remains authoritative. Existing risks remain raised. The accepted verification
criteria, required checks and separate human verification decision are unchanged.
Desktop and automatic startup/compaction delivery are outside this contract.

## Evidence

- [Observed sessions and archive inventory](observations.json)
- [Bounded native transcripts, task inputs, failed results and command records](native01-observations.zip)
- The archive preserves the exact input, response and generated report bytes.
  Claims above are based on actual calls rather than the agents' summaries.
  Credentials, full profiles, environments, cloned repositories and container
  volumes are excluded.

No full source/distribution suite or final candidate verification is claimed at
this checkpoint. The work remains in progress pending the native tool-permission
decision and completion of all required scenarios.
