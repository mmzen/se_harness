+++
id = "REQ-PLG-027"
type = "requirement"
title = "Publish truthful released onboarding"
status = "draft"
owners = ["product-owner"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "WHEN plugin onboarding is published, THE INSTALLATION GUIDE SHALL describe the available released installation route, its provided-Python prerequisite, observed activation checks, and current limitations."
verification_method = ["test", "inspection"]
priority = "must"
source = "PR #360 and owner plugin-installation feedback, 2026-09-08"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Publish truthful released onboarding

## In plain words

The guide describes an installation people can actually use. It makes the Python prerequisite and remaining limitations clear.

## Why

Future plans presented as available commands waste operator time. Instructions need clear outcomes when prerequisites or activation are missing.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| Public onboarding published | Describe the current released route and its checks | Keep unavailable features explicitly prospective |

## Examples

### Normal

**Given** a qualified released plugin.

**When** the guide is published.

**Then** commands and prerequisites match that release.

### Failure

**Given** an unreleased plugin.

**When** guidance is drafted.

**Then** the guide claims no available installation.
