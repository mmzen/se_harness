+++
id = "WO-DLC-003"
type = "work_order"
title = "Require a recorded decision chain for every definition status past draft"
status = "draft"
owners = ["engineering-owner"]
created = "2026-08-26"
updated = "2026-08-26"

[assurance]
commit_bound_verification = "required"
rationale = "The work closes a permission that 449 of this repository's 630 definitions currently rely on, and every consumer repository with a hand-authored status relies on the same permission. A wrong candidate converts 449 valid definitions into 449 governance errors. The frozen 449-identifier constant must be measured at the correct commit, and only a commit-bound record can establish which commit that was."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "templates/repository/standard/scripts/validate_engineering_artifacts.py",
  "templates/repository/standard/docs/engineering/templates/WORK_ORDER.template.md",
  "templates/repository/standard/docs/engineering/TRACEABILITY.md",
  "templates/repository/standard/docs/engineering/WORKFLOW.md",
  "se_harness/pre_contract_statuses.py",
  "se_harness/governance_migration.py",
  "se_harness/preflight.py",
  "tests/",
  "docs/notes/harnessctl-reference.md",
  "docs/notes/definition-lifecycle.md",
  "docs/engineering/definition-lifecycle/evidence/",
]

[relations]
implements = ["REQ-DLC-004", "REQ-DLC-005"]
specifications = ["SPEC-DLC-003"]
architecture = ["ARCH-DLC-001", "ADR-DLC-001", "ADR-DLC-002"]
verification = ["VER-DLC-001"]
+++

# Work Order: Require a recorded decision chain for every definition status past draft

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification, the assurance decision, integration, and release are separate
decisions by the roles that own them.

## Objective

Implement `SPEC-DLC-003` so that a definition carrying any status other than
`draft` requires an append-only `lifecycle_events` chain from `draft` to that
status, so that the absence of a chain is a governance error unless a declared
pre-contract exemption resolves, and so that every resolved exemption stays
visible as a maintenance diagnostic on every run.

This closes the permission — `events is None: continue` — that let 449 statuses
be hand-authored and that is the reason the other two defects in this domain grew
undetected behind a zero-error verdict.

This increment must land after `WO-DLC-001` and `WO-DLC-002`. Its frozen set
covers the same 165 `implemented` definitions those increments reason about, and
a set measured before they settle would be frozen around a moving target.

## In scope

- Replacement of `validate_lifecycle_events`'s `events is None` early exit with
  the obligation, for the nine definition families only.
- Chain requirement: first event `from = "draft"`, each event's `from` equal to
  the previous event's `to`, last event's `to` equal to the current status.
- `E022` in the governance plane for an unchained, undeclared definition, naming
  the artifact, its status, and both recovery routes.
- New pure resolver module mirroring `se_harness/legacy_release_evidence.py`: the
  frozen 449-identifier set with declarer name
  `pre-contract-definition-statuses`, declaration parsing bounded at 512 entries,
  the `draft -> approved` approval precondition, and one stable reason per failure
  mode.
- `W025` for every resolved exemption, on every run, with text stating only that
  the status predates the obligation and is declared — naming no actor and no
  date.
- Equivalent self-contained implementation inside the canonical validator script,
  agreeing with the package module on a shared committed vector fixture under
  `tests/fixtures/`.
- Committed generating measurement for the frozen set, the test comparing its
  output against the committed constant, and the recorded measurement commit.
- Declaration packet field for consumers, documented in `TRACEABILITY.md`, with
  the multiple-declaration path for populations above 512.
- Stale-declaration reporting for a named definition that has since gained a
  chain.
- Governance-migration scenario for the version pair this increment lands in.
- Tests and fixtures per `VER-DLC-001` scenarios 14 to 20.
- One non-authoritative note; reference updates; work-order-keyed evidence.

## Out of scope

- Writing, defaulting, inferring, or backfilling a `lifecycle_events` entry for
  any artifact. No chain is fabricated. The 7 `rejected` and 3 `superseded`
  chainless definitions are not touched, since inventing a decision for a
  rejected artifact would rewrite history.
- Any change to a definition's status, relations, or bytes.
- Work orders, verification records, and release records. The obligation applies
  to the nine definition families only.
- Changing how an existing chain is validated. The chain-shape, ordering, actor,
  and append-only rules are unchanged.
- The architecture-generation exemption, `E014`, `W014`, `E015`, and `W015`.
- The lifecycle graph, the recommendation table, and the realization derivation.
- Any date-based, Git-based, or artifact-supplied exemption input. `ADR-DLC-002`
  rejects all three.
- Editing root managed copies or `.engineering-harness.lock` of this repository.
- Approving or transitioning any definition or this work order.
- Building a release or upgrading the governor.

## Authorized decision envelope

The implementation agent may decide the module layout, function and dataclass
names, the stable reason strings, the declaration packet's table and field names,
the fixture organization, and the note structure. If `E022` or `W025` has been
taken by a concurrent change, it uses the next free code and reports that
`SPEC-DLC-003` needs amending.

It may not weaken the obligation, fabricate a chain, reopen the frozen set, raise
or remove the 512-entry bound, drop the approval precondition, suppress `W025`,
extend the scope beyond the nine definition families, change the enumerated
grandfathering mechanism `ADR-DLC-002` selects, or change any path outside scope.

## Constraints

- Use the exact external released evaluator, invoked from outside the checkout,
  for identity, integrity, graph, focus, and preflight results. Use the candidate
  for implementation and tests.
- The change belongs in `templates/repository/standard/`. The root managed script
  belongs to the released version and is not edited.
- Measure the frozen set once, at this increment's candidate commit, and record
  that commit in the evidence. A set measured at an earlier commit is a finding.
- Measure the candidate template script and the released evaluator separately,
  each against its own baseline.
- LF line endings.

## Expected change surface

The canonical validator template, one artifact template, two managed documents,
one new package module, two package modules for migration and preflight surfaces,
tests and fixtures including a 449-entry constant and its generating measurement,
one note, reference updates, evidence.

## Required verification

Execute `VER-DLC-001` scenarios 14 to 20 completely, plus the
repository-required checks. Full suite on Windows and Linux with figures labelled
per platform. Paired released-lineage measurement at the merge base and at the
candidate: zero errors at both ends, `W013`, `W014`, and `W015` identifier sets
exactly equal, and exactly the declared `W025` set added and nothing else. Review
preflight and a handoff check with the complete changed-path set.

## Evidence to record

Under `docs/engineering/definition-lifecycle/evidence/WO-DLC-003/`: exact
commands with evaluator identity and version; full base and candidate output
labelled per platform; complete diagnostic identifier sets rather than counts;
the generating measurement output for the 449-identifier set and its commit,
with proof that commit is at or after `WO-DLC-001` and `WO-DLC-002` landed; the
per-family obligation fixture results; the declaration failure corpus with each
stable reason including the 513-entry and two-declaration cases; proof that no
code path writes a `lifecycle_events` entry; consumer upgrade observations and the
migration scenario; the complete changed-path set; material deviations.

## Stop and escalate conditions

Stop if the frozen set cannot be measured at a commit at or after both prior
increments landed; if the measurement does not equal the definitions then
carrying a non-`draft` status with no chain; if the obligation cannot be confined
to the nine definition families; if any declaration failure mode is not
fail-closed; if closing the permission moves any error count other than by
converting declared cases to `W025`; if `E022` or `W025` cannot be reserved; or
if any path outside scope must change.

## Completion report format

Return the `harnessctl check . --artifact WO-DLC-003 --checkpoint handoff`
schema-2 block verbatim with the complete changed-path set asserted, and its
`result_sha256`.
