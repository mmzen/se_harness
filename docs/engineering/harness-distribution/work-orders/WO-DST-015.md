+++
id = "WO-DST-015"
type = "work_order"
title = "Load Explorer data progressively and safely"
status = "implemented"
owners = ["engineering-owner", "technical-owner", "security-owner", "quality-owner", "product-owner"]
created = "2026-08-17"
updated = "2026-08-17"

[assurance]
commit_bound_verification = "required"
rationale = "The work changes browser acquisition, cryptographic verification, cache and race behavior, CSP, safe content timing, navigation reliability, and failure presentation used by human engineering and assurance review."
decided_by = "repository-owner"

[relations]
implements = ["REQ-DST-050", "REQ-DST-051", "REQ-DST-052", "REQ-DST-053"]
specifications = ["SPEC-DST-014"]
verification = ["VER-DST-014"]
architecture = ["ARCH-DST-010", "ADR-DST-010"]
+++

# Work Order: Load Explorer data progressively and safely

## Lifecycle

The repository-owner request and authorization recorded in `WO-DST-014` also accepts this coordinated browser scope. It may proceed in the same isolated stacked branch after the complete packet validates. It remains a distinct work order so generation/publication integrity and asynchronous browser behavior retain separate verification contracts and evidence.

No commit, VREC, push, pull request, release, package publication, Pages publication, or change to PR 63 is authorized by implementation.

## Objective

Make Overview, Lineage, Readiness, artifact details, and retained evidence consume the verified static bundle progressively while preserving current semantics, navigation, safe rendering, accessibility, and authority boundaries.

## In scope

- Implement bootstrap/manifest/summary startup and one preparse same-origin size/SHA verification boundary.
- Load compact topology for Overview/Lineage and readiness only on Readiness entry.
- Load one artifact detail on first focus and one evidence body on explicit expansion.
- Add revision-scoped in-memory verified cache, in-flight deduplication, cancellation where available, and unconditional stale-response suppression.
- Preserve filters, graph, lane board, relation direction, labels, EARS, safe Markdown, 20-history navigation, focus/reveal, Readiness, and provenance.
- Add scoped loading, failure, integrity, unsupported-transport, and keyboard-operable retry states.
- Update CSP and documentation only as needed for same-origin static fetch and local HTTP serving.
- Add browser/network/security/accessibility/performance tests and retain evidence keyed to `WO-DST-015`.

## Out of scope

- Bundle generation/publisher implementation owned by `WO-DST-014`, except integration adjustments.
- Prefetching all artifact/evidence resources, persistent caching, service workers, offline/file support, server search, API/database, authentication, telemetry, analytics, editing, comments, or repository writes.
- New assurance derivation, artifact/relationship semantics, graph layout redesign, topology sharding, CDN change, automatic publication, or lifecycle decisions.

## Authorized decision envelope

The implementation agent may choose loading indicators, retry wording, request/cache helper names, cancellation implementation, cache eviction within the manifest bound, and whether topology begins immediately after summary or on the next rendering opportunity. It must preserve exact trigger boundaries, full preparse verification, no bulk prefetch, history semantics, safe renderers, and latest-selection-wins invariants.

## Constraints

- Use browser platform APIs already available on supported current browsers; no new CDN or runtime library.
- Treat HTTP responses and repository-derived data as untrusted and render only verified/sanitized content.
- Keep the exact accepted graph CDN exception optional and repository-data-free.
- Preserve one standard managed installation, canonical/active parity, current visual identity, responsive behavior, and protected controls.
- Do not alter or restore the stashed `VREC-DST-011` on this branch.

## Expected change surface

- canonical and active Explorer template and generator integration;
- focused WebUI/browser fixtures and tests, including a local static server where necessary;
- managed lock entries through supported reconciliation;
- current dashboard/reference/publication notes;
- DST-015 artifacts, domain index, and retained evidence.

No validator, inspector, preflight, self-hosting governor, release action, package publication, or demonstrator deployment mutation is expected.

## Required verification

Execute all cases in `VER-DST-014`, relevant regressions from `VER-DST-010..012`, actual browser/static-server request tracing, unsupported `file://`, manifest/resource tamper, topology/readiness deferral, first/repeat artifact visits, shared/multiple evidence, rapid navigation/reordered completion, retry and failure containment, 20-history/focus behavior, hostile Markdown/CSP/network checks, desktop/narrow/accessibility review, no console errors, full tests, deterministic generation, managed upgrade/idempotence/parity, formal validation, phase preflight, doctor, inspect, and `git diff --check`.

## Evidence to record

Retain exact browser/server versions; request order/count/bytes; manifest/resource hashes; delay/tamper/failure fixtures; cache/history/state transitions; screenshots where useful; CSP/console/network output; safe-render and accessibility observations; deterministic and managed parity; changed paths; deviations; residual risks; and external actions not performed in `docs/engineering/harness-distribution/evidence/WO-DST-015-verification.md`.

## Stop and escalate conditions

Stop for any unverified parse/render, cross-origin content fetch, bulk prefetch, stale overwrite, cache crossing manifests, unsafe Markdown, history/semantics regression, new dependency/origin, persistent storage/service worker, server requirement beyond static HTTP, topology-sharding need, protected-control change, failing tests, or unauthorized commit/VREC/PR/release/publication/deployment.

## Completion report format

Report request sequence and triggers; verification/cache/race design; view/artifact/evidence states; history and safe-render preservation; HTTP/CSP behavior; payload measurements; browser/accessibility review; managed parity; tests; documentation; changed paths; deviations; residual risks; and all external actions not performed.

## Completion

Manifest-first loading, verified same-origin resources, view/detail/evidence deferral, in-memory deduplication, stale-response suppression, failure containment, safe rendering, static-origin documentation, browser review, tests, and retained evidence are complete. This state records completed implementation only; commit-bound assurance remains required and no commit, VREC, push, pull request, release, package publication, or Pages deployment was performed.
