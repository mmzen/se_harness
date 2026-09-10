+++
id = "ADR-PLG-002"
type = "adr"
title = "Share evaluator adapters and qualify each coding host"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-10"

[relations]
decides = ["ARCH-PLG-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-10T06:11:30Z"
decided_by = "technical-owner"
reason = "The operator explicitly approved the reviewed plugin packets in this task: \"i approve the packets, i authorize the work\". On 2026-09-10 they selected \"we will merge later: GO for WO-PLG-007  and then WO-PLG-008\" after deciding DEC-PLG-001 and DEC-PLG-002 for the tested Windows activation routes. Record only the named definitions decision for the D04 governing chain or WO-PLG-007, from reviewed proposal 0b42325b. Sibling work-order states, completion, assurance, release and merge remain separate."
+++

# ADR: Share evaluator adapters and qualify each coding host

## Status

Approved under the operator's packet approval; see the lifecycle event above.

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

The selected choice is two host bindings around session-context.py and check-tool-action.py.
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
