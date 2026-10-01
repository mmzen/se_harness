+++
id = "WO-RLO-013"
type = "work_order"
title = "Select formal release records during build replay"
status = "in_progress"
owners = ["mmzen"]
created = "2026-10-01"
updated = "2026-10-01"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen confirmed required commit-bound verification because release decisions depend on the corrected replay selecting formal authority. Approval: i approve. Work and verification scope are WO-RLO-013 and VER-RLO-010."
decided_by = "mmzen"

[execution_scope]
paths = [
  "scripts/replay_release_build.py",
  "tests/test_release_build.py",
  "docs/engineering/release-orchestration/work-orders/WO-RLO-013.md",
  "docs/engineering/release-orchestration/verification/VER-RLO-010.md",
  "docs/engineering/release-orchestration/evidence/WO-RLO-013/",
  "docs/engineering/release-orchestration/verification-records/VREC-RLO-013.md",
  "docs/engineering/release-orchestration/evidence/VREC-RLO-013-evaluator.json",
]

[relations]
implements = ["REQ-RLO-014"]
specifications = ["SPEC-RLO-004"]
verification = ["VER-RLO-010"]
architecture = ["ARCH-RLO-004", "ADR-RLO-004"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-01T20:30:30Z"
decided_by = "engineering-owner"
reason = "Human mmzen: i approve. Approves the reviewed WO-RLO-013 and VER-RLO-010 with required commit-bound verification, the two-file replay selector correction, ordinary updates to work/release-0-21-0 and draft PR 517, and existing read-only rehearsals. Permits the released 0.20.1 role-label encoding; mmzen remains the human decision-maker. Human verification, merge and exact release-record decision remain separate. Reviewed SHA256 9e77624778513987491ff8f89a0a97059a385549229ac98cecdca4b37b2b8348. Only confirmed work-order assurance metadata was added."
scope_paths = ["scripts/replay_release_build.py", "tests/test_release_build.py", "docs/engineering/release-orchestration/work-orders/WO-RLO-013.md", "docs/engineering/release-orchestration/verification/VER-RLO-010.md", "docs/engineering/release-orchestration/evidence/WO-RLO-013/", "docs/engineering/release-orchestration/verification-records/VREC-RLO-013.md", "docs/engineering/release-orchestration/evidence/VREC-RLO-013-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-01T20:31:19Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."
+++

# Select formal release records during build replay

## Objective

Make release replay select the one formal RLS without counting retained copies
under evidence as additional authority. Keep genuine ambiguity a failure.

## Observed defect

Read-only publication rehearsal 36919403159 on commit
2b7d318fd00e955edfec0443d5d7158891a41509 passed the candidate's two pinned
builds but failed the RLS-SEH-030 leg with:

> expected exactly one release record RLS-SEH-030; found 2

The recursive scanner reads both the formal record in
`docs/engineering/release-0-20-1/releases/RLS-SEH-030.md` and its preserved
copy in `docs/engineering/release-0-20-1/evidence/WO-RLS-029/released-record.md`.
The existing publisher selects formal files under domain `releases/` directories.
An evidence copy is not another formal release record.

## In scope

1. Restrict `_selected_record` in `scripts/replay_release_build.py` to the
   canonical `docs/engineering/*/releases/RLS-*.md` locations already used by
   the publisher. Keep the file and symlink checks, exact type/ID matching,
   parsing behavior, and refusal unless exactly one formal record matches.
2. Add focused regression cases in `tests/test_release_build.py`: a formal
   record with an evidence copy, an evidence copy without a formal record,
   two conflicting formal records, and exclusion of a symlink record where
   the platform supports symlink creation. Check preservation of input bytes.
3. Retain the original failure, run the required checks and repeat the existing
   read-only rehearsal for RLS-SEH-030 at the exact correction commit.
4. Prepare a separate commit-bound VREC for this repository tooling change.

## Proposed assurance

Required commit-bound verification is proposed because future release decisions
rely on the replay's selection of authority. Human confirmation is pending;
no assurance decision or work approval is recorded by this draft.

## Authorized decision envelope

After approval, the agent may start, implement, check, commit, record completion
and prepare verification within these paths. The proposal includes ordinary
updates to `work/release-0-21-0` and draft PR #517 in `mmzen/se_harness`, and
existing read-only publication rehearsal dispatches. No force push is permitted.
Human verification, merge, the exact release-record decision and protected
publication approval remain separate. Existing v0.21.0 publication authority
is retained for its matching later release.

Apply any human approval through released 0.20.1. Its required legacy role
label may encode that decision only with mmzen and the actual decision retained
in the reason. Approval of this work also confirms this compatibility encoding.

## Constraints and design

Use the existing selector and the publisher's established file boundary.
No new shared framework, new command, generalized scanner change or workflow
is needed. Reuse REQ-RLO-014, SPEC-RLO-004, ARCH-RLO-004 and ADR-RLO-004 unchanged.
VER-RLO-010 defines this narrow regression assessment; it does not replace or
weaken VER-RLO-004 or the later candidate and bound-record release checks.

Keep the two-file correction separate from wheel release membership. This work
changes repository replay tooling, not portable evaluator or plugin behavior.
REL-SEH-033 retains its exact thirteen work orders. Verify this work separately;
do not add its VREC to that contract's aggregate release record.

The implementation baseline is 2b7d318fd00e955edfec0443d5d7158891a41509.
PR coverage must also include WO-RLS-031 and retain the original PR base
f5f7c77c6eadfd7d6f1c68e136f1f7cc29cfc0a5. Do not hide earlier release changes
by substituting the correction baseline for the complete PR baseline.

## Expected change surface

One selector in the replay script; focused cases in its existing test suite;
this work order and verification contract; its own evidence, review and VREC.
The general distribution validator and publisher are inspection references only.

## Out of scope

No edits to accepted RLS, evidence copies, accepted definitions, release membership,
recipe, accepted hashes, build interpreter, workflow permissions, installed
instructions, evaluator selection, desktop criterion, marketplace or live tags.
Do not delete the evidence copy or special-case RLS-SEH-030 to make replay pass.

## Required verification and evidence

Meet VER-RLO-010 with released 0.20.1 as the governing evaluator and repository
source only as the system under test. Retain commands, working directories,
runtime identities, commit IDs, exits, outputs, failed attempts, preservation
hashes and hosted results under `evidence/WO-RLO-013/` in this domain.
VREC-RLO-013 and its evaluator JSON are proposed unused destinations; confirm
availability before supported capture. Include preparation-review material
under the same evidence directory. A ready VREC is not human acceptance.

## Stop and escalate conditions

Stop the affected action if a required check fails, the fix needs another file
or a different selection contract, accepted bytes would change, formal records
remain ambiguous, the destination advances, or publication/desktop criteria
would need to be weakened. Preserve all observed failures.

## Completion report format

Report the exact correction commit, test and hosted replay outcomes, preserved
record identities, remaining release blockers, current lifecycle state and the
evaluator's next accountable decision. A passing historical rehearsal does not
verify v0.21.0 or replace its later bound-record replay.
