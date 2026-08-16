# WO-DST-011 implementation and verification evidence

## Authority and boundary

On 2026-08-16 the repository owner explicitly authorized implementation of `WO-DST-011`. The approved work order classifies commit-bound verification as required. This evidence records candidate implementation checks only; it does not create a candidate commit, verify a VREC, authorize release, update the public demonstrator, publish a package, or deploy software.

Start preflight passed with `WO-DST-011` approved before source changes. The work order then moved to `in_progress`. The selected intent, capability, `REQ-DST-035..039`, `SPEC-DST-010`, and `VER-DST-010` were read with the complete managed policy manifest. Before candidate commit, owner review identified duplicate semantic colors and authorized the bounded correction retained in `REQ-DST-039` and the amended specification, verification contract, and work order.

## Implemented mapping

- `REQ-DST-035`: removed the unbounded Overview Definition Coverage panel and its `coverageRows` renderer. The compact coverage metric, canonical coverage array, node-level coverage labels, focused Lineage, and artifact detail remain.
- `REQ-DST-036`: added the exact `0 / 1 / 2` context selector, deterministic multi-root breadth-first traversal over resolved incident relations, a 100-context-node budget, explicit truncation, match/context counts, size-based non-color distinction, and stale graph-selection clearing. Stored relation direction and authority are unchanged.
- `REQ-DST-037`: sidebar status now labels an observed revision, visibly abbreviates only complete 40- or 64-character hexadecimal values to 12 characters plus `…`, retains the complete value in Snapshot Information and screen-reader text, and applies generic long-token containment.
- `REQ-DST-038`: added a stable native `Clear artifact filter` button. It is disabled for an empty field, clears only the text query, refreshes through the existing render path, preserves other graph controls and valid selection, and returns focus to the search field.
- `REQ-DST-039`: replaced the collision-prone hash-to-five-color function with independent deterministic state, type, and assurance maps built from the complete normalized snapshot. Each current category in one mode receives a distinct stable color; selected amber, labels, counts, and match/context size cues remain separate.

The reviewed prototype structure, three views, visual identity, focused Lineage, Readiness, optional CDN-backed `3d-force-graph@1.79.0`, CSP, canonical snapshot schema, generator, CLI, and authority model remain unchanged.

## Managed distribution transaction

The reusable source was changed only at `templates/repository/standard/scripts/harness_explorer/index.template.html`. Candidate `harnessctl upgrade .` planned one managed update and protected `.engineering-harness.toml` and `.github/workflows/engineering-harness.yml`. Explicit `upgrade . --apply` updated `scripts/harness_explorer/index.template.html` and its schema-2 lock digest; a second plan reported no update.

Canonical and active template raw SHA-256 after LF normalization are both:

`f04e120e3977f789ebea0a2c4e4d5cbe1e28480d59453e788ffef958b3e44562`

The lock records the same normalized digest. No protected self-hosting control, generator, workflow, package metadata, dependency, or runtime URL changed.

## Automated checks

| Check | Result |
| --- | --- |
| Focused `tests.test_dashboard_webui` | PASS — 12 tests |
| Complete `unittest` discovery | PASS — 220 tests, 3 expected skips |
| `harnessctl validate .` | PASS — 399 artifacts, 0 errors, 42 pre-existing maintenance warnings |
| `harnessctl doctor .` | PASS — managed Explorer template and lock unchanged |
| Candidate-source start preflight | PASS — `WO-DST-011` approved |
| Candidate-source review preflight | PASS — `WO-DST-011` implemented with retained evidence |
| Managed upgrade replay | PASS — protected controls plus 32 unchanged managed files; no update |
| `python -m se_harness --help` | PASS — public command surface unchanged |
| Two consecutive final dashboard generations | PASS — identical snapshot SHA-256 `245dfecb825cce787c6792b7485b19d97c225863f7794bcc922636d1bdd064c3` |
| `harnessctl inspect .` | PASS — no active work; `WO-DST-011` correctly reported as awaiting commit-bound verification |
| `git diff --check` | PASS |

