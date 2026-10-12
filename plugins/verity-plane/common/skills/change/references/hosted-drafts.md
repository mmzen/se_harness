## Select the current step

Use exact instructions already delivered with their source identity. Reading that
content satisfies its read instruction. Open its file only if required content
is missing, changed or no longer retained. A pointer alone is not content.

Complete [Hosted selection](../../setup/references/hosted-context.md) once for
the unchanged selection. Draft preparation grants no decision right or Git authority.

Match the request and existing confirmed context to the current step:

| Available inputs | Read from the selected release |
| --- | --- |
| The intended outcome or scope still needs clarification | `docs/engineering/harness/DEFINE_CHANGE.md`: **Read this when**, **Before this action**, then **Describe the intended outcome**. Use **Define the limits of the change** when its inputs are available. |
| Confirmed outcome, scope and selected definitions; a definition draft is needed | `docs/engineering/harness/DRAFT_DEFINITIONS.md`: **Read this when**, **Before this action**, then the requested type's procedure below. |

The clarification procedure produces transient discussion, not a formal artifact.
Use its requester-confirmation process and reuse an existing matching confirmation.
An instruction to create a draft does not supply the inputs that procedure requires.
Do not import, open a draft context or create a template merely to ask a question.
For a clarification stop, include three short parts in the final reply:

- **Actions:** State whether any hosted change was attempted. Include observed
  failures or denials.
- **Known inputs:** Keep existing definitions and supplied scope limits.
- **Questions:** Ask only for missing facts needed now.

This retained reply is the transient report only if no hosted mutation command
was invoked and the captured attempted-call record is complete. Refused or denied
mutation commands are still attempts. If capture is incomplete or its completeness
is unknown, use the saved report in **Report and recover** and state that limit,
even when no change was observed. The clarification reply
needs no duplicate file or new lifecycle checkpoint.

For a requested intent, consult `docs/engineering/ARTIFACT_AUTHORING.md#intent`
when identifying missing content. Read other prerequisites when their stated
condition applies. Before selecting artifacts, load the clarification procedure's
artifact and link references. Before drafting, use this type table:

| Type | Drafting procedure |
| --- | --- |
| Verification | **Define how the result will be verified** |
| Release or operating contract | **Prepare a release or operating contract** |
| Other definition | **Draft any missing definitions** |

Apply the drafting procedure's prerequisites, including
`ARTIFACT_AUTHORING.md#design-simplicity` and the type checklist. Use full type
names such as `#intent`, `#verification`, or `#work_order`, not codes.

For a release contract in a private lifecycle test, the source fixture commit
is not the disposable Git candidate that verification will capture. Do not
complete or approve a contract with a guessed candidate. If the final candidate
is not yet known, defer completing and approving the contract. Take its exact
`candidate_commit` from the final verified VREC, complete the release scope and
evidence requirements, then obtain the contract's required decision. An explicitly
supplied candidate constraint remains binding.

The released `harnessctl ... REPO` examples act on repository files. Hosted work
uses the selected tool index or `docs/notes/harnessctl-reference.md#concise-hosted-authoring`.
Do not combine their arguments. The canonical content rules still apply.

Obtain missing sections together from the selected resource root; batch independent
file reads with known paths. Missing, ambiguous or changed sources
stop the affected action. For 0.22.1's repeated
`CONTINUE.md#continue-selected-work` title, read its unique `#procedure` parent.
Load [lifecycle instructions](hosted-test-lifecycle.md) only for that task.

## Check the inputs before writing

Compare the requested type's required content with the request and definitions:

| Content | Source or authoring authority |
| --- | --- |
| User problem, improvement, success measure, existing gap | Require a source that supplies it. A creation request supplies no missing fact. |
| Proposed method, check, evidence destination | Choose within the requested design scope; label it planned. |

For an intent, resolve the user's problem, desired improvement and way to observe
that improvement. Ask for missing inputs and reuse confirmed ones. Message text,
channels or function signatures describe a solution; they do not explain why the
user needs it. An unmeasured baseline is allowed; a missing success measure stays
missing. Do not offer `not measured` as a replacement for how the owner will know
the change helped. Do not invent a purpose or measure from engineering activity.

