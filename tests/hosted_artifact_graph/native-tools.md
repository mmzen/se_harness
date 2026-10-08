# Native test tools

Use `selection.json` for the exact `approved_shell_argv_prefix` and absolute
input/output paths. Append one helper operation per shell call. Use native
Read/Write/Edit for files. Keep normal permissions: no wrappers, loops, pipes,
directory listing, direct client commands or permission changes. This index
describes capabilities; it supplies no workflow or finished artifact.

## Typed authoring

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
| `read` (revision) | `--artifact ID --expected-revision REVISION` and `--baseline ID` or `--context UUID --context-version N`; no mutation fields |

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
| Fixture assertion | `assert-greeting --record ABSOLUTE_NEW_RECORD` |
| Text when native Read is unavailable | `read-text ABSOLUTE_FILE`; inventoried inputs or work files, at most 64 KiB |

For `instructions`, use canonical IDs such as `docs/engineering/harness/DRAFT_DEFINITIONS.md#read-this-when`. The earlier `released-resources/` inventory prefix also works. Request known sections together.

For known paths, use them directly. Inventory names are relative to the staged
inputs directory: `released-resources/docs/engineering/ARTIFACT_AUTHORING.md`,
`source/src/greeting.py`, `client-help/create-artifact.txt`. **Do not add `inputs/`
to these names.** Native Read takes the absolute path, not an inventory name.
A digest or lookup is not a content read. Unknown headings must not be guessed;
read the named file once to locate its actual headings. Request known current
sections together and reuse unchanged content. A full inventory is not required.

## Other operations

Raw mode remains `remote OPERATION --request ABSOLUTE_FILE --record ABSOLUTE_NEW_RECORD`.
Use it for operations without typed input, or when explicitly checking a raw
contract. Original schemas are under `reference/server/contracts/`. Selected
schema views use `schemas/remote-v1/OPERATION.json` or `schemas/read-v1/OPERATION.json`.
Each view retains its original pointer/digest. Lifecycle test-copy schemas are
separate; do not load them for drafting alone. `--key` reads a receipt, not a document.

Use `observations` before the final failure report. It reads existing native event/command captures and identifies the snapshot boundary; subsequent report writes are not yet counted. Keep its paths as evidence instead of copying every command. It supplies no draft text, content judgement or lifecycle decision.

Retain failed calls and recoveries. Template admission is not a content review.
Report only inspected facts and actual outcomes; distinguish unresolved content
from a completed definition. Do not claim an exhaustive failure count from memory.
