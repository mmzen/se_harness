+++
id = "REQ-DST-045"
type = "requirement"
title = "Navigate every resolved relation reference"
status = "approved"
owners = ["product-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"
statement = "WHEN a reader selects a resolved artifact reference in the Relations tab, THE SYSTEM SHALL focus that exact artifact through the reversible Lineage navigation session."
verification_method = "automated-browser-test"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Navigate every resolved relation reference

## Rationale

The current Relations tab prints both relation endpoints but exposes a separate focus control only for the other endpoint. Making resolved artifact IDs themselves consistently interactive reduces interpretation and navigation friction.

## Preconditions and trigger

This requirement applies to source, target, and via-artifact references rendered from declared or derived relation records in the focused artifact's Relations tab.

## Required response

- Render every resolved artifact ID reference as a keyboard-operable artifact control.
- Preserve relation name, source-to-target direction, authority, via path, and missing-target meaning.
- Selecting a different artifact uses the ordinary Lineage visit operation, updates the board and detail panel, and appends or branches the bounded history.
- Selecting the current artifact is a safe no-op and creates no consecutive duplicate visit.
- Restore focus predictably after the detail and board rerender.

## Failure and boundary behavior

An unresolved target is explicit non-interactive text and is never substituted with another artifact. Self-relations, reverse relations, repeated references, parallel relations, and derived via paths remain safe and deterministic.

## Constraints

- A click records only reader navigation, never a new formal relation or evidence item.
- Preserve the 20-visit sliding-window and current-visit reveal contract of `REQ-DST-041`.
- Do not change relation direction, name, authority, resolution, or canonical data.

## Acceptance examples

### Example: target navigation

**Given** a visible relation `SPEC-DST-012 -> REQ-DST-045`,

**When** the reader selects `REQ-DST-045`,

**Then** it becomes the selected Lineage artifact and the visit appears in Navigation history.

### Example: unresolved target

**Given** a relation references a missing target,

**When** the Relations tab is rendered,

**Then** the missing ID remains visible and explicitly unresolved but cannot be activated.

## Open decisions

None when approved.
