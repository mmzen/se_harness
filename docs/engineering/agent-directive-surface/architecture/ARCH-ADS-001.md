+++
id = "ARCH-ADS-001"
type = "architecture"
title = "Prose guarantees move into the workflow contract, result renderer, preflight, and CI verifier"
status = "approved"
owners = ["technical-owner", "repository-owner"]
created = "2026-08-25"
updated = "2026-08-25"
[decision_assessment]
outcome = "adr_required"
triggers = ["public-interface-or-protocol", "cross-cutting-policy", "material-alternatives"]
rationale = "The proposal adds one field to a public result schema, one managed installed file, one optional pull-request trailer read by CI, and a rule that failure renderings live in the machine contract rather than in prose or skills. Material alternatives exist for where each guarantee lives. An ADR is required before this architecture can be approved."
assessed_by = "technical-owner"

[relations]
addresses = ["REQ-ADS-001", "REQ-ADS-002", "REQ-ADS-003", "REQ-ADS-004", "REQ-ADS-005", "REQ-ADS-006"]
conforms_to = ["SPEC-ADS-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T10:36:12Z"
decided_by = "technical-owner"
+++

# Architecture: Prose guarantees move into the workflow contract, result renderer, preflight, and CI verifier

## Context and scope

Every guarantee in the directive surface that works today is one the evaluator
computes: integrity, gates, provenance. Every guarantee that is unmeasured is
one only prose asks for: verbatim return, complete reading, one next step,
findings kept in scope. This architecture assigns each of the six requirements
to an existing component so that the prose asks for nothing the tool cannot
check or render.

## Components and responsibilities

### Workflow contract (`WORKFLOW.json`)

Owns corrective forms per predicate (`ADS-RST-001`). Remains the single
authority for rules, steps, effects, and non-effects. Gains no new rule kinds.

### Result renderer (`workflow_result.py`)

Owns failure rendering (`ADS-RST-002/003`), the schema-2 default and the
schema-1 warning (`ADS-NXT-002`), and the canonical block bytes and digest
(`ADS-DIG-001`).

### Shared step resolver (`workflow.py`, `workflow_procedures.py`)

Owns `ADS-NXT-001/003`. `focus` and `check` become two renderings of one
resolution.

### Preflight (`preflight.py`)

Owns the closed reading manifest (`ADS-RDM-001`) and `W-ADS-002`
(`ADS-DGN-002`).

### Installer (`installer.py`, standard template)

Owns rendering of the operating card as a managed file (`ADS-RDM-002`), the
router reading instruction and scope paragraph (`ADS-RDM-003`, `ADS-SCP-001`),
and the pull-request template line (`ADS-DIG-002`).

### CI selector and workflow (`github_ci.py`, managed workflow)

Owns `W-ADS-001` (`ADS-DGN-001`) and digest recomputation (`ADS-DIG-003`).

## Dependency direction

```text
WORKFLOW.json + QUALITY_GATES.json
        |
        v
shared step resolver ---> result renderer ---> focus / check / --json
        |                        |
        v                        v
   preflight manifest      result_sha256 ---> CI recomputation
        |
        v
 installer: OPERATING_CARD.md, router text, PR template
```

Nothing below the contracts defines a rule. The card, the router paragraph,
and the corrective commands are renderings of contract content.

## Trust and failure boundaries

Pull-request bodies, evidence paths, and Git ancestry are untrusted input.
Diagnostics report and never mutate. The digest binds bytes, not
understanding. Contract loading, card conformance, and CI comparison fail
closed.

## Quality attributes

Determinism (same state, same block, same digest); boundedness (card size,
closed manifest); compatibility (additive schema field, one-release schema-1
window).
