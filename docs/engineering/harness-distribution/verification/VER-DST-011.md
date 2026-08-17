+++
id = "VER-DST-011"
type = "verification"
title = "Verify structured and reversible Explorer Lineage"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
verifies = ["REQ-DST-040", "REQ-DST-041"]
+++

# Verification Contract: Verify structured and reversible Explorer Lineage

## Independence

Expected stage/type membership, artifact terminology, relation direction and authority, traversal depth and budget, history semantics, and authority boundaries come from `REQ-DST-040`, `REQ-DST-041`, `SPEC-DST-011`, the canonical snapshot contract, and existing Explorer security/distribution contracts - not from implementation-specific card coordinates, CSS selectors, connector curves, or state-variable names.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| `REQ-DST-040` | deterministic scope/layout fixtures, static template checks, browser interaction, accessibility review, and canonical-output comparison | every current type, unknown/missing type, inbound/outbound/reverse/same-stage/self/parallel relations, declared/derived authority, cycles, unresolved targets, dense direct neighbors, bounded second-level context, CDN failure, narrow width | groups and sublanes are correct and deterministic; selected plus every direct neighbor remains visible; depth-two additions are deterministic and capped at 100; truncation is explicit; cards and relations retain canonical meaning; detail routes and fallback remain usable |
| `REQ-DST-041` | browser-state model tests, DOM/accessibility assertions, keyboard interaction, and reload/external-entry cases | `A -> B -> C`, back/forward, chip jump, branch after back, current reselection, non-consecutive revisit, return to initial, 20/21 visits, current-visit reveal at both scroll edges, unavailable ID, external entry, reload | cursor and branch semantics are exact and bounded; current/disabled/unavailable states are accessible; the current visit is fully visible without page scroll or focus theft; external entry resets; return remains available; no visit is represented or persisted as formal lineage |

## Acceptance scenarios

- Focus a requirement connected to purpose, definition, design, delivery, assurance, and release artifacts; confirm every card uses the prescribed group and exact-type sublane and remains sorted by ID.
- Focus an artifact with inbound and outbound relations that run both with and against stage order; confirm every arrow and relation label preserves canonical source, target, name, and authority.
- Render declared and derived relations between the same artifacts; confirm both remain distinguishable and available in the Relations detail.
- Render an unknown artifact type and a malformed missing type; confirm neither disappears or is renamed into a current formal type.
- At depth 1, confirm the root and all direct resolved neighbors are present even when their count exceeds 100.
- At depth 2, use more than 100 eligible non-direct nodes; confirm all depth-1 artifacts remain, exactly the deterministic first 100 non-direct IDs are added, and visible/omitted counts report truncation.
- Select `A`, `B`, and `C`; exercise Back, Back, Forward, then select `D`; confirm the current artifact and resulting `A`, `B`, `D` branch.
- Select the current artifact repeatedly and confirm no consecutive duplicate; revisit an older artifact after other visits and confirm the non-consecutive visit is retained.
- Create 21 distinct visits and confirm the bound, cursor, accessible announcement, and separate Return to initial behavior.
- Extend history beyond its visible width, then exercise append, Back, Forward, an older chip, and Return to initial; confirm the current chip is fully visible after each action, the list scrolls toward both edges as needed, document/board scroll is unchanged, and card/control focus follows the specified action rather than the reveal operation.
- Open Lineage from a different Overview artifact and confirm a new depth-1 session rather than an accidental extension of the former visit trail.
- Block the optional CDN and confirm Overview reports its explicit failure while the Lineage board, navigation, relation details, evidence, readiness, and provenance remain usable.

## Deterministic board and graph fixtures

Exercise all 12 current formal artifact types, multiple artifacts per sublane, missing stages, unknown types, disconnected nodes, directed chains, inbound-only roots, outbound-only roots, reverse-stage relations, same-group and same-sublane relations, self-relations, duplicate and parallel relations, declared and derived authority, unresolved targets, cycles, and deliberately shuffled artifact/relation input.

For identical normalized content, selected ID, and depth, assert identical visible artifact IDs, group/type placement, card order, visible relation identities, direct/context roles, truncation state, and history-independent board model. Connector pixel paths may vary with responsive dimensions but must not change the semantic relation set.

