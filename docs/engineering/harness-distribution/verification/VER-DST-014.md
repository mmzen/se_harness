+++
id = "VER-DST-014"
type = "verification"
title = "Verify progressive Explorer acquisition and navigation"
status = "approved"
owners = ["quality-owner", "security-owner", "product-owner"]
created = "2026-08-17"
updated = "2026-09-01"

[relations]
verifies = ["REQ-DST-050", "REQ-DST-051", "REQ-DST-052", "REQ-DST-053"]
+++

# Verification Contract: Verify progressive Explorer acquisition and navigation

## Independence

Browser tests observe actual HTTP requests, delayed/reordered responses, DOM output, focus, cache behavior, and console/network effects through a static server. Fixtures are independently hashed and tampered after generation so success cannot rely solely on producer metadata or mocked helper return values.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| REQ-DST-050 | Browser network and view-isolation tests | Overview, Lineage, Readiness, topology/readiness failure | only required coarse datasets load; unrelated verified panels remain usable |
| REQ-DST-051 | Artifact-selection/history tests | first visit, cache revisit, relation click, Back/Forward/initial, mismatched detail | exactly selected detail loads and existing 20-visit/focus semantics remain correct |
| REQ-DST-052 | Evidence-expansion and hostile-content tests | collapsed/multiple/shared/tampered evidence | no body loads before expansion; one verified document renders safely per action |
| REQ-DST-053 | Delayed/reordered/failure injection | rapid navigation, retry, stale completion, cache revision, parse/render failure | latest verified selection wins and failure remains scoped and non-authoritative |

## Acceptance scenarios

- Start the page and assert request order: index, manifest, summary; no readiness, artifact, or evidence content before its trigger.
- Enter Overview/Lineage and verify one topology request; enter Readiness and verify one readiness request.
- Visit several artifacts, navigate back and forward through the Lineage history controls, and confirm the request/cache counts.
- Expand one of several evidence documents, then one shared by another artifact; verify exact requests, digest reuse, safe rendering, and metadata visibility.
- Delay artifact A, select B, complete B then A, and prove B remains selected; repeat with abort unavailable.
- Tamper each resource class and verify no bytes are parsed/rendered before size/digest checks.

## Property and invariant tests

- One manifest/revision scopes every descriptor, in-flight request, cache entry, view state, and artifact/evidence render.
- Only verified resources enter cache; retries repeat all checks; identical in-flight requests deduplicate.
- Selected ID/history updates synchronously from verified topology and cannot be redefined by detail JSON.
- Stale completion never changes selected ID, active view, history cursor, focus target, or visible newer content.
- Artifact and evidence requests are at most one per uncached digest; no bulk detail/evidence prefetch occurs.
- Error states never become empty canonical data, lifecycle changes, assurance claims, or aggregate scores.

## Static and architecture checks

- One verified-fetch boundary performs same-origin/path/HTTP/size/SHA/schema checks before parsing.
- No `eval`, dynamic import, unsafe URL construction, persistent storage, service worker, telemetry, polling, or backend endpoint exists.
- Renderer safety, EARS clauses, relation direction/authority, semantic labels, Lineage history, and Readiness provenance remain intact; no remote origin is requested.
- CSP permits required same-origin data while preserving active-content and external-origin restrictions.

## Security and privacy checks

- Exercise redirect, cross-origin, wrong path, MIME confusion, invalid UTF-8/JSON, duplicate key where applicable, prototype-shaped keys, oversized response, digest mismatch, hostile Markdown/URL, and injected IDs.
- Assert verification precedes parsing and sanitizer remains after Markdown parsing.
- Confirm console/errors do not print complete repository/evidence bodies or unsafe response URLs.
- Confirm static requests use no unexpected credentials and graph CDN receives no repository data.

## Performance and resilience checks

- Record uncompressed transfer/request sequence, time to shell/summary/topology/current detail, main-thread errors, cache entries, and verified bytes on current repository and throttled network.
- Assert no artifact/evidence Markdown on initial path and no Readiness request until entry.
- Exercise offline-after-cache, server 404/500, delayed response, repeated retry, rapid 100-selection stress, and renderer failure without global UI loss.
- Confirm cache remains bounded by finite manifest descriptors and resets on reload/revision.

## Manual assessments

At desktop and narrow widths review shell-first comprehension, loading stability, retry affordance, nonjumping detail layout, history reveal/focus, relation navigation, multiple evidence expansion, accessible announcements, keyboard operation, error distinction, no-color meaning, and the `file://` serving instruction.

## Evidence retention

Retain browser/server versions, exact request logs and order, resource hashes, delay/tamper scripts, history/cache transition tables, screenshots where useful, accessibility and responsive observations, CSP/console output, byte/timing observations, deterministic bundle identity, changed paths, deviations, residual risks, and all external actions not performed under `docs/engineering/harness-distribution/evidence/WO-DST-015-verification.md`.

## Residual uncertainty

Network timing and browser scheduling vary, so correctness relies on tokens/invariants rather than timing thresholds. Web Crypto and static HTTP are required for supported progressive operation. Manual accessibility and performance review supplements, but does not replace, deterministic request and state tests.

## Amendment record

**History and CDN checks follow the `SPEC-DST-014` amendment, proposed 2026-09-01
under `WO-DST-023`.** The `REQ-DST-051` matrix row's reference to the 20-visit
window reads as the Lineage history controls of the designed page. Every
other check is unchanged.
