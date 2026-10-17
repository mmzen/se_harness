# Native test tools

Append one operation to `selection.json`'s exact `approved_shell_argv_prefix` per
shell call. Use native Write/Edit; native Read takes absolute paths. No wrappers,
loops, pipes, listing, direct client commands or permission changes.
This is a capability guide, not workflow authority.

Records, evidence and exports require new paths under selected `work/`; other
locations are refused before execution. Use selected absolute paths or include
`work/` in relative paths. Observations scan only `work/`.

## Draft mutations

Prefer typed input; consult raw schemas/help only for missing fields.
The selected plugin's hosted-drafts reference governs authoring and reporting.

```text
remote OPERATION --typed --compact --record ABSOLUTE_NEW_RECORD [FIELDS]
```

All take `--operation-key KEY --expected-project-version N --evaluator-file FILE`
(selected `evaluator_file`). The adapter supplies the selected endpoint, project,
token environment and exact installed client. The client builds/checks the request;
no automatic version refresh/retry. Typed and raw input cannot be mixed.

| Operation | Other fields |
| --- | --- |
| `import` | `--source-manifest FILE` (selected `source_manifest`) |
| `draft-open` | `--baseline ID --work-order WO-ID` |
| `create-artifact` | `--context UUID --context-version N --domain NAME --artifact-type TYPE`; optional `--artifact ID --include-document` |
| `revise-artifact` | `--context UUID --context-version N --artifact ID --expected-revision REVISION --document-file FILE` |

Creation allocates/writes at once: no `--dry-run` or local preview.
`--include-document` reads that revision, returning text or its decoded path.
UTF-8 documents need no manual base64 or copied client digest.

`--record` saves the command; its new `.evidence` directory holds exact requests,
responses and decoded documents. Reuse displayed `client_view` fields; inspect
outcomes/findings and required omissions. For uncertain effects after capture
failure, use `remote operation --key KEY --record ABSOLUTE_NEW_RECORD` with the
original key. A failure after sending can conceal a committed effect.

## Read one revision

```text
remote read --typed --compact --record ABSOLUTE_NEW_RECORD --artifact ID --expected-revision REVISION --context UUID --context-version N
```

For imports use `--baseline ID` instead of context fields. Select exact revisions
from inputs/results. Reads take no `--operation-key`, `--expected-project-version`
or `--evaluator-file`.

## Reads and discovery

| Need | Operation |
| --- | --- |
| Service readiness/components | `remote status --record ABSOLUTE_NEW_RECORD` |
| Local wheel metadata | `identity` |
| Captured calls/reads/failures | `observations --record ABSOLUTE_NEW_RECORD` |
| Complete released sections | `instructions --section "RESOURCE_ID#HEADING"`; repeat up to 12 |
| Unknown input location | `find-file BASENAME --under RELATIVE_DIRECTORY/` |
| Exact inventory entry | `lookup-file RELATIVE_NAME` |
| JSON | `read-json ABSOLUTE_FILE`; optional `--pointer '"/field"'`, `--keys`, or `--decode-base64` for a raw base64 field |
| Text | `read-text ABSOLUTE_FILE [ABSOLUTE_FILE ...]`; up to eight inventoried inputs, pinned task.md or work files; 64 KiB limit |
| Truncated text | `read-text ABSOLUTE_FILE --offset 0 --limit 4096`; one file, character offsets; follow next_offset until complete |

Use canonical instruction IDs, e.g. `docs/engineering/harness/DRAFT_DEFINITIONS.md#read-this-when`.
The legacy `released-resources/` prefix works. Entry conditions are included when
present; links are not followed. Read applicable prerequisites. Checklist and
repeated continuation selectors are in plugin `change/references/hosted-drafts.md`.

Inventory names omit `inputs/`, e.g. `source/src/greeting.py`. Lookup/digest is not
content. Use known paths; batch independent reads/sections and reuse unchanged
content. Locate unknown headings by reading the file once; do not guess them.
No full inventory is required.

Read [Execution tools](native-execution-tools.md) before planning/executing checks
for available assertions/evidence. Reading or planning grants no execution authority.

## Other operations

For raw requests, lifecycle rehearsal or handoff encoding, first read
[their command details](native-execution-tools.md#raw-requests-and-lifecycle-rehearsal).

## Report evidence

Run `observations --record ABSOLUTE_NEW_RECORD` before reporting: full snapshot
saved, bounded failures/pointers returned, no verdict. `observed_content_reads`
contains successful visible reads; `file_reads` includes failed Claude Read attempts.
Use the trace, not inventory lookups. Missing reads stay unknown; later reads
prove nothing about earlier reads. Capture may be incomplete and excludes later
report writes. Retain the record path instead of copying commands.

`record` is a JSON file even without an extension. Use `read_arguments` with the
approved prefix; optionally add `--pointer`, never append a filename.
`command_records` includes extensionless captures and exact available
`response_fields` (receipt/outcome/provenance), sorted by filename, not time.
Inspect original requests/results for claims; the index selects no handoff base
or retry. Apply hosted-drafts' report/content rules; memory proves no failure count.
