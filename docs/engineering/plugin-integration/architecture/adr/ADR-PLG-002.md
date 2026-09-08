+++
id = "ADR-PLG-002"
type = "adr"
title = "Share evaluator adapters and qualify each coding host"
status = "draft"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
decides = ["ARCH-PLG-002"]
+++

# ADR: Share evaluator adapters and qualify each coding host

## Status

Proposed. No architecture decision has been approved.

## Context

The proposal adds skills, hooks, and optional helpers to two coding hosts.
Their installation events and interception coverage are not interchangeable.

## Decision drivers

One policy owner, supported installation, honest coverage claims, and retained human authority.

## Considered options

| Option | Consequence |
| --- | --- |
| Instructions alone | Simple packaging, but no automatic session checks or tool-event response. |
| One assumed universal adapter | Less initial code, but hides differences in trust, events, and context limits. |
| Shared scripts with qualified host bindings | Reuses evaluator calls while proving each host's loading and event behavior. |

## Decision

The proposed choice is two host bindings around session-context.py and check-tool-action.py.
Skills invoke the same existing evaluator.
Each binding uses a thin host-shell guard and an evidenced activation route. Missing runtime produces setup guidance; Python handlers still verify readiness. An unsupported host remains unqualified.
Optional helpers remain read-only and can be replaced by the main agent.

## Consequences

Two small host probes precede production adapter approval.
Hook failure reports incomplete readiness or coverage; it never implies universal enforcement.
Existing decisions and qualifying delegation remain unchanged.
Owner decisions and independent external controls remain necessary for protected effects.

## Validation

The host probes, session tests, and action-mapping tests retain observed behavior for each claimed configuration.
WO-ECP-004 addresses authenticated decisions separately; this ADR does not implement or verify that work.
