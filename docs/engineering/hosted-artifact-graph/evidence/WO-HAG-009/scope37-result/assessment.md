# Scope and verification planning: Opus 5.5 rerun

**The two targeted corrections worked in this run.** Claude authored a usable
verification plan and a work order covering the complete change, ran the greeting
assertion, demonstrated both intended refusals, and reached an accepted handoff.
All four accepted operations replayed successfully through released evaluator
0.22.1. **Qualification remains incomplete:** Claude skipped one required authority
section before approval. Full paired-host scenarios were not run here.

Candidate: `50a215cdf44b68637d4c5aa8ab1fbfcbbe0d611f`. Trial: `claude-331`.
PR #543 remains draft, targeting `main`. Earlier observations remain unchanged.

## Changes

Four Markdown files clarify existing behavior:

- Read execution capabilities while planning verification. The plan must match
  the available assertion, platform and evidence fields.
- Apply the canonical complete-work-scope instruction before proposing the work
  order. Include definition approval writes and generated evidence in the
  complete retained comparison.
- Make the test-tool description discoverable during planning, and state its
  existing behavior precisely: local Windows equality assertion, source digest
  guard, recorded command/output/timing, no separate type assertion or Python
  version field, and no automatic verification record.

No executable code, service behavior, helper behavior, dependency, schema,
permission, formal criterion or decision right changed. The review and local
checks are in [scope37](../../WO-HAG-011/scope37/review.md). The original selected
canonical rules remain the authority; no parallel workflow is introduced.

## Observed result

| Check | Independent observation |
| --- | --- |
| Six artifacts | Agent authored INT/CAP/REQ/SPEC/VER/WO-P3-901; all type checklists were read |
| Verification content | VER describes the actual Windows equality assertion and available evidence; the prior invented Linux/type-check requirements are absent |
| Complete scope | WO includes the six formal files and its evidence directory; the final Git-derived handoff contains nine paths, all permitted |
| Greeting assertion | Passed in 0.070922 seconds; submitted evidence bytes equal the actual capture |
| Changed-draft stale preview | Revised VER invalidated the earlier preview; service returned `HAG_REMOTE_STALE_PREVIEW`; fresh preview recovered |
| Out-of-scope handoff | Intended `QGP-G4I-PATHS` / `WEX201` refusal; corrected evidence path passed without expanding scope |
| Lifecycle effects | Definitions approved, WO approved, WO started, handoff accepted: all four independently replayed |
| Cypher | Both native MCP responses complete and exactly equal to independent HTTP results |
| Refusal effects | Both original refused keys returned 404; versions remained unchanged until the next accepted operation |
| Final test state | Project 19, context 17; WO-P3-901 remains `in_progress` with accepted handoff; task forbade completion |
| Boundaries | All 120 inputs unchanged; 24 observed Write/Edit requests stayed under work/; 31 command captures retained; monitored repository and host settings unchanged |

The native report correctly discloses its gaps. Its transcribed Cypher files are
not the independent evidence: exact captured native responses and independent
HTTP replies are retained separately. No hints, completed requests, corrective
commands, hidden workflow or operator graph mutations were supplied during the
run. Only the exact test containers were stopped afterward; volumes remain.

## Remaining findings

1. **Required authority reading was skipped.** `AUTHORIZE_WORK.md#before-this-action`
   requires `AUTHORITY.md#delegation-and-separation` before reviewing approval.
   The entry conditions were delivered, but the section was not read. The agent
   explicitly admits this. Passing evaluator gates do not prove instruction
   compliance. The existing guidance table lists decision rights explicitly and
   leaves this second required section behind a further link. A small follow-up
   should make the complete applicable approval reading visible together, using
   canonical file pointers, then retest. Do not duplicate the policy text.
2. **Five avoidable failed calls remain.** Four helper usage errors and one
   draft-open request for a WO absent from the imported baseline caused retries.
   Two other failed calls are the intended refusal tests. All seven are retained;
   recovery does not erase them.
