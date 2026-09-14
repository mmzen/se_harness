+++
id = "REQ-KIS-008"
type = "requirement"
title = "Make proportionate design and review guidance available through existing routes"
status = "approved"
owners = ["product-owner"]
created = "2026-09-14"
updated = "2026-09-14"

statement = "THE HARNESS SHALL provide shared, project-independent simplicity guidance for specification authoring and implementation review through its existing policy, template, instruction and skill routes."
verification_method = ["test", "inspection"]
source = "CAP-KIS-002"

[relations]
derives_from = ["CAP-KIS-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-14T19:44:45Z"
decided_by = "product-owner"
reason = "The owner accepted the generic simplicity rule and exact policy/template/instruction/skill routing, then said \"OK, go for this modification then\" on 2026-09-14. Record product-owner approval of REQ-KIS-008 for that bounded proposal. No completion, verification, release, merge or live adoption decision is inferred."
+++

# Make proportionate design and review guidance available through existing routes

## In plain words

Ask whether each significant obligation and design choice is needed before building it
and again when reviewing the result. Keep the wording in one place that agents read.

## Why

The owner wants this to govern any project, rather than a list of forbidden techniques
drawn from the plugin simplification. A justified complex solution remains acceptable.

## Acceptance

An installed project contains the common rule and relevant questions. Artifact creation
prints its type's questions, start and review list the policy to read, and instruction and
skill routes apply it at existing decisions. VER-KIS-002 checks those observable routes
and reviews the wording without introducing a new machine gate or mandatory artifact field.
