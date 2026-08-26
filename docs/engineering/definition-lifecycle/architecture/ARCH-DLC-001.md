+++
id = "ARCH-DLC-001"
type = "architecture"
title = "One question per mechanism: declared generation, terminal approval, derived realization"
status = "draft"
owners = ["technical-owner", "repository-owner"]
created = "2026-08-26"
updated = "2026-08-26"

[relations]
addresses = ["REQ-DLC-001", "REQ-DLC-002", "REQ-DLC-003", "REQ-DLC-004", "REQ-DLC-005"]
conforms_to = ["SPEC-DLC-001", "SPEC-DLC-002", "SPEC-DLC-003"]

[decision_assessment]
outcome = "adr_required"
triggers = ["responsibility-or-dependency-direction", "public-interface-or-protocol", "cross-cutting-policy", "material-alternatives"]
rationale = "The proposal retires a reachable state from the managed lifecycle contract that every consumer repository pins, removes a status input from a managed validator script, and adds two mandatory governance obligations with declared grandfathering. It changes the dependency direction between lifecycle status, validator behavior, and coverage reporting, and it defines a public declaration surface inside work orders. Material alternatives exist for each of the three increments and for the grandfathering mechanism. Two ADRs are required before this architecture can be approved."
assessed_by = "technical-owner"
+++

# Architecture: One question per mechanism: declared generation, terminal approval, derived realization

## Context and scope

A definition's lifecycle status is currently read as an answer to three unrelated
questions: does this artifact govern, which schema generation is it, and has it
been built. `INT-DLC-001` establishes that the three are conflated and that each
wrong answer is load-bearing somewhere.

This architecture assigns exactly one mechanism to each question and fixes the
dependency direction between them. `SPEC-DLC-001` owns the generation mechanism,
`SPEC-DLC-002` owns lifecycle termination and the realization derivation, and
`SPEC-DLC-003` owns the recorded-decision obligation. Existing architecture
continues to own everything else: `ARCH-VSP-001` and the migration contract own
version and predecessor boundaries, `ARCH-IAR-*` own artifact validation
structure, and the release architecture owns distribution.

Three increments land in a fixed order. Nothing here migrates an artifact, edits
an artifact field, or changes the status vocabulary.

## Components and responsibilities

### Declared generation resolver

A new pure module, mirroring `se_harness/legacy_release_evidence.py`, owns the
answer to "is this architecture exempt from the required decision assessment".
Its only inputs are the frozen 14-identifier self-hosting set and declarations
inside approved work orders. It owns no status reading, and the constant
`LEGACY_ARCHITECTURE_STATUSES` is removed from both validator copies.

It does not own `E015`, the missing-deciding-ADR error, and does not own `W015`,
the deprecated-`constrains` finding. Both are unchanged and both are already
status-independent.

### Managed lifecycle contract

`se_harness/workflow_contract.json` and the standard template's
`docs/engineering/WORKFLOW.json` own the reachable transition graph. They keep
their byte-identical relationship. The definition family's `approved` row loses
its `implemented` target; the `implemented` row is retained as unreachable,
visible, authority-granting compatibility vocabulary, exactly as `ready`,
`in_progress`, `verified`, `released`, and `superseded` already are in that
family.

`WORKFLOW.md`, `DECISION_RIGHTS.md`, and `QUALITY_GATES.md` remain the managed
narrative authority. `WORKFLOW.md`'s state table changes; `DR-DEFINITION-DECIDE`
does not, because it already describes only the approve-or-reject decision that
survives.

### Workflow recommendation table

The contract's `recommendations` own routing. `WFL-DEFINITION-COMPLETE` keeps its
identifier and its `approved` match and is re-pointed at work selection.
`WFL-DEFINITION-WORK` keeps matching `implemented` so the 165 existing
implemented definitions keep a resolvable recommendation.
`PROC-DEFINITION-COMPLETE` and `STEP-DEFINITION-COMPLETE`, the only carriers of
an `implemented` outcome no decision right authorizes, are retired.

The resolver `se_harness/workflow.py` is unchanged. Its `RuntimeError` on an
unmatched `(artifact_type, status)` pair is the reason the conformance
enumeration is mandatory rather than optional.

### Realization derivation

