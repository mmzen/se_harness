# Checks after synchronizing the stacked base

The Claude probe branch inherits Codex probe commit
`fdff3a3046fb93fcc4b353c05e1c1af5ba8a5663`, including current main
`4ea947be4fb94e4d0ff137e8f0a3cf6148e3ba3a`. The released evaluator remains
the isolated 0.16.0 installation. The four repository checks in this directory
passed after synchronization; their command records retain the actual outputs.

## Handoff check and retry

The first handoff check reported four inherited Codex fixture paths outside
WO-PLG-004's scope. Its complete result is retained in
[handoff-initial-blocked.json](handoff-initial-blocked.json).

Subsequent direct Git comparisons found no changes to those inherited files.
The [investigation](git-path-investigation.json) repeated the released evaluator's
exact diff and untracked-file commands from both working directories, with
default, disabled and enabled Git long-path handling. All 12 commands succeeded;
none reported an inherited Codex path. The observer script is retained as
[source](investigate_probe_git_paths.py.txt).

An unchanged retry of the released handoff command then passed:
[handoff-retry-passed.json](handoff-retry-passed.json). No scope declaration,
governing evaluator, policy, or Git configuration was changed to obtain that
result. The cause of the initial discrepancy is not established; long-path
handling or Git stat-cache behavior has not been proved to be its cause.

The selected work order remains `in_progress`. Passing this mechanical check
does not exercise the engineering owner's completion decision or independent
assurance.
