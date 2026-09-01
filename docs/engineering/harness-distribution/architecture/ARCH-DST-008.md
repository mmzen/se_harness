+++
id = "ARCH-DST-008"
type = "architecture"
title = "Direct canonical-snapshot Explorer architecture"
status = "implemented"
owners = ["technical-owner", "security-owner"]
created = "2026-08-13"
updated = "2026-09-01"

[relations]
addresses = ["REQ-DST-029", "REQ-DST-031", "REQ-DST-033", "REQ-DST-067", "REQ-DST-068"]
conforms_to = ["SPEC-DST-023"]

[decision_assessment]
outcome = "adr_required"
triggers = ["responsibility-or-dependency-direction", "public-interface-or-protocol", "security-privacy-or-trust-boundary", "technology-framework-vendor-or-external-service", "cross-cutting-policy"]
rationale = "Selecting the canonical snapshot boundary, controlling presentation derivation, removing a runtime CDN, and preserving managed distribution integrity materially affect interfaces, dependency direction, trust, and cross-cutting provenance policy."
assessed_by = "technical-owner"
+++

# Architecture: Direct canonical-snapshot Explorer architecture

## Context and scope

Harness Explorer is a static view over validator-derived repository state. The reviewed WebUI prototype introduced both a second data shape and a CDN-backed 3D renderer. This architecture keeps the existing canonical snapshot as the only data boundary, adapts it in browser memory to the original page modules, and retains the prototype's pinned external renderer as an explicitly accepted optional presentation dependency.

## Components and responsibilities

- The validator owns formal graph diagnostics and never delegates authority to the UI.
- The snapshot builder owns deterministic normalization, derived findings, definition coverage, readiness observations, revision provenance, supersession, experiments, and evidence indexes.
- The renderer owns deterministic safe embedding into one managed HTML template.
- The browser presentation owns only bounded in-memory view models, navigation, filtering, and visualization: a shell that verifies every resource it parses, the designed Overview, Lineage, Virtual Twin, and record components on a vendored component runtime and React, and the Readiness view. Everything the page executes ships inside the document.
- The standard distribution owns canonical template copies, any reviewed local assets, managed hashes, and package parity.
- `harnessctl dashboard` continues to dispatch to the installed target-local generator and preserve its result.

## Dependency direction

Formal artifacts and Git observation feed the validator and snapshot builder. The renderer consumes the snapshot. The browser consumes the embedded snapshot. No data or decision flows from browser presentation back into formal artifacts, lifecycle state, verification capture, or release authority.

The canonical standard-distribution template and active managed root copy are reconciled under existing managed ownership. Target repositories do not depend on this checkout or a hosted application, and the page requests no third-party origin.

## Data and control flow

```text
repository artifacts + Git observation
  -> validator and deterministic snapshot builder
  -> harness-dashboard-snapshot-v1
  -> safe deterministic HTML embedding
  -> bounded browser view models
  -> designed Overview / Lineage / Virtual Twin / Readiness views and the record panel
  -> the five Explorer questions
```

`dashboard-data.json` remains the verification-hashed payload. Run metadata flows separately to `generation-summary.json`.

## Trust boundaries

Repository metadata, prose, paths, evidence, experiments, and Git observations are untrusted. They remain inert data throughout serialization and DOM construction and are never sent to the CDN. No third-party origin participates at runtime; the vendored runtime and React builds are digest-verified at build time and evaluated as the template's own sources, never with repository text.

## Required patterns

- Direct consumption of `harness-dashboard-snapshot-v1`.
- One sentinel with deterministic context-safe JSON escaping.
- Text-safe DOM construction and bounded graph algorithms.
- Explicit visual and textual distinction for authority, derivation, absence, and history.
- Transactional output and managed/package parity.
- Preserve the designed composition as retained sources rebuilt by one deterministic build, and canonical artifact-type strings.
- Name and request no remote origin; contain every resource failure to its view.

## Prohibited patterns

- A persisted WebUI-specific graph, metrics, lineage, or readiness schema.
- A timestamp in canonical snapshot data.
- Any runtime CDN, hosted API, telemetry, npm install, remote font, or persistent browser storage.
- Aggregate confidence or health scoring.
- Inferring verified, released, covered, authoritative, or satisfied state in presentation code.
- Dropping unknown types, rich finding fields, provenance, supersession, evidence, or experiments.

## Quality attributes and conformance

The architecture prioritizes semantic fidelity, prototype fidelity, deterministic evidence, hostile-input safety, graceful degradation, accessibility, explainability, and distributable parity. The page is complete offline. `ADR-DST-008` records both the model-boundary decision and accepted CDN risk. `VER-DST-008` verifies contract mapping, determinism, escaping, bounded behavior, five-question coverage, exact artifact-type presentation, the permitted network boundary, fallback behavior, accessibility, managed integrity, and fresh-install parity.

## Dependency reassessment: 2026-08-16

The technical and security owners reassessed this architecture against the 2026-08-15 revision of `SPEC-DST-008`. That revision removed the redundant `templates/webui/` handoff and made `templates/repository/standard/scripts/harness_explorer/index.template.html` the sole reusable Explorer source, with the active root file retained as its managed operational copy.

This consolidation strengthens the architecture's existing single-model and managed-distribution boundaries. It does not change the canonical snapshot interface, browser data flow, DOM safety rules, external CDN trust boundary, non-3D fallback, accessibility obligations, or the risk accepted by `ADR-DST-008`. The architecture remains applicable; only the formerly ambiguous source-copy sentence was corrected.

## Related ADRs

`ADR-DST-008` decides this architecture.

## Amendment record

**The presentation component becomes the designed self-contained page and the
CDN dependency is removed, amended 2026-09-01 under `WO-DST-023` (`SPEC-DST-023`,
`ADR-DST-013`).** The snapshot boundary, dependency direction from formal
artifacts to presentation, safe embedding, transactional output, and
managed parity are unchanged. The addressed requirements follow the
supersession of `REQ-DST-032` by `REQ-DST-067` and add `REQ-DST-068`; the
conformance target follows the supersession of `SPEC-DST-008` by
`SPEC-DST-023`. `ADR-DST-008` continues to decide the snapshot boundary;
`ADR-DST-013` decides the self-contained presentation.
