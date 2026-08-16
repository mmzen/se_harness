+++
id = "VER-DST-010"
type = "verification"
title = "Verify Explorer Overview refinements"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
verifies = ["REQ-DST-035", "REQ-DST-036", "REQ-DST-037", "REQ-DST-038", "REQ-DST-039"]
+++

# Verification Contract: Verify Explorer Overview refinements

## Independence

Expected coverage meaning, canonical relation fields, filter and clear semantics, traversal depth, context budget, revision provenance, semantic category identity, and authority boundaries come from `REQ-DST-035`, `REQ-DST-036`, `REQ-DST-037`, `REQ-DST-038`, `REQ-DST-039`, `SPEC-DST-010`, the canonical snapshot contract, and the existing Explorer architecture—not from implementation-specific DOM structure or force-layout coordinates.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| `REQ-DST-035` | static template assertions, snapshot/output comparison, artifact-detail fixture, and manual Overview review | large active coverage, complete/partial/missing coverage, CDN failure | exhaustive Overview table and renderer are absent; compact metric, canonical coverage bytes, and artifact-level meaning remain available without implied VREC assurance |
| `REQ-DST-036` | deterministic graph-scope fixtures, browser interaction, accessibility review, and bounded-hostile-graph tests | depth 0/1/2, exact and multiple matches, type/status roots, cycles, self-links, duplicates, missing targets, dense hubs, unknown types, zero matches | every match remains, context is correct and visibly distinct, at most 100 context nodes are added, truncation is explicit, relation semantics remain authoritative, and interaction terminates safely |
| `REQ-DST-037` | revision-format fixtures, canonical-data comparison, accessibility inspection, and responsive review | SHA-1, SHA-256, shared 12-character prefixes, `unavailable`, missing/malformed values, long repository and branch labels | only valid full hashes are visibly abbreviated; full values remain canonical and accessible; prefixes never drive identity; all sidebar text remains contained |
| `REQ-DST-038` | DOM-state assertions, browser interaction, keyboard/accessibility review, and responsive review | empty, whitespace-only, populated, pointer, Enter, Space, non-default filters/depth/mode, valid and stale selections | clear state tracks the literal field value; activation empties only the text filter, refreshes immediately, preserves other controls and valid state, restores input focus, and does not obstruct Snapshot Information |
| `REQ-DST-039` | deterministic palette assertions and browser legend/node review | every current state, formal artifact type, and assurance signal; filtered subsets; context nodes; selection override; unknown category | each mode has a stable one-to-one category/color map, filtering does not recolor retained categories, graph/lens/legend agree, selection remains amber, and labels/non-color cues remain authoritative |

## Acceptance scenarios

- Search exactly for `SPEC-DST-007`; confirm depth zero shows one matching node, depth one adds its direct resolved neighbors, and depth two adds only nodes reachable within two displayed relations.
- Apply artifact type `specification` and depth one; confirm specifications remain the roots while connected requirements, architecture, work, or verification artifacts may appear as context.
- Use a query matching several roots and confirm expansion starts from all roots in deterministic ID order.
- Select a visible node, change filters until it is absent, and confirm stale graph selection and inspector action are cleared.
- Reset the graph and confirm search is empty, filters are all, analysis mode is state, and context depth is zero.
- Block the optional CDN and confirm the explicit failure state plus coverage metric, textual filter/context scope, Lineage, Readiness, provenance, evidence, and outcomes remain accessible.
- Render full SHA-1 and SHA-256 revisions and confirm the sidebar shows exactly 12 original characters plus `…`, while Snapshot Information and programmatically associated accessible text expose the complete unchanged value.
- Render two snapshots whose revisions share a 12-character prefix and confirm every comparison and displayed full-detail route still distinguishes their complete values.
- Render `unavailable`, missing, malformed, and very long non-hash revision text plus long repository and branch labels; confirm no abbreviation invents provenance and no text crosses or horizontally expands the sidebar.
- Enter `SPEC-DST-007`, select non-default artifact type, lifecycle, context depth, and analysis mode, then activate the clear control; confirm only the text becomes empty, graph scope refreshes, remaining choices persist, and focus returns to the search field.
- Confirm the clear control is disabled for an empty value, enabled for whitespace and other nonempty values, has the announced purpose `Clear artifact filter`, supports pointer/Enter/Space equivalently, and does not move when its state changes.
- Clear a query while a node is selected and confirm a still-visible selection persists while the existing stale-selection rule clears only a selection that becomes invalid.
- Select state, type, and assurance analysis in turn; for each complete mode assert that every legend category has a distinct computed color and every node with that category uses the same color.
- Record the color of a retained category, narrow and expand text/type/status/depth filters, and confirm the category color remains unchanged because assignment comes from the complete snapshot rather than the visible subset.
- In assurance mode, explicitly confirm `attention`, `assured`, `decision_required`, and `not_assessed` do not share colors. In type mode, confirm all current formal artifact types have distinct colors.
- Select and clear a node and confirm amber is only the temporary selection override; after clearing, the node returns to its stable category color.

