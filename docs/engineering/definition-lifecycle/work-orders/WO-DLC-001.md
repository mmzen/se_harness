+++
id = "WO-DLC-001"
type = "work_order"
title = "Replace the architecture-generation status proxy with a declared exemption"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-08-26"
updated = "2026-08-26"

[assurance]
commit_bound_verification = "required"
rationale = "The work removes a status input from a managed validator script that every consumer repository pins, and replaces it with a declaration surface inside work orders. A wrong candidate converts 14 maintenance warnings into 14 governance errors and stops the repository validating. Future engineering, assurance, and release decisions depend on exact candidate behaviour."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "templates/repository/standard/scripts/validate_engineering_artifacts.py",
  "templates/repository/standard/docs/engineering/templates/ARCHITECTURE.template.md",
  "templates/repository/standard/docs/engineering/templates/WORK_ORDER.template.md",
  "templates/repository/standard/docs/engineering/TRACEABILITY.md",
  "se_harness/definition_generation.py",
  "se_harness/governance_migration.py",
  "se_harness/preflight.py",
  "tests/",
  "docs/notes/harnessctl-reference.md",
  "docs/notes/definition-lifecycle.md",
  "docs/engineering/definition-lifecycle/evidence/",
]

[relations]
implements = ["REQ-DLC-001", "REQ-DLC-005"]
specifications = ["SPEC-DLC-001"]
architecture = ["ARCH-DLC-001", "ADR-DLC-001", "ADR-DLC-002"]
verification = ["VER-DLC-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-26T09:36:25Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-26T09:40:33Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-26T14:52:19Z"
decided_by = "engineering-owner"
reason = "DR-WO-COMPLETE exercised by the engineering-owner. The handoff checkpoint passed through the released 0.6.0 evaluator with the complete twenty-path changed set asserted; result_sha256 d4b38b3e6e0b6bcf2bdf792d38c18c7374dc95ebb6fc13ff4396e5437aa3de33 over formal snapshot 0b2a5214010d0600cbe71aed1812fef1fb94f9f9f32866d1951d4f1f5f64e398. Implementation commit 5e25388. Retained evidence is in docs/engineering/definition-lifecycle/evidence/WO-DLC-001/. The owner accepts seven disclosed deviations as residuals rather than blocking this transition. Two are settled by separate decisions taken at the same time. The false claim in SPEC-DLC-001, VER-DLC-001 and WO-DLC-001 that W015 and E015 are already status-independent, and VER-DLC-001 scenario 16's draft-target contradiction with DLC-GEN-005, are recorded as residuals for correction under a later dedicated work order; neither artifact is in this work order's scope. The undelivered governance-migration scenario of line 86 is accepted as an authorized stop under this work order's own out-of-scope stop condition, because the migration contract byte-pins the module and its capability vocabulary is a closed set of eight names the predecessor already holds in full. Commit-bound verification remains required and has not been decided. This transition is not that decision."
+++

# Work Order: Replace the architecture-generation status proxy with a declared exemption

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification, the assurance decision, integration, and release are separate
decisions by the roles that own them.

## Objective

Implement `SPEC-DLC-001` so that an architecture's exemption from the required
decision assessment is resolved from a frozen closed self-hosting set and from
explicit declarations in approved work orders, and never from the architecture's
lifecycle status.

This is the first of three increments and must land before `WO-DLC-002` and
`WO-DLC-003`. It is the only one of the three that is strictly a correction, and
both of the others touch the `implemented` population it protects.

## In scope

- New pure resolver module mirroring `se_harness/legacy_release_evidence.py`:
  the frozen 14-identifier set with declarer name
  `self-hosting-compatibility-set`, declaration parsing bounded at 512 entries,
  the `draft -> approved` approval precondition, and one stable reason per
  failure mode.
- Removal of `LEGACY_ARCHITECTURE_STATUSES` from the canonical validator template
  and replacement of `decision_assessment_state`'s `legacy` computation with the
  resolver. No code path may read an architecture's status in that assessment.
- Declaration packet field in the work-order template and the shape documented in
  `TRACEABILITY.md`.
- Equivalent self-contained implementation inside the canonical validator script,
  agreeing with the package module on a shared committed vector fixture under
  `tests/fixtures/`.
- `W014` message text stating that generation is declared, naming the source, and
  mentioning no lifecycle status.
- Diagnostics for every unresolved and stale declaration.
- Governance-migration scenario for the version pair this increment lands in.
- Committed generating measurement for the frozen set, plus the test that
  compares its output against the committed constant.
- Tests and fixtures per `VER-DLC-001` scenarios 1 to 5, 16, 17, 18, and 19.
- One non-authoritative note; reference updates; work-order-keyed evidence.

## Out of scope

- Any change to a definition's status, `lifecycle_events`, relations, or bytes.
  In particular, none of the 28 `implemented` architectures is edited.
- `E015` and the missing-deciding-ADR rule, and `W015` and the deprecated
  `constrains` finding. Both are unchanged and both are already
  status-independent.
- The definition lifecycle graph, `WORKFLOW.json`, `WORKFLOW.md`,
  `DECISION_RIGHTS.md`, and `QUALITY_GATES.*`. Those belong to `WO-DLC-002`.
- The `lifecycle_events` obligation, `E022`, and `W025`. Those belong to
  `WO-DLC-003`.
- The realization derivation, `I-DLC-001`, and `W-DLC-001`. Those belong to
  `WO-DLC-002`.
- Editing root managed copies or `.engineering-harness.lock` of this repository.
- Approving or transitioning any definition or this work order.
- Building a release or upgrading the governor.
- Adding any date-based, Git-based, or artifact-supplied exemption input.

## Authorized decision envelope

The implementation agent may decide the module layout, function and dataclass
names, the exact stable reason strings, the declaration packet's table and field
names, the fixture organization, and the note structure.

It may not change the frozen set's membership or closure, the 512-entry bound,
the approval precondition, the fail-closed behaviour, the removal of the status
input, the rule that exemption never suppresses `W014`, or any path outside
scope.

## Constraints

- Use the exact external released evaluator, invoked from outside the checkout,
  for identity, integrity, graph, focus, and preflight results. Use the candidate
  for implementation and tests.
- The change belongs in `templates/repository/standard/`. The root managed script
  belongs to the released version recorded in `.engineering-harness.toml` and is
  not edited.
- Measure the candidate template script and the released evaluator separately,
  each against its own baseline. A governor-versus-candidate warning gap is
  expected and is not skew.
- LF line endings.

## Expected change surface

One new package module, the canonical validator template, two artifact templates,
one managed traceability document, two package modules for migration and
preflight surfaces, tests and fixtures, one note, reference updates, evidence.

## Required verification

Execute `VER-DLC-001` scenarios 1 to 5, 16, 17, 18, and 19 completely, plus the
repository-required checks. Full suite on Windows and Linux with figures labelled
per platform. Paired released-lineage measurement at the merge base and at the
candidate, comparing the `W013`, `W014`, and `W015` identifier sets for exact set
equality rather than count. Review preflight and a handoff check with the
complete changed-path set.

## Evidence to record

Under `docs/engineering/definition-lifecycle/evidence/WO-DLC-001/`: exact
commands with evaluator identity and version; full base and candidate output
labelled per platform; complete diagnostic identifier sets rather than counts;
the ablation matrix for all 14 frozen identifiers; the generating measurement
output and its commit; the declaration failure corpus with each stable reason;
consumer upgrade observations and the migration scenario; the complete
changed-path set; material deviations.

## Stop and escalate conditions

Stop if the 14-identifier measurement at the merge base does not equal the
`W014` identifier set; if the exemption cannot be resolved without reading a
status, a date, a Git reference, or an environment value; if the declaration
cannot be bounded and made fail-closed within the `SPEC-LRE-001` shape; if the
paired measurement moves any diagnostic identifier set; if the `W014` count falls;
or if any path outside scope must change.

## Completion report format

Return the `harnessctl check . --artifact WO-DLC-001 --checkpoint handoff`
schema-2 block verbatim with the complete changed-path set asserted, and its
`result_sha256`.
