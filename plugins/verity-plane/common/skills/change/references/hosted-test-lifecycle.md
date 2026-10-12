# Hosted lifecycle instructions

Read [Hosted selection](../../setup/references/hosted-context.md) for the current selection.
Read the current released procedure and applicable prerequisites before its schema.
Resolve named inputs through the selected inventory, not a guessed local path.
Keep full requests/results in files; inspect failures, incompleteness and required
checks. Reuse unchanged instructions and recover them after compaction.

## Private lifecycle test copy

When the approved task explicitly selects the hosted rehearsal, use the installed
candidate client's `remote rehearse --test-copy` command and the closed v2 request
schema in `server/contracts/lifecycle-v2.json`. If a supplied test helper restricts
commands, use its documented spelling instead; do not append direct-client flags
that the helper does not accept. Preview the exact action, then
apply it with that preview digest and unchanged versions. The service reruns the
released evaluator. After an uncertain reply, look up the original operation key;
do not rebase or invent a replacement key to conceal the outcome.

Read the overall `outcome` before following any sub-command's next step. A refused
action commits none of its proposed effects, even if earlier sub-commands passed.
Inspect the failed command and correct its inputs before a new preview. Do not
apply a refused preview or guess a digest.

Before proposing a work order, apply
`docs/engineering/harness/WORK_AND_EVIDENCE.md#complete-work-scope` to the planned
handoff comparison. Include every intended changed path: new definitions, their
approval writes, implementation and generated evidence or paired decisions.
Definitions approved in the same rehearsal contribute changes after the retained
base. Before approval, compare each planned artifact-producing action with
`execution_scope.paths`, including each paired record. Future-output prose does
not add paths to that list; use the command preview or template to resolve them.

For a handoff's `from_git`, use a retained comparison base in the service's test
Git history that covers the complete work. In a fresh test copy, retain
`provenance.input_git_head` from its first accepted lifecycle mutation. An
unapplied preview's head may not be retained. The imported source commit identifies
provenance; it is not automatically present in this separate Git history. Do not
replace the retained base with a later head to omit changed files.
Keep the head, operation key and exact receipt path in transient working material
before continuing. Recover that evidence after compaction. A start result's head
does not replace the earlier approval input head.

This is test data. Supplied actors are synthetic inputs, not human consent.
Imported records stay immutable. Keep real decisions and work in the authoritative
Git workflow. No rehearsal record authorizes a real release or external action.

## Read the current procedure

Use the exact resource selectors below with the selected section reader. Read
only the current row and its applicable prerequisites. The evaluator's returned
current-step reference takes precedence if it selects a different section.
Read the complete current row together. The section view includes the selected
file's entry conditions; request `#before-this-action` explicitly if the selected
reader does not return them. Read any further prerequisite whose condition applies.
Reuse unchanged content while retained. After compaction, recover the current
row and its prerequisites before sending its request. A previous operation's
next step does not establish a different action's required reads.

