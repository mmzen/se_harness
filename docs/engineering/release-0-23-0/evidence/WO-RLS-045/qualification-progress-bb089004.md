# Qualification of candidate bb089004

Release preparation remains incomplete. Codex Windows desktop tests are deferred
and unverified at mmzen's request. A separate Codex read-only trial also exposed
an unresolved communication-reading prerequisite failure. No aggregate VREC or
release record is ready, and no implementation, verification or release state is
advanced by this report.

Exact implementation and package candidate: `bb0890045f462343ecae66ca30b20b06cf6e8ae6`. Released evaluator 0.22.1
governs the repository and private service. Client/evaluator candidate 0.23.0 and
plugin 0.2.7 are test inputs; Git remains authoritative.

## Functional and package checks

| Area | Observed result | Limit |
| --- | --- | --- |
| Windows source | 1,339 tests, 24 skips, exit 0 | Skips remain skips |
| CI Linux source | 1,339 tests, 2 skips, exit 0 | CI tested merge f6e34bfb251ff8ccf9b7d4c50d95234053ce9d2b, whose tree equals review head 97b1d2e7; eleven evidence-only paths differ from C |
| Packages | Two pinned builds byte-identical; released verifier, installed wheel/sdist and Windows/Linux surface checks passed | No publication |
| Real upgrades | Two successful rehearsals, same semantic digest fcd031e1d854ed39c7674e9a46afc1e364cbda089f517fcb5c66b447dd6f44ee | Exact candidate export; expected predecessor refusal retained |
| Private service | Walkthrough, 64 boundary observations and restart/restore passed | Private source-built sandbox only; database ACL remains deferred |
| Native delivery | Both CLIs: startup, activation after clone, resume, manual and actual automatic compaction observed; selection/isolation and setup boundary evidence retained | CLI/app-server is not Windows desktop; cached-offline check is adapter evidence |
| Local work-to-verification | Both disposable execution cases reached implemented work and a ready, commit-bound verification record; independent readback passed | Separate seeded approvals; no human verification or push; proposal finding R23-NATIVE-011 remains |
| Focused drafting | Both missing-input diagnostics and all four positive drafts passed independent content/readback assessment | Efficiency goals reported separately below |
| Claude full workflow | 11 accepted operations and 2 exports passed independent released replay; all seven MCP tools matched exact HTTP reads | Synthetic test decisions only |
| Codex full workflow | 12 accepted operations and 5 exports passed independent released replay | Original MCP views later became stale; separate immutable reads provide functional comparisons |
| Codex immutable read case | All seven tools matched exact independent HTTP responses; project version remained 29 | Communication prerequisite failed; no overall qualification pass |

The full Claude run read communication at event 19/result 20 before its first
explanation at event 30. Full Codex completed that read at event 30 before its
first explanation at event 31. The exact one-paragraph change therefore worked
in those two observed workflows. It did not reliably cover the separate read-only
trial described below.

The synthetic verified/released candidates remain
`c50c47cad7dba77ac7098e37ce10a8fc79e44480` (Claude) and
`d54f90430f866ab38456e2fa95941f3db563ca1a` (Codex). They do not verify C.
Imported source and records, Git-blob bytes, retry receipts and original candidate
bindings were checked. Actual failed calls remain in the archives and assessments.
The local successor execution also had a recovered Python quoting error at
event 32 despite PowerShell returning aggregate exit 0. Its separate command
diagnostics retain this error; the final fixture checks establish the later result.

## Outstanding observations

### R23-NATIVE-010 — Communication read occurred after the first update

In `codex-reads2`, the first English update is event 11. The first hosted-context
read is event 19 and the complete communication read is event 31. The agent reports
this accurately. Reading the policy later and passing all graph queries do not
repair the earlier ordering failure. Preserve the full workflows' narrower
successes and this trial's failure. No retry-to-pass or relaxed criterion applies.

The previous `codex-reads` attempt stopped before any graph read because the
operator's copied input inventory retained absolute paths from another workspace.
The reader correctly refused those paths. The fresh case relocated only inventory
metadata, compared every original input byte and repeated the permission probes.
It preserved the original failure and changed no product instruction or boundary.

### R23-NATIVE-011 — Proposed work-order scope remains incomplete

Both disposable new-work proposals remain draft, with no assurance decision or
implementation. They propose required commit-bound assurance but omit the fixed
generated VREC destinations while claiming no generated destination is unresolved.
That claim is too broad. The authoring boundary passed; complete proposal readiness
is not established. The execution cases use separate, independently seeded
approved WO-FLW-001 records with those paths included. Their passing execution
cannot approve or repair WO-FLW-002.

### Codex Windows desktop — deferred, unverified

mmzen requested "let's defer codex app tests". The prepared desktop kit was not
run. This records scheduling, not accepted release omission, risk acceptance or
an amendment to VER-RLS-040. Earlier releases' accepted omissions do not apply.

## Duration and context

| Positive drafting case | Seconds | Native calls | Peak input-context tokens |
| --- | ---: | ---: | ---: |
| Claude 1 | 232.215 | 13 | 61,780 |
| Claude 2 | 161.165 | 11 | 56,732 |
| Claude 3 | 165.552 | 12 | 56,954 |
| Codex | 203.414 | at least 12 | unavailable |

Claude median: 165.552 seconds; range 161.165–232.215. All three met the call
goal, two met the duration goal, none met the context goal. Codex missed duration;
its exact call count and context are unavailable, so those goals cannot be assessed.
The initial complete entries stayed below 64 KiB: Claude 64,537 bytes; Codex
65,309 bytes. Diagnostic times were 140.439 and 119.73 seconds respectively;
they are missing-input cases, not faster completed authoring.

Full workflows took 1,341.105 seconds for Claude (172 calls; 149 turns; reported
peak context 616,674) and 1,503.510 seconds for Codex (230 visible tool items as a
lower bound; exact calls, turns and context unavailable). The separate Codex
immutable-read case took 351.885 seconds and 55 visible tool items. Three focused
samples and concurrent runs are not a general model benchmark. Full-workflow and
focused models differ. This instruction correction claims no performance improvement.

## Evidence and next step

The [evidence index](../WO-RLS-054/evidence-index-bb089004.json) lists bounded
archives with SHA-256 and byte counts. Per-case assessments are retained under
`../WO-RLS-046/`; local fixture assessments are in the delivery archive.
Each archive contains its member inventory and publication method. Private reasoning,
credentials, runtime profiles and package/database payloads are excluded. Visible
commands, responses, failures and reports remain retained. Historical candidates
and their failed observations are unchanged.

WO-RLS-054 remains `in_progress`. Fresh checkpoint-free evaluation selects
`PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK`. Required checks and evidence are
not complete; no completion transition is applied. Resolve the instruction-order
and proposal-content observations within separately reviewed correction scope
before a successful aggregate qualification claim. Desktop remains pending.
The marketplace review ref, aggregate capture and release-record rehearsals also
remain unfinished. Public delivery WO-RLS-047 remains approved and unstarted.
