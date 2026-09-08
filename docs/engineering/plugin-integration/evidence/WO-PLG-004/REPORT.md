# Claude Code probe: partial observations

WO-PLG-004 remains in progress. This report supplies evidence for review; it
does not complete the work, verify a candidate, or select production support.
All seven full acceptance cases remain **unavailable/incomplete**. Positive
startup observations below must not be read as passing those whole cases.

## What was actually observed

On Windows, Claude Code **2.1.265** loaded a disposable inline plugin and found
its setup skill. `--init-only` ran its SessionStart hook without a conversation.
The initial `powershell.exe -File guard.ps1` route was rejected by the machine's
existing execution policy. The script never started. The failure is retained
in the original C01–C07 outputs and debug logs; no policy setting was changed.

A separately identified inline PowerShell command, registered through the
documented hook `shell` and `command` fields, ran successfully. It does not
read or evaluate the refused script. Its live host events show missing-runtime
guidance, two invocations of the prepared evaluator, hook disable/enable behavior,
a version change followed by restart, and detection of the removed interpreter.
This proves these particular startup observations, not before-tool enforcement.

The first inline trial called `identity` with an incorrect expected root and
no checkout boundary. Its failed identity result remains in [native-inline](native-inline/).
The corrected trial uses the environment root and disposable repository boundary.
Both repeated identity calls passed, with version 0.16.0, matching payload SHA256
and an observed archive SHA256 matching the supplied wheel. See
[corrected C03](native-inline-corrected/C03/observations.json).
The fixture always reports `governance_readiness: false`.

The observer created the disposable environment with supplied Python **3.14.6**,
then installed the existing wheel offline with `--no-index --no-deps`. This was
not a Claude tool action and cannot satisfy C07.

## Case coverage and remaining work

| Case | Retained observation | Still needed; whole-case status |
| --- | --- | --- |
| C01 | Plugin inventory, setup skill, registered events, actual SessionStart. File route refused; inline route ran. | Actual resume, compaction and setup reachability; unavailable. |
| C02 | Real missing-interpreter shell check gives guidance; no Python download or repository initialization. | Old Python and unusable venv/ensurepip profiles, plus the actual host setup entry; unavailable. |
| C03 | Two real corrected startup calls return matching evaluator identity and fixture context bytes. | Model-visible delivery, beyond init-only output; unavailable. |
| C04 | Governance content changed. A real bounded no-tools prompt returned `authentication_failed` and “Not logged in”. | Actual authenticated resume/compact and fresh context comparison; unavailable. |
| C05 | Disabled hooks emitted zero fixture events; re-enabled hooks emitted SessionStart. | Interactive trust/permission interaction; unavailable. |
| C06 | Paths with spaces worked; restart after plugin version change preserved the plugin-data path; removed interpreter was not invoked. | Interactive reload and any resulting permission interaction; unavailable. |
| C07 | No Claude tool setup, repair or governed write was performed. The target's recorded hash stayed unchanged. | Actual tool-driven setup/repair and independently observed unready write; unavailable. |

The corrected prepared-start trials took **1.900 s** and **2.007 s**. These are
two local observations, not a performance claim. The plugin-data path remained
under the isolated profile and was stable across the tested version restart.
Linux and macOS were unavailable on this machine and were not simulated.

## Evidence and reproduction

- [Original cases](C01/observations.json) retain the PowerShell file refusal,
  missing authentication, commands, exits and sanitized host output. The first strict
  manifest check also caught missing author metadata; the corrected manifest
  passed with no warnings. Empty original inventory output was not discovery
  proof: the original variadic MCP argument consumed that subcommand.
- [Corrected inline inventory](native-inline-corrected/C01/stdout.txt),
  [events](native-inline-corrected/events.jsonl), and C01/C03/C05/C06 subdirectories
  retain the separate working startup route. Exact generated fixture snapshots
  are under [fixtures](fixtures/), including the failed identity caller.
- [Identities](identities.json) record the supplied interpreter, wheel digest,
  initial fixture hashes, platform and documentation. [Unit test evidence](unit-tests.json)
  records final source hashes and fifteen passing independent observer tests.
  Those tests check isolation/reporting boundaries, not live host compatibility.
- [Isolation](isolation.json) records unchanged readable normal-profile metadata.
  The global Git ignore inventory was inaccessible; its state is unknown.
  No credential files were opened by the probe or copied. The probe writes
  only its declared fixture/evidence paths and disposable sandbox. It does not
  change execution policy or the installed Claude binary. Metadata checks do
  not establish a complete inventory of the operator's whole profile.

Use the commands in [the fixture instructions](../../../../../tests/plugin_integration/claude_probe/README.md).
Run `probe.py` with a fresh external sandbox. Then run `inline_probe.py` against
that sandbox, with a fresh `--label` and `--profile-name` to retain a separate
trial. Each case's `actions.txt` and `commands.json` preserve the exact observed
argv; `stdout.txt`, `stderr.txt` and debug logs preserve results. Current code
contains the corrected manifest/inventory/identity calls; earlier failures are
retained rather than silently replaced.

At the end of these trials, the task-owned evaluator executable is renamed
`python.removed` to retain the C06 condition. Only that disposable environment
may be repaired. The normal provided interpreter remains intact.

Official references used: [CLI](https://code.claude.com/docs/en/cli-reference),
[plugin reference](https://code.claude.com/docs/en/plugins-reference),
[hooks](https://code.claude.com/docs/en/hooks),
[settings](https://code.claude.com/docs/en/settings), and
[credential isolation](https://code.claude.com/docs/en/authentication#credential-management).

## Current handoff

Public debug/output captures are sanitized observations, not byte-for-byte raw
logs. Review found local IPC authentication examples in host debug logs even
without account login. The retained copies were redacted, and both runners now
sanitize before writing any public debug, command, event or observation capture.
Sensitive JSON fields/arguments are replaced; credential-bearing text lines and
IPC injection examples are removed whole. Local raw debug logs remain outside
the checkout and must not be published directly. [The redaction audit](redaction-audit.json)
records application to existing public captures. Seven new tests cover these
paths, nested JSON, unchanged diagnostics and repeat sanitization. No host or
login profile was invoked or changed during this fix.

The official login flow for the isolated `run-20260908-02/isolated profile` is
being handled separately by the operator. The corrected startup trial used a
different `identity recheck profile`. Authentication completion, additional
host actions and the remaining C01–C07 evidence must be observed before making
a completion claim. No VREC or production activation decision is created here.
