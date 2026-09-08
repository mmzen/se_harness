+++
id = "REQ-PLG-022"
type = "requirement"
title = "Repair using a fresh private environment"
status = "draft"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "WHEN plugin environment repair is requested, THE SETUP SKILL SHALL prepare and verify a fresh isolated environment before replacing its active environment reference."
verification_method = ["test", "inspection"]
priority = "must"
source = "PR #360 and owner plugin-installation feedback, 2026-09-08"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Repair using a fresh private environment

## In plain words

Repair prepares a clean replacement before switching to it. Failure leaves a usable previous environment available.

## Why

Installing over a damaged environment can preserve unknown files. Switching too early can turn a recoverable failure into an outage.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| Environment repair requested | Verify a fresh environment before selecting it | Preserve the previous verified selection |

## Examples

### Normal

**Given** working provided Python and a verified package.

**When** repair succeeds in a fresh environment.

**Then** selection changes only after verification.

### Failure

**Given** wheel installation fails in the replacement.

**When** repair stops.

**Then** the previous active selection is unchanged.
