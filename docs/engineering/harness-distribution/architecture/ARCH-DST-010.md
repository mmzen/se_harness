+++
id = "ARCH-DST-010"
type = "architecture"
title = "Integrity-addressed progressive Explorer bundle"
status = "implemented"
owners = ["technical-owner", "security-owner"]
created = "2026-08-17"
updated = "2026-08-19"

[relations]
addresses = ["REQ-DST-049", "REQ-DST-050", "REQ-DST-052", "REQ-DST-054", "REQ-DST-055"]
conforms_to = ["SPEC-DST-013", "SPEC-DST-014"]

[decision_assessment]
outcome = "adr_required"
triggers = ["responsibility-or-dependency-direction", "public-interface-or-protocol", "data-ownership-or-persistence", "security-privacy-or-trust-boundary", "deployment-or-operating-model", "concurrency-consistency-reliability-or-failure-strategy", "material-performance-scalability-or-cost-tradeoff", "cross-cutting-policy", "material-alternatives"]
rationale = "Replacing one embedded canonical snapshot with asynchronously fetched static resources changes the generated public interface, data partition and ownership, browser/publisher trust chain, static serving contract, failure and race strategy, caching, performance tradeoffs, and migration boundary; these are coherent significant decisions with material alternatives."
assessed_by = "technical-owner"
+++

# Architecture: Integrity-addressed progressive Explorer bundle

## Context and scope

`ARCH-DST-009` safely projects repository bodies into one embedded snapshot, but the resulting page now embeds about 2.57 MB of data above its approximately 103 KB UI shell. The generated bundle separately contains a nearly 2.97 MB snapshot and passive evidence copies. This architecture preserves the one-way validator-to-Explorer projection while partitioning its generated representation so readers pay content cost progressively.

The scope begins after canonical in-memory projection and ends at a verified static resource rendered in one browser panel. It includes deterministic sharding, manifest integrity, transactional output, Pages packaging, same-origin fetch, cache/race containment, and local HTTP serving. It excludes formal graph semantics, repository mutation, application servers, publication authority, assurance decisions, and topology sharding beyond the current compact dataset.

## Components and responsibilities

- The validator/parser remains owner of formal artifact identity, body separation, relations, findings, and readiness inputs.
- The bundle partitioner derives summary, compact topology, readiness, per-artifact detail, and digest-shared evidence from one in-memory projection.
- The deterministic serializer/manifest builder owns schemas, ordering, controlled paths, byte counts, SHA-256, entry points, and the noncyclic HTML bootstrap binding.
- The transactional writer owns recursive exact-set verification, temporary-tree containment, rollback, and promotion.
- The Pages packager independently revalidates the selected manifest, governance revision, paths, bytes, hashes, and exact set before copying.
- The browser resource loader owns same-origin fetch, preparse integrity verification, revision-scoped in-memory cache, request deduplication, cancellation, and stale-response suppression.
- Existing Explorer view and safe-content renderers own presentation only and receive verified typed resources.
- Static HTTP hosting serves inert bytes; it owns no application or governance logic.

## Dependency direction

```text
validator-owned canonical projection
  -> deterministic bundle partitioner
  -> content-addressed resource bytes
  -> versioned manifest
  -> bounded index bootstrap

explicit Pages publication
  -> independent manifest/exact-set validation
  -> static HTTP origin
  -> browser bootstrap + verified progressive loader
  -> existing Overview / Lineage / Readiness renderers
```

Browser state, timing, cache, failure, and rendered DOM never flow back into generator inputs, formal artifacts, evidence, lifecycle, verification, release, or publication authority.

## Data and control flow

Generation builds one canonical projection, partitions it without semantic rewriting, serializes child resources, computes their identities, writes the manifest, binds its digest into the shell, recursively verifies the temporary tree, and promotes it. Publication validates the already-generated tree against the selected governance revision and copies bytes unchanged.

At runtime the shell verifies the manifest and summary. View entry requests topology or readiness. Artifact visit requests one detail, and explicit evidence expansion requests one passive content resource. Every response is size/digest verified before parsing or rendering. A revision-scoped cache stores only verified values; request tokens prevent old completion from winning over newer navigation.

## Trust boundaries

Repository content, IDs, paths, Markdown, URLs, artifact metadata, generated directories, HTTP responses, caches, and hosting behavior are untrusted. The index bootstrap trusts only controlled fields generated in the same transaction. Manifest and resource SHA-256 protect integrity, not authenticity against a malicious party able to replace both the published HTML and data; release/Pages governance remains the authenticity and authorization boundary.

Same-origin static fetch is allowed. Redirects outside the expected resource identity, arbitrary repository fetches, unverified parsing, persistent caches, remote content services, and executable repository content are prohibited. The existing exact graph CDN exception remains isolated and receives no repository payload.

## Required patterns

- One canonical in-memory projection with several deterministic generated representations.
- Coarse summary/topology/readiness resources plus per-artifact and digest-shared evidence resources.
- Controlled or content-addressed paths and one versioned exact-set manifest.
- Noncyclic bootstrap-to-manifest binding.
- Verify bytes before JSON/UTF-8 parsing and before Markdown rendering.
- Same-origin static HTTP, revision-scoped bounded in-memory caching, in-flight deduplication, and stale-response suppression.
- Panel-local loading/error/retry states and preserved verified unrelated data.
- Transactional generator output and independent publication validation.
- Explicit byte budgets and factual size observations.

## Prohibited patterns

- Full snapshot or body/evidence collections embedded in `index.html`.
- Gzip/minification as the sole response to monolithic acquisition and parsing.
- Repository IDs or paths used directly as generated resource names or browser URLs.
- A backend API, database, service worker, persistent content cache, telemetry, or runtime repository access.
- Parsing or rendering before declared size and SHA-256 verification.
- Cache reuse across manifests, stale response overwrites, silent empty-data fallback, or retry without full checks.
- Manifest self-hash cycles, publisher directory globs, partial publication, or implicit deployment.
- Treating payload size, resource success, cache state, or loaded content as assurance.

## Quality attributes

The design prioritizes fast first comprehension, deterministic reproducibility, explicit integrity, hostile-input safety, static portability, bounded failure, navigation continuity, browser accessibility, cache correctness, managed distribution parity, and observable size. It accepts more generated files and on-demand requests to avoid paying for unused content.

## Conformance checks

`VER-DST-013` proves schemas, deterministic partitioning, controlled paths, exact manifest/resource hashes, budgets, recursive transaction behavior, publication validation, static portability, managed distribution, and unchanged authority. `VER-DST-014` proves verified fetch ordering, deferred network behavior, cache and race invariants, history continuity, panel-local recovery, hostile resources, safe rendering, CSP, accessibility, and browser performance.

## Dependency reassessment: 2026-08-19

The repository owner's revision of `REQ-DST-055` and `SPEC-DST-013` raises only the generated shell ceiling from 153,600 to 262,144 UTF-8 bytes. The separately authorized fragment and History API presentation state remains within the browser-navigation responsibility already assigned by this architecture and persists no canonical content. The static bundle protocol, data ownership, manifest trust chain, progressive acquisition, same-origin boundary, in-memory cache, failure containment, publication model, and all other budgets remain unchanged. The architecture therefore continues to conform without a new significant structural decision; `ADR-DST-010` records the corresponding reaffirmation.

## Related ADRs

`ADR-DST-010` records the proposed choice of a content-addressed static bundle with coarse view resources, per-artifact details, and explicitly expanded evidence. It must be accepted before this architecture and its work orders may be approved.
