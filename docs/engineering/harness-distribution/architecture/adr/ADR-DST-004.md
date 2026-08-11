+++
id = "ADR-DST-004"
type = "adr"
title = "Pair a user story with a semantic Mermaid graph and text fallback"
status = "approved"
owners = ["technical-owner", "product-owner", "documentation-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
decides = ["ARCH-DST-004"]
+++

# ADR: Pair a user story with a semantic Mermaid graph and text fallback

## Status

Accepted.

## Context

The root README is operationally complete but makes readers assemble the practical value of governed coding-agent work from several detailed sections. A short story can establish that value quickly, while a graph can make traceability, human decisions, evidence, exact revision provenance, and release separation visible at a glance.

The same README is also package metadata. GitHub explicitly supports Mermaid diagrams, while other Markdown renderers may preserve a `mermaid` fence as code rather than produce a visual diagram. Required meaning therefore cannot depend on visual rendering alone.

## Decision drivers

- Sell practical value before deep reference material.
- Keep routine harness mechanics with the coding agent and accountable authority with humans.
- Preserve one reviewable README and avoid duplicated or generated public content.
- Make semantic categories visible without relying on color alone.
- Retain a useful fallback without JavaScript, network access, or external styles.
- Keep the formal graph and Explorer authoritative only within their existing boundaries.

## Considered options

1. **Keep only the detailed reference sections**: rejected because the value remains slow to discover.
2. **Add only a conversational example**: useful but does not make the resulting traceability and decision structure visible.
3. **Add only Mermaid**: rejected because it overemphasizes mechanics and may degrade to source on some renderers.
4. **Commit a static image and make it the primary explanation**: rejected because image production, link portability, accessibility, and synchronization add another maintenance surface.
5. **Pair concise narrative, inline semantic Mermaid, and complete textual fallback**: proposed because it is repository-native, reviewable, visually effective where supported, and still meaningful as plain Markdown.

## Decision

Add one `What this looks like in practice` section after the quick start. Use a representative API rate-limiting request to show user approval and assurance decisions around agent-operated preflight, implementation, evidence, and provenance. Follow it with one semantically styled Mermaid graph and a concise textual statement of the resulting value.

Use named `classDef` groups with high-contrast text. Use diamonds for architecture, assurance, and release decisions; use labels and dotted Explorer relations so meaning survives without color. Do not use external CSS, scripts, images, or generated fragments.

## Consequences

GitHub readers receive a colored visual explanation. Renderers without Mermaid visualization may show the graph source, so the surrounding prose must remain complete and the source must stay compact. The focused tests gain a small static contract for section placement, meaning, and graph semantics. The README becomes slightly longer but offers a faster path to understanding why the deeper workflow exists.

## Validation

Apply `VER-DST-004`, retain the existing `VER-DST-003` public-onboarding checks, manually inspect Markdown source and a Mermaid-capable rendering, run the full repository suite and harness diagnostics, and defer package-index rendering observation to a future authorized release inspection.

## Revisit conditions

Revisit if the package-index experience makes the fenced source materially harmful, if the graph grows beyond a compact example, if a stable renderer-neutral diagram format becomes available without a second source of truth, or if accessibility review identifies an unresolved barrier.
