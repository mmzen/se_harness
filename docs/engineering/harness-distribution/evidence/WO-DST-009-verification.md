# WO-DST-009 implementation evidence

## Scope and authority

On 2026-08-14, the repository owner supplied `C:\Users\mathi\Desktop\ui\released\index.template.html` and explicitly requested its integration after reviewing the draft `WO-DST-009`. On 2026-08-15, the owner instructed removal of the redundant `templates/webui/` directory because the canonical standard template is sufficient. The change remained presentation and distribution-source cleanup only and continued to use `harness-dashboard-snapshot-v1`, the existing generator, and the exact accepted `3d-force-graph@1.79.0` unpkg URL. No commit, push, VREC, release, publication, or deployment was performed.

## Integrated result

The supplied design adds refined navigation icons, state/type/assurance color lenses, graph legends, directional 3D links, a card-based focused lineage with relation labels and zoom controls, improved gate styling, and responsive presentation refinements. Overview, Lineage, Readiness, the five Explorer questions, canonical artifact-type strings, evidence, provenance, supersession, controlled outcomes, and non-3D fallback content remain present.

Review corrected three defects before integration:

- removed a duplicate `renderLineage()` implementation so there is one active renderer;
- changed the interactive lineage container from `role="img"` to `role="group"`, keeping its child artifact buttons exposed to assistive technology;
- replaced mobile `display:none` navigation labels with visually hidden labels, preserving accessible names at narrow widths.

The initial integration temporarily maintained prototype parity to satisfy the then-current contract. The owner's follow-up decision retired that redundant copy. `SPEC-DST-008`, `VER-DST-008`, the distribution index, and focused tests now identify `templates/repository/standard/scripts/harness_explorer/index.template.html` as the sole reusable WebUI source, while `scripts/harness_explorer/index.template.html` remains its byte-equivalent active copy.

No canonical snapshot, generator, CLI, validator, formal lifecycle, relation vocabulary, runtime URL, or network boundary changed.

## Changed paths

- `.engineering-harness.lock`
- `scripts/harness_explorer/index.template.html`
- `templates/repository/standard/scripts/harness_explorer/index.template.html`
- `tests/test_dashboard_webui.py`
- `docs/engineering/harness-distribution/README.md`
- `docs/engineering/harness-distribution/specifications/SPEC-DST-008.md`
- `docs/engineering/harness-distribution/verification/VER-DST-008.md`
- `docs/engineering/harness-distribution/work-orders/WO-DST-009.md`
- `docs/engineering/harness-distribution/evidence/WO-DST-009-verification.md`

Deleted as redundant design-source material:

- `templates/webui/DESIGN-HANDOFF.md`
- `templates/webui/DESIGN-MANIFEST.json`
- `templates/webui/brand-spec.md`
- `templates/webui/harness-dashboard-data.md`
- `templates/webui/harness-dashboard-data.schema.json`
- `templates/webui/harness-lineage-prototype.html`

The active and canonical templates are byte-identical. Their Windows checkout SHA-256 is `0d675903e13c820ce2306765df9c44115097f9e5fa06e6fa855e25d351d5dabb`; their schema-2 `utf8-text-lf-v1` managed digest is `8c923a7dfc3b0722cca77d3c52804e81e8a25e875190aa8d6d6455d2505319e7`.

## Automated verification

| Check | Result |
| --- | --- |
| Start preflight | PASS for approved `WO-DST-009` and its complete governing chain. |
| Formal artifact validation | PASS: 285 artifacts, 0 errors, 38 existing migration/location warnings. |
| Final focused WebUI and self-hosting tests | PASS: 18 tests. |
| Broader dashboard, CLI, and self-hosting tests | PASS after reconciliation: 43 tests with 1 expected Windows symlink skip. |
| Complete standard-library suite | PASS: 148 tests, 3 expected skips, in 50.232 seconds. |
| Managed-integrity doctor | PASS for required, distribution, managed, lock, and self-hosting checks; 9 existing `W013` location advisories remain. |
| Template parity and single-source boundary | PASS: active and canonical bytes are equal; `templates/webui/` is absent. |
| Static boundary assertions | PASS: one snapshot marker, one `renderLineage()` declaration, one exact permitted graph URL, interactive group role, zoom controls, directional links, and retained accessible mobile labels. |
| Diff hygiene | PASS; Git emitted only expected Windows LF-to-CRLF checkout notices. |

The first focused run correctly failed the transitional prototype-parity and managed-integrity assertions. Prototype parity was initially restored under the prior contract. After the owner explicitly retired the redundant directory, the active specification, verification contract, tests, and distribution index were reconciled to a single canonical source. Only the changed template's schema-2 canonical digest was updated; the upgrade plan's unrelated self-hosting control changes were not applied. A narrow-width browser review exposed hidden navigation labels, which were corrected before the final suite.

Two harmless command-invocation mistakes were corrected during final verification: the standalone validator was first called with an unsupported positional root before being rerun successfully with `--root .`, and the first external-output dashboard attempt was launched outside the source checkout where the package was not importable before both successful runs were launched from the repository. Neither invocation modified the candidate or produced an accepted result.

## Deterministic generation

Two consecutive real-repository generations produced:

- 285 artifacts;
- 1,025 projected relations;
- 0 validator errors;
- 46 derived review warnings;
- identical final `dashboard-data.json` SHA-256 `ab688f04f0e9fb551ceaa64017e4acd80dc446cd12c9c1e5212326dedbbd3753` after the work order reached `implemented`, the single-source contract was reconciled, and this evidence path was retained.

The final rendered `index.html` SHA-256 is `59a3ded27409379f2cee5c3b9de7a7346139f4992e0dd905ebc90069e77250a2` for both runs.

## Browser review

The real generated dashboard was served from a temporary loopback-only server and reviewed in the in-app Chromium browser. The temporary server was stopped after review.

At 1280x720:

- the 3D topology loaded from the single accepted URL;
- the page had no horizontal overflow;
- the graph displayed eight lifecycle legend categories;
- focused lineage rendered nine bounded artifact cards;
- zoom changed the lineage transform from `scale(1)` to `scale(1.1)`;
- selecting a lineage card updated the artifact detail;
- Readiness exposed 52 subjects and all six G0-G5 gates;
- browser logs contained no warnings or errors.

At 390x844:

- document client width and scroll width were both 375 pixels, so no horizontal overflow remained;
- focused lineage switched to the single-column card layout with nine visible cards and no scale transform;
- Overview, Lineage, and Readiness retained accessible text names while remaining visually icon-only in the bottom navigation.

The CDN-failure catch path and explicit `Interactive 3D topology unavailable` state are unchanged from the previously verified implementation. Static tests and inspection confirm that only the optional 3D topology degrades and canonical non-3D views remain embedded. This refinement did not inject a new live CDN failure because it did not change loader or fallback behavior.

## Residual risk

The pre-existing CDN availability, request-metadata, and executable third-party supply-chain risks remain accepted under `ADR-DST-008`. The refined lineage is bounded but dense paths can still require scrolling and visual interpretation. Additional assistive-technology combinations and unusually large repositories remain representative-testing concerns rather than inferred guarantees.
