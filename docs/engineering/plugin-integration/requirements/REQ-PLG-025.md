+++
id = "REQ-PLG-025"
type = "requirement"
title = "Qualify the accepted host matrix"
status = "draft"
owners = ["requirements-steward"]
created = "2026-09-08"
updated = "2026-09-08"
statement = "WHEN plugin qualification is performed, THE QUALIFICATION PROCESS SHALL retain reproducible scenario evidence for every host and platform combination selected by the accountable owner."
verification_method = ["test", "inspection"]
priority = "must"
source = "PR #360 and owner plugin-installation feedback, 2026-09-08"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Qualify the accepted host matrix

## In plain words

A support claim needs repeatable checks on the named tools and computers. Missing coverage remains visible.

## Why

One working machine cannot establish host integration. Reviewers need the exact versions, observations, and gaps behind support claims.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| Qualification on the accepted matrix | Retain scenario inputs, outcomes, versions, and gaps | Report untested combinations without claiming support |

## Examples

### Normal

**Given** an accepted host and platform matrix.

**When** the selected scenarios run.

**Then** each result identifies reproducible inputs and versions.

### Failure

**Given** one host scenario was not exercised.

**When** qualification is reported.

**Then** that combination remains unqualified.
