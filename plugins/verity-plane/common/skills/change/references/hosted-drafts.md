## Select the instructions

Complete [Hosted selection](../../setup/references/hosted-context.md) once for
the unchanged selection. Use its separate client and exact baseline or context
version. Draft preparation grants no decision right or Git authority.

Read the selected release's `docs/engineering/harness/DRAFT_DEFINITIONS.md`:
**Read this when**, **Before this action**, and the requested type's procedure:

| Type | Procedure |
| --- | --- |
| Verification | **Define how the result will be verified** |
| Release or operating contract | **Prepare a release or operating contract** |
| Other definition | **Draft any missing definitions** |

Follow its applicable content rules and prerequisites, including
`ARTIFACT_AUTHORING.md#design-simplicity` and the type checklist. Use full type
names such as `#intent`, `#verification`, or `#work_order`, not codes.

The released procedure's `harnessctl ... REPO` examples act on repository files.
For this hosted selection, use the remote operations in the selected tool index
or `docs/notes/harnessctl-reference.md#concise-hosted-authoring`. Do not combine
their arguments with local command examples. The content rules still apply.

Reuse complete sections already delivered with source identity. Obtain missing
sections together from the selected resource root; batch independent file reads
with known paths. A pointer is not a read. Missing, ambiguous or changed sources
stop the affected action. For 0.22.1's repeated
`CONTINUE.md#continue-selected-work` title, read its unique `#procedure` parent.
Load [lifecycle instructions](hosted-test-lifecycle.md) only for that task.

## Check the inputs before writing

Compare the requested type's required content with the request and definitions:

| Content | Source or authoring authority |
| --- | --- |
| User problem, improvement, success measure, existing gap | Require a source that supplies it. A creation request supplies no missing fact. |
| Proposed method, check, evidence destination | Choose within the requested design scope; label it planned. |

For an intent, identify the change in the user's situation and how the owner
will observe whether it helped. Producing a record, running a check or confirming
output is an engineering activity; do not invent an operational purpose.
An unmeasured baseline cannot supply a missing outcome or measure.

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
constraints absent from definitions. Each verification assertion must test its
stated pass condition. Report this content review separately from template checks.

Submit the complete UTF-8 file with `revise-artifact`. Inspect the saved document,
versions, receipt and findings before another draft. Imported records, lifecycle
history, decisions and evidence stay immutable. Resolve blocked reads first.

## Report and recover

Retain complete requests and results in files. Read required omitted findings.
Keep one short transient report outside the repository:

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
After compaction, reuse this report to locate evidence and obtain fresh context.

For stale input, inspect the selection without silently refreshing versions.
For an uncertain reply or capture failure, look up `remote operation --key KEY`
with the same selection and credential, or retry identical bytes and key. Resolve
the effect before selecting another key. Changed bytes under an accepted key are
refused. Never fall back to local writes.
