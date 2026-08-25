+++
id = "CAP-ADS-001"
type = "capability"
title = "Give a coding agent one tool-computed next step and one bounded reading set"
status = "approved"
owners = ["product-owner", "domain-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
derives_from = ["INT-ADS-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T10:36:12Z"
decided_by = "product-owner"
+++

# Capability: Give a coding agent one tool-computed next step and one bounded reading set

## Description

A supported coding agent operating under the managed harness can, for any
selected artifact and phase, obtain from the released evaluator: the exact set
of files it must read; one next typed step, identical across `focus` and
`check`; a corrective command or accountable escalation whenever a checkpoint
is blocked; a warning before a known recurring trap; and a digest that binds
the restitution block it returns.

## Users

Coding agents executing a lifecycle stage; engineering, assurance, and release
owners who read restitution; CI that verifies a pull request.

## Boundaries

The capability computes, renders, and verifies. It does not approve, start,
complete, verify, release, or perform an external action. It does not change
what a state means or who decides it.

## Derived requirements

`REQ-ADS-001` through `REQ-ADS-006`.
