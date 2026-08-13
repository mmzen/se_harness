# WO-DST-007 implementation evidence

## Scope and authority

The accountable repository owner approved `WO-DST-007` on 2026-08-13 with `go implementation`. During review of the uncommitted candidate, the owner corrected the design direction: preserve the original prototype, including its current CDN-loaded `3d-force-graph`, while changing the page only to reflect the canonical harness model and prevent artifact-type exclusion or renaming.

The governing requirement, specification, architecture, ADR, verification contract, and work order were amended before this final implementation was assessed. `ADR-DST-008` records the accepted CDN risk. No commit, VREC, release, tag, package build, publication, or deployment was performed.

The generator's snapshot builder, deterministic serializer, transactional output, and `harnessctl dashboard` dispatch were inspected and did not require semantic changes.

## Requirement results

| Requirement | Result |
| --- | --- |
| `REQ-DST-029` | The prototype, handoff, manifest, documentary schema, and active UI consume `harness-dashboard-snapshot-v1`; the browser adapter is ephemeral and no second persisted WebUI schema exists. |
| `REQ-DST-030` | The original Overview, Lineage, and Readiness composition retains all five questions, rich findings, definition coverage, G0-G5 conditions, revision provenance, supersession, evidence, and experiments. Relations retain canonical names and authority. |
| `REQ-DST-031` | Two final unchanged generations produced byte-identical `dashboard-data.json` with SHA-256 `27797f755a00c7490f8c99ded1ef531685ab5f2aa1cf86e5f08b700971fb008b`; run time remains outside the snapshot. |
| `REQ-DST-032` | The exact pinned `3d-force-graph@1.79.0` unpkg URL is the only permitted runtime asset. Hostile embedded data remains escaped. Browser checks confirmed both the 3D path and a deliberately failed-CDN path with all non-3D evidence retained. |
| `REQ-DST-033` | Root, canonical package template, and WebUI prototype are byte-identical; the canonical file remains in the standard installation set; schema-2 managed integrity and doctor pass. |

## Prototype and model reconciliation

The original staged prototype was restored as the structural and visual baseline. Its sidebar, Overview/Lineage/Readiness navigation, top bar, metrics, operator queue, topology-led layout, graph controls, 3D renderer, focused lineage, detail tabs, readiness panels, typography, colors, spacing, and responsive rules remain recognizable.

The prototype's separate `1.0.0` payload, mandatory `generatedAt`, reduced artifact vocabulary, renamed relation shape, and flattened readiness model were not retained. An in-memory adapter derives the existing page modules directly from canonical sections. Artifact types are discovered from `artifacts`, inserted into the filter with `new Option(v, v)`, and displayed from `item.type` or `node.type`; there is no type whitelist or renaming map. A synthetic `future_control` artifact survived rendering unchanged.

Small model-fidelity additions expose the five questions, definition coverage, commit-bound provenance, supersession authority, and controlled outcomes without replacing the original information architecture.

## Runtime dependency and accepted risk

The original renderer loads:

`https://unpkg.com/3d-force-graph@1.79.0/dist/3d-force-graph.min.js`

Static checks found no other remote script, font, image, style, API, telemetry, `fetch`, WebSocket, or dynamic import. CSP permits inline owned code and scripts from `unpkg.com`, while `connect-src`, fonts, objects, forms, and base changes remain denied. Repository data is embedded locally and is not appended to the CDN URL.

The versioned URL is not content-addressed and has no retained SRI digest. Availability, ordinary request-metadata disclosure, and CDN/package supply-chain compromise remain accepted residual risks under `ADR-DST-008`. Controls include the exact URL, narrow CSP, 15-second timeout, visible failure state, and complete non-3D evidence fallback.

## Changed implementation surfaces

- `scripts/harness_explorer/index.template.html`
- `templates/repository/standard/scripts/harness_explorer/index.template.html`
- `templates/webui/DESIGN-HANDOFF.md`
- `templates/webui/DESIGN-MANIFEST.json`
- `templates/webui/brand-spec.md`
- `templates/webui/harness-dashboard-data.md`
- `templates/webui/harness-dashboard-data.schema.json`
- `templates/webui/harness-lineage-prototype.html`
- `.engineering-harness.lock`
- `tests/test_dashboard_webui.py`
- the `REQ-DST-029..033`, `SPEC-DST-008`, `ARCH-DST-008`, `ADR-DST-008`, `VER-DST-008`, and `WO-DST-007` packet plus its distribution index entry

