+++
id = "ADR-DST-009"
type = "adr"
title = "Project repository Markdown through a bounded local content pipeline"
status = "approved"
owners = ["technical-owner", "security-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-19"

[relations]
decides = ["ARCH-DST-009"]
+++

# ADR: Project repository Markdown through a bounded local content pipeline

## Status

Accepted.

Reassessed on 2026-08-19 against the directory-aware evidence-path convention in `SPEC-EVK-001`. The selected bounded local content pipeline remains applicable because discovery still supplies only safe repository-local associations and all content, rendering, capacity, and publication controls are unchanged.

## Context

Explorer currently embeds deterministic artifact metadata and evidence paths. The proposed detail experience requires complete artifact bodies, safe evidence rendering, and raw evidence links that work in a standalone generated bundle. Repository Markdown is untrusted and may contain active HTML, dangerous links, remote media, excessive content, or paths that escape intended roots. The distribution currently has no Python runtime dependencies and permits only one explicit runtime CDN URL for optional Overview topology.

## Decision drivers

- Complete human-readable artifact and evidence context.
- Preserve the canonical snapshot as the sole persisted data boundary.
- Deterministic snapshot hashing and static output.
- No new runtime network dependency or hosted repository-content service.
- Strong hostile-content, path-containment, and active-link controls.
- Portable local and GitHub Pages behavior without vendor-specific source URLs.
- Bounded package, memory, browser, and generated-output cost.
- Compatibility with historical snapshots and managed consumer upgrades.

## Considered options

1. Keep paths only and open repository files directly. Rejected because standalone and Pages dashboards cannot reliably resolve local repository paths and the requested integrated reading experience is absent.
2. Fetch Markdown or rendered HTML from GitHub or another hosted service at runtime. Rejected because it is vendor-specific, requires network and authentication policy, can disclose repository identity, and makes the detail view externally available only.
3. Load a Markdown/EARS parser from a CDN and render raw repository content in the browser. Rejected because it expands the accepted executable CDN boundary, weakens availability and supply-chain controls, and does not by itself sanitize active content.
4. Pre-render arbitrary Markdown to HTML in the generator and treat the HTML as trusted. Rejected because parser output still needs an explicit sanitization boundary and persisted HTML creates a stronger executable-content interface.
5. Add optional raw Markdown/evidence records to the canonical snapshot, enforce deterministic bounds and content hashes in the generator, render through locally distributed parser plus sanitizer code, and emit digest-named passive raw evidence files. Selected.

## Decision

Adopt option 5. Preserve `harness-dashboard-snapshot-v1` and its existing fields; add optional content fields that older consumers can ignore. Reuse `Artifact.body`, select evidence only through governed associations and safe roots, normalize line endings, enforce a 256 KiB per-document limit and a 16 MiB total projection limit, and record whole-document omissions explicitly.

Markdown rendering is local and two-stage: parsing with raw HTML disabled, followed by an explicit allowlist sanitizer. No new runtime URL is permitted. The implementation may choose the concrete locally packaged parser/sanitizer after license, package, security, deterministic-output, and fresh-install checks; if no acceptable combination preserves the distribution constraints, implementation must stop for a revised decision rather than ship a home-grown unsafe full parser.

Evidence raw links target passive `content/<sha256>.txt` files within the generated bundle. The generator derives names from computed content hashes, verifies nested output containment and completeness transactionally, and never turns repository paths into output names or vendor-specific URLs.

EARS highlighting uses a small deterministic local tokenizer over the exact canonical statement. It is explanatory only and falls back to exact unclassified text; it is not a syntax validator and does not use Prism or another CDN.

## Consequences

Artifact and evidence context becomes inspectable in one static Explorer. Generated bundles and canonical snapshots become larger, so deterministic limits and omission states are visible product behavior. The package may gain reviewed local rendering/sanitization assets or dependencies, increasing distribution and upgrade verification. The sanitizer and path/output logic become security-critical test surfaces.

Publishing a bundle publishes its included artifact bodies, evidence bodies, and raw evidence copies. This is intentional only after the existing explicit publication action; generation remains local and nonpublishing. No secret-scanning or redaction assurance is implied.

Historical dashboards remain unchanged. Older v1 consumers ignore additive fields; the updated Explorer remains compatible when the optional fields are absent.

## Validation

`VER-DST-012` checks hostile HTML and URL payloads, no remote media or new runtime request, parser failure fallback, path traversal and symlink rejection, digest/raw-copy equality, deterministic budget selection and omission, recursive transactional rollback, twice-generated equality, v1 snapshots with and without content, EARS ambiguity fallback, full relation-history navigation, public-disclosure wording, managed/package parity, and fresh installation.
