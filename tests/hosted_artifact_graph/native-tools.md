# Native test tool index

Read `selection.json` for the exact `approved_shell_argv_prefix`, project and
paths. Append one operation below to that prefix per shell call. Use native
Read/Write/Edit for files. Output directories already exist. Direct client
commands, directory listing, wrappers and permission changes are not permitted.
This index lists capabilities; the agent selects the workflow from its task and
the applicable released instructions.

| Need | Helper operation |
| --- | --- |
| Candidate wheel identity | `identity` returns metadata and SHA-256 only. |
| One known input path and digest | `lookup-file RELATIVE_NAME` |
| Locate a filename | `find-file BASENAME` with optional `--under DIRECTORY/`; the trailing slash is required. No wildcards. |
| Inspect saved JSON | `read-json ABSOLUTE_FILE --pointer '"/field"'`; `--keys` lists names only. Omit the pointer for the root. |
| Read a base64 document field | Add `--decode-base64` to that exact field read; inspect its text and digest. |
| Encode authored document bytes | `encode-file ABSOLUTE_DOCUMENT`; not for wheel identity. |
| Service identity/readiness | `remote status --record ABSOLUTE_NEW_RECORD`; no request file. Status reports `project_version`. |
| One selected remote operation | `remote OPERATION --request ABSOLUTE_REQUEST --record ABSOLUTE_NEW_RECORD` |
| Mutation receipt | `remote operation --key KEY --record ABSOLUTE_NEW_RECORD` |

All draft/request/result paths belong under the selected output directory.
Read each actual result and its omitted fields as needed. `--record` retains
complete output; the displayed `result_fields` are bounded exact values, not an
independent verdict. `remote read` needs a request; `--key` cannot read a document.

## Request discovery

After selecting an operation, read its one schema view under `inputs/schemas/`.
Each view cites its original schema, pointer and digest. No values are supplied.

| Family | Available operation names |
| --- | --- |
| `remote-v1` | `import`, `draft-open`, `create-artifact`, `revise-artifact`, `freeze` |
| `read-v1` | `revision`, `work-context`, `compare`, `impact`, `lineage`, `check`, `cypher` |

The relative view name is `schemas/FAMILY/OPERATION.json`. Read operations use
the CLI's `remote read`. The original schemas remain under
`reference/server/contracts/`. `status` and receipt lookup have no request schema.
Captured CLI help is `inputs/client-help/OPERATION.txt` for `read`, `operation`,
`create-artifact` and `revise-artifact`. Other helper syntax is available with
`--help`; do not guess options. Lifecycle schemas are separate and unnecessary
for a drafting-only task.

Input names for lookup are relative to `inputs/`: `plugin/verity-plane/skills/`,
`released-resources/` and `source/`. Read only the required sections after lookup.
A digest or file search is not a content read. To report a digest, cite its exact
lookup/inventory entry or copy that entry's own value. Keep complete inputs and
failures as evidence without loading their entire inventory into context.
