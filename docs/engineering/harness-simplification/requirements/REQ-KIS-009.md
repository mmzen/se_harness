+++
id = "REQ-KIS-009"
type = "requirement"
title = "Use work-order approval as permission for routine execution"
status = "approved"
owners = ["product-owner"]
created = "2026-09-14"
updated = "2026-09-14"

statement = "THE HARNESS SHALL authorize routine execution through work-order approval and provide one execution procedure for every executor, retaining scope, local evidence and accountable acceptance boundaries."
verification_method = ["test", "inspection"]

[relations]
derives_from = ["CAP-KIS-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-14T20:38:27Z"
decided_by = "product-owner"
reason = "The owner requested the delegated route as the only route, reviewed the complete proposal and accepted it with \"yes: go\" on 2026-09-14. Record product-owner approval of REQ-KIS-009 for that bounded scope, including its retained acceptance boundaries and prospective adoption. No completion, verification, merge, release or live adoption result is inferred."
+++

# Use work-order approval as permission for routine execution

## Behavior and why

One approved execution procedure removes route selection, optional delegation metadata
and repeated permission requests. It retains checks of actual approval, unchanged scope
and required evidence. Execution does not imply acceptance of the result.

## Acceptance

VER-KIS-003 checks normal local execution, human/agent attribution, missing approval,
scope changes, failed local gates, multi-WO capture and preserved owner decisions/history.
