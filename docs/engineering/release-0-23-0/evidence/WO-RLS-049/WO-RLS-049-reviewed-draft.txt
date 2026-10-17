+++
id = "WO-RLS-049"
type = "work_order"
title = "Clarify missing-input and failure-report instructions before release"
status = "draft"
owners = ["mmzen"]
created = "2026-10-12"
updated = "2026-10-12"

[execution_scope]
paths = ["plugins/verity-plane/common/skills/change/references/hosted-drafts.md", "docs/engineering/release-0-23-0/"]

[relations]
implements = ["REQ-HAG-014"]
specifications = ["SPEC-HAG-008"]
verification = ["VER-HAG-008", "VER-RLS-040"]
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
