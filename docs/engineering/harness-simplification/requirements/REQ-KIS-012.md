+++
id = "REQ-KIS-012"
type = "requirement"
title = "Match repository protection to the stated approval policy"
status = "approved"
owners = ["product-owner"]
created = "2026-09-19"
updated = "2026-09-20"

statement = "The repository makes its approval and integration guarantees explicit, requires the checks that establish acceptance, and ties consequential review to the actual work and version reviewed."
verification_method = ["inspection", "demonstration"]
priority = "must"
source = "Recovery plan dated 2026-09-19; assessment findings F1, F2, F5, F6"

[relations]
derives_from = ["CAP-KIS-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-20T06:27:29Z"
decided_by = "product-owner"
reason = "On 2026-09-20 the owner approved the presented recovery artifact package with \"i approve\". Record approval of this reviewed artifact in the named owner role. Reviewed full-byte SHA-256: 9c39468b2e063041af80be44d80c80b95bd10226c87c2003c2c20b2bda744a6f. DEC-KIS-001 separately records the explicit owner-review choice. WO approval grants the bounded execution operations in DR-015; this transition records no implementation result, assurance acceptance or external action."
+++

# Match repository protection to the stated approval policy

## Why

Local names and editable approvals do not authenticate a person. The assessed server rules required fewer checks and reviews than the narrative implied. The project needs honest guarantees using its existing host controls.

## Acceptance

The repository makes its approval and integration guarantees explicit, requires the checks that establish acceptance, and ties consequential review to the actual work and version reviewed.

- **Normal:** The selected review policy is recorded, required checks succeed for the current candidate, and the responsible human reviews the actual change before the permitted integration action.
- **Failure:** A required test is missing or failed, a required current review is absent, or an approval scope is expanded without the owner decision. The normal protected route refuses, or the owner-controlled residual is clearly recorded where enforcement is unavailable.

VER-KIS-006 defines the observable checks. SPEC-KIS-006 defines how the outcome is judged.
The cited findings are dated baseline observations, not fresh claims about current main.
