+++
id = "REQ-PLG-021"
type = "requirement"
title = "Keep operator briefing explicit and bounded"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-10"
statement = "WHEN the operator explicitly names the briefing skill, THE BRIEFING SKILL SHALL preserve its existing bounded-source and protected-content contract through the plugin installation."
verification_method = ["test", "inspection"]
priority = "must"
source = "PR #360 and owner plugin-installation feedback, 2026-09-08"

[relations]
derives_from = ["CAP-WEX-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-10T18:19:50Z"
decided_by = "requirements-steward"
reason = "The operator previously stated \"i approve the packets, i authorize the work\" for the reviewed plugin proposal, then on 2026-09-10 explicitly selected \"WO-PLG-010 next, followed by WO-PLG-011 and WO-PLG-012  (delegated route)\". Record only REQ-PLG-021 approval under requirements-steward, from proposal 0b42325b75bc6d1c36897369687c3d3ed578bdb9; reviewed/current draft SHA-256 57557adcef3d4c73befbe5d32f89063e906d10d1b137eb94a760dcb2aba59e5c. The definition meaning is unchanged from the reviewed packet. Assurance of implementation, release and PR merge remain separate human decisions."
+++

# Requirement: Keep operator briefing explicit and bounded

## In plain words

The existing briefing tool explains only the supplied material. It runs when named and preserves important technical text.

## Why

Installation must preserve the briefing boundary. Ordinary work does not require a separate briefing process.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| Briefing skill explicitly named | Return a brief bound to the supplied source | Preserve the source and report invalid input |

## Examples

### Normal

**Given** an explicit briefing request with a valid source.

**When** the skill renders a brief.

**Then** protected text and supplied decision meaning remain intact.

### Failure

**Given** no explicit briefing request.

**When** an ordinary work instruction arrives.

**Then** the briefing skill does not activate.
