+++
id = "REQ-IAR-029"
type = "requirement"
title = "Use one pinned release resource set"
status = "approved"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-09-30"
statement = "Agents, CLI and CI use the repository-selected released policy, guidance and templates without requiring repository copies."
verification_method = ["test", "inspection", "demonstration"]
priority = "must"
source = "Human mmzen accepted the external-resource proposal and requested its artifacts, explicitly applying KIS principles, on 2026-09-30."

[relations]
derives_from = ["CAP-IAR-002", "CAP-DST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-30T11:12:12Z"
decided_by = "mmzen"
reason = "Human mmzen: I confirm and approve. Approves the updated external-resource package and required commit-bound verification for WO-IAR-028, WO-IAR-029 and WO-IAR-030. Clarification confirmed: Ok for this plan; short bootstrap before cloning, immediate activation of the actual checkout, per-session recovery after compaction/resume and independent parallel sessions. DEC-IAR-003 separately records future release and separate adoption. Reviewed file SHA-256 177e42a560f0003cf9501dbca340a4e3fa428769968f10eac12bb074474b8a14."
+++

# Use one pinned release resource set

## Why

Copying shared harness material into each repository creates installation noise
and makes the same content appear to have several owners.

## Behavior

Keep standard instructions, authoring guidance, artifact templates and machine
policy in the selected released evaluator's package outside the repository.
The plugin delivers this material to agents. CLI and CI use the same release
without requiring a plugin. The repository retains its selection and its formal
records. The evaluator remains the only lifecycle authority.

## Acceptance

- A repository without installed guide or template copies supports inspection,
  validation, artifact creation and the selected lifecycle checks.
- Every returned guide reference resolves to the selected release and heading;
  formal-artifact references still identify repository files.
- Artifact creation writes the requested draft and necessary parent directories,
  not a template collection or unrelated sample artifacts.
- Wrong, missing or changed resource identity prevents the affected action before
  a lifecycle write. Verified installed resources work without network access.

## Boundary

This defines a future release layout. It does not change the installed 0.20.0
contract, lifecycle decisions, or accepted historical records.
