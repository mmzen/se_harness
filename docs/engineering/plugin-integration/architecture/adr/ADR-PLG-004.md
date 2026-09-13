+++
id = "ADR-PLG-004"
type = "adr"
title = "Choose explicit checks and disposable skill replacement"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-13"
updated = "2026-09-13"

[relations]
decides = ["ARCH-PLG-004"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-13T06:30:56Z"
decided_by = "technical-owner"
reason = "The owner accepted the complete plugin simplification proposal on 2026-09-13 and requested its artifact packet and work order through the delegated route: \"i accept this proposal, let's go you can create the artifact packet and work order (delegated route)\". Record the technical-owner approval of ADR-PLG-004 for that accepted scope, including explicit checks instead of blocking hooks and SPEC-PLG-021's applicability table. The retained proposal and 50-scenario coverage map identify the accepted behavior. This approves a definition or the bounded execution delegation only; it records no implementation start, completion, verification result, release, merge, publication or live adoption."
+++

# ADR: Choose explicit checks and disposable skill replacement

## Context

The project is at an early development stage and has exactly one user, its owner.
The owner rejected preserving local edits inside old plugin-replaced skills and accepted the KISS proposal on 2026-09-13.
The retained proposal lists 50 scenarios; its coverage map records each disposition.

## Decision drivers

- Make setup and upgrades easy to understand and retry.
- Remove checks for scenarios the owner does not need.
- Keep useful boundaries around deletion, unrelated content and actual lifecycle decisions.
- Reduce current test and CI cost without rewriting old evidence.

## Considered options

| Option | Consequence |
| --- | --- |
| Keep the transaction and automatic hook design | Retains locks, binding inventories, recovery states, host profiles and extensive fault matrices. |
| Simplify migration but keep a small blocking hook | Reduces migration code but retains per-edit host integration, failure translation and qualification work. |
| Use disposable replacement and explicit checks | Removes those layers; the owner and skill instructions invoke the normal checker at the appropriate stage. |

## Decision

Choose disposable replacement and explicit checks, as defined by SPEC-PLG-021.
Remove automatic blocking hooks instead of rebuilding their enforcement framework.
Use one small provider record, ordinary file operations, repairable setup and a local development assembly path.

## Consequences

Edits and extra files inside the four old harness skill directories are deleted deliberately.
A repeated command completes an interrupted replacement; concurrent mutation and arbitrary crash rollback are not supported guarantees.
Ordinary editor actions have no plugin interception guarantee. The existing harness still decides lifecycle legality when invoked.
Publication provenance and general evaluator integrity remain in their existing owners.
The applicability table replaces current obligations only for the new delivery; historical decisions and verification remain unchanged.

## Revisit condition

Reconsider a removed protection only after a concrete user need or observed failure makes its cost worthwhile.
That future change needs its own bounded scope; a hypothetical multi-user scenario is insufficient by itself.
