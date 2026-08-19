+++
id = "SPEC-DST-011"
type = "specification"
title = "Structured and reversible Explorer Lineage"
status = "approved"
owners = ["technical-owner", "product-owner", "quality-owner", "security-owner"]
created = "2026-08-16"
updated = "2026-08-19"

[relations]
specifies = ["REQ-DST-040", "REQ-DST-041"]
+++

# Specification: Structured and reversible Explorer Lineage

## Scope

Replace the current free-positioned two-hop/nine-card Lineage projection with a deterministic artifact board and reversible navigation history. The board groups formal artifact types for scanning while the canonical snapshot, exact type names, directed relations, relation authority, lifecycle labels, artifact details, evidence, and accountable decision boundaries remain authoritative.

This contract changes only the Lineage browser presentation and its bounded in-memory view state. It does not change the Overview topology, `harness-dashboard-snapshot-v1`, generator semantics, validators, inspection, formal artifacts, coverage, readiness, commit-bound assurance, release eligibility, CLI behavior, or the accepted CDN boundary.

## Conceptual board model

1. Render the following fixed presentation groups from left to right, with their exact formal artifact types as labeled sublanes:

   | Presentation group | Exact artifact-type sublanes |
   | --- | --- |
   | Purpose | `intent`, `capability` |
   | Definition | `requirement`, `specification` |
   | Design | `architecture`, `adr` |
   | Delivery | `work_order` |
   | Assurance | `verification`, `verification_record` |
   | Release and operation | `release_contract`, `release_record`, `operating_contract` |

2. Treat the group order as explanatory layout metadata only. It does not alter artifact schemas, impose mandatory stages, define a state machine, establish release order, or make visual left-to-right position authoritative.
3. Place every unknown nonempty artifact type in an `Other` group and a sublane labeled with its exact canonical value. Place a missing type in a visibly invalid `Unknown type` sublane without inventing a formal type.
4. Order groups by the table, sublanes by the table or exact unknown value, and cards within a sublane by canonical artifact ID. Identical normalized input and scope produce identical group, sublane, and card order.
5. Use a horizontally scrollable board at desktop widths. At narrow widths, stack or section the same labeled groups without hiding cards, changing their semantic group, or relying on connector geometry as the only relation route.
6. Replace the current rank coordinates, absolute free-positioning, and zoom-dependent comprehension. Existing zoom controls may be removed; readable card scale, scrolling, focus movement, and labeled board structure are the primary navigation mechanisms.

## Focused scope and traversal

7. Maintain an independent Lineage depth control with exactly `1 - direct relations` and `2 - second-level context`. Initial and externally opened Lineage sessions start at depth 1.
8. At depth 1, include the selected root and every existing artifact incident to a resolved direct relation in either direction. Do not cap or silently omit direct neighbors.
9. At depth 2, retain the complete depth-1 scope and add at most 100 distinct non-direct artifacts through iterative breadth-first traversal of resolved incident relations.
10. Sort traversal candidates by depth, neighbor ID, relation name, authority, source, and target before applying the second-level budget. Shuffled canonical input must select the same added IDs.
11. Root and direct artifacts do not consume the 100-node second-level budget. If eligible non-direct context exceeds the budget, report the visible and omitted counts in persistent text and accessible status.
12. Traverse cycles, self-relations, duplicate edges, and repeated paths using visited artifact IDs and a fixed depth bound. Do not recurse without a bound or synthesize nodes for missing targets.
13. Recompute scope when the selected artifact or Lineage depth changes. The Overview text/type/status/context controls remain independent and are not silently applied to focused Lineage.

## Cards and relation presentation

14. Render each included artifact once as a keyboard-operable card containing its exact ID, title or concise statement, exact type, and lifecycle status.
15. Distinguish the selected root, direct neighbors, and second-level context through text plus border, weight, opacity, or another non-color treatment. Preserve established lifecycle meaning and do not recolor a card into an invented state.
16. Render every resolved relation whose endpoints are included. Preserve canonical source and target direction with an arrow or equivalent explicit directional label.
17. Preserve the exact relation name and declared or derived authority. Direct relations incident to the selected root receive primary visual emphasis and an immediately readable relation label. Secondary relations may use lighter connectors and reveal labels on keyboard focus, pointer inspection, or the authoritative Relations detail.
18. Do not reverse a relation for visual order. Route reverse-group, same-group, same-type, self, and parallel relations safely; connector overlap must not change meaning.
19. If multiple relations join the same endpoints, retain every relation name and authority through separate connectors or an explicit grouped control. Do not collapse different relations into an unlabeled edge.
20. Report unresolved direct relation count and target IDs near the board or selected-artifact summary, and keep their full records in the Relations tab. Missing targets are not formal-artifact cards.
21. Retain the current artifact detail tabs, evidence paths, complete direct-relation list, and non-authoritative next-step information. Update `On This Path` wording if needed so it does not duplicate or contradict navigation history.
22. The relation connector layer is presentation only. The DOM's card content, relation labels or list, and scope text must retain the board's meaning when connectors cannot be perceived.

## Reversible navigation state

