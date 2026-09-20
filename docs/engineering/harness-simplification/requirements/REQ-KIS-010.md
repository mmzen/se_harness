+++
id = "REQ-KIS-010"
type = "requirement"
title = "Keep evidence outcomes truthful"
status = "approved"
owners = ["product-owner"]
created = "2026-09-19"
updated = "2026-09-20"

statement = "The harness reports what each retained observation establishes and refuses to treat missing, failed or stale required checks as successful verification."
verification_method = ["test", "inspection"]
priority = "must"
source = "Recovery plan dated 2026-09-19; assessment findings F3, F9"

[relations]
derives_from = ["CAP-KIS-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-20T06:27:29Z"
decided_by = "product-owner"
reason = "On 2026-09-20 the owner approved the presented recovery artifact package with \"i approve\". Record approval of this reviewed artifact in the named owner role. Reviewed full-byte SHA-256: df594d22685dd94a58dc82d972a347c3860948038a2d47415b85daa5d880ee2e. DEC-KIS-001 separately records the explicit owner-review choice. WO approval grants the bounded execution operations in DR-015; this transition records no implementation result, assurance acceptance or external action."
+++

# Keep evidence outcomes truthful

## Why

The assessment passed an explicitly failed report and relabelled old output after code changed. The owner needs reliable results without restoring rigid evidence headers or repeated full test runs.

## Acceptance

The harness reports what each retained observation establishes and refuses to treat missing, failed or stale required checks as successful verification.

- **Normal:** A required command ran successfully for the selected inputs. Its result remains usable when only an unrelated note changes, with its original tested version preserved.
- **Failure:** A report says required tests did not run. A handoff refuses the required successful-test claim and leaves that report unchanged.

VER-KIS-004 defines the observable checks. SPEC-KIS-004 defines how the outcome is judged.
The cited findings are dated baseline observations, not fresh claims about current main.
