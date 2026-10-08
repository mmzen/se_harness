# Review: simpler and faster hosted authoring

## Decision requested

Approve implementation and review publication for **WO-HAG-011**, with required
commit-bound verification under **VER-HAG-008**, and approve **REQ-HAG-014** and
**SPEC-HAG-008**. All four records are currently draft. Accountable human: mmzen.

The existing WO-HAG-009 explicitly excludes new client behavior. The new package
adds that scope; it does not repeat or replace the existing work approvals.

## Useful outcome

An agent receives the applicable instructions, writes one document file and
submits it through the existing client. The client handles transport formatting
and retains full evidence while returning concise useful results. This addresses
the 11-minute, 56-call, 112,326-token one-intent diagnostic.

## Changes and verification

| Problem | Change | Evidence |
| --- | --- | --- |
| Instructions too long | Short skill entry points, selected route references and canonical section views | Source/section identity comparison and native read trace |
| Content repeated | One owner per rule; document files and compact result fields; full evidence stored once | Exact byte and result comparison |
| Too many calls and excessive duration | Typed existing operations, mechanical encoding/capture and useful returned fields | Same-task Claude runs and an affected Codex run, with actual calls and timings |

Experimental goals: under 3 minutes, at most 15 calls and under 40,000 peak input
tokens for the same fresh-project task. Record each goal separately from correctness.
Start with one Claude diagnostic; repeat twice only after a correct unassisted run,
then exercise Codex. Missed goals, provider limits and incorrect content stay visible.

No server, wire-schema, lifecycle-policy, template-meaning or authority change is
included. No new dependency, orchestration service or KIS gate. The full existing
VER-HAG-007 qualification remains pending and is not replaced by this diagnostic.

## What approval permits

Bounded local client/instruction implementation, ordinary checks, disposable
package builds, authorized native CLI tests and preparation of a verification
record bound to the exact candidate. Verification acceptance stays with mmzen.

The proposed publication grant covers ordinary pushes and updates to draft PR
#543 in mmzen/se_harness, from codex/hosted-agent-qualification to main, including
this package, its evidence, ready verification record and the later separately
supplied verification-decision commit. Keep the PR draft while existing full
qualification is incomplete. No merge, force-push, release, adoption or host update.

## Checks and pending input

- Released 0.22.1 validation: **1,991 artifacts, zero errors, zero authoring
  advisories**; 63 existing warnings outside this package remain.
- Planned scope: **35 paths covered**, no uncovered paths or invalid declarations.
  This checks the supplied plan; it is not proof that implementation cannot expose
  an additional dependency.
- Work-authorization graph, integrity and decision predicates pass.
- Approval is currently blocked by **QGS-ASSURANCE**: the human has not yet
  confirmed required commit-bound verification for this newly prepared work order.
  The requested package approval includes this classification; record it before
  the approval preview/apply. No decision field has been fabricated.
- Exact evaluator next step: **PROC-FOCUS-SELECTED / STEP-FOCUS-SELECTED**,
  supply the corrective input for QGS-ASSURANCE.
- No implementation, native run or lifecycle transition was performed for this
  package. Earlier qualification results and historical evidence remain unchanged.

## Review files

- [REQ-HAG-014](../../requirements/REQ-HAG-014.md)
- [SPEC-HAG-008](../../specifications/SPEC-HAG-008.md)
- [VER-HAG-008](../../verification/VER-HAG-008.md)
- [WO-HAG-011](../../work-orders/WO-HAG-011.md)
- [Checks and exact reviewed file digests](preparation-checks.json)

The package reuses INT-HAG-002 and CAP-HAG-002. It applies the existing KIS policy
to the entire agent task, including user effort and duration. New architecture,
risk-acceptance and decision records are unnecessary for this bounded adaptation.
Existing RISK-HAG-001/002 receive only affected-work links; their states and
history are preserved.
