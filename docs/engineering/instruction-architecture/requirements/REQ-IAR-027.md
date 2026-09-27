+++
id = "REQ-IAR-027"
type = "requirement"
title = "Complete migration and clear communication"
status = "approved"
owners = ["repository-owner", "technical-owner"]
created = "2026-09-20"
updated = "2026-09-27"
statement = "The migrated instruction set preserves agreed meanings, has one canonical owner for each detailed rule, and gives agents precise actions with verified discovery coverage."
verification_method = ["test", "inspection", "demonstration"]
priority = "must"
source = "Repository owner discussion culminating in the 2026-09-20 instruction-discovery split and request to create its delivery artifacts."

[relations]
derives_from = ["CAP-IAR-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-27T07:37:39Z"
decided_by = "repository-owner"
reason = "User instruction: so let's start the work orders. Apply the reviewed package under DEC-IAR-001 versioned-successor; selected 0.18.0 governance remains installed until separate release/adoption."
+++

# Complete migration and clear communication

## Why

Relocation must not hide unresolved policy or replace precise commands with prose that changes authority.

## Behavior

Retain the two Human/Agent profiles and human-reserved decisions. Preserve exact command arguments and evidence meanings. Use plain language and transient notes only in conversation or temporary storage outside the repository. Keep machine requirements in formal artifacts, not agent-use procedures. State unsupported exception and linked-revision capabilities honestly.

## Acceptance

Review the source-to-destination map, resolve annotated and broken references, verify all local links, and measure complete representative reading sets including communication policy and selected references. Show measured improvement over the full source without treating fewer words as proof of correctness.

## Failure

An unresolved change in meaning remains an explicit review item. Unsupported capabilities do not gain a command, authority or waiver from prose.
