# Hosted artifact graph: sandbox protocol and implementation

This guide explains the approved SPEC-HAG-001/002/003 protocol. The private
service and candidate remote client are implemented under WO-HAG-001. Development
integration tests have run; final qualification of all twelve scenarios remains
pending. Use [the operating procedure](../../server/README.md) to build and test
the exact combination. Git remains authoritative. This is not a public service.

DEC-HAG-001 is decided. The bounded revision in DEC-HAG-002 selects public
evaluator 0.22.1 for this sandbox; candidate client 0.22.2 is separate.

## Project and source identities

The explicit operator initialization command allocates a UUIDv4 `project_id`
once and stores it on Project with `command_version = 0` and `schema_revision = 1`.
An operator may supply a fixed UUID for a reproducible disposable test. Repeating
initialization confirms the same identity; it cannot silently replace a store.
The readable name `hosted-artifact-poc` is a display name, outside revision hashes.
Clients obtain the UUID from initialization output or authenticated status.
Requests never allocate projects and never take a principal identity on trust.

The reference source is `https://github.com/mmzen/se_harness`, Git SHA-1 commit
`82f5a0ed7438a73da8f03aee23ad02a9b8cc09e1`. The source manifest lists every formal
artifact path, ID, blob OID, byte length and raw SHA-256. Generate it from Git
blobs using the released discovery list, not Explorer output or a worktree read.
On Windows, `git archive` needs `-c core.autocrlf=false`: archive defaults can
convert LF to CRLF even when the blob is LF. Compare each exported artifact with
`git cat-file` bytes. Preserve original bytes, including CRLF when present in Git.

The operator mounts the pinned source/evidence snapshot read-only. Import requests
identify this configured source; they cannot make the server fetch URLs or read
arbitrary host paths. Check every manifest entry against its mounted bytes, then
use the released parser for the canonical artifact set. Missing, duplicate,
extra or conflicting entries prevent complete import. Supporting code/evidence
belongs to the immutable historical resolver, outside the 64 MiB artifact limit.

## Revision and baseline bytes

`server/contracts/remote-v1.json` names the exact fields. A StoredRevision contains
`revision_id`, `envelope` and `document_base64`. The envelope binds the full raw
document SHA-256; the store verifies it against decoded bytes. Imported provenance
contains the original repository/object format/commit and Git blob OID. Draft
provenance records the authenticated principal, operation key and server-assigned
creation time once. An accepted retry returns the retained bytes and time.

Canonical JSON uses UTF-8 without BOM, sorted object keys, compact separators,
literal Unicode, no Unicode normalization and no floats. Reject duplicate object
keys and non-finite numbers before decoding into a map. Semantic sets are sorted
and deduplicated before encoding: relation targets, artifact selection keys and
resolved relation triples. Preserve meaningful sequence order. Raw document
bytes receive no line-ending or Unicode conversion for the new revision scheme.

The revision hash input is `se-harness-artifact-revision/v1`, LF, then canonical
envelope bytes. `revision_id` is `sha256:` plus the lowercase hex digest. The
baseline hash input uses `se-harness-artifact-baseline/v1`, LF and the canonical
manifest; its identifier is that scheme plus `:sha256:` and the hex digest.
Neither hash payload includes its own derived ID or a future verification record.
The baseline manifest binds sorted selection, resolved revision-to-revision
triples, provenance and the exact evaluator identity. A missing relation target
prevents a complete baseline. Saved incomplete drafts remain distinct from
complete frozen selections and from approved definitions.

The fixture file `canonical-v1.json` supplies exact JSON strings and hash-input
bytes for three connected draft artifacts, LF/CRLF, composed/decomposed Unicode,
a body edit, sequence order and a baseline. These are synthetic byte examples,
not claimed receipts. Its all-zero parent baseline is an explicit fixture marker.
Future serializer tests must consume these fixed expectations; do not regenerate
expected hashes from serializer output.

## Command-specific fields

