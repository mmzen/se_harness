# Windows inline-hook continuation, 2026-09-09

This is a live Claude Code 2.1.266 trial under a fresh, unauthenticated profile.
It uses the documented inline PowerShell command form. It neither evaluates the
previously refused `.ps1` nor changes the execution policy. The pending login
profile is untouched.

The previous handler's JSON was observational telemetry. Claude ignored its
unknown fields. This revision retains telemetry separately and emits only the
documented SessionStart context envelope. The real host now records
`provided additionalContext (61 chars)` in both prepared startup logs. An
authenticated conversation is still needed to observe the model using it.

| Case | Result | Evidence |
| --- | --- | --- |
| C01 | Incomplete: missing-runtime guidance and discovery observed; resume/compact still pending. | [Observation](C01/observations.json) |
| C03 | Incomplete: two identities pass and the host recognizes the context envelope; no conversation started. | [Observation](C03/observations.json), [first host log](C03-first.debug.txt), [second host log](C03-second.debug.txt) |
| C05 | Pass for this route: disabled hooks emit no event; enabled hooks emit SessionStart. The explicit settings change is the enablement interaction. | [Observation](C05/observations.json), [disabled settings](C05/settings-disabled.json), [enabled settings](C05/settings-enabled.json) |
| C06 | Pass for this route: version change plus process restart preserves the plugin-data location; removed Python is not invoked. Paths contain spaces. | [Observation](C06/observations.json), [old manifest](C06/manifest-before.json), [new manifest](C06/manifest-after.json) |

C02, C04 and C07 were not executed in this continuation. These conclusions are
observations for the assessed route, not an assurance decision. Linux and macOS
are unavailable on this Windows machine.

The [identity record](identities.json) names host/version, wheel/payload digests,
source hashes and references. The [fixture](fixture/) preserves the exact input
files and executed runner sources. Review corrected each case's provenance link
to this run's identity record; that reporting-only correction is marked in the
observations. [Nineteen passing unit tests](unit-tests.json) record the final
source hashes. They validate reporting and native output boundaries with
explicit test data, not live Claude compatibility.

The `guard.ps1` and `handler.py` source snapshots were first captured through
the text-output sanitizer, which normalized their line endings. Review replaced
only these two fresh snapshots with the exact private fixture bytes after
confirming they match both the recorded SHA256 and repository source. This
corrects source capture, not a host result. Host logs remain sanitized text;
source snapshots and their digests preserve the executed bytes.

Each case has actions, command output, exits and duration. The
[event log](events.jsonl) records the host-provided event, interpreter and data
path. [Isolation checks](isolation.json) show unchanged listed normal-profile
metadata and unchanged top-level disposable repository files. This is not a
complete inventory of the normal profile. Public outputs are sanitized; raw
debug logs stay in the external sandbox.

To reproduce after the original probe created its disposable environment and
retained `python.removed`, run from this checkout with new label/profile names:

```powershell
& $providedPython -I tests/plugin_integration/claude_probe/inline_probe.py `
  --sandbox $existingExternalSandbox --claude $claudeExe `
  --label $newEvidenceLabel --profile-name $newDisposableProfileName
```

The observer restores only that environment's renamed executable for the
prepared-start trials, then renames it back for C06. This is **not** host-tool
setup or repair evidence for C07. The runner rejects an existing profile name.

Protocol expectations come from the official [SessionStart hook contract](https://code.claude.com/docs/en/hooks#sessionstart-decision-control).
The [hook settings documentation](https://code.claude.com/docs/en/hooks#disable-or-remove-hooks)
defines `disableAllHooks`. The [plugin reference](https://code.claude.com/docs/en/plugins-reference#edit-reload-and-disable-a-skills-directory-plugin)
documents restarting to pick up hook changes. No interactive hot-reload or
marketplace-install behavior is claimed.
