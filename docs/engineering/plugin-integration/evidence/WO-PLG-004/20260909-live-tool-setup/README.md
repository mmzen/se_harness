# Real tool setup, repair and exact denial transport

Claude Code **2.1.266** ran these actions in the signed-in isolated profile.
All target paths are disposable. The selected wheel is the approved 0.16.0
archive. The existing supplied Python was used; no Python installation occurred.

| Observation | Evidence |
| --- | --- |
| The first Write stopped at Claude's read-before-write precondition, before the hook. This is not hook-denial proof. | [Initial Write](before-setup-write.json) |
| A real Bash tool created the external venv. Claude first appended an unauthorized `echo`; ordinary host permissions denied that extra command. The exact authorized command then succeeded. | [venv setup](setup-venv.json) |
| A real Bash tool installed the exact wheel with `--no-index --no-deps`. | [Offline installation](setup-pip.json) |
| A new session hook ran the selected evaluator and its identity check passed. | [After setup](after-setup-start.json) |
| The observer renamed only the disposable environment's interpreter. The next real host events show no interpreter invocation, then the authorized venv command restored it. | [Repair](repair-venv.json) |
| Pip reported the same package already installed. A subsequent session hook again passed evaluator identity. | [Repair pip](repair-pip.json), [After repair](after-repair-start.json) |
| A separate Read-then-Write trial satisfied the host precondition. The exact PreToolUse sentinel emitted `deny`; the host returned that refusal and the target hash stayed unchanged. | [Exact denial](exact-denial/observations.json) |

The exact sentinel compares the absolute path of one fixture file. It does not
interpret arbitrary commands, compute work-order authority, or implement
production policy. Its successful refusal proves host transport of that test
decision. Ordinary permission mode remained active; exact supplied-command
allow rules covered only the authorized venv and pip commands.

**Full C07 remains limited/unavailable.** The fixture always reports governance
readiness as false. Successful setup, evaluator identity and denial transport
do not establish a production ready state or its transition. This probe does
not silently turn an installation result into governance authority.

The model's final repair explanation said that nothing was repaired. Actual
host events establish a narrower, different fact: the interpreter was absent
before the repair command and successfully invoked afterward. Only the
interpreter was restored; reinstalling an unchanged wheel was unnecessary.
Model prose is retained but is not the source of that finding.

[C07](C07/observations.json) retains the full action sequence;
[identities](identities.json), [exact fixtures](fixture/) and
[isolation](isolation.json) identify the host, supplied Python, archive, sources
and bounded effects. The separate denial trial retains its updated sentinel
command and exact runner. Historical passive-observer trials are unchanged.

Normal-profile metadata is equal within the tool-setup runner's captured window.
That snapshot ends before the separate denial trial. Also, `.claude.json`
metadata differs between the earlier live-session snapshot and this runner's
initial snapshot. Those incomplete windows do not establish the cause or prove
an unchanged normal profile across the full continuation. See the
[inventory-window comparison](../continuation-inventory-windows.json). No
credential contents were read and no normal-profile file was restored.

```powershell
& $providedPython -I tests/plugin_integration/claude_probe/tool_setup.py `
  --sandbox $existingExternalSandbox --claude $claudeExe `
  --python $providedPython --wheel $releasedWheel --label $newLabel
& $providedPython -I tests/plugin_integration/claude_probe/denial_probe.py `
  --run $createdExternalRun --claude $claudeExe
```

The host's [PreToolUse contract](https://code.claude.com/docs/en/hooks#pretooluse-decision-control)
defines the denial response. The [permission documentation](https://code.claude.com/docs/en/permissions)
defines ordinary tool permission rules. No permission-bypass mode was used.
