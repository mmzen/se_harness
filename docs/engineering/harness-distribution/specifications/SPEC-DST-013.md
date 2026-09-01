+++
id = "SPEC-DST-013"
type = "specification"
title = "Deterministic sharded Explorer bundle"
status = "approved"
owners = ["technical-owner", "security-owner", "quality-owner", "release-owner"]
created = "2026-08-17"
updated = "2026-09-01"

[relations]
specifies = ["REQ-DST-048", "REQ-DST-049", "REQ-DST-054", "REQ-DST-055"]
+++

# Specification: Deterministic sharded Explorer bundle

## Scope and authority

Replace the generated monolithic `harness-dashboard-snapshot-v1` HTML embedding with a deterministic static bundle whose small shell, summary, topology, readiness, per-artifact details, and retained content can be loaded independently. This changes the generated dashboard data interface, not formal artifact authority, validation, lifecycle, evidence meaning, verification, release, publication authorization, or source-repository state.

## Actors and external systems

- `harnessctl dashboard` owns local deterministic generation and never publishes.
- The validator-owned artifact model remains the only canonical input projection.
- The repository-specific Pages packager validates a selected generated bundle and publishes only after its separate explicit trigger.
- A static HTTP origin serves inert generated files. It performs no application computation.
- The Explorer browser verifies and consumes resources under `SPEC-DST-014`.

## Inputs

- validated repository, artifacts, relations, findings, readiness, provenance, and retained-content selections;
- the owned Explorer template and generation limits;
- the exact observed Git revision and object format;
- the existing explicit Pages governance snapshot and publication inputs.

## Outputs

One transactional output tree containing:

```text
index.html
dashboard-manifest.json
generation-summary.json
data/summary/<sha256>.json
data/topology/<sha256>.json
data/readiness/<sha256>.json
data/artifacts/<sha256>.json
content/<sha256>.txt
```

The implementation may use equivalent fixed directory names, but every nonroot data filename is a lowercase SHA-256 plus a controlled extension and every resource appears exactly once in the manifest.

## State model

Generation progresses `projected -> partitioned -> serialized -> hashed -> manifest-bound -> recursively-verified -> promoted`. Any failure before promotion discards the temporary tree and preserves the previous valid output. Publication separately progresses `selected -> governor-validated -> manifest-validated -> exact-set-validated -> packaged`; it never repairs or completes a bundle.

## Behavioral rules

1. Build the canonical in-memory projection once from validator-parsed data. Sharding must not parse a second artifact model or change relation semantics.
2. Emit `dashboard-manifest.json` with schema `harness-dashboard-bundle-v2`, repository revision, Git object format, resource descriptors, and semantic entry points for summary, topology, readiness, and artifact details.
3. A descriptor contains controlled relative path, role, UTF-8 byte count, lowercase SHA-256, and JSON schema where applicable. The manifest enumerates every generated data and content resource but does not include itself or create a self-hash cycle.
4. Embed only a bounded bootstrap in `index.html`: bundle schema, repository revision, manifest path, expected manifest byte count, and expected manifest SHA-256. Do not embed the manifest, complete snapshot, artifact bodies, or evidence bodies.
5. The summary resource contains repository identity, validation state, aggregate metrics, lifecycle distribution, queue counts, finding summaries, and only the minimum identifiers needed to route views. It contains no graph, artifact body, or evidence body.
6. The topology resource contains one compact node per artifact and exact declared/derived relations needed by Overview, search, adjacency, Lineage, labels, and history. Nodes retain ID, title, type, state, assurance classification, authority, and their manifest-controlled artifact-detail descriptor, but no Markdown body.
7. The readiness resource contains readiness subjects, gates, explicit findings, revision provenance, experiments, coverage observations, and evidence indexes needed by Readiness, but no artifact or evidence body.
8. Emit one artifact-detail JSON resource per formal artifact. It contains exact metadata, dates, applicable type-specific fields, statement, safe body projection metadata and Markdown, relation presentation inputs not already in topology, and evidence descriptors. It does not duplicate evidence body text.
9. Retained evidence remains one passive `content/<sha256>.txt` resource per distinct included content digest. Artifact details reference its exact path, size, digest, path identity, associations, and state.
10. Normalize line endings and serialize JSON deterministically with stable property and collection ordering. Identical accepted inputs produce an identical recursive tree.
11. Construct every output path from generator-owned constants and verified lowercase digests. Repository IDs and paths may appear as inert data but never directly select output paths.
12. Apply existing per-document and total-content limits before serialization. Enforce the shell and summary limits from `REQ-DST-055` before promotion and report every resource size plus totals by role.
13. Write through one temporary sibling tree, reject path collisions and unsafe parents, verify the exact recursive set, recompute bytes/digests, then atomically promote using the existing rollback boundary.
14. Update the Pages packager to accept only the root files and manifest-declared resources, verify all descriptors and the observed governance revision, reject additional/missing files and redirects, and copy bytes unchanged.
15. Keep all publication provenance, governor isolation, explicit workflow triggers, and no-authority language unchanged.

