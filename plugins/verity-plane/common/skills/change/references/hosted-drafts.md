## Read the selected instructions once

Complete [Hosted selection](../../setup/references/hosted-context.md) once for
the unchanged selection. Use its separate candidate client and exact baseline
or context/version. Draft preparation grants no decision right or Git authority.

Read the selected release's `docs/engineering/harness/DRAFT_DEFINITIONS.md`:
**Read this when**, **Before this action**, and the requested type's procedure:

| Type | Procedure |
| --- | --- |
| Verification | **Define how the result will be verified** |
| Release or operating contract | **Prepare a release or operating contract** |
| Other definition | **Draft any missing definitions** |

Follow its applicable prerequisites before choosing a type, linking or writing.
These include `ARTIFACT_AUTHORING.md#design-simplicity` and the type checklist:
use full names such as `#intent`, `#verification`, or `#work_order`, not codes.
Read instructions before command fields. Load [lifecycle procedures](hosted-test-lifecycle.md)
only when needed; the released evaluator selects the next step.

Reuse exact sections already supplied with source identity. For missing sections,
use the selected resource root and known IDs; request independent sections together.
Batch independent file reads when their exact paths are known. Read their complete
content; pointers alone do not prove reading. Look up only unknown paths. A missing,
ambiguous or changed source stops that read.
For released 0.22.1, the repeated `CONTINUE.md#continue-selected-work` heading
requires its unique `#procedure` parent, not the later typed-step index.

## Decide whether the inputs support a draft

Before create or revise, check each required claim against the request and
definitions already read:

| Content | Source or authoring authority |
| --- | --- |
| User problem, improvement, success measure, or existing gap | Require a source that supplies it. A creation request does not supply missing facts. |
| Proposed method, check, or evidence destination | Choose within the requested design scope. Label it as planned, without claiming observation or execution. |

For an **intent**, identify the change in the user's situation and how the owner
will observe whether it helped. Producing a record, running a check or confirming
output describes an engineering activity. Do not invent an operational purpose
to make it fit the template. An unmeasured baseline cannot supply a missing
outcome or measure.

Before claiming a coverage gap, read the applicable requirements, specifications
and verification contracts. Code or one same-type record cannot establish their
absence. For a verification plan, derive expected values from definitions; name
the check, pass condition and complete proposed evidence path, including filename.
Resolve any work-order directory in that path.

For a missing required fact, state the question and stop dependent writing.
A partial draft may omit it and remain incomplete. An unsupported required claim
cannot become a non-blocking observation. Report a type/outcome mismatch without
changing type. Use the existing report below.

## Author and submit supported content

Use typed inputs from the tool index or
`docs/notes/harnessctl-reference.md#concise-hosted-authoring`, without also loading
raw schemas/help for documented fields. Choose the operation, target, versions,
key and document. Supply the evaluator identity file; the client checks its wheel.
Import is operator-only and uses the complete source manifest.

Use `--typed --compact --record-directory NEW_DIRECTORY`, or the restricted
helper's documented permission route. Raw `--request FILE` requires its schema
and referenced definitions. Do not mix modes or encode typed documents manually.
Freeze is raw-only and grants no approval. Explicit IDs permit a new domain;
automatic allocation needs an existing domain with an evaluable ID token.

After create, inspect `--include-document` or [read the exact revision](../../harness-orient/references/hosted-reads.md#read-one-hosted-revision).
The option reads and saves the template without another mutation. Findings are
not the document. Fill only supported content. Review the text against the type
checklist before submission: remove unsupported claims, duplicate checks and
constraints absent from the definitions. For verification, confirm each assertion
tests its stated pass condition. Record the review in the existing report.
Resolve or report a blocked read before continuing.

Submit the full UTF-8 file through `revise-artifact`. Inspect the actual document,
versions, receipt and findings before starting another draft. Imported records,
lifecycle history, decisions and evidence remain immutable.

## Retain the result and recover uncertainty

Keep complete requests/results in files; read required omitted findings before
concluding. Keep one short transient report outside the repository:

- **Content readiness:** your assessment against the requested type's checklist.
  Use complete when the required content is supported and reviewed; incomplete
  when required content is missing or unsupported; blocked when an unavailable
  input or action prevents assessment. State the actual reason.
- **Saved state:** selection, revision, versions and exact document/result paths.
- **Validation and review:** evaluator findings, separate content-review findings,
  missing inputs or uncertain effects, and the returned procedure/step if available.

Draft validation checks template shape and required links. Its `content_review`
value `not_assessed` means the evaluator did not assess content. It does not by
itself make your content review incomplete. An empty `incomplete` list does not
make your review complete. Perform and report that review separately.
Saving, reading back or reviewing a draft does not verify its planned checks.
Describe future checks as planned. Use the same readiness and actual-check
claims in the report and final reply.
Reuse the report after compaction to locate evidence and obtain fresh context.

Report the observed method: source inspection, executed test or evaluator check.
Include failed and denied calls after recovery. Use mechanical observations before
an exhaustive failure claim; link them rather than rewriting inventories or metrics.
Add content findings and limits to the same report. Use exact evidence paths and
confirmed inventory digests; omit unconfirmed values.

After stale input, inspect the current selection; do not silently refresh versions.
After an uncertain reply or capture failure, inspect `remote operation --key KEY`
with the same selection and credential, or retry identical bytes/key. Resolve the
effect before selecting a new key. Changed bytes under an accepted key are refused.
Never fall back to local writes.
