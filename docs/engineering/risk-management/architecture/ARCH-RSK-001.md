+++
id = "ARCH-RSK-001"
type = "architecture"
title = "A risk lifecycle family with stage-resolved disposition and a predicate in existing gates"
status = "draft"
owners = ["technical-owner", "repository-owner"]
created = "2026-08-25"
updated = "2026-08-25"
[decision_assessment]
outcome = "adr_required"
triggers = ["public-interface-or-protocol", "cross-cutting-policy", "material-alternatives"]
rationale = "The proposal adds a lifecycle family and a decision right to the managed contracts, a gate predicate that cross-cuts every stage, two public commands, and a scope exception. Material alternatives exist for each: reusing the definition family, a dedicated risk-owner role, and a dedicated risk gate. An ADR is required before this architecture can be approved."
assessed_by = "technical-owner"

[relations]
addresses = ["REQ-RSK-001", "REQ-RSK-002", "REQ-RSK-003", "REQ-RSK-004", "REQ-RSK-005", "REQ-RSK-006"]
conforms_to = ["SPEC-RSK-001"]
+++

# Architecture: A risk lifecycle family with stage-resolved disposition and a predicate in existing gates

## Context and scope

Risk must be a formal artifact (so `TRC-001` and the validator apply), must
block the stage it threatens (`HRN-008`), and must be disposed by exactly one
accountable role (`DR-010`) without automation deciding (`DR-004/005`). The
architecture places each of those in the component that already owns the
analogous behaviour.

## Components and responsibilities

### Traceability and validator
Own the `risk` type, its `[risk]` schema, score and stage consistency, and
the four relations. Reject malformed risks on the structure or governance
plane like any other artifact.

### Workflow contract
Owns the `risk` lifecycle family, `WFL-RISK-RAISED`, `WFL-RISK-MITIGATING`,
their procedures, the reading steps, and the corrective forms.

### Decision rights
Own `DR-RISK-DISPOSE` and the stage-to-role table. No new role.

### Quality gates and compliance
Own the evaluator `undisposed_risks_threatening_scope` and its seven
predicates; `check`, `transition`, `capture-verification`, and
`prepare-release` evaluate it through the existing checkpoint service.

### Commands
`raise-risk` (preparation, mutation-guarded, writes one file) and `risks`
(read-only). `prepare-release` derives `lists_risks`.

### Configuration and installer
`[risk]` section in the installation file and its template; `doctor`
validates it.

### Explorer and inspect
Render the register and the raised queue; they compute nothing.

## Dependency direction

```text
TRACEABILITY + validator  ->  risk artifacts (identity, relations, score)
        |
WORKFLOW.json (family, rules, steps)  ->  transition / check / focus
        |
QUALITY_GATES.json (evaluator, predicates)  ->  checkpoint service
        |
DECISION_RIGHTS (DR-RISK-DISPOSE, stage table)  ->  transition actor check
        |
raise-risk / risks / prepare-release  ->  files and records
        |
Explorer / inspect  ->  views
```

## Trust and failure boundaries

Score and status are computed from fields the validator checks; an actor
cannot lower a score without the mismatch failing validation. The scope
exception admits only undisposed risk files. A missing `[risk]` section is
the strictest policy, not a disabled one.

## Quality attributes

Bounded effect (only the threatened stage blocks); determinism (same
register, same gate result); compatibility (empty register is a no-op;
existing records untouched).
