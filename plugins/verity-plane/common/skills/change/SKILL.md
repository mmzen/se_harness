---
name: change
description: Draft or amend an SE Harness artifact package and execute a selected work order through existing released workflow commands. Continue work already covered by actual authority, and stop the affected action when its scope, inputs or gates no longer match.
---

# Change

Turn the selected change into a coherent artifact package or carry its work
order forward. The installed harness decides lifecycle legality; this skill
connects its existing procedures to the operator's request.

## Repository context

Read the selected repository's AGENTS.md and ENGINEERING_HARNESS.md on entry,
after compaction, and after switching repositories. Read the operating card and
the reading manifest for the selected work. Use normal file reads.

For drafting, design and review, read and apply the selected repository's
`docs/engineering/ARTIFACT_AUTHORING.md`: its shared design principle and the
questions relevant to the current artifact or review of implemented changes.

Use the repository-selected released evaluator in its private environment,
through the absolute Python path with `-I -m se_harness`. Run
`check ABSOLUTE_REPOSITORY --artifact ID --json` when beginning governed work,
then follow its procedure and required checkpoints. Preserve its actual result,
including failures. Run setup if the evaluator environment needs repair.

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
If an operation is interrupted, inspect current files and lifecycle history
before retrying. For a WO, VREC, RLS or DEC, also use checkpoint-free
`check --artifact ID`; that command does not accept definition artifacts.
Compare the readback with the plan and retained result; resume only unapplied
effects. An uncertain write is a blocker, not permission to replay the
operation or overwrite its output.

At a stop or stage handoff, obtain the selected schema-2 result. Report actual
effects, final state, blocker or accountable decision, and its one typed next
step. A preview's proposed state is not an applied change. Report readiness
blockers separately from lifecycle projections. Evidence preparation follows
the installed procedure; use the `evidence` skill only if it is available.
