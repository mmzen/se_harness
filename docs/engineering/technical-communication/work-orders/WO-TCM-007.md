+++
id = "WO-TCM-007"
type = "work_order"
title = "Ship the reader-first intent shape, the success-measure rule and the Explorer's outcome line"
status = "draft"
owners = ["engineering-owner"]
created = "2026-09-04"
updated = "2026-09-04"

[assurance]
commit_bound_verification = "required"
rationale = "The change edits the managed intent template, adds a front-matter field the validator must accept on every repository that adopts the release, extends the validator's advisory class and changes the Explorer's record panel, lineage board and a G0 condition; a wrong validator change would refuse valid intents or stay silent across every adopting repository."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/",
  "templates/repository/standard/docs/engineering/",
  "templates/repository/standard/scripts/",
  "repository_tools/explorer_design/",
  "tests/",
  "docs/notes/",
  "docs/engineering/technical-communication/",
]

[delegation]
class = "execution"

[relations]
implements = ["REQ-TCM-009", "REQ-TCM-010", "REQ-TCM-011"]
specifications = ["SPEC-TCM-004"]
verification = ["VER-TCM-004"]
+++

# Work Order: Ship the reader-first intent shape, the success-measure rule and the Explorer's outcome line

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

Give the next intent a shape its reader understands on first reading and an
outcome sentence the Explorer can show (`REQ-TCM-009`, `TCM-RFI-001` to
`TCM-RFI-003`, `TCM-RFI-005`, `TCM-RFI-007`); tell a success measure from
an acceptance check on the draft (`REQ-TCM-010`, `TCM-RFI-004`); render the
outcome and derive the G0 intent-quality condition from it (`REQ-TCM-011`,
`TCM-RFI-006`). Approved intents are not rewritten.

## In scope

- `INTENT.template.md` in the reader-first shape with the `outcome` field
  and its comment; the intent section of `ARTIFACT_AUTHORING.md` rewritten
  for the shape, the field, the budgets, the success-measure rule and the
  two sentences on when a new intent is warranted.
- The candidate validator: `outcome` accepted on intents and `E-AUT-002`
  when malformed; `W-AUT-011` to `W-AUT-015` on intent drafts only; the
  shared codes `W-AUT-005`, `W-AUT-007`, `W-AUT-008` and `W-AUT-009` raised
  on intent drafts with the intent constants, the requirement constants
  unchanged.
- The dashboard generator's `outcome` and `plain_words` projection on
  intents; the record panel and lineage board rendering; the derived
  `intent_quality` condition; the Explorer template rebuilt from its
  sources.
- `docs/notes/diagnostic-codes.md` regenerated; `docs/notes/artifact-authoring.md`,
  `docs/notes/harnessctl-reference.md` and `docs/notes/harness-operational-phasing.md`
  where they describe the intent shape, the advisories or the G0 condition.
- `tests/`: the rows of `VER-TCM-004`; the corpus negative control over the
  33 intents; declared candidate-versus-root exceptions where a hash-locked
  root copy lags.
- This domain's index and the evidence packet.

## Out of scope

Any edit to an approved intent; any change to the requirement advisories or
constants of `SPEC-TCM-003`; the capability template, which the assessment
names as the next pass; the hash-locked root copies; the release carrying
this change; making any advisory blocking; a gate result derived from
`intent_quality`.

## Authorized decision envelope

The exact advisory wording; the path and line-range patterns within the
two shapes `TCM-RFI-003` names; whether the intent and requirement budgets
share one helper with a constant table or two helpers; test names and
fixture layout; the visual placement of the outcome beyond "beneath the
title" and "before the lifecycle events".

## Constraints

- Advisories stay on the maintenance plane and fire on intent drafts only.
- The two contract copies stay byte-identical; the root managed copies are
  not edited.
- The word "governor" is not introduced into `docs/notes/`.
- The 33 approved intents raise no advisory and render as before; the
  bundle for this repository is generated to prove it.
- The Explorer template is rebuilt from `repository_tools/explorer_design/`
  sources, never edited in place.

## Expected change surface

The intent template, the authoring guide, the candidate validator, the
dashboard generator and the Explorer build with its rebuilt template, three
notes and the regenerated index, tests, the domain index and the packet.

## Required verification

Execute every row of `VER-TCM-004`; the full suite on Windows against the
recorded baseline and the Linux lane; the released-evaluator `validate`,
`doctor` and `preflight`; the handoff check over the Git-derived change
set.

## Evidence to record

`docs/engineering/technical-communication/evidence/WO-TCM-007/`.

## Stop and escalate conditions

Any need to rewrite an approved intent; an advisory raised on any approved
artifact or on any type other than intent; a hash-locked file in the
change set; a validator change that refuses an intent the root evaluator
accepts today; a need to change a rule of `SPEC-TCM-003`.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
