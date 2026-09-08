+++
id = "WO-AUT-005"
type = "work_order"
title = "Wave 5, corpus: typed architecture relations, decision assessments, the vocabulary verification method"
status = "draft"
owners = ["engineering-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[assurance]
commit_bound_verification = "required"
rationale = "The change rewrites the front matter of two hundred and eighty-six approved or implemented formal artifacts, the traceability every later reading of the graph relies on, and it is the precondition of the validator work order that closes the windows."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "docs/engineering/agent-directive-surface/requirements/",
  "docs/engineering/agentic-execution/requirements/",
  "docs/engineering/aggregate-release/architecture/",
  "docs/engineering/aggregate-release/requirements/",
  "docs/engineering/artifact-authoring/README.md",
  "docs/engineering/artifact-authoring/evidence/",
  "docs/engineering/artifact-authoring/requirements/",
  "docs/engineering/artifact-authoring/specifications/",
  "docs/engineering/artifact-authoring/verification-records/",
  "docs/engineering/artifact-authoring/verification/VER-AUT-003.md",
  "docs/engineering/artifact-authoring/work-orders/WO-AUT-005.md",
  "docs/engineering/ci-pipeline/requirements/",
  "docs/engineering/dashboard-publication/requirements/",
  "docs/engineering/evidence-keying/requirements/",
  "docs/engineering/harness-distribution/architecture/",
  "docs/engineering/harness-distribution/requirements/",
  "docs/engineering/hash-bound-integrity/requirements/",
  "docs/engineering/instruction-architecture/architecture/",
  "docs/engineering/instruction-architecture/requirements/",
  "docs/engineering/integration-package/requirements/",
  "docs/engineering/legacy-release-evidence/requirements/",
  "docs/engineering/operating-contract-activation/requirements/",
  "docs/engineering/portable-managed-integrity/architecture/",
  "docs/engineering/portable-managed-integrity/requirements/",
  "docs/engineering/pypi-publication/architecture/",
  "docs/engineering/pypi-publication/requirements/",
  "docs/engineering/release-contract-disposition/requirements/",
  "docs/engineering/release-orchestration/requirements/",
  "docs/engineering/released-evaluator-boundary/requirements/",
  "docs/engineering/repository-harness-upgrade/requirements/",
  "docs/engineering/revision-provenance/architecture/",
  "docs/engineering/revision-provenance/requirements/",
  "docs/engineering/root-cause-analysis/requirements/",
  "docs/engineering/self-hosting-boundary/requirements/",
  "docs/engineering/technical-communication/requirements/",
  "docs/engineering/test-suite/requirements/",
  "docs/engineering/verification-supersession/architecture/",
  "docs/engineering/verification-supersession/requirements/",
  "docs/engineering/work-order-assurance-classification/requirements/",
  "docs/engineering/work-order-lifecycle/architecture/",
  "docs/engineering/work-order-lifecycle/requirements/",
  "docs/engineering/workflow-execution/requirements/",
  "docs/notes/artifact-authoring.md",
  "scripts/migrate_verification_methods.py",
  "tests/",
]

[relations]
implements = ["REQ-AUT-008"]
specifications = ["SPEC-AUT-003"]
verification = ["VER-AUT-003"]
+++

# Work Order: Wave 5, corpus: typed architecture relations, decision assessments, the vocabulary verification method

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. It carries no delegation table: it rewrites
approved and implemented artifacts, and each of its fourteen retroactive
assessments is a technical-owner statement, so its start, completion and
record preparation are the engineering owner's explicit decisions. Its
authoritative state, and the timestamp and reason of every decision taken on
it, are the front matter and `[[lifecycle_events]]` above. Commit-bound
verification is `required`.

The owner's decision 3 on issue #381 (2026-09-07) orders this migration
first; the validator work order that closes the windows follows in the next
candidate and is drafted after this one merges.

## Objective

Execute rules `AUT-MIG-001` to `AUT-MIG-011` of `SPEC-AUT-003`: the fifteen
legacy architectures take `addresses` and `conforms_to`, the fourteen without
an assessment gain one naming their deciding ADR, the verification-method
migration is applied once with four steward decisions, and the script leaves
the repository with its test and its note paragraph.

## In scope

- The fifteen architectures measured on `main` at `a68caf70`: `ARCH-AGR-001`,
  `ARCH-DST-001` to `-005`, `ARCH-IAR-001` to `-004`, `ARCH-PMI-001`,
  `ARCH-PYP-001`, `ARCH-REV-001`, `ARCH-VSP-001`, `ARCH-WLC-001`; all but
  `ARCH-IAR-004` also gain the assessment. Each has exactly one deciding ADR
  and every constrained requirement has a specifying specification.
- The 271 requirements with a string `verification_method`, across the 32
  `requirements/` directories listed in the scope; the four steward
  decisions on `REQ-REB-004`, `-011`, `-014` and `-018`.
- `scripts/migrate_verification_methods.py`, its test
  `test_migration_maps_strings_keeps_originals_and_is_idempotent`, and the
  paragraph of `docs/notes/artifact-authoring.md` that describes it: deleted
  after the run.
- The corpus test of `AUT-MIG-009`; the amendment record on `SPEC-AUT-001`;
  the domain index; the evidence packet.

## Out of scope

- Any change to `se_harness/`: the `W014` and `W015` branches, the
  `W-ECP-002` grace, the `WEX-ECP-030` hint and the notes on the
  `prepared_at` and `execution_scope` branches are the following work order.
- The prose bodies of the migrated artifacts beyond the amendment record;
  their titles, statements, statuses and ADR relations.
- Records without `prepared_at` and work orders without `execution_scope`:
  historical facts the owner decided to keep.
- Any artifact under `templates/`, any managed path, any release.

## Authorized decision envelope

The triggers chosen per architecture from the controlled vocabulary, read
from the deciding ADR; the wording of rationales and amendment records; the
order of the two rewrites; where the corpus test lives. The implementer may
not change a relation target the migration does not require, alter a
statement or status, map a steward decision to anything but `["test"]`, or
touch a product module.

## Constraints

- Every rewrite is applied by script from the checkout and the script
  retained in the evidence; no hand edit of a front-matter value.
- Validate with the released 0.16.0 evaluator after each rewrite; stop on
  the first error.
- Merge `origin/main` before the handoff so that no requirement added by a
  concurrent packet keeps a string method unnoticed.

## Expected change surface

Fifteen architecture front matters and amendment records; 271 requirement
front matters, two lines each; one script and one test deleted; one test
added; one note paragraph; one amendment record; this packet.

## Required verification

Execute `VER-AUT-003` in full; repository-required checks; the pull
request's lanes; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/artifact-authoring/evidence/WO-AUT-005/`: the per-code
validator counts before and after, the mapping report, the four steward
decisions with reasons, the list of migrated files, the rewrite scripts, the
`validate` and `doctor` readings.

## Stop and escalate conditions

An `E016` or `E014` on a migrated architecture; a constrained requirement
without a specifying specification; an architecture with two deciding ADRs or
none; a requirement whose front matter the script refuses; any product module
or managed path in the change set; a validator count other than `W014` and
`W015` that differs from the baseline.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution: the before-and-after counts, the fifteen architectures with
their triggers and ADRs, the four steward decisions, the deleted paths. The
completion decision is the engineering owner's.
