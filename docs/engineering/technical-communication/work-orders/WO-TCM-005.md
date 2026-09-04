+++
id = "WO-TCM-005"
type = "work_order"
title = "Ship the reader-first requirement shape and retire the Open decisions section"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-09-04"
updated = "2026-09-04"

[assurance]
commit_bound_verification = "required"
rationale = "The change edits the managed requirement template and every definition template, the authoring gate that every approval passes, the validator's advisory class and the Explorer's record panel; a wrong gate change would refuse or admit approvals across every repository that adopts the release."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/",
  "templates/repository/standard/docs/engineering/",
  "templates/repository/standard/scripts/",
  "repository_tools/explorer_design/",
  "tests/",
  "docs/notes/",
  "docs/engineering/decision-management/specifications/SPEC-DCM-001.md",
  "docs/engineering/technical-communication/",
]

[delegation]
class = "execution"

[relations]
implements = ["REQ-TCM-006", "REQ-TCM-008"]
specifications = ["SPEC-TCM-003"]
verification = ["VER-TCM-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-04T16:14:37Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable repository owner on 2026-09-04 with the instruction 'i approve the packet, the work orders can be start with execution delegation', after reviewing PR #335 (REQ-TCM-006..008, SPEC-TCM-003, VER-TCM-003, WO-TCM-005, WO-TCM-006). WO-TCM-005 and WO-TCM-006 carry the delegation class: this approval delegates DR-WO-START, DR-WO-COMPLETE and DR-VREC-PREPARE to the delegated-executor role under the required validate check, with the class read from the base of the pull request; the verification decision, merge, release and publication stay human."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-04T16:23:05Z"
decided_by = "delegated-executor"
reason = "Delegated DR-WO-START under [delegation] class 'execution': required check 'validate' success at 6762388dab7b4808fc1c3ec84b903966d3d63af7 (check-run 101094604662, source github-checks). Delegated DR-WO-START: execution branch wo/tcm-005-execution (PR #336) opened from main after PR #335 merged the approved packet."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-04T16:34:19Z"
decided_by = "delegated-executor"
reason = "Delegated DR-WO-COMPLETE under [delegation] class 'execution': required check 'validate' success at 93f589a93f09033eb6564938c37177dc3386122b (check-run 101097989654, source github-checks). Delegated DR-WO-COMPLETE: the reader-first requirement shape, the draft advisories, the Explorer plain-words line and the retirement of the Open decisions section are implemented in the candidate per SPEC-TCM-003 rules TCM-RFR-001 to TCM-RFR-006; evidence docs/engineering/technical-communication/evidence/WO-TCM-005/ with the retained Git-derived handoff result; Windows suite 1220 tests, zero failures, the one baseline error; released 0.14.0 validate PASS. Four disclosures are in the evidence packet."
+++

# Work Order: Ship the reader-first requirement shape and retire the Open decisions section

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

Give the next requirement a shape its reader understands on first reading
(`REQ-TCM-006`, `TCM-RFR-001` to `TCM-RFR-005`) and read a definition's
pending decisions from the decision graph instead of an `Open decisions`
section (`REQ-TCM-008`, `TCM-RFR-006`). Approved artifacts are not
rewritten.

## In scope

- `REQUIREMENT.template.md` in the reader-first shape; the `Open decisions`
  section removed from every definition template; the requirement section
  of `ARTIFACT_AUTHORING.md` rewritten for the shape, the named actor, the
  budgets and the glossary pointer.
- The candidate validator: `W-AUT-003` at 30 words; `W-AUT-005` to
  `W-AUT-010` on drafts only.
- `authoring_ready` in the candidate source: the section is no longer
  required; legacy sections keep their rule.
- The dashboard generator's `plain_words` projection and the Explorer
  record panel's rendering beneath the statement, with the template rebuilt
  from its sources.
- `SPEC-DCM-001`: one amendment record on rule 11.
- `docs/notes/diagnostic-codes.md` regenerated; `docs/notes/artifact-authoring.md`
  and `docs/notes/harnessctl-reference.md` where they describe the shape or
  the advisories.
- `tests/`: the rows of `VER-TCM-003` for `REQ-TCM-006` and `REQ-TCM-008`;
  declared candidate-versus-root exceptions where a hash-locked root copy
  lags.
- This domain's index and the evidence packet.

## Out of scope

Any edit to an approved requirement's body; the glossary seed and the
vocabulary report (`WO-TCM-006`); any change to a decision-artifact rule
other than rule 11's legacy reading; the hash-locked root copies; the
release carrying this change; making any advisory blocking.

## Authorized decision envelope

The exact advisory wording; the tokenizer used for word and sentence
counts; test names and fixture layout; the visual placement of
`plain_words` beneath the statement.

## Constraints

- Advisories stay on the maintenance plane and fire on drafts only.
- The two contract copies stay byte-identical; the root managed copies are
  not edited.
- The word "governor" is not introduced into `docs/notes/`.
- The candidate template's authoring gate must still admit this packet's
  own drafts, which carry `Open decisions` for the current root gate.

## Expected change surface

Definition templates, the authoring guide, the candidate validator, one
module of the candidate source, the dashboard generator and the Explorer
build with its rebuilt template, one specification amendment record, two
notes and the regenerated index, tests, the domain index and the packet.

## Required verification

Execute the `REQ-TCM-006` and `REQ-TCM-008` rows of `VER-TCM-003`; the
full suite on Windows against the recorded baseline and the Linux lane;
the released-evaluator `validate`, `doctor` and `preflight`; the handoff
check over the Git-derived change set.

## Evidence to record

`docs/engineering/technical-communication/evidence/WO-TCM-005/`.

## Stop and escalate conditions

Any need to rewrite an approved artifact; a change to the authoring gate
that refuses a currently approvable draft for a reason other than the
retired section; a hash-locked file in the change set; a rule of
`SPEC-DCM-001` other than rule 11 needing change.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
