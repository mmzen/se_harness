# Harness Explorer brand and semantic tokens

The interface is precise, calm, and evidence-led. Visual polish must make relationships easier to inspect without making derived observations look authoritative.

## Typography

- Display: `Aptos Display`, then `Segoe UI`, then system sans-serif.
- Body: `Aptos`, then `Segoe UI`, then system sans-serif.
- IDs, commits, paths, and relation names: `SFMono-Regular`, `Consolas`, then monospace.
- No remote fonts.

## Core palette

- Page: `oklch(0.982 0.006 255)`
- Surface: `oklch(1 0 0)`
- Ink: `oklch(0.238 0.024 255)`
- Muted: `oklch(0.505 0.022 255)`
- Border: `oklch(0.882 0.014 255)`
- Accent: `oklch(0.49 0.16 255)`
- Topology field: `oklch(0.19 0.025 255)`

Artifact-stage colors distinguish intent, capability, requirement, definition, delivery, and release/operation. Unknown types use the neutral definition color.

## Semantic states

- Satisfied: green plus explicit text.
- Unsatisfied or validator error: red plus explicit text.
- Warning or `not_assessable`: amber plus explicit text.
- Derived observation: blue, a `derived` label, and dashed topology edges where applicable.
- Superseded or historical: neutral gray plus lifecycle text and successor relation.
- Selected artifact: amber outline plus `aria-current` or selected-state semantics.

Color is never the only carrier of type, lifecycle, authority, gate state, or selection. Maintain visible keyboard focus and readable contrast on every surface.

## Layout

Use square panels, thin borders, generous whitespace, compact monospace metadata, and one dominant topology field. At narrow widths, stack inspectors and tables without hiding any of the five Explorer questions or their underlying evidence.
