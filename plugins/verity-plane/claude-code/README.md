# Claude Code adapter

This adapter uses DEC-PLG-002's inline PowerShell route on Claude Code 2.1.266,
Windows, Python 3.14.6 and released evaluator 0.16.0. Configuration eligibility
does not establish qualification: inspect the WO-PLG-006 acceptance report for
actual host receipt, refusal and missing-enforcement observations.

Assemble this host manifest, hooks and binding helper alongside unchanged shared
scripts and the selected shared skills. Native discovery uses `skills/NAME/SKILL.md`;
the selected names are setup, change, evidence, harness-orient and
harness-operator-brief. Repository ownership migration and initialization are
separate work. The adapter adds no agents.

After accepting the package and preparing its private evaluator using the shared
setup skill, use `scripts/binding.py` with explicit `--repo`, `--environment`,
`--claude` and `--artifact` arguments. Retain its JSON in private plugin data,
outside both the repository and plugin cache. Pass the absolute JSON path in
`VERITY_PLANE_CLAUDE_BINDING` to the selected absolute Claude executable. The
helper prints a selection; it installs nothing and grants no work authority.
An unavailable selection or environment returns UNREADY guidance. Do not edit
an installed cache, change execution policy, or substitute an unaccepted host.

The two synchronous command hooks are generated from `hooks/guard.txt`; the
registered command contains its inline text. No script-file PowerShell route is
used. `SessionStart` forwards startup, resume and compact events to the shared
session handler. Context is bounded to 32768 UTF-8 bytes; complete-read fallback
is disabled. Anything larger remains UNREADY. Delivered-byte proof is required
for any readiness assessment.

`PreToolUse` maps Write/Edit through the shared handler's existing pre-action
check. Unmapped tools receive an explicit coverage gap while ordinary host
permissions and authorized setup remain available. Success never emits an
`allow` permission decision. Missing binding or output cannot be repaired by
the missing component itself: inspect hook diagnostics and actual target effects.

Bindings reserve 60 seconds at the host, 35 seconds for evaluator work and
5 seconds each for startup, process-tree cleanup and response. These are explicit
candidate budgets; qualification requires observing their adequacy. Both bindings
are synchronous. Lost guard startup, host cancellation, or missing denial proves
no protection and leaves the affected route unqualified.

The unchanged shared scripts own evaluator identity, integrity, lifecycle checks,
path mapping and evaluator process control. The host binding only preserves
arguments, transports bytes, validates envelopes and reports activation failures.
It emits diagnostic JSON on stderr, never writes an approval or readiness cache,
and does not override host permissions.

References: [hook protocol](https://code.claude.com/docs/en/hooks),
[native plugin layout](https://code.claude.com/docs/en/plugins-reference).
