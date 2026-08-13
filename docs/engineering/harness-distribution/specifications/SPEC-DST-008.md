+++
id = "SPEC-DST-008"
type = "specification"
title = "Canonical Harness Explorer WebUI"
status = "implemented"
owners = ["technical-owner", "product-owner", "quality-owner", "security-owner"]
created = "2026-08-13"
updated = "2026-08-13"

[relations]
specifies = ["REQ-DST-029", "REQ-DST-030", "REQ-DST-031", "REQ-DST-032", "REQ-DST-033"]
+++

# Specification: Canonical Harness Explorer WebUI

## Scope

Integrate the reviewed WebUI prototype while retaining its page structure, visual identity, responsive behavior, and `3d-force-graph` interaction. Keep the existing deterministic generator and canonical snapshot as the model boundary, reconcile the prototype terminology with the actual harness, and distribute one managed implementation.

This contract changes presentation and presentation-side derivation. It does not change formal artifacts, relation authority, validator rules, lifecycle transitions, quality-gate meaning, verification capture, release eligibility, or the `harnessctl dashboard` command boundary.

## Source data contract

1. The only persisted Explorer model is `harness-dashboard-snapshot-v1`.
2. The canonical top-level sections remain `schema`, `finding_rules_version`, `quality_gates_version`, `repository`, `artifacts`, `relations`, `diagnostics`, `findings`, `coverage`, `readiness`, `revision_provenance`, `revision_policy`, `experiments`, and `evidence`.
3. The UI must not require `schemaVersion`, `generatedAt`, `metrics`, `graph`, `lineage`, or a second `readiness` shape. Presentation metrics and focused graph subsets are derived in memory from canonical sections.
4. Generation time and run observations remain in `generation-summary.json`, outside canonical snapshot hashing.
5. The owned HTML template contains exactly one `__HARNESS_SNAPSHOT_JSON__` marker in an inert JSON script element. Rendering replaces it with deterministic escaped canonical JSON.
6. Unsupported schemas and malformed payloads produce a visible bounded error state.

## Artifact and relation presentation

7. The UI supports the current artifact types without hard failure: `intent`, `capability`, `requirement`, `specification`, `architecture`, `adr`, `work_order`, `verification`, `verification_record`, `release_contract`, `release_record`, and `operating_contract`.
8. Unknown future types use neutral styling and remain inspectable.
9. Relations retain `source`, `relation`, `target`, `authority`, `target_exists`, and optional `via`. The UI must not rename these into a smaller incompatible relation vocabulary.
10. Declared and derived relations are visually and textually distinguishable. A derived path never becomes formal authority.
11. Focused lineage traversal is cycle-safe and bounded. The reader can reach the complete declared relation list even when a visual view is reduced.

## Five-question interaction contract

12. The interface retains explicit routes for the five current questions: existence, definition coverage, reassessment impact, inconsistency/readiness, and controlled harness outcomes.
13. Overview, Lineage, and Readiness may remain as primary visual groupings when every question stays directly discoverable and no information is lost.
14. The existence view shows artifact identity, type, lifecycle, owners, direct typed relations, and a bounded connected lineage.
15. Definition coverage separately reports active specification and verification-contract coverage. It must not call this commit-bound verification.
16. Impact shows direct inbound, direct outbound, transitive inbound, and transitive outbound declared connectivity. It labels results as reassessment candidates, not automatic changes.
17. Findings retain `rule`, `severity`, `message`, `artifacts`, `paths`, `authority`, and `evidence` when present. Validator diagnostics remain distinguishable from derived findings.
18. Readiness renders each G0-G5 gate and its exact conditions in canonical states `satisfied`, `unsatisfied`, or `not_assessable`. It never emits an aggregate assurance score.
19. Revision presentation distinguishes observed checkout state from commit-bound authoritative records, including commit, object format, dirty state, checkout comparison, policy, and supersession.
20. Controlled experiments remain observations. Their cohorts, measures, provenance, limitations, and comparisons do not become product or release authority.

## Security and local execution

21. Generated output may load exactly `https://unpkg.com/3d-force-graph@1.79.0/dist/3d-force-graph.min.js` at runtime to preserve the reviewed 3D topology. No other runtime script, font, image, style, hosted API, telemetry, dynamic import, or WebSocket is permitted.
22. The CDN request must not contain repository artifact data. The page must remain a useful static evidence viewer when the 3D renderer is unavailable; only the 3D topology may degrade. `ADR-DST-008` records and accepts the non-content-addressed CDN availability and supply-chain risk for this candidate.
23. Repository strings are rendered with `textContent` or equivalent safe node construction. Dynamic HTML parsing of repository content is prohibited.
24. Embedded JSON escapes at least `&`, `<`, `>`, U+2028, and U+2029. Tests include closing-script, sentinel, markup, path, Unicode, long-string, and cyclic-graph inputs.
25. Graph and list work is bounded so hostile or unusually large repositories cannot create unbounded recursion.

## Visual and accessibility behavior

26. Preserve the original prototype's sidebar, Overview/Lineage/Readiness structure, topology-led composition, typography, colors, spacing, responsive behavior, and 3D interaction. Change the page only where required for canonical model fidelity, safe data handling, accessibility, and explicit failure states.
27. Status, authority, derived state, warning, error, and supersession cannot depend on color alone. Focus remains visible and interactive controls remain keyboard operable.
28. Desktop and narrow-width layouts must preserve every question, gate condition, finding, and provenance field. A visualization fallback may be simpler but not semantically empty.
29. Empty, invalid, unsupported, no-experiment, no-evidence, missing-target, and optional-visualization-failure states receive explicit copy.
30. Missing preview PNGs are removed from the design manifest and handoff rather than represented as shipped assets.

## Distribution and integration

31. `scripts/generate_harness_dashboard.py` remains the target-local standard-library generator and `se_harness/cli.py` remains a dispatcher unless a verified incompatibility requires a separately reviewed change.
32. The active root template and canonical copy under `templates/repository/standard/` remain byte-equivalent where managed parity applies.
33. Any new local asset is included in package data, installation planning, lock generation, safe upgrade, doctor, and package-parity tests.
34. Output remains transactional and contains deterministic `dashboard-data.json`, non-canonical `generation-summary.json`, and `index.html`. Snapshot data and all non-3D evidence views are embedded; the optional 3D renderer is the single documented CDN exception.
35. The revised `templates/webui/` handoff, schema documentation, manifest, brand contract, and prototype describe this same implementation model and do not claim independent authority.

## Compatibility and migration

Existing valid artifact repositories and the `harness-dashboard-snapshot-v1` consumer contract remain supported. No repository-owned formal artifact is rewritten. Safe upgrade follows existing managed-file integrity and customization rules. A snapshot schema change, if later needed, requires a separately governed compatibility decision.

## Explicitly unspecified decisions

The implementation agent may choose bounded traversal limits and the in-memory adapter from the canonical snapshot to the preserved prototype modules. It may not substantially reinterpret the original layout or visual identity, introduce a second persisted snapshot schema, add any runtime dependency beyond the exact accepted `3d-force-graph` URL, add an aggregate assurance score, infer lifecycle authority, rename artifact types, or lose canonical fields.
