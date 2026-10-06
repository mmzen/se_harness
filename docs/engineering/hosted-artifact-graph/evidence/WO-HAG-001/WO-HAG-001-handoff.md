```toml
artifact = "WO-HAG-001"
checkpoint = "handoff"
formal_snapshot_sha256 = "8bfea947566e62452e7b5658aed6d4a4ebba302756c42a584510a6984c4df1ab"
rebound_at = "2026-10-06T04:08:07Z"
```

# WO-HAG-001 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Phase 1 continuation handoff

This packet accompanies the user's request to transfer unfinished work to another
Codex agent. It does not claim completion of WO-HAG-001 or acceptance of the hosted
service. The work order remains in progress.

The independent Phase 1 contract checkpoint is
`9b6a2c378c61ce3f35e4a70a960dd12406da5c7e`. Its scope, 60 schema checks, full
1,284-test regression result (22 reported skips), structural/distribution checks,
review findings and remaining work are retained in
[phase1-continuation.json](phase1-continuation.json) and
[phase1-continuation-observations.json](phase1-continuation-observations.json).
No hosted service scenario has been executed.

The initial publication check reported missing handoff evidence and the open
DEC-HAG-001. The released evidence command supplied the machine header above.
The decision remains open: mmzen already chose `extend-evaluator`, but the released
decision command rejected the actual human identity against the legacy owner
label. [The original decision attempt](correction-decision-attempt.json) remains
unchanged. No disposition or completion event is fabricated by this packet.

The receiving agent must preserve the released 0.22.0 governor, the verified
evaluator correction and its evidence, the open release/adoption dependency, and
RISK-HAG-001. Obtain fresh selected context before continuing. The full Phase 2
implementation, package walkthrough and recovery evidence remain outstanding.

## Phase 2 continuation — 2026-10-05

The Phase 1 narrative above is historical. DEC-HAG-001 is now decided, and the
selected public evaluator is 0.22.1. The prior complete packet is preserved in
[protocol04-prior-handoff.md](phase2-20261005/protocol04-prior-handoff.md).

The current [qualification assessment](phase2-20261005/protocol04-assessment.md)
records tested candidate 7290af984337e122b193981a187e58c29de41a16 and links the
component tuple, bounded raw observations and exact-byte inventory. The packaged
client, live boundary tests, independent evaluator comparisons and restart/restore
pass. Required native-agent qualification remains incomplete. Claude OAuth expired;
the prior Codex model session could not read the guidance under its tool policy.
Desktop is unperformed. RISK-HAG-001 remains raised.

This is an unfinished-work handoff for the authorized draft PR update. It does
not claim completion, verification acceptance, merge or public deployment.
WO-HAG-001 and WO-HAG-007 remain in_progress. Continue with the retained inputs
in [protocol04-continuation.json](phase2-20261005/protocol04-continuation.json).

## Claude qualification continuation — 2026-10-06

The preceding Phase 2 status is historical. The [Claude report](claude-20261006/report.md)
records candidate 5fa50787dba1fdd010f625335d844416dd3bf002 and the native MCP schema correction.
The guided CLI sequence, seven native MCP reads and service boundary suite pass.
Claude misreported a large partial response as complete; that finding remains.
Codex native qualification and desktop remain incomplete. Earlier independent
evaluator/recovery runs remain bound to candidate04. Both work orders remain
in_progress. No hosted VREC or verification acceptance is claimed. The complete
previous packet is archived in the new report before supported rebinding.

## Codex qualification continuation — 2026-10-06

The [Codex report](codex-20261006/report.md) records successful guided execution
of all 18 installed-client operations and seven native MCP reads on the same
candidate 5fa50787dba1fdd010f625335d844416dd3bf002. All seven responses match HTTP;
Codex correctly reports the large impact result as partial. The earlier local
file-access and approval-policy refusals are retained. Successful runs used
normal approval review. Automatic candidate-plugin loading and desktop were
not exercised. Claude reporting and final exact-tuple qualification remain
open as described in the report. Both selected work orders remain in_progress;
no completion, hosted VREC or human decision is supplied by these observations.

## Completed Phase 2 qualification — 2026-10-06

The preceding continuation entries are historical. The
[final assessment](final-20261006/report.md) records all twelve VER-HAG-001
scenarios on product candidate `21d268664ffeb111b8b9e9e94921073c7bc99ec1`.
It covers the native guided walkthrough, both native MCP clients, the independent
released evaluator, failures and refusals, concurrent writes, retries, and actual
restart/restore. Its archive preserves the previous packet bytes and failed runs.

The evidence supports implementation-completion and verification preparation
under the existing approvals. It supplies no human verification decision.
Read the work orders and their directly linked verification record for current
lifecycle state. RISK-HAG-001 remains raised; automatic Codex candidate-plugin
loading and desktop were not exercised. PR #535 keeps its existing target and
original comparison base.
