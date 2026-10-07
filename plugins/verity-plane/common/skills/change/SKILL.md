---
name: change
description: Draft or amend an SE Harness artifact package and execute a selected work order through existing released workflow commands. Continue work already covered by actual authority, and stop the affected action when its scope, inputs or gates no longer match.
---

# Change

Turn the selected change into a coherent artifact package or carry its work
order forward. The installed harness decides lifecycle legality; this skill
connects its existing procedures to the operator's request.

## Hosted reading and context

For an explicit hosted test copy, follow setup's hosted selection.

For draft preparation, enter the selected release's
`docs/engineering/harness/DRAFT_DEFINITIONS.md`: read **Read this when**,
**Before this action**, and the current drafting step. Follow its prerequisites
before choosing a type, linking records or writing content. This includes
`ARTIFACT_AUTHORING.md#design-simplicity` and the selected type's checklist.
Read these instructions before the command schema. Do not load future lifecycle
procedures while the current task is drafting.

Before a lifecycle request, read the current released procedure and its applicable
prerequisites. Resolve paths against the selected released-resource directory,
not the test output directory. The command schema supplies fields, not policy.
Use an available file lookup to resolve one named resource; the full inventory
is evidence, not a prerequisite reading list. After choosing an operation, read
its schema section and referenced definitions. An operation-specific view must
identify its original schema and preserve its required fields and constraints.
The task-to-file table below locates instructions; only the released evaluator
determines the next action and whether it is permitted.

Keep complete requests and results in files. Read only the fields needed for
the current action, then the required procedure section. Use bounded file reads
or an available read-only JSON field selector. A selected field is not the full
result: inspect reported failures, required checks and incomplete-response flags
before proceeding. Do not read an entire historical transcript into context to
recover one artifact ID or result.

Keep a small transient progress note outside the repository when needed. Record
the current selection, exact last request/result paths, unresolved effects, and
the evaluator's current procedure/step and instruction references. Cite source
fields rather than copying large receipts. Update it after inspecting a result.
After compaction, use it to locate the original evidence and recover current
context; it grants no authority and does not replace a fresh required check.

## Private lifecycle test copy

When the approved task explicitly selects the hosted rehearsal, use the installed
candidate client's `remote rehearse --test-copy` command and the closed v2 request
schema in `server/contracts/lifecycle-v2.json`. Preview the exact action, then
apply it with that preview digest and unchanged versions. The service reruns the
released evaluator. After an uncertain reply, look up the original operation key;
do not rebase or invent a replacement key to conceal the outcome.

This is test data. Supplied actors are synthetic inputs, not human consent.
Imported records stay immutable. Keep real decisions and work in the authoritative
Git workflow. No rehearsal record authorizes a real release or external action.

| Current task | Released procedure to read |
| --- | --- |
| Complete draft content | `docs/engineering/ARTIFACT_AUTHORING.md` and the selected type's checklist |
| Record supplied definition/work decisions | `docs/engineering/harness/AUTHORITY.md` and `AUTHORIZE_WORK.md` |
| Start, retain handoff or complete work | The current step in `docs/engineering/harness/EXECUTE_WORK.md` |
| Prepare or assess a test VREC | The current step in `docs/engineering/harness/VERIFY_OUTCOME.md` |
| Prepare or assess a test RLS | The current step in `docs/engineering/harness/RELEASE.md` |
| Report a refusal or unknown reply | `docs/engineering/harness/RESULTS.md` |

These local-style commands run inside the service's disposable projection. Express
the selected operation through the closed v2 request; do not run it against the
real checkout. Read the literal target state from the released procedure. Words
such as "accept" in a task description are not lifecycle-state values to guess.
A refused edge is not a reason to try arbitrary states or freeze a context.

For `decide`, `action.decision` is the supplied actor identity; explanatory text
belongs in `action.reason`. Preserve the supplied option exactly: mitigation does
not authorize risk acceptance. Preparation owners must match the fixture's
supplied preparation identities. Do not infer a different actor or decision from
a passed gate, an available owner label or a generated record.

## Explicit hosted sandbox drafts

