# Hosted lifecycle instructions

Read [Hosted selection](../../setup/references/hosted-context.md) for the current selection.
Read the current released procedure and applicable prerequisites before its schema.
Resolve named inputs through the selected inventory, not a guessed local path.
Keep full requests/results in files; inspect failures, incompleteness and required
checks. Reuse unchanged instructions and recover them after compaction.

## Private lifecycle test copy

When the approved task explicitly selects the hosted rehearsal, use the installed
candidate client's `remote rehearse --test-copy` command and the closed v2 request
schema in `server/contracts/lifecycle-v2.json`. Preview the exact action, then
apply it with that preview digest and unchanged versions. The service reruns the
released evaluator. After an uncertain reply, look up the original operation key;
do not rebase or invent a replacement key to conceal the outcome.

Read the overall `outcome` before following any sub-command's next step. A refused
action commits none of its proposed effects, even if earlier sub-commands passed.
Inspect the failed command and correct its inputs before a new preview. Do not
apply a refused preview or guess a digest.

For a handoff's `from_git`, use a retained comparison base in the service's test
Git history that covers the complete work. In a fresh test copy, retain
`provenance.input_git_head` from its first accepted lifecycle mutation. An
unapplied preview's head may not be retained. The imported source commit identifies
provenance; it is not automatically present in this separate Git history. Do not
replace the retained base with a later head to omit changed files.

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
