+++
id = "ADR-IAR-004"
type = "adr"
title = "Use explicit conditional ADR applicability"
status = "approved"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
decides = ["ARCH-IAR-004"]
+++

# ADR: Use explicit conditional ADR applicability

## Status

Accepted on 2026-08-12 through the repository owner's instruction `ok for implementation`.

## Context

Agent judgment currently determines whether an ADR is authored, while preflight later requires at least one ADR globally. This neither guides first-time architecture design nor distinguishes significant decisions from routine use of an existing design.

## Decision drivers

- Surface material decisions before implementation authorization.
- Avoid one ceremonial ADR per requirement or routine change.
- Make no-ADR outcomes explicit, accountable, and reviewable.
- Enforce coverage per architecture rather than through global artifact presence.
- Remain adoptable by repositories containing historical active artifacts.

## Considered options

1. **Require an ADR for every requirement, specification, or work order.** Mechanically simple but produces duplication and low-value records.
2. **Keep ADR creation entirely optional and agent-judged.** Low ceremony but repeats the reported failure and cannot fail closed.
3. **Require an explicit applicability assessment and conditionally require ADR coverage.** Adds structured authoring but preserves meaningful optionality.
4. **Infer significance automatically from architecture prose or source diffs.** Appears convenient but is non-deterministic and would let automation exercise architecture judgment.

## Decision

Choose option 3. Every new or materially changed architecture receives a structured, technically accountable decision assessment. A significant trigger requires one or more active ADRs deciding that architecture. A no-ADR outcome requires zero triggers and a non-empty accepted rationale. ADR cardinality follows coherent decisions, not requirement count.

## Consequences

- Missing ADR becomes a precise coverage anomaly rather than an implicit authoring choice.
- Routine changes avoid ceremonial ADRs but must still document why no significant decision exists.
- Templates, policies, validation, preflight, dashboard, tests, and migration behavior change together.
- False no-ADR rationales remain possible because structural automation cannot understand arbitrary architecture semantics; accountable review is still essential.
- Historical repositories need a bounded compatibility window instead of automatic mass rewrites.

## Validation

Execute `VER-IAR-004`, including the full assessment matrix, significant first-design case, routine no-ADR case, multi-architecture and one-ADR-many-requirements cases, legacy migration behavior, Explorer anomalies, integrity parity, and dual-runtime regression.