| Current task | Released resource selector |
| --- | --- |
| Complete draft content | Use [Hosted drafting](hosted-drafts.md) for the selected type's exact checklist |
| Identify decision authority | `docs/engineering/harness/AUTHORITY.md#decision-rights` |
| Assess an approval package | `docs/engineering/harness/AUTHORIZE_WORK.md#assess-the-proposed-artifact-package`, `docs/engineering/harness/AUTHORITY.md#decision-rights` and `docs/engineering/harness/AUTHORITY.md#delegation-and-separation` |
| Apply supplied approval decisions | `docs/engineering/harness/AUTHORIZE_WORK.md#apply-the-selected-transitions`, `docs/engineering/harness/AUTHORITY.md#decision-rights` and `docs/engineering/harness/AUTHORITY.md#delegation-and-separation` |
| Start approved work | `docs/engineering/harness/EXECUTE_WORK.md#start-the-selected-work` and `docs/engineering/harness/AUTHORITY.md#authority-from-work-approval` |
| Record a risk and paired decision | `docs/engineering/harness/RISKS_AND_DECISIONS.md#record-risks-risk-affecting-the-change` and `docs/engineering/harness/RISKS_AND_DECISIONS.md#raised-risks` |
| Apply a supplied decision disposition | `docs/engineering/harness/AUTHORIZE_WORK.md#resolve-approval-blockers` and `docs/engineering/harness/AUTHORITY.md#decision-rights` |
| Retain handoff evidence | `docs/engineering/harness/EXECUTE_WORK.md#retain-the-implementation-evidence` and `docs/engineering/harness/AUTHORITY.md#authority-from-work-approval` |
| Complete work | `docs/engineering/harness/EXECUTE_WORK.md#record-implementation-completion` and `docs/engineering/harness/AUTHORITY.md#authority-from-work-approval` |
| Assess verification evidence | `docs/engineering/harness/VERIFY_OUTCOME.md#assess-the-verification-evidence` |
| Prepare a test VREC | `docs/engineering/harness/VERIFY_OUTCOME.md#prepare-the-verification-record` |
| Apply a supplied verification decision | `docs/engineering/harness/VERIFY_OUTCOME.md#record-the-verification-decision` and `docs/engineering/harness/AUTHORITY.md#decision-rights` |
| Prepare a test RLS | `docs/engineering/harness/RELEASE.md#prepare-a-release-record` |
| Apply a supplied release decision | `docs/engineering/harness/RELEASE.md#record-the-release-decision-when-required` and `docs/engineering/harness/AUTHORITY.md#decision-rights` |
| Report a refusal or unknown reply | `docs/engineering/harness/RESULTS.md#report-a-lifecycle-result` |

These local-style commands run inside the service's disposable projection. Express
the selected operation through the closed v2 request; do not run it against the
real checkout. Read the literal target state from the released procedure. Words
such as "accept" in a task description are not lifecycle-state values to guess.
A refused edge is not a reason to try arbitrary states or freeze a context.

For `decide`, `action.artifact` selects the paired **DEC**, not its RISK.
`action.decision` is the supplied actor identity, not the decision artifact ID;
explanatory text belongs in `action.reason`. Read the selected DEC and its current
evaluator result before choosing the disposition and option-specific fields.
Do not invent an `authority_owner` value to resolve a refusal. Preserve the
supplied option exactly: mitigation does not authorize risk acceptance.
A release contract (REL) is a definition. Use its supplied definition-approval
decision. An RLS decision or an artifact owner field does not grant that right.

Preparation owners must match the fixture's
supplied preparation identities. Do not infer a different actor or decision from
a passed gate, an available owner label or a generated record.

## Read the selected request shape

The v2 schema remains the input contract. In a staged native test its inventory
name is `reference/server/contracts/lifecycle-v2.json`. Read the complete schema
once when its envelope constraints are not already in context. Reuse unchanged
constraints. When only the selected action needs recovery, use its pointer below
instead of reading the whole schema again. These pointers select unchanged sections;
they do not replace its constraints or supply an operation sequence.

| Selection | JSON pointer |
| --- | --- |
| `validate` | `/properties/action/oneOf/0` |
| `check` | `/properties/action/oneOf/1` |
| `preflight` | `/properties/action/oneOf/2` |
| `transition` | `/properties/action/oneOf/3` |
| `decide` | `/properties/action/oneOf/4` |
| `raise-risk` | `/properties/action/oneOf/5` |
| `handoff` | `/properties/action/oneOf/6` |
| `capture-verification` | `/properties/action/oneOf/7` |
| `prepare-release` | `/properties/action/oneOf/8` |

Check that the selected schema's `kind.const` matches the intended action.
Use the original whole schema if this mapping does not match the selected version.
Keep all required envelope fields,
including `preview_digest: null` where the schema permits it for a non-apply
request. Use a new operation key for a different request; recover an uncertain
write through its original key and exact bytes.

A later missing path requires an authorized correction; do not expand approved
scope by editing its record.
