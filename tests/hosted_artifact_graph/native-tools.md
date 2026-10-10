# Native test tools

Use `selection.json` for the exact `approved_shell_argv_prefix` and absolute
input/output paths. Append one helper operation per shell call. Use native
Write/Edit for files; read with native Read or the documented `read-text` helper.
Use one `read-text` call for independent files whose exact paths are known.
Keep normal permissions: no wrappers, loops, pipes,
directory listing, direct client commands or permission changes. This index
describes capabilities; it supplies no workflow or finished artifact.

## Draft mutations

Prefer typed input for the operations below. This table supplies their CLI fields;
you do not also need their raw schemas or help files unless a needed field is
missing. Choose the operation, target, versions, key and content yourself.

```text
remote OPERATION --typed --compact --record ABSOLUTE_NEW_RECORD [FIELDS]
```

Every typed mutation takes `--operation-key KEY --expected-project-version N
--evaluator-file FILE`. Use the selected `evaluator_file` path. The fixed adapter
supplies the selected endpoint/project/token environment and exact installed
client wheel. The client constructs the existing request and verifies its identity.

| Operation | Other fields |
| --- | --- |
| `import` | `--source-manifest FILE`; use selected `source_manifest` |
| `draft-open` | `--baseline ID --work-order WO-ID` |
| `create-artifact` | `--context UUID --context-version N --domain NAME --artifact-type TYPE`; optional `--artifact ID --include-document` |
| `revise-artifact` | `--context UUID --context-version N --artifact ID --expected-revision REVISION --document-file FILE` |

The client never refreshes a version or retries a mutation on its own. Typed and
raw input cannot be mixed. Documents are exact UTF-8 files. No manual base64 or
copied client digest is needed. `--include-document` adds one read of the exact
created revision, returning text or a decoded file path. Inspect it before editing.

`--record` retains the command. Its new `.evidence` directory retains exact
requests/responses and decoded documents. The displayed `client_view` is the
client's own view. Inspect outcomes and findings; read required omitted content.
Do not reread a whole receipt just to extract a small field already displayed.
A capture error after send can leave a committed effect. Reconcile its original
key with `remote operation --key KEY --record ABSOLUTE_NEW_RECORD`.

## Read one revision

```text
remote read --typed --compact --record ABSOLUTE_NEW_RECORD --artifact ID --expected-revision REVISION --context UUID --context-version N
```

For an imported baseline, replace the context fields with `--baseline ID`.
Reads take no `--operation-key`, `--expected-project-version` or `--evaluator-file`.
Choose the exact revision and context from the selected inputs or actual results.

## Reads and discovery

| Need | Operation |
| --- | --- |
| Service readiness and selected components | `remote status --record ABSOLUTE_NEW_RECORD` |
| Local wheel metadata | `identity` |
| Captured calls/failures so far | `observations`; includes recovered and denied native calls, no content verdict |
| Complete released instruction sections | `instructions --section "RESOURCE_ID#HEADING"`; repeat for up to 12 sections |
| One unknown input location | `find-file BASENAME --under RELATIVE_DIRECTORY/` |
| One exact inventory entry | `lookup-file RELATIVE_NAME` |
| One saved JSON field | `read-json ABSOLUTE_FILE --pointer '"/field"'`; omit pointer for root; optional `--keys` |
| A raw base64 field | Add `--decode-base64` to that field read |
| One text file or independent reads together | `read-text ABSOLUTE_FILE [ABSOLUTE_FILE ...]`; up to eight selected inventoried inputs or work files, at most 64 KiB output |

For `instructions`, use canonical IDs such as `docs/engineering/harness/DRAFT_DEFINITIONS.md#read-this-when`. The earlier `released-resources/` inventory prefix also works. Request known sections together.
For authoring checklists and the repeated released 0.22.1 continuation heading,
use the exact selectors in the selected plugin's `change/references/hosted-drafts.md`.

For known paths, use them directly. Inventory names are relative to the staged
inputs directory: `released-resources/docs/engineering/ARTIFACT_AUTHORING.md`,
`source/src/greeting.py`, `client-help/create-artifact.txt`. **Do not add `inputs/`
to these names.** Native Read takes the absolute path, not an inventory name.
A digest or lookup is not a content read. Batch independent reads when their exact
paths are known. Unknown headings must not be guessed;
read the named file once to locate its actual headings. Request known current
sections together and reuse unchanged content. A full inventory is not required.

Source inspection and test execution are different actions. Drafting a verification
contract describes future checks; it does not require running them. If the task
authorizes execution, use [Execution tools](native-execution-tools.md).

## Other operations

Raw mode remains `remote OPERATION --request ABSOLUTE_FILE --record ABSOLUTE_NEW_RECORD`.
Use it for operations without typed input, or when explicitly checking a raw
contract. Original schemas are under `reference/server/contracts/`. Selected
schema views use `schemas/remote-v1/OPERATION.json` or `schemas/read-v1/OPERATION.json`.
Each view retains its original pointer/digest. Lifecycle test-copy schemas are
separate; do not load them for drafting alone. `--key` reads a receipt, not a document.

Use `observations` before the final failure report. Its snapshot does not include
later report writes. Link it; it supplies no content judgement or lifecycle decision.
Follow the hosted drafting guide for review, failure reporting and recovery.
