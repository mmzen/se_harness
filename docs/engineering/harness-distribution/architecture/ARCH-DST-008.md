+++
id = "ARCH-DST-008"
type = "architecture"
title = "Direct canonical-snapshot Explorer architecture"
status = "implemented"
owners = ["technical-owner", "security-owner"]
created = "2026-08-13"
updated = "2026-08-13"

[relations]
addresses = ["REQ-DST-029", "REQ-DST-031", "REQ-DST-032", "REQ-DST-033"]
conforms_to = ["SPEC-DST-008"]

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
- The browser presentation owns only bounded in-memory view models, navigation, filtering, and visualization. It loads the pinned `3d-force-graph` bundle for the Overview topology and retains embedded non-3D views when that load fails.
- The standard distribution owns canonical template copies, any reviewed local assets, managed hashes, and package parity.
- `harnessctl dashboard` continues to dispatch to the installed target-local generator and preserve its result.

## Dependency direction

Formal artifacts and Git observation feed the validator and snapshot builder. The renderer consumes the snapshot. The browser consumes the embedded snapshot. No data or decision flows from browser presentation back into formal artifacts, lifecycle state, verification capture, or release authority.

The source candidate and canonical installed-template copy are reconciled under existing managed ownership. Target repositories do not depend on this checkout or a hosted application, but viewing the optional 3D topology currently depends on `unpkg.com` serving the pinned library URL.

## Data and control flow

```text
repository artifacts + Git observation
  -> validator and deterministic snapshot builder
  -> harness-dashboard-snapshot-v1
  -> safe deterministic HTML embedding
  -> bounded browser view models
  -> original Overview / Lineage / Readiness composition
  -> optional CDN-backed 3D topology plus local semantic fallback
  -> the five Explorer questions
```

`dashboard-data.json` remains the verification-hashed payload. Run metadata flows separately to `generation-summary.json`.

## Trust boundaries

Repository metadata, prose, paths, evidence, experiments, and Git observations are untrusted. They remain inert data throughout serialization and DOM construction and are never sent to the CDN. The public CDN and returned JavaScript are outside the repository trust boundary: the pinned version narrows accidental drift but does not provide content-addressed integrity, availability, privacy, or compromise protection. Executable repository markup remains prohibited.

## Required patterns

- Direct consumption of `harness-dashboard-snapshot-v1`.
- One sentinel with deterministic context-safe JSON escaping.
- Text-safe DOM construction and bounded graph algorithms.
- Explicit visual and textual distinction for authority, derivation, absence, and history.
- Transactional output and managed/package parity.
- Preserve the reviewed prototype composition and canonical artifact-type strings.
- Load only the exact pinned `3d-force-graph@1.79.0` URL.
- Local fallback that retains all non-3D semantics when the optional visualization cannot run.

## Prohibited patterns

- A persisted WebUI-specific graph, metrics, lineage, or readiness schema.
- A timestamp in canonical snapshot data.
- Runtime CDN other than the exact accepted `3d-force-graph@1.79.0` URL; hosted API, telemetry, npm install, or remote font requirement.
- Aggregate confidence or health scoring.
- Inferring verified, released, covered, authoritative, or satisfied state in presentation code.
- Dropping unknown types, rich finding fields, provenance, supersession, evidence, or experiments.

## Quality attributes and conformance

The architecture prioritizes semantic fidelity, prototype fidelity, deterministic evidence, hostile-input safety, graceful degradation, accessibility, explainability, and distributable parity. Complete offline 3D availability is explicitly not guaranteed. `ADR-DST-008` records both the model-boundary decision and accepted CDN risk. `VER-DST-008` verifies contract mapping, determinism, escaping, bounded behavior, five-question coverage, exact artifact-type presentation, the permitted network boundary, fallback behavior, accessibility, managed integrity, and fresh-install parity.

## Related ADRs

`ADR-DST-008` decides this architecture.
