# Private lifecycle rehearsal wire contract

The v2 endpoint accepts only `lifecycle-v2.json`. Every request and result selects
test data. Git remains authoritative for real work. Existing v1 routes and the
seven read-only MCP tools keep their contract; they cannot dispatch v2 actions.
In an explicitly configured test project their results use
`se-harness-graph-read/v2`, with a required test-copy label. Ordinary Phase 2
projects retain their v1 read result shapes. Revision byte hashing is unchanged;
test revisions add explicit test-copy provenance, without rewriting v1 fixtures.

`inspect` accepts check, preflight and validate. `preview` runs a mutation in a
discarded projection and returns its input digest and complete proposed file
effects. `apply` requires that digest, reruns the released checks, and commits
the complete result once. A preview never changes graph state. Actor strings
are synthetic test inputs, not authenticated human consent.

The digest binds project/context versions, all selected revision IDs, retained
snapshot, exact command/file inputs, principal and released evaluator identity.
Mode and operation key are excluded from the preview binding, but included in
the accepted request digest used for principal-scoped retry lookup.

## Permitted file effects

| Action | Permitted effects in the disposable projection |
| --- | --- |
| check / preflight / validate | No file writes |
| transition | Only selected newly authored artifacts and evaluator sidecars declared by their records |
| decide | Selected new decision and its explicitly linked rehearsal risk |
| raise-risk | New risk and optional paired decision at released domain paths |
| handoff | Declared bounded file inputs within the selected work order's scope; released handoff packet and evaluator evidence |
| capture-verification | New VREC and its released evaluator sidecar |
| prepare-release | New RLS and its released evaluator sidecar |

Handoff first uses the released procedure's fixed `evidence` preparation command,
then `check --checkpoint handoff --from-git`. It exposes no arbitrary evidence
command. File inputs cannot alter formal records, harness selection/instructions,
Git configuration, hooks, or executables used by the service. The service never
runs source tests. The local qualification runner supplies observed test evidence.

The adapter enumerates every regular file before and after the operation. It
rejects deletions, links, unexpected paths, missing sidecars, imported-record
changes and evaluator failure before opening an acceptance transaction.

## Snapshots and Git

Each accepted operation retains an immutable complete snapshot: exact file bytes,
self-contained Git history and its source/test-candidate identities. Content
digests bind the snapshot to the resulting baseline. Context heads, artifact
revisions, snapshot and receipt share one database transaction. Temporary Git
repositories are discarded after the result is accepted or refused.

Capture first commits the exact input projection as test candidate P. P excludes
the new VREC. The output retains the input hosted baseline B, source fixture S,
P and evaluator identity. Actual implementation candidate C is recorded separately
by qualification. Subsequent commits never alter the candidate stored in a VREC.

Export selects an immutable baseline, checks its complete snapshot and Git bundle,
and returns exact bounded bytes. The installed client writes only to a new explicit
destination and leaves an incomplete marker until every file hash is checked.
No export writes to or synchronizes an authoritative repository.

## Bounds and failure categories

Keep 4 MiB requests, 2 MiB responses, 1 MiB individual file inputs, two concurrent
projections, 120-second evaluator calls and 10,000 retained artifact revisions.
A pilot snapshot/export that exceeds the response bound is refused atomically.
Retained complete snapshots have a separate explicit project count bound of 128.
This is a small private pilot, not an unbounded document store.

Boundary/malformed requests, stale inputs, evaluator refusals, invalid output and
unknown transport outcomes remain distinct. Read the operation receipt after a
lost reply. A changed request under the same accepted key is a conflict. The
service does not automatically rerun a mutation at a newer version.
