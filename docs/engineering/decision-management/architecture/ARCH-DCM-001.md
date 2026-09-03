+++
id = "ARCH-DCM-001"
type = "architecture"
title = "Decision gating architecture"
status = "approved"
owners = ["technical-owner", "quality-owner"]
created = "2026-09-03"
updated = "2026-09-03"

[relations]
addresses = ["REQ-DCM-001", "REQ-DCM-002", "REQ-DCM-003"]
conforms_to = ["SPEC-DCM-001"]

[decision_assessment]
outcome = "adr_required"
triggers = ["public-interface-or-protocol", "data-ownership-or-persistence", "cross-cutting-policy", "difficult-to-reverse", "material-alternatives"]
rationale = "A new persisted artifact type with its own lifecycle family, a gate evaluated at every transition of four other families, a new CLI command and a new decision right change the public interface, the persisted model and a cross-cutting policy, and cannot be withdrawn once decisions are recorded; two alternatives were seriously considered."
assessed_by = "technical-owner"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-03T19:10:33Z"
decided_by = "technical-owner"
reason = "Approved by the accountable repository owner on 2026-09-03 with the instruction 'i approve with execution delegation', after reviewing the decision-artifact proposal and the drafted packet. WO-DCM-001 carries the delegation class: this approval delegates DR-WO-START, DR-WO-COMPLETE and DR-VREC-PREPARE to the delegated-executor role under the required validate check, with the class read from the pull request's base."
+++

# Architecture: Decision gating architecture

## Context and scope

The harness computes lifecycle legality from formal artifacts and evaluates
gates at checkpoints. This architecture adds one artifact type, the
decision, and one gate that reads it, so that a pending decision blocks the
transitions of the artifacts it names and a disposition is a recorded,
attributed act. It addresses `REQ-DCM-001` (blocking), `REQ-DCM-002`
(disposition) and `REQ-DCM-003` (standing deviations), and conforms to
`SPEC-DCM-001`.

## Components and responsibilities

- **Layout registry and templates** (`artifact_layout_registry.py`,
  `templates/README.md`, `DECISION.template.md`) own the type, its prefix
  and its canonical directory.
- **Validator** (`validate_engineering_artifacts.py`) owns the field rules,
  the relation target types, the diagnostics `E-DCM-*` and `W-DCM-*`, and
  the projection of standing deviations onto specifications, work orders
  and records.
- **Workflow contract** (`WORKFLOW.json`, `workflow_contract.json`) owns
  the lifecycle family `decision` and the procedure step that disposes.
- **Quality-gates contract** (`QUALITY_GATES.json`,
  `quality_gates_contract.json`) owns `QGP-DECISION-OPEN` and binds it to
  every transition checkpoint of definitions, work orders, verification
  records and release records.
- **Compliance evaluator** (`workflow_compliance.py`) evaluates the
  predicate and renders the refusal with the corrective command.
- **CLI** (`cli.py`) owns `harnessctl decide` and writes the disposition
  through the same atomic transition path as `transition`.
- **Decision rights** (`DECISION_RIGHTS.md`) own `DR-DECISION-DISPOSE`.
- **Explorer** (generator and template sources) projects open decisions,
  decision trails and standing deviations; the summary metrics gain the
  decision counts and times.

## Dependency direction

Formal artifacts feed the validator. The validator feeds the gate. The gate
feeds the transition. The CLI invokes the transition. The Explorer reads
the validator's projection. No component writes a decision except the CLI
through the transition path, and no presentation component computes
legality.

## Data and control flow

```text
actor raises DEC (create-artifact)  -> validator: fields, relations, E-DCM-*
transition request on blocked X     -> gates: QGP-DECISION-OPEN reads open/deferred DEC
                                    -> refuse with decision, options, role, `decide` command
harnessctl decide DEC --option o    -> decision right check -> atomic transition
                                    -> [disposition] + lifecycle event written
accept on a deviation               -> validator projects standing deviation
                                    -> record evidence lists DEC; Explorer shows it
revisit passed                      -> W-DCM-001 on the specification
```

## Trust boundaries

Decision text is repository content and untrusted: it is rendered as text
in refusals and in the Explorer, never evaluated. The disposition is
trusted only because the tool wrote it under a checked decision right; a
hand-written disposition is a graph error. The gate reads decisions from
the formal tree at the evaluated revision, never from a branch other than
the one under evaluation.

## Required patterns

- One lifecycle family, one predicate, one command, following the existing
  contract shapes.
- Fail closed: an unreadable or malformed decision blocks like an open one.
- Verbatim record: option id and label copied from the artifact into the
  disposition; reason kept as given.
- Time bounds enforced at disposition, not discovered later.
- Additive projection: standing deviations are computed, never written into
  the specification or the record by hand.

## Prohibited patterns

- A numeric priority or any field that admits a transition while a decision
  is open.
- A disposition by a role without the right, or written by hand.
- Deleting or rewriting a decided or withdrawn decision.
- Presentation code deciding whether a decision blocks.
- Reusing the decision type for risks.

## Quality attributes

Determinism (the same tree yields the same refusals and projections),
auditability (every answer attributed and verbatim), bounded ceremony (the
authoring threshold keeps the artifact count small), and reversibility of
the gate's scope through the deferral mechanism only.

## Conformance checks

`VER-DCM-001` checks the gate on fixtures for every blocked family, the
decision-right refusal, the time-bound refusals, the projection onto
records and the Explorer, the diagnostics, the templates and registry, and
the upgrade of a consumer repository.

## Related ADRs

`ADR-DCM-001` decides this architecture: a pending decision is a blocking
artifact with a verbatim disposition, rather than prose, a lifecycle-event
convention, or a field on the concerned artifact.
