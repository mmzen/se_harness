+++
id = "SPEC-DST-014"
type = "specification"
title = "Verified progressive Explorer data access"
status = "approved"
owners = ["technical-owner", "security-owner", "quality-owner", "product-owner"]
created = "2026-08-17"
updated = "2026-09-01"

[relations]
specifies = ["REQ-DST-050", "REQ-DST-051", "REQ-DST-052", "REQ-DST-053"]
+++

# Specification: Verified progressive Explorer data access

## Scope and authority

Make the existing Overview, Lineage, and Readiness UI consume the static bundle from `SPEC-DST-013` progressively. Preserve the accepted visual structure, graph behavior, lane board, 20-visit navigation, rich details, safe Markdown/EARS presentation, relation semantics, readiness boundaries, and non-authoritative labels.

## Actors and external systems

The reader controls navigation and expansion. The browser fetches same-origin immutable static resources. GitHub Pages or an ordinary static HTTP server returns bytes only. No browser operation modifies artifacts, evidence, repository state, assurance, release, or publication state.

## Inputs

- bounded index bootstrap;
- manifest and descriptors defined by `SPEC-DST-013`;
- reader view, filter, selection, history, relation-navigation, and evidence-expansion actions;
- verified resource cache scoped to one manifest digest.

## Outputs

Incrementally rendered repository summary, topology, focused Lineage, artifact details, retained evidence, Readiness, loading/error/retry states, and bounded in-memory cache observations. No loaded or rendered value is persisted as formal authority.

## State model

Startup progresses `shell -> manifest-verifying -> summary-verifying -> summary-ready`. Overview/Lineage topology and Readiness independently progress `not_requested -> loading -> ready | failed`. Each artifact detail and evidence document follows the same resource state. Selection state is independent: `selected_id` changes synchronously from compact verified topology, while a generation token prevents older resource completion from replacing a newer selection.

## Behavioral rules

1. Refuse progressive startup under `file://` with a concise HTTP-serving instruction; do not attempt repository-path fallbacks.
2. Fetch the bootstrap-declared manifest from the same origin with no credential escalation, verify HTTP success, final origin/path expectation, exact bytes, and SHA-256 before JSON parsing.
3. Reject an unsupported schema, duplicate or malformed descriptor, revision mismatch, unsafe path, or resource outside the manifest. Do not partially trust a manifest.
4. Implement one `fetchVerified` boundary that fetches bytes, enforces declared size and bounded maximum, verifies SHA-256 with Web Crypto, then parses JSON or decodes passive UTF-8 according to the descriptor role.
5. Load and render summary immediately after manifest verification. Defer topology until Overview or Lineage needs it and defer readiness until Readiness is entered.
6. Deduplicate identical in-flight descriptor requests and cache only verified values by manifest digest plus resource digest. Do not use persistent storage or reuse across bundle revisions.
7. Populate graph filters, search, adjacency, Lineage cards, exact relation direction, labels, and history from compact verified topology. Do not require artifact bodies for those operations.
8. On artifact visit, set exact selected ID and history first, show a scoped detail-loading state, and request only its topology-declared artifact descriptor when absent from cache.
9. Render verified artifact details through the existing curated metadata, EARS tokenizer, and safe Markdown allowlist. A detail resource cannot redefine its topology identity; mismatch fails that detail.
10. Evidence metadata renders from the verified artifact detail. Evidence body is not requested by tab entry; the first explicit expansion fetches its declared passive content and renders only after integrity and sanitizer checks.
11. Use request cancellation where available and a monotonically increasing selection/view token in all cases. Stale completion may populate the matching cache but cannot alter the latest panel, focus, history cursor, or view.
12. Keep the Lineage view's in-memory visit history, its back and forward controls, and its visit chips consistent for loaded, loading, cached, and failed detail states; visits are navigation state and never lineage.
13. Contain failures to the affected startup stage, view, artifact, or evidence entry. Preserve unrelated verified data and provide a keyboard-operable retry that repeats full verification.
14. Update CSP/connect policy only as required for same-origin static data fetches. The page names and requests no remote origin (`SPEC-DST-023` rule 7).
15. Bound cache entries to the finite manifest resource set and clear all runtime state on page reload. No timer, analytics, telemetry, polling, repository mutation, or automatic publication is added.

## Error and recovery behavior

Distinguish unsupported transport, HTTP failure, redirect/origin failure, size mismatch, digest mismatch, schema/JSON/UTF-8 failure, missing artifact, stale response, and safe-render fallback without exposing unsafe payloads. Retry never bypasses validation. Summary failure prevents repository facts from rendering; later-resource failure leaves summary/navigation and other ready panels intact.

## Data and interface contracts

Compact nodes are navigation/index records, not complete artifacts. Artifact details must match their descriptor's ID and content digest. Evidence descriptors retain repository identity separately from generated digest paths. The UI may derive presentation state only after the same canonical semantics already approved for Explorer; it may not create formal relations or decisions.

## Security and privacy properties

Use same-origin relative fetches, no credentials beyond static-origin defaults, no executable JSON, no dynamic import, no `eval`, and no repository-derived URL construction. Hash verification occurs before parsing or rendering. Preserve safe Markdown, EARS exact-text, external-link, active-content, disclosure, and failure-fallback rules from `SPEC-DST-012`.

## Performance and capacity

Initial HTML plus summary stays within `REQ-DST-055`; topology and readiness load at most once per manifest; one uncached artifact request follows one new selection; one uncached evidence request follows explicit expansion. Render loading state without blocking the main thread on deferred Markdown. Cache is bounded by manifest entries and naturally by the 20-entry navigation pattern, while shared evidence digests avoid duplicate bytes.

## Observability

The snapshot-information panel reports bundle schema, short and full observed revision, manifest digest, loaded resource classes, verified/failed resource counts, and total verified bytes as factual session observations. Browser console output must not include complete repository content or claim assurance.

## Compatibility and migration

Preserve all current views and interactions; only acquisition timing and loading/error presentation change. Older generated v1 pages keep their embedded runtime. New pages require HTTP serving. Document a Python-standard-library local serving command and progressive loading in the dashboard/publication notes. No new Python runtime dependency or browser CDN is expected.

## Examples and counterexamples

- Valid: opening Overview renders metrics, then asynchronously renders topology.
- Valid: Back selects a cached artifact instantly while a never-visited artifact shows a loading state.
- Valid: evidence metadata is visible and content remains unfetched until expansion.
- Invalid: selecting any artifact downloads all artifact shards.
- Invalid: a failed evidence digest empties Lineage or marks the repository invalid.
- Invalid: an earlier slow response replaces the latest selected artifact.

## Explicitly unspecified decisions

The implementation agent may choose loading indicators, retry wording, cache helper structure, prefetch none or the single current artifact after topology, and whether Overview topology begins immediately after summary or on the next rendering opportunity. It may not prefetch every detail/evidence resource, change history semantics, persist content, add a service worker, or weaken verification.

## Amendment record

**Rules 12 and 14 follow the designed page, proposed 2026-09-01 under `WO-DST-023`
(`SPEC-DST-023`).** The previous page's 20-entry sliding window and its
optional CDN exception belonged to a presentation this repository no longer
ships; the verified progressive access this specification defines is
unchanged and the designed shell implements it (`SPEC-DST-023` rules 8-10).
