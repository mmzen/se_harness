+++
id = "WO-DST-027"
type = "work_order"
title = "Issue #433, templates: the retired relation in the traceability policy and the completion decider in the work-order template"
status = "implemented"
owners = ["engineering-owner", "technical-owner", "quality-owner"]
created = "2026-09-10"
updated = "2026-09-10"

[assurance]
commit_bound_verification = "required"
rationale = "The change rewrites a rule of the managed traceability policy and the guidance of the managed work-order template that every consumer installs and every later work order is drafted from; the next release and this repository's own root adoption rely on its correctness."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "templates/repository/standard/docs/engineering/TRACEABILITY.md",
  "templates/repository/standard/docs/engineering/templates/WORK_ORDER.template.md",
  "tests/",
  "docs/notes/harness-uml-model.md",
  "docs/engineering/harness-distribution/README.md",
  "docs/engineering/harness-distribution/evidence/",
  "docs/engineering/harness-distribution/verification-records/",
  "docs/engineering/harness-distribution/requirements/REQ-DST-076.md",
  "docs/engineering/harness-distribution/requirements/REQ-DST-077.md",
  "docs/engineering/harness-distribution/specifications/SPEC-DST-028.md",
  "docs/engineering/harness-distribution/verification/VER-DST-028.md",
  "docs/engineering/harness-distribution/work-orders/WO-DST-027.md",
]

[delegation]
class = "execution"

