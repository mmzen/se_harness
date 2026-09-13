+++
id = "ADR-KIS-001"
type = "adr"
title = "Use proportionate checks for the one-user development stage"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-13"
updated = "2026-09-13"

[relations]
decides = ["ARCH-KIS-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-13T16:40:43Z"
decided_by = "technical-owner"
reason = "The owner accepted all 38 candidates in the retained 2026-09-13 codebase KISS review and requested the work orders: \"OK ! Let's create the work orders to implement all candidates\". Record the technical-owner approval of ADR-KIS-001 within that accepted scope and the established delegated route. SPEC-KIS-001 makes the replacement contracts and seven retained protections explicit; the coverage map assigns all candidates. This records definition approval or bounded execution delegation only, not implementation start, completion, verification, release, merge, publication, live adoption or historical evidence deletion."
+++

# Use proportionate checks for the one-user development stage

## Context and drivers

The owner accepted the full KISS review after the plugin simplification. There is exactly one user and no need for competing-authority or hostile-environment simulations around every ordinary action.
Real file safety, exact tested candidates and published package integrity remain useful.

## Options and consequences

| Option | Consequence |
| --- | --- |
| Keep every existing proof and tune its performance | Preserves the formatting, network and receipt blockers and their test maintenance. |
| Put checks at the action that needs them | Makes ordinary work simpler while retaining explicit decisions and meaningful boundary checks. |
| Remove all validation and provenance | Loses protection for actual file mistakes and the ability to identify what was tested or published. |

## Decision

Use the second option through SPEC-KIS-001. Delete retired restrictions and their tests in the same implementation slices.
Use one shared contract and seven bounded work orders rather than a work order for every small finding.
Do not replace removed locks or receipts with a new proof framework. Keep the seven retained protections.

## Consequences

Some internal mutations cease to recompute complete package identity; explicit full inspection remains available.
Local actions no longer prove live CI success; repository integration and publication still evaluate their CI gates.
Owner configuration and guidance become easier to edit. Machine policy and exact installation identity remain distinguishable.
Historic evidence remains unchanged, while new evidence becomes smaller. Broader future needs require a demonstrated problem and a new decision.