A new pure read-only function owns the answer to "has this definition been
built". It reads work-order statuses and the verification records bound to them,
classifies each requirement, specification, and architecture as covered,
partially covered, or uncovered, and names the exact commit of each covering
record. It joins the existing shared finding family as `I-DLC-001` and
`W-DLC-001`, rendered in `inspect` only; the dashboard and explorer surfaces are
a decided deferral to separately approved work.

It stores nothing, proposes no transition, and never reads the definition's own
status. It is surface-independent, so the deferred rendering work adds a renderer
and no logic.

### Recorded-decision obligation

The existing `validate_lifecycle_events` owns chain shape, ordering, actor, and
append-only rules and keeps them unchanged. Its `events is None` early exit is
replaced by the obligation plus a second declared-exemption resolver, of the same
shape as the generation resolver, holding the frozen 449-identifier pre-contract
set.

### Declaration surface

Work-order declaration packets own consumer grandfathering for both new
obligations. The surface is the one `SPEC-LRE-001` already established: a bounded
array inside an approved work order, resolving only after a recorded
`draft -> approved` event, fail-closed, and reported when it resolves nothing.

### Outcome-preservation harness

The test suite owns the assertion that no existing outcome moves. It measures the
released-lineage verdict at the merge base and at each candidate, asserts exact
diagnostic identifier-set equality rather than cardinality, and asserts that a
derivation run leaves every file byte-identical.

## Dependency direction

```text
governed artifact content (statuses, relations, lifecycle_events)
                              |
        +---------------------+---------------------+
        |                     |                     |
        v                     v                     v
 declared generation   managed lifecycle    declared pre-contract
     resolver              contract              resolver
        |                     |                     |
        v                     v                     v
   E014 / W014        legality + routing        E022 / W025
        |                     |                     |
        +---------------------+---------------------+
                              |
                              v
            work orders -> verification records -> commits
                              |
                              v
                  realization derivation (read-only)
                              |
                              v
                    I-DLC-001 / W-DLC-001 report
                              |
                              v
                 existing accountable decision point
```

Each mechanism reads governed content and reports. None reads another's output,
and none writes. The realization derivation sits strictly downstream of work
orders and records and strictly upstream of nothing. No arrow runs from a report
back into an artifact field, which is what makes `HRN-006` hold structurally
rather than by discipline.

## Data and control flow

1. The evaluator loads the artifact graph.
2. For each architecture with no `decision_assessment`, the generation resolver
   consults the frozen set, then approved declarations, and returns exempt with a
   source or not-exempt with a stable reason. The architecture's status is never
   read.
3. Exempt architectures report `W014`; the rest report `E014`. `E015` is decided
   afterwards, unchanged, from ADR `decides` relations.
4. For each definition whose status is not `draft`, the chain is checked. Absent
   chains consult the pre-contract resolver and report `W025` when it resolves,
   `E022` when it does not. Malformed chains report the existing diagnostics and
   never consult the resolver.
5. A transition plan for a definition is checked against the contract. `approved
   -> implemented` is refused through the ordinary legality path.
6. Routing resolves a recommendation from the target status, which for every
   status present in any repository matches exactly one rule.
7. On `inspect`, the derivation walks work orders and records and
   emits coverage findings, citing records and commits and claiming no authority.
8. Any accountable decision is supplied by the existing harness procedure. None
   of the above adds a decision, a role, or a gate.

## Trust boundaries

- Artifact metadata, work-order text, declaration arrays, and declared
  identifiers are untrusted parser input.
- The frozen sets are compile-time constants in both implementations and are not
  configurable, overridable, or extendable at runtime.
- A declaration is trusted only after its work order's `draft -> approved` event
  is present. Approval authority stays with the engineering owner.
- No mechanism reads a lock, an installed evaluator identity, an environment
  value, a command-line flag, or Git state beyond commits the records bind.
- No mechanism writes a file, runs a subprocess, or performs a network or Git
  operation.
- Verification records remain the only accountable statement about a commit. The
  derivation cites them and never restates or replaces them.
- A green validation run is evidence about the graph, not evidence that the
  exempt populations are complete.

## Required patterns

- Declaration over inference for every grandfathering decision, on the
  `SPEC-LRE-001` model.
- Frozen, closed, compile-time self-hosting sets with a named declarer.
- A bounded per-declaration entry count and an approval precondition.
- Fail-closed resolution: a defective declaration resolves nothing.
- Exemption suppresses the error and never the diagnostic.
- Equivalent package and self-contained implementations agreeing on one shared
  committed vector fixture.
