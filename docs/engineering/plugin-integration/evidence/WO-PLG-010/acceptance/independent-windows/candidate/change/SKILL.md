---
name: change
description: Draft or amend an SE Harness artifact package and execute a selected work order through existing released workflow commands. Continue work already covered by actual authority, and stop the affected action when its scope, inputs or gates no longer match.
---

# Change

Turn the selected change into a coherent artifact package or carry its work
order forward. The installed harness decides lifecycle legality; this skill
connects its existing procedures to the operator's request.

## Establish context

Before a governed write, require the current repository's verified governance
context: a freshly verified released evaluator, passing managed integrity, and
the complete managed `AGENTS.md` gate and `ENGINEERING_HARNESS.md` router read in
this session. A prior summary, successful lifecycle projection, or handler
receipt alone is insufficient. After compaction, a repository switch or changed
governance inputs, recover through `setup` and fresh context delivery first.

`setup` currently prepares the evaluator environment. It does not initialize a
repository or establish complete context by itself. Where the host supports
`session-context.py`, read its entire verified delivery through the matching
`END VERIFIED GOVERNANCE` marker; execute its exact full-read argument array
when requested. If verified delivery is unavailable, report that readiness
blocker. Do not invent a ready flag or bypass it by running a mutation directly.

Use setup's verified absolute environment Python with `-I -m se_harness` from
outside the checkout, with cleared `PYTHONPATH` and that environment's `Scripts`
or `bin` first in the process PATH. Here, `harnessctl` in returned argument arrays
means this invocation, not an ambient executable. Preserve argument boundaries
and use the absolute repository path. Inspect the selected release's command
help before first use; stop if an operation is unsupported.

## Follow the selected operation

- For a package or amendment, read [Artifact packages](references/artifacts.md).
- For WO approval, start, implementation or completion, read
  [Work orders](references/work-orders.md).
- Before reusing any decision, apply the input comparison in
  [Continuing authority](references/authority.md).

Read the installed operating card and every file in the selected phase reading
manifest. Use the actual schema-2 result's procedure, gates and next action.
An unchecked next step supplies no decision. These references route to
`WORKFLOW.json`, `DECISION_RIGHTS.md` and `ARTIFACT_AUTHORING.md`; they neither
replace those contracts nor authenticate their inputs.

Continue covered work without another skill invocation or duplicate approval.
If an operation is interrupted, inspect current files and checkpoint-free
`check --artifact ID` before retrying. Compare with its plan and retained result;
resume only unapplied effects. An uncertain write is a blocker, not permission
to replay the operation or overwrite its output.

At a stop or stage handoff, obtain the selected schema-2 result. Report actual
effects, final state, blocker or accountable decision, and its one typed next
step. A preview's proposed state is not an applied change. Report readiness
blockers separately from lifecycle projections. Evidence preparation follows
the installed procedure; use the `evidence` skill only if it is available.
