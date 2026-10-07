# Native qualification retry: permission review

WO-HAG-009 is approved and in progress. VER-HAG-007 is approved. The first native
sessions are failed setup observations, not qualification passes.

## Observed results

- Codex CLI reached the supplied files and passed the local greeting assertion.
  Windows denied reading the archived wheel; Git refused the fixture under the
  sandbox identity. Service status returned project-access HTTP 403.
- Claude Code loaded candidate plugin 0.2.7 and discovered seven MCP tools.
  Its non-interactive session denied out-of-directory reads, writes, commands and
  MCP calls because no approval surface was available. No lifecycle test passed.
- Claude's configured default model returned HTTP 404. A session-only probe using
  `claude-haiku-4-5-20251001` returned AUTH_OK. Codex's live probe also passed.

The service failure was my setup error: new project UUIDs were created but the
fresh private principal entries still allowed only the old fixture project.
Both stores were observed at version zero. The correction binds each test key
only to its own new project; it changes no actual account, host or provider policy.
The fresh project IDs also change the deployment configuration digest. That
binding is corrected. Installed-client status now confirms both selected services
are ready at version zero. This is operator setup evidence, not an agent scenario.

## Proposed fresh-session permissions

1. Stage digest-checked copies of the selected public candidate wheel, plugin,
   schemas, guidance and synthetic source under each new session's `inputs/`.
   This replaces the unusable external build-directory layout in a fresh run.
   Preserve all old files, failed sessions and exact digests. No ACL or global
   Git safe-directory change is proposed.
2. Keep Codex workspace sandboxing and normal automatic approval review. Only
   the new test directory is writable. It uses the same bounded localhost service.
3. For Claude, pass [the exact proposed rules](claude-permissions-proposed.json)
   through its session-only `--settings` option. Permit reads of the new test
   directory, edits in `work/` and the two report files, all seven read-only hag
   MCP tools, and one fixed command prefix. Keep existing managed/deny rules and
   normal permission checking; no bypass mode or permanent host edit.
4. The command prefix invokes the reviewed
   [one-call helper](../../../../../tests/hosted_artifact_graph/native_call.py).
   It accepts a single bounded remote operation chosen by the agent, a local
   file encoding, identity hashing, or the exact greeting assertion. The fixed
   selection supplies the loopback endpoint, project, client and token variable.
   Requests/exports/records stay inside the new workspace. It neither supplies
   draft content nor chooses a sequence, decision, retry or next step.

The Claude session root is `C:\Users\mathi\Documents\Codex\2026-09-20\verity-plane-plugin-verity-plane-se\work\hag-agent-qualification-execution-20261007\claude\native02`. The precise allowed command prefix is:

```text
C:/Users/mathi/AppData/Local/Python/pythoncore-3.14-64/python.exe -I C:/Users/mathi/Documents/Codex/2026-09-20/verity-plane-plugin-verity-plane-se/work/hag-agent-qualification-execution-20261007/claude/native02/inputs/native_call.py
```

The agent still constructs and reads each request/result itself. A new denial
stops its affected action. Allow rules do not override a managed deny. Explicit
reads of staged material do not establish automatic startup/compaction delivery.

## Decision requested

Authorize these bounded session-only tool permissions and staged test inputs
for the new Codex/Claude runs. This is the missing native tool-permission grant,
not another work-order approval or acceptance of a qualification gap. No provider
settings, real credentials, actual repository decisions or global permission
settings are changed. Human verification remains separate.

The approved [work order](../../work-orders/WO-HAG-009.md) says: "Keep normal
permission checks. Do not bypass sandboxing, approval review or hook trust."
It also requires stopping a denied host action. That is why the refused native
actions have not been retried under broader permissions without this review.

## Documentation checked

Claude's [permission documentation](https://code.claude.com/docs/en/permissions)
defines session rules, Windows path matching and deny precedence. OpenAI's
[Windows sandbox documentation](https://learn.chatgpt.com/docs/windows/windows-sandbox)
describes the separate Windows sandbox execution identity. The actual CLI logs,
not these references, establish the observed failures.