Every mutation carries the project ID, operation key, expected project version,
exact evaluator archive/payload identity, and candidate client version/wheel hash.
The server checks compatibility against the qualified tuple before mutation.
The authenticated principal comes from credentials; claimed component identity
does not grant authority. Reject unknown fields and contradictory selectors.

| Operation | Required selection and content | Accepted effect |
| --- | --- | --- |
| `import` | Complete configured source manifest; no baseline/context selector | Original immutable revisions and imported baseline, deterministic report, receipt, one project-version increment |
| `draft-open` | Base baseline ID and selected work-order ID | New UUID context at version 0; unchanged base; receipt and project-version increment |
| `create-artifact` | Context ID/version, domain, supported type; ID or explicit null for allocation | New draft revision and proposed selection; context and project versions increment once |
| `revise-artifact` | Context ID/version, artifact ID, expected selected revision, complete base64 document | New draft revision and derived relations; replace only that context selection; increment both versions |
| `freeze` | Context ID/version | New immutable baseline from the resolved complete view; project version increments; context stays open with its original base and version |

An empty project has no baseline to select. Import therefore has no view selector.
Operation lookup is `GET /v1/projects/{project}/operations/{key}` and is scoped to
the authenticated principal. It requires neither a baseline nor a current version.
Readiness also has no view selector. These are the applicable-field interpretations
of HAG-API-001/002, not changes to the named protocol schemes.

The draft view is its base plus explicit proposals. New IDs are reserved across
all retained project artifacts, not just the selected baseline. The command adapter
uses the released authoring template and allocation behavior in a disposable
projection. The isolated public 0.22.1 evaluator supplies standalone draft
admission. Protected lifecycle/provenance/evidence fields remain protected.

Freeze does not rebase, close, clear or otherwise change its context. Editing that
context later creates another proposed revision. Opening a fresh context from
the frozen baseline explicitly selects a new base. Repeating an already accepted
operation key returns its original receipt even if live versions have advanced.
A different request under the same principal/project/key returns conflict.

## Atomic acceptance and reads

Bind evaluation to project version N and the exact context/revision selection.
In a short explicit database transaction, conditionally change the same Project
guard from N to N+1 and recheck context/revision guards. Commit the new content,
derived edges, selection changes and accepted receipt in that transaction. A
competing guard update or constraint conflict refuses; a process mutex is not
the transaction boundary. Do not retry against newer input without caller action.

Imported content and repeated source identity cannot disagree. Reimporting the
same complete source may return the already present immutable baseline; it must
not duplicate revisions or change the stable import report. A new operation key
still has its own guarded command/receipt; retrying the original key has no new
effect. A refusal creates no accepted receipt.

Domain reads select either an immutable baseline or an explicit context/version.
Exact revision, work context, comparison, impact, verification lineage and check
all return selection identity, provenance, evaluator identity and completeness.
Comparison explicitly names both views. Check is read-only and checkpoint-free;
it reports released findings and cannot apply a lifecycle transition. Operation
lookup returns the recorded receipt, not a recomputed result at the latest view.
Unsupported live-view forms are refused until their semantics are qualified.

Domain and MCP reads share handlers. Context completeness requires all selected
governing artifacts and declared paths; truncated results cannot establish a
governing claim. The pinned reference fixture has 12 governing IDs and 11 paths
for WO-RLS-038; VREC dependencies remain separately classified.

## Validation at each stage

| Stage | Required assessment | Meaning of success |
| --- | --- | --- |
| Decode | Strict UTF-8, unique JSON keys, integer-only request numbers, closed wire shape, contained source paths and configured source identity | A request can be evaluated; no authority or mutation follows from decoding |
| Import | Complete Git manifest, raw byte/provenance equality, released parsing and relation validation, all referenced targets resolved | A faithful historical baseline; imported lifecycle claims acquire no new decision event |
| Draft creation/revision | Released standalone draft classification, server rights, protected-field comparison and exact input selection | A saved draft may retain the evaluator's narrow permitted incompleteness; malformed content or supplied invalid relations refuse |
| Freeze | Complete selection, resolvable declared edges, canonical manifest and version guards | An immutable baseline of that selection; draft members remain drafts |
| Context/read/check | Explicit view, exact released context/findings, original-path historical resolver and honest resource limits | A bounded observation; `complete` does not mean approved or gate-passing |
| Approval/verification/release | Unsupported in this sandbox | No remote command can confer a human decision or produce a verified/released record |

