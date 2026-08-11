+++
id = "CAP-WLC-001"
type = "capability"
title = "Represent and validate finite work-order lifecycles"
status = "approved"
owners = ["repository-owner", "engineering-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
derives_from = ["INT-WLC-001"]
+++

# Capability: Represent and validate finite work-order lifecycles

## Capability statement

Repository owners and assurance reviewers can distinguish work authorization, completed work, commit-bound verification, and release through consistent statuses and authoritative validation without recursively verifying governance decisions.

## Observable outcomes

- Work-order status has one documented meaning across source and installed repositories.
- Governance-only work stops at `implemented` unless a separate verified VREC explicitly covers it.
- Repositories that require verified-work provenance cannot validate an uncovered `verified` or `released` work order.
- Explorer findings do not duplicate an authoritative validator diagnostic.

## Exclusions

The capability does not infer completion from prose, automatically change lifecycle status, approve evidence, or publish software.
