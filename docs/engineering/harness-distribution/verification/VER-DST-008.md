+++
id = "VER-DST-008"
type = "verification"
title = "Verify canonical Harness Explorer WebUI"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-13"
updated = "2026-08-13"

[relations]
verifies = ["REQ-DST-029", "REQ-DST-030", "REQ-DST-031", "REQ-DST-032", "REQ-DST-033"]
+++

# Verification Contract: Verify canonical Harness Explorer WebUI

## Independence

Verification derives expected model fields and authority semantics from the approved formal artifacts, validator, canonical snapshot builder, and managed distribution contract rather than from the implementation's DOM structure. Automated fixture assertions are complemented by accountable visual and accessibility review.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-DST-029` | snapshot and renderer contract tests | current repository plus minimal and future-type fixtures | UI consumes `harness-dashboard-snapshot-v1` directly; no persisted second schema or mandatory timestamp exists |
| `REQ-DST-030` | DOM/static assertions and manual semantic review | every current artifact type, relation authority, rich finding, G0-G5 state, revision, supersession, evidence, and experiment | all five questions remain reachable and no authoritative distinction is flattened or inferred |
| `REQ-DST-031` | repeat-generation and provenance tests | same repository state generated at least twice | `dashboard-data.json` bytes and snapshot SHA-256 are identical; run time exists only outside the snapshot |
| `REQ-DST-032` | adversarial static/browser tests, network-boundary inspection, CDN-failure test, and accessibility review | closing-script text, sentinel text, HTML handlers, Unicode separators, long strings, cycles, invalid repository, blocked CDN, narrow width, keyboard navigation | repository content cannot execute; only the exact accepted 3D URL may be requested; CDN failure preserves non-3D evidence views; output is bounded and understandable without color alone |
| `REQ-DST-033` | parity, installer, upgrade, doctor, package, and fresh-environment tests | source candidate, canonical template, built package, initialized and adopted repositories | one managed local implementation and asset set is complete, equivalent, integrity-checked, and transactionally installed |

## Acceptance scenarios

- Generate from the real repository and inspect Overview, Lineage, Readiness, definition coverage, impact, findings, revision history, supersession, evidence, and experiments.
- Render every canonical artifact type and an unknown synthetic future type without failure or silent omission.
- Preserve each artifact type's canonical string in filters, inspectors, details, and 3D labels instead of mapping it to a smaller display vocabulary.
- Show declared versus derived relations, missing targets, direct versus transitive impact, and `via` paths.
- Show `satisfied`, `unsatisfied`, and `not_assessable` gate conditions without a health score or implied approval.
- Show observed checkout revision separately from commit-bound VREC and release provenance.
- Show an explicit superseded-to-successor relation while preserving both historical candidates and work coverage.
- Run with no experiments and no evidence, and with an invalid graph, without producing a success-looking empty screen.

## Property and invariant tests

- Identical repository and Git state produce identical canonical snapshot bytes and SHA-256 values.
- Snapshot serialization is independent of generation time and browser interaction.
- Focused graph traversal terminates for cycles, self-relations, duplicate paths, missing targets, and bounded large fixtures.
- Every canonical artifact and relation remains discoverable from the rendered document.
- Unknown types remain neutral data rather than executable behavior or dropped records.

## Static and architecture checks

- Exactly one safe snapshot marker exists in the owned template.
- The only HTTP or HTTPS runtime asset is `https://unpkg.com/3d-force-graph@1.79.0/dist/3d-force-graph.min.js`; CSP permits scripts from `unpkg.com` and denies other remote categories.
- No remote font, image, style, hosted API, telemetry, dynamic import, fetch, WebSocket, repository-data transmission, or repository-derived code execution exists.
- Repository strings reach the DOM only through text-safe operations.
- Root and canonical managed copies plus any asset inventories are equivalent.
- CLI dispatch and exit-code behavior remain unchanged unless an approved deviation is recorded.
- The revised WebUI schema documentation, handoff, manifest, brand contract, and prototype agree with `SPEC-DST-008` and contain no missing asset references.

## Security and privacy checks

Use fixtures containing `</script>`, the snapshot marker, markup, event handlers, URL-like values, ampersands, angle brackets, U+2028/U+2029, bidirectional text, long paths, and cyclic relations. Inspect generated HTML and execute bounded browser checks. Confirm no repository content executes, the only permitted request is the accepted 3D bundle, repository data is not placed in its URL, and diagnostics do not expose file bodies unnecessarily.

Confirm that blocking the CDN produces the explicit 3D-unavailable state while Overview metrics and filters, focused Lineage, definition coverage, Readiness, provenance, evidence, and controlled-outcome sections remain populated. Record that no local digest or SRI value is claimed and review the risk acceptance in `ADR-DST-008`.

## Manual assessments

At desktop and narrow widths, a reviewer must confirm the original prototype's structure and visual identity remain recognizable; the five questions are easy to find; every canonical artifact type remains exact and selectable; relation direction and authority are clear; definition coverage is not confused with VREC assurance; gates and conditions are readable; observed and authoritative commits are distinct; superseded history remains understandable; CDN failure is explicit; focus and keyboard navigation work; and color is not the only carrier of meaning.

## Evidence retention

Retain exact commands, runtimes, changed paths, snapshot and output hashes, test counts, hostile-input cases, model-field inventory, asset provenance if applicable, browser widths, accessibility observations, managed parity, package inspection, fresh-install results, deviations, and residual risks under `docs/engineering/harness-distribution/evidence/WO-DST-007-verification.md`.

## Residual uncertainty

Static and fixture checks cannot prove that every very large real repository remains visually comprehensible, that every assistive technology behaves identically, or that a third-party CDN/package remains available and uncompromised. Manual review samples representative widths and navigation, while the fallback preserves access to embedded non-3D data. `ADR-DST-008` owns the accepted runtime dependency risk.