The draft stage uses the selected public 0.22.1 evaluator. Its archive and payload
are fixed by SPEC-HAG-003. Earlier Phase 1 reports retain their original 0.22.0
observations and unresolved-dependency status as historical evidence.

## Read request and response details

`server/contracts/read-v1.json` defines the seven POST request variants and their
response shapes. HTTP path operation/project and body values must agree. MCP
uses the same normalized request and authenticated handler. A context selector
requires its exact version. If that version has changed, refuse with 409; no
implicit latest view or historical context reconstruction is promised. Freeze a
selection when later reads need an immutable identity. A compare request names
two views in the same project.

| Read | Selection and returned data |
| --- | --- |
| `revision` | Artifact ID and revision ID must match the selected view. Return the complete StoredRevision, including raw bytes; a known revision outside that view is an unknown selected identity |
| `work-context` | Selected work order, governing bindings, exact declared paths, dependencies and relevant decisions in separate fields; embed the unchanged checkpoint-free evaluator result |
| `compare` | Added/removed/changed artifact bindings plus added/removed resolved relation triples; a missing side of a binding is null |
| `impact` | The root and reverse reachability through known declared relations at the selected view, within depth; exclude the root from the returned artifact list |
| `lineage` | The root and connected declared verification/evidence relations, with endpoint revisions; this reports recorded links and claims, not new assurance |
| `check` | Only a WO, VREC, RLS or DEC accepted by the selected released checkpoint-free `check`; return its JSON unchanged with the selected binding |
| `cypher` | Columns and rows from the admitted query, bound to the selected view; column names and row widths agree and graph values expose only the documented public properties |

Sort domain bindings by artifact ID, paths lexically, and edges by
`(source.artifact_id, kind, target.artifact_id)`. Preserve evaluator output and
Cypher row order. A read's `provenance` names the unique Git sources of its selected
inputs; synthetic draft-only examples may have none. Draft provenance is retained
in each revision envelope. Resolve every returned revision through the view.
For comparison, resolve each side independently. These equality and resolution
checks require the service; JSON Schema checks only their shapes.

`complete=true` means that this response contains the whole requested answer at
the stated view and no unresolved references. It can still contain draft hints,
open decisions, failed gates or a missing historical binding in the unchanged
evaluator result. When missing bindings prevent the requested assessment, report
`complete=false` with `binding_unavailable` and identify the exact missing input
in evaluator output. Do not convert `not_assessable` into a pass.

Budgets apply to the aggregate graph rows across all returned collections, not
500 rows per nested array. Paths and unresolved-reference entries also consume
that allowance. The byte budget includes the entire serialized response and
embedded evaluator output; never truncate that JSON. Traversal stops must be
visible even if the last returned node has no displayed outgoing edge. A bounded
partial response uses `complete=false`, the specific limit and concrete
instructions to repeat at the same view with a narrower selection. That strategy
does not turn a partial work context into a governing claim. If the operation
has no meaningful narrower selection, repeat with a larger budget within the
fixed limits; if the minimum honest response cannot fit, refuse with 429.
Unresolved graph targets require a new complete view, not silent continuation at
an altered context version. No pagination cursor or server-side read session is
introduced in this initial contract.

