+++
id = "REQ-PLG-003"
type = "requirement"
title = "Require an available Python installation"
status = "approved"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-09"
statement = "WHEN environment setup starts, THE SETUP ROUTINE SHALL require operator-provided or host-provided Python 3.11 or newer with working environment and package-installation support."
verification_method = ["test","demonstration"]
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

# Requirement: Require an available Python installation

## In plain words

The operator or coding host provides Python. Setup explains what is missing before creating the tool environment.

## Why

The plugin must not silently install a programming runtime or depend on an unsupported interpreter.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| First setup | Check the selected Python version and support for creating the isolated environment and installing the supplied package. | Stop with installation guidance; do not download or install Python. |

## Examples

### Normal

**Given** a selected Python installation with the required support.

**When** setup checks prerequisites.

**Then** the prerequisites pass without changing the repository.

### Failure

**Given** Python is absent, too old, or lacks required support.

**When** setup starts.

**Then** it reports the missing prerequisite and makes no environment or repository changes.
