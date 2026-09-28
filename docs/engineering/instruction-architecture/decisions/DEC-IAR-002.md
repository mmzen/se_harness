+++
id = "DEC-IAR-002"
type = "decision"
title = "Scope of obsolete-guide retirement"
status = "decided"
owners = ["repository-owner", "technical-owner"]
created = "2026-09-28"
updated = "2026-09-28"
kind = "question"
question = "Should this evolution stop shipping the six compatibility guides product-wide, or only remove eligible copies from this repository?"
raised_by = "Codex"
recommendation = "product-wide"

[[options]]
id = "product-wide"
label = "Stop seeding the six guides in a future release, preserve existing owner files, and adopt the change separately in this repository."

[[options]]
id = "repository-only"
label = "Keep shipping compatibility guides and prepare only a bounded cleanup of this repository after consumer checks."

[[options]]
id = "retain"
label = "Keep the six pointers for now and implement only plugin qualification and active-reference corrections."

[relations]
concerns = ["REQ-IAR-028", "SPEC-IAR-015", "VER-IAR-017", "WO-IAR-022"]
blocks = ["REQ-IAR-028", "SPEC-IAR-015", "VER-IAR-017", "WO-IAR-022"]

[disposition]
option = "product-wide"
label = "Stop seeding the six guides in a future release, preserve existing owner files, and adopt the change separately in this repository."
decided_by = "repository-owner"
decided_at = "2026-09-28T07:46:06Z"
reason = "For DEC-IAR-012: product wide retirement."

[[lifecycle_events]]
from = "open"
to = "decided"
decided_at = "2026-09-28T07:46:06Z"
decided_by = "repository-owner"
reason = "For DEC-IAR-012: product wide retirement."
+++

# Scope of obsolete-guide retirement

## Question and facts

The six guides contain 210 words in total and no unique current policy. Their
removal is primarily a discoverability improvement; it is not a large startup
context saving. Current templates and the exposed plugin cache still contain
legacy references. The report's temporary-copy probe proves lock reconciliation,
not consumer compatibility.

## Options and consequences

- **product-wide:** Complete WO-IAR-021 first, then implement WO-IAR-022 under
  REQ-IAR-028/SPEC-IAR-015. New installations omit the guides. Existing owner
  files stay intact. Packaging and supported-upgrade tests add work; the result
  avoids generating obsolete routes in every new repository.
- **repository-only:** Keep distributed templates. Prepare a new bounded adoption
  WO after active-host qualification and exact file review. Replace the current
  retirement drafts before approval; do not approve their broader contract under
  this option. Other repositories continue to receive the pointers.
- **retain:** Preserve compatibility now. WO-IAR-020 and WO-IAR-021 may proceed
  independently. Do not approve the retirement drafts. Revisit after compatible
  plugins are proven in use and the remaining consumer list is empty.

## Recommendation

Choose product-wide retirement with explicit later adoption. Use the installer's
existing seed-preservation boundary instead of building an automatic deletion
mechanism. This removes obsolete default entry points while keeping owner control.

## Decision boundary

This is an open recommendation, not the owner's decision. The four blocked
records must remain unapproved until the choice is recorded with the supported
decision procedure. Choosing an option alone does not approve the work order,
release a version or authorize an installation. No disposition is hand-authored.
