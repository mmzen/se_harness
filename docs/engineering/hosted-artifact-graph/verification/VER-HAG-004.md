+++
id = "VER-HAG-004"
type = "verification"
title = "Released evaluator reconciliation without losing hosted history"
status = "approved"
owners = ["mmzen"]
created = "2026-10-05"
updated = "2026-10-05"

[relations]
verifies = ["REQ-HAG-007", "REQ-HAG-008"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-05T12:41:38Z"
decided_by = "mmzen"
reason = "Human mmzen answered \"I approve\" to the reviewed WO-HAG-005 / VER-HAG-004 request, including DEC-HAG-002 bounded-manual-revision for the exact SPEC-HAG-003 and VER-HAG-001 replacements, required commit-bound verification, and ordinary updates to draft PR #535 in mmzen/se_harness from codex/hosted-artifact-phase1 to codex/hosted-artifact-graph-inputs, including ready-record review and the later separately supplied verification decision. The review binding SHA-256 is 2dd5104adee7a1f8cc94df384ae62f6cbc0169448d91dae738dedb7292acab0a. Earlier accepted bytes and lifecycle history are preserved. This is an explicit bounded manual amendment authorization; it grants no general amendment mechanism, verification acceptance, risk acceptance, merge, release or deployment. No machine lifecycle rule or required gate is waived."
+++

# Released evaluator reconciliation without losing hosted history

## Independence

Expected identities come from public RLS-SEH-033, the merged adoption commit
and the exact pre-amendment Git blobs named in WO-HAG-005 and DEC-HAG-002.
Use separately installed released 0.22.1 outside the checkout. Candidate
source does not govern its own reconciliation. Windows is the preparation
host; retain actual platform identities. This contract qualifies the bounded
prerequisite reconciliation, not the hosted service or a new public package.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-HAG-007 | Test + inspection | RC-01, RC-02, RC-03 | Exact released evaluator selected; decision attribution and draft admission work; prior authority/evidence remains exact. |
| REQ-HAG-008 | Analysis + test | RC-04, RC-05 | Branch integration preserves Phase 1 and reviewed main inputs; complete bounded scope and applicable checks pass without claiming hosted qualification. |

## Acceptance cases

1. RC-01: Compare both old complete definition blobs and preserved `.txt`
   copies with the recorded SHA-256. Compare proposed replacements with the
   reviewed digests. Confirm actual manual authority and activation are recorded.
   Existing lifecycle events are unchanged. Verify every pre-existing HAG
   evidence blob, fixture, candidate binding and VREC-HAG-001/002 is unchanged.
   The sole live-packet exception is WO-HAG-001-handoff.md: before a supported
   rebind, preserve its complete original Git-blob bytes at
   evidence/WO-HAG-006/WO-HAG-001-handoff-before.txt and prove their equality.
   The live packet may then acquire the current formal-snapshot binding;
   historical test observations and all older VREC-bound evidence remain exact.
2. RC-02: Run released `doctor`, `validate`, selected `check` and identity
   reporting on the integrated checkout. Root selection, CI pin and resource
   identity must all identify public 0.22.1 with the approved wheel/payload
   digests. Source remains separately identified as development 0.22.2.
   Preview and apply the existing DEC-HAG-001 choice only under actual mmzen
   authority. The disposition must identify mmzen and authority_owner
   engineering-owner separately; WO-HAG-001 ownership and state stay unchanged.
3. RC-03: In disposable projections run released `validate-draft` on generated
   incomplete and empty-link requirements, a valid capability link, an existing
   release-record link, a missing real target, duplicate TOML and an ID/type
   mismatch. Incomplete means authoring findings without approval; the valid
   capability is admissible; actual invalidity is refused. Preserve the public
   reference source bytes and historical evidence; record any selection overlay.
   Reuse existing correction scenarios, without copying evaluator policy into
   a service. No hosted HTTP/database scenario is claimed by these probes.
4. RC-04: Compare the merged tree against both fixed parent commits. Every
   imported release/adoption evidence blob must equal main. Every prior HAG
   fixture, canonical implementation and evidence blob must equal the HAG head.
   Review the automatic workflow/reference merges; retain both index additions.
   Verify the original PR target and a complete changed-path list. Check combined
   scope with WO-HAG-001/003/004/005; disclose any uncovered path and stop.
5. RC-05: Run the repository canonical test runner, distribution checks and CLI
   smoke check on the integrated candidate. Run affected focused HAG/workflow
   tests if the suite does not execute them. Run applicable local harness gates
   and later actual PR CI. Record skips as skips. Existing full-suite counts
   are historical observations, not a predetermined required count.

## Evidence retention

Retain results and exact commands under
`docs/engineering/hosted-artifact-graph/evidence/WO-HAG-005/`.
Preserve failures. Prepare a VREC only through the released capture procedure
on a clean exact candidate. Recheck its returned record and evaluator-evidence
destinations under the automatic relationship rules before writing.

## Residual uncertainty

Zero hosted scenarios have run at proposal time. All twelve VER-HAG-001 cases,
the packaged walkthrough and restart/restore remain required under WO-HAG-001.
RISK-HAG-001 remains raised. This result provides no service readiness,
host-desktop qualification, public delivery or production safety claim.

## Linked preservation amendment

This revision requires the explicit DEC-HAG-003 bounded-manual-revision decision.
The prior accepted file is preserved in full at
../evidence/WO-HAG-006/VER-HAG-004-accepted-before.txt. Its original lifecycle
events remain unchanged. The exception permits current handoff maintenance;
it supplies no hosted test, completed work, assurance decision or gate waiver.