- Retained unreachable status rows for compatibility vocabulary.
- Retained published identifiers even when their behavior changes, with the
  residue disclosed.
- Derived-and-reported rather than stored for any fact that can be falsified
  later.
- Exact identifier-set equality assertions on diagnostic outcomes.
- Per-platform labelling of every measured figure.

## Prohibited patterns

- Reading a lifecycle status to decide a schema generation, a validator branch,
  or a grandfathering outcome.
- Fabricating, defaulting, inferring, or backfilling a `lifecycle_events` chain.
- Migrating, normalizing, superseding, or re-deciding any of the 165
  `implemented` definitions or the 449 chainless ones.
- Storing a realization or coverage result in an artifact field.
- Adding an identifier to a frozen set, or making a set configurable.
- Any flag, field, or configuration that suppresses `W014` or `W025`.
- Deleting the `implemented` row, or removing `implemented` from
  `ALLOWED_STATUSES`.
- Re-admitting the retired edge to accommodate a predecessor evaluator, instead
  of using the migration contract's adapter path.
- Introducing a new decision right, role, quality gate, artifact type, relation
  type, or artifact field.
- Landing the recorded-decision obligation before the first two increments
  settle, or measuring its frozen set before they do.
- Treating a reduced warning count as an improvement.

## Quality attributes

- **Authority clarity:** each of the three questions has exactly one mechanism,
  and no mechanism answers a question it does not own.
- **Correctness under change:** a fact that a later work order can falsify is
  derived, so a sixteenth work order reopens coverage automatically.
- **Honesty:** every grandfathered population stays visible as an outstanding
  diagnostic on every run, permanently.
- **Determinism:** identical graph content produces identical resolutions,
  findings, and ordering, with no environment input.
- **Consumer safety:** a repository that would break is blocked with a named
  remedy, never partially migrated.
- **Auditability:** every exemption names its source, and every declaration that
  fails names its reason.
- **Compatibility:** no artifact byte changes, no status becomes invalid, and the
  existing diagnostic identifier sets are preserved exactly.
- **Reviewability:** each increment is one work order with an independently
  measurable outcome.

## Conformance checks

- Assert `LEGACY_ARCHITECTURE_STATUSES` is absent from both validator copies and
  that no code path reads an architecture status in the assessment.
- Fixture-remove each of the 14 frozen identifiers and assert each becomes
  `E014`, proving the declaration and not the status suppresses the error.
- Assert the exempt architecture set is byte-for-byte the same identifier set
  before and after the first increment.
- Enumerate all nine definition families against every status in
  `ALLOWED_STATUSES` and assert no pair occurring in the graph reaches
  `_recommend`'s `RuntimeError`.
- Assert the reachable transition graph matches the `WORKFLOW.md` state table
  exactly, and that the two contract copies are byte-identical.
- Plan `approved -> implemented` on one artifact of each definition family and
  assert every plan is refused; plan `approved -> rejected` and assert each
  succeeds.
- Validate and focus each of the 165 existing `implemented` definitions and
  assert zero errors, a resolvable recommendation, and unchanged bytes.
- Exercise the derivation over covered, partially covered, uncovered, reopened,
  rejected-record, and superseded-record graphs, and assert byte-identical files
  after every run through an independent write sentinel.
- Author a fixture definition with a non-`draft` status and no chain, in no
  declaration, and assert `E022`; add a recorded event and assert it validates.
- Exercise every declaration failure mode for both resolvers: shape, size,
  duplicate keys, unapproved work order, invalid identifier, unknown target,
  ambiguous target, wrong target type, and already-satisfied target.
- Assert both implementations agree on the shared committed vector fixtures.
- Measure the released-lineage verdict at the merge base and at each candidate on
  Windows and Linux separately, and assert exact equality of the `W013`, `W014`,
  and `W015` identifier sets.
- Provide a governance-migration scenario for the version pair each increment
  lands in.

## Related ADRs

`ADR-DLC-001` proposes replacing status inference with declaration for all three
questions, in three ordered increments, with no data migration. `ADR-DLC-002`
proposes the grandfathering mechanism — enumerated frozen vectors versus a frozen
cutover date over `created`. Both remain draft and must be accepted or revised by
the technical owner before this architecture can be approved.