## Error and recovery behavior

Reject unknown schemas, duplicate JSON keys, unsafe paths, unsupported roles/media, duplicate paths, conflicting content, noncanonical digest names, malformed descriptors, bytes outside declared bounds, digest mismatch, incomplete resources, added files, promotion failure, or governance-revision mismatch. No fallback re-embeds the monolith, reads repository files from the browser, or publishes a subset.

## Data and interface contracts

- `index.html` bootstrap is the trust root for the manifest path, size, digest, schema, and observed revision.
- Manifest descriptors are the only browser and publisher resource allowlist.
- JSON resources are UTF-8 objects with explicit supported schema identifiers and duplicate-key rejection in Python-side validation.
- Artifact-detail lookup is carried by compact topology node descriptors; an unknown ID has no guessed path.
- Generation summary remains noncanonical operational metadata and binds the index and manifest digests, resource counts, role totals, omitted content, and observed revision.

## Security and privacy properties

Treat all repository content and paths as untrusted. Preserve path containment, regular-file checks, race checks, content limits, inert Markdown, no remote media, and explicit public-disclosure language from `SPEC-DST-012`. The bundle does not add secret scanning or redaction. Publishing still exposes every manifest-declared resource.

## Performance and capacity

- `index.html` maximum: 524,288 UTF-8 bytes.
- summary maximum: 262,144 UTF-8 bytes.
- artifact/evidence source maximum: existing 262,144 bytes each.
- combined projected-content maximum: existing 16,777,216 bytes.
- current repository topology acceptance target: 2,097,152 bytes, measured before HTTP compression.
- Larger consumer topology is reported, not treated as a formal-graph error; topology sharding requires separate authority.

## Observability

Print and record bundle schema, revision, resource counts, per-role byte totals, largest resource, omitted-document counts, total output bytes, manifest digest, and deterministic summary digest. These are size/integrity observations, never health or assurance scores.

## Compatibility and migration

Newly generated output uses bundle v2. Historical self-contained v1 HTML remains unchanged and readable by its embedded code. The current Explorer does not combine a v2 shell with v1 data or silently downgrade. Update canonical and active managed generator/template copies, lock hashes, focused tests, package data, consumer generation, Pages packaging, and publication documentation together. Direct `file://` viewing is replaced by documented static HTTP serving.

## Examples and counterexamples

- Valid: summary loads first, topology later, one artifact detail on selection, and one evidence file on expansion.
- Valid: two artifacts share one identical evidence content file through the same digest descriptor.
- Invalid: `index.html` still contains the serialized `artifacts` collection.
- Invalid: a manifest trusts `data/artifacts/REQ-DST-049.json` constructed from an artifact ID.
- Invalid: Pages copies every file found below `data/` without matching it to the selected manifest.
- Invalid: gzip alone is used to justify retaining the monolithic parse and memory cost.

## Explicitly unspecified decisions

The implementation agent may choose internal Python structures, compact JSON property ordering, request helper names, deterministic cache implementation, and exact summary partitioning within the stated roles. Stop if implementation requires a server API, persistent browser database, service worker, new runtime origin, topology sharding, weakened digest/path checks, or changes to formal governance semantics.

## Amendment record

**The shell budget rises to 524,288 UTF-8 bytes, proposed 2026-09-01 under `WO-DST-023`
(`SPEC-DST-023`, `ADR-DST-013`).** The designed Explorer inlines its component
runtime, both React production builds, the design-system stylesheet, and its
view components into one self-contained document so that no script ships as
a bundle resource and no remote origin is requested; that document measures
431,072 bytes at revision `c065e3d`. The summary, per-document, and
total-content maxima and the topology acceptance target are unchanged, and
no artifact body or evidence is embedded. Nothing else in this specification
changes.
