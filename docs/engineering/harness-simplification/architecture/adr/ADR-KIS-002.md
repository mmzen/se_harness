+++
id = "ADR-KIS-002"
type = "adr"
title = "Remove the execution-route choice"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-14"
updated = "2026-09-14"

[relations]
decides = ["ARCH-KIS-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-14T20:38:27Z"
decided_by = "technical-owner"
reason = "The owner requested the delegated route as the only route, reviewed the complete proposal and accepted it with \"yes: go\" on 2026-09-14. Record technical-owner approval of ADR-KIS-002 for that bounded scope, including its retained acceptance boundaries and prospective adoption. No completion, verification, merge, release or live adoption result is inferred."
+++

# Remove the execution-route choice

## Context and drivers

The owner wants KISS across governed projects and repeated execution permission removed.

## Options

| Option | Consequence |
| --- | --- |
| Enable delegation by default and keep owner execution | Retains route branches, fallback behavior and duplicated instructions. |
| Make bounded execution part of approval | Uses one procedure and existing checks; requires a clear prospective policy amendment. |
| Let execution approve its own result | Removes the meaningful owner acceptance boundary and exceeds the accepted scope. |

## Decision and consequences

Use the second option. Approval explicitly grants the routine sequence. Retain scope,
evidence and acceptance checks. Read old events without rewriting them; old grants that
did not cover execution need approval through the existing amendment process. Do not
require a subagent or add a configuration mode. This is a project-generic responsibility
choice, not an assumption that every governed project has one user.
