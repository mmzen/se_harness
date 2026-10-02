+++
id = "INT-RLO-002"
type = "intent"
title = "Complete a release under one human approval"
status = "approved"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"
outcome = "The owner approves one verified release and receives all declared public delivery results without repeated authorization requests."

[relations]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T20:17:28Z"
decided_by = "mmzen"
reason = "Human repository owner mmzen answered \"Approve package, verification and review PR\" to the exact package review for WO-RLO-014/015/016 and their governing definitions, with required commit-bound verification under VER-RLO-011. This authorizes bounded implementation, local checks and commits, completion and verification preparation, ordinary review-branch push and draft PR from work/complete-release-approval to mmzen/se_harness:main, and its later verification-decision update. Human verification acceptance, merge, actual releases and the exact live configuration change remain separate. The selected released evaluator 0.21.0 governs this work. Reviewed draft SHA-256 eb64ed23c340939eae43e1c3be7a5ab2e2a0d74cfd869c6aa1531b85161baf6d; approved transition input SHA-256 eb64ed23c340939eae43e1c3be7a5ab2e2a0d74cfd869c6aa1531b85161baf6d. Only the confirmed WO assurance fields were added before this transition."
+++

# Complete a release under one human approval

## Problem

The owner repeatedly authorizes parts of one SE Harness release: the release
record, publication, marketplace delivery and release markers. Plugin assurance
also happens after evaluator publication. A release can therefore remain partly
delivered while waiting for further replies.

## Intended outcome

For the repository owner, one approval of a prepared and verified release starts
all declared delivery actions. The agent completes them without further approval
when the reviewed inputs and conditions remain unchanged. The owner receives a
report of actual public results, including any incomplete step.

The owner confirmed this outcome and the four-part proposal on 2026-10-02 with
"Ok i approve". That confirmation selects the direction. The concrete artifacts,
work scopes and assurance classification in this package still need review.

## Success measures

| Measure | Today | When reached | Observed |
| --- | --- | --- | --- |
| Further permission requests after complete-release approval | Repeated across evaluator, plugin and markers; exact count not measured | Zero when approved inputs and conditions hold | Owner's next complete release |
| Public outputs left waiting only for repeated authorization | Observed in prior release conversations | None | Final delivery report for each release |
| Uncertain or failed steps reported as complete | No allowed cases | Zero | Owner's review of each delivery report |

## Scope

Portable instructions explain a single human response covering the release
decision and its listed external actions. Repository automation delivers the
evaluator, GitHub release, PyPI, plugin marketplace, documentation, demonstration
pages and release markers. Required release-only integration is listed too.

This is a wider outcome than INT-RLO-001, whose non-goals excluded removal of
the PyPI decision and automatic integration. INT-RLO-001 and its historical work
keep their meaning. This new intent governs a prospectively selected complete
release route; it does not revise or activate replacements for old definitions.

## Limits

- Required checks and human verification remain required before release approval.
- No blanket permission for later versions, unrelated merges or deployments.
- No automatic repository adoption or host authentication changes.
- No new formal artifact type, service, general publisher framework or lifecycle state.
- Implementation approval does not publish a particular release or change live settings.
