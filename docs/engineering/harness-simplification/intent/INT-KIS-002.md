+++
id = "INT-KIS-002"
type = "intent"
title = "Prevent unnecessary complexity during design and review"
status = "approved"
owners = ["product-owner"]
created = "2026-09-14"
updated = "2026-09-14"

outcome = "Authors and reviewers prevent unjustified complexity using the existing engineering decisions."

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-14T19:44:45Z"
decided_by = "product-owner"
reason = "The owner accepted the generic simplicity rule and exact policy/template/instruction/skill routing, then said \"OK, go for this modification then\" on 2026-09-14. Record product-owner approval of INT-KIS-002 for that bounded proposal. No completion, verification, release, merge or live adoption decision is inferred."
+++

# Prevent unnecessary complexity during design and review

## Problem and outcome

Specifications can demand unnecessary behavior; implementation review can then reward
faithful delivery of that complexity. Projects need the simplest complete solution to
their agreed needs, with significant complexity justified before it grows code and tests.
This applies to every governed project, including SE Harness's own development.

## Success and scope

Authors and reviewers receive the shared rule through ordinary instructions, templates
and skills. Review can identify an unnecessary obligation as well as unnecessary code.
Installation and CLI inspection demonstrate availability; human review judges simplicity.
No automatic reduction in defects or development time is claimed. Project scale and
required quality come from each project's agreed constraints.
