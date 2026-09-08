+++
id = "REQ-PLG-003"
type = "requirement"
title = "Require an available Python installation"
status = "draft"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "WHEN environment setup starts, THE SETUP ROUTINE SHALL require operator-provided or host-provided Python 3.11 or newer with working environment and package-installation support."
verification_method = ["test","demonstration"]
priority = "must"
source = "Owner-reviewed plugin proposal, PR #360 at 9e894e99; granular implementation request of 2026-09-08."

[relations]
derives_from = ["CAP-DST-001"]
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
