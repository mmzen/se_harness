+++
id = "ARCH-DST-009"
type = "architecture"
title = "Bounded repository-content Explorer pipeline"
status = "implemented"
owners = ["technical-owner", "security-owner"]
created = "2026-08-16"
updated = "2026-09-01"

[relations]
addresses = ["REQ-DST-043", "REQ-DST-046"]
conforms_to = ["SPEC-DST-023"]

[decision_assessment]
outcome = "adr_required"
triggers = ["public-interface-or-protocol", "data-ownership-or-persistence", "security-privacy-or-trust-boundary", "technology-framework-vendor-or-external-service", "material-performance-scalability-or-cost-tradeoff", "cross-cutting-policy", "material-alternatives"]
rationale = "Projecting and publishing artifact and evidence bodies changes the canonical snapshot and static-bundle interfaces, moves untrusted Markdown across an active browser boundary, requires a renderer/sanitizer strategy and deterministic capacity limits, and creates material alternatives for portable source access and disclosure control."
assessed_by = "technical-owner"
+++

# Architecture: Bounded repository-content Explorer pipeline

## Context and scope

`ARCH-DST-008` establishes the canonical snapshot as Explorer's only persisted data boundary and keeps repository strings inert. The detail panel now needs artifact and evidence bodies, which are larger and structurally richer than the current metadata/path projection. This architecture extends that one-way pipeline without creating a second model or letting Markdown become executable repository code.

The scope begins at validator-parsed artifact bodies and governed evidence references and ends at deterministic snapshot fields, safe rendered DOM, and passive raw content files inside the generated dashboard bundle. Formal validation, relation authority, assurance decisions, repository writes, publication authority, and external hosting remain outside the component.

## Evidence-keying reassessment

The 2026-08-19 reconciliation of `REQ-DST-046` and `SPEC-DST-012` expands governed discovery from filename-only keys to the exact path-component convention in `SPEC-EVK-001`. The content pipeline still receives only repository-contained, nonsymlink evidence associations from the managed generator and retains the same projection, sanitization, capacity, output, and publication boundaries. No component, dependency direction, trust boundary, or decision outcome changes.

## Components and responsibilities

- The existing validator/parser owns front-matter/body separation and formal artifact identity.
- The content projector owns allowed-path resolution, UTF-8 reading, line-ending normalization, byte limits, SHA-256, deterministic ordering, omission records, and additive snapshot fields.
- The dashboard output writer owns collision-resistant raw evidence names, nested path containment, transactional completeness, rollback, and generation-summary counts.
- The locally distributed Markdown renderer and sanitizer own allowlisted presentational structure and escaped fallback; they own no lifecycle or validation inference.
- The EARS tokenizer owns presentational clause segmentation only.
- The Lineage detail controller owns curated metadata, semantic labels, relation navigation through the existing visit operation, evidence expansion, and focus restoration.
- The explicit Pages publication workflow remains the only component that can transmit the generated bundle.

## Dependency direction

```text
validated Artifact.body + governed evidence references
  -> bounded deterministic content projector
  -> additive harness-dashboard-snapshot-v1 fields + content/<sha256>.txt
  -> locally distributed Markdown renderer/sanitizer
  -> inert detail DOM and reversible Lineage navigation

explicit publication action
  -> complete already-generated static bundle
```

No browser content, navigation state, rendered HTML, or publication result flows back into artifacts, validation, evidence selection, assurance, verification, or release records.

## Data and control flow

Artifacts reuse the parser's existing body. Evidence paths pass through allowlisted-root, regular-file, symlink, encoding, size, and digest checks. Accepted content enters deterministic optional snapshot fields; accepted evidence also receives a digest-named raw file. Omitted content retains identity and reason. Browser rendering consumes only embedded data and generated local raw links.

The snapshot remains the verification-hashed payload. Raw content files are deterministically derived from and checked against projected SHA-256 values; generation summary records counts and bytes outside the canonical hash input's time-free data.

## Trust boundaries

All Markdown, paths, links, artifact statements, titles, metadata, and evidence are untrusted. Raw HTML and active content are prohibited. Repository paths never select dashboard output names. Renderer output is sanitized after parsing, and failure falls back to escaped text. External links cannot obtain opener access. No repository data is sent to the existing graph CDN or another network destination.

A generated bundle containing content may later become public. Generation is local and nonpublishing; publication is a separate explicit authority action and exposes the complete selected bundle. Automatic secret detection or redaction is not claimed.

## Required patterns

- One additive canonical snapshot contract; no persisted detail-only schema.
- Parser-owned body extraction and allowlisted evidence selection.
- Per-document and total deterministic capacity limits with whole-document omission.
- SHA-256 content identity and generator-owned raw filenames.
- Local pinned Markdown rendering plus post-render allowlist sanitization.
- Raw HTML disabled, no remote media, and no new runtime URL.
- Text plus non-color semantics for EARS and artifact labels.
- Transactional recursive output verification and rollback.
- Explicit publication disclosure and unchanged publication authority.

## Prohibited patterns

- Reading arbitrary paths named by repository content, following unsafe links, or copying nonregular files.
- Rendering repository HTML directly or trusting a Markdown parser without sanitization.
- CDN Markdown/EARS dependencies, runtime content fetch, telemetry, or hosted rendering.
- Vendor-specific repository URLs inferred from local paths.
- Silent truncation, nondeterministic budget selection, or incomplete raw links.
- Treating highlighted EARS, rendered evidence, definition coverage, or content presence as validation or assurance.
- Browser-to-repository mutation or navigation history as formal lineage.

## Quality attributes

The architecture prioritizes hostile-input safety, deterministic provenance, semantic fidelity, bounded memory/output, portable static review, graceful fallback, accessibility, managed distribution parity, and explicit disclosure. Rich Markdown fidelity is subordinate to inert rendering and stable generation.

## Conformance checks

`VER-DST-012` verifies additive snapshot compatibility, content hashes and budgets, path/symlink containment, hostile Markdown, link protocols, no runtime URLs, raw-copy integrity, transaction rollback, EARS fallback, relation-history reuse, semantic-label distinctions, deterministic generation, package parity, browser behavior, and publication disclosure.

## Related ADRs

`ADR-DST-009` decides this architecture.

## Amendment record

**The conformance target moves from `SPEC-DST-012` to `SPEC-DST-023`, amended
2026-09-01 under `WO-DST-023`.** `SPEC-DST-012` is superseded by `SPEC-DST-023`, whose
rule 16 carries the bounded, inert rendering of artifact bodies, EARS
statements, and retained evidence this architecture conforms to. Nothing
else in this architecture changes.
