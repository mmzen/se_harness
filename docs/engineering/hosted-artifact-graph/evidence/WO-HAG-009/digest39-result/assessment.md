# Native preview-digest refusal and recovery

**The focused diagnostic passed.** Claude sent an old approval-preview digest
with the current project and context versions. The service returned
`HAG_REMOTE_STALE_PREVIEW`, committed no effect, then accepted one approval
after a fresh preview. Independent released-evaluator replay passed.

Candidate: `ee86a842550c19fb6a56913841757b42df9ecaec`. Trial: `claude-351`.
Model: Opus 5.5. Pinned CLI: 2.1.280. Service evaluator: released 0.22.1.
Client: 0.22.2. Session-local plugin guidance: 0.2.7.

## What this run covers

This is a narrower NQ-03 diagnostic on the same exact candidate and packages as
[Claude341](../authority38-result/assessment.md). It asks for the previously
missing digest-guard observation and recovery. It does not repeat the greeting
workflow or change a qualification criterion. No product source or instruction
file changed, and no package was rebuilt.

A fresh private project started empty. Claude chose to author one new intent,
INT-P3-001, with content based on the supplied greeting outcome. It selected its
own commands, amendment and query. The amendment added the task's exclusion of
source and greeting-text changes. No completed artifact or command sequence was
supplied. Decisions used only the synthetic test-owner identity.

## Evidence of the guard and recovery

| Observation | Independent result |
| --- | --- |
| Initial approval preview | Project 4 / context 2, selected original draft; digest D1 returned |
| Draft amendment | New revision; project 5 / context 3 |
| Stale apply | Same action and D1, but current expected versions 5 / 3 |
| Actual refusal | HTTP 409, `HAG_REMOTE_STALE_PREVIEW`; no receipt, files or affected revisions |
| State after refusal | Project 5 / context 3; amended revision still draft; rejected operation lookup returns 404 |
| Recovery | Fresh preview D2; one accepted apply advances project 5→6, context 3→4, intent draft→approved |
| Independent replay | Released 0.22.1 replay passed; only INT-P3-001 changed |
| Imported history | All seven -900 records match the source bytes in the independent projection |
| Cypher | Three complete native responses exactly match separate HTTP reads at project versions 4, 5 and 6 |
| Approval reading | Delegation section successfully read at event 47; first approval request at event 210 |
| Boundaries | All 120 inputs unchanged; 11 observed Write/Edit requests inside work/; repository and monitored host settings unchanged |

The prior run reached the earlier version guard. This run reaches the digest
guard. The digest itself binds revisions, versions and other inputs together;
this observation does not isolate each internal component. That is an explicit
limit, not a newly added qualification requirement. The native report states it
correctly. Its transcribed Cypher files are supplemented by exact captured
native responses and independent HTTP replies.

## Costs and remaining imperfections

Native duration was **7m39s (458.664 seconds)**, with **62 tool calls** and
**177,692 peak input-context tokens**. This includes import, one draft, amendment,
preview/refusal/recovery and reporting. It includes no greeting assertion or new
source implementation. Independent replay, setup and assessment are separate.
The narrower task is not comparable to the previous full greeting diagnostic;
these numbers do not establish a performance improvement.

Five failed tool items are retained: one unsupported instruction selector,
three JSON-pointer quoting errors and the intended stale-preview refusal.
The first preview also contained a doubled artifact prefix in its reason.
Claude preserved that action for the stale test, then corrected the reason in
the fresh preview/apply. There were no observed permission denials or operator
corrections during the run.

The report identifies the qualification candidate correctly but elsewhere calls
implementation candidate C inapplicable because it made no source implementation.
The actual C is the exact candidate above; no test candidate P was captured.
This wording issue remains disclosed. Source inspection supports the new intent
content, but the native agent's own review is not independent assurance.

## Checks, state and next work

The candidate's previous 1,339-test source suite (24 reported skips), focused
checks, distribution/smoke checks and exact package build remain applicable:
no product bytes changed. Package and helper identity, permissions and staged
input hashes were checked before this run. Live authentication passed. Evidence
scope, preflight and released validation are retained with this report.

At the preceding PR head `fabfdeba`, technical checks passed and three conditional
release rehearsals were skipped. The harness CI failure is the existing
WO-HAG-009 `QGP-G4I-EVIDENCE` blocker for unfinished qualification. New-head CI
is reported separately. PR #543 remains draft, targeting main, with the original
complete comparison base.

The specific missing digest-guard diagnostic is now closed. Continue the remaining
native qualification under VER-HAG-007/008; full NQ-01 through NQ-05 for both hosts
and required Opus 4.6 authoring cases remain pending. No criterion was relaxed.
Broad performance work remains deferred.

Actual WO-HAG-009/011 remain `in_progress` at
`PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK`. The test intent's approval does
not advance real work or provide human verification. No actual VREC, merge,
release, deployment, host update or risk acceptance occurs. Git remains
authoritative. Only the exact disposable test containers were stopped; volumes
are preserved.

## Retained evidence

- [Visible transcript](claude-351-visible.md).
- [Native inventory](claude-351-inventory.json) and [archive](claude-351-evidence.zip):
  exact requests, results, draft revisions, native report, guard review, read
  ordering, independent replay, refusal lookup, parity and boundaries.
- [Provenance inventory](provenance-inventory.json) and [archive](provenance.zip):
  task, preparation/observer sources, fresh identities and exact package reuse.
- [Report checks](report-checks.zip) and [inventory](report-checks-inventory.json).

Private reasoning, provider/account logs, credentials and executables are omitted.
Earlier evidence and its verdicts remain unchanged.
