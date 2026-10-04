# Hosted artifact graph: Phase 1 implementation contract

This guide makes the approved SPEC-HAG-001/002/003 concrete for implementation.
It does not change those definitions or claim an operating service. The wire
shapes and fixed vectors are ready for inspection; the released-evaluator
admission dependency is open in DEC-HAG-001. Phase 2 qualification has not run.

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
projection. DEC-HAG-001 must resolve standalone draft admission before this route
is implemented. Protected lifecycle/provenance/evidence fields remain protected.

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
