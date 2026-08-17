+++
id = "REQ-DST-041"
type = "requirement"
title = "Provide reversible Lineage navigation history"
status = "approved"
owners = ["product-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"
statement = "WHEN a reader follows artifact selections in focused Lineage, THE SYSTEM SHALL retain a bounded reversible navigation history so earlier and later focused boards can be restored without representing visits as formal artifact ancestry or governance relations."
verification_method = "automated-test-and-manual-review"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Provide reversible Lineage navigation history

## Rationale

Selecting a current Lineage card immediately replaces the board root. The existing repository-and-artifact text looks like a breadcrumb but records neither earlier selections nor a hierarchy. Readers cannot safely explore and return without remembering artifact IDs or restarting from another view.

The interface needs browser-like navigation semantics while remaining explicit that the visit trail is presentation state, not evidence and not a formal graph path.

## Preconditions and trigger

This requirement applies when a reader enters focused Lineage from Overview, another Explorer action, or a prior Lineage selection and then selects one or more visible artifact cards.

## Required response

- Label the control as `Navigation history` or equivalent non-hierarchical wording; do not present it as formal ancestry.
- Retain an in-memory ordered history of focused artifact IDs with a current cursor and a separate initial artifact.
- Provide keyboard-operable Back and Forward controls, clickable visited-artifact chips, and a direct Return to initial artifact action.
- Selecting a different card appends it after the current cursor. Selecting the current artifact does not add a consecutive duplicate.
- Navigating Back, Forward, or to an existing history chip moves the cursor without rewriting history. Selecting a new card after moving backward removes the abandoned forward branch before appending the new selection.
- Keep at most 20 visit entries as a sliding window. When the bound is exceeded, remove the oldest non-current visit while retaining the separate Return to initial artifact action and report the bounded behavior accessibly.
- After every visit or history action, reveal the current visit within the horizontally scrollable history region, including when it would otherwise be outside the rendered area. Revealing it must not scroll the page or replace the focus behavior of the selected card or activating history control.
- Restoring a history entry must restore the same selected artifact and focused-board semantics for the current snapshot and depth setting.
- When Overview or another external Explorer route opens a new focused Lineage, start a new navigation session whose initial entry is that artifact.
- Keep the current entry and disabled control states visually and programmatically identifiable without color alone.
- Move focus predictably after rerendering and preserve ordinary button semantics for keyboard and assistive-technology users.

## Failure and boundary behavior

If a history entry no longer resolves in the loaded snapshot, disable or skip that entry with an explicit unavailable state; never substitute a different artifact. Empty history, one-entry history, repeated non-consecutive visits, cycles, and rapid selection must remain safe.

Reloading the generated page starts a new history. Navigation state must not be written into formal artifacts, canonical snapshot data, URLs, browser history, local storage, cookies, analytics, or repository files.

## Constraints

- Navigation history is a reader convenience only. It is not declared or derived lineage, validation evidence, accountable approval, or provenance.
- Preserve exact artifact IDs and the authoritative relation and detail routes.
- Preserve safe inert rendering, bounded state, responsive access, and managed-template parity.
- Do not change graph relations, lifecycle state, readiness, VREC/RLS authority, release behavior, or repository content.

## Acceptance examples

### Example: reversible exploration

**Given** the reader focuses `REQ-DST-040`, then selects `SPEC-DST-011`, then `WO-DST-012`,

**When** the reader activates Back twice and Forward once,

**Then** the focused board restores `REQ-DST-040`, then `SPEC-DST-011`, then `SPEC-DST-011` remains current after the forward action, with visited entries still available.

### Example: branch after back

**Given** the visit history is `A`, `B`, `C` with `B` current,

**When** the reader selects `D`,

**Then** the history becomes `A`, `B`, `D` and Forward is disabled.

### Example: current visit remains visible

**Given** 20 retained visits extend beyond the visible width of the Navigation history region,

**When** a new visit is appended or the reader activates Back, Forward, a retained visit, or Return to initial,

**Then** the 20-entry sliding window is preserved and the current visit is automatically brought fully into the history region without moving page scroll or stealing focus.

### Example: authority boundary

**Given** the visible history includes two artifacts with no direct formal relation,

**When** the reader inspects the history,

**Then** the interface describes them only as visits and does not draw or report a formal relation between them.

## Open decisions

None when approved.
