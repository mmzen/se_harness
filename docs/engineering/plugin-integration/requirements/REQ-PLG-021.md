+++
id = "REQ-PLG-021"
type = "requirement"
title = "Keep operator briefing explicit and bounded"
status = "draft"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "WHEN the operator explicitly names the briefing skill, THE BRIEFING SKILL SHALL preserve its existing bounded-source and protected-content contract through the plugin installation."
verification_method = ["test", "inspection"]
priority = "must"
source = "PR #360 and owner plugin-installation feedback, 2026-09-08"

[relations]
derives_from = ["CAP-WEX-001"]
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
