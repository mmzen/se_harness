+++
id = "ARCH-DST-004"
type = "architecture"
title = "Portable explanatory graph boundary"
status = "implemented"
owners = ["technical-owner", "documentation-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-09-08"

[relations]
addresses = ["REQ-DST-014"]
conforms_to = ["SPEC-DST-004"]

[decision_assessment]
outcome = "adr_required"
triggers = ["public-interface-or-protocol", "technology-framework-vendor-or-external-service", "material-alternatives"]
rationale = "ADR-DST-004 chose paired narrative, inline semantic Mermaid and a complete textual fallback over four alternatives. It adds a renderer-dependent element to the same file PyPI publishes as package metadata."
assessed_by = "technical-owner"
+++

# Architecture: Portable explanatory graph boundary

## Components and responsibilities

- **User-perspective narrative**: demonstrates delegation, review, and decision rights without requiring users to operate the harness control plane directly.
- **Inline Mermaid source**: provides one repository-native, reviewable definition of the representative graph and its semantic styling.
- **Textual fallback**: carries the complete value proposition when Mermaid is displayed as source rather than rendered as a visual diagram.
- **Root README**: remains the single GitHub and package-index description and the only implementation surface for the narrative and graph.
- **Focused static tests**: protect placement, semantic stages, authority boundaries, accessibility cues, and absence of external rendering dependencies.
- **Formal artifact graph**: remains authoritative; the README graph is a derived explanatory model only.

## Dependency direction

```text
approved packet --------------------> README narrative + Mermaid source
formal artifact semantics ----------> representative node and edge labels
human authority model --------------> decision diamonds and narrative boundaries
README text ------------------------> renderer-independent value explanation
Mermaid-capable renderer -----------> optional colored visual presentation
focused tests ----------------------> deterministic static conformance
```

No README renderer, diagram, Explorer view, package-index page, badge, or test result grants formal authority.

## Trust and rendering boundaries

- Treat Markdown rendering capability as external and variable.
- Do not execute JavaScript, load remote styles, or depend on an externally mutable image to communicate required meaning.
- Keep the graph small enough that its fenced source remains intelligible.
- Preserve labels and decision shapes so color is supplementary.
- Do not imply that the illustrative API example is implemented by this repository.
- Do not equate a visual edge with a validated formal relation unless the underlying repository artifacts establish it.

## Required patterns

- One narrative and one graph in the root README.
- Human decisions and agent execution use different labels, shapes, and colors.
- Commit-bound verification precedes the later governance decision that marks a record verified.
- Release authorization remains downstream and separate.
- Explorer connections are dotted to show derived observation rather than approval or artifact authority.
- Standard-library tests inspect source without network or rendering dependencies.

## Prohibited patterns

- A screenshot or generated image as the only graph source.
- An external Mermaid runtime, remote stylesheet, or dynamic build-time graph generation.
- A second README for PyPI or a renderer-specific copy of the narrative.
- A graph that makes automation the approval, assurance, or release actor.
- Replacing the formal artifact model or five Explorer questions with the example.

## Quality attributes and conformance

The section shall be concise, reviewable as plain Markdown, visually legible on a Mermaid-capable renderer, and understandable without the visual rendering. Conformance is checked by `VER-DST-004`, the existing public-onboarding contract, the complete regression suite, graph validation, doctor, preflight, dashboard generation, and manual README review.

## Amendment record

**Typed `addresses` and `conforms_to` relations replace the legacy
`constrains` relation and a decision assessment is recorded, amended
2026-09-08 under `WO-AUT-005` (`SPEC-AUT-003`, `ADR-DST-004`).** The addressed
requirement becomes `REQ-DST-014` and `conforms_to` names `SPEC-DST-004`, the
active specification that specifies it. The assessment reads the drivers and
rejected options of `ADR-DST-004`, the one active ADR that decides this
architecture. Title, status, statement and ADR relations are unchanged.
