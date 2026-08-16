+++
id = "REQ-DST-039"
type = "requirement"
title = "Distinguish Explorer graph categories by color"
status = "approved"
owners = ["product-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"
statement = "WHEN Harness Explorer colors graph nodes by state, artifact type, or assurance, THE SYSTEM SHALL assign every category in that analysis mode a stable distinct color while retaining authoritative text labels and non-color cues."
verification_method = "automated-test-and-manual-review"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Distinguish Explorer graph categories by color

## Rationale

The current hash-to-five-color mapping can assign the same color to different categories. In assurance mode, for example, `attention` and `not_assessed` can both appear light green; artifact-type analysis necessarily collides when more than five types are visible. The legend names remain authoritative, but exact duplicate colors undermine the purpose of the analysis lens.

## Required response

- Maintain an independent deterministic color map for each analysis mode: lifecycle state, artifact type, and derived assurance signal.
- Give every distinct category present in one mode's complete normalized snapshot a distinct color in that mode.
- Keep a category's color stable when text, type, lifecycle, or context-depth filters change the visible subset.
- Apply the same category color to root matches and context nodes; retain size and text as their non-color distinction.
- Preserve selected-node amber as a temporary selection override and restore the category color when selection clears.
- Keep category names in the graph legend and analysis lens. Color supplements labels and must never become authority or evidence.
- Handle an unknown future category deterministically without changing canonical data, schema, network behavior, or repository state.

## Acceptance examples

### Assurance analysis

**Given** `attention`, `assured`, `decision_required`, and `not_assessed` are present

**When** the reader selects assurance analysis

**Then** the four legend entries and their nodes use four distinct stable colors.

### Type analysis

**Given** all current formal artifact types are present

**When** the reader selects artifact-type analysis and changes graph filters

**Then** every type has a distinct color and a type's color does not change merely because another type becomes hidden.

### Non-color interpretation

**Given** a reader cannot distinguish two colors reliably

**When** the graph and lens render

**Then** category labels, counts, node labels, match/context sizing, and selected-node emphasis still communicate the applicable meaning.

## Out of scope

This requirement does not change artifact categories, lifecycle or assurance derivation, canonical snapshot data, selected-node meaning, graph filtering, focused Lineage, readiness decisions, or accessibility authority.
