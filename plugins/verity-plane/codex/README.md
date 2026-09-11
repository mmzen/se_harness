# Codex binding

This component implements the native inline route selected by DEC-PLG-001:
Codex CLI 0.153.4, Windows, Python 3.14.6, and released evaluator 0.16.0.
Installation and acceptance in WO-PLG-005 are confined to disposable profiles.
The acceptance report, not this manifest or a successful script invocation,
states which host behavior was actually observed.

The assembled package maps `.codex-plugin/plugin.json`, `hooks/hooks.json` and
`codex/dispatch.py` from this directory. Its `scripts/` and selected `skills/`
come unchanged from the common source at the same commit. The assembly fixture
selects setup, change and evidence. Overlapping retained repository skills are
not activated by this selection; ownership migration remains separate work.

`native-guard.txt` is source for a direct native command string, not a script-file
launch. `render_hooks.py` writes that string into each hook; `--check` detects
drift. The accepted host executes the inline command in its native Windows
shell. No nested PowerShell command, execution-policy change or cached-payload
edit is used. The current generic Plugin Creator validator does not accept
the `hooks` manifest key; native 0.153.4 discovery is the relevant acceptance
surface for this explicitly selected route. No generic-validator pass is claimed.

## Explicit binding inputs

Install the immutable assembled plugin through its disposable local marketplace,
review its actual commands using `/hooks`, and retain native discovery and trust
observations. Select the executable by absolute path and record its actual
version and digest before each acceptance sequence. A profile label in JSON is
not evidence of the running host's version.

Prepare the private evaluator with the existing shared setup procedure. One
`binding.json` in the host's documented `PLUGIN_DATA` directory selects one
already initialized fixture repository, prepared environment and work order:

```json
{
  "schema": "verity-codex-binding-v1",
  "repo": "C:\\absolute\\disposable repository",
  "environment": "C:\\absolute\\private environment",
  "artifact": "WO-PROBE-001",
  "profile": {"host": "0.153.4", "os": "windows", "python": "3.14.6", "evaluator": "0.16.0"},
  "capture": false
}
```

These are explicit transport inputs, not approval or cached readiness. The
guard never installs dependencies or selects an ambient interpreter. Missing
inputs/runtime produce UNREADY guidance; supplied inputs still run fresh shared
identity and context checks. A 0.17 repository lock does not match this profile.
Set `capture` only for reviewed disposable acceptance: it appends local argv,
input digests, evaluator diagnostics and response observations to
`PLUGIN_DATA/observations.jsonl`. That diagnostic log has no decision authority.

## Events and coverage

SessionStart startup/resume/clear/compact invokes the unchanged
`session-context.py` with absolute Python, `-I -B`, fixed released identities,
a 16,000-byte context capacity and no assumed complete-read fallback. Full
delivery still needs a matching end marker in the actual host receipt.

PreToolUse native `apply_patch` invokes unchanged `check-tool-action.py` with
the selected work order. It owns mapping, current evaluator checks and process
tree cleanup. Denials are forwarded; a passed check returns additional context,
never a permission override. Other actual tools receive an explicit unenforced
coverage warning while ordinary host permissions and authorized setup remain
available. Malformed before-tool fields receive a denial.

Both bindings are synchronous with a 30-second outer timeout. The shared tool
handler gets an 8-second inner budget plus 4-second startup, 4-second cleanup
and 2-second response reserves. Actual startup, complete transport and accepted
denial must fit those budgets in live acceptance. The dispatcher returns output
after the shared process finishes; a shared timestamp alone proves no host
receipt. Host timeout, absent binding, launch failure and missing denial require
independent effect inspection before any retry and cannot qualify enforcement.

The adapter grants no lifecycle, repository connection, release or external
action authority. Shell commands, continuing sessions, MCP and unobserved
routes remain coverage gaps. A disabled hook cannot report its own absence;
use the host's hooks inventory and current acceptance observations.
