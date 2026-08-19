+++
id = "VER-DST-012"
type = "verification"
title = "Verify content-rich Explorer artifact details"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-16"
updated = "2026-08-19"

[relations]
verifies = ["REQ-DST-042", "REQ-DST-043", "REQ-DST-044", "REQ-DST-045", "REQ-DST-046", "REQ-DST-047"]
+++

# Verification Contract: Verify content-rich Explorer artifact details

## Independence

Expected metadata, content identity, Markdown safety, EARS clause meaning, relation direction/authority, history semantics, evidence associations, capacity behavior, assurance vocabulary, and publication boundaries come from the six requirements, `SPEC-DST-012`, `ARCH-DST-009`, `ADR-DST-009`, existing canonical snapshot contracts, and formal repository artifacts. Verification must not derive acceptance from implementation-specific CSS, parser internals, DOM selectors, library marketing claims, or visual similarity alone.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-DST-042` | snapshot fixtures, browser assertions, and metadata comparison | every current artifact type, optional/missing fields, hostile metadata, long title/path, narrow width | heading is exact ID-title; dates and applicable canonical fields are present and inert; irrelevant fields are omitted; no authority is inferred |
| `REQ-DST-043` | deterministic content fixtures, hostile-input tests, parser/sanitizer review, browser fallback | headings, lists, tables, code, links, raw HTML, active URLs, remote images, malformed/empty/oversized Markdown | safe structures are readable; exact text remains; active content and requests are impossible; omissions and fallback are explicit; output is bounded and deterministic |
| `REQ-DST-044` | tokenizer property tests and accessibility review | ubiquitous, event, state, optional, unwanted, combined, mixed-case, punctuation, hostile, ambiguous, long statements | recognized clauses are stable and non-color-readable; exact statement is preserved; ambiguity becomes unclassified, never a validation claim |
| `REQ-DST-045` | browser state/history tests and relation fixtures | source, target, via, self, reverse, parallel, repeated, missing, current artifact, branch after back, 20-entry bound | every resolved ID is operable; selected artifact, board, detail, focus, and history agree; current is no-op; unresolved remains noninteractive; relation meaning is unchanged |
| `REQ-DST-046` | filesystem/security fixtures, output inspection, browser review, and publication-boundary checks | keyed work-order evidence, VREC paths, duplicate content, missing/unsafe/symlink/non-UTF-8/oversized files, collision, rollback, standalone serving | associations, path, size, digest, rendered content, raw link, and omission are correct; raw bytes match digest; no escape or incomplete promotion; disclosure is explicit |
| `REQ-DST-047` | semantic-state table, DOM/accessibility assertions, and responsive review | all current types/states, four assurance signals, requirement coverage combinations, unknown future values | Type, State, and Assurance are independently named; ready is decision required; coverage appears only as named requirement metadata; color is supplementary |

## Canonical projection and capacity fixtures

- Compare every projected artifact body with validator-parsed `Artifact.body`, including LF normalization, UTF-8 byte count, SHA-256, and empty-body state.
- Assert existing v1 snapshot fields and meanings are byte-for-byte unchanged apart from expected additive optional content and evidence-document fields.
- Load an older v1 fixture without optional content and confirm the current Explorer remains usable with explicit unavailable content.
- Use files at 0, 1, 262143, 262144, and 262145 bytes; assert the exact per-document boundary and whole-document omission.
- Cross 16,777,216 total bytes with shuffled discovery order; assert deterministic canonical ID/path selection, explicit omissions, stable counts, and no partial document.
- Generate twice from identical state and assert identical snapshot JSON, raw content filenames/bytes, HTML, and canonical snapshot SHA-256. Generation time remains outside canonical data.

## Markdown security and rendering tests

- Exercise headings, paragraphs, emphasis, strong text, lists, quotes, rules, inline/fenced code, tables, safe relative raw links, and allowed HTTP(S) links.
- Exercise script/style/iframe/object/embed/form/custom elements, SVG/MathML, raw HTML, `javascript:`, `data:`, protocol-relative URLs, encoded protocols, event attributes, CSS, remote images, broken nesting, and parser edge cases.
- Assert no repository-derived markup, selector, style, event handler, network request, executable URL, opener access, or active media survives.
- Assert renderer or sanitizer failure displays escaped exact text and a visible notice without breaking tabs, Lineage, Readiness, or provenance.
- Inspect dependency/version/license/package provenance and confirm no runtime URL beyond the accepted exact 3D graph URL.

## EARS tests

- Tokenize representative ubiquitous, event-driven, state-driven, optional-feature, unwanted-behavior, and combined EARS statements with mixed case and punctuation.
- Concatenate accessible token text and assert exact equality with the original statement.
- Assert clause names and non-color cues are available to assistive technology and no result says valid, invalid, compliant, approved, or verified.
- Exercise nested/repeated `WHEN`/`IF`, absent `SHALL`, multiple `SHALL`, hostile text, and long input; assert deterministic bounded unclassified fallback.

## Relation and history tests

- Render declared and derived relation records with resolved source, target, and via IDs; activate each resolved reference and assert the exact focused artifact.
- Assert the shared `visitLineage` path applies forward-branch truncation, no consecutive duplicate, 20-entry sliding bound, current-chip reveal, and predictable focus.
- Assert source-to-target direction, relation name, authority, via list, self-relation, parallel relation, and unresolved target text are unchanged after interaction.
- Assert an unresolved target has no artifact control and cannot select a similarly named artifact.

## Evidence filesystem and output tests

- Cover flat-filename and directory-component work-order discovery under `SPEC-EVK-001`, VREC `evidence_paths`, deduplication, multiple associations, identical contents, and stable ordering.
- Reject absolute paths, traversal, alternate separators, symlinks/junctions escaping the root, directories, devices, nonregular files, non-UTF-8 bytes, unsafe extensions where applicable, and files changed during generation.
- Assert each included evidence SHA-256 equals `content/<sha256>.txt`, raw bytes, projected Markdown, and displayed metadata.
- Force nested-directory creation, filename collision, incomplete expected file set, write failure, and promotion failure; assert no partial output replaces the previous valid dashboard and rollback stays within the intended output parent.
- Serve the output as a standalone static directory and assert every raw link resolves without GitHub or repository-host assumptions.

## Semantic-label tests

- Evaluate the complete current type/state/assurance cross-product and unknown values. Assert exact text, dimension prefixes, accessible names, deterministic visual tokens, and no collision that makes adjacent labels indistinguishable.
- Assert verified/released artifacts are `assured`, ready artifacts are `decision_required`, explicit attention conditions are `attention`, and the remaining artifacts are `not_assessed` according to the approved derivation.
- For each requirement coverage combination, assert specification and verification-contract coverage are independently named in Overview. Assert no nonrequirement gets `Not applicable` definition coverage.
- Confirm the former unnamed header coverage badge is absent.

## Architecture, distribution, and regression checks

- Assert `ARCH-DST-009` addresses only the significant content/trust requirements, conforms to `SPEC-DST-012`, records `adr_required`, and is decided by selected `ADR-DST-009` before approval.
- Assert direct canonical snapshot dependency direction, inert browser-to-repository boundary, validator authority, no aggregate score, and explicit publication authority remain intact.
- Reconcile every changed managed generator, Explorer template, and local asset through the supported upgrade transaction; assert canonical/active byte parity, schema-2 lock hashes, protected governor controls, and idempotence.
- Verify package metadata/data, wheel and sdist contents if dependencies/assets change, fresh-environment installation, init/adopt/upgrade/doctor, and `harnessctl dashboard` in a consumer fixture.
- Run current Explorer regressions for Overview 3D/fallback, filters, semantic colors, bounded context, Lineage board/history, detail tabs, Readiness, provenance, responsive behavior, CSP, snapshot embedding, unknown types, and hostile content.
- Run formal validation, start/review preflight when lifecycle allows, focused tests, complete standard-library tests, JavaScript/browser load, `git diff --check`, and twice-generated deterministic output.

## Manual assessments

At desktop and narrow widths, review ID-title scanability, metadata density, long Markdown, document outline, table/code overflow, EARS meaning without color, three semantic-label dimensions, relation-link affordance, history/focus behavior, multiple evidence expansion, raw-link portability, omission notices, and explicit publication disclosure. Confirm content is useful without making Explorer look like an editor or a source of assurance authority.

## Evidence retention

Retain exact commands and exit codes, fixture bytes and digests, snapshot diffs, content budgets and selection order, renderer/sanitizer versions and configuration, hostile payload outcomes, observed network requests, EARS token tables, relation-history transitions, raw output tree and hashes, rollback cases, accessibility and responsive observations, managed/package parity, consumer installation, changed paths, deviations, residual risks, and publication status under `docs/engineering/harness-distribution/evidence/WO-DST-013-verification.md`.

## Residual uncertainty

Allowlisted Markdown cannot reproduce every Markdown extension, and clause highlighting cannot fully interpret natural-language requirements. Evidence can contain sensitive information that no generic renderer can identify reliably. Safe fallback, explicit omissions, deterministic limits, no active content, no validation claim, explicit publication authority, and accountable review constrain but do not eliminate those risks.
