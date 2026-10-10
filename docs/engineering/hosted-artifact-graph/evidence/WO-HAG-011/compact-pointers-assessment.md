# Compact results and content-review qualification

Candidate `d31e337425696c944ee61eda9957b6ac4bd2c82b` passes the two missing-input
cases and all four positive draft-content reviews. The context goal remains
missed in every Claude drafting run. This establishes the observed correctness
of the focused cases, not the full hosted lifecycle qualification.

## Changes assessed

- Retained instruction content satisfies its read obligation; recover it when
  missing, changed or lost from context.
- Codex must use the saved-report fallback when attempted-call capture is incomplete.
- Compact results retain one full-response path and JSON pointers for omitted
  catalogue fields. Small fields remain inline when a pointer would be larger.
- Content review matches each stated pass condition to its planned check.

The [candidate25 failure](concise-results-assessment.md) remains recorded. Its
second draft asserted a side-effect condition with no planned check. These new
trials do not replace that failure or combine with its repetition set. See the
[correction review](compact-pointers-review.md) for the bounded implementation.

## Native observations

| Trial | Case | Content/report result | Seconds | Native calls | Peak input tokens |
| --- | --- | --- | ---: | --- | ---: |
| claude-201 | Clarification | Pass | 98.782 | 2 | 32,863 |
| codex-201 | Clarification | Pass | 65.531 | At least 5 visible items | Unavailable |
| claude-202 | Verification draft | Pass | 170.423 | 9 | 52,717 |
| claude-203 | Verification draft | Pass | 219.800 | 12 | 56,440 |
| claude-204 | Verification draft | Pass | 241.706 | 8 | 54,685 |
| codex-202 | Verification draft | Pass | 173.295 | At least 13 visible items | Unavailable |

Comparable Claude positive runs, same candidate/model/task/permissions and fresh projects:

- Seconds: 170.423–241.706; median 219.800.
- Native calls: 8.000–12.000; median 9.000.
- Peak input tokens: 52,717.000–56,440.000; median 54,685.000.

Goals remain under 180 seconds, at most 15 calls and under 40,000 peak input
tokens. Per-run verdicts are in the assessments. They are measured separately
from correctness; none is waived. Three trials are not a general benchmark.
Clarification stops are not faster completed drafting. Codex call counts are
visible-item lower bounds, and its peak context is unavailable. Cumulative usage
does not establish peak context or an exact call total.

Independent review checked the saved artifact, not only the final reply. Each
positive draft has the correct verifies link, independently derived expected
value, a usable requirement-to-evidence matrix and exact evidence destination.
No positive result claims executed tests or lifecycle acceptance. All saved
documents match submitted bytes, and all seven imported records remain exact.
Both clarification projects remain at version zero. Codex uses the saved report
and discloses incomplete capture instead of treating it as proof of no attempts.

claude-203 used a second revision to add platform/evaluator detail. Its project
version is therefore 5; the other draft versions and full operation sequences
are retained in their independent assessments. No native failure was observed
in the completed streams; Codex's capture limitation remains explicit.

## Remaining cost and design review

The positive Claude task is 64,153 bytes: 20,069 canonical instruction bytes,
22,289 selected reference bytes, 5,490 fixture bytes, 11,475 selection/provenance
and presentation bytes, and 4,830 remaining task bytes. The first positive run
starts at 32,815 input tokens. The starting payload alone leaves little room
under the 40,000-token goal. It is not valid to equate these byte counts with tokens.

The new route avoids rereading delivered instruction files. It still carries a
large fixed entry and repeated operation results. One exact representative
response displays as 10,018 bytes with candidate25, 9,433 with the correction,
and 9,889 with all catalogue fields inline, using the same real path lengths.
The complete wire response is unchanged. This small display reduction does not
establish a general latency or token improvement.

The first positive run spent 6.705 seconds in recorded client commands and
received 30,880 visible tool-result characters. Remaining time is unclassified;
do not subtract overlapping tool time and call the remainder model time. Other
per-run costs and read traces are retained. The exact build/package/install
preparation took 395.296 seconds, separately from native task duration.