Before claiming a coverage gap, read the applicable requirements, specifications
and verification contracts. Code or one same-type record cannot establish their
absence. For a verification plan, derive expected values from definitions; name
the check, pass condition and full proposed evidence path, including filename
and any work-order directory. In an environment with restricted execution tools,
read their capability descriptions before choosing the check. This is a planning
read, not test execution. Match the planned assertions, platform and evidence
fields to those tools. Distinguish the local test runtime from the service and lifecycle evaluator.
If a required condition cannot be assessed with the available tools, report that
gap before requesting approval; do not promise an unavailable check.

Distinguish a missing input from a draft omission. Ask for a required fact absent
from the confirmed inputs and stop dependent writing. If the fact is available
and only the draft omits it, correct the editable draft within the requested
scope. A partial draft stays incomplete. Report a type/outcome mismatch without
changing type or inventing a fact.

## Author and submit

Choose the operation, target, expected versions, retry key and content. Use the
documented typed fields and evaluator identity file; do not also load raw schemas
for those fields. Import is operator-only and uses the complete source manifest.

Use `--typed --compact --record-directory NEW_DIRECTORY`, or the selected helper's
documented permission route. Raw `--request FILE` needs its schema and referenced
definitions. Do not mix modes or manually encode typed documents. Freeze is
raw-only and grants no approval. Explicit IDs permit a new domain; automatic
allocation requires an existing domain with an evaluable ID token.

Inspect the created template through `--include-document` or
[an exact revision read](../../harness-orient/references/hosted-reads.md#read-one-hosted-revision).
Findings are not the document. Complete only supported content and review it
against the type checklist. Trace each verification pass condition to its
governing definition and planned check. Remove unsupported claims, duplicate
checks and constraints absent from definitions; an unrequested extra check is
not a required gap. Correct omissions from confirmed inputs before stopping.
Report the content review separately from template checks.

Submit the complete UTF-8 file with `revise-artifact`. Review the saved document
and its returned versions, receipt and findings. If this review finds a supported
in-scope correction, revise the draft and review the new saved revision.
`revise-artifact` edits an editable draft, not an approved or imported record.
Lifecycle history, decisions and evidence stay immutable. If a protected-record
refusal occurs, stop that revision. Do not retry it with changed state, history
or content. A separate draft proposal does not amend or replace an accepted
record; use the selected release's amendment boundary and obtain any missing
authority before dependent work. Resolve blocked reads first.

## Report and recover

For the clarification reply, use **Select the current step**. Otherwise retain
complete requests/results and one short report outside the repository, including
after a mutation attempt or uncertain effect. Read required omitted findings.
The report contains:

- **Content readiness:** one conclusion: complete, incomplete or blocked against
  the selected type checklist. Refer to the latest saved revision. A correction
  resolves the earlier omission; an unresolved required gap prevents completion.
- **Saved state:** selection, revision, versions and exact document/result paths.
- **Validation and review:** evaluator findings, independent content findings,
  local and remote failures (including recovered ones), denials, uncertain effects,
  and any returned procedure/step. Use observations before exhaustive failure claims.
  Its snapshot excludes later calls: add their failures, including failed reads of
  that snapshot. Link evidence; do not copy inventories.

Draft validation checks template shape and required links. `content_review`
being `not_assessed` means only that the evaluator did not assess content. It
does not invalidate your separate review; an empty `incomplete` list does not
complete it. Name the method: source inspection, executed test or evaluator check.
Planned checks are not executed tests. Keep report and final reply consistent.
Separate successful reads from accepted mutations. Attribute facts to their
actual source: response metadata is not content in the saved artifact. Use only
confirmed paths/digests; saving alone establishes no completeness.
After compaction, recover the retained reply or report and obtain fresh context.

For stale input, inspect the selection without silently refreshing versions.
For an uncertain reply or capture failure, look up `remote operation --key KEY`
with the same selection and credential, or retry identical bytes and key. Resolve
the effect before selecting another key. Changed bytes under an accepted key are
refused. Never fall back to local writes.
