+++
id = "CAP-KIS-002"
type = "capability"
title = "Apply a common simplicity rule to specifications and implementation review"
status = "approved"
owners = ["product-owner"]
created = "2026-09-14"
updated = "2026-09-14"

ability = "Authors and reviewers can challenge unnecessary requirements and implementation complexity against agreed project needs."

[relations]
derives_from = ["INT-KIS-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-14T19:44:45Z"
decided_by = "product-owner"
reason = "The owner accepted the generic simplicity rule and exact policy/template/instruction/skill routing, then said \"OK, go for this modification then\" on 2026-09-14. Record product-owner approval of CAP-KIS-002 for that bounded proposal. No completion, verification, release, merge or live adoption decision is inferred."
+++

# Apply a common simplicity rule to specifications and implementation review

## Ability

An author or reviewer can find one shared simplicity rule, apply the questions relevant
to their current artifact or implementation, and retain material reasoning in ordinary
design or review evidence. Generic agent instructions and the plugin use the same policy.

## Boundaries

The rule supports human judgement. Project requirements determine the necessary scale,
reliability and other quality properties. It grants no additional decision rights.
