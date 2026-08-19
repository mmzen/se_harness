+++
id = "SPEC-DST-017"
type = "specification"
title = "Owner-authorized Explorer dashboard revision"
status = "approved"
owners = ["technical-owner", "product-owner", "quality-owner", "security-owner"]
created = "2026-08-19"
updated = "2026-08-19"

[relations]
specifies = ["REQ-DST-030", "REQ-DST-032", "REQ-DST-033", "REQ-DST-035", "REQ-DST-040", "REQ-DST-041", "REQ-DST-042", "REQ-DST-045", "REQ-DST-047", "REQ-DST-050", "REQ-DST-055"]
+++

# Specification: Owner-authorized Explorer dashboard revision

## Scope

On 2026-08-19 the repository owner supplied a revised `index.template.html`, instructed the agent to integrate that revision, authorized raising the initial Explorer shell budget to 256 KiB, and authorized controlled URL fragments and browser History API state. After browser verification exposed an initialization-order defect and an uncaught malformed-fragment decode, the owner explicitly answered `yes OK` to the requested minimal template corrections. This specification records those accountable product and technical decisions without granting verification, release, publication, or deployment authority.

Integrate the supplied dashboard revision into the single canonical managed Explorer implementation, changing only its explicitly authorized route initialization and safe-decoding behavior, while preserving the progressive bundle, manifest verification, canonical evidence semantics, safe rendering, accessibility, deterministic distribution, and existing runtime-network boundary.

## Actors and external systems

- Repository readers use Overview, Lineage, and Readiness to inspect derived repository evidence.
- The package-owned and target-local generators create the same deterministic static bundle.
- A static same-origin HTTP server supplies manifest-declared resources.
- The exact accepted `3d-force-graph@1.79.0` URL remains the only third-party runtime asset.

## Inputs

- Owner-supplied `C:/Users/mathi/Downloads/index.template.html` with intake SHA-256 `6b6881a095fac417c358548342eb31737c58b9bf6345cf632b066f8aa53f470a`.
- The validated canonical artifact projection and integrity-addressed bundle contract.
- Untrusted repository-derived strings, metadata, and retained evidence.

## Outputs

- Byte-equivalent canonical and active Explorer templates.
- A managed lock digest produced through the supported upgrade transaction.
- Generated dashboards within a 262,144-byte UTF-8 `index.html` limit.
- Controlled same-document routes for Overview, Lineage, and Readiness presentation state.

## State model

The progressive loading, verified-resource cache, current artifact, Lineage visit trail, Readiness selection, retry containment, and optional 3D fallback remain presentation state. URL fragments expose only the controlled current route. Browser history entries navigate those routes but do not become formal lineage, evidence, provenance, approval, verification, or release state.

## Behavioral rules

1. Use the owner-supplied bytes as the dashboard revision base, apply only the separately authorized routing corrections, and keep the final canonical and active templates byte-equivalent.
2. Raise the generator-owned `index.html` maximum from 153,600 to 262,144 UTF-8 bytes in both canonical and active generators.
3. Preserve exactly one `__HARNESS_BOOTSTRAP_JSON__` marker, the progressive bundle-v2 schemas, same-origin resource verification, manifest byte/digest checks, and transactional output promotion.
4. Preserve the existing CSP and exact accepted graph CDN URL; add no runtime URL, dependency, storage, cookie, telemetry, service, or repository write.
5. Retain Overview repository posture, bounded topology scope, artifact inspection, semantic lens, operator queue, and density controls without treating derived observations as authority.
6. Retain the structured Lineage board, exact relation direction and authority, depth bounds, optional connectors, detail routes, reversible 20-entry visit trail, focus behavior, and non-hierarchical history language.
7. Permit controlled fragments and History API entries for Overview, selected Lineage artifact, Readiness index, Readiness subject, and gate-state listing. Reloading a routed URL starts a new bounded Lineage visit trail from that route rather than restoring prior visits.
8. Safely ignore or reduce unsupported routes. Never derive an external URL, resource path, executable selector, or authority claim from a fragment value.
9. Retain Readiness gate rollups, subject listings, evidence-state filters, exact gate states, `not_assessable`, and explicit derived/read-only boundaries without manufacturing approval or readiness.
10. Preserve safe inert rendering of artifact identity, bodies, relations, evidence, findings, provenance, experiments, and unknown values.
11. Preserve keyboard operation, visible focus, accessible names, non-color meaning, desktop and narrow-width access, explicit failures, and CDN fallback.
12. Update focused tests for the authorized History API behavior, the 262,144-byte shell limit, new DOM controls, and the `data-integrity` presentation attribute without weakening the prohibition on Subresource Integrity claims for the dynamically acquired graph script.
13. Reconcile the active copies and schema-2 lock only through the supported candidate upgrade transaction; customized or ambiguous targets remain protected.
14. Decode route path components through a non-throwing boundary. A malformed encoded component must reduce to a safe local view and must not prevent dashboard initialization.
15. Apply a requested Lineage artifact route after verified topology is available and before rendering can replace the requested fragment with the default artifact.

## Error and recovery behavior

Missing or malformed bootstrap, manifest, resources, fragments, selected IDs, gate states, or deferred content fail visibly and remain bounded to the requesting route or panel. A hard byte-budget violation fails before output promotion. History navigation never repairs data, substitutes an artifact, or broadens network access.

## Data and interface contracts

- `index.html` remains the static shell and bootstrap trust root.
- Fragment routes are presentation-only strings rooted at `#overview`, `#lineage`, or `#readiness` with controlled encoded identifiers or gate-state parameters.
- Artifact and evidence lookup continues to use manifest-controlled descriptors, never raw route-derived filesystem paths.
- `data-integrity` is a local visual-state attribute and is not a Subresource Integrity declaration.

## Security and privacy properties

Repository content remains inert and untrusted. Route decoding cannot create HTML, selectors, scripts, styles, resource requests, external navigation, storage keys, or repository writes. The only runtime network exception remains the accepted pinned-version graph URL, which receives no repository data.

## Performance and capacity

The generated `index.html` hard limit is 262,144 UTF-8 bytes before compression. Summary, topology, artifact/evidence source, and total-content limits remain unchanged. The new template requires no build step or runtime framework.

## Observability

Retain deterministic shell/resource byte measurements, manifest digests, repository validation state, observed revision, integrity/loading/failure state, and explicit non-authority language.

## Compatibility and migration

Existing repositories receive the revision only through safe managed upgrade. Customized templates are not overwritten. Historical generated dashboards and release records remain unchanged.

## Examples and counterexamples

- Intended: `#lineage/REQ-DST-055` opens that focused artifact and begins a new bounded visit trail.
- Intended: `#readiness?gate=G4&state=unsatisfied` lists matching subjects without asserting readiness.
- Invalid: a fragment becomes a fetch path, restores the complete prior visit trail, or creates an external navigation.
- Invalid: raising or bypassing another content limit merely because the shell budget changed.

## Explicitly unspecified decisions

The supplied CSS values, markup order, copy, and local interaction details are accepted as implementation input. The implementation agent may update focused tests and formal compatibility wording and may make only the two route corrections explicitly authorized after browser review. Any other template-byte change requires further explicit owner permission.
