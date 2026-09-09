+++
id = "SPEC-AUT-004"
type = "specification"
title = "Closing the compatibility windows: the retired relation, the unassessed architecture, the header-less packet, the v1 hint"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-09"
updated = "2026-09-09"
contract = "The validator, the preflight, the evidence predicate and the contract loader hold no branch for the migrated corpus windows; two historical gaps stay and are documented as permanent."

[relations]
specifies = ["REQ-AUT-009"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-09T17:21:18Z"
decided_by = "technical-owner"
reason = "Approved on 2026-09-09 by the accountable owner by selecting the presented option 'Approve all four (Recommended)', given after the packet closing the compatibility windows (issue #381 owner decision 3 of 2026-09-07, migrate the corpus then close; SPEC-AUT-003 AUT-MIG-012) was presented on pull request #423 with the released 0.16.0 evaluator reading 0 errors and 0 authoring advisories. Approval of a definition authorizes no work. Rules AUT-WIN-001 to AUT-WIN-018. In the same prompt the owner selected 'Keep the template out of scope (Recommended)': the TRC-008 sentence of the managed TRACEABILITY.md template stays untouched and is owed to the next managed-template work order, as AUT-WIN-018 states."
+++

# Specification: Closing the compatibility windows: the retired relation, the unassessed architecture, the header-less packet, the v1 hint

## In plain words

One work order deletes four tolerances the corpus no longer needs and their
four codes. Each is replaced by the refusal that already exists beside it,
and the two tolerances that stay are written down.

## Scope

Seven modules: `se_harness/engine/validation_architecture.py`,
`se_harness/engine/validation_decisions.py`,
`se_harness/engine/dashboard_snapshot.py`, `se_harness/preflight.py`,
`se_harness/workflow_predicates.py`, `se_harness/workflow_contract.py` and
`se_harness/codes.py`. With them come the tests that pin them, the
diagnostic-code index and the two notes that describe the grace and the
tolerances. Four specifications that still name a window gain an amendment
record. The corpus does not change (`REQ-AUT-008`), and no managed template
changes.

## Terms

- **Window.** A branch of the validator, the preflight, a predicate or a
  loader that accepts a shape the rules no longer admit. It names the
  acceptance with a warning or a hint.
- **Baseline.** The released 0.16.0 evaluator's `validate` on `main` at the
  work order's base: 0 errors, 44 `W013`, no other warning, 0 advisories.

## Rules

**AUT-WIN-001.** `architecture_traceability_state` MUST report a
`constrains` relation as an issue naming it retired, whatever the
architecture's status, so that `validate` reports `E016`.

**AUT-WIN-002.** The states `dual_declared`, `legacy_requirement_trace`,
`legacy_specification_trace` and `legacy_ambiguous`, the `legacy_targets`
field and the `constrains` entry of `RELATION_TARGET_TYPES` MUST go.

**AUT-WIN-003.** `decision_assessment_state` MUST return `missing` for every
architecture without a `decision_assessment` table, so that a completed one
reads `E014` like any other.

**AUT-WIN-004.** The `legacy_missing` state, the `W014` branch and the
legacy `E015` message MUST go, while `E015` stays for an `adr_required`
architecture without an active deciding ADR.

**AUT-WIN-005.** The preflight MUST read relevance and applicability from
the `typed` state alone and MUST emit no `W019`, which leaves the registry.

**AUT-WIN-006.** The dashboard MUST drop the `legacy_adr_covered` and
`legacy_adr_missing` assessment states and `constrains` from its
architecture relation set.

**AUT-WIN-007.** `QGP-G4I-EVIDENCE` MUST read the machine header only,
reporting a packet without one as `not_assessable` with the `evidence`
command as the corrective.

**AUT-WIN-008.** The substring fallback of that predicate and `W-ECP-002`
MUST go.

**AUT-WIN-009.** `load_quality_gate_contract` MUST raise the loader's own
schema error for any schema it does not accept, and
`RETIRED_QUALITY_GATES_SCHEMAS` with the v1 hint MUST go.

**AUT-WIN-010.** `WEX-ECP-030` MUST stay for every transition-binding fault
it names today.

**AUT-WIN-011.** `W014`, `W015`, `W019` and `W-ECP-002` MUST leave
`se_harness/codes.py` and the diagnostic-code index with no tombstone
(`SPEC-ECP-022`, the `ECP-TMB` policy).

**AUT-WIN-012.** The `prepared_at` branch and the `execution_scope` branch
MUST stay, each documented as permanent at the branch and in
`docs/notes/artifact-authoring.md` with the counts measured at the base.

**AUT-WIN-013.** `SPEC-ECP-002`, `SPEC-ECP-005`, `SPEC-ECP-017` and
`SPEC-WEX-002` MUST be amended by record where they promise the grace or
the hint, with no rule identifier, statement or relation moving.

**AUT-WIN-014.** `docs/notes/harnessctl-reference.md` MUST stop describing
the grace, and `docs/notes/diagnostic-codes.md` MUST be regenerated from the
source.

**AUT-WIN-015.** Tests MUST pin AUT-WIN-001 to AUT-WIN-011: the two
refusals, the absent `W019`, the `not_assessable` packet, the loader's own
error, the absent codes and the dashboard sets.

**AUT-WIN-016.** `validate` on the candidate MUST report 0 errors with every
count equal to the baseline, and the released 0.16.0 evaluator's reading of
the same tree MUST equal it.

**AUT-WIN-017.** The change set MUST hold only the seven modules of the
Scope, `tests/`, the notes and the index, the four amendment records, this
packet, the domain index and the evidence.

**AUT-WIN-018.** This work MUST NOT change a managed template, a root
managed byte or a corpus artifact; the `TRC-008` sentence of the
`TRACEABILITY.md` template is owed to the next managed-template work order.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| an architecture declares `constrains` | validation fails naming the file and the retired relation | `E016` |
| a completed architecture has no `decision_assessment` | validation fails naming the file | `E014` |
| an evidence packet has no machine header | the handoff check does not complete; the corrective is `harnessctl evidence` | `QGP-G4I-EVIDENCE` `not_assessable` |
| `QUALITY_GATES.json` carries `se-harness-quality-gates-v1` | the loader refuses before any read | the loader's schema error |
| a module still emits a retired code | the registry test fails naming the code | test failure |
| a test still expects a retired warning | the test fails naming it | test failure |

## Examples

**Given** an approved architecture with `constrains = ["REQ-X"]` in a
scratch copy, **when** `validate` runs, **then** it reports `E016` naming
the retired relation and the file (AUT-WIN-001).

**Given** an implemented architecture whose `[decision_assessment]` table
is removed in a scratch copy, **when** `validate` and the preflight run,
**then** `validate` reports `E014` and the preflight prints no `W019`
(AUT-WIN-003, AUT-WIN-005).

**Given** a packet bound by the older substring lines and no header, **when**
the handoff check runs, **then** `QGP-G4I-EVIDENCE` is `not_assessable` and
names `harnessctl evidence` (AUT-WIN-007).

**Given** this repository, **when** the candidate and the released 0.16.0
evaluator validate it, **then** both report 0 errors and 44 `W013`
(AUT-WIN-016).

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-AUT-009` | AUT-WIN-001, AUT-WIN-002, AUT-WIN-003, AUT-WIN-004, AUT-WIN-005, AUT-WIN-006, AUT-WIN-007, AUT-WIN-008, AUT-WIN-009, AUT-WIN-010, AUT-WIN-011, AUT-WIN-012, AUT-WIN-013, AUT-WIN-014, AUT-WIN-015, AUT-WIN-016, AUT-WIN-017, AUT-WIN-018 |

## Not decided here

- The exact wording of the `E016` and `E014` messages and of the
  `not_assessable` text, provided each names what is missing.
- The wording of the four amendment records and of the two note sentences.
- Where the test pins live: the existing traceability, applicability,
  compliance and contract modules, or one new module.

## Compatibility and migration

A consumer whose corpus still holds `constrains` or an unassessed completed
architecture reads `E016` or `E014` after upgrading to the carrying
release. Before, it read `W015` or `W014`. The retained rewrite scripts
under `docs/engineering/artifact-authoring/evidence/WO-AUT-005/` are the
migration. A packet bound by substring lines needs `harnessctl evidence`
once. This repository's own root evaluator keeps the windows until the root
adoption of the carrying release; the corpus satisfies both readings
already.
