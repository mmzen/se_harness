+++
id = "ADR-RSK-001"
type = "adr"
title = "Model risk as its own lifecycle family, dispose by stage owner, gate through existing gates"
status = "approved"
owners = ["technical-owner", "repository-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
decides = ["ARCH-RSK-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T13:25:29Z"
decided_by = "technical-owner"
+++

# ADR: Model risk as its own lifecycle family, dispose by stage owner, gate through existing gates

## Status

Proposed.

## Context

Three independent choices shape the risk artifact: which lifecycle it
follows, who disposes it, and how it blocks. Each has a plausible
alternative that would reduce new surface at the cost of meaning.

## Decision drivers

- `HRN-008` fail closed; `DR-001`/`DR-010` one accountable actor; `HRN-003`
  bounded effect.
- Closed role catalogue; closed evaluator key set; nine fixed restitution
  headings.
- Owner decisions of 2026-08-25: stage-resolved disposer; default raise
  everything; `mitigating` blocks release; 5x5.

## Considered options

### Lifecycle: own family (chosen) vs. reuse `definition`
The definition states (`draft -> approved -> implemented`) carry approval
authority a risk never has, and none of accept/avoid/mitigate. Reuse would
force prose to carry the disposition — exactly what the harness forbids.

### Disposer: stage owner (chosen) vs. dedicated risk owner
A dedicated role centralises but adds a seventh role that solo owners hold
anyway, and separates the risk from the person who owns the thing at risk.
Stage resolution keeps `DECISION_RIGHTS.md` closed and the decision local.

### Blocking: predicate in existing gates (chosen) vs. a new `QG-RISK` gate
A new gate would need its own workflow rule bindings and would not inherit
the corrective-form rendering; a predicate lands in every checkpoint the
harness already evaluates and is rendered like any other blocker.

### Raising: computed at creation (chosen) vs. a human raise decision
A human raise step would let a risk sit `identified` by omission. Computing
the comparison at creation is preparation, like a VREC being created `ready`.

## Decision

Own family; stage-resolved `DR-RISK-DISPOSE`; one evaluator across seven
existing gates; computed raise; default acceptance level 1; `mitigating`
blocks release; 5x5 scale.

## Consequences

- Managed contracts change (family, rule, predicates, right); repositories
  receive them at their next governor upgrade.
- The scope exception is a deliberate hole in `changed_paths_within_scope`,
  bounded to undisposed risk files.
- Independence between raiser and disposer is not provided; that is an
  assessment-service property, out of scope.
