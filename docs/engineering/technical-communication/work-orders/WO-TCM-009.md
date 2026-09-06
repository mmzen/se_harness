+++
id = "WO-TCM-009"
type = "work_order"
title = "Ship the reader-first specification shape, one rule identity, mechanical coverage and the deviation anchor"
status = "draft"
owners = ["engineering-owner"]
created = "2026-09-06"
updated = "2026-09-06"

[assurance]
commit_bound_verification = "required"
rationale = "The change edits the managed specification template, the authoring guide, the validator's advisory type table shared with three other types, a new decision-management error, the dashboard generator and the Explorer's record panel; a wrong constant, a wrong rule parser or a wrong anchor reaches every repository that adopts the release and every deviation raised after it."
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
  "docs/engineering/decision-management/specifications/SPEC-DCM-001.md",
]

[delegation]
class = "execution"

[relations]
implements = ["REQ-TCM-014", "REQ-TCM-015", "REQ-TCM-016"]
specifications = ["SPEC-TCM-006"]
verification = ["VER-TCM-006"]
+++

# Work Order: Ship the reader-first specification shape, one rule identity, mechanical coverage and the deviation anchor

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

Four decision artifacts, `DEC-TCM-001` to `DEC-TCM-004`, block the three
requirements this work order implements until the product owner disposes
them; this is the first use of the decision artifact in this repository.

## Objective

Give the next specification a shape whose rules a test can cite, a work
order can execute and a deviation can name (`REQ-TCM-014`, `TCM-RFS-001`
to `TCM-RFS-014`, `TCM-RFS-023`); make the promise that a requirement is
covered by named rules mechanical and visible on both sides
(`REQ-TCM-015`, `TCM-RFS-010`, `TCM-RFS-015` to `TCM-RFS-019`); and give
the deviation reference a rule to point at (`REQ-TCM-016`, `TCM-RFS-020`
to `TCM-RFS-022`). Approved artifacts are not rewritten.

This work order extends the advisory type table `WO-TCM-007` introduced
and `WO-TCM-008` extended: the table gains its specification row, and the
`plain_words` projection that serves requirements, intents and
capabilities serves specifications. It starts on a branch from `main`
after the 0.15.0 adoption, so the packet's own drafts are already read by
the reader-first gate.

## In scope

- `SPECIFICATION.template.md` in the reader-first shape with the `contract`
  field; the specification section of `ARTIFACT_AUTHORING.md` rewritten
  for the shape, the rule identifier, the coverage table and the nine
  optional sections, with "Number rules" removed.
- The candidate validator: `contract` accepted and `E-AUT-002` on an empty
  or non-string value; the rule parser of `TCM-RFS-006`; `W-AUT-019` to
  `W-AUT-023` on drafts only; the specification row of the type table with
  the constants of `TCM-RFS-012` and no `W-AUT-008`; `E-DCM-005` on
  deviations.
- The dashboard generator: `contract`, `plain_words`, `rules` and
  `coverage` on specifications; `covered_by` on requirements.
- The Explorer record panel (contract, plain words, anchored rules,
  coverage table; `covered_by` links on a requirement; the deviation
  reference as a link), with the template rebuilt from its sources.
- `SPEC-DCM-001` rule 3 amended by record for the identifier example and
  the `E-DCM-005` check.
- `docs/notes/diagnostic-codes.md` regenerated;
  `docs/notes/artifact-authoring.md` and `docs/notes/harnessctl-reference.md`
  where they describe the specification shape, the advisories or the
  deviation reference; `GLOSSARY.md` if a term of `SPEC-TCM-006` is new to
  it.
- `tests/`: the rows of `VER-TCM-006`; declared candidate-versus-root
  exceptions where a hash-locked root copy lags.
- This domain's index and the evidence packet.

## Out of scope

Any edit to an approved specification's body; the requirement, intent and
capability constants and rules; the hash-locked root copies; the release
carrying this change; making any advisory blocking; any behavioural
diagram or `Model` section, which the owner set aside on 2026-09-06.

## Authorized decision envelope

The exact advisory and error wording; the tokenizer used for word,
sentence and keyword counts; the rule parser's tolerance for an identifier
followed by a parenthesised short name, as `SPEC-TCM-005` writes them; the
placement of the coverage table and the `covered_by` list within their
rules; test names and fixture layout.

## Constraints

- Advisories stay on the maintenance plane and fire on specification
  drafts only; the other three rows of the type table are unchanged.
- `E-DCM-005` is an error from the start: no deviation exists in any
  repository this candidate has shipped to.
- The two contract copies stay byte-identical; the root managed copies are
  not edited.
- The word "governor" is not introduced into `docs/notes/`.
- `SPEC-TCM-006` itself must draw no advisory of its own rules once
  approved, and its coverage table must be complete under `TCM-RFS-010`.

## Expected change surface

One definition template, the authoring guide, the candidate validator, the
dashboard generator and the Explorer build with its rebuilt template, one
decision-management specification amended by record, two or three notes
and the regenerated index, the glossary if needed, tests, the domain index
and the packet.

## Required verification

Execute `VER-TCM-006` in full; the full suite on Windows against the
recorded baseline and the Linux lane; the released-evaluator `validate`,
`doctor` and `preflight`; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/technical-communication/evidence/WO-TCM-009/`.

## Stop and escalate conditions

Any need to rewrite an approved artifact; a change that alters another
type's constants; a rule parser that reads fewer than 23 rules from
`SPEC-TCM-006` or any rule from an approved file's prose; a hash-locked
file in the change set; an `E-DCM-005` that fires on any artifact of this
repository at the candidate commit.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
