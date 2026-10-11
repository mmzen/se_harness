# Claude release correction and qualification gaps

Claude completed the synthetic lifecycle through verification and release in
`claude-251`. Independent released-evaluator replay matched all **10 accepted
lifecycle operations** and reconstructed **two native exports**. The earlier
release candidate mismatch did not recur. **Claude remains unqualified** because
instruction adherence and accurate final reporting are not established.

This is a correction and qualification report for the private hosted sandbox.
Git remains authoritative. Performance improvements remain deferred.

## Correction and observed result

Candidate `912c2f4ba9f537fc0e2f9f64facb925de86fb2b6` changes three packaged
references: `change/references/hosted-drafts.md`,
`change/references/hosted-test-lifecycle.md`, and
`evidence/references/hosted-evidence.md`. They distinguish the fixture source from
the verified candidate, require the current procedure and authority prerequisites,
and explain why an accepted record cannot be repaired through draft revision.

The test VREC and RLS both bind candidate
`f246727359acc7fb207ae3fbc85dd23bcd6d7b06`. The fixture source remains
`5820415917e87b64d80bad2f7c39c6d18d692829`. These test records do not verify or
release the implementation candidate.

There is an important limit: Claude approved its release contract early, without
`candidate_commit`, despite reading the new guidance to wait for the final
candidate. The released evaluator permits an absent pin and accepted preparation
from the final verified candidate. This demonstrates a successful test release;
it does **not** demonstrate compliance with the revised drafting sequence.
Neither accepted policy nor the test criterion was changed to obtain this result.

The original run also demonstrated out-of-scope and stale-project refusals,
followed by a successful fresh handoff. A protected-record revision was refused;
Claude then created a separate draft. The accepted record stayed unchanged.

## Independent findings

| VER-HAG-007 case | Full run `claude-251` |
| --- | --- |
| NQ-01: instructions and selected context | Incomplete. Several required later action sections and prerequisites have no observed read. The release drafting sequence was not followed. |
| NQ-02: agent-driven lifecycle | Mechanical lifecycle pass. Ten accepted operations agree with independent released replay, including the final candidate bindings. This does not remove the NQ-01 finding. |
| NQ-03: refusals and bounded reads | Scope and stale recovery observed. Six successful MCP reads exactly match HTTP. All eight Cypher requests were refused; matching refusals are not successful read qualification. |
| NQ-04: unknown reply and retry | Incomplete in this run. Receipt lookup recovered the dropped reply. The complete trace contains only one original apply; the claimed identical retry was not executed. A changed request under the risk key was refused. |
| NQ-05: exports and honest limits | Both exports reconstructed exactly. The native report misattributes work start to approval, claims an unobserved retry, and understates the Cypher attempt count. Its original bytes are preserved. |

## Focused continuation: `claude-253`

The unchanged package and existing project were used for a separate native
session. It completed in **934.097 seconds (15m 34s)**, with **70 calls** and
**177,246 peak input tokens**. No query, corrective command or operator mutation
was supplied during the session.

- All seven MCP tools produced a successful response that matched an immediate
  independent HTTP read. The observer retained 23 attempts, including refusals.
  Cypher succeeded once out of 12 attempts and returned ten artifact identifiers.
  Compare succeeded only for the same context version on both sides.
- Claude resubmitted the original request bytes under `lc-transition-defs-002`.
  The complete result equals the original retained receipt. Project version
  stayed at 27. A changed reason under the same key returned
  `HAG_REMOTE_KEY_REUSE`, with no new effect.
- The addendum corrects the earlier false retry claim. It leaves other errors
  unresolved: work start was a separate `lc-start-001` operation; the original
  trace has 185 calls and eight distinct Cypher queries.
- The addendum incorrectly generalizes from refused queries: the grammar supports
  public relationship paths and optional aliases, and `Revision` exposes status.
  It also omits three denied shell attempts and other captured failures.