For a fixture with 150 direct neighbors and 150 additional second-level candidates, assert that depth 1 retains all 151 root/direct artifacts and depth 2 retains those plus exactly 100 deterministic non-direct artifacts. Confirm the report identifies 50 omitted second-level artifacts and never describes direct artifacts as truncated.

## Navigation state tests

- Model zero, one, and multiple retained entries; assert Back/Forward enabled states and current cursor.
- Jump to an earlier history chip, move forward, and select a new card; assert forward-branch truncation occurs only on the new selection.
- Exercise repeated IDs at current and non-current positions; assert only consecutive current reselection is suppressed.
- Cross the 20-entry bound from different cursor positions and assert the current entry is never removed, indices remain valid, and Return to initial still resolves or appends through the ordinary bounded rule.
- With history wider than its viewport, assert the current chip lies completely within the history-list bounds after append, Back, Forward, chip jump, and Return to initial; assert only the list's horizontal scroll position changes for reveal.
- Inject an unavailable retained ID and assert no fallback artifact is substituted.
- Assert external entry resets history/depth while internal card and relation selection appends.
- Reload the page and assert no history is recovered from URL, browser history, storage, cookies, snapshot, or repository state.
- Assert history chips and controls do not create connector edges, relation rows, findings, evidence, or canonical output.

## Static, security, and architecture checks

- Assert the current rank-based free-positioned two-hop/nine-node contract is removed and the fixed group/type map, depth `1 / 2`, 100 non-direct budget, and 20-visit bound are present once in the canonical implementation.
- Assert exact artifact-type labels and relation fields are consumed from normalized canonical data and unknown values remain inert text.
- Assert dynamic artifact, relation, missing-target, and history text cannot create markup, style, selectors, URLs, scripts, storage keys, or executable behavior.
- Assert traversal and history algorithms are iterative, cycle-safe, and bounded; no force simulation or new dependency is used for Lineage.
- Assert the only runtime URL remains the accepted `3d-force-graph@1.79.0` URL used by Overview; CSP, no-fetch/no-WebSocket controls, and CDN fallback remain unchanged.
- Confirm no canonical schema, generator, validator, CLI, workflow, readiness, VREC/RLS, architecture, or ADR behavior changes.
- Generate dashboard data twice from identical repository state and assert byte-identical `dashboard-data.json`, snapshot SHA-256, artifact list, relations, readiness, findings, and provenance. Presentation-only HTML changes are expected.

## Distribution and regression checks

- The canonical standard template and active managed copy are byte-equivalent after the supported managed candidate/upgrade transaction, and the schema-2 lock contains the resulting digest without unrelated managed-file changes.
- Installation, adoption, doctor, safe upgrade plan/apply/idempotence, package data, fresh-environment CLI, dashboard generation, and public-demonstrator generation remain valid.
- Relevant `VER-DST-008` and `VER-DST-010` regression cases pass, including safe snapshot embedding, exact artifact types, relation authority, detail tabs, Overview topology and filters, Readiness, responsive behavior, and CDN failure.
- Formal validation, start/review preflight, focused Explorer tests, complete standard-library tests, JavaScript syntax/load checks, and `git diff --check` pass.

## Manual assessments

At desktop and narrow widths, review stable stage comprehension, horizontal or stacked navigation, dense sublanes, card readability, selected/direct/context distinction, connector direction, relation-label access, declared/derived distinction, unresolved-relation reporting, scroll behavior, keyboard card selection, focus restoration, Back/Forward/chips/Return controls, history-bound announcement, detail tabs, and non-color interpretation. Confirm the history looks like visited navigation rather than a hierarchy or governed artifact path.

## Evidence retention

Retain exact commands and exit codes, test counts, fixture inputs and expected scopes, stage/type placement output, relation sets, depth/truncation results, history transition tables, 20/21-entry and current-reveal behavior, accessibility and responsive observations, focus and scroll behavior, CDN-failure result, canonical snapshot hashes, managed transaction output, active/canonical template hashes, changed paths, deviations, and residual risks under `docs/engineering/harness-distribution/evidence/WO-DST-012-verification.md`.

## Residual uncertainty

A deterministic board cannot make every dense formal graph immediately simple. Very large direct neighborhoods remain complete and may require scrolling, while connector routing can still overlap. Stable lanes, direct-relation emphasis, explicit counts, authoritative relation details, responsive/manual review, and bounded optional context reduce but do not eliminate that usability uncertainty.
