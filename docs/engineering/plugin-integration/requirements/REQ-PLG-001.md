+++
id = "REQ-PLG-001"
type = "requirement"
title = "Distribute the exact released evaluator wheel"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-09"
statement = "WHEN a plugin package is assembled, THE PACKAGER SHALL include the selected published evaluator wheel unchanged and exclude Python runtimes and rebuilt evaluators."
verification_method = ["test","inspection"]
priority = "must"
source = "Owner-reviewed plugin proposal, PR #360 at 9e894e99; granular implementation request of 2026-09-08."

[relations]
derives_from = ["CAP-DST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-09T18:23:58Z"
decided_by = "requirements-steward"
reason = "Operator explicitly approved the reviewed plugin packets in this task: i approve the packets, i authorize the work. On 2026-09-09 the operator selected go for WO-PLG-001 after the D03 delivery and assembly-first sequence were presented. This records the named definition approval from proposal be8b4126; it does not start WO-PLG-002."
+++

# Requirement: Distribute the exact released evaluator wheel

## In plain words

The installation package carries the released checking tool. Users supply Python separately.

## Why

Rebuilding the checking tool would create another identity to trust. Shipping Python would add a runtime distribution responsibility outside this change.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| Package assembly | The selected wheel is present with its published identity; no Python runtime is included. | Refuse the package if the wheel is missing, changed, or not the selected release. |

## Examples

### Normal

**Given** the selected published wheel.

**When** both host packages are assembled.

**Then** each carries those unchanged bytes and no Python runtime.

### Failure

**Given** a wheel whose bytes differ from the selected release.

**When** assembly is requested.

**Then** packaging stops before producing a usable package.