[relations]
implements = ["REQ-DST-076", "REQ-DST-077"]
specifications = ["SPEC-DST-028"]
verification = ["VER-DST-028"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-10T10:18:43Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-09-10 by selecting the presented option 'Approve both packets (Recommended)', as a decision distinct from the approval of its definitions in the same transaction. This approval is the delegating act under DR-007 and DR-015: the work order carries [delegation] class = 'execution', so DR-WO-START, DR-WO-COMPLETE and DR-VREC-PREPARE may be applied by the delegated-executor role while the required validate check is success for the exact candidate head, read from the base of the pull request. It authorizes only the declared scope: the TRC-008 paragraph of the standard TRACEABILITY.md template, the guidance under the Completion report format heading of the standard work-order template, the tests, the UML note, the domain index, the evidence file and the handoff packet. It authorizes no change to any root managed byte, no rewrite of an existing work order, no verification decision, no release, no publication and no adoption; the merges remain the owner's decisions."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-10T12:21:47Z"
decided_by = "delegated-executor"
reason = "Delegated DR-WO-START under [delegation] class 'execution': required check 'validate' success at f00b93e04f6b340c07194fa6e51bfbfd7ebdcb9b (check-run 102867058651, source github-checks)."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-10T12:36:45Z"
decided_by = "delegated-executor"
reason = "Delegated DR-WO-COMPLETE under [delegation] class 'execution': required check 'validate' success at 8b68d8ab706128eb762f54e39f7dd88851fbeec7 (check-run 102871046134, source github-checks). Completion decided by the delegated-executor role on 2026-09-10 under the execution delegation class WO-DST-027 carries, delegated by the engineering owner in the approval of 2026-09-10 and read at the base of pull request #440, main at f36c8bf1. Rules DST-TPL-001 to DST-TPL-008 of SPEC-DST-028 are met and mapped to evidence in docs/engineering/harness-distribution/evidence/WO-DST-027-verification.md and evidence/WO-DST-027/WO-DST-027-handoff.md: TRC-008 of the standard TRACEABILITY.md says ARCH.constrains is retired and refused with E016, names the typed pair as the only form and keeps its installation sentence; the standard WORK_ORDER.template.md names who decides completion under Completion report format; the UML note follows; the parity test declares both changes against the 0.17.0 root; tests/test_managed_template_texts.py pins them with a drafted work order as scenario B. DST-TPL-009 is carried to the root adoption of the carrying release. The retained handoff check from origin/main completed, nine predicates passing, ten changed paths in scope. Released 0.17.0: validate 1,485 artifacts, 0 errors, 46 W013; doctor 99 PASS; preflight PASS. Local suite 1,132 tests, 7 added, at the Windows baseline; the hosted validate check at 8b68d8ab is success. Every root managed byte is identical to main. Disclosed: scenario B runs as a test through the suite's mutation-authority patch because both evaluators refuse a consumer-style create-artifact here; the UML note's third sentence gained 'otherwise'; the parity equality branch is first observed at the root adoption. Completion approves nothing: record preparation is this role's separate decision; verification and the merge remain the human owners."
+++

# Work Order: Issue #433, templates: the retired relation in the traceability policy and the completion decider in the work-order template

## Lifecycle

This work order carries `[delegation] class = "execution"`: approving it is
the act of delegating `DR-WO-START`, `DR-WO-COMPLETE` and `DR-VREC-PREPARE`
to the `delegated-executor` role, each unlocked only while the required
`validate` check is `success` for the exact candidate head (`REQ-ECP-011`,
`SPEC-ECP-006`). The class is read at the base of the pull request, so the
approved packet merges to `main` first and the execution follows on a second
branch. The approval below, the verification of the record it prepares, and
every merge stay human decisions. Commit-bound verification is `required`.

The two template changes ship with the release after next and are felt in
this repository only at the root adoption of that release; nothing here
changes a root managed byte.

## Objective

Execute rules `DST-TPL-001` to `DST-TPL-008` of `SPEC-DST-028`: `TRC-008` of
the managed traceability policy says `ARCH.constrains` is retired and refused
with `E016`, with `addresses` and `conforms_to` as the only form; the
"Completion report format" heading of the managed work-order template names
who decides completion; the UML note follows; the parity test declares both
changes and tests pin them.

## In scope

- `templates/repository/standard/docs/engineering/TRACEABILITY.md`: the
  `TRC-008` paragraph only (`DST-TPL-001` to `DST-TPL-003`).
- `templates/repository/standard/docs/engineering/templates/WORK_ORDER.template.md`:
  the guidance under "Completion report format" (`DST-TPL-004`).
- `docs/notes/harness-uml-model.md`: the sentence on the retired relation
  (`DST-TPL-005`).
- `tests/`: the declared exceptions in `test_artifact_catalog.py`
  (`DST-TPL-006`) and the pins of `DST-TPL-007`.
- The domain index, the evidence file and the handoff packet.

## Out of scope

- Any byte of this repository's root `docs/engineering/TRACEABILITY.md`,
  root `docs/engineering/templates/WORK_ORDER.template.md`,
  `.engineering-harness.lock` or other root managed file; they move at the
  root adoption of the carrying release (`DST-TPL-009`).
- The 79 existing work orders that carry the copied completion sentence;
  they are records of their time (`DST-TPL-008`).
- `ARCH-CIP-001` and `REQ-CIP-002`, repaired by `WO-CIP-008`.
- Any change to the validator, the installer, the lock schema, the skills or
  any other managed template.
- Building, releasing, publishing or adopting anything.

## Authorized decision envelope

The exact wording of the rewritten rule and of the template guidance within
`SPEC-DST-028`; the wording of the note sentence; where the new tests live
and how the parity test expresses the two exceptions. The implementer may not
change any other line of either template, touch a root managed byte, rewrite
an existing work order or widen the scope.

## Constraints

- Read `ENGINEERING_HARNESS.md` and run the review preflight with the
  released 0.17.0 evaluator from its venv outside the checkout before
  completion.
- The candidate suite must pass on the hosted Linux lane; the local Windows
  suite is a control whose skips are labelled.
- The template diff is one paragraph in each file; the parity test still
  reaches equality once a root carries both changes.
- Keep the diff free of unrelated changes, and list every test file touched
  in the completion report.

## Expected change surface

Five lines in `TRACEABILITY.md`; four lines in the work-order template; two
lines in the note; two declared exceptions and about six assertions in the
tests; this domain's index, evidence file and handoff packet.

## Required verification

`VER-DST-028` in full: the template tests, the note test, the parity test
under the 0.17.0 root, the three scenarios, the two inspections, with outputs
retained.

## Evidence to record

`docs/engineering/harness-distribution/evidence/WO-DST-027-verification.md`:
the rule before and after, the template guidance, the note before and after,
the parity branch taken, the scenario outputs, the hosted lane's test report,
the local control reading, the list of test files changed and the review
preflight result; the handoff packet under `evidence/WO-DST-027/`.

## Stop and escalate conditions

- The parity test cannot express the two changes as declared exceptions
  without touching a root copy.
- Any line of either template outside the two paragraphs would need to
  change.
- The scope check reports a path outside `[execution_scope]`, or a root
  managed byte is in the change set.

## Completion report format

The evidence file, the changed-path ledger and the handoff `check`
restitution: the rule and the guidance before and after, the note sentence,
the parity branch, the three scenario outcomes, the hosted lane result and
the local control reading each labelled; state that every root managed byte
is identical to `main`; name the adoption obligation `DST-TPL-009` carried
forward to the next root-adoption work order. The completion decision is the
`delegated-executor`'s under the class this work order carries, while the
required `validate` check is `success` for the head; the owner refuses it by
rejecting the pull request.