The baseline GET retrieves one canonical manifest resource, not a row query:
`{schema: "se-harness-artifact-baseline/v1", baseline_id, manifest}`. Validate the
manifest with `BaselineManifest`, recompute its identity, and return the full
selection and resolved relations. The 2 MiB response limit still applies; reject
an import/freeze whose complete baseline response cannot fit before committing.
Do not clip the manifest to the graph-query row budget or label a fragment as B.
Operation GET returns exactly the stored accepted `remote-result/v1` object for
the authenticated principal/project/key. Status GET reports project UUID, schema
revision, readiness, actual evaluator and component identities, and the supported
protocols. Missing built/qualified identities keep readiness false. Neither GET
requires a context selector; operation lookup never guesses an acceptance.

## Accepted receipts, refusals and retry order

`server/contracts/result-v1.json` defines immutable accepted receipts and stable
remote refusal codes. Every successful mutation returns HTTP 200 and one UUIDv4
`receipt_id`. Store that entire result with the operation. Bind `request_digest`
to SHA-256 of `se-harness-remote-command/v1`, one LF, and canonical JSON of the
complete validated command. Canonicalize manifest entries as their declared set
before hashing; retain original document bytes and all expected versions. Reject
duplicate manifest entries before normalization. Credentials, connection metadata
and transport timestamps are outside the command and digest.

An accepted result's project `after` equals `before + 1`. For context open,
context `before` is null and `after` is zero. Create/revise increments the context
once; freeze reports equal context versions. Import has a null context version
record. The returned view names the imported/frozen baseline or resulting context;
affected revision IDs are sorted unique IDs created by this operation, so an
identical-source reimport may report none. Receipt IDs are correlation identities,
not substitutes for revision or baseline hashes.
`affected_artifacts` supplies the corresponding artifact/revision bindings, so
creation with automatic ID allocation returns the allocated artifact ID directly.
Its revision set must equal `affected_revision_ids`; a refusal returns both empty.

Apply checks in this order:

1. Authenticate and enforce project/operation access, then perform bounded strict
   decoding and shape checks. Reject unknown fields such as caller-supplied actor.
2. For a valid command, compute its request digest and inspect the accepted key.
   Equal digest returns the original result immediately, even after versions or
   the configured tuple change. Different digest returns key-reuse conflict.
   Current project access remains required; never evaluate a retry as a new write.
3. For a new key, check the supported tuple, known selections, then project,
   context and selected-revision guards in that order. Refuse the first mismatch.
4. Check source/protected input and invoke the released evaluator against the
   bound selection. Invalid draft/import, incomplete freeze and unavailable
   mandatory bindings have distinct 422 codes. Resource refusal is 429.
5. Recheck guards and selection in the write transaction, write all effects and
   receipt, then commit. On a concurrent equal-key conflict, read the winner's
   committed receipt. Never update a stale request's expectations automatically.

Malformed input uses 400, unauthenticated 401, forbidden 403, unknown accessible
identity 404, stale/key/source/tuple conflict 409, invalid content 422 and resource
refusal 429. The schema enumerates the `HAG_REMOTE_*` codes. These codes wrap the
remote operation; existing evaluator codes and JSON remain unchanged. Refusals
have no receipt and no affected revisions. Populate correlation/view/versions
only when known and authorized; otherwise use null. When versions are returned
on refusal, before equals after. Read refusals use null command correlation and
versions. Denial must not leak another project's identities or findings.

The schemas describe the selected evaluator profile as well as wire shapes.
Their pinned evaluator constants are compatibility checks: a well-formed but
different version/archive/payload is 409, not malformed JSON. Keep those checks
separate from primitive shape decoding and accepted-key recovery. Strictly
decode base64 and require its canonical encoding before digest calculation;
invalid base64 is malformed input, while invalid decoded TOML is invalid draft
content. A successful shape check alone never supplies an admission decision.

A lost response, evaluator process crash or ambiguous database commit is not an
accepted or refused receipt. The client reports transport uncertainty and uses
operation lookup or an identical retry. A 404 lookup alone cannot prove that a
concurrent transaction rolled back. A known precommit failure leaves no effects;
an unknown commit must be reconciled against the authoritative operation store.

