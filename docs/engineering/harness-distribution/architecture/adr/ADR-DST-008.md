+++
id = "ADR-DST-008"
type = "adr"
title = "Use the canonical snapshot as the WebUI boundary"
status = "approved"
owners = ["technical-owner", "security-owner", "quality-owner"]
created = "2026-08-13"
updated = "2026-09-01"

[relations]
decides = ["ARCH-DST-008"]
+++

# ADR: Use the canonical snapshot as the WebUI boundary

## Status

Accepted.

## Context

The existing Explorer generator emits deterministic `harness-dashboard-snapshot-v1` data whose hash is captured by commit-bound verification records. The new WebUI prototype defines another top-level model with different artifact types, relation fields, findings, readiness, metrics, and a mandatory generation timestamp. It also loads a graph library from a public CDN at runtime.

The product needs the original reviewed visual direction—including its interactive 3D topology—without allowing presentation design to redefine harness semantics or weaken deterministic provenance. On 2026-08-13, the accountable repository owner explicitly required preservation of the original prototype and its current CDN-loaded `3d-force-graph`, while accepting model-fidelity edits that prevent artifact-type omission or renaming.

## Decision drivers

- One explainable model shared by validation evidence and visualization.
- Stable commit-bound snapshot hashing.
- Fidelity to the original page structure, look and feel, responsive behavior, and 3D interaction.
- A narrow, documented runtime dependency boundary rather than an unrecorded or open-ended network allowance.
- Faithful rendering of rich findings, readiness conditions, provenance, supersession, and experiments.
- Safe handling of hostile repository content.
- Consistent source, package, and installed-repository behavior.

## Considered options

1. Replace the canonical snapshot with the prototype schema. Rejected because it discards current concepts, makes `generatedAt` nondeterministic, and couples assurance data to one presentation.
2. Keep both schemas and add a generator-side adapter. Rejected because two persisted models can drift and create ambiguous authority and compatibility obligations.
3. Host or fetch a dashboard service that transforms repository data. Rejected because repository data would cross the network boundary and presentation availability would depend on a service.
4. Keep `harness-dashboard-snapshot-v1` as the only persisted boundary, derive view-specific structures in browser memory, preserve the original UI, and retain only its pinned CDN-loaded 3D renderer. Selected.

## Decision

Adopt option 4. Reconcile the WebUI contract and prototype to consume the current canonical snapshot directly through an ephemeral browser adapter. Keep presentation-only metrics and focused graph subsets ephemeral. Preserve the existing safe embedding marker and deterministic snapshot serialization. Preserve the original sidebar, Overview/Lineage/Readiness views, visual tokens, responsive composition, and 3D topology.

The page may load only `https://unpkg.com/3d-force-graph@1.79.0/dist/3d-force-graph.min.js`. This exception does not authorize fetching repository data, fonts, styles, images, APIs, telemetry, or any other runtime dependency. If the script cannot load, the page must say that the 3D topology is unavailable and retain the embedded non-3D evidence views.

The redesigned interface must retain all five current Explorer questions and every material semantic distinction. Visual design is subordinate to the validator and snapshot contract whenever they conflict.

## Consequences

The verification hash retains its meaning and installed repositories receive one consistent Explorer. UI code performs bounded derivation and must handle the canonical model's richer fields without dropping or visually renaming artifact types. The generated page remains a read-only consumer, but full 3D behavior is no longer offline. Any future canonical snapshot change or dependency-boundary change remains an explicit governed decision rather than an incidental design edit.

## Accepted CDN risk

The exact package version in the URL reduces accidental version drift, but the response is not pinned by a retained cryptographic digest or browser-enforced Subresource Integrity value. The residual risks are:

- unpkg or the network may be unavailable, delaying or preventing the 3D topology;
- CDN, registry, package, DNS, or transport compromise could supply executable code within the page's origin context;
- the CDN observes ordinary request metadata such as client address and user agent, although the implementation sends no repository artifact data;
- browser or organizational network policy may block the script.

The accountable owner accepts these risks for the current candidate to preserve the reviewed 3D experience. Controls are the exact versioned URL, a CSP restricted to that origin, no repository-data transmission, no other remote assets, a 15-second timeout, a visible failure state, and complete embedded non-3D evidence views. Reconsider local vendoring, an independently verified SRI digest, or a dependency-free renderer before a security-sensitive or offline deployment, when the dependency version changes, if unpkg/package provenance changes, or if organizational policy prohibits runtime third-party code.

## Reassessment: 2026-08-16

The technical and security owners reaffirmed this decision after `SPEC-DST-008` and `ARCH-DST-008` were updated to remove the redundant `templates/webui/` handoff and identify the canonical standard-distribution template as the sole reusable Explorer source. That consolidation is compatible with selected option 4 and strengthens its single-model, consistent-distribution consequence.

The canonical snapshot boundary, browser adapter, safe embedding, UI fidelity, exact CDN exception, fallback, accepted residual risks, and reconsideration triggers remain unchanged. No alternative, outcome, or accepted risk was modified.

## Reassessment: 2026-09-01

The repository owner approved the designed Explorer packet (`WO-DST-023`).
`ADR-DST-013` decides that page: one self-contained document with a
hand-rolled topology, no runtime CDN, and a Content Security Policy that
names no remote origin. The exact `3d-force-graph` exception, its accepted
CDN risk, and the reconsideration triggers above are therefore closed by
that decision; the "dependency-free renderer" trigger fired. The canonical
snapshot boundary, browser-side derivation, safe embedding, and
single-model consequence of option 4 stand and continue to govern
`ARCH-DST-008` as amended.

## Validation

`VER-DST-008` checks direct contract use, twice-generated byte identity, sentinel and hostile-input safety, the single exact permitted runtime URL and CSP boundary, graceful CDN failure, semantic field retention, non-whitelisted artifact types with canonical names, exact readiness states, provenance and supersession visibility, five-question reachability, responsive keyboard use, managed copy equality, doctor, package contents, and fresh-install behavior.
