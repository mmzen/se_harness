+++
id = "WO-TCM-008"
type = "work_order"
title = "Ship the reader-first capability shape and read derivation from the graph"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-09-04"
updated = "2026-09-04"

[assurance]
commit_bound_verification = "required"
rationale = "The change edits the managed capability template, the authoring guide, the validator's advisory type table shared with intents and requirements, and the Explorer's record and lineage panels; a wrong constant or projection reaches every repository that adopts the release."
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
implements = ["REQ-TCM-012", "REQ-TCM-013"]
specifications = ["SPEC-TCM-005"]
verification = ["VER-TCM-005"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-04T19:45:21Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable repository owner on 2026-09-04 with the instruction 'i apprive' (approve), after reviewing PR #342 (REQ-TCM-012, REQ-TCM-013, SPEC-TCM-005, VER-TCM-005, WO-TCM-008), carrying the owner's four decisions on the capability assessment of the same day. WO-TCM-008 carries the delegation class: this approval delegates DR-WO-START, DR-WO-COMPLETE and DR-VREC-PREPARE to the delegated-executor role under the required validate check, with the class read from the base of the pull request; the verification decision, merge, release and publication stay human. Execution stacks on WO-TCM-007."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-04T20:21:27Z"
decided_by = "delegated-executor"
reason = "Delegated DR-WO-START under [delegation] class 'execution': required check 'validate' success at 72a0c4c6d0e54c74939ca96777304a6cf655b8e1 (check-run 101162456699, source github-checks). Delegated DR-WO-START: execution branch wo/tcm-008-execution opened from main after WO-TCM-007 merged with VREC-TCM-007 verified; the intent advisories and constants it landed are the base this work order extends."
+++

# Work Order: Ship the reader-first capability shape and read derivation from the graph

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

Give the next capability a shape its reader understands on first reading
(`REQ-TCM-012`, `TCM-RFC-001` to `TCM-RFC-004`, `TCM-RFC-007`) and show
what derives from a capability from the graph instead of a list in its
body (`REQ-TCM-013`, `TCM-RFC-005`, `TCM-RFC-006`). Approved artifacts are
not rewritten.

This work order stacks on `WO-TCM-007`: the advisory type table that
`SPEC-TCM-004` introduces for intents gains its capability row here, and
the `plain_words` and outcome projections that `WO-TCM-007` adds to the
generator and the Explorer are extended, not duplicated. Execution starts
on a branch from `WO-TCM-007`'s merged result, or from its execution branch
if the owner asks for a stacked pull request.

## In scope

- `CAPABILITY.template.md` in the reader-first shape with the `ability`
  field; the capability section of `ARTIFACT_AUTHORING.md` rewritten for
  the shape, the field, the budgets and the two guidance sentences, with
  "lists its derived requirements" removed.
- The candidate validator: `ability` accepted and `E-AUT-002` on an empty
  or non-string value; `W-AUT-016` to `W-AUT-018` on drafts only; the
  capability row of the type table with the constants of `TCM-RFC-003`.
- The dashboard generator: `ability`, `plain_words` and
  `derived_requirements` on capability artifacts.
- The Explorer record panel (ability, plain words, `Derives` list) and the
  lineage second stage, with the template rebuilt from its sources.
- `docs/notes/diagnostic-codes.md` regenerated;
  `docs/notes/artifact-authoring.md` and `docs/notes/harnessctl-reference.md`
  where they describe the capability shape or the advisories.
- `tests/`: the rows of `VER-TCM-005`; declared candidate-versus-root
  exceptions where a hash-locked root copy lags.
- This domain's index and the evidence packet.

## Out of scope

Any edit to an approved capability's body; the intent and requirement
constants and rules; any change to the intent-to-capability relation or to
the mandatory capability layer; the hash-locked root copies; the release
carrying this change; making any advisory blocking.

## Authorized decision envelope

The exact advisory wording; the tokenizer used for word and sentence
counts and for the words `can` and `under`; the placement of the `Derives`
list within the rule; test names and fixture layout.

## Constraints

- Advisories stay on the maintenance plane and fire on capability drafts
  only; the intent and requirement rows of the type table are unchanged.
- The two contract copies stay byte-identical; the root managed copies are
  not edited.
- The word "governor" is not introduced into `docs/notes/`.
- The candidate template's authoring gate must still admit this packet's
  own drafts, which carry `Open decisions` for the current root gate.

## Expected change surface

One definition template, the authoring guide, the candidate validator, the
dashboard generator and the Explorer build with its rebuilt template, two
notes and the regenerated index, tests, the domain index and the packet.

## Required verification

Execute `VER-TCM-005` in full; the full suite on Windows against the
recorded baseline and the Linux lane; the released-evaluator `validate`,
`doctor` and `preflight`; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/technical-communication/evidence/WO-TCM-008/`.

## Stop and escalate conditions

Any need to rewrite an approved artifact; a change that alters the intent
or requirement constants; a type table that `WO-TCM-007` did not land in
the form `SPEC-TCM-004` describes; a hash-locked file in the change set.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
