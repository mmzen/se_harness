+++
id = "SPEC-DST-010"
type = "specification"
title = "Refine Explorer overview navigation and provenance"
status = "approved"
owners = ["technical-owner", "product-owner", "quality-owner", "security-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
specifies = ["REQ-DST-035", "REQ-DST-036", "REQ-DST-037", "REQ-DST-038", "REQ-DST-039"]
+++

# Specification: Refine Explorer overview navigation and provenance

## Scope

Refine the existing canonical Harness Explorer Overview by removing its exhaustive Definition Coverage table, adding bounded context expansion around the artifacts selected by its current filters, making the artifact text filter directly clearable, and keeping observed repository provenance legible in the bounded sidebar. Preserve the established visual design, canonical snapshot boundary, focused Lineage behavior, safe static rendering, optional 3D dependency, and managed distribution model.

This contract changes browser-side presentation and in-memory graph projection only. It does not change `harness-dashboard-snapshot-v1`, generator semantics, formal graph relations, coverage calculation, validator or inspection rules, readiness, VREC/RLS authority, or `harnessctl dashboard` command behavior.

## Overview compaction

1. Remove the `Definition Coverage` panel, its table markup, `coverageRows` target, and table-population behavior from the Overview.
2. Preserve canonical `coverage` unchanged in the embedded snapshot and standalone `dashboard-data.json`.
3. Preserve `metricCoverage` and `metricCoverageDetail`, with total, specified, and verification-contract-covered meaning unchanged.
4. Preserve the artifact-detail definition-coverage field and requirement discovery through the graph and focused Lineage.
5. Do not introduce a replacement exhaustive Overview list, aggregate score, inferred verification, or a persisted coverage view model.

## Root filtering and context projection

6. Compute `rootMatches` from the current text, artifact-type, and lifecycle filters using the existing case-insensitive ID/title search and exact canonical type/status values.
7. Add one labeled select control with values `0`, `1`, and `2`, presented as matches only, direct neighbors, and two hops. The initial and reset value is `0`.
8. At depth `0`, `visibleNodes` equals `rootMatches` and preserves existing link filtering.
9. At depth `1` or `2`, construct an in-memory adjacency index from resolved relations already projected into the Overview. Traverse incident relations in either direction, breadth first, from every root match.
10. Sort roots by canonical artifact ID and adjacency candidates by neighbor ID, relation type, authority, source, and target before traversal. Interaction over identical snapshot and control values must select the same visible node set.
11. Root matches are never removed by the context budget. Add at most 100 distinct non-root context nodes. Stop adding context when the budget is reached while retaining all links whose endpoints are visible.
12. A missing target is never synthesized as a node. Cycles, self-relations, duplicate edges, repeated paths, unknown artifact types, and zero matches terminate safely.
13. Type and lifecycle filters constrain roots, not context. Context nodes may have other canonical types or states and must not be counted as filter matches.

## Presentation behavior

14. Root matches, context nodes, and the selected node are three distinct presentation states. Selected emphasis remains amber. Match/context distinction uses at least size, opacity, shape, label text, or another non-color cue.
15. Semantic state/type/assurance colors retain their current role for all visible nodes; context styling must not overwrite artifact semantics, and the mode-specific mapping must satisfy the distinct-color contract below.
16. The graph count reports root-match count, context-node count, visible resolved relation count, selected depth, and a clear truncation marker when applicable.
17. The analysis lens describes the complete visible graph rather than mislabeling context nodes as filter matches. Its text reports the match/context scope.
18. Changing text, type, status, or depth recomputes the view without changing the snapshot. A selected artifact that leaves the visible set is cleared from the graph inspector; a visible selection remains selected.
19. The existing `Fit graph`, `Reset`, node inspector, and `Open focused lineage` interactions remain available. Graph reset restores mode `state`, all types, all states, empty text search, and context depth `0`.
20. The dedicated Lineage view remains the bounded detailed navigation route. Overview context expansion does not change its two-hop/nine-node contract or relation-detail access.

## Accessibility, fallback, and safety

21. The new select is keyboard operable, has a programmatic label, and remains usable at desktop and narrow widths.
22. Match, context, depth, counts, and truncation are available as text and do not depend on the 3D canvas or color perception.
23. When the CDN-backed 3D renderer fails, the page retains coverage metrics, filter/context controls and textual scope reporting, Lineage, Readiness, provenance, evidence, and controlled outcomes. The removed table is not required as fallback content because coverage remains available through metrics and artifact detail.
24. The traversal consumes only normalized canonical IDs and relations. It creates no HTML, URL, script, style, network request, telemetry, storage entry, or repository mutation from repository content.
25. Context work is iterative and bounded; no recursive unbounded traversal is permitted.

## Distribution and compatibility

26. `templates/repository/standard/scripts/harness_explorer/index.template.html` remains the sole reusable template source and `scripts/harness_explorer/index.template.html` remains its byte-equivalent active managed copy.
27. Reconciliation must use the supported managed candidate/upgrade transaction and update only the applicable schema-2 lock entry. Repository-specific self-hosting controls remain protected.
28. Existing valid snapshots, unknown future artifact types, generator outputs, package data, installation, adoption, doctor, safe upgrade, and CDN policy remain compatible.
29. No runtime URL or dependency changes. The exact accepted `3d-force-graph@1.79.0` unpkg URL and `ADR-DST-008` risk boundary remain unchanged.
30. The release-bound public demonstrator may expose this behavior only from a later release/governance snapshot containing the implementation; a replay of v0.4.0 must remain historical.

## Observed-revision presentation

31. Preserve `snapshot.repository.revision` exactly as normalized canonical data. Presentation must not mutate, replace, or write an abbreviated value back into the snapshot or any derived identity field.
32. Treat a revision as abbreviable only when it is exactly 40 or 64 ASCII hexadecimal characters. Compare case-insensitively for this presentation test and preserve the original character case in displayed and complete values.
33. In the bounded sidebar repository-status area, show an abbreviable revision as its first 12 characters followed by the single Unicode ellipsis `…`. Describe it as an observed revision or snapshot revision; do not label the prefix as an exact commit ID.
34. Keep the complete revision visible in the existing Snapshot Information interaction and expose it as programmatically associated accessible text for the abbreviated sidebar value. No mouse-only disclosure may be the sole route to the complete value.
35. Render `unavailable`, missing values, and any other nonmatching value without abbreviation, invented substitution, link construction, or executable interpretation.
36. Apply generic containment to repository-status text, including repository, branch, and revision values: flex or grid children must be shrinkable and long untrusted tokens must wrap or clip within the sidebar without creating horizontal page overflow at supported desktop and narrow widths.
37. Never use the abbreviated prefix for equality, lookup, filtering, selection, URL construction, manifest data, digests, VREC/RLS commit binding, provenance decisions, or assurance text. All such behavior continues to use the complete canonical value.

## Artifact-filter clearing

38. Add a dedicated native button immediately adjacent to the existing `search` input in the top action group. Preserve the Snapshot Information button and keep all controls usable without overlap at supported desktop and narrow widths.
39. Give the button a programmatic label with the meaning `Clear artifact filter`. Any icon or shortened visible treatment is supplementary and must not be the only expression of purpose.
40. Keep the clear button in a stable layout position. Disable it exactly when the search value is empty and enable it when the value contains one or more characters, including whitespace before trimming for matching.
41. Activation sets only the search input value to the empty string and invokes the same application update path as a user-originated search-input change. Overview root matches, context, visible relations, counts, analysis text, and stale-selection handling must recompute immediately.
42. Preserve graph mode, artifact type, lifecycle status, context depth, current view, zoom, and any selection that remains visible and valid after recomputation. The existing graph Reset action remains the operation that restores all graph controls to defaults.
43. After activation, return focus to the search input so keyboard users can immediately enter another query. Native button activation through pointer, Enter, or Space must have equivalent results.
44. Do not use the cleared or prior query to mutate canonical data, construct markup or URLs, persist history, trigger network activity, or change matching semantics. Repository-derived text remains inert.

## Semantic analysis colors

45. Build an independent deterministic category-to-color map for each analysis mode from all nodes in the complete normalized snapshot, not only the currently visible filter result.
46. Sort each mode's canonical category values before assigning colors. Every distinct category in the same mode must receive a distinct color, and the same category must retain that color while text, type, lifecycle, or context-depth filters change.
47. State, type, and assurance maps are independent. A value in one mode may share a color with a value in another mode because those categories never coexist in one legend.
48. Root matches and context nodes use the same mode/category mapping. Match/context size distinction and textual scope remain unchanged.
49. Selected-node amber remains a temporary override and must not enter the category map or legend. Clearing selection restores the node's mapped category color.
50. The deterministic palette must cover every category in the current formal type, lifecycle, and derived-assurance vocabularies without reuse. Unknown future categories receive deterministic fallback colors without changing snapshot data or executable behavior.
51. The legend and analysis lens must use the same map as graph nodes and continue to expose category names and counts. Color remains supplementary and does not infer status, assurance, authority, coverage, or compliance.

## Architecture applicability assessment

`ARCH-DST-008` and `ADR-DST-008` remain the implemented architecture and decision context. This refinement stays within their browser-presentation responsibility, canonical-data dependency direction, managed-source boundary, and accepted optional CDN risk. It adds no architecturally significant driver, dependency, protocol, trust boundary, deployment model, or vendor choice; therefore no new architecture artifact or ADR is applicable to this packet.

## Explicitly unspecified decisions

The implementation agent may choose concise control wording, the clear-control icon or visible treatment, responsive placement, match/context size and opacity treatment, truncation copy, efficient adjacency-map structure, exact palette values within the established visual identity, and the exact non-authoritative sidebar label within this contract. It may not hide the clear control through color alone, turn it into a full reset, increase the maximum depth or context-node budget, hide roots, apply type/status filters to context, change relation authority, reuse a color for two categories in one mode, make color authoritative, treat an abbreviated revision as identity, or add a second data model without an approved packet amendment.
