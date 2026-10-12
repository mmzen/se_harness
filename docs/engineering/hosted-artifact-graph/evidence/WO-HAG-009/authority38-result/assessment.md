# Approval instruction discovery: Opus 5.5 rerun

**The targeted reading omission is corrected in this run.** Claude read
`AUTHORITY.md#delegation-and-separation` before its first approval request.
It authored six artifacts, ran the greeting assertion and reached an accepted
handoff. All three accepted operations replayed successfully through released
evaluator 0.22.1.

**Qualification remains incomplete.** The stale request reached the project
version guard before the preview-digest guard. This run therefore does not
demonstrate rejection of an old preview digest with current versions. Full
paired-host scenarios were not run here.

Candidate: `ee86a842550c19fb6a56913841757b42df9ecaec`. Trial: `claude-341`.
PR #543 remains draft, targeting `main`. Earlier evidence is preserved.

## Change and authority

Two rows in `plugins/verity-plane/common/skills/change/references/hosted-test-lifecycle.md`
now name the existing canonical delegation section beside decision rights.
Both approval-package review and application show their required reading together.
The change adds file pointers, without copying policy text or creating a second
workflow. No service, helper, schema, dependency, permission, decision right or
qualification criterion changed.

Existing WO-HAG-009/011 authority covers this correction and evidence. The
[implementation review](../../WO-HAG-011/authority38/review.md) retains the
bounded diff and local checks. No actual approval or start was repeated.

## Observed result

| Check | Independent observation |
| --- | --- |
| Required authority reading | Successful delegation section content return at event 239; first approval request at event 290 |
| Six artifacts | INT/CAP/REQ/SPEC/VER/WO-P3-001 authored; all six type checklists read |
| Verification content | Matches native Windows equality assertion, fixture digest and available evidence fields |
| Complete scope | Six formal files plus assertion and two generated handoff files; nine paths in final comparison |
| Greeting assertion | Passed in 0.077949 seconds; submitted evidence bytes equal the actual capture |
| Stale request | `HAG_REMOTE_STALE_PROJECT`; no current-run preview-digest-guard claim |
| Out-of-scope handoff | `QGP-G4I-PATHS` / `WEX201` refusal for `docs/notes/greeting-assertion.json`; approved evidence path then passed |
| Accepted lifecycle operations | Combined approval of six artifacts, work start, handoff; all three independently replayed |
| Cypher | Three complete native MCP responses exactly match independent HTTP replies |
| Refusal effects | Original refused operation keys return 404; independent reads confirm unchanged project versions until the next accepted mutation |
| Final test state | Project 18, context 16; WO-P3-001 remains `in_progress` with accepted handoff |
| Boundaries | All 120 staged inputs unchanged; 24 observed Write/Edit requests inside work/; 30 command captures; monitored repository and host settings unchanged |

The complete comparison starts at `234100a1501a042160c2f27a4f669ce0dbdf1f84`,
the first approval's input Git head. No later base or expanded approved scope
was used. The assertion checks existing greeting source; this diagnostic does
not claim new source implementation or a verification record.

No answers, prepared mutation requests, corrective commands, permission changes
or operator graph writes were supplied during the native run. Read-only
independent comparisons were separate. Only this trial's service and graph
containers were stopped afterward; their volumes remain.

## Remaining findings

1. **Preview-digest coverage is still missing from this run.** After changing
   VER, Claude supplied both old versions and an old digest. The version check
   refused first. Its report correctly acknowledges that the digest guard was
   not reached. The previous trial demonstrated that guard with the same
   service bytes; that historical observation is not a new native pass here.
2. **Six avoidable failed calls remain.** Five helper/input errors and one
   draft-open request for a work order absent from the baseline caused retries.
   The other two failed calls are deliberate refusal tests. All eight remain
   in the retained transcript and captures.
