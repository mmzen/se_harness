## Hosted reading and context

Follow [Hosted selection](../../setup/references/hosted-context.md) once for the current unchanged selection.

For draft preparation, enter the selected release's
`docs/engineering/harness/DRAFT_DEFINITIONS.md`: read **Read this when**,
**Before this action**, and **Draft any missing definitions**
(`draft-any-missing-definitions`). Follow its prerequisites
before choosing a type, linking records or writing content. This includes
`ARTIFACT_AUTHORING.md#design-simplicity` and the selected type's checklist.
Read these instructions before the command schema. Do not load future lifecycle
procedures while the current task is drafting.

Before a lifecycle request, read the current released procedure and its applicable
prerequisites. Resolve paths against the selected released-resource directory,
not the test output directory. The command schema supplies fields, not policy.
Use the selected resource root with its known relative resource ID directly.
Use lookup only when a file's location is unknown. A full inventory is evidence,
not a prerequisite reading list. Use actual heading names from instructions or
an inspected file; do not guess a heading or repeat a failed section selection.
For raw request mode, read the selected operation schema and referenced
definitions. For typed mode, read the corresponding CLI/tool-index inputs; the
client constructs that existing schema. An operation-specific view must
identify its original schema and preserve its required fields and constraints.
The [lifecycle reference](hosted-test-lifecycle.md) locates later procedures; only the released evaluator
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


An available section reader can return complete selected sections together, with
source path, heading, release and SHA-256. Choose the sections required by the
current procedure; a pointer alone is not proof of reading. Reuse unchanged
content already in context. Missing, ambiguous or changed sources stop the read.

When using a section reader, request the known entry conditions, current step and
shared prerequisites together. For typed operations, the input table is sufficient
unless a needed field or constraint is absent; do not also discover raw schemas
or CLI help for fields already documented there.

## Explicit hosted sandbox drafts

For an explicitly selected hosted sandbox, follow setup's hosted selection first.
Use its separate candidate client and retain the exact baseline or context/version.
Sandbox draft authority permits only the requested preparation. It does not change
repository authority or grant a human decision right.

Use the installed client's typed mode for one selected operation at a time.
The supplied tool index or the selected product's
`docs/notes/harnessctl-reference.md#concise-hosted-authoring` describes the inputs. Select the operation, target,
expected versions and operation key yourself. Supply the exact evaluator identity
file from the selected inputs. The client verifies its installed wheel identity.

- `draft-open`: selected baseline and work order.
- `create-artifact`: domain, type, context/version and optional explicit artifact ID.
- `revise-artifact`: context/version, artifact, expected revision and UTF-8 document file.
- `import`: operator-only, using the configured complete canonical source manifest.

Use `--typed --compact --record-directory NEW_DIRECTORY`. `--include-document`
on create adds one read of that exact returned revision and saves its template.
Inspect the text before editing. This performs no subsequent mutation. Raw
`--request FILE` remains available; do not mix it with typed fields. Freeze uses
raw mode and is no approval. Never manually encode a document for typed mode.

An explicit artifact ID can create a draft in a new domain. Automatic allocation
requires an existing domain whose identifier token the evaluator can read.
Read the actual view, versions, affected revisions, receipt and findings.
A compact view retains the full response at its evidence path. Read any required
omitted findings before a conclusion. Imported records and their lifecycle,
decision and evidence claims stay immutable. A local capture failure after send
can leave a committed effect; reconcile the original operation key.

### Read and complete the created template

Apply the selected release's drafting sequence to one artifact at a time.
After `create-artifact`, inspect the `--include-document` result, or use the returned
`view` and `affected_artifacts` entry to [read that exact revision](../../harness-orient/references/hosted-reads.md#read-one-hosted-revision).
Inspect the returned UTF-8 document before editing it; creation findings alone
are not the document. Complete and review this draft under its type checklist,
then submit the full document with `revise-artifact` and inspect that result.
Only then create the next missing artifact. If reading or completing the current
draft is blocked, stop that step and report the exact error. Creating another
template does not resolve the failed step.

### Review and report the draft

Before calling a draft complete, read the finished text against its template
and selected type checklist. Check the claims against the source actually
inspected. Keep operational success measures separate from acceptance checks
where the template requires that distinction. An admissible result with no
incomplete fields is not a content-review verdict; report unmet writing guidance.

For verification or documentation of existing behavior, describe that requested
evidence or record. Do not claim missing behavior or absent definitions without
inspecting evidence for that claim. If an operational measure is not supplied,
report it as unresolved; do not replace it with an acceptance check or invent an
outcome to make a template look complete.

Report the observed method: source inspection, an executed test, or an evaluator
check. Include failed and denied calls, their recorded outcomes and any recovery.
Use exact result paths and fields for evidence. For instruction digests, cite the
matching lookup or inventory entry; if copying a value, compare that file's own
entry before reporting it. Omit an unconfirmed digest rather than guess one.
Retain the original failures even when a later call succeeds.
Do not call a failure list complete unless compared with the actual records.
A mechanical summary can supply the operation and failure list; your review
supplies the content judgement and limits.

After a stale-input refusal, read the current selection and review the change
before preparing a new request. Do not silently replace expected versions.
For uncertain transport, use `remote operation --key KEY` with the same
endpoint/project/credential, or retry the identical request and key. Do not create
a new key until the previous outcome is resolved. A different request under an
accepted key is refused. Never fall back to local writes.

