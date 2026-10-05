---
name: change
description: Draft or amend an SE Harness artifact package and execute a selected work order through existing released workflow commands. Continue work already covered by actual authority, and stop the affected action when its scope, inputs or gates no longer match.
---

# Change

Turn the selected change into a coherent artifact package or carry its work
order forward. The installed harness decides lifecycle legality; this skill
connects its existing procedures to the operator's request.

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

The rest of this skill applies to local governed work. Remote lifecycle decisions,
verification/release preparation and authority cutover are unsupported here.

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
