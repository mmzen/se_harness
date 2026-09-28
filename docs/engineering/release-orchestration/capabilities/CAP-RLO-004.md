+++
id = "CAP-RLO-004"
type = "capability"
title = "Track delivery across all release surfaces"
status = "draft"
owners = ["mmzen"]
created = "2026-09-28"
updated = "2026-09-28"
ability = "A release operator can identify outstanding delivery work across the evaluator, plugin marketplace and current documentation after any release stage."

[relations]
derives_from = ["INT-RLO-001"]
+++

# Capability: Track delivery across all release surfaces

## In plain words

Publishing the evaluator does not also publish its host plugins or update
their installation instructions. A delivery surface is one place from which
users obtain the release or its current instructions.

## Actor and need

The release operator needs an explicit plan for each surface and an honest
completion report. The human release owner needs to see pending work,
responsible owners and evidence before declaring the delivery complete.

This extends repository-owned operational reporting across existing delivery
surfaces. It does not replace the approved publisher transaction or change
what an existing formal release record authorizes.

## Not decided here

- The plugin version for the next marketplace correction.
- The content of a particular release contract or its publication authority.
- Host credentials, provider-directory submissions or automatic publication.
- Formal artifact lifecycle rules and existing released records.
