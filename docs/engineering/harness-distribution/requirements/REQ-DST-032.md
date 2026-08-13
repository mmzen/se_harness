+++
id = "REQ-DST-032"
type = "requirement"
title = "Render a safe and accessible Explorer with a resilient 3D view"
status = "implemented"
owners = ["security-owner", "product-owner", "quality-owner"]
created = "2026-08-13"
updated = "2026-08-13"
statement = "WHEN Harness Explorer is opened from generated output, THE SYSTEM SHALL render repository data safely and responsively, keep its canonical evidence views available without the optional 3D dependency, and load only the explicitly accepted pinned 3D renderer from the documented CDN."
verification_method = "automated-security-test-and-manual-accessibility-review"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Render a safe local and accessible Explorer

## Rationale

Artifact titles, paths, owners, relation labels, findings, evidence paths, and experiment text are untrusted repository input. The Explorer may be used to inspect a repository that is misleading or hostile. The original reviewed interaction uses `3d-force-graph`; preserving that interaction currently requires one documented runtime CDN dependency.

## Required response

The generated dashboard must:

- load only `https://unpkg.com/3d-force-graph@1.79.0/dist/3d-force-graph.min.js` as its runtime third-party asset;
- send no repository artifact data to the CDN and require no hosted API, telemetry, remote font, image, or style;
- prevent embedded data from ending its inert script container or creating executable markup;
- render untrusted strings through text-safe DOM operations;
- use bounded graph traversal and rendering for cycles or large repositories;
- remain usable at desktop and narrow widths with keyboard-operable navigation;
- preserve meaning without color and provide distinguishable focus, warning, error, derived, and historical states;
- report invalid, empty, unsupported, and partially assessable states without implying success.

The URL pins the package version but does not provide content-addressed integrity. `ADR-DST-008` explicitly accepts the remaining CDN availability and supply-chain risk for this candidate. Local vendoring or an integrity-pinned alternative remains a future hardening option, not part of this work order.

## Failure and boundary behavior

If the optional CDN-backed visualization cannot initialize, the original page must display a clear 3D-unavailable state while its embedded canonical metrics, filters, focused lineage, definition coverage, readiness, findings, provenance, evidence, and controlled outcomes remain usable. Failure must not hide findings or authoritative provenance.

## Acceptance examples

### Example: hostile artifact title

**Given** an artifact title contains `</script>` and HTML event-handler text

**When** Explorer is generated and opened

**Then** the text is displayed or safely encoded and no repository-supplied script executes.

### Example: CDN unavailable

**Given** the generated dashboard is opened without access to `unpkg.com`

**When** the 3D renderer cannot load

**Then** the page identifies the unavailable 3D topology and preserves all non-3D evidence views from the embedded canonical snapshot.