The active template, canonical template, and prototype are byte-identical. Each has raw SHA-256 `044c3510f48ce04bda4f3ee67a595975ca21c0e3644bc408950af223b8251253` and size 46,986 bytes. Their schema-2 `utf8-text-lf-v1` managed digest is `7f6622a755cc8dcaa885a2de85f3df9f13fbec23a5c5415599defe8cada0732c`.

## Automated checks

| Check | Result |
| --- | --- |
| Formal artifact validation | PASS: 279 artifacts, 0 errors, 38 existing legacy-layout/architecture migration advisories. |
| Review preflight for `WO-DST-007` | PASS with the complete governing manifest and implemented work-order status. |
| Focused `tests.test_dashboard_webui` | PASS: 6 tests covering original-design retention, canonical contract, five questions, exact/future artifact types, CDN boundary, hostile embedding, parity, and determinism. |
| Supersession projection regression | PASS, including `Superseded by` and `Supersession authorized by`. |
| Complete standard-library suite | PASS: 147 tests in 53.668 seconds, 3 expected conditional skips. |
| JavaScript syntax | PASS with the bundled Node.js runtime using `new Function` over the final inline program. |
| Managed-integrity doctor | PASS for all required, distribution, managed, lock, and self-hosting checks; only 9 existing `W013` canonical-location advisories remain. |
| Template and package discovery | PASS: root/canonical/prototype bytes equal and the Explorer template remains in the standard installation set. |
| `git diff --check` | PASS after final evidence update; checkout may report expected Windows LF-to-CRLF notices. |

## Deterministic generation

Two consecutive final `python -B -m se_harness dashboard .` runs produced:

- 279 artifacts;
- 979 relations;
- 0 validator errors;
- 39 derived review warnings;
- identical snapshot SHA-256 `27797f755a00c7490f8c99ded1ef531685ab5f2aa1cf86e5f08b700971fb008b`.

Presentation and CDN behavior do not enter the canonical snapshot hash.

## Security cases

Focused tests rendered a title containing a closing script tag, markup with an event handler, ampersand, U+2028, U+2029, and the snapshot sentinel. The HTML contained the expected `\u003c`, `\u003e`, `\u0026`, `\u2028`, and `\u2029` escapes; the hostile closing tag did not appear; and the sentinel was replaced exactly once.

The original prototype uses owned `innerHTML` templates for several modules, but every repository-derived value on those paths passes through the HTML escaper. Ordinary scalar labels use `textContent`. Tests and browser execution found no repository-derived code execution.

## Browser review

The generated page was reviewed at 1280x720 in the in-app Chromium browser from a dashboard-only localhost server.

With the accepted CDN available:

- the page retained the original sidebar and three-view composition;
- all five questions rendered;
- all 279 artifacts and 957 declared relations were summarized;
- the artifact-type filter contained all 12 canonical types with their exact underscore names;
- the `3d-force-graph` canvas initialized and rendered the repository topology;
- 93 active definition-coverage rows, 48 readiness subjects, and 21 commit-bound provenance records rendered;
- the no-experiment state explicitly said effectiveness is not measured;
- body width equaled client width and browser logs contained no warnings or errors.

For the failure case, an isolated test copy replaced the CDN URL with a refused localhost endpoint. The page displayed `Interactive 3D topology unavailable`; graph readiness stayed false; and all 279 artifacts, 13 filter options including `all`, 93 coverage rows, 48 readiness subjects, and 21 provenance records remained available. The only browser warning was the expected graph-library load failure.

## Residual uncertainty and next hardening options

No second snapshot, generator, CLI, validator-authority, or lifecycle deviation remains. The material residual risk is the explicitly accepted third-party runtime code boundary. Before security-sensitive, disconnected, or audit-constrained deployment, reassess local vendoring, independently verified Subresource Integrity, or a dependency-free renderer. Very large repositories and assistive-technology combinations also require continued representative visual review.
