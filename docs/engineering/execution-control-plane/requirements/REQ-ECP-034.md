+++
id = "REQ-ECP-034"
type = "requirement"
title = "One primitive per family, and the contract tables drive the code that reads them"
status = "draft"
owners = ["repository-owner", "engineering-owner"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "THE SYSTEM SHALL implement each shared primitive once in the package, keep every recorded digest unchanged, and read its operation, restitution, aggregation and digest-mode tables from the contracts."
verification_method = ["test", "inspection"]
priority = "should"
measure = "one definition per family row of issue #377 in se_harness and repository_tools; every recipe, lock and evidence digest equal to main's; the four declarative sections read at run time with their Python copies gone; the suite at its baseline"
source = "issue #377 (code health assessment 2026-09-07, section 2.1 and the wave 2 plan) and the owner decision of 2026-09-07 recorded on issue #381, item 4: wire the declarative contract sections"

[relations]
derives_from = ["CAP-ECP-003"]
+++

# Requirement: One primitive per family, and the contract tables drive the code that reads them

## In plain words

The same small helpers are written many times with small differences, and
four tables live once in a contract file and again in Python. This
requirement keeps one of each.

## Why

The assessment counted thirteen Git launchers, eight front-matter parsers,
sixteen digest helpers, thirteen serializers and six atomic writers.
Several already disagree: timeouts differ, two parsers fail on CRLF, and
two serializers of one name produce different bytes. Each copy is a place
the next fix can miss. The owner also decided that four contract tables
drive behaviour instead of their Python copies.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| a caller launches a process, parses front matter, hashes, serializes or writes atomically | it calls the one primitive and keeps its own exception type | the duplication scan names the copy |
| a reader needs one of the four tables | it reads the contract section | the sync test names the Python copy |
| a recorded digest is recomputed after the change | it equals the digest on main | the digest suites fail |

## Examples

### Normal

**Given** the candidate after this change,

**When** the duplication scan runs over the package and the tools,

**Then** it reports none of the seven cross-file blocks, and every digest pin
in the suite holds.

### Failure

**Given** a CRLF checkout,

**When** an artifact's front matter is read by any command,

**Then** the one parser reads it, where two copies failed before.

## Open decisions

None.
