# Claude Code probe: partial observations

**WO-PLG-004 is implemented following the engineering owner's explicit
completion decision.** Candidate verification and production support remain
separate decisions.
The Windows inline-plugin trials on Claude Code **2.1.266** complete
**C01, C03, C04, C05, C06 and C07** as observation cases.
**The full C02 prerequisite matrix remains incomplete.** These case
findings do not qualify a production integration or establish full case coverage.
The [current case index](case-status.json) points to the latest assessment for
each case; original failed and incomplete attempts remain unchanged.

## What was actually observed

In the earlier 2026-09-08 trials, Claude Code **2.1.265** on Windows loaded a
disposable inline plugin and found
its setup skill. `--init-only` ran its SessionStart hook without a conversation.
The initial `powershell.exe -File guard.ps1` route was rejected by the machine's
existing execution policy. The script never started. The failure is retained
in the original C01-C07 outputs and debug logs; no policy setting was changed.

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
That earlier fixture always reports `governance_readiness: false`.

Review of that older trial found a separate fixture defect: Claude explicitly
ignored its arbitrary JSON output keys. Returned identity and context telemetry
were real, but that output did not deliver governance context. The failure stays
in the original logs. The [2026-09-09 trial](20260909-context-envelope/README.md)
observed Claude Code **2.1.266**. It keeps telemetry in the event log and emits
the documented SessionStart
`hookSpecificOutput.additionalContext` envelope. Claude's debug log now confirms
that it received 61 characters of additional context. This is protocol receipt
from `--init-only`, not proof that an authenticated model processed the context.

After isolated sign-in, the [authenticated session trial](20260909-live-sessions/README.md)
observed two real conversations receiving the fixture context, fresh delivery
after resume and completed compaction, and the missing-runtime route through
startup, skill dispatch, resume and compact. C04 preserves a model safeguard
refusal; its passing finding is fresh hook/event delivery and actual compaction,
not compliance with a request to repeat context.

The observer created the disposable environment with supplied Python **3.14.6**,
then installed the existing wheel offline with `--no-index --no-deps`. This was
not a Claude tool action and cannot satisfy C07. A later
[real tool trial](20260909-live-tool-setup/README.md) created the venv, installed
the exact wheel offline and repaired the deliberately removed interpreter
through Claude's Bash tool. A separate Read-then-Write trial reached the exact
test sentinel: the host applied its denial and the file stayed unchanged.
A [later complete trial](20260909-live-ready-repair-02/README.md) used explicitly
synthetic governed inputs and real released preflight/check results. It observed
fresh `ready:true` and nine-file context receipt before interpreter removal,
then actual tool repair and fresh readiness/context again. This supplies the
C07 readiness sequence without implementing a production adapter or recording
a real lifecycle decision. The first attempted readiness run stopped on an
evidence-parser error; that incomplete attempt remains retained.

## Case coverage and remaining work

| Case | Retained observation | Still needed; whole-case status |
| --- | --- | --- |
| C01 | Missing-runtime startup, setup-skill dispatch, resume and actual manual compaction; no interpreter invoked. Earlier file-route refusal retained. | Pass for the authenticated inline route. Model claims of tool activity are excluded where no tool was invoked. |
| C02 | Actual setup-skill dispatch checks an absent provided Python using an exact scoped Bash command; tool result records missing-path exit 2 and operator installation guidance. | Older Python and unusable venv/ensurepip variants remain unavailable. See [prerequisite trials](20260909-live-prerequisite-scoped/README.md). |
| C03 | Two authenticated fresh conversations received the marker provided only in fixture hook context; both identities passed. | Pass. Earlier ignored-JSON output remains retained. |
| C04 | Actual resumed and compacted sessions delivered fresh source digests and context bytes; compact boundary and PostCompact retained. | Pass for event/content delivery. A model safeguard refusal is preserved and is not counted as a successful reply. |
| C05 | Fresh disabled/enabled runs retain exact settings, commands, events, exits and durations. Disabled hooks emitted no event; enabled hooks emitted SessionStart. | Pass for the recorded inline/init-only route. No interactive trust-dialog claim. |
| C06 | Fresh runs retain before/after manifest versions and digests, paths with spaces, two restarts and persistent-data metadata. Removed Python was not invoked. | Pass for the recorded process-restart route. No hot-reload or marketplace-install claim. |
| C07 | Real tool setup, exact Write denial, genuine released-evaluator readiness and fresh nine-file context; interpreter removal, actual tool repair and fresh readiness/context again. Repository hashes and profile metadata match within this trial. | Pass for the inline Windows probe with synthetic test inputs. No production adapter, support decision or real authority transition. |

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
- [Original identities](identities.json) record the supplied interpreter, wheel
  digest, initial fixture hashes, platform and documentation. The fresh trial
  has its own [identities](20260909-context-envelope/identities.json) and exact
  executed runner copies. [Current unit evidence](20260909-final-tests/unit-tests-final.json)
  records the current runner hashes and 29 passing independent tests. Five
  execute native PowerShell against explicit test data to check the output
  boundary; none simulates proof of Claude compatibility. The earlier fifteen
  tests remain in the [historical unit evidence](unit-tests.json).
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

At the end of the historical C06 trials, the task-owned evaluator executable was
renamed `python.removed`. The authenticated continuation restored that
environment for session checks, then used a different disposable environment
for real-tool setup and repair. Those later environments are left prepared;
the earlier renamed-executable condition is not their final state.

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

The operator completed the official login flow for
`run-20260908-02/isolated profile`. A normalized auth-status check confirmed the
login without publishing account details or credential material. Later live
trials used that same profile and new disposable fixtures. The unavailable older/unusable C02 prerequisite combinations remain an
explicit limitation. No VREC or production activation decision is created here.

The authenticated continuation also has an isolation-evidence limitation:
normal `.claude.json` metadata changed between two separately captured windows.
Resume/compact and the later denial trial lacked their own before/after normal
profile snapshots. The cause is unknown, so the full continuation cannot be
reported as proving an unchanged normal profile. The
[window comparison](continuation-inventory-windows.json) preserves this gap;
credential contents were not read and unowned files were not restored.
