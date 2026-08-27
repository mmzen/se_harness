+++
id = "REQ-ECP-015"
type = "requirement"
title = "The reading manifest carries a generated command block, not the owner narrative"
status = "draft"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-27"
updated = "2026-08-27"
statement = "WHEN `preflight` emits the phase reading manifest, THE SYSTEM SHALL list the owner-controlled region of `AGENTS.md` only through a generated command block bounded to 2048 bytes, excluding the remaining owner narrative."
verification_method = ["test"]
priority = "should"
source = "review section 6"
measure = "2048 bytes"

[relations]
derives_from = ["CAP-ECP-001"]
+++

# Requirement: The reading manifest carries a generated command block, not the owner narrative

## Rationale

`CLAUDE.md` importing `AGENTS.md` auto-loads 7.6 KB, 79% of it owner narrative;
the mandatory twelve-file manifest is 49.5 KB, 30% of it repository-generic
(docs/notes/agentic-execution-review-2026-08.md:278-279). The 2026-08 agentic
execution review recommends dropping the `AGENTS.md` owner region from the
manifest and keeping commands and managed-path lists as a generated block
(section 9; section 6 at :298-300). Principle 3 of the target architecture
shrinks instructions to the router and the card, with everything else returned
on demand.

## Behavior

- Trigger: `harnessctl preflight <repo> --phase <phase>` emits the reading
  manifest.
- Response: the manifest entry for `AGENTS.md` refers to a generated block,
  rendered from the owner region's command lines and managed-path lists only,
  whose UTF-8 length is at most 2048 bytes; the remaining owner narrative is
  listed nowhere in the manifest; the manifest's byte total decreases
  accordingly.
- On failure: when the generated block would exceed 2048 bytes, `preflight`
  reports the overflow as a warning naming the excess and truncates nothing
  silently.

## Assumptions and dependencies

- The owner region keeps its existing delimiters, so the generator can locate
  commands and path lists.
- `harnessctl next` (REQ-ECP-001) returns the same manifest.
- The router and `OPERATING_CARD.md` remain in the manifest unchanged.

## Acceptance examples

Executable scenarios live in `acceptance/REQ-ECP-015.feature` and are named by
the verification contract that covers this requirement.

### Example: normal behavior

**Given** `AGENTS.md`'s owner region is 6 KB, of which 900 bytes are command
lines and path lists.

**When** `harnessctl preflight . --phase execute` runs.

**Then** the manifest lists a generated block of about 900 bytes for
`AGENTS.md`, no narrative paragraph appears in it, and the total is smaller than
before by the excluded narrative.

### Example: failure behavior

**Given** the owner region grows its command lists to 2.5 KB.

**When** `preflight` runs.

**Then** the manifest carries the block and a warning naming a 512-byte excess
over 2048; no bytes are dropped without a diagnostic.

## Open decisions

None.
