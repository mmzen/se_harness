---
name: change
description: Draft or amend an SE Harness artifact package and execute a selected work order through existing released workflow commands. Continue work already covered by actual authority, and stop the affected action when its scope, inputs or gates no longer match.
---

# Change

Turn the selected change into a coherent artifact package or carry its work
order forward. The installed harness decides lifecycle legality; this skill
connects its existing procedures to the operator's request.

## Repository context

Use this repository's ENGINEERING_HARNESS.md in the current context. Read it
when it is absent, after switching repositories, or when its selected release
changes. Follow its task router and read applicable owner instructions when
present. AGENTS.md is not a plugin installation or instruction-delivery requirement.

When a result includes `instruction_discovery`, require `status = "available"`.
Read its current step's exact file and heading and each prerequisite whose
condition applies. Read the selected formal records separately. The
`evaluator_only_inputs` are not normal agent reading. An incompatible result
stops the affected action; report the version/discovery gap.

For a released result without this field, use that installed root's procedure
router and reading manifest. Do not apply candidate instructions to an older
selected release. A manual root read does not prove automatic host delivery.

For drafting, design and review, read and apply the selected repository's
`docs/engineering/ARTIFACT_AUTHORING.md`: its shared design principle and the
questions relevant to the current artifact or review of implemented changes.

Use the repository-selected released evaluator in its private environment,
through the absolute Python path with `-I -m se_harness`. Run
`check ABSOLUTE_REPOSITORY --artifact ID --json` when beginning governed work,
then follow its procedure and required checkpoints. Preserve its actual result,
including failures. Run setup if the evaluator environment needs repair.

## Follow the selected operation

When the root selects `docs/engineering/harness/`, use its selected action
file and returned reading locations. The legacy references below apply only
to installations without that collection; do not load them on the new route.

- For a package or amendment, read [Artifact packages](references/artifacts.md).
- For WO approval, start, implementation or completion, read
  [Work orders](references/work-orders.md).
- Before reusing any decision, apply the input comparison in
  [Continuing authority](references/authority.md).

Use the actual schema-2 result's procedure, gates and next action. An unchecked
next step supplies no decision. On a legacy installation, read its required
operating card and phase manifest as directed by that installed root. Skills
neither replace the released contracts nor authenticate their inputs.

Continue the selected approved execution under its installed policy without
another skill invocation or duplicate start, completion or preparation approval.
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