## Scenario and schema qualification

`tests/hosted_artifact_graph/fixtures/scenarios-v1.json` maps all twelve
VER-HAG-001 cases to explicit positive/failure outcomes and storage support. Every
hosted execution entry is `unperformed`. Its wire examples contain synthetic
identities and demonstrate shape only; their apparent receipt values are not
observed acceptances. The original fixed canonical vectors remain unchanged.

For independent shape qualification, install `jsonschema==4.26.0` in a disposable
environment and run its Python against:

```text
python -I -B tests/hosted_artifact_graph/validate_wire_contracts.py
python -m unittest tests.test_hosted_artifact_graph
```

The first command registers the three local schemas without network resolution,
validates fixed vectors and the complete source manifest, and exercises accepted
and rejected shapes. It does not introduce a core runtime dependency. The second
command checks fixed bytes and digests through the existing test entry point.
Neither command executes service admission, transactions, Cypher or recovery.

## Physical representation

Project stores identity, schema revision and the integer command guard. Artifact
stores project-scoped identity. Revision stores its canonical `envelope_json`,
`document_base64`, artifact ID, raw document digest and derived type/status.
Baseline stores `manifest_json`; its SELECTS edges are derived from that manifest.
DraftContext stores base baseline, selected work order, version and proposals.
Operation stores project/principal/key, semantic request digest and immutable
`result_json`. JSON text properties retain exact machine structures without
expanding scalar fields into graph nodes.

HAS_REVISION links Artifact to Revision. SELECTS links Baseline to Revision.
BASED_ON links DraftContext to Baseline. PROPOSES links DraftContext to Revision
with the selected artifact ID. DECLARES links Revision to the target Artifact,
with `kind` and `target_artifact_id`; resolve the target revision through the view.
Cross-project edges, duplicate selections, and edges inconsistent with canonical
content fail import/export checks. Unresolved authoring placeholders remain
explicit findings and cannot become invented valid target nodes.

The public Cypher surface uses the selected project's Artifact and Revision
nodes, its selected Baseline (or context/base), and the corresponding storage
edges above. Project exposes only project ID, schema revision and the observed
command version. Artifact exposes project/artifact IDs. Revision exposes its IDs,
type, status, document digest, envelope JSON and document base64. Baseline exposes
its IDs and manifest JSON. DraftContext exposes its IDs, selected work order,
base baseline and context version. DECLARES exposes kind and target artifact ID;
PROPOSES exposes the selected artifact ID. Other edge properties are not public.

Operation nodes and their result JSON are private to command handling and the
principal-scoped operation lookup. They are not available through Cypher. A
query cannot use internal labels/properties, an unselected revision, another
baseline/context, or caller-authored project filters to widen this surface. The
service must apply that projection before query execution and use the same
read-only transaction snapshot for selection and results. This is application
admission; it does not resolve RISK-HAG-001 or prove database privileges.

`graph-v1.cypher` supplies six composite/single uniqueness keys, key/content
existence constraints and explicit lookup indexes. Memgraph requires separate
indexes for uniqueness constraints ([official constraint documentation](https://memgraph.com/docs/fundamentals/constraints)).
Schema creation must be an explicit operator step on an empty store; later
startup verifies it and refuses mismatch. Runtime schema qualification is pending.

## Deferred boundary and remaining qualification

Cypher remains part of the sandbox: parse a narrow read grammar, constrain the
selected view, apply row/byte/depth/time limits and roll back the read transaction.
Database-enforced read-only access remains RISK-HAG-001; no authoritative-pilot or
public-service claim is made. The current contract does not authorize a parser
bypass, a replacement lifecycle policy or suppression of malformed input.

The first service still needs a dependency lock, image/Compose files, admission
adapter, transaction implementation, packaged client/plugin changes and all
VER-HAG-001 cases. Phase 1 fixture checks do not satisfy the twelve-step sandbox,
concurrency, restart/restore, actual package or release-delivery obligations.
