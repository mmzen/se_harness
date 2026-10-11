# Execution tools

Read this when choosing a check for a verification plan or executing an
authorized check. Use these capabilities to assess whether the plan can run in
the selected environment. A listed command does not authorize execution.

Use the same `approved_shell_argv_prefix` and one-helper-call boundary from
`selection.json`. The fixture assertion is:

```text
assert-greeting --record ABSOLUTE_NEW_RECORD
```

This runs the selected fixture's `greeting()` once and asserts that its result
equals `Hello rehearsal`. It runs locally through `selection.json`'s
`client_python`, on the native test host; it does not run inside the Linux
service. The source digest must match the selected `greeting_sha256` before
execution. It makes no separate type assertion.

The new record retains the exact command, working directory, exit status,
stdout, stderr and elapsed time. Exit 0 with `exact greeting passed` records a
passing equality assertion. A failing assertion returns a nonzero exit. The
record does not contain a Python version or create commit-bound verification.
Use the selected source manifest/commit and digest to identify the tested input;
keep test-fixture identity separate from a later verification candidate.

Retain actual results at the selected new path. Source inspection alone is not
an executed test. Do not claim a different platform, extra assertions or evidence
fields from this tool. A required check beyond these capabilities remains a gap.
