# Verification evidence for WO-DST-015

## Authority and scope

This coordinated evidence uses the same 2026-08-17 owner authorization as `WO-DST-014`. It covers browser acquisition and presentation behavior only and grants no assurance or publication authority.

## Browser loading and integrity behavior

- Startup parses only the bounded bootstrap, revalidates the same-origin manifest, verifies its byte count and SHA-256, then verifies and renders the summary before acquiring view data.
- Overview begins compact topology after the first rendering opportunity. Readiness is fetched only on Readiness entry. Artifact detail is fetched only when Lineage focuses that artifact, and evidence text only when its disclosure control is expanded.
- Every response rejects redirects and cross-origin final URLs, verifies exact bytes and SHA-256 with Web Crypto before UTF-8 decoding or JSON parsing, checks the declared schema and revision, and never derives a path from an artifact ID.
- Revision-scoped in-memory verified and in-flight caches deduplicate repeated requests. Detail completion may populate its cache after navigation, but the selection generation and artifact identity prevent a slow response from replacing a newer selection.
- Compact topology immediately supplies identity, type, title, state, labels, relations, filters, board cards, and history. Verified detail restores exact dates, metadata, type-specific fields, EARS presentation, and safely rendered body. Evidence expansion uses the same existing inert Markdown renderer.
- Direct `file://` startup and missing, malformed, redirected, mismatched, or unsupported resources produce scoped unavailable states. No persistent storage, service worker, cross-origin repository data, or bulk body prefetch exists.

## Actual static-origin review

The final generated directory was served with Python's standard-library HTTP server on `127.0.0.1`. The in-app Chromium browser rendered Overview, Lineage, Relations, Evidence, and Readiness with the existing visual model and authority wording.

The server trace showed the intended sequence:

1. `/`, `dashboard-manifest.json`, one summary JSON, and one topology JSON on Overview startup;
2. one artifact-detail JSON for each explicitly visited Lineage artifact;
3. one evidence text only after `Read rendered evidence` was expanded; and
4. one readiness JSON only after selecting Readiness.

The selected intent body rendered exact metadata and Markdown. Clickable Relations navigated `INT-AGR-001 -> CAP-AGR-001 -> REQ-AGR-001 -> WO-AGR-001` while preserving history. The Evidence tab initially showed only descriptor metadata and a disclosure control; expansion then rendered `WO-AGR-001` evidence. Readiness subsequently rendered its subject, gates, evidence rows, findings, and provenance. No artifact detail or evidence request appeared in the initial request set.

## Regression coverage

Focused tests assert bootstrap/manifest schemas, CSP `connect-src 'self'`, same-origin final URL, redirect rejection, Web Crypto verification, descriptor equality, controlled paths, manifest revalidation, request deduplication, view deferral, explicit evidence expansion, stale-selection suppression, no browser persistence, bounded shell/summary/topology, safe Markdown/EARS presentation, relation navigation, 20-entry history, semantic colors, and the unchanged pinned optional `3d-force-graph` URL. The complete suite result and formal checks are recorded in `WO-DST-014` evidence.

## Residual risk and actions not taken

Current-browser Web Crypto and static HTTP are required; the page deliberately does not retain offline/file support. The optional graph CDN remains the previously accepted external availability/trust exception and receives no repository payload. Browser cache and host propagation can temporarily expose a stale fixed manifest, which fails its bootstrap hash rather than mixing data.

Each scoped failure now exposes a keyboard-operable retry control. Retry evicts the affected verified-cache entry and repeats the same fetch, origin, byte-count, digest, UTF-8, JSON, schema, revision, and identity checks; startup retry clears the revision-scoped caches and revalidates the manifest and summary. No commit, VREC, PR, push, release, package publication, Pages update, or deployment was performed.
