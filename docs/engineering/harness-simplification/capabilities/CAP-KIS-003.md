+++
id = "CAP-KIS-003"
type = "capability"
title = "Execute approved work through one shared procedure"
status = "approved"
owners = ["product-owner"]
created = "2026-09-14"
updated = "2026-09-14"

[relations]
derives_from = ["INT-KIS-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-14T20:38:27Z"
decided_by = "product-owner"
reason = "The owner requested the delegated route as the only route, reviewed the complete proposal and accepted it with \"yes: go\" on 2026-09-14. Record product-owner approval of CAP-KIS-003 for that bounded scope, including its retained acceptance boundaries and prospective adoption. No completion, verification, merge, release or live adoption result is inferred."
+++

# Execute approved work through one shared procedure

## Ability

A selected executor can start an approved eligible WO, implement its bounded behavior,
run required checks, record completion and prepare required verification evidence using
the permission granted by WO approval. A person and an agent follow the same procedure.

## Constraints

Only selected eligible work starts. Owners decide scope changes, result acceptance and
delivery unless the exact delivery is already authorized. Failing checks remain failures.
