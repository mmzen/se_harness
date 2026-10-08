## Explicit hosted sandbox

For an explicitly selected hosted sandbox, first follow [Hosted selection](../../setup/references/hosted-context.md).
Use its separate candidate client, exact project and baseline or context/version.
Do not run the repository-orientation helper against an endpoint.

Create a transient request outside the checkout. Use the selected service's v1
read schema or its MCP tool schema, including `operation`, `project_id`, `view`
and a budget within 500 rows, 2 MiB and depth eight. Domain reads are `revision`,
`work-context`, `compare`, `impact`, `lineage` and `check`; `cypher` is constrained
exploration with parameters. MCP exposes these same reads, not mutations.

Before a Cypher query, read the selected product's
`docs/notes/hosted-artifact-graph.md#physical-representation` and
`server/contracts/lifecycle-v2.md#bounded-cypher-reads`. They define the public
labels/properties and show the supported query form. Require these references in
the staged input set; do not guess labels from the JSON field names or assume the
full database query language is exposed.

```text
CLIENT_PYTHON -I -m se_harness remote read --endpoint ENDPOINT --project PROJECT --token-env TOKEN_VARIABLE --request ABSOLUTE_REQUEST_JSON --json
```

Read `complete`, unresolved references and any continuation before reporting a
governing context. A partial response cannot support that claim.
If the host saves or truncates a response, inspect the returned file through an
available, permitted read tool. A saved-file notice or successful tool call does
not establish completeness. For large JSON, extract the result metadata without
loading the whole graph into the conversation. If the response cannot be read,
report its completeness as unassessed; do not report unseen content or use it to
support a governing claim.

Retain the view,
revision and evaluator identities and report the embedded released result unchanged.
An accepted read is not an approval. Database-side read-only enforcement remains
unverified under RISK-HAG-001; use only the private public-data sandbox.


### Read one hosted revision

Use the exact `view`, artifact ID and revision ID returned by the selected
operation. Typed CLI read takes `--artifact ID --expected-revision REVISION`
and either `--baseline ID` or `--context ID --context-version N`. Add `--typed
--compact --record-directory NEW_DIRECTORY` to retain the exact response and
decoded document. Read the returned text, or its local path when large.
Inspect completeness, continuation, view and revision identity before authoring.
The client checks decoded bytes against the envelope's document digest.

Raw `remote read --request FILE` and the read-only revision MCP tool remain
available. Their v1 schema is the `revision` branch of `$defs.Request` in
`server/contracts/read-v1.json`, with RequestFields, View and Budget. The raw
response contains `data.document_base64`; decode as base64/UTF-8 without newline
conversion and compare SHA-256 with `data.envelope.document_sha256` before use.
`--key` belongs only to receipt lookup (`remote operation`), not document reads.
Stop incomplete, mismatched or unreadable results; return to the drafting step.

## Reading a hosted test copy

The seven existing MCP tools remain read-only. In the explicit lifecycle pilot,
their result schema is `se-harness-graph-read/v2` and every result is labeled test
data. Read its selected view and evaluator output; report any incomplete context.
A synthetic actor label, test `verified` state or test `released` state establishes
no real human decision. Git remains authoritative for the actual repository.