23. Maintain `lineageHistory`, `lineageHistoryIndex`, and `lineageInitialId` or equivalent bounded in-memory state. None is serialized into canonical output.
24. Starting Lineage from Overview, Readiness, or another explicit external entry point resets history to the target artifact, sets it as the initial artifact, sets the cursor to zero, and initializes depth to 1.
25. Selecting a different Lineage card or artifact-detail relation truncates entries after the current cursor, appends the selected artifact, advances the cursor, and rerenders the board. Selecting the current artifact changes nothing.
26. Back decrements the cursor when possible. Forward increments it when possible. A history chip sets the cursor to that exact visit without deleting other entries.
27. Disable Back at the first retained entry and Forward at the latest entry. Expose the current entry with `aria-current` or an equivalent programmatic state.
28. Render a labeled, horizontally scrollable `Navigation history` region containing visited-ID controls in visit order plus separate Back, Forward, and Return to initial controls.
29. The history region must state that visits are navigation state, not formal artifact lineage. It must not draw edges between visits or call them parents, ancestors, descendants, provenance, or approvals.
30. Keep no consecutive duplicate ID. Non-consecutive revisits remain distinct visits because they record actual navigation order.
31. Retain at most 20 visits. On the twenty-first append, remove the oldest entry that is not current, adjust the cursor, preserve `lineageInitialId` separately, and announce that older visit history was discarded.
32. Return to initial focuses `lineageInitialId`. If it is still a retained history entry, move to that visit; otherwise append it using the ordinary branch rule without exceeding the bound.
33. If a retained ID no longer resolves in the loaded snapshot, mark its control unavailable and do not substitute another artifact. If the current entry becomes unavailable, show a bounded empty state and allow navigation to another retained entry or the initial artifact.
34. A page reload or newly generated page begins a new bounded visit-history session. Controlled same-document URL fragments and `history.pushState`/`history.replaceState` may route only Overview, a selected Lineage artifact, the Readiness index, a selected Readiness subject, or a gate-state listing. Route parsing must reject or safely ignore unknown values, must not serialize the visit trail or canonical content, and must not add runtime network calls. Do not use local or session storage, cookies, telemetry, repository writes, or cross-document route state.
35. After a card selection rerenders the board, move focus to the corresponding selected card or its board heading. Back, Forward, history-chip, and Return actions retain predictable focus on the activating control or its replacement.
36. After history is rendered for an append, Back, Forward, history-chip jump, or Return to initial, compare the current visit control with the visible bounds of the history list and adjust only that list's horizontal scroll position by the minimum amount needed to reveal the current control fully. The reveal must work toward either edge, must not scroll the document or board, and must not assign focus.

## Accessibility, safety, and fallback

37. Stage headings, sublane headings, current selection, context depth, history position, truncation, relation direction, relation authority, and unavailable state must be available as text and not depend on color, connector geometry, or hover.
38. Cards and navigation controls use native buttons or equivalent keyboard semantics, visible focus, descriptive accessible names, and touch targets consistent with the current Explorer.
39. Repository-derived IDs, titles, statements, types, states, relation names, paths, and missing-target values remain inert through text-safe DOM construction or context-appropriate escaping.
40. Board traversal and history operations are iterative and bounded. Layout uses no force simulation and must not execute artifact-provided markup, style, selectors, URLs, or script.
41. The Lineage board, history, detail, evidence, and relation list remain usable when the optional `3d-force-graph` CDN load fails. No new runtime URL or dependency is permitted.
42. Invalid or unsupported canonical input keeps the existing bounded snapshot failure behavior rather than rendering a partially authoritative board.

## Distribution and compatibility

43. `templates/repository/standard/scripts/harness_explorer/index.template.html` remains the sole reusable Explorer template and `scripts/harness_explorer/index.template.html` remains its byte-equivalent active managed copy.
44. Reconcile the active copy through the supported managed candidate/upgrade transaction and update only the applicable schema-2 lock entry.
45. Preserve current installation, adoption, doctor, safe upgrade, package-data, dashboard generation, and public-demonstrator compatibility.
46. Preserve the exact accepted `3d-force-graph@1.79.0` unpkg URL for Overview and the fallback/risk controls of `ADR-DST-008`; this Lineage implementation does not consume that library.
47. Preserve historical generated dashboards. Only dashboards generated from a later candidate contain the new Lineage presentation.

## Architecture applicability assessment

This change remains inside the browser-presentation responsibility, canonical-data dependency direction, managed source boundary, and trust controls implemented by `ARCH-DST-008` and decided by `ADR-DST-008`. `ARCH-DST-008` does not currently declare an `addresses` relation to `REQ-DST-040` or `REQ-DST-041`; these requirements are a routine presentation refinement rather than a new architecture-significant driver. Accordingly, no `architecture` relation, architecture amendment, or new ADR is selected for `WO-DST-012`.

Stop and reassess architecture applicability if implementation requires canonical snapshot fields, generator behavior, persisted UI state, URL/browser-history ownership, another dependency, network behavior, trust-boundary change, deployment change, or a change to the accepted CDN decision.

## Explicitly unspecified decisions

The implementation agent may choose concise group descriptions, board spacing, connector routing, label placement for secondary relations, narrow-screen stacking, overflow treatment for dense direct lanes, selected/direct/context visual tokens, focus-restoration mechanics, and the exact accessible history-bound announcement within this contract. It may not change group/type membership, omit direct neighbors, exceed depth two or the second-level budget, silently truncate, reverse relations, turn visit history into graph lineage, persist navigation, rename canonical types, add a model or dependency, or alter governance authority.