Focused assertions cover removal of the table/renderer, preservation of compact and artifact-level coverage, exact depth options, iterative budgeted traversal markers, role-based node sizing, reset behavior, clear-control semantics, SHA-1/SHA-256 format gating, full canonical revision retention, twelve unique palette entries, stable mode-specific map construction, removal of hash/modulo assignment, safe text rendering, responsive containment, active/canonical parity, and the unchanged accepted CDN URL.

## Browser interaction and accessibility review

The generated dashboard was served only on temporary localhost and inspected in the in-app browser. The pinned 3D renderer loaded successfully and browser logs contained no warnings or errors.

- Exact query `SPEC-DST-007`: depth 0 reported `1 MATCHES · 0 CONTEXT`; depth 1 reported 10 context nodes and 40 resolved relations; depth 2 reported 32 context nodes and 130 resolved relations.
- Dense filtered scope: 28 roots retained, exactly 100 context nodes added, and `TRUNCATED AT 100 CONTEXT NODES` reported.
- Clear action: emptied only search, became disabled, returned focus to `search`, and preserved assurance mode, specification type, implemented lifecycle, and depth 2.
- Post-implementation owner feedback before candidate commit aligned keyboard focus with the visual control group: focus on either the search field or enabled clear button now draws one blue outline around both controls, while Snapshot Information remains outside the group.
- State analysis rendered 6 categories with 6 computed colors. Type analysis rendered all 12 formal artifact types with 12 computed colors. Assurance analysis rendered 3 categories with 3 computed colors: `Attention` was green and `Not Assessed` was purple rather than both light green.
- Narrowing assurance analysis to requirement roots retained the complete-snapshot color for `Not Assessed`; changing the visible subset did not recolor the retained category. Graph/lens/legend rendering produced no browser warning or error.
- Reset action: restored state mode, all types, all states, empty search, disabled clear control, and depth 0.
- Repository status exposed visible `be6d91ac37df…` and screen-reader text containing the complete observed revision; Snapshot Information continued to use the full canonical value.
- At 390×844, search, clear, and Snapshot Information remained visible with no horizontal page overflow. At 1024×768, the 232-pixel sidebar contained the repository status and the Overview controls wrapped without overlap.
- Match/context/truncation meaning remained textual and node size distinguished match, context, and selected states independently of semantic color.

## Governor separation observation

Candidate preflight, tests, validation, doctor, and rendering were executed from the editable candidate environment and are evidence only. The exact v0.3.0 governor wheel named by `.self-hosting/governor.toml` was separately downloaded and its SHA-256 `260e22371b05e5bb6c59143a1f0229855305a6bf7994984be50aa147a02ea516` verified. A diagnostic direct preflight from that older governor rejected current v0.4.0 graph and managed-file semantics, including routine work orders that validly omit non-applicable architecture. It made no repository change.

The configured CI does not use v0.3.0 to preflight the current graph: candidate-source review preflight uses the candidate implementation, while the isolated released governor proves its identity and later runs `accept-candidate` against the exact non-promotable candidate wheel and commit. That independent acceptance remains unavailable until a candidate commit exists and is not claimed here.

## Deviations and residual risk

No approved product or architecture deviation was required. The graph remains a force-directed visual whose final spatial arrangement is not deterministic; deterministic membership, textual counts, focused Lineage, and explicit truncation constrain interpretation. The optional 3D topology still depends on the accepted pinned unpkg resource; the documented textual fallback remains. Twelve-character revision prefixes are presentation only and may collide; complete canonical values remain authoritative.

Two final dashboard-generation attempts made under the restricted filesystem sandbox could not replace temporary target directories and returned Windows access-denied diagnostics. Repeating the same authorized local-only command with the repository write boundary enabled succeeded twice with the identical snapshot digest recorded above; this was an execution-environment retry, not a product or evidence deviation.

The 42 validator warnings are the repository's existing maintenance observations and are unrelated to this work. The public release-bound demonstration remains unchanged and continues to represent its released snapshot.
