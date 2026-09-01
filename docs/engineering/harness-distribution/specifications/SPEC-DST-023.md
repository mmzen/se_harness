+++
id = "SPEC-DST-023"
type = "specification"
title = "Designed self-contained Harness Explorer"
status = "approved"
owners = ["technical-owner", "product-owner", "quality-owner", "security-owner"]
created = "2026-09-01"
updated = "2026-09-01"

[relations]
specifies = ["REQ-DST-029", "REQ-DST-030", "REQ-DST-031", "REQ-DST-033", "REQ-DST-035", "REQ-DST-037", "REQ-DST-038", "REQ-DST-039", "REQ-DST-040", "REQ-DST-041", "REQ-DST-042", "REQ-DST-043", "REQ-DST-044", "REQ-DST-045", "REQ-DST-046", "REQ-DST-047", "REQ-DST-067", "REQ-DST-068"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-01T20:51:14Z"
decided_by = "technical-owner"
reason = "Approved by the accountable repository owner on 2026-09-01 by selecting the presented option 'Approve, start, complete on green (Recommended)', after reviewing the designed Explorer against the complete repository bundle in the local design loop and instructing its integration as the canonical template. The owner also accepted, by selecting 'Accept now, next design round fixes it (Recommended)', the recorded deviation that the Lineage view prefetches every artifact detail until a following design round loads details for the selected spine only."
+++

# Specification: Designed self-contained Harness Explorer

## Scope

Replace the canonical Explorer template with the designed page the repository
owner reviewed and selected on 2026-09-01, built deterministically from
retained sources into one self-contained document; extend the generator with
the indicators and proof fields that page presents; retire the runtime CDN;
and carry the Readiness view forward. The integrity-addressed bundle
(`SPEC-DST-013`), verified progressive access (`SPEC-DST-014`), and the
canonical snapshot boundary are unchanged.

This specification supersedes the presentation contracts `SPEC-DST-008`,
`SPEC-DST-010`, `SPEC-DST-011`, `SPEC-DST-012`, `SPEC-DST-016`, and
`SPEC-DST-017` once approved. Their verification contracts stay active,
because verified records bind them; `VER-DST-023` verifies the carried
requirements against the designed page beside them. The source-data,
determinism, and distribution obligations of `SPEC-DST-008` are carried
forward in rules 20-23 rather than dropped.

## Actors and external systems

- Repository readers open the generated page over a same-origin static HTTP
  host and inspect derived, read-only evidence.
- The candidate generator produces the bundle and embeds the bootstrap.
- The design session exports views; its exports are retained sources, not
  authority.
- No external system participates at runtime: the page requests only its
  own origin.

## Inputs

- Retained sources under `repository_tools/explorer_design/sources/`: the
  exported views `Overview.dc.html`, `Lineage View.dc.html`, `Graph.dc.html`,
  `Record.dc.html`; the component runtime `support.js`; the design-system
  `styles.css`; the vendored `vendor/react.production.min.js` and
  `vendor/react-dom.production.min.js` (React 18.3.1); the shell sources
  `shell/shell.html`, `shell/explorer.js`, `shell/readiness.css`.
- The validated canonical projection and the bundle-v2 manifest, summary,
  topology, readiness, artifact, and evidence resources.
- Untrusted repository text in every artifact field, body, and evidence file.

## Outputs

- `templates/repository/standard/scripts/harness_explorer/index.template.html`,
  one UTF-8 document of at most 524,288 bytes with exactly one
  `__HARNESS_BOOTSTRAP_JSON__` marker.
- The summary resource's `metrics` object; record details carrying
  `evaluator_evidence_path`, `evaluator_evidence_sha256`, and (release
  records) `distribution`; compact topology rows carrying `path` and, for
  release records, `version`, `released_at`, `distribution`; a repository
  `source_url`.

## State model

Per view: `loading` (identity from topology painted, record pending) ->
`verified` or `failed` (contained, with retry). Per resource: `requested` ->
`verified` (cached by path and digest) or `rejected`. Routing state lives in
the query string only: `view`, `artifact`, and for Readiness `subject`,
`gate`, `state`, `all`. No state persists beyond the page.

## Behavioral rules

1. The template is produced by
   `python -m repository_tools.explorer_design.build_explorer_template` from
   the retained sources; `--check` fails when the committed bytes differ from
   the build after line-ending normalization. A hand-edited template is a
   defect.
2. The build applies an explicit patch list to the exported views, each entry
   an exact replacement with the number of occurrences it must hit across
   named files; any other count fails the build. The patches only: remove
   the design-system link and script elements from each view's helmet;
   rewrite inter-view links to `?view=` routes and drop the design-rationale
   link; route data access through the shell (`bundle()`, `topology()`,
   `artifactResponse(id)`, `evidenceResponse(path)`); keep same-view deep
   links on the current view; replace `localStorage` with the shell's
   in-memory preferences; add the Readiness link to each navigation; give
   the Lineage text filter `type="search"`; and make the Overview read the
   generator's `metrics` when present, falling back to its detail fan-out
   otherwise, with its hard-coded example identifiers replaced by computed
   lists (missing coverage, delegated artifacts, drafts and ready records,
   the latest aggregate record).
3. Both vendored React builds must hash to the subresource-integrity digests
   the component runtime declares (`REACT_SRI`, `REACT_DOM_SRI`); the build
   refuses otherwise.
4. The stylesheet's single remote `@import` is removed; no `url(` remains.
   The Overview's token block becomes the document's base tokens; the
   Readiness stylesheet uses those tokens.
5. The document contains, in order: the head (charset, viewport, the CSP of
   rule 7, title, one style element), a `noscript` notice, a hidden failure
   surface, the root `<x-dc>` with one conditional import per designed view
   and a host element for Readiness, the bootstrap script, one runtime
   script, and the root logic script. Exactly three `<script` occurrences.
6. The runtime script concatenates the shell, a frozen registry mapping each
   view name to a `Blob` of its patched source, React, ReactDOM, and the
   component runtime. Embedded sources are JSON string literals with `<`,
   `>`, `&`, U+2028, and U+2029 escaped; the two vendored string literals
   spelling `<script` are respelled `\x3cscript`; the runtime's three
   `https://unpkg.com/` fallback origins are rewritten to
   `about:blank#vendored/`. The only URL-shaped literals the document may
   contain are the five W3C XML namespace identifiers and React's
   error-decoder pointer; none is requested.
7. The Content Security Policy is exactly
   `default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline' 'unsafe-eval'; img-src data:; connect-src 'self'; font-src 'none'; base-uri 'none'; form-action 'none'; object-src 'none'`.
   `'unsafe-eval'` exists because the component runtime compiles each view's
   logic with the `Function` constructor; the only inputs to that path are
   the template's own embedded sources.
8. The shell reads the bootstrap element, requires `harness-dashboard-bootstrap-v2`
   over `harness-dashboard-bundle-v2`, fetches the manifest with
   `credentials: same-origin`, `redirect: error`, `cache: no-cache`, checks
   byte length and SHA-256 against the bootstrap, requires the manifest
   revision to equal the bootstrap revision, and requires valid `summary`,
   `topology`, and `readiness` entrypoints.
9. Every resource path must match
   `dashboard-manifest.json | data/(summary|topology|readiness|artifacts)/<sha256>.json | content/<sha256>.txt`;
   every fetch verifies same origin, declared bytes, and SHA-256 before
   parsing; JSON resources must carry the descriptor's schema; identical
   in-flight requests are deduplicated; verified values are cached by path
   and digest for the page's life only. Resource revisions must equal the
   bootstrap revision; an artifact detail must carry the id its topology row
   declares.
10. The shell hands the views one flattened bundle: `source_url`,
    `repository_revision`, `repository`, `counts`, `lifecycle_counts`,
    `queue_counts`, `metrics`, `finding_rules_version`,
    `quality_gates_version`, `artifacts` (id, type, status, title, owners,
    authority, path, and for release records version and released_at),
    `relations` (declared and derived, unresolved targets excluded),
    `coverage`, `detail_ids`, and `distributions` keyed by release record.
    `data_root` is empty: evidence `raw_path` values are fetched as declared.
11. Routing: `view` is one of `overview`, `lineage`, `graph`, `readiness`;
    an unknown value falls back to `overview`, and an `artifact` parameter
    without a view opens `lineage`. Switching views is a document
    navigation. Selecting within a view uses `replaceState` on the current
    view's route. Readiness exposes `subject`, or `gate` and `state`, or
    `all`, and reduces any malformed value to its index.
12. Reader preferences (the navigation width) live in an in-memory store
    with the Storage interface; no `localStorage`, `sessionStorage`,
    cookie, or IndexedDB use exists in the document.
13. Overview: four trust tiles (requirement coverage with the missing
    requirements listed when coverage is incomplete, graph integrity, the
    evaluator's gate reading with rule and gate versions, release currency
    with the latest record's version, date, commit, and wheel digest); four
    accountability tiles (recorded and attributed decisions with the role
    distribution, delegated transitions and records with the delegated
    artifacts linked, refusals with the rejected and superseded artifacts
    linked, commit-bound verification with released-work coverage); three
    flow tiles (lead time median and p90 with n and the distribution, work
    in flight with each draft and ready record linked, release cadence with
    the last arc). Every figure comes from the bundle; with `metrics`
    present no artifact detail is fetched.
14. Lineage: a fixed six-stage board (Purpose, Definition, Design, Delivery,
    Assurance, Release by artifact type) over the working set; selecting an
    artifact lights its spine, the monotone closure over outgoing and
    incoming lineage relations excluding `superseded_by`; release records
    render a roster of released work with its verifying records; a search
    field of type `search` matches id or title, Enter selects the first
    result and Escape clears; an in-memory visit history offers back,
    forward, and visit chips labelled as navigation; the record panel
    (rule 16) opens beside the board; repository links use
    `source_url/blob/<revision>/<path>`.
15. Virtual Twin: every artifact on one canvas, clustered by the domain
    segment of its id, coloured by stage, brightened by status, sized by
    degree, laid out from a seed derived from the repository revision so two
    generations of one bundle render alike; lenses by stage, status, and
    domain dim and never remove; clicking a node opens a right rail hosting
    the record panel with `Open in Lineage`; the rail becomes a bottom sheet
    under 900 px; Escape clears the selection; a reduced-motion preference
    disables the settle animation.
16. Record panel: identity strip painted from topology before the detail
    arrives; type gloss; status; owners; decision trail listing every
    lifecycle event with `from -> to`, timestamp, decider (delegated actors
    styled distinctly), and the verbatim reason; proof block with commit,
    tag, version, `artifact_snapshot_sha256`, `evaluator_evidence_sha256`,
    and the distribution digests when present, each absent field omitted,
    never blank; verify commands; evidence rows with in-place text and
    text-less rows named and sized; EARS clauses of a requirement statement
    distinguished with the exact statement preserved; the rendered body
    collapsed by default; relation references open Lineage.
17. Readiness: derived from the readiness resource and the flattened bundle;
    G0-G5 gate rollup with clickable figures that list matching subjects;
    the subject view with gate groupings labelled as navigation, not policy,
    quality-gate evidence rows with state filters, findings naming the
    subject, and accountable owners; repository-wide commit-bound
    provenance, findings, and controlled outcomes. Every panel states that
    no approval, verification, or release decision is inferred.
18. Generator: `MAX_INDEX_BYTES = 524_288`; the summary's `metrics` object
    holds `lifecycle_events`, `unattributed_events`, `decided_by` (sorted),
    `delegated_transitions`, `delegated_records`, `delegated_artifacts`
    (sorted), `lead_times` (`id`, `hours` to two decimals, sorted by hours
    then id, approval to implementation), `released_work_orders`,
    `released_work_orders_verified`, `latest_release` (`id`, `version`,
    `released_at`, `commit`, `verification_record` via
    `includes_verification`), and `release_arc` (`contract_id` via
    `satisfies`, `contract_approved_at`, `released_at`, `hours`), each
    derived only from lifecycle events, declared relations, and front matter;
    record details carry `evaluator_evidence_path` and
    `evaluator_evidence_sha256`; release-record details carry the scalar
    string and integer fields of `[distribution]` under sorted keys of up to
    64 lowercase characters, strings up to 512 characters, or `null` when
    absent; compact topology rows carry `path`, and release records also
    `version`, `released_at`, `distribution`.
19. `repository.source_url` is the origin remote normalized to
    `https://github.com/<owner>/<name>` when it matches the https, ssh, or
    `git@` GitHub spellings; otherwise `null`. The page derives links only
    from that value, the bootstrap revision, and declared paths.
20. Carried forward: the canonical snapshot's sections, its absence of
    timestamps, and deterministic serialization remain as `SPEC-DST-008`
    rules 1-10 stated; presentation derives everything else in memory.
21. Carried forward: exactly one bootstrap marker with context-safe JSON
    escaping; transactional output promotion; twice-generated byte identity.
22. Carried forward: one managed template shipped in the package and
    reconciled at the root only through the supported upgrade transaction;
    customized copies are never overwritten.
23. Carried forward: repository text is inert in every rendering path;
    unknown artifact types render under their recorded names; readiness
    states are exactly `satisfied`, `unsatisfied`, `not_assessable`; no
    aggregate score exists.

## Error and recovery behavior

A missing or unsupported bootstrap, a `file:` origin, a manifest mismatch, or
a rejected resource surfaces in the requesting view (or the shell's failure
surface before any view) with the reason and a retry that repeats full
verification. Stale responses never paint over a newer selection. Nothing is
substituted, and no remote fallback exists.

## Data and interface contracts

- Bundle-v2 manifest, entrypoints, resource prefixes, and the verifier are
  unchanged; the additions of rule 18 are new fields inside existing
  resources.
- The flattened bundle of rule 10 is a browser-memory shape only.
- Requirement compliance carried by this specification:
  `REQ-DST-029`/`031` by rules 8-10, 18-21; `REQ-DST-030` by rules 13-17;
  `REQ-DST-033` by rules 1, 22; `REQ-DST-035` by rule 13; `REQ-DST-037` by
  the seven-character display with the full revision in the element title
  and the Readiness header; `REQ-DST-038` and `REQ-DST-041` by rule 14;
  `REQ-DST-039` by rule 15; `REQ-DST-040` by rule 14; `REQ-DST-042`,
  `043`, `044`, `045`, `046`, `047` by rule 16; `REQ-DST-067` by rules
  1-12, 17; `REQ-DST-068` by rules 18-19. `REQ-DST-032` and `REQ-DST-036`
  are superseded by `REQ-DST-067`.

## Security and privacy properties

No remote origin is named or requested. Vendored code is digest-verified at
build. Repository text enters the page only as data through React text nodes
and the shell's escaping; the `Function` evaluation path receives only the
template's embedded sources. No storage, cookie, telemetry, WebSocket, or
repository write exists. The shell verifies every byte it parses.

## Performance and capacity

`index.html` at most 524,288 UTF-8 bytes (431,072 at this revision); summary
at most 262,144; per-document 262,144 and total 16,777,216 unchanged;
topology acceptance target 2,097,152 (1,337,400 observed at `c065e3d`). The
Overview issues no per-artifact request when `metrics` is present.

Recorded deviation, accepted by the repository owner on 2026-09-01: the
designed Lineage view requests every artifact detail when it opens (1,224
same-origin, manifest-verified requests, about 7 MB at this revision) to
merge lifecycle facts into its board, where `SPEC-DST-014` rule 7 draws
Lineage cards from the compact topology alone. The owner accepted the
behaviour for this integration and directed a following design round to
load details only for the selected spine; until that round lands, rule 7
reads as amended for the Lineage view by this deviation.

## Observability

The generation summary keeps its byte measurements and digests. The Overview
displays the evaluator's own error, warning, and advisory counts with the
rule and gate versions of the projection, and every view names the revision.

## Compatibility and migration

The root template and generator remain the released copies until the next
adoption; consumer repositories receive the redesign through the ordinary
managed upgrade; the Pages publication workflow and allowlist are unchanged;
historical dashboards and records are untouched. Design rounds re-export
into the retained sources and rebuild; a drifted patch target fails the
build and is re-aligned deliberately.

## Examples and counterexamples

- Intended: `index.html?view=graph&artifact=RLS-SEH-021` opens the
  constellation with that node selected, its rail showing commit `3dcde4b`,
  tag `v0.12.0`, and wheel digest `639edbee...`.
- Intended: `?artifact=WO-ECP-024` opens Lineage with the delegated start and
  completion visible in the trail, each with its check-run reference.
- Invalid: a view that fetches `artifacts/<id>.json` directly, a stylesheet
  `@import`, a second `<link>`, or a `localStorage` call.
- Invalid: a template committed without a matching build, or a generator
  that fabricates a distribution digest when the table is absent.

## Explicitly unspecified decisions

The design's copy, colour values, spacing, animation curves, and card
anatomy are accepted as implementation input from the retained sources. The
build tool's module layout, the Readiness markup, and screenshot viewports
are the implementation agent's. Any change to a designed view outside the
patch list is a new design round, not an implementation choice.