For an explicitly selected hosted sandbox, follow setup's hosted selection first.
Use its separate candidate client and retain the exact baseline or context/version.
Sandbox draft authority permits only the requested preparation. It does not change
repository authority or grant a human decision right.

Use `remote draft-open` to open a context at the selected baseline/work order.
Then use `remote create-artifact` with the released template type/domain, or
`remote revise-artifact` with the full UTF-8 document encoded as canonical base64.
All mutations take a transient JSON request outside the checkout. Follow the v1
command schema: include the expected project version, expected evaluator/client
identities, a new operation key, and the required context/revision guards.
An explicit artifact ID can create a draft in a new domain. Automatic allocation
requires an existing domain whose identifier token the evaluator can read.

```text
CLIENT_PYTHON -I -m se_harness remote create-artifact --endpoint ENDPOINT --project PROJECT --token-env TOKEN_VARIABLE --client-wheel ABSOLUTE_CLIENT_WHEEL --request ABSOLUTE_REQUEST_JSON --json
```

The same options apply to `draft-open`, `revise-artifact` and `freeze`. Import is
operator-only and accepts the configured complete canonical source manifest.
Read each accepted result's actual view, versions, affected revisions and receipt.
An incomplete template is a draft with findings. Baseline freeze is no approval.
Imported records and their lifecycle, decision and evidence claims are immutable.

After a stale-input refusal, read the current selection and review the change
before preparing a new request. Do not silently replace expected versions.
For uncertain transport, use `remote operation --key KEY` with the same
endpoint/project/credential, or retry the identical request and key. Do not create
a new key until the previous outcome is resolved. A different request under an
accepted key is refused. Never fall back to local writes.

For real governed work, use the local repository procedure below. The explicit
test-copy exception is described above under **Private lifecycle test copy**. It permits
rehearsal operations only; real remote decisions and authority cutover remain
unsupported.

## Repository context

Use the selected entry returned by activation in the current context. If no
checkout is active, follow the setup skill's activation procedure with the actual
checkout path and host/session values delivered by the hook. After switching or
compaction, validate the selected checkout again. Read applicable owner instructions.
AGENTS.md is not a plugin installation or instruction-delivery requirement.

For a `released-resources-v1` selection, use the exact evaluator's
`resources ABSOLUTE_REPOSITORY --resource RESOURCE_ID --content --json` to read one
required instruction or checklist. Resolve returned resource locations outside
the checkout; formal artifact paths stay relative to the checkout. Do not require
repository copies of ENGINEERING_HARNESS.md or docs/engineering/harness/.
For a legacy selection, use its validated repository entry and task router.

When a result includes `instruction_discovery`, require `status = "available"`.
Read its current step's exact file and heading and each prerequisite whose
condition applies. Read the selected formal records separately. The
`evaluator_only_inputs` are not normal agent reading. An incompatible result
stops the affected action; report the version/discovery gap.

For a released result without this field, use that installed root's procedure
router and reading manifest. Do not apply candidate instructions to an older
selected release. A manual root read does not prove automatic host delivery.

For drafting, design and review, read and apply the selected repository's
`docs/engineering/ARTIFACT_AUTHORING.md` resource: its shared design principle and the
questions relevant to the current artifact or review of implemented changes.

Use the repository-selected released evaluator in its private environment,
through the absolute Python path with `-I -m se_harness`. Run
`check ABSOLUTE_REPOSITORY --artifact ID --json` when beginning governed work,
then follow its procedure and required checkpoints. Preserve its actual result,
including failures. Run setup if the evaluator environment needs repair.

## Follow the selected operation

When the root selects `docs/engineering/harness/`, use its selected action
file and returned reading locations. The two legacy references below apply only
to installations without that collection; do not load them on the new route.

- For a package or amendment, read [Artifact packages](references/artifacts.md).
- For WO approval, start, implementation or completion, read
  [Work orders](references/work-orders.md).

On either route, before reusing a decision, apply the input comparison in
[Continuing authority](references/authority.md#continuing-authority). Before an
external mutation, read [External actions](references/authority.md#external-actions)
for this provider's required controls.

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
