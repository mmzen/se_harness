# Claude Code activation probe

This Windows-only observation fixture supports WO-PLG-004. It is not a plugin
implementation, policy engine, or production support decision.

`probe.py` creates an isolated Claude profile and a disposable plugin outside the
checkout. The plugin exposes a setup skill and registers SessionStart,
PreToolUse and PostCompact. Its PowerShell guard observes whether the selected
interpreter exists. When it can run, `handler.py` calls the released evaluator's
identity command and records fixture context. It never grants authority.

The runner copies no credentials and changes no execution policy. It records
live host failures, including a guard that cannot start. Old/missing Python
features, interactive trust, resume, compact and real tool setup remain
unavailable unless actually exercised. An observer-created venv is not evidence
that Claude performed setup. The no-tools prompt only checks authentication.

Run from the repository root with an external Python:

```powershell
& $providedPython -I tests/plugin_integration/claude_probe/probe.py `
  --sandbox $newExternalSandbox --evidence $workOrderEvidence `
  --claude $claudeExe --python $providedPython --wheel $releasedWheel
& $providedPython -I -m unittest discover -s tests/plugin_integration/claude_probe -p 'test_*.py' -v
```

Use a new sandbox directory for each run. The evidence path must be
`docs/engineering/plugin-integration/evidence/WO-PLG-004/` in this checkout.
Archive an earlier run before reusing that evidence destination. The selected
wheel must match the published 0.16.0 archive SHA256 recorded by the repository
lock. No online package installation occurs.

The runner gives every case its required command/output/observation files.
Public captures pass through `publish_capture`, `publish_text` or `publish_json`
before writing. They redact credential fields, credential arguments, private
keys, bearer/API tokens and entire IPC authentication-example lines. Nested
JSON remains parseable. These are sanitized observations, not byte-for-byte raw
logs; local raw debug files stay in the disposable sandbox and must not be
published directly. This pattern-based filter does not prove arbitrary future
output is free of secrets; inspect new output formats before publication.
`sanitize_evidence.py` reapplies the filter to existing public captures and
records an audit, excluding the root agent's `governance/` directory.

Explicit failure results are retained. It reads only names,
sizes and timestamps when checking normal-profile files, including credentials;
unreadable inventory entries are reported as limitations. Evidence contains
local paths, but no credential contents. Linux and macOS are unavailable on this
host. The independent unit tests check reporting and isolation boundaries;
they do not establish Claude compatibility.

`inline_probe.py` runs a separate native PowerShell command trial against the
existing disposable sandbox. Always supply a new `--label` and a fresh
`--profile-name`; it refuses an existing profile, including a pending login.
It preserves exact settings, fixture files, manifest versions, event logs and
the limited before/after inventories. This runner restores only its task-owned
renamed interpreter and removes it again for C06; that is observer activity,
not host-tool setup evidence.

The inline guard emits the documented SessionStart `additionalContext` envelope
and stores identity telemetry in its event log. Arbitrary telemetry JSON is not
a Claude context protocol: the older trial's rejected output remains retained.
Recognized `--init-only` output does not prove delivery to an authenticated model.
