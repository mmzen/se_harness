+++
id = "WO-RLS-049"
type = "work_order"
title = "Clarify missing-input and failure-report instructions before release"
status = "in_progress"
owners = ["mmzen"]
created = "2026-10-12"
updated = "2026-10-13"

[assurance]
commit_bound_verification = "required"
rationale = "mmzen confirmed required commit-bound verification because release decisions depend on exact instructions and their independently observed native behavior."
decided_by = "mmzen"

[execution_scope]
paths = ["plugins/verity-plane/common/skills/change/references/hosted-drafts.md", "docs/engineering/release-0-23-0/"]

[relations]
implements = ["REQ-HAG-014"]
specifications = ["SPEC-HAG-008"]
verification = ["VER-HAG-008", "VER-RLS-040"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-13T01:25:48Z"
decided_by = "mmzen"
reason = "Human mmzen replied \"I approve\" on 2026-10-13 to WO-RLS-049, required commit-bound verification and its linked release-membership amendment, reviewed in PR #544 at 4afdbbcd048a09c8e543952c4fc87185cf52800a. This authorizes the exact one-file hosted-drafts instruction correction, bounded local checks and new-candidate qualification under unchanged VER-HAG-008 and VER-RLS-040. It explicitly authorizes the reviewed manual REL-SEH-036 gates amendment, preserving accepted bytes and lifecycle history, and includes this work in the existing review-publication grant for codex/release-0-23-0 to mmzen/se_harness:main, including later separately given verification-decision pushes. Human verification, merge, complete-release approval, desktop omission, adoption and host updates remain separate. Reviewed work-order SHA-256 93db645f0dbaf36a49a3f696077c655849acfcd694e5909badf057cabe6813a6; instruction before 55a07b9eee409692014db67d2758ea9dfc5224cd38f349a1d0a21ed19a581985 and after cdd3d9f13a7998a36ff5f2c293dff8dad6f61c54997f69f41edd48c6b096c23e; release amendment before fdb373581bd98b334536b9212f72f9d15739d5b20d1834641f48c94ad832f464 and after e56efa4b4b4a2e5045db06e68995423f3ddbb7b2bcebd0a9d6d6ccdc543d2c2c."
scope_paths = ["plugins/verity-plane/common/skills/change/references/hosted-drafts.md", "docs/engineering/release-0-23-0/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-13T01:28:50Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."
+++

# Clarify missing-input and failure-report instructions before release

## Objective and evidence

Correct the instruction route implicated by R23-NATIVE-001/002 in the exact
464034e8f0b189d330c3a8c5d8ce64c090b5cc86 Claude diagnostic. Keep the accepted
content and evidence criteria. This is a proposed one-file correction, not a
claim that wording alone guarantees agent compliance.

## In scope and expected change surface

- `plugins/verity-plane/common/skills/change/references/hosted-drafts.md`: move
  the existing intent-input check into the clarification step; keep unknown facts
  explicit; share the exhaustive-failure check between clarification and saved
  reports; identify the supplied selection path instead of guessing its location.
  The complete proposed bytes and diff are in evidence/WO-RLS-049/.
- `docs/engineering/release-0-23-0/`: preserve this failed candidate, exact proposal,
  checks, new-candidate qualification, aggregate verification and generated
  sidecars. With explicit approval, apply the exact REL-SEH-036 membership
  amendment that adds only this work order, preserving accepted bytes and history.

The existing fixed package map already includes this file for both hosts. The
complete-input adapter already delivers it byte-for-byte. Run existing delivery,
section-fidelity and package-link checks; no new parser, helper, schema, test
answer, workflow sequence or second policy implementation is needed. SPEC-HAG-008
records why no new architecture decision applies to this instruction-only scope.

## Out of scope and constraints

No runtime, evaluator pin, dependency, database, permissions, model, fixture,
requested outcome or qualification threshold changes. Do not edit accepted
SPEC-HAG-008 or VER-HAG-008, weaken a failed criterion, supply missing answers,
discard failed trials or retry until a pass. Broad performance work remains
deferred. Git remains authoritative; the service remains private.

## Verification and evidence

Required commit-bound verification is proposed because release decisions rely
on these instructions and their actual native behavior. The human must confirm
that classification before approval; no classification decision is fabricated.
Use VER-HAG-008 and VER-RLS-040 at the new exact candidate. First run and
independently assess one fresh Claude EFF-04A2 diagnostic. A failure stops further
native repetitions on that candidate. After a pass, continue the existing Codex
diagnostic/boundary checks and positive-case sequence. Full required native and
delivery qualification remains separate; desktop is still pending.

Rebuild and qualify the new exact package identities under the existing release
work. Preserve raw outcomes, visible transcripts, independent state/readback,
skips, timings and source comparisons. Reuse earlier results only where the
contracts permit exact, documented applicability. Include this work in the
final aggregate commit-bound record; do not create a duplicate assurance layer.

## Authorized decision envelope

This draft grants no implementation authority. Approval would permit the exact
instruction edit, local checks, evidence, completion and verification preparation.
Request inclusion in the current review-publication grant for
codex/release-0-23-0 to mmzen/se_harness:main, PR #544, including the later
separately supplied verification-decision push.

The installed evaluator has no generic accepted-definition amendment command.
The separate explicit request is to apply only the reviewed REL-SEH-036
membership amendment, preserving previous accepted bytes and lifecycle history.
Human verification, merge, complete-release approval, adoption and host updates
remain separate. This proposal neither accepts the current failure nor grants
the final release decision.

## Completion and stop

Complete only after the one-file correction and required independent checks
pass with evidence retained. Stop on another failed diagnostic, changed
requirements, uncovered paths or missing required evidence. Report actual
changes, checks, limits and the released evaluator's next step. No new owner
completion approval is added.
