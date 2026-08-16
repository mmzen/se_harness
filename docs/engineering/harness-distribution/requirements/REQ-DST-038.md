+++
id = "REQ-DST-038"
type = "requirement"
title = "Clear the Explorer artifact text filter directly"
status = "approved"
owners = ["product-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"
statement = "WHEN the Harness Explorer artifact text filter contains a value, THE SYSTEM SHALL provide a direct accessible control that clears only that value and immediately refreshes the applicable view without resetting the reader's other graph choices."
verification_method = "automated-test-and-manual-review"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Clear the Explorer artifact text filter directly

## Rationale

The top-right artifact filter can be cleared by manually selecting and deleting its text, and some browsers add an inconsistent native affordance for `type="search"`. A visible harness-owned control makes the operation predictable for mouse, keyboard, and assistive-technology users.

Clearing a text query is not the same operation as resetting the graph. Readers may deliberately retain an artifact-type filter, lifecycle filter, context depth, analysis mode, selection, or current view.

## Required response

- Place a dedicated clear control adjacent to the artifact text-filter field without removing the Snapshot Information control.
- Give the control an explicit accessible name and a visible non-color state.
- Disable the control when the text filter is empty and enable it when the field contains any value.
- On activation, clear only the text value, immediately apply the same filtering/rendering response as direct text editing, and return keyboard focus to the text field.
- Preserve artifact type, lifecycle, context depth, analysis mode, current view, and any selection that remains valid after recomputation.
- Continue to clear all applicable graph controls through the existing graph Reset action; do not make the new control a second reset operation.
- Preserve safe inert handling of repository-derived filter text and responsive top-bar behavior.

## Acceptance examples

### Clear a populated filter

**Given** the reader entered `SPEC-DST-007` and selected a non-default type, lifecycle, context depth, or analysis mode

**When** the reader activates the clear control

**Then** the text field becomes empty, results refresh immediately, focus returns to the field, and every other choice remains unchanged.

### Empty filter

**Given** the artifact text filter is empty

**When** the top bar renders

**Then** the clear control remains identifiable but disabled and does not cause layout movement.

### Keyboard and assistive use

**Given** the text filter contains a value

**When** a keyboard or assistive-technology user reaches the clear control

**Then** its purpose is announced as clearing the artifact filter and normal button activation performs the same operation as pointer activation.

## Out of scope

This requirement does not broaden search fields, change matching semantics, add persisted search history, introduce keyboard shortcuts, reset unrelated controls, alter canonical snapshot data, or change graph authority.
