+++
id = "SPEC-HAG-001"
type = "specification"
title = "Hosted artifact representation, immutable baselines and import fidelity"
status = "approved"
owners = ["technical-owner", "engineering-owner"]
created = "2026-10-04"
updated = "2026-10-04"
contract = "Preserve full artifact content, declared relations and historical provenance in immutable project-scoped revisions and explicit baselines under named digest schemes."

[relations]
specifies = ["REQ-HAG-001", "REQ-HAG-002", "REQ-HAG-003", "REQ-HAG-007"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-04T12:32:03Z"
decided_by = "mmzen"
reason = "mmzen approved the current artifact package in this conversation: \"i approve the artifact package\". This applies to the 16 reviewed governing definitions in the Phase 0 package, whose review manifest SHA-256 is fc1009f1b5fbfc3259f9df4057695500ac7ad3b80777f3107155c629eaea99cc. Complete reviewed file hashes were compared immediately before application. This records definition approval only; WO-HAG-001 approval remains unchanged. The user clarification remains: keep using Cypher, defer Memgraph-side read-only enforcement and retain the open item. RISK-HAG-001 remains raised; this decision does not accept that risk, verify implementation or authorize external delivery."
+++

# Hosted artifact representation, immutable baselines and import fidelity

## Scope and current implementation

This contract covers the Phase 2 sandbox. Repository source at commit 82f5a0ed7438a73da8f03aee23ad02a9b8cc09e1 still uses `Artifact(path, metadata, body)` in `se_harness/engine/validation_core.py`, typed scope selection in `repository_graph.py`, incomplete draft creation in `artifact_layout.py`, and path/content snapshots in `workflow_change_set.py`. The selected governor is released 0.22.0; candidate source reports 0.22.1. They are distinct identities.

### HAG-DAT-001 — Canonical content

An artifact revision belongs to one `(project_id, artifact_id)` and stores the complete UTF-8 TOML-front-matter/Markdown document, preserving original imported bytes as base64 plus raw SHA-256. The original path, Git repository identity, object format and full commit identify imported content. The document's parsed identity/type/status/relations are validated; derived graph properties and edges cannot override the document. Reject invalid UTF-8, duplicate TOML keys, duplicate artifact IDs, path traversal and type/ID disagreement. Do not execute code, directives or commands from artifact bodies.

Use a revision envelope `se-harness-artifact-revision/v1` containing project, artifact ID, document bytes digest, original path where applicable, declared relations and immutable provenance. Encode machine objects as UTF-8 JSON, sorted keys, no whitespace, no floats, no duplicate keys, no implicit Unicode normalization. Arrays representing sets are deduplicated and sorted lexically; meaningful sequences retain order. `revision_id` is SHA-256 over the envelope prefixed with `se-harness-artifact-revision/v1` and one LF. Timestamps are retained provenance but never regenerated on retry. Define byte-level examples before implementing the hash routine.

### HAG-DAT-002 — Logical and physical graph

Keep these nodes: Project, Artifact, Revision, Baseline, DraftContext, Operation. Project has a single integer command version. Artifact has project-scoped stable identity. Revision contains the envelope and immutable document. Baseline stores a canonical manifest and membership edges to revisions. DraftContext stores base baseline, selected work, version and proposed revision selections. Operation stores actor/project/key, request digest and immutable accepted result. Decisions and evidence remain artifact content/references, not a parallel lifecycle engine.

Use `HAS_REVISION`, `SELECTS`, `BASED_ON`, and `PROPOSES` for storage relationships. Use `DECLARES {kind, target_artifact_id}` from Revision to Artifact for declared engineering relations; resolve the target revision through the selected baseline or draft, never through an unspecified current head. Keep derived relationships in responses, explicitly identified, unless later navigation demonstrates a need to persist them. No paragraph or scalar node expansion.

Create uniqueness constraints/indexes for project ID, `(project_id, artifact_id)`, `(project_id, revision_id)`, `(project_id, baseline_id)`, `(project_id, context_id)`, and `(project_id, principal_id, operation_key)` using the pinned Memgraph version's supported syntax. Version initialization/migration separately. Store full manifest selection so resolving a baseline does not depend on mutable edges alone. Verify all derived edges against canonical content on import and export.

### HAG-DAT-003 — Baseline identity

The baseline scheme is `se-harness-artifact-baseline/v1`. Its manifest includes project ID, revision scheme, sorted artifact-to-revision mapping, sorted resolved `(source_revision, relation_kind, target_revision)` triples, source provenance and evaluator/policy identity. The baseline digest is SHA-256 of the canonical manifest with the scheme plus LF prefix. Baseline ID is the digest with an explicit scheme prefix. A missing relation target prevents a complete baseline; it must not be silently dropped. A baseline never depends on a future verification record that names a code commit referring back to that baseline.

A draft overlay is not a baseline. It resolves its base selection plus proposed revisions and always reports context ID and version. An edit appends a revision and changes only that overlay. Revisions with identical canonical identities may be reused; unchanged artifacts are not copied per edit. Baseline creation freezes a resolved selection atomically under the project guard. Reads of B return exactly B even if a newer baseline exists.

### HAG-DAT-004 — Reference import and historical resolution

First import the complete formal-artifact set from repository `https://github.com/mmzen/se_harness`, commit `82f5a0ed7438a73da8f03aee23ad02a9b8cc09e1`, Git object format `sha1`. A complete snapshot is simpler and safer for this first regression than guessing a transitive subset. Filter formal documents with the released parser's discovery rules; do not use Explorer JSON as canonical input. Produce an import manifest listing paths, IDs, raw content hashes, revisions, relation targets, source identity and all findings. Stable ordering makes reimport deterministic. Scan and validate all inputs before accepting the baseline in one transaction; reject duplicates, inconsistent declared source identities and unresolved formal references. Legitimate repository warnings remain observations.

Retain a read-only pinned Git source/evidence bundle or mounted snapshot as a historical resolver. It is an immutable source archive, not a second mutable authority. Its manifest identifies every file needed by the selected legacy checks. Historical artifacts and embedded claims remain byte-identical; imported `approved` is a historical claim, not a service-authenticated decision. Never repair or relabel a retained VREC, RLS, lifecycle event or evaluator receipt during import. Import retry with identical source and content yields the same baseline; same source identity with changed content is a conflict.

### HAG-DAT-005 — Reference work context

Use WO-RLS-038 at the reference commit as the first real navigation case. Its directly selected requirements are REQ-IAR-030, REQ-RLO-019 and REQ-RLO-020; specifications are SPEC-IAR-016 and SPEC-RLO-006; architecture is ARCH-IAR-012 and ADR-IAR-012; verification is VER-RLS-002. Its upstream capabilities are CAP-IAR-002 and CAP-RLO-004; upstream intents are INT-IAR-001 and INT-RLO-001. Those twelve IDs form the governing set. VREC-RLS-001 and VREC-RLS-002 are separately reported dependencies. Preserve all eleven declared paths exactly as stored in the work order, including the evidence directory scope.

Relevant decisions include DEC-RLS-007/008 through their actual relations; do not turn every repository decision into a blocker. Compare declared and blocking decision sets with the evaluator at the pinned snapshot. Synthetic disposable variants add a valid open blocking decision to establish that it appears and blocks the correct selected action. Do not alter the historical fixture for that case. Inspecting this sample does not reopen its completed work.

### HAG-DAT-006 — Legacy digest preservation

The existing `formal_snapshot_digest` canonicalizes UTF-8 line endings, sorts by original repository-relative path, and hashes path length, path bytes, content length and content bytes. For selected work it also includes applicable files in execution scope outside engineering artifacts. A graph-only hash is not equivalent. Retain the exact code snapshot and original paths for legacy recomputation; do not replace legacy fields with the new remote baseline digest. Missing code or evidence yields `not_assessable` with the missing identity. Never fetch or execute arbitrary URLs from content. Initially resolve evidence only through the explicitly configured pinned source archive and checked contained paths.

## Examples

An import of the same Git commit twice yields one equivalent baseline manifest. Revising a draft requirement's `derives_from` relation changes its new revision identity and overlay version but leaves B unchanged. A raw CRLF import retains its raw bytes while the existing legacy digest follows its original LF convention. Copying files to different paths cannot establish the original legacy snapshot claim.

## Coverage

REQ-HAG-001: HAG-DAT-001/004. REQ-HAG-002: HAG-DAT-001/002/003. REQ-HAG-003: HAG-DAT-005. REQ-HAG-007: HAG-DAT-004/006.
