+++
id = "SPEC-DST-016"
type = "specification"
title = "Owner-directed Harness Explorer presentation refresh"
status = "approved"
owners = ["technical-owner", "product-owner", "quality-owner", "security-owner"]
created = "2026-08-18"
updated = "2026-08-18"

[relations]
specifies = ["REQ-DST-030", "REQ-DST-032", "REQ-DST-033", "REQ-DST-035", "REQ-DST-047"]
+++

# Specification: Owner-directed Harness Explorer presentation refresh

## Scope

On 2026-08-18, after reviewing this bounded packet and the proposed required assurance classification, the repository owner instructed `ok go implement`. That decision approves this prospective presentation contract; it does not verify a candidate, authorize a commit, or grant release or publication authority.

Integrate the owner-supplied `index.template.html` presentation into the single managed Harness Explorer template while preserving the progressive bundle, browser behavior, canonical evidence semantics, security boundary, accessibility, and managed-distribution parity.

The reviewed input is `C:/Users/mathi/Downloads/index.template.html`, observed at intake with raw SHA-256 `5b52939838a9c91d04689814ba8523e8fca627111704dde9e4da31faf02a8368`. This specification intentionally retires the literal five-question navigation strip; it does not retire the underlying semantic questions or the evidence needed to answer them.

## Actors and external systems

- Repository readers use Overview, Lineage, and Readiness to inspect derived evidence.
- `harnessctl dashboard` and the target-local generator continue to own deterministic bundle creation.
- The exact accepted `3d-force-graph` URL remains the only permitted third-party runtime asset.

## Inputs

- The current progressive dashboard bundle and bootstrap contract.
- The owner-supplied HTML/CSS presentation.
- Untrusted repository-derived strings and resources.

## Outputs

- Byte-equivalent active and canonical standard-template copies.
- Generated dashboards with refreshed presentation and unchanged progressive data contracts.
- A schema-2 managed lock matching the canonical template.

## State model

The browser state model is unchanged: progressive loading, Overview selection and filters, reversible Lineage navigation, artifact detail tabs, Readiness selection, verified-resource caching, retry containment, and optional 3D fallback.

## Behavioral rules

1. Replace the active and canonical Explorer presentation with the owner-supplied design while keeping both repository copies byte-equivalent.
2. Remove the literal five-question strip and numbered question copy. The interface need not reproduce those questions verbatim.
3. Preserve direct access through Overview, Lineage, Readiness, artifact details, Relations, Evidence, provenance, findings, and controlled outcomes so `REQ-DST-030` remains satisfied.
4. Preserve the current inline JavaScript bytes and behavior. No schema, progressive resource, generator, navigation, sanitization, or network behavior change is authorized.
5. Preserve the current CSP and exact `https://unpkg.com/3d-force-graph@1.79.0/dist/3d-force-graph.min.js` exception; add no URL, dependency, storage, telemetry, or hosted service.
6. Reorganize Overview only through static markup and local CSS while retaining compact coverage, topology controls, inspector, assurance lens, operator queue, and evidence routes.
7. Present a textual boundary that Explorer is derived/read-only and infers no approval, verification, or release decision.
8. Label Readiness gate groupings as Explorer navigation, identify managed `QUALITY_GATES.md` as the policy owner, and state that the groupings grant no authority.
9. Preserve exact artifact type, lifecycle state, and derived assurance labels without conflating definition coverage with assurance.
10. Preserve keyboard operation, visible focus, accessible names, non-color meaning, narrow-width access, explicit failures, and CDN fallback.
11. Replace focused assertions for the literal question phrases with assertions for retained semantic routes and authority-boundary copy; do not weaken security, data, provenance, or distribution checks.
12. Update the managed digest only through the supported canonical-candidate and safe-upgrade transaction.

## Error and recovery behavior

Existing bounded loading, integrity, retry, race, malformed-resource, missing-target, empty-state, and CDN-failure behavior remains unchanged. Stop if the supplied template changes inline JavaScript, CSP, external URLs, bootstrap markers, required DOM hooks, or progressive schemas.

## Data and interface contracts

- Preserve exactly one `__HARNESS_BOOTSTRAP_JSON__` marker.
- Preserve every DOM identifier/data hook consumed by the unchanged script; `gatePanelTitle` may be added for accessible labeling.
- Preserve Overview, Lineage, and Readiness `data-view` values.
- Preserve progressive schema constants, same-origin resource verification, and formal artifact/relation vocabulary.

## Security and privacy properties

Repository content remains inert untrusted data. The refresh must not introduce repository-derived executable HTML, CSS, URLs, event handlers, scripts, or storage. Runtime requests remain limited to same-origin bundle resources plus the exact accepted 3D script.

## Performance and capacity

Current graph, Lineage, history, resource, content, and timeout bounds remain unchanged. Static markup/CSS growth must require no build step.

## Observability

Retain visible loading, failure, retry, validation, revision, resource-integrity, gate-boundary, and authority-boundary information.

## Compatibility and migration

Existing repositories receive the refresh only through safe managed upgrade; customized or ambiguous templates remain protected. Historical released templates and records remain unchanged. This prospective specification does not reinterpret released candidates.

## Examples and counterexamples

**Intended:** the numbered question strip is absent, while Overview, Lineage, Readiness, details, findings, provenance, evidence, and outcomes remain directly reachable.

**Gate boundary:** adjacent text identifies Explorer groupings as navigation, points to managed `QUALITY_GATES.md`, and grants no authority.

**Prohibited:** changing JavaScript to compensate for missing DOM hooks, adding another question model, weakening CSP, or removing an evidence route.

## Explicitly unspecified decisions

After approval, the implementation agent may preserve supplied CSS values, breakpoints, static element order, spacing, and concise copy. Only minimal markup corrections needed for valid accessible structure and unchanged-script compatibility are delegated, and every deviation from the supplied input must be recorded.
