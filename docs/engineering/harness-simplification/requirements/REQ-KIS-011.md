+++
id = "REQ-KIS-011"
type = "requirement"
title = "Use the full current checks before completion"
status = "approved"
owners = ["product-owner"]
created = "2026-09-19"
updated = "2026-09-20"

statement = "The harness permits work-order completion only when the current selected changes and evidence pass the same relevant checks used by handoff, preview and planning."
verification_method = ["test", "inspection"]
priority = "must"
source = "Recovery plan dated 2026-09-19; assessment findings F4, F8"

[relations]
derives_from = ["CAP-KIS-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-20T06:27:29Z"
decided_by = "product-owner"
reason = "On 2026-09-20 the owner approved the presented recovery artifact package with \"i approve\". Record approval of this reviewed artifact in the named owner role. Reviewed full-byte SHA-256: b0210c5b7036b40073008eb654f0752ba1a824fbeb5d6552da8ff7ca58148ef5. DEC-KIS-001 separately records the explicit owner-review choice. WO approval grants the bounded execution operations in DR-015; this transition records no implementation result, assurance acceptance or external action."
+++

# Use the full current checks before completion

## Why

The released checker rejected an outside-scope edit at handoff but accepted direct completion. An unrelated draft also gave different answers in checking and planning. One checking path removes both surprises.

## Acceptance

The harness permits work-order completion only when the current selected changes and evidence pass the same relevant checks used by handoff, preview and planning.

- **Normal:** An approved task with complete in-scope changes and valid evidence completes offline. An unrelated incomplete draft does not change that result.
- **Failure:** An outside-scope file is present in the real diff. Handoff and direct completion both refuse; the work order stays in progress.

VER-KIS-005 defines the observable checks. SPEC-KIS-005 defines how the outcome is judged.
The cited findings are dated baseline observations, not fresh claims about current main.