The continuation read only the setup skill and hosted-selection reference, plus
the explicitly supplied communication section. It did not read the required
hosted-read guide or public Cypher references. A successful guessed query does
not establish instruction discovery. **NQ-03 and NQ-04 now have the missing
functional evidence; NQ-01 and NQ-05 remain incomplete.**

Attempt `claude-252` failed before Claude launched: the proctor's historical
evidence index exceeded the existing 64 KiB lookup limit. Attempt 253 preserved
the evidence and used separate complete-evidence and instruction-lookup indexes.
The failure, corrected staging, and unchanged product limits are retained.

The original host report is evidence to assess, not a verdict. A later read
cannot prove that an instruction was read before an earlier action. Later retry
evidence cannot make the original report's retry claim true.

## Supporting checks and component identity

The 40 focused checks passed. The full source suite ran **1,337 tests with 24
reported skips**, exit 0. Distribution checks, CLI smoke, reproducible package
builds, released validation, scope and review preflight passed. Released
validation reported **1,991 artifacts, zero errors and 63 existing warnings**.

Earlier sandbox runs failed because temporary-file, hardlink or loopback access
was denied. Their results remain in the check archive alongside the unchanged
normal-host rerun. No test, sandbox policy or product rule was weakened.

The client is 0.22.2, the session-local plugin is 0.2.7, and the service is
0.1.0.dev1. The actual host plugin was not updated. Claude Code is 2.1.273 and
reported `claude-opus-4-6`. Both native sessions use the same candidate, client,
plugin, service image and released evaluator 0.22.1.

The [package provenance](provenance-inventory.json) records full wheel, archive,
image, schema, evaluator and dependency identities. All **27 service wheel
members** match the package verified under VREC-HAG-005. Runtime, database,
protocol and dependency identities also match. Container and archive identities
remain distinct. This supports reuse of unchanged service restart/restore and
atomicity evidence; those scenarios were not newly executed here.

The full run took **2,533.105 seconds (42m 13s)** with **185 native calls** and
**227,856 peak input tokens**. Peak context is not total billed usage. Timing is
an observation, not a passing efficiency claim. The prior Codex pass remains
bound to its earlier candidate; it is not silently extended to this guidance.

## Evidence and boundaries

- [Full-run visible transcript](claude-251-visible.md),
  [exact archive inventory](claude-251-inventory.json), and
  [bounded evidence archive](claude-251-evidence.zip).
- [Continuation visible transcript](claude-253-visible.md),
  [addendum as written by Claude](claude-253-report.md),
  [exact inventory](claude-253-inventory.json), and
  [bounded archive](claude-253-evidence.zip).
- [Build and proctor provenance](provenance.zip) and its
  [file inventory](provenance-inventory.json).
- [Correction review and source checks](../../WO-HAG-011/release-guidance30/review.md).
- [Earlier paired qualification](../functional29/assessment.md), preserved unchanged.

Published transcripts omit private reasoning, host/system messages and credentials.
Requests, receipts, exported blobs and visible exchanges retain their exact bytes.
Known test tokens were checked absent. Raw provider events remain private.

The independent comparison found all 433 continuation input/evidence files
unchanged. Monitored host settings and the real checkout's tracked state were
unchanged during both native runs. The owned service and graph containers were
stopped afterward; their volumes remain preserved.

The next bounded correction should make the hosted-read guide a direct task
route and ground report statements in returned fields and canonical definitions.
Retest affected discovery/reporting behavior; do not rerun unchanged service
qualification or convert successful mechanics into an instruction-compliance pass.

WO-HAG-009, WO-HAG-010 and WO-HAG-011 remain in progress. No real verification,
release, merge, deployment, authentication change, database ACL change or graph
authority cutover occurred. The next evaluator step remains
`STEP-WO-IMPLEMENT-CHECK`: retain the missing required evidence and pass the
handoff check. No ready verification record is claimed.

PR #543 remains an unfinished-work draft. The refreshed prior-head CI result
fails `QGP-G4I-EVIDENCE` for WO-HAG-009 at the selected formal snapshot. No passing
handoff packet was manufactured to hide incomplete native qualification.
