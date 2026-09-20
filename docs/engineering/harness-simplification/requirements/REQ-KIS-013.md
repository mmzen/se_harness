+++
id = "REQ-KIS-013"
type = "requirement"
title = "Give agents one consistent route with bounded reading"
status = "approved"
owners = ["product-owner"]
created = "2026-09-19"
updated = "2026-09-20"

statement = "The harness presents a concise, consistent selected-task route that preserves the applicable rules, reuses existing execution approval and coordinates unique record IDs across active tasks."
verification_method = ["inspection", "demonstration"]
priority = "must"
source = "Recovery plan dated 2026-09-19; assessment findings F7, F9, F10"

[relations]
derives_from = ["CAP-KIS-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-20T06:27:29Z"
decided_by = "product-owner"
reason = "On 2026-09-20 the owner approved the presented recovery artifact package with \"i approve\". Record approval of this reviewed artifact in the named owner role. Reviewed full-byte SHA-256: e8626a9555ac5b74100496122a3c0ad58639315b827c2c0068df0c2ee7c17384. DEC-KIS-001 separately records the explicit owner-review choice. WO approval grants the bounded execution operations in DR-015; this transition records no implementation result, assurance acceptance or external action."
+++

# Give agents one consistent route with bounded reading

## Why

Conflicting start/completion instructions, broad check names and large repeated reading sets make routine tasks harder. The fix should remove duplication and confusing claims without adding a second policy source or ID service.

## Acceptance

The harness presents a concise, consistent selected-task route that preserves the applicable rules, reuses existing execution approval and coordinates unique record IDs across active tasks.

- **Normal:** A fresh agent and a resumed agent use the project-selected checker, execute ordinary approved steps and stop at the actual assurance decision without repeated permission prompts.
- **Failure:** A task brief lacks a required decision or a relevant contract. The agent identifies that specific gap rather than treating the proposed next command as approval.

VER-KIS-007 defines the observable checks. SPEC-KIS-007 defines how the outcome is judged.
The cited findings are dated baseline observations, not fresh claims about current main.
