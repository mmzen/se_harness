+++
id = "WO-TCM-011"
type = "work_order"
title = "Turn the four authoring-advisory families blocking at approval"
status = "draft"
owners = ["engineering-owner"]
created = "2026-09-06"
updated = "2026-09-06"

[assurance]
commit_bound_verification = "required"
rationale = "The change edits the approval gate's evaluator, which every repository that adopts the release runs on every definition approval; a wrong read refuses valid drafts or admits the shape the four decisions rejected."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/",
  "templates/repository/standard/docs/engineering/",
  "templates/repository/standard/scripts/",
  "tests/",
  "docs/notes/",
  "docs/engineering/technical-communication/",
]

[delegation]
class = "execution"

[relations]
implements = ["REQ-TCM-017"]
specifications = ["SPEC-TCM-007"]
verification = ["VER-TCM-007"]
+++

# Work Order: Turn the four authoring-advisory families blocking at approval

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above.

Commit-bound verification is `required`.

This work order carries `[delegation] class = "execution"`. Approving it is
the act of delegating `DR-WO-START`, `DR-WO-COMPLETE` and `DR-VREC-PREPARE`
to the `delegated-executor` role, each act admitted only while the required
`validate` check is `success` for the exact candidate head, with the class
read from the base of the pull request. The verification decision on the
record, merge, release and publication stay human.

## Objective

Execute the regime the owner chose four times, last as `DEC-TCM-004`:
after one release of advisories, a definition draft that still draws an
authoring advisory is not approved (`REQ-TCM-017`, `TCM-RFB-001` to
`TCM-RFB-012`). Validation, approved artifacts, the budgets and the codes
do not change. The reading of 2026-09-06 is the input: of nine definitions
drafted under the 0.15.0 root, three were within budget and six were
approved with advisories on them, the two new specifications with more than
ten each.

## In scope

- The validator's `authoring_advisories(artifact)` in the candidate
  template, wrapping the requirement, intent, capability and specification
  functions and evaluating the artifact as a draft.
- `authoring_ready` in `se_harness/workflow_compliance.py`: the advisory
  check after the placeholder and `Open decisions` checks, for the four
  definition kinds only, with the listed failure message.
- The four definition checklists of `ARTIFACT_AUTHORING.md`: one sentence
  each stating that a draft drawing an advisory is not approved.
- `docs/notes/artifact-authoring.md` and `docs/notes/harnessctl-reference.md`
  where they describe the advisories or the approval gate; the
  diagnostic-code index if a code is added, which none is.
- `tests/`: the rows of `VER-TCM-007`; declared candidate-versus-root
  exceptions where a hash-locked root copy lags.
- This domain's index and the evidence packet under
  `docs/engineering/technical-communication/evidence/WO-TCM-011/`.

## Out of scope

Any budget, code or message of `SPEC-TCM-003` to `SPEC-TCM-006`; any change
to approved artifacts; a waiver mechanism; the quality-gates contract,
unless the implementation needs a new predicate id, which is a stop; the
release carrying this change.

## Authorized decision envelope

The exact refusal wording beyond the code, the message and the closing
sentence; test names and fixture layout; whether the checklist sentence
sits at the top or the bottom of each section.

## Constraints

- Execution starts only after `RLS-SEH-025` (0.16.0) is released and
  adopted as this repository's root, so the specification family has had
  its one release of advisories, as `DEC-TCM-004` requires. Approval before
  that date is approval of the design, not a start.
- The two contract copies stay byte-identical; the root managed copies are
  not edited.
- The word "governor" is not introduced into `docs/notes/`.
- The packet's own drafts, `REQ-TCM-017`, `SPEC-TCM-007`, `VER-TCM-007`
  and this work order, are within every budget at approval; if the gate
  built here would refuse them, the packet is wrong, not the gate.

## Expected change surface

The candidate validator, `se_harness/workflow_compliance.py`, the
authoring guide, two notes, tests, the domain index and the packet.

## Required verification

Execute `VER-TCM-007` in full; the full suite on Windows against the
recorded baseline and the Linux lane; the released-evaluator `validate`,
`doctor` and `preflight`; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/technical-communication/evidence/WO-TCM-011/`.

## Stop and escalate conditions

A need to change a budget or a code; a need for a new predicate id in the
quality-gates contract; any approved artifact refused by the new check in
a throwaway approval of the corpus; a hash-locked file in the change set.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
