+++
id = "ADR-IAR-005"
type = "adr"
title = "Use dual typed architecture traceability"
status = "approved"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
decides = ["ARCH-IAR-005"]
+++

# ADR: Use dual typed architecture traceability

## Status

Accepted on 2026-08-12 through the repository owner's instruction `ok for implementation`.

## Context

The current model uses one `constrains` relation for two observed meanings. Some architecture artifacts target requirements, others target specifications, and the validator does not type the relation. The template and formal graph therefore disagree while preflight interprets every target as a requirement coverage claim.

## Decision drivers

- Retain the direct link from architecture to its architecturally significant drivers.
- Record the exact behavioral and interface contracts relevant to architecture.
- Avoid artificial architecture coverage for every routine requirement.
- Make relation types and transitive projections deterministic.
- Preserve historical repositories without silent rewrites.
- Keep architecture decisions and implementation verification separate.

## Considered options

1. **Architecture targets only requirements.** Preserves rationale but cannot identify the exact specification contract and perpetuates broad nominal coverage.
2. **Architecture targets only specifications.** Produces a neat linear chain but makes the architectural driver only transitive and cannot distinguish significant from routine requirements.
3. **Retain polymorphic `constrains`.** Minimizes migration but leaves the meaning and target type ambiguous.
4. **Use typed `addresses` and `conforms_to` relations.** Preserves both forms of traceability and makes their different semantics enforceable.

## Decision

Choose option 4. Architecture directly `addresses` only architecturally significant requirements and `conforms_to` applicable specifications. Every addressed requirement must be reachable through at least one conforming specification's `specifies` relation. The reverse is intentionally false: a specification may contain routine requirements that do not drive architecture.

Treat `constrains` as a bounded compatibility relation. Completed unambiguous historical forms receive visible migration advisories; ambiguous mixed forms fail. New and ongoing architecture uses the typed model. Automation never rewrites owner artifacts or infers significance.

## Consequences

- The graph gains an intentional triangle rather than a strictly linear chain.
- Architecture impact analysis can answer both why and under which exact contract.
- Preflight no longer demands nominal architecture coverage for every implemented requirement.
- Validator, preflight, Explorer, policies, templates, tests, and the managed lock must change together.
- Existing artifacts need classification and eventually accountable migration.
- Reusing `conforms_to` in a type-specific relation namespace requires clear target-type validation because verification records already use the same verb for verification contracts.
- Reviewers remain responsible for challenging omitted architectural drivers.

## Validation

Execute `VER-IAR-005`, including fresh typed graphs, inconsistent triangles, routine requirements, work-order applicability, direct-versus-derived Explorer views, every compatibility class, no-rewrite upgrades, security boundaries, and full Python 3.11+ regression.
