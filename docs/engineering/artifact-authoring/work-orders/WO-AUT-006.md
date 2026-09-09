+++
id = "WO-AUT-006"
type = "work_order"
title = "Close the compatibility windows: W014, W015, the W-ECP-002 grace and the WEX-ECP-030 v1 hint"
status = "implemented"
owners = ["engineering-owner", "technical-owner", "quality-owner"]
created = "2026-09-09"
updated = "2026-09-09"

[assurance]
commit_bound_verification = "required"
rationale = "The change alters the validator, the preflight and the evidence predicate that every harnessctl command and every managed lane reads, and ships in the wheel; a consumer whose corpus still holds a legacy shape meets a refusal where it met a warning, so the exact candidate behaviour must be bound."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/codes.py",
  "se_harness/engine/validation_architecture.py",
  "se_harness/engine/validation_decisions.py",
  "se_harness/engine/dashboard_snapshot.py",
  "se_harness/preflight.py",
  "se_harness/workflow_predicates.py",
  "se_harness/workflow_contract.py",
  "se_harness/engine/validation_lifecycle.py",
  "tests/",
  "docs/notes/diagnostic-codes.md",
  "docs/notes/harnessctl-reference.md",
  "docs/notes/artifact-authoring.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-002.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-005.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-017.md",
  "docs/engineering/workflow-execution/specifications/SPEC-WEX-002.md",
  "docs/engineering/artifact-authoring/README.md",
  "docs/engineering/artifact-authoring/evidence/",
  "docs/engineering/artifact-authoring/verification-records/",
  "docs/engineering/artifact-authoring/requirements/REQ-AUT-009.md",
  "docs/engineering/artifact-authoring/specifications/",
  "docs/engineering/artifact-authoring/verification/VER-AUT-004.md",
  "docs/engineering/artifact-authoring/work-orders/WO-AUT-006.md",
]

[delegation]
class = "execution"

