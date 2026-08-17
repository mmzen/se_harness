+++
id = "WO-DST-012"
type = "work_order"
title = "Restructure Explorer Lineage navigation"
status = "implemented"
owners = ["engineering-owner", "product-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[assurance]
commit_bound_verification = "required"
rationale = "The distributed Explorer can influence human understanding of formal relation direction, artifact context, assurance boundaries, and release lineage; omitted or misrepresented neighbors, reversed relations, or misleading visit history could cause incorrect reassessment and governance decisions."
decided_by = "repository-owner"

[relations]
implements = ["REQ-DST-040", "REQ-DST-041"]
specifications = ["SPEC-DST-011"]
verification = ["VER-DST-011"]
+++

# Work Order: Restructure Explorer Lineage navigation

## Lifecycle

After `WO-DST-011` was verified and its pull request merged on 2026-08-16, the repository owner requested a separate artifact packet for the previously discussed Lineage evolution. The owner had accepted the challenged product direction: use a deterministic `Lineage board` rather than literal Kanban, preserve exact formal relation semantics, and add non-hierarchical reversible navigation. On 2026-08-16 the owner explicitly authorized implementation with `go for implementation`; start preflight passed with the governing definitions and work order approved. Initial implementation review then identified that the 30-visit bound was too large and that the current visit could remain outside the horizontally rendered history area after append, Back, Forward, or Return to initial. The owner requested a 20-entry sliding window and automatic current-visit reveal. The canonical implementation, managed copy, tests, browser interaction, and retained evidence now implement that correction, so the work order is `implemented`.

Commit-bound verification remains required. Candidate commit, VREC preparation or transition, pull request, merge, release selection, public-demonstrator publication, package publication, and deployment remain separate decisions.

Code changes and retained evidence are authorized only within this work order. Candidate commit, VREC preparation or transition, pull request, merge, release selection, public-demonstrator publication, package publication, and deployment remain separate decisions.

## Objective

Make focused Explorer Lineage readable and safely explorable by replacing its rank-based free-positioned graph with a deterministic conceptual-stage/exact-type board, preserving authoritative directed relations, and adding bounded Back/Forward/visited-item navigation that cannot be confused with formal lineage.

## In scope

- Replace the current two-hop/nine-card rank layout with the stage/type board and exact mapping in `SPEC-DST-011`.
- Include the selected artifact and all direct resolved neighbors by default; add a separate depth-2 option with the deterministic 100-node non-direct budget and explicit truncation.
- Preserve exact artifact IDs, titles or statements, exact types, lifecycle states, relation names, direction, declared/derived authority, and unresolved direct-relation reporting.
- Emphasize selected/direct/second-level scope without relying on color and keep complete relation, evidence, and artifact-detail routes.
- Add a labeled in-memory Navigation history with Back, Forward, visit chips, Return to initial, branch-after-back behavior, a 20-entry sliding-window bound, automatic current-visit reveal without page scroll or focus theft, and accessible current/disabled/unavailable states.
- Reconcile the canonical template into the active managed copy through the supported managed candidate/upgrade transaction and update the applicable lock digest.
- Add focused deterministic board, scope, relation, history, security, accessibility-contract, managed-parity, and regression tests.
- Retain implementation and verification evidence keyed to `WO-DST-012`.

## Out of scope

- Changing Overview content, its 3D topology, filters, context depth, semantic colors, or the accepted CDN URL/risk boundary.
- Changing `harness-dashboard-snapshot-v1`, generator data, formal relations, artifact schemas or types, lifecycle states, validation, inspection, coverage, findings, readiness, revision provenance, VREC/RLS meaning, CLI behavior, or exit codes.
- Treating conceptual columns as a required lifecycle, reversing relations for aesthetics, fabricating missing-target artifacts, dropping direct neighbors, silently truncating, or deriving governance meaning from presentation.
- Persisting visit history in the snapshot, URL, browser history, storage, cookies, analytics, repository state, evidence, or formal graph.
- Adding server-side search, telemetry, another runtime package, a second UI schema, another design-source directory, or public Pages deployment.
- Modifying or republishing historical generated dashboards or the v0.4.0 release payload.

## Architecture applicability

No architecture or ADR relation is selected. `REQ-DST-040` and `REQ-DST-041` refine presentation inside the existing `ARCH-DST-008` browser component and accepted `ADR-DST-008` canonical-snapshot/CDN boundary, but that architecture does not declare that it addresses these routine requirements. The work introduces no new architecturally significant driver.

Stop and amend the packet if implementation requires a canonical data or generator change, persisted navigation, URL/browser-history ownership, a new dependency or network request, a trust-boundary change, a deployment change, or revision of the accepted CDN decision.

## Authorized decision envelope after approval

The implementation agent may choose the concrete HTML/CSS board structure, group descriptions, board spacing, connector routing, label placement for secondary relations, narrow-width stacking, dense-lane overflow treatment, selected/direct/context visual tokens, focus-restoration mechanics, and concise accessible wording within `SPEC-DST-011`. It must preserve the exact stage/type mapping, depth values, numeric bounds, complete direct scope, relation direction/authority, visit-history semantics, safe rendering, managed ownership, and current visual identity.

## Constraints

- Preserve Python 3.11+ standard-library repository behavior and target-local static dashboard generation.
- Treat every repository string as untrusted inert data.
- Keep `templates/repository/standard/scripts/harness_explorer/index.template.html` as the sole reusable source and the active root copy byte-equivalent.
- Use the supported schema-2 managed transaction; do not hand-edit the lock or adopt a modified active managed copy as canonical.
- Preserve unrelated work and historical formal records.
- Do not deploy or mutate the public demonstration under this work order.

## Expected change surface

- `templates/repository/standard/scripts/harness_explorer/index.template.html`
- `scripts/harness_explorer/index.template.html`
- `.engineering-harness.lock`, limited to the managed template digest produced by the supported upgrade
- `tests/test_dashboard_webui.py` and only directly applicable managed/package/browser-contract tests
- the DST-012 packet, domain index, and `docs/engineering/harness-distribution/evidence/WO-DST-012-verification.md`

No generator, CLI, workflow, package metadata, public Pages workflow, architecture, ADR, or other managed file is expected to change. Stop if implementation demonstrates otherwise.

## Required verification

Execute every applicable case in `VER-DST-011` plus relevant regression cases from `VER-DST-008` and `VER-DST-010`. At minimum run formal validation; start and review preflight; focused Explorer tests; complete standard-library tests; doctor; supported managed-upgrade plan/apply/idempotence; active/canonical parity; twice-generated canonical snapshot comparison; all-type, unknown-type, directed/cyclic/parallel/unresolved/dense graph fixtures; depth and budget checks; complete navigation transition and 20/21-entry tests; automatic reveal at both history edges with page-scroll and focus preservation; JavaScript/browser-load checks; desktop, narrow, keyboard, focus, scroll, detail, and non-color manual review; CDN-failure fallback; fresh-install or package-data parity; and `git diff --check`.

## Evidence to record

Retain exact authorization, requirement mapping, commands and exit codes, test counts, fixture inputs and expected board scopes, stage/type map output, direct and second-level counts, relation identities, truncation observations, history transition tables, bound and unavailable-entry behavior, keyboard/focus/accessibility review, canonical/template/lock hashes, managed transaction, CDN fallback, consumer isolation, changed paths, deviations, residual risks, and deployment status in `docs/engineering/harness-distribution/evidence/WO-DST-012-verification.md`.

## Stop and escalate conditions

Stop if a direct neighbor would be hidden; type or relation terminology would be renamed; visual order would reverse authority; context cannot remain deterministic and bounded; history would need persistence or imply formal lineage; connector loss would remove the only relation route; schema, generator, CLI, validator, workflow, package, network, dependency, CSP, trust, architecture, or deployment boundaries must change; managed customization would be overwritten; tests fail; or any commit, VREC, PR, release, publication, or deployment action lacks explicit authority.

## Completion report format

Report requirement mapping, board and stage/type behavior, visible-scope and depth semantics, direct-neighbor completeness, relation-direction and authority preservation, navigation transitions and bounds, accessibility and responsive behavior, active/canonical/lock parity, tests and browser review, canonical and template hashes, changed paths, deviations, residual risks, and public-demonstrator status.
