+++
id = "WO-DST-027"
type = "work_order"
title = "Issue #433, templates: the retired relation in the traceability policy and the completion decider in the work-order template"
status = "draft"
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
