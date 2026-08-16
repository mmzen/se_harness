+++
id = "WO-DST-011"
type = "work_order"
title = "Refine Explorer Overview navigation"
status = "implemented"
owners = ["engineering-owner", "product-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[assurance]
commit_bound_verification = "required"
rationale = "The distributed Explorer can influence human understanding of requirement coverage, graph impact, and observed provenance; incorrect filtering, hidden roots, nondeterministic truncation, semantic drift, or ambiguous revision presentation could mislead later review and upgrade decisions."
decided_by = "repository-owner"

[relations]
implements = ["REQ-DST-035", "REQ-DST-036", "REQ-DST-037", "REQ-DST-038", "REQ-DST-039"]
specifications = ["SPEC-DST-010"]
verification = ["VER-DST-010"]
+++

# Work Order: Refine Explorer Overview navigation

## Lifecycle

The repository owner requested the artifact packet on 2026-08-16 after reviewing and accepting the challenged proposal to remove the large Definition Coverage listing and add bounded `0 / 1 / 2` graph context. During definition, the owner also accepted compact non-authoritative observed-revision presentation, generic sidebar containment, and a direct artifact-filter clear control within the same cohesive Explorer change. On 2026-08-16 the owner explicitly authorized implementation with `ok go for implementation of work order WO-DST-011`; start preflight passed and the bounded implementation reached review. Before candidate commit, the owner identified duplicate semantic colors and requested a correction; `REQ-DST-039`, `SPEC-DST-010`, and `VER-DST-010` were amended to require stable distinct category colors in each analysis mode. The corrected implementation and retained evidence are complete, and the work order is `implemented`. Commit-bound verification remains a later decision over an exact candidate commit.

Commit-bound verification is required. Candidate commit, VREC preparation or transition, pull request, merge, release selection, public-demonstrator publication, package publication, and deployment remain separate decisions.

## Objective

Make the Explorer Overview shorter, its filtered topology easier to navigate, and its bounded repository status legible by removing the exhaustive coverage table, adding deterministic context around filter matches, providing a direct text-filter clear action, assigning stable distinct colors within each analysis mode, and abbreviating valid observed revisions only for presentation, without changing canonical evidence, provenance identity, relation authority, focused Lineage, security, distribution, or historical release behavior.

## In scope

- Remove the exhaustive Definition Coverage panel and its presentation-only renderer from the active and canonical Explorer templates.
- Preserve the compact coverage metric, canonical snapshot coverage, and artifact-level coverage detail.
- Add the exact depth `0 / 1 / 2` control and deterministic match/context projection specified by `SPEC-DST-010`.
- Add explicit match, context, visible-relation, depth, and truncation text and non-color node distinction.
- Present valid full SHA-1 and SHA-256 revisions as a 12-character-plus-ellipsis observed-revision label in the bounded sidebar while preserving full canonical and accessible values.
- Add generic containment for long untrusted repository-status text at supported widths, without treating shortened values as identity.
- Add a stable accessible clear button beside the artifact text filter that clears only that field, immediately refreshes the applicable graph scope, preserves other controls and valid selection, and returns focus to the field.
- Preserve existing graph analysis and semantic labels while replacing collision-prone color hashing with stable distinct mode-specific category maps; preserve selection, fit/reset, focused Lineage, responsive design, and CDN-failure fallback.
- Reconcile the canonical template into the active managed copy through the supported candidate/upgrade transaction and update the applicable lock entry.
- Add focused graph-scope, template, managed-parity, hostile-input, accessibility-contract, and regression tests.
- Retain implementation and verification evidence keyed to `WO-DST-011`.

## Out of scope

- Changing the canonical snapshot schema, generator data, validator, inspection, formal relations, coverage calculation, readiness gates, lifecycle states, VREC/RLS meaning, CLI behavior, or exit codes.
- Abbreviating revisions in canonical data or using a visible prefix for identity, comparison, lookup, links, manifests, digests, VREC/RLS binding, provenance, or assurance.
- Broadening search matching, persisting queries, adding search history or shortcuts, clearing unrelated controls, or replacing the existing graph Reset action.
- Arbitrary or user-entered traversal depth; more than two hops; more than 100 added context nodes; silent truncation; dropping root matches; or treating context as a filter match.
- Changing focused Lineage's traversal contract, replacing the 3D topology, modifying the accepted CDN URL or CSP boundary, or adding another runtime/network dependency.
- Introducing a health/compliance/assurance score, server-side search, analytics, telemetry, storage, a second UI schema, or a new `templates/webui/` source.
- Re-rendering or republishing the historical v0.4.0 public demonstration with candidate code.

## Architecture applicability

No new architecture artifact or ADR is selected. The change stays within the implemented `ARCH-DST-008` browser-presentation component and accepted `ADR-DST-008` boundary, without changing architecture-significant requirements. If implementation needs new generator data, a schema change, a dependency or network change, a trust-boundary change, or materially different navigation ownership, stop and amend the packet with architecture assessment.

## Authorized decision envelope after approval

The implementation agent may choose concise labels, clear-button icon treatment, control placement, responsive wrapping, match/context node sizing and opacity, truncation copy, an efficient deterministic adjacency representation, exact high-contrast palette values, and the exact observed-revision label. It must preserve all exact semantic and numeric bounds in `SPEC-DST-010`, complete revision identity, canonical artifact terminology, selected-node meaning, safe rendering, keyboard access, stable mode-specific category mapping, and the existing visual identity.

## Constraints

- Preserve Python 3.11+ standard-library repository behavior and target-local dashboard generation.
- Treat every repository string as untrusted inert data.
- Keep `templates/repository/standard/scripts/harness_explorer/index.template.html` as the sole reusable source and the active root copy byte-equivalent.
- Use the supported schema-2 managed transaction; do not hand-edit the lock or adopt a modified managed root as canonical.
- Preserve unrelated work and historical formal records.
- Do not deploy or mutate the public demonstration under this work order.

## Expected change surface

- `templates/repository/standard/scripts/harness_explorer/index.template.html`
- `scripts/harness_explorer/index.template.html`
- `.engineering-harness.lock`, limited to the managed template digest produced by the supported upgrade
- `tests/test_dashboard_webui.py` and only directly applicable managed/package/browser-contract tests
- the new DST-011 packet, domain index, and `docs/engineering/harness-distribution/evidence/WO-DST-011-verification.md`

No generator, CLI, workflow, package metadata, public Pages workflow, or other managed file is expected to change. Stop if implementation demonstrates otherwise.

## Required verification

Execute every applicable case in `VER-DST-010` plus relevant regression cases from `VER-DST-008`. At minimum run formal validation; start and review preflight; focused Explorer tests; complete standard-library tests; doctor; supported managed-upgrade plan/apply/idempotence; active/canonical parity; twice-generated snapshot comparison; hostile and dense graph fixtures; search-clear state/focus/preservation cases; SHA-1/SHA-256/non-hash/collision revision fixtures; all-mode category-color uniqueness and filter-stability cases; JavaScript/browser-load checks; desktop, narrow, keyboard, fit/reset, inspector, top-bar coexistence, sidebar-overflow, and full-revision accessibility review; CDN-failure fallback; fresh-install or package-data parity; and `git diff --check`.

## Evidence to record

Retain exact authorization, change mapping, commands and exit codes, test counts, fixture inputs and expected root/context sets, context-budget behavior, search-clear state/focus/preserved-control cases, full and presented revision fixtures, mode-specific category/color maps and filter-stability observations, template/lock/snapshot hashes, managed transaction, browser observations, coverage and provenance preservation, top-bar and sidebar containment, consumer isolation, deviations, residual risks, and deployment status in `docs/engineering/harness-distribution/evidence/WO-DST-011-verification.md`.

## Stop and escalate conditions

Stop if coverage data would be removed; a root would be hidden; type/status filters must suppress context; traversal cannot be deterministic and bounded; clearing search would reset unrelated state or change matching semantics; a revision prefix would influence identity or assurance; the full revision would become unavailable; 3D semantics or focused Lineage must be redefined; schema, generator, CLI, validator, workflow, package, network, dependency, CSP, or trust boundaries must change; managed customization would be overwritten; tests fail; or any commit, VREC, PR, release, publication, or deployment action lacks explicit authority.

## Completion report format

Report requirement mapping, removed Overview elements, preserved coverage routes, root/context/depth semantics, deterministic limits, search-clear behavior and preserved state, revision abbreviation and full-value preservation, top-bar and sidebar containment, presentation and accessibility behavior, active/canonical/lock parity, tests and browser review, snapshot and template hashes, changed paths, deviations, residual risks, and public-demonstrator status.
