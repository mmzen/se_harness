# Work orders

Select one WO and read its approved behavior, paths, constraints, verification
contract and phase reading manifest. Use `check REPO --artifact WO-ID --json`
to inspect its actual state and procedure. Projection is read only.

## Approval and execution

Read the installed `DECISION_RIGHTS.md` and `WORKFLOW.json` for the grant made
by work-order approval. Follow their execution procedure and returned commands;
do not maintain a second authorization test in this skill. Where approval
covers execution, continue the selected eligible work without requesting another
start, completion or required verification-preparation decision. A person or
agent follows the same procedure; no additional agent needs to be launched.

Approval itself leaves a WO approved until start is applied. Run the required
start preflight, preview and apply the selected transition, then inspect state.
Use the actual executor identity; a role argument cannot create missing approval.
Each `ID=value` remains one argument. A preview does not start implementation.

## Implement and complete

Continue edits and ordinary local commits within the approved scope. Compare
proposed behavior and paths with that scope. Use the `scope` checkpoint with
the complete change set and intended paths. Use `pre-action` when the installed
procedure calls for it, rather than adding a new gate before every edit.
An allowed directory does not authorize unrelated behavior.

Run the selected verification contract and repository checks, retain actual
outcomes and relevant failures, and review the diff and tests. Apply
`docs/engineering/ARTIFACT_AUTHORING.md#review-of-implemented-changes` during
that review. Retain material findings and their resolution with ordinary evidence.

Follow the installed handoff procedure using its trusted Git base and complete
change set. Handoff and evidence commands can write retained evidence; check
their actual destinations against the approved preparation scope.
Once work and required evidence are complete, preview and apply the selected
completion transition. Record only work actually completed.

Follow required verification preparation already covered by approval without
another request. An implemented WO classified `not_required` needs no new VREC:
report completion and follow the authorized delivery instruction, if any.
Preparation, owner acceptance and external delivery remain distinct actions.

## Stops and continuation

An actual missing grant, changed scope or failed gate stops the affected action.
Repair an in-scope failure and reuse unchanged authority. Ask the accountable
owner for a scope change when necessary; do not switch execution routes or
claim an owner decision to bypass a refusal. Follow the installed evaluator's
actual requirements while a repository still uses an earlier release.

Use [Continuing authority](authority.md) for already supplied decisions. No
execution grant permits self-verification, release, merge or publication.
Reuse a separately authorized delivery action when its inputs still match.
