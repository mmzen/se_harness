+++
id = "SPEC-IAR-004"
type = "specification"
title = "Conditional ADR applicability and enforcement contract"
status = "implemented"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
specifies = ["REQ-IAR-012"]
+++

# Specification: Conditional ADR applicability and enforcement contract

## Scope

Add an explicit decision-assessment contract to architecture artifacts, distribute authoring guidance, replace unconditional work-order ADR selection with per-architecture conditional coverage, and expose the result through validation, preflight, CI, and Explorer.

## Metadata contract

Each compliant architecture artifact contains:

```toml
[decision_assessment]
outcome = "adr_required"
triggers = ["system-boundary", "data-ownership-or-persistence"]
rationale = "The design selects component boundaries and durable data ownership."
assessed_by = "technical-owner"
```

or:

```toml
[decision_assessment]
outcome = "no_significant_decision"
triggers = []
rationale = "The work applies the previously approved architecture without changing a material trade-off."
assessed_by = "technical-owner"
```

Fields have these rules:

- `outcome` is exactly `adr_required` or `no_significant_decision`.
- `triggers` is a duplicate-free list using only the controlled values in `REQ-IAR-012`.
- `rationale` and `assessed_by` are non-empty strings.
- `adr_required` requires at least one trigger.
- `no_significant_decision` requires zero triggers.

## Behavioral rules

1. The architecture template contains the structured block, trigger checklist, examples, and an instruction that omission is not a no-ADR decision.
2. The ADR template explains that an ADR captures one significant coherent decision, may cover several requirements or architectures, and is not created merely to satisfy a one-per-artifact quota.
3. `WORKFLOW.md` requires decision applicability assessment during architecture definition before work-order approval.
4. `DECISION_RIGHTS.md` assigns assessment accountability and no-ADR rationale acceptance to the technical owner; an implementation agent may draft but not self-approve the assessment unless separately named in that accountable role.
5. `QUALITY_GATES.md` defines G2 as passing only when every applicable architecture has a valid assessment and every `adr_required` architecture has active deciding ADR coverage.
6. `TRACEABILITY.md` defines architecture-to-ADR coverage by `ADR.decides -> ARCH`, independent of requirement cardinality.
7. The work-order template states that its `architecture` relation selects every applicable architecture and every required deciding ADR; an ADR is omitted only for a selected architecture with an accepted `no_significant_decision` assessment.
8. Formal validation checks the metadata schema and internal contradictions. It emits errors for malformed assessments and rejects `decision_assessment` on a non-architecture artifact.
9. Preflight evaluates every architecture selected by the work order. It replaces unconditional `W015` behavior with stable decision-assessment diagnostics and retains the existing wrong-target check.
10. Preflight succeeds without an ADR only when every selected architecture has a valid `no_significant_decision` assessment. It requires at least one selected active ADR deciding each `adr_required` architecture.
11. CI inherits the rule through candidate validation and review preflight; it never infers significance from a diff.
12. Explorer shows one of `ADR required: covered`, `ADR required: missing`, `No significant decision: justified`, `Assessment missing`, or `Assessment invalid` per architecture and reports unresolved states as anomalies.

## Diagnostic contract

Stable diagnostics must distinguish:

- assessment missing;
- invalid outcome, trigger, rationale, or assessor;
- `adr_required` with no trigger;
- `no_significant_decision` with a trigger;
- required deciding ADR missing;
- selected ADR does not decide a selected architecture.

Exact numeric codes are delegated to implementation, but text and JSON output must preserve these categories deterministically.

## Migration and compatibility

- Freshly scaffolded architecture drafts include unresolved assessment placeholders and cannot become active without completion.
- Existing completed architecture artifacts are not rewritten automatically.
- During one published compatibility window, `implemented`, `verified`, or `released` architecture with no assessment is classified deterministically as legacy and produces a visible advisory in repository-wide validation and Explorer. Preflight may accept it only when an active selected ADR already decides it; absence of either the assessment or related ADR coverage otherwise fails.
- Architecture in `draft`, `approved`, or `in_progress` state cannot use the legacy exception.
- A completed architecture is historical for this rule and must not be materially rewritten to introduce a new decision. New architectural choices require a new draft architecture artifact and assessment; candidate review remains responsible for detecting an attempted semantic rewrite.
- A later separately governed release may remove the legacy exception after migration evidence exists.
- Installation and upgrade update managed templates, validators, Explorer, and policies transactionally and never move or rewrite repository-owned formal artifacts.

## Security and authority boundaries

Artifact metadata, paths, relations, trigger strings, and rationale text are untrusted input. Validation never executes rationale text or shell-interpolates artifact values. Automation can verify structured consistency but cannot approve architecture risk, generate authority, or infer a significant decision from arbitrary prose or source.

## Explicitly unspecified decisions

Diagnostic numbers, parser-helper boundaries, dashboard styling, and the exact compatibility-warning label are delegated to implementation if deterministic and consistent with this contract.
