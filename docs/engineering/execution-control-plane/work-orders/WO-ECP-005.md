+++
id = "WO-ECP-005"
type = "work_order"
title = "One kernel: schema 2 only, one selector, one precondition engine"
status = "draft"
owners = ["engineering-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[assurance]
commit_bound_verification = "required"
rationale = "The work removes a result schema, merges two rule selectors, and routes `transition` through the contract's gate evaluator. Every later handoff, transition, verification-record, and release-record result is produced by this kernel, so commit-bound assurance is required."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/workflow.py",
  "se_harness/workflow_result.py",
  "se_harness/workflow_compliance.py",
  "se_harness/workflow_contract.py",
  "se_harness/cli.py",
  "se_harness/provenance.py",
  "se_harness/quality_gates_contract.json",
  "templates/repository/standard/docs/engineering/QUALITY_GATES.json",
  "templates/repository/standard/docs/engineering/QUALITY_GATES.md",
  "tests/",
  "docs/engineering/execution-control-plane/evidence/",
]

[relations]
implements = ["REQ-ECP-009", "REQ-ECP-010"]
specifications = ["SPEC-ECP-005"]
architecture = ["ARCH-ECP-001", "ADR-ECP-004"]
verification = ["VER-ECP-005"]
+++

# Work Order: One kernel: schema 2 only, one selector, one precondition engine

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification, the assurance-owner decision, integration, and release are
separate decisions by the roles that own them. Approval of `REQ-ECP-009`,
`REQ-ECP-010`, `SPEC-ECP-005`, `ARCH-ECP-001`, `ADR-ECP-004`, and
`VER-ECP-005` are separate acts by their owners and precede approval of
this work order. This work order is independent of the others but precedes
`WO-ECP-006`, which unlocks transitions through the gate evaluator this
work order installs.

## Objective

End every disagreement between `check` and `transition` on the same state.
Today there are two result envelopes, two rule engines, and three
precondition implementations (complexity audit P0-6,
`docs/notes/complexity-audit-2026-08.md:224-253`): schema 1 is still the
default on `transition`, `capture-verification`, and `prepare-release`;
`_recommend` and `select_rule` compute `successor_id` differently; the
gate contract's `transition` checkpoint is unreachable because
`check_workflow` refuses it (`se_harness/workflow_compliance.py:395`) while
`QUALITY_GATES.md` `QG-010` promises transitions recheck contract
predicates (the 2026-08 agentic execution review, section 3).

## In scope

- Schema 2 as the only result of `focus`, `check`, `transition`,
  `capture-verification`, and `prepare-release`; `--result-schema 1`
  refused; `legacy_to_schema2` and the schema-1 `handoff` renderer removed,
  per `ECP-KRN-*`.
- `_recommend` delegating to `select_rule`; one context builder.
- `plan_transition` evaluating the contract's `transition` checkpoint gates
  through `_gate_results`; `_validate_preconditions` reduced to
  graph-structural checks; transition failures labelled by predicate rather
  than a blanket `WEX201` (`se_harness/cli.py:521`).
- `se_harness/provenance.py` rendering its results in schema 2 only.
- The `transition` checkpoint made explicit in
  `se_harness/quality_gates_contract.json` and its template renderings
  `QUALITY_GATES.json` and `QUALITY_GATES.md`.
- Tests; work-order-keyed evidence.

## Out of scope

- Authenticating decisions (`WO-ECP-004`); the delegation class
  (`WO-ECP-006`); the root managed `QUALITY_GATES.*` copies; any change to
  a gate predicate's identifier or meaning, to lifecycle states, or to
  decision rights; any lifecycle transition of any artifact.

## Authorized decision envelope

The implementation agent may decide how the shared context is built, the
refusal diagnostic for schema 1, and test names. It may not change
`result_sha256`'s definition over the schema-2 block, add a predicate
outside the existing `QG-`/`QGP-` identifiers, or write outside the listed
paths.

## Constraints

- Use the exact released evaluator, se-harness 0.7.1, installed outside the
  checkout, for identity, integrity, graph, focus, and preflight readings;
  exercise the candidate `transition` only against temporary repositories.
- Root managed copies are not edited.
- LF line endings; assert bytes against blobs.
- Stage every deletion before any preflight or check run.

## Expected change surface

The workflow kernel, the result renderer, the compliance module's
checkpoint entry, the contract loader and selector, the CLI defaults, the
provenance module's result path, one gate contract and its two template
renderings, tests, evidence.

## Required verification

Execute `VER-ECP-005` completely plus the repository-required checks; run
the complete suite on Linux and Windows with figures labelled per platform.

## Evidence to record

Under `docs/engineering/execution-control-plane/evidence/WO-ECP-005/`:
paired `check` and `transition` results per fixture, the mutated contract
copy and outcome, refusal diagnostics, per-platform test figures, and the
complete changed-path set.

## Stop and escalate conditions

Stop if any consumer of schema 1 is found outside tests, if the
`transition` checkpoint cannot be evaluated without a new predicate
identifier, if the released evaluator refuses the edited gate contract, or
if any path outside scope must change.

## Completion report format

Return the `harnessctl check . --artifact WO-ECP-005 --checkpoint handoff`
schema-2 block verbatim with the complete changed-path set asserted, and
its `result_sha256`.