KIS assessment: typed file submission removes manual encoding and identity
copying; retained content removes repeat reads; exact evidence files avoid
displaying duplicate payloads. Remaining mutations each have a distinct effect:
import, open a draft context, create a template, and submit authored content.
This change adds no workflow command, service, dependency or approval. Pointer
handling adds a small maintenance cost justified by exact evidence retrieval;
the size guard prevents it from making small values larger. The saved-content
instruction replaces an abstract review sentence without a new report or gate.

The next optimization should address the fixed entry and routine result volume.
Measure which provenance and operation fields need to stay visible, and retain
the rest once with precise pointers. Reduce duplicated route explanation within
the approved skill scope. Do not silently trim canonical obligations, the
operator-selected fixture, expected outcomes or failure reporting. A change to
the approved input-delivery contract requires a linked amendment first.

## Supporting checks and identities

The source suite passed: 1,337 tests, 24 skips. Focused native/client tests,
installed-client tests, package/distribution checks and CLI smoke passed. Two
pinned builds matched. Released 0.22.1 validation reported 1,991 artifacts,
zero errors and 63 existing warnings. Scope and review preflight passed.

Fresh installed EFF-02/03 checks passed typed/raw equivalence, exact saved bytes,
stale-version and reused-key refusals, recovery after local capture failure,
and original-key recovery/retry after a dropped accepted reply. No duplicate
mutation occurred. Service evidence reuse is limited to unchanged server,
dependencies and governor bytes; changed client behavior has fresh checks.

- Client wheel 0.22.2 SHA-256: `d6577c4a549b5f12847f04eb9dd349ac0f42d9531875d3b217984bad4ab2c75a`.
- Claude plugin 0.2.7 SHA-256: `004783977efac9ed3f832fad6f4c4fb069fced1ca0dfe09fd66d41ff7438dc1f`.
- Codex plugin 0.2.7 SHA-256: `18c87c6e2a99fee82cc5c2db6573c07afdd54f8d7cdd7ef32f7c3d59e8ac77cf`.
- Governor: released evaluator 0.22.1 in its separate environment.

Fresh Codex boundary probes passed before both trials: selected-service access
and owned writes worked; outside writes and external networking were refused.
This session-only profile is not port-level isolation. Host warnings, including
the after-agent notification path error, remain in evidence. Host settings and
the active application were not changed. Owned containers were stopped; test
volumes remain available. Both small live authentication probes passed.

## Evidence and limits

Each trial has an `*-assessment.json`, `*-visible.md`, `*-evidence.zip` and
`*-inventory.json` in this directory. [candidate26-checks.zip](candidate26-checks.zip)
and its [inventory](candidate26-checks-inventory.json) retain commands, versions,
package identities, exact source comparisons, deliberate failures and recovery.
Private reasoning, raw host/system events and credentials are excluded from
published evidence. Original local captures are unchanged. The copied label in
claude-201's component proof is corrected by a separate clarification; its
hashes were already those of candidate26.

Full NQ-01 through NQ-05 under WO-HAG-009/010 remains incomplete. These focused
cases do not qualify desktop, compaction/resume, production use or release.
WO-HAG-011 remains in progress and verification is pending. The released next
step is `PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK`, the handoff check.
Draft PR #543 keeps target main and the disclosed WO-HAG-009
`QGP-G4I-EVIDENCE` blocker. No evidence is rebound to hide incomplete work.

The fresh single-work-order handoff check against the unchanged complete PR base
also reports `QGP-G4I-PATHS` for
`docs/engineering/hosted-artifact-graph/evidence/WO-HAG-009/claude-discovery-read-trace16.json`
and missing WO-HAG-011 handoff evidence at formal snapshot
`fe9dca7d6953d5998ec1b06420d8ec5388ed1975a422c6aba1c8af3ec9eac6d6`.
This check cannot treat the multi-work-order diff as WO-HAG-011 alone. The combined
PR check uses the existing complete declaration; its WO-HAG-009 evidence blocker
still prevents a passing overall handoff. The base, approved scopes and old
evidence remain unchanged. These results are retained as failures, not passes.
