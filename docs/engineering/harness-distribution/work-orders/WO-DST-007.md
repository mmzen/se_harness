+++
id = "WO-DST-007"
type = "work_order"
title = "Integrate the canonical Harness Explorer WebUI"
status = "implemented"
owners = ["engineering-owner", "quality-owner", "security-owner"]
created = "2026-08-13"
updated = "2026-08-13"

[relations]
implements = ["REQ-DST-029", "REQ-DST-030", "REQ-DST-031", "REQ-DST-032", "REQ-DST-033"]
specifications = ["SPEC-DST-008"]
architecture = ["ARCH-DST-008", "ADR-DST-008"]
verification = ["VER-DST-008"]
+++

# Work Order: Integrate the canonical Harness Explorer WebUI

## Lifecycle

The accountable repository owner reviewed the proposed WebUI alignment and its formal packet, then explicitly instructed `go implementation` on 2026-08-13. That human decision approves this bounded work order and its governing requirements, specification, architecture, ADR, and verification contract.

Use `implemented` only after the integrated implementation and retained evidence are complete. Commit-bound verification, commit, push, pull request, release selection, publication, and deployment remain separate decisions.

## Objective

Reconcile the user-provided WebUI design materials with the current harness model, then integrate the original page structure, look and feel, responsive behavior, and CDN-backed 3D interaction as the managed Harness Explorer without changing the canonical snapshot, validator authority, deterministic provenance, or CLI ownership boundary.

## In scope

- Preserve and review the existing user-owned files under `templates/webui/`; reconcile their handoff, manifest, brand contract, data documentation, schema documentation, and prototype to `SPEC-DST-008`.
- Remove the incompatible WebUI-specific persisted schema and describe direct use of `harness-dashboard-snapshot-v1`.
- Remove missing asset references; retain only the original exact `3d-force-graph@1.79.0` unpkg dependency and document its accepted risk.
- Preserve the original sidebar, Overview/Lineage/Readiness layout, controls, 3D topology, typography, colors, spacing, and responsive behavior.
- Adapt Overview, Lineage, and Readiness presentation so all five current Explorer questions and canonical semantic fields remain reachable.
- Integrate the selected presentation into `scripts/harness_explorer/index.template.html` and its canonical standard-template copy.
- Change `scripts/generate_harness_dashboard.py` and its canonical copy only where required for safe asset rendering or integration; preserve snapshot construction and deterministic serialization unless a defect prevents conformance.
- Keep `se_harness/cli.py` as target-local generator dispatch unless tests reveal an integration defect that cannot be fixed within the managed generator boundary.
- Add deterministic model, rendering, security, accessibility-contract, distribution, installer, upgrade, doctor, package-parity, and regression tests.
- Update managed locks, package inventories, and template parity only where the final local asset set requires it.
- Retain work-order-keyed evidence.

## Out of scope

- Changing formal artifact types, relation vocabulary, lifecycle transitions, decision rights, validator acceptance, quality-gate meaning, readiness authority, VREC capture fields, release eligibility, or supersession rules.
- Replacing or versioning `harness-dashboard-snapshot-v1`.
- Adding an aggregate health, confidence, compliance, verification, or release score.
- Adding a hosted dashboard, telemetry, repository mutation from the UI, npm build, runtime package manager, installation profile, external service, or runtime dependency beyond the exact accepted `3d-force-graph` URL.
- Rewriting repository-owned formal artifacts or customized managed files.
- Changing historical VREC or release facts.
- Commit, push, pull request, merge, release contract, VREC, release record, tag, wheel, publication, or deployment authority.

## Authorized decision envelope

The implementation agent may choose the canonical-to-view in-memory adapter, bounded traversal limits, test fixture organization, and small additions needed to expose current model sections. It must preserve the prototype's CSS structure, visual tokens, responsive breakpoints, page composition, and 3D renderer except where a model-fidelity, accessibility, deterministic, or security correction is necessary.

The agent may not introduce a second persisted schema, omit a canonical field to preserve the mockup, exclude or rename an artifact type, infer authority, add a score, perform runtime access beyond the exact accepted CDN URL, or weaken transactional managed-file behavior. If preserving a prototype feature requires one of those changes, stop and escalate.

## Constraints

- Preserve Python 3.11+ standard-library runtime behavior.
- Treat repository data, target paths, templates, and asset metadata as untrusted.
- Preserve unrelated staged and unstaged user changes; inspect the exact index and worktree diff before every commit proposal.
- Keep root and canonical managed copies synchronized where required.
- Do not build a promotable distribution without separate release authority.
- Keep every non-3D evidence view usable without external network access; full 3D operation may use only the accepted pinned CDN URL.

## Expected change surface

WebUI design inputs under `templates/webui/`; the Explorer HTML template; the generator only if integration requires it; canonical copies under `templates/repository/standard/`; managed lock and package data only for final asset parity; focused and regression tests; harness-distribution index; and retained `WO-DST-007` evidence.

## Required verification

Execute every check in `VER-DST-008`. At minimum run formal graph validation, start and review preflight, doctor, focused dashboard and distribution tests, the complete standard-library suite, twice-generated snapshot comparison, hostile-input rendering cases, root/canonical equality, package-data inspection, fresh init/adopt/upgrade fixtures, CLI help and dispatch checks, narrow-width and keyboard review, local-link and missing-asset inspection, and `git diff --check`.

## Evidence to record

Retain exact commands and exit codes, Python versions, test counts, model-field mapping, artifact/relation type coverage, snapshot and rendered-output hashes, hostile inputs, runtime request observations, browser widths, keyboard and non-color review, asset provenance and checksum if applicable, managed/package parity, installed-repository results, changed paths, deviations, and residual risks in `docs/engineering/harness-distribution/evidence/WO-DST-007-verification.md`.

## Stop and escalate conditions

Stop if the canonical snapshot must change; model fidelity conflicts with an approved artifact; the UI would imply authority, hide a material field, or exclude/rename an artifact type; safe embedding or bounded rendering cannot be demonstrated; any runtime dependency beyond the accepted URL appears necessary; owner content would be overwritten; managed/package parity cannot be preserved; a required test fails; or the work needs commit, release, external-service, or governance authority beyond this work order.

## Completion report format

Report requirement mapping, design-material reconciliation, model and authority invariants, implementation and managed-copy changes, tests and manual review, exact output hashes, asset disposition, deviations, residual risks, and the bounded candidate path set.

## Implementation result

The canonical WebUI integration was corrected after owner review. The active, canonical, and prototype templates preserve the original prototype's sidebar, Overview/Lineage/Readiness composition, visual system, responsive behavior, and CDN-backed 3D topology. An in-memory adapter consumes `harness-dashboard-snapshot-v1` without a second persisted schema; artifact types remain dynamically discovered and displayed with their canonical strings. All five Explorer questions, definition coverage, typed relations, exact readiness states, commit provenance, supersession, evidence, and experiments remain available. No generator or CLI semantic change was required.

The only runtime dependency is the exact versioned unpkg URL recorded in `ADR-DST-008`; its availability, metadata-disclosure, and non-content-addressed supply-chain risks are explicitly accepted for this candidate. A clear fallback preserves every non-3D evidence view. Formal validation, managed-integrity doctor, focused security/model/CDN-boundary tests, the complete standard-library suite, deterministic dashboard generation, JavaScript parsing, desktop and narrow browser review, fallback inspection, package-template discovery, and diff hygiene are retained in `docs/engineering/harness-distribution/evidence/WO-DST-007-verification.md`. Commit, VREC capture, assurance transition, release, push, publication, and deployment remain separate decisions.
