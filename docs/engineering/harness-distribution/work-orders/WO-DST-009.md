+++
id = "WO-DST-009"
type = "work_order"
title = "Refine the Harness Explorer presentation"
status = "implemented"
owners = ["engineering-owner", "quality-owner"]
created = "2026-08-14"
updated = "2026-08-15"

[relations]
implements = ["REQ-DST-029", "REQ-DST-030", "REQ-DST-031", "REQ-DST-032", "REQ-DST-033"]
specifications = ["SPEC-DST-008"]
architecture = ["ARCH-DST-008", "ADR-DST-008"]
verification = ["VER-DST-008"]
+++

# Work Order: Refine the Harness Explorer presentation

## Lifecycle

The repository owner requested a new bounded work order on 2026-08-14 before making slight changes to `scripts/harness_explorer/index.template.html`. After the draft was presented, the owner supplied the replacement template and explicitly instructed the agent to integrate it. Inspection confirmed that the intended design stays within this presentation-only decision envelope. That human decision approves this bounded work order; the three integration corrections identified during review—removing a duplicate lineage renderer, preserving interactive accessibility, and retaining mobile navigation names—are also within scope.

Use `in_progress` while the approved edits are being made and `implemented` only after the active and canonical templates are synchronized and the required evidence is retained. Commit-bound verification, commit, push, pull request, release selection, publication, and deployment remain separate decisions.

On 2026-08-15, the owner additionally directed removal of the redundant `templates/webui/` directory because the canonical standard template is sufficient. This instruction amends the same bounded integration without changing runtime behavior or the accepted trust boundary.

## Objective

Allow small owner-directed refinements to the Harness Explorer page while preserving the implemented canonical snapshot model, exact harness terminology, reviewed visual identity, security boundary, accessibility behavior, and managed-distribution parity, with one canonical reusable WebUI source.

## In scope

- Adjust presentation markup, local CSS, explanatory copy, layout details, or bounded presentation-only interaction in `scripts/harness_explorer/index.template.html`.
- Apply the same final template bytes to `templates/repository/standard/scripts/harness_explorer/index.template.html`.
- Remove the redundant `templates/webui/` handoff, prototype, schema, manifest, and brand materials after reconciling the active specification, verification contract, tests, and domain index.
- Treat `templates/repository/standard/scripts/harness_explorer/index.template.html` as the sole reusable WebUI source; keep the active root copy byte-equivalent.
- Preserve the Overview, Lineage, and Readiness views; the five Explorer questions; the 3D topology; and every existing canonical data section.
- Update focused template assertions only when an approved presentation change legitimately changes their expected markup.
- Retain verification evidence keyed to this work order.

## Out of scope

- Changing `harness-dashboard-snapshot-v1`, the generator's canonical data, formal artifact or relation vocabulary, lifecycle states, validator authority, readiness gates, commit provenance, release eligibility, or supersession behavior.
- Removing or replacing `3d-force-graph`, changing its exact approved URL, or adding another runtime dependency, network request, telemetry path, build tool, or package manager.
- Excluding, renaming, or collapsing artifact types or authoritative relation fields.
- Adding an aggregate health, confidence, compliance, verification, or release score.
- Rewriting the Explorer generator or CLI dispatch, changing repository-owned formal artifacts, or modifying historical verification and release records.
- Commit, push, pull request, merge, release, publication, or deployment authority.

## Authorized decision envelope

After approval, the owner or implementation agent may choose presentation details within the active HTML template, including spacing, typography, local color use, copy, element placement, and small bounded interactions. Those choices must leave canonical meanings, safe rendering, keyboard access, responsive access, the permitted CDN boundary, and non-3D fallback behavior intact.

If an intended refinement needs generator data, a schema change, a new dependency, a changed trust boundary, a material alteration of the reviewed design structure, or reduced access to canonical evidence, stop and extend the formal packet before implementation.

## Constraints

- Preserve Python 3.11+ standard-library runtime behavior and the target-local `harnessctl dashboard` ownership boundary.
- Treat all embedded repository strings as untrusted data; do not introduce repository-derived executable HTML, script, URLs, or styles.
- Keep the active and canonical managed templates byte-equivalent.
- Preserve the exact `https://unpkg.com/3d-force-graph@1.79.0/dist/3d-force-graph.min.js` exception and its existing local semantic fallback.
- Preserve unrelated user changes and inspect the index and worktree before any later commit proposal.

## Expected change surface

- `scripts/harness_explorer/index.template.html`
- `templates/repository/standard/scripts/harness_explorer/index.template.html`
- removal of `templates/webui/DESIGN-HANDOFF.md`, `DESIGN-MANIFEST.json`, `brand-spec.md`, `harness-dashboard-data.md`, `harness-dashboard-data.schema.json`, and `harness-lineage-prototype.html`
- `.engineering-harness.lock`, limited to the changed managed-template digest
- `docs/engineering/harness-distribution/specifications/SPEC-DST-008.md`
- `docs/engineering/harness-distribution/verification/VER-DST-008.md`
- `docs/engineering/harness-distribution/README.md`
- focused Explorer tests that enforce the single-source boundary
- `docs/engineering/harness-distribution/evidence/WO-DST-009-verification.md`

No other path is authorized without accountable review of an amended work order. The owner explicitly retired the transitional prototype-parity obligation after confirming that the canonical standard template is sufficient; this does not expand runtime behavior or authority.

## Required verification

Apply the relevant cases from `VER-DST-008`. At minimum, run formal artifact validation, focused Explorer WebUI tests, the complete standard-library suite, `harnessctl doctor`, twice-generated deterministic dashboard comparison, active/canonical template equality, JavaScript syntax or browser-load checks, hostile-content rendering checks, desktop and narrow-width visual review, keyboard review, CDN-failure fallback review, and `git diff --check`.

## Evidence to record

Retain the precise owner-directed refinements, changed paths, commands and exit codes, test counts, template hashes, deterministic snapshot hashes, browser widths, visual and keyboard observations, CDN and fallback observations, deviations, and residual risks in `docs/engineering/harness-distribution/evidence/WO-DST-009-verification.md`.

## Stop and escalate conditions

Stop if a change falls outside the two templates and necessary tests or evidence; changes canonical data or authority; changes the runtime dependency boundary; drops or renames harness concepts; weakens safe rendering, responsiveness, keyboard access, or fallback behavior; breaks managed parity or determinism; conflicts with another user's work; or requires commit, release, publication, or deployment authority.

## Completion report format

Report the owner-requested presentation changes, requirement and specification conformance, active/canonical parity, tests and manual review, snapshot and template hashes, deviations, residual risks, and the exact candidate path set.

## Implementation result

The owner-supplied Explorer template was integrated into the active and canonical copies. Review removed a duplicate lineage renderer, retained interactive lineage cards through an accessible group role, and preserved mobile navigation names while keeping the icon-only narrow layout. The refined semantic color lenses and legends, directional 3D links, card-based lineage, relation labels, zoom controls, gate styling, and responsive presentation operate on the unchanged canonical snapshot.

The redundant six-file `templates/webui/` directory is removed. `SPEC-DST-008`, `VER-DST-008`, the distribution index, and focused tests now state and enforce that the canonical standard template is the sole reusable WebUI source and the active root copy remains byte-identical. The managed lock contains the canonical newline-normalized digest. Focused tests, the complete suite, formal validation, doctor, deterministic real-repository generation, prior desktop and narrow-width browser review, interaction checks, and diff hygiene pass as recorded in the retained evidence. Commit-bound verification, commit, push, pull request, release, publication, and deployment remain separate decisions.