3. **Candidate wording remains inconsistent.** The report correctly identifies
   this qualification candidate, but later labels implementation candidate C
   unknown. The exact C above is independently established. No VREC candidate P
   was captured, as required by this focused task's stopping boundary.

The report also questions why the failed handoff lists one changed path and the
valid handoff lists nine. The evidence explains this: the first stops at the
caller-declared scope check; the second continues through evidence generation to
the complete Git-derived handoff. The unchanged adapter performs both checks.
This is not evidence of missing changes or a service defect.

## Same-task comparison

| Metric | Previous Claude321 | This Claude331 |
| --- | --- | --- |
| Model / CLI | Opus 5.5 / pinned 2.1.280 | Same |
| Native duration | 13:56 | 11:50 (710.395s) |
| Native tool calls | 112 | 103 |
| Failed items, including negative tests | 8 | 7 |
| Peak input context | 315,053 tokens | 305,803 tokens |
| Accepted operations | 3 | 4 |
| Verification matches execution | No | Yes |
| Valid handoff | Refused for omitted scope | Accepted |
| Intended stale and scope refusals | Not both demonstrated | Both demonstrated |
| Required instruction reading | Other limitations retained | One authority prerequisite skipped |

This is one observation per candidate, with different stopping outcomes. It is
not a controlled completion-time benchmark or a claim that performance is fixed.
Peak context uses the same provider-reported input/cache metric as the previous
assessment, not total billed tokens. The 0.071-second assertion is only one part
of the 11:50 native session; build, setup and independent assessment are separate.
Broad performance work remains deferred.

## Candidate, checks and limits

The task, fixture, model, CLI, permissions and 20-minute bound match Claude321
after normalizing disposable paths. Exactly 113 staged files are byte-identical.
Four instruction documents and two project/component identity files changed.
The rebuilt client wheel archive also differs, but all 127 wheel members are
byte-identical. The initial comparison stopped on that extra archive difference;
member inspection resolved it before launch. The comparison proof retains it.
The host CLI was not updated again for this rerun.

The exact candidate was built twice with the pinned producer and installed.
Both plugin archives contain the exact changed guidance. All 27 service wheel
members and the evaluator/runtime/database/protocol/dependency identities match
the prior package; earlier service qualification is reused, not newly claimed.

Source suite: 1,339 tests, 24 reported skips, exit 0. Focused resource, native and
plugin checks, distribution checks and CLI smoke passed. Released validation:
1,991 artifacts, zero errors, 63 existing warnings. The initial sandbox-denied
resource-test attempt is preserved alongside the passing host-access retry.

Before this update, all applicable technical CI checks on 176ca91 passed; three
conditional rehearsals were skipped. Harness validation remained failed for
unfinished qualification (`QGP-G4I-EVIDENCE`). Current-head CI is reported in the
PR, independently of these local observations.

WO-HAG-009/010/011 remain in progress. The actual selected released step remains
`PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK`. The synthetic test WO's later next
step does not advance these real work orders. This diagnostic does not replace
NQ-01 through NQ-05, the required Opus 4.6 authoring cases or paired Codex/Claude
qualification. No actual VREC, human verification, merge, release, deployment or
risk acceptance occurs. Git remains authoritative.

## Evidence

- [Visible transcript](claude-331-visible.md).
- [Native inventory](claude-331-inventory.json) and [archive](claude-331-evidence.zip):
  exact requests, results, authored content, reports, read trace, replay, refusal,
  parity and boundary evidence.
- [Provenance inventory](provenance-inventory.json) and [archive](provenance.zip):
  exact build/setup/observer sources, package comparison and component identities.
- Report scope, preflight and validation: report-checks.zip and
  report-checks-inventory.json.

Private reasoning, provider/account logs, credentials and executable binaries
are excluded. Historical evidence and exact retained source bytes are preserved.
