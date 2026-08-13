# Harness Explorer design handoff

This handoff describes the visual implementation governed by `SPEC-DST-008`. When design material conflicts with the canonical snapshot, validator semantics, managed integrity, accessibility, or security, the approved harness artifacts win.

## Product intent

Harness Explorer helps a reviewer understand a repository without granting authority. It exposes purpose, definition coverage, reassessment impact, consistency/readiness observations, commit-bound provenance, supersession, retained evidence, and controlled outcomes.

The interface must keep five explicit reader questions:

1. Why does this exist?
2. Is the definition covered?
3. What needs reassessment?
4. What is inconsistent or unassessable?
5. Does the harness help?

Overview, Lineage, and Readiness may be used as broader visual groupings only when these questions remain directly reachable.

## Data integration

- Consume embedded `harness-dashboard-snapshot-v1` directly.
- Use the single marker `__HARNESS_SNAPSHOT_JSON__`.
- Do not require `schemaVersion`, `generatedAt`, `metrics`, `graph`, `lineage`, or a WebUI-specific readiness object.
- Derive counts, focused graph neighborhoods, and visual coordinates in browser memory.
- Keep generation time in `generation-summary.json`, never in canonical `dashboard-data.json`.
- Treat definition coverage separately from commit-bound VREC assurance.
- Preserve `satisfied`, `unsatisfied`, and `not_assessable` exactly.
- Preserve relation authority, optional derived paths, missing targets, rich findings, revision provenance, supersession, evidence, and experiments.

See `harness-dashboard-data.md` and `harness-dashboard-data.schema.json` for the contract.

## Interaction model

### Repository summary

Show graph validity, repository name, observed revision, artifact root, artifact count, relation count, definition coverage, and consistency findings. Metrics are derived observations, not an assurance score.

### Topology and lineage

Preserve the prototype's interactive 3D topology using the pinned `3d-force-graph@1.79.0` bundle loaded from unpkg. Artifact nodes are derived directly from the canonical `artifacts` array without a type whitelist; filters, inspectors, details, and labels display the canonical type string rather than substituting a smaller vocabulary. Focused lineage remains a bounded local SVG view and exact relation fields remain available in artifact details.

The selected-artifact inspector retains owners, statement, architecture traceability, decision assessment, declared commit, worktree state, version/tag, evidence, revision comparison, and supersession fields when present.

### Definition coverage and impact

Coverage lists active specifications and independent verification contracts separately. Impact lists direct inbound, direct outbound, transitive inbound, and transitive outbound connectivity and says `reassess`, never `automatically change`.

### Consistency, readiness, and provenance

Render every finding field that is present. Show each G0-G5 gate and every condition with its exact state and evidence. Display VREC and release candidates separately from the observed checkout, including lifecycle class, work coverage, contracts, checkout comparison, and explicit supersession.

### Controlled outcomes

Compare only compatible treatments from one retained trial. `null` remains `not measured`. The UI does not infer effectiveness when no experiment exists.

## Security and runtime boundary

- The only permitted runtime request is `https://unpkg.com/3d-force-graph@1.79.0/dist/3d-force-graph.min.js` for the original 3D topology.
- No repository artifact data is sent to the CDN. No other script, remote font, image, style, dynamic import, `fetch`, WebSocket, telemetry, API, or hosted service is permitted.
- The versioned URL is not content-addressed and has no retained SRI value. `ADR-DST-008` accepts the availability, request-metadata, and supply-chain risk for this candidate.
- When the CDN is blocked or unavailable, show the 3D-unavailable state and keep metrics, filters, focused lineage, definition coverage, readiness, findings, provenance, evidence, and controlled outcomes usable from embedded data.
- Do not use `innerHTML` with repository data.
- Escape embedded JSON for script context.
- Bound graph traversal and rendering for cycles or large repositories.
- Unsupported, malformed, invalid, empty, no-evidence, and no-experiment states must be visible and must not resemble success.

## Responsive and accessibility behavior

- Desktop: topology and selected-artifact inspector sit side by side.
- Medium: inspector stacks below topology; lineage and gate grids reduce columns.
- Narrow: all panels stack; tables scroll horizontally; no question disappears.
- Tab navigation supports arrow keys, Home, and End.
- SVG nodes support Enter and Space.
- Focus is visible and meaning never depends on color alone.

## Assets

- `harness-lineage-prototype.html`: generator-ready static template and visual reference.
- `harness-dashboard-data.md`: canonical data-contract explanation.
- `harness-dashboard-data.schema.json`: documentary JSON Schema.
- `brand-spec.md`: visual and semantic tokens.
- `DESIGN-MANIFEST.json`: machine-readable handoff inventory.

There are no preview PNGs or local third-party assets in this handoff. The one runtime third-party asset and its accepted risk are documented above.

## Coding checklist

1. Preserve the exact canonical snapshot and safe embedding marker.
2. Keep all five questions and all canonical semantic fields reachable.
3. Preserve the original 3D interaction and permit only the exact documented CDN bundle; verify the non-3D fallback.
4. Keep root and canonical managed templates byte-identical.
5. Verify twice-generated snapshot identity and hostile embedded strings.
6. Test invalid and empty states, keyboard behavior, narrow widths, managed integrity, package contents, and a fresh installed repository.
