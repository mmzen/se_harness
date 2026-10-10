## Check the facts before drafting

Read the request and the existing definitions needed for each claim. Keep three
things separate: what a source states, its lifecycle state, and what is unknown.
A draft or untested definition is still an existing record. Do not describe it
as absent, or invent a problem to justify the requested new artifact.

Apply the selected type's checklist before creating or revising:

- For an intent, establish the present problem, affected user, wanted improvement
  and how the owner will observe that benefit. An output check alone does not
  establish an operational benefit. Ask for facts the sources do not provide.
- For missing behavior or checks, inspect the relevant requirement, specification
  and verification contract. Code or a same-type record cannot establish absence.
- For a verification plan, define the check, pass condition and complete proposed
  evidence filename. Resolve any work-order directory; distinguish planned
  evidence from existing results and execution authority.

If required input is missing, state the unanswered question in the transient
report and stop dependent writing. A partial draft may retain supported facts
and identify unknowns; it must not replace unknowns with plausible statements.
Before saving, compare its problem and outcome claims with the inspected sources.
Correct contradictions in the draft itself; an incomplete label in the report
does not correct false content. Report a type/outcome mismatch without choosing
a different type or inventing a benefit.

## Read the applicable instructions once

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
Group independent known file paths into one bounded read. Read their complete
content; pointers alone do not prove reading. Look up only unknown paths. A missing,
ambiguous or changed source stops that read.
For released 0.22.1, the repeated `CONTINUE.md#continue-selected-work` heading
requires its unique `#procedure` parent, not the later typed-step index.

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
not the document. Fill the template and review it against the type checklist.
Remove duplicate checks and constraints absent from the definitions. For
verification, confirm each assertion tests its stated pass condition.
Resolve or report a blocked read before continuing.

Submit the full UTF-8 file through `revise-artifact`. Inspect the actual document,
versions, receipt and findings before starting another draft. Imported records,
lifecycle history, decisions and evidence remain immutable.

## Retain the result and recover uncertainty

Keep complete requests/results in files; read required omitted findings before
concluding. Keep one short transient report outside the repository:

- **Content readiness:** complete, incomplete or blocked, with the reason. Any
  unresolved required content finding makes it incomplete, even after a successful save.
- **Saved state:** selection, revision, versions and exact document/result paths.
- **Validation and review:** evaluator findings, separate content-review findings,
  missing inputs or uncertain effects, and the returned procedure/step if available.

Draft validation checks template shape and required links. An empty `incomplete`
list is not a content verdict; the agent performs the content review.
Reuse the report after compaction to locate evidence and obtain fresh context.

Report the observed method: inspection, executed test or evaluator check. Include
failed and denied calls after recovery. Link mechanical observations and exact
evidence instead of copying their fields into the report. Use them before an
exhaustive failure claim. Add content findings and limits; omit unconfirmed values.

After stale input, inspect the current selection; do not silently refresh versions.
After an uncertain reply or capture failure, inspect `remote operation --key KEY`
with the same selection and credential, or retry identical bytes/key. Resolve the
effect before selecting a new key. Changed bytes under an accepted key are refused.
Never fall back to local writes.
