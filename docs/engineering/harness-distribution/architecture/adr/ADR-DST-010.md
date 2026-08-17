+++
id = "ADR-DST-010"
type = "adr"
title = "Content-addressed static sharding for progressive Explorer access"
status = "approved"
owners = ["technical-owner", "security-owner", "product-owner"]
created = "2026-08-17"
updated = "2026-08-17"

[relations]
decides = ["ARCH-DST-010"]
+++

# ADR: Content-addressed static sharding for progressive Explorer access

## Status

Accepted by the accountable repository and technical owner through the 2026-08-17 instruction `go for implementation` after the progressive-loading proposal and packet scope were established.

## Context

The current Explorer is operationally simple and self-contained, but its generated HTML is about 2.68 MB because all artifact and evidence bodies are embedded. The complete snapshot is duplicated in `dashboard-data.json`, and evidence is duplicated again as raw content. GitHub Pages compression reduces transfer but not full download, parse, memory, or unused-content cost.

The dashboard must remain deterministic, static, portable, read-only, safe for untrusted repository Markdown, and explicitly published. The browser needs complete compact topology for search and lineage, but it rarely needs all bodies or evidence. Moving data outside HTML creates new integrity, partial-failure, and local-serving responsibilities.

## Decision drivers

- Make the initial page proportional to the UI and summary rather than repository content volume.
- Keep Overview/Lineage relationships usable without loading all bodies.
- Load artifact and evidence content only when requested.
- Preserve deterministic output, exact revision provenance, transactionality, and independent Pages validation.
- Avoid an application backend, database, persistent browser store, or new runtime dependency/origin.
- Retain current safe Markdown/EARS behavior and explicit authority boundaries.
- Contain asynchronous failure and race behavior visibly and testably.

## Considered options

1. Keep the single embedded snapshot and rely on gzip/minification. Rejected: it retains full acquisition, parsing, memory, duplication, and regression risk.
2. Split only by page into three large JSON files. Rejected: simpler, but artifact and evidence bodies still arrive in bulk when Lineage opens.
3. Emit a deterministic static manifest, coarse summary/topology/readiness resources, per-artifact detail resources, and digest-shared evidence loaded on expansion. Selected.
4. Add an HTTP API/database for search and details. Rejected: it changes deployment, operation, trust, authentication, cost, and offline generation far beyond the need.
5. Use a service worker or IndexedDB to install the whole bundle locally. Rejected: it adds persistent cache/version/security complexity and does not improve first access sufficiently.
6. Encode one binary/compressed snapshot and range-read it. Rejected: GitHub Pages range behavior, browser decoding, random access, schema tooling, and debugging are less portable and more complex than static JSON/text resources.

## Decision

Adopt `harness-dashboard-bundle-v2` as a generated static bundle. Keep `index.html` as a bounded UI shell containing only a small bootstrap that binds the expected manifest path, revision, byte size, and SHA-256. Partition data into summary, compact topology, readiness, one content-addressed detail resource per artifact, and digest-shared passive evidence files.

The manifest is the exact resource allowlist and contains size/hash/role/schema descriptors without hashing itself. Generation verifies and promotes the recursive bundle transactionally. The Pages packager independently verifies the selected revision and exact manifest-declared set. The browser fetches only same-origin descriptors and verifies bytes before parsing or rendering.

Load summary first, topology for Overview/Lineage, readiness on entry, one detail on artifact visit, and one evidence body on explicit expansion. Cache only verified data in memory for one manifest; deduplicate requests, cancel when practical, and suppress stale completion unconditionally. Keep panel-local loading/error/retry states and all existing navigation/authority semantics.

## Consequences

Positive consequences include a shell near 100 KB rather than 2.68 MB, bounded initial data, no initial Markdown bodies, browser caching of immutable resources, reusable shared evidence, and failures isolated below the complete application. Static hosting and Python standard-library generation remain sufficient.

Negative consequences include hundreds of small generated resources, additional schema and publisher code, asynchronous UI states, hash work in the browser, more security/race tests, and loss of supported direct `file://` opening. Local review must use a static HTTP server. Large topology remains one growing resource; further sharding is deliberately deferred.

Security consequences are mixed: fetching creates more substitution surfaces, mitigated by bootstrap/manifest/resource hashes, same-origin constraints, controlled paths, exact-set publication, preparse verification, and existing sanitization. Hashes do not authenticate a malicious replacement of the whole published site; accountable publication governance remains necessary.

Migration is forward-only for newly generated output. Historical v1 HTML remains self-contained. Generator, Explorer, managed templates, lock data, tests, Pages packager, and documentation must move together.

Include positive, negative, operational, security, and migration consequences.

## Validation

Run `VER-DST-013` and `VER-DST-014`: deterministic twice-generation and recursive diff; manifest/schema/path/hash/size and tamper cases; output rollback; publisher exact-set/revision checks; browser request tracing; no-body startup assertions; topology/readiness deferral; one-artifact/one-evidence fetch; Web Crypto preparse verification; cache/race/failure injection; history and safe-render regressions; static HTTP and `file://` behavior; payload budgets; CSP; full managed installation/upgrade parity; and complete repository tests.
