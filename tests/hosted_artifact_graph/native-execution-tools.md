# Execution tools

Read this only when the selected task calls for executing a check. For drafting
a verification contract, describe the proposed check and retained evidence in
the artifact. A command listed here does not authorize its execution.

Use the same `approved_shell_argv_prefix` and one-helper-call boundary from
`selection.json`. The fixture assertion is:

```text
assert-greeting --record ABSOLUTE_NEW_RECORD
```

This executes the selected fixture's `greeting()` assertion. Retain its actual
result at the selected new path. Source inspection alone is not an executed test.
