+++
id = "WO-TCM-006"
type = "work_order"
title = "Install a repository-owned glossary and report its drift"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-09-04"
updated = "2026-09-04"

[assurance]
commit_bound_verification = "required"
rationale = "The change adds an installed file to every repository that adopts the release and a report to inspect; the distribution boundary it introduces, that no glossary term ever ships, is a property every later release must keep, so its first proof must be commit-bound."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/",
  "templates/repository/standard/",
  "tests/",
  "docs/notes/",
  "docs/engineering/technical-communication/",
]

[delegation]
class = "execution"

[relations]
implements = ["REQ-TCM-007"]
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
decided_at = "2026-09-04T17:27:00Z"
decided_by = "delegated-executor"
reason = "Delegated DR-WO-START under [delegation] class 'execution': required check 'validate' success at e4222743fec27ed3a8b88fd6808c78cd08806422 (check-run 101113465388, source github-checks). Delegated DR-WO-START: execution branch wo/tcm-006-execution opened from main after WO-TCM-005 merged with VREC-TCM-005 verified."
+++

# Work Order: Install a repository-owned glossary and report its drift

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

Give every repository the place for its own glossary and a read-only
measure of how well the glossary keeps up with the corpus, while keeping
every term out of the distribution (`REQ-TCM-007`, `TCM-RFR-007` to
`TCM-RFR-010`).

## In scope

- `templates/repository/standard/docs/notes/glossary.md.seed`: structure,
  the two-vocabulary rule, an empty `Terms` section, no term.
- The installer, if the seed mode needs anything beyond what the domain
  index seeds already exercise; otherwise no code change there.
- The candidate `inspect_engineering_artifacts.py`: the `vocabulary`
  section, the two stoplists, the `--vocabulary-threshold` flag,
  deterministic output.
- `ARTIFACT_AUTHORING.md`: the two upkeep sentences of `TCM-RFR-009`.
- `docs/notes/glossary.md` of this repository: the nine terms the
  assessment named, each citing the artifact that fixes its meaning, and
  the two-vocabulary rule in its Summary; `docs/notes/harnessctl-reference.md`
  for the new `inspect` section.
- `tests/`: the `REQ-TCM-007` rows of `VER-TCM-003`, including the
  distribution-boundary test.
- This domain's index and the evidence packet.

## Out of scope

The requirement template and advisories (`WO-TCM-005`); any glossary
content for any repository other than this one; a configuration key for
the glossary path; any change to the hash-locked root copies; the release
carrying this change.

## Authorized decision envelope

The contents of the two stoplists; the tokenizer; the default threshold
within 30 to 100 occurrences; the layout of the vocabulary section; test
names and fixture layout.

## Constraints

- The seed carries no term; a test proves it on every run.
- The report is read-only and deterministic; it never blocks.
- Standard library only in the inspection script.
- The word "governor" is not introduced into `docs/notes/`.

## Expected change surface

One new seed template, one inspection script, one authoring-guide
paragraph, this repository's glossary and command reference, tests, the
domain index and the packet.

## Required verification

Execute the `REQ-TCM-007` rows of `VER-TCM-003`; the full suite on Windows
against the recorded baseline and the Linux lane; the released-evaluator
`validate` and `doctor`; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/technical-communication/evidence/WO-TCM-006/`.

## Stop and escalate conditions

Any glossary term found in a template; a seed the installer would rewrite
or hash; a need to change the installer's seed semantics for every seed;
a hash-locked file in the change set.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
