+++
id = "ADR-IAR-010"
type = "adr"
title = "Classify temporal reassessment by artifact role and declared relation"
status = "approved"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
decides = ["ARCH-IAR-010"]
+++

# ADR: Classify temporal reassessment by artifact role and declared relation

## Status

Accepted on 2026-08-16 through the repository owner's instruction to implement the reviewed Phase 1 correction.

## Context

An update timestamp means different things for a living definition, completed work, and a commit-bound assurance record. Applying one generic comparison to every graph edge creates plausible-looking but incorrect actions. The public rule already feeds both dashboard and inspection, so the correction must preserve one producer and one stable rule identity.

## Decision drivers

- Make findings actionable rather than merely chronologically true.
- Preserve immutable provenance and completed-work history.
- Keep the rule deterministic, offline, explainable, and testable.
- Fail closed for unknown types and extension relations.
- Avoid duplicating finding semantics in `inspect`.

## Considered options

1. Keep blanket date comparison and document exceptions. Rejected because false actions remain in machine output.
2. Generate every finding, then suppress selected rows in each renderer. Rejected because dashboard and inspection could diverge and hidden findings would still affect counts.
3. Replace the rule immediately with aggregate VREC/RLS provenance inference. Rejected because provenance eligibility is a different, larger rule family.
4. Apply an explicit source-type, lifecycle, relation, and authority predicate in the shared finding producer. Selected because it is small, auditable, fail-closed, and preserves the existing public rule.

## Decision

Choose option 4. Encode the exact table in `SPEC-IAR-010`, evaluate only declared relations, exclude historical records and inactive definitions, and use a narrower lifecycle rule for work orders. Include the relation name in the observation and bump the finding-rules version.

`inspect` continues to consume the Explorer snapshot unchanged. A future dedicated provenance observation requires a separate artifact packet.

## Consequences

- Misleading warnings for completed work orders, VRECs, RLSs, supersession, and derived projections disappear.
- Living definitions still receive useful change-impact prompts.
- Unknown future relations receive no warning until deliberately governed.
- Some genuine provenance concerns will not be represented by `W-HEX-003`; existing formal provenance checks remain authoritative.

## Validation

Execute `VER-IAR-010`, including controlled predicate fixtures, current-repository inspection, root/canonical parity, package and installation coverage, determinism, no-write proof, Python 3.11+, formal validation, doctor, and preflight.