3. **Candidate wording remains inconsistent.** The native report identifies
   this qualification candidate but elsewhere marks implementation candidate C
   unknown. The exact C above is established independently. No candidate P was
   captured. The native agent's review of its own authored content also must
   not be treated as independent verification.

The agent unsuccessfully tried the concise-hosted-authoring reference. This
does not create another mandatory-reading failure: the applicable hosted-drafts
instruction permits the selected tool index **or** that reference. It read
the index. The failed access and retry cost remain evidence.

The successful delegation-section read proves content delivery and ordering;
it does not prove understanding or every other instruction obligation.

## Same-task comparison

| Metric | Previous Claude331 | Current Claude341 |
| --- | --- | --- |
| Model / CLI | Opus 5.5 / pinned 2.1.280 | Same |
| Native duration | 11:50 (710.395s) | 11:43 (703.218s) |
| Tool calls | 103 | 101 |
| Failed items, including negative tests | 7 | 8 |
| Peak input context | 305,803 tokens | 340,733 tokens |
| Accepted operations | 4: separate definition and WO approvals, start, handoff | 3: combined approval, start, handoff |
| Required delegation section | Skipped | Read before approval |
| Old preview digest with current versions | Guard reached | Not tested; earlier version guard reached |
| Complete scope and valid handoff | Passed | Passed |

These are single observations, not a controlled performance benchmark.
Context increased and total duration remains high. The 0.078-second assertion
is only one part of the 11:43 session. Setup, builds and independent review are
separate. Peak context uses the same provider-reported input/cache metric as
the earlier report; it is not total billed tokens. Broad performance work
remains deferred.

## Exact inputs and checks

The task, permissions and 20-minute limit match the prior run after disposable
path normalization. Of 120 staged inputs, 116 are byte-identical. The differences
are one guidance file, two project/component identity files and the client
wheel archive. All 127 client wheel members are byte-identical to the prior
wheel. The exact comparison passed before native launch.

The candidate was built twice with the pinned producer and installed. Plugin
packages contain its exact guidance. All 27 service wheel members and the
evaluator/runtime/database/protocol/dependency identities match the prior
package. Earlier service qualification is reused, not claimed as rerun. A live
authentication probe passed. No host CLI update occurred during this rerun.

Source suite: 1,339 tests, 24 reported skips, exit 0. Focused resource, native
and plugin checks, distribution checks and CLI smoke passed. Released
validation: 1,991 artifacts, zero errors, 63 existing warnings.

Before this update, applicable technical CI checks at review head `83a0a01`
passed; three conditional rehearsals were skipped. Harness validation remained
failed for unfinished qualification (`QGP-G4I-EVIDENCE`). New-head CI is reported
separately in the PR; local checks do not establish its result.

WO-HAG-009/010/011 remain in progress. Fresh checks for the selected WO-HAG-009/011
return `PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK`. The synthetic WO's handoff
does not advance those real work orders. This diagnostic does not replace
NQ-01 through NQ-05, required Opus 4.6 authoring cases or paired Codex/Claude
qualification. No actual VREC, human verification, merge, release, deployment
or risk acceptance occurs. Git remains authoritative.

## Next work

Retain the current pass for the targeted reading fix. Complete the missing
preview-digest diagnostic under the existing contract, with the version guard
and digest guard assessed separately, then resume remaining qualification.
Do not weaken criteria or count the earlier guard as the intended digest check.

## Evidence

- [Visible transcript](claude-341-visible.md).
- [Native inventory](claude-341-inventory.json) and [archive](claude-341-evidence.zip):
  exact requests, results, authored files, reports, reading order, replay,
  refusal, parity and boundary observations.
- [Provenance inventory](provenance-inventory.json) and [archive](provenance.zip):
  exact build/setup/observer sources, comparisons and component identities.
- [Report checks](report-checks.zip) and [inventory](report-checks-inventory.json).

Private reasoning, provider/account logs, credentials and executables are
excluded. Historical evidence and exact retained bytes remain unchanged.