[relations]
implements = ["REQ-AUT-009"]
specifications = ["SPEC-AUT-004"]
verification = ["VER-AUT-004"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-09T17:21:18Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-09-09 by selecting the presented option 'Approve all four (Recommended)' on pull request #423, as a decision distinct from the approval of its definitions in the same transaction. This approval is the delegating act under DR-007 and DR-015: the work order carries [delegation] class = 'execution', so DR-WO-START, DR-WO-COMPLETE and DR-VREC-PREPARE may be applied by the delegated-executor role while the required validate check is success for the exact candidate head, read from the base of the pull request. It authorizes only the declared scope: the seven modules named in SPEC-AUT-004, tests/, the three notes and the regenerated index, the amendment records on SPEC-ECP-002, SPEC-ECP-005, SPEC-ECP-017 and SPEC-WEX-002, the domain index and the evidence packet. It authorizes no change to a managed template or any root managed byte, no change to a corpus artifact, no verification decision, no release and no publication; the merges remain the owner's decisions. In the same prompt the owner selected 'Keep the template out of scope (Recommended)', so the TRC-008 sentence of the managed TRACEABILITY.md template is owed to the next managed-template work order."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-09T17:37:24Z"
decided_by = "delegated-executor"
reason = "Delegated DR-WO-START under [delegation] class 'execution': required check 'validate' success at b11ea53709814e8e3a1411d3f22a3295b2e7d841 (check-run 102575250379, source github-checks). Start decided by the delegated-executor role on 2026-09-09 under the execution delegation class WO-AUT-006 carries, delegated by the engineering owner in the approval of 2026-09-09 and read at the base of this branch: main at b11ea53709814e8e3a1411d3f22a3295b2e7d841, the merge of the packet, where the required validate check is success. Branch wo/aut-006-close-the-windows off main at b11ea537. This decision authorizes only the declared execution scope: the seven modules of SPEC-AUT-004, tests/, the three notes and the regenerated index, the amendment records on SPEC-ECP-002, SPEC-ECP-005, SPEC-ECP-017 and SPEC-WEX-002, the four artifacts of the packet, the domain index and the evidence packet. It authorizes no change to a managed template or any root managed byte, no change to a corpus artifact, no new diagnostic code, no release, publication or adoption. Completion and record preparation are separate decisions of this role under the same gate; verification and every merge remain the accountable human owners."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-09T18:23:05Z"
decided_by = "delegated-executor"
reason = "Delegated DR-WO-COMPLETE under [delegation] class 'execution': required check 'validate' success at d5ee428436661401179df07993d1a5918da1f476 (check-run 102588037814, source github-checks). Completion decided by the delegated-executor role on 2026-09-09 under the execution delegation class WO-AUT-006 carries, read at the base of pull request #431. Rules AUT-WIN-001 to AUT-WIN-018 of SPEC-AUT-004 are met and mapped to evidence in docs/engineering/artifact-authoring/evidence/WO-AUT-006/: constrains is an E016 issue naming it retired, an architecture without a decision assessment reads E014, the preflight emits no W019, a header-less evidence packet is not assessable naming harnessctl evidence, a v1 quality-gates contract meets the loader's own error, W014, W015, W019 and W-ECP-002 left the registry and the index, the two permanent branches carry a comment and the note their counts, and four specifications are amended by record. The handoff check from main's tip completed, nine predicates passing, 27 changed paths inside the scope the owner amended on 2026-09-09 to admit validation_lifecycle.py, result 0edcd4c4 at its fixed point. Released 0.17.0 and the candidate read the same on this tree: 1,450 artifacts, 0 errors, 46 W013, 0 advisories; doctor and the review preflight PASS. Suite 1,119 to 1,126 tests at the Windows baseline; the hosted suite passed. Scenarios on a scratch worktree reproduce E016, E014 without W019, the loader's own error, and the traceability test failing when the window is restored; the header-less packet scenario is repeated at the bound commit. Lanes: five of five success at the packet head d5ee4284; at bb2e73a4 the managed lane named validation_lifecycle.py outside the scope before the amendment. No corpus artifact, managed template or root managed byte changed; the TRC-008 template sentence is owed to the next managed-template work order. Completion approves nothing; preparation, verification and the merge are separate decisions."
+++

# Work Order: Close the compatibility windows: W014, W015, the W-ECP-002 grace and the WEX-ECP-030 v1 hint

## Lifecycle

This work order carries `[delegation] class = "execution"`: approving it is
the act of delegating `DR-WO-START`, `DR-WO-COMPLETE` and `DR-VREC-PREPARE`
to the `delegated-executor` role, each unlocked only while the required
`validate` check is `success` for the exact candidate head (`REQ-ECP-011`,
`SPEC-ECP-006`). The class is read at the base of the pull request, so the
approved packet merges to `main` first and the execution follows on a second
branch. The approval below, the verification of the record it prepares, and
every merge stay human decisions. Commit-bound verification is `required`.

It is the work order `SPEC-AUT-003` `AUT-MIG-012` named as following
`WO-AUT-005`, under issue #381 owner decision 3 of 2026-09-07: migrate the
corpus, then close the windows.

## Objective

Execute rules `AUT-WIN-001` to `AUT-WIN-018` of `SPEC-AUT-004`: `constrains`
is refused, an unassessed completed architecture is refused, a header-less
packet is not assessable, a v1 quality-gates contract meets the loader's own
error; `W014`, `W015`, `W019` and `W-ECP-002` leave the package and the
index; the `prepared_at` and `execution_scope` branches are written down as
permanent; four specifications say so by record.

## In scope

- `validation_architecture.py`: the retired relation as an issue, the
  legacy states and `legacy_targets` gone, the relation-type entry gone
  (`AUT-WIN-001`, `AUT-WIN-002`).
- `validation_decisions.py`: `missing` for every architecture without the
  table, the `W014` branch and the legacy `E015` message gone
  (`AUT-WIN-003`, `AUT-WIN-004`).
- `preflight.py`: relevance and applicability from the `typed` state, `W019`
  gone (`AUT-WIN-005`).
- `dashboard_snapshot.py`: the legacy assessment states and `constrains` gone
  (`AUT-WIN-006`).
- `workflow_predicates.py`: the header-only evidence predicate
  (`AUT-WIN-007`, `AUT-WIN-008`); `workflow_contract.py`: the loader without
  the v1 hint (`AUT-WIN-009`, `AUT-WIN-010`); `codes.py`: four codes gone
  (`AUT-WIN-011`).
- The two permanent branches: a comment at each and the paragraph in
  `docs/notes/artifact-authoring.md` (`AUT-WIN-012`).
- Amendment records on `SPEC-ECP-002`, `SPEC-ECP-005`, `SPEC-ECP-017` and
  `SPEC-WEX-002` (`AUT-WIN-013`); the reference note and the regenerated
  index (`AUT-WIN-014`).
- `tests/`: the pins of `AUT-WIN-015`, and every test that asserts one of
  the four codes or a legacy state, measured on `main` at `4ea947be` in
  `test_adr_applicability.py`, `test_architecture_traceability.py`,
  `test_validation_taxonomy.py` and `test_workflow_compliance.py`.
- The domain index and the evidence packet.

## Out of scope

- Every artifact of the corpus: the closing needs no artifact to change
  (`REQ-AUT-008`).
- The `prepared_at` and `execution_scope` branches themselves: they stay.
- `WEX-ECP-030` for transition-binding faults, `E014`, `E015`, `E016` and
  every other code.
- The managed templates and every root managed byte; the `TRC-008`
  sentence of the standard `TRACEABILITY.md` is owed to the next
  managed-template work order.
- The two never-collected `REQ-AUT-007` tests of issue #415.

## Authorized decision envelope

The exact wording of the `E016` and `E014` messages and of the
`not_assessable` text; the placement of the test pins; the wording of the
amendment records, the branch comments and the note paragraph. The
implementer may not add a new code, keep a retired code under another name,
touch a corpus artifact or a template, or widen the scope.

## Constraints

- Read `ENGINEERING_HARNESS.md` and run the review preflight with the
  released 0.16.0 evaluator from its venv outside the checkout before
  completion.
- The candidate suite must pass on the hosted Linux lane; the local Windows
  suite is a control whose skips are labelled.
- The amendment records change prose only; no rule identifier, statement or
  relation moves.
- Keep the diff free of unrelated changes, and list every test file touched
  in the completion report.

## Expected change surface

About sixty lines removed and twenty added across the seven modules; four
codes removed; about a dozen assertions changed or added across four test
modules plus the new pins; two note edits and one regenerated page; four
amendment records; this domain's index and evidence.

## Required verification

`VER-AUT-004` in full: the fixture tests, the five scratch scenarios at the
bound commit, the baseline-versus-candidate count comparison, the two
inspections, with outputs retained.

## Evidence to record

`docs/engineering/artifact-authoring/evidence/WO-AUT-006/`: the baseline and
candidate `validate` readings count by count, the scenario outputs, the code
inventory before and after, the two measured counts, the suite readings
labelled hosted and local, the list of test files changed, the review
preflight result and the handoff check result.

## Stop and escalate conditions

- Any count of the candidate's `validate` on this tree differs from the
  baseline, or any error appears.
- A consumer-facing behaviour other than the four refusals changes.
- An amendment would need more than prose.
- The scope check reports a path outside `[execution_scope]`, or a template
  or root managed byte is in the change set.

## Completion report format

The evidence packet, the changed-path ledger and the handoff `check`
restitution: the four refusals each named with its test and its scenario,
the count comparison, the two permanent branches with their counts, the
list of test files touched, and the `TRC-008` obligation carried to the next
managed-template work order. Completion is the delegated executor's decision
under the class above; verification and the merge are the accountable human
owners'.

## Scope amendment, 2026-09-09

`se_harness/engine/validation_lifecycle.py` joins `[execution_scope]`. It
holds the `prepared_at` branch that `SPEC-AUT-004` `AUT-WIN-012` requires
to carry a comment naming it permanent; the scope as approved listed the
`execution_scope` branch's module and not this one, and the managed lane's
scope check named the path at the implementation head `bb2e73a4`
(`WEX201`). The engineering owner widened the scope by this one path under
`DR-REMEDIATION-SCOPE` on 2026-09-09 by selecting the presented option
"Amend the scope: add the module (Recommended)". The change to that module
is the three-line comment and nothing else; nothing else is widened, and
the retained evidence is re-bound to the snapshot this amendment moves.
