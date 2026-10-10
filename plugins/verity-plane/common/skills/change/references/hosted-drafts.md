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

For an intent, ask which change in the user's situation is needed and how the
owner will know it helped, when those inputs are missing. An audience name or
replacement output alone does not answer those questions. Reuse supplied answers;
do not invent a purpose or measure from an engineering activity or baseline.

Before claiming a coverage gap, read the applicable requirements, specifications
and verification contracts. Code or one same-type record cannot establish their
absence. For a verification plan, derive expected values from definitions; name
the check, pass condition and full proposed evidence path, including filename
and any work-order directory.

State a missing required fact as a question and stop dependent writing. A partial
draft may omit it and remain incomplete. Do not call an unsupported required claim
a non-blocking observation. Report a type/outcome mismatch without changing type.

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
against the type checklist. Remove unsupported claims, duplicate checks and
constraints absent from definitions. For every verification pass condition,
identify the planned check that assesses it. Add a missing check or narrow the
claim; an untested condition prevents a complete-content claim. Report this
review separately from template checks.

Submit the complete UTF-8 file with `revise-artifact`. Apply that review to the saved
document, then inspect its versions, receipt and findings before another draft. Imported records, lifecycle
history, decisions and evidence stay immutable. Resolve blocked reads first.

## Report and recover

For the clarification reply, use **Select the current step**. Otherwise retain
complete requests/results and one short report outside the repository, including
after a mutation attempt or uncertain effect. Read required omitted findings.
The report contains:

- **Content readiness:** complete, incomplete or blocked against the selected
  type checklist. Give the supported content or exact missing input; saving alone
  establishes no completeness.
- **Saved state:** selection, revision, versions and exact document/result paths.
- **Validation and review:** evaluator findings, independent content findings,
  captured command observations including recovered failures and denials, uncertain
  effects, and any returned procedure/step. Use mechanical observations before an
  exhaustive failure claim. Link original evidence; do not copy its inventories.

Draft validation checks template shape and required links. `content_review`
being `not_assessed` means only that the evaluator did not assess content. It
does not invalidate your separate review; an empty `incomplete` list does not
complete it. Name the method: source inspection, executed test or evaluator check.
Planned checks are not executed tests. Keep report and final reply consistent
about readiness and actual checks. Use only confirmed paths/digests.
After compaction, recover the retained reply or report and obtain fresh context.

For stale input, inspect the selection without silently refreshing versions.
For an uncertain reply or capture failure, look up `remote operation --key KEY`
with the same selection and credential, or retry identical bytes and key. Resolve
the effect before selecting another key. Changed bytes under an accepted key are
refused. Never fall back to local writes.