## Deterministic graph fixtures

Exercise directed chains, inbound-only neighbors, outbound-only neighbors, cycles, self-relations, duplicate relations, declared and derived relations, unresolved targets, disconnected components, unknown artifact types, and deliberately shuffled input order. For identical normalized content and control state, assert identical root IDs, context IDs, truncation state, and visible relation IDs.

For a fixture with more than 100 eligible non-root nodes, assert all roots remain, exactly the first deterministic 100 context nodes are added, and truncation is reported. For more than 100 roots, assert no root is dropped and the context budget still applies only to non-root additions.

## Coverage and authority checks

- Assert the template no longer contains the `Definition Coverage` panel, `coverageRows`, or table-population code.
- Assert `normalizeCanonical` still consumes canonical coverage, the coverage metric still reports total/specified/verification-contract-covered counts, and artifact detail still exposes coverage meaning.
- Generate before and after the presentation change from the same clean repository and assert `dashboard-data.json` and its snapshot SHA-256 remain unchanged.
- Confirm the UI never converts complete definition coverage into `verified`, `released`, `compliant`, a percentage score, or a health grade.
- Assert generated `dashboard-data.json`, embedded canonical revision, provenance calculations, and snapshot SHA-256 retain the complete revision and are unaffected by its sidebar presentation.
- Assert clearing the artifact filter does not mutate embedded or standalone canonical data, change matching semantics, or invoke the all-control graph Reset behavior.
- Assert semantic color-map construction consumes only normalized node category values, produces independent deterministic maps by mode, assigns no duplicate within a current mode, and does not write category colors into canonical data.

## Static, security, and distribution checks

- The only runtime URL remains the exact accepted `3d-force-graph@1.79.0` resource; CSP and no-fetch/no-WebSocket controls remain unchanged.
- Repository strings remain inert and cannot select executable behavior, paths, URLs, or markup; revision abbreviation is gated by an exact full-hash format test, and unknown category values can select only a deterministic color-map entry rather than arbitrary style content.
- The clear control uses native button semantics, updates through the established search-render path, and introduces no inline repository-derived markup, URL, storage, telemetry, or network behavior.
- The context algorithm is iterative, depth-limited, budget-limited, and cycle-safe.
- Root and canonical templates are byte-equivalent after the supported managed upgrade; the schema-2 lock records the new digest and protects both self-hosting controls.
- Installation, adoption, doctor, managed upgrade, package-data, fresh-environment, CLI, and generator regression tests pass.
- No `templates/webui/`, second snapshot schema, runtime package, persisted UI state, or generated repository source is introduced.

## Manual assessments

At desktop and narrow width, review control placement, search/clear/Snapshot Information coexistence, clear-button enabled and disabled states, keyboard operation, returned input focus, focus visibility, readable match/context/truncation text, non-color distinction, distinct and stable state/type/assurance colors, selected-node emphasis, graph fit/reset, inspector clearing, focused-Lineage navigation, repository-status containment, full-revision accessibility, and non-authoritative revision wording. Confirm that removing the large coverage table materially shortens the Overview without making definition coverage disappear or look like commit-bound assurance.

## Evidence retention

Retain exact commands and exit codes, test counts, fixture graphs and expected sets, search/clear state cases, focus and preserved-control observations, revision fixtures and full/presented values, changed paths, managed transaction output, template and snapshot hashes, full-suite results, browser widths, depth screenshots or observations, truncation and accessibility review, sidebar containment, CDN-failure behavior, consumer-install parity, deviations, and residual risks under `docs/engineering/harness-distribution/evidence/WO-DST-011-verification.md`.

## Residual uncertainty

Bounded deterministic membership does not guarantee an aesthetically stable 3D force layout or universal comprehensibility for every dense repository. The context budget, explicit truncation, focused Lineage route, textual counts, and manual representative review constrain but do not eliminate that uncertainty.
