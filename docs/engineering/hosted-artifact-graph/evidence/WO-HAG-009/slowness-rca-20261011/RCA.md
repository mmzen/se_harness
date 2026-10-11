# RCA: slow native agent qualification

Analysis date: 2026-10-11. Observed runs: 2026-10-10.
Scope: WO-HAG-009 qualification, with WO-HAG-011 efficiency work as context.
Status: evidence-based diagnosis; corrective actions below are proposals.

## Finding

**The strongest supported cause is excessive agent orchestration: too many
serial reads, request-construction steps and recoveries for a small task.**
The interface still makes the model work out mechanical lifecycle inputs.
Instruction discovery and large results add more work at each stage.

The evidence does **not** show the graph database or network taking most of
the time. In Claude's 30-minute run, all 130 tool calls together occupied
about **1 minute 29 seconds**. The remaining **28 minutes 31 seconds** fell
outside those observed intervals. That time includes model responses, provider
waiting, compaction and other host work. The available trace cannot divide it
accurately between those causes. Calling all of it “reasoning time” would be
unsupported.

This is an operational root-cause assessment, not a controlled measurement of
each cause's contribution. The observed failures support the diagnosis;
matched before/after tests are needed to prove how much each fix saves.

## What was slow

The greeting function already existed. These runs did not spend 30 minutes
implementing that function. They tested a full governed lifecycle around it:
create seven initial formal artifacts, validate and approve them in a disposable
test project, start work, check the greeting, record a risk and decision, exercise
failure recovery, hand off, verify, release, export and read the graph.
All decisions in the test were synthetic. They granted no real authority.

| Run | Duration | Tool activity | Result |
| --- | ---: | --- | --- |
| Codex full lifecycle | 27m 19s | 242 observed tool items; lower bound | Completed the corrected test lifecycle; 13 accepted operations and four exports replayed independently |
| Claude full lifecycle | 30m 00s | 130 calls: 37 Read, 65 Bash, 28 Write | Timed out before handoff apply; five accepted operations replayed; no native exports |
| Codex read-only repeat | 4m 46s | 32 observed tool items; lower bound | Nine valid HTTP/MCP comparisons matched across all seven read tools |

Codex's combined native time was **32m 05s**, including the separate read repeat.
Builds, independent replay and report preparation are outside these durations.
Claude's timeout is an incomplete result, not a 30-minute successful completion.
Call counts are not directly comparable: Codex's format exposes a lower bound.

Impact: long feedback cycles, high context use, repeated recovery and incomplete
qualification. Claude reached 165,599 peak input tokens. Codex's peak context was
not available. Billing cost cannot be derived reliably from these observations.
The real repository's tracked state and selected noncredential settings matched
their before/after observations. No authority bypass or data loss was observed.
The PR remains unfinished because required qualification evidence is missing.

See the [full assessment](../lifecycle27/assessment.md) for exact outcomes and
the [visible Codex](../lifecycle27/codex-221-visible.md) and
[visible Claude](../lifecycle27/claude-221-visible.md) exchanges.

## Where the time went

These are approximate wall-clock intervals between completed milestones.
Each interval includes all activity between its boundaries, including reads,
model/host time and recovery. They are not isolated measurements of one action.
The [timing evidence](timing-evidence.json) records the exact boundaries and method.

| Milestone interval | Codex | Claude |
| --- | ---: | ---: |
| Discover instructions, import, open context | 1m 29s | 2m 56s |
| Create and complete seven initial artifacts | 3m 36s | 4m 38s |
| Validate, approve, start and recover; initial reads in Codex | 5m 06s | 7m 14s |
| Check greeting, record risk and decision | 1m 34s | 8m 15s |
| Handoff attempts; scope correction and completion in Codex | 8m 16s | 6m 57s, then timeout |
| Verification, release and exports | 3m 24s | Not reached |
| Inspect evidence and produce final reports | 3m 54s | Not reached |
| **Total** | **27m 19s** | **30m 00s** |

Claude's timestamped tool intervals total **89.373 seconds**. Their complement
is **1,710.749 seconds**, or **95.0%** of elapsed time. Separately, its 43 helper
command records total 64.030 seconds of subprocess execution. Codex's 73 helper
records total 114.480 seconds. These helper totals are a subset of activity,
can overlap, and must not be added to tool intervals or used as an exact service
latency total.

## Causes and contributing factors

### 1. Mechanical lifecycle work remains with the model

**Observed:** Claude constructed request files and recovered from wrong lifecycle
states, risk-decision fields, identities, command flags and handoff inputs.
Examples include using `accepted` where `approved` was required, incorrect
decision inputs, and an incorrect handoff content digest. Its trace contains
28 file writes and 23 `remote rehearse` calls. Codex used 38 `remote rehearse`
calls. These counts include valid previews and deliberate failure tests as well
as mistakes; they are not counts of unnecessary calls.

**Assessment:** The system requires the model to reproduce details that a narrow
client interface could construct and validate. A wrong field causes another
tool call, response, read and model turn. This is a strong contributor to the
duration and recovery burden. Its exact time share is unmeasured.

The earlier typed interface covered import, opening a draft context, creating
an artifact, revising it and reading a revision. It did not remove this burden
from the later lifecycle operations. Extending that interface requires a new
bounded proposal; it is outside the current five-operation client scope.

### 2. Instruction navigation still causes guessing and repeated reads

**Observed:** Claude guessed headings such as `AUTHORITY#read-this-when` and
`EXECUTE_WORK#start-the-work`, and guessed file locations. It also used an
unsupported helper flag. Codex requested two instruction resources without
their required headings, then read full files and later requested exact sections.

In Codex, roughly **179 seconds** elapsed between the successful corrected
handoff preview and its apply record. This interval contains a result read,
a task reread, the failed instruction request, full-file reads and the later
section request. It also contains model/host time; 179 seconds is not a measured
file-reading cost.

**Assessment:** Providing a file pointer alone is insufficient when the next
action needs an exact section or input contract. The route should identify the
existing canonical section at the point of use. Reading already retained,
unchanged content again adds context without adding information.

### 3. Result volume and context growth amplify the work

**Observed:** Visible tool results contained 1,817,151 characters for Codex and
430,213 for Claude. Characters are not tokens. Claude's peak input context was
165,599 tokens and automatic compaction occurred.

Claude's longest observed gap between tools was **176.3 seconds**. Compaction
events occurred within that gap. The trace does not establish that compaction
alone took 176.3 seconds.

**Assessment:** Large results and repeated instruction reads give the model
more material to process and retain. Compaction adds recovery work. This is a
plausible feedback loop, supported by the observed growth and compaction, but
these runs do not measure latency per token or prove how much time compact
output would save.

### 4. Unplanned recovery adds to deliberate failure testing

**Required test work:** lost-reply recovery, identical retry, changed-request
conflict, out-of-scope handoff and stale preview checks. These cases explain
part of the workload. They should not be counted as normal feature delivery.

**Unplanned work:** Codex's original work-order scope omitted the paired decision
file. The evaluator correctly refused the handoff. Codex prepared a corrected
work order and release definition, then validated, approved and started the
corrected test work. About **3m 06s** elapsed from that scope refusal to starting
the correction. This was separate from the deliberate out-of-scope test.

Claude additionally recovered malformed requests and navigation mistakes before
reaching the required failure cases. The risk/decision interval alone took
8m 15s and included compaction and recovery.

**Assessment:** Input completeness and discoverability problems are detected
too late. Required guards worked; removing guards would conceal errors. The fix
is to make valid inputs easier to construct and omissions easier to detect
before approval, while keeping unexpected paths refused.

There is also a baseline cost from the workflow itself: seven initial records,
their links and the separate lifecycle stages. Shorter instructions cannot
remove that cost. Review whether each obligation is necessary for the intended
use case, separately from whether a test must exercise it. Changing an accepted
obligation needs an explicit amendment; this RCA does not waive one.

### 5. Test orchestration and telemetry have their own defects

The proctor compared Codex's initial MCP responses against HTTP too late, after
the graph had changed. All nine comparisons mismatched. The separate fixed-view
repeat added **4m 46s** of native time. Its first launch also failed before Codex
started because the required empty work directory was missing. Both failures
remain recorded. They do not establish a graph-service parity defect.

Claude used extensionless helper-record filenames. The original cost collector
searched only `.json` and reported zero command time. The preserved supplemental
scan found all 43 records. This did not slow the native run, but it impaired
diagnosis. Codex lacks comparable per-tool timestamps, and phase timing initially
depended on filesystem metadata. These gaps prevent precise cost attribution.

## Is the hosted service the cause? What about local artifacts?

These runs used a local private Docker service, not a distant production server.
Observed tool durations do not support network or database execution as the
dominant cause here. They do not prove service performance at larger scale or
over a real remote connection.

The hosted route adds imports, draft contexts, versions, receipts, request
encoding, exports and HTTP/MCP comparisons. Some are product work and some are
qualification work. A local-artifact workflow does not necessarily incur those
same costs.

Instruction discovery, formal artifact authoring, approval boundaries, evidence
reading and reporting are shared concerns. They can also make a local workflow
slow. **We have no matched local-versus-hosted benchmark, so we cannot state
that local artifacts take the same time or quantify the hosted overhead.**

## Did earlier improvements help?

Yes, the narrower task improved, with limits. In the three candidate26 Claude
runs that created one verification draft, the median was **219.8 seconds,
nine calls and 54,685 peak input tokens**. All three content reviews passed.
The earlier candidate17 medians were 296.55 seconds, 13 calls and 62,427 tokens.
These are small observed samples. The candidate26 median still missed the
180-second and 40,000-token goals, while meeting the 15-call goal.

The full lifecycle exercises substantially more work. Comparing its 30 minutes
with a one-artifact run does not establish a regression. In the comparable full
rounds, Claude timed out in both. Candidate27 fixed the test Git-base problem and
reached a successful handoff preview, but did not show an overall time improvement.
Codex took longer than round26 and incurred the additional scope correction.

Sources: [focused authoring assessment](../../WO-HAG-011/compact-pointers-assessment.md),
[candidate17 observations](../../WO-HAG-011/complete-input-qualification-assessment.md),
[previous full lifecycle](../lifecycle26/assessment.md),
[candidate27 correction](../../WO-HAG-011/lifecycle-correction27/review.md).

## Corrective action proposal

Prioritize fewer model-mediated steps, not simply fewer instruction words.
KIS means reducing total work for the user, agent, client and test operator.
Replacing a long instruction with a vague pointer can increase that work.

| Priority | Proposed change | Responsible area | Evidence of success |
| --- | --- | --- | --- |
| 1 | Give each affected action exact resource paths, headings, required inputs and one valid example. Reuse unchanged instructions already in context. | Plugin guidance | Targeted Claude risk/decision and handoff cases complete without guessed headings, fields or flags; fewer calls and shorter wall time |
| 1 | Return concise results for routine use, with explicit pointers to retained full evidence and the next required section. Keep failures, gates and incomplete-result indicators visible. | Existing client/result helpers and guidance | Lower visible output and peak context; exact full evidence remains available; content and failure reviews still pass |
| 1 | Fix diagnostic collection and test scheduling: timestamp phases/tools, accept all record filenames, compare reads at the same version, check launch prerequisites. | Qualification driver | Recomputable timing coverage; no repeat caused by changed comparison state or a missing directory |
| 2 | Propose small typed constructors for the remaining lifecycle requests. Derive mechanical fields from exact returned context; keep evaluator decisions and explicit preview/apply boundaries. | Client, through a new bounded package | No agent-authored encoding/digest fields for covered requests; unchanged authority, stale-input and retry tests; fewer calls |
| 2 | Check the planned generated paths before work approval, including paired risk/decision and evidence outputs. Show omissions for correction. | Guidance/client design | No surprise generated-path omission on the normal path; unapproved paths remain refused |
| 2 | Measure the normal lifecycle separately from failure qualification, then compare local and hosted routes using the same task and conditions. Preserve every required failure scenario. | Verification design | Three independent runs per comparable case; median/range, content quality, calls, context and errors reported separately |

Start with the affected Claude operations, not another unchanged 30-minute run.
Extend to the full qualification only when the targeted cases pass and show a
measured improvement. Existing focused goals remain the reference for the
one-artifact task. Set a separate normal-lifecycle budget after obtaining a
comparable baseline; this RCA does not invent a new acceptance gate.

Instruction and test-driver corrections may fit the current approved work.
New lifecycle client behavior or changes to accepted test criteria require a
bounded proposal and the corresponding authority. Moving failure scenarios out
of a normal-path benchmark must not remove them from qualification.

Do not add a general workflow engine, new model agents, global caches or another
policy layer as the first response. Use direct helpers and one canonical source
for each instruction. Do not reduce quality checks to meet a time target.

## Evidence, method and limits

- Tested implementation: `1b4ca16833b3908882e4a961c150156aca417f3c`.
  Existing evidence commit: `05da5b74e30cc0b80f9e5f0fff9a72cf1fa27b71`.
  Released evaluator: 0.22.1. Candidate client: 0.22.2; candidate plugin: 0.2.7.
- [Timing evidence](timing-evidence.json) contains phase anchors, file digests,
  captured filesystem timestamps and Claude's 130 matched tool intervals.
  Tool-use/result timestamps are retained without tool contents or private reasoning.
  Union the intervals to reproduce 89.373 seconds; subtract from the recorded
  1,800.122-second session to reproduce the complement.
- Phase anchors use last-write times of newly created command records. The helper
  creates them exclusively rather than overwriting them. This is an approximate
  reconstruction: Git does not preserve those timestamps. The captured metadata
  is now retained. All four Claude anchors match their unique tool-result times
  within 0.052 seconds. Comparable Codex timestamp crosschecks are unavailable.
- All entries in the three existing native evidence archives were checked against
  their inventories. The selected phase records match their archived bytes.
  [Codex inventory](../lifecycle27/codex-221-inventory.json),
  [Claude inventory](../lifecycle27/claude-221-inventory.json),
  [read-repeat inventory](../lifecycle27/codex-221-reads-inventory.json).
- The original Claude zero-command cost result remains preserved; the separate
  `command-cost-supplement.json` in its archive supplies the corrected total.
  Raw provider streams, private reasoning and credentials are not published.
- There is one full run per host in this round. Models, permissions and workloads
  differ. No controlled provider-speed, context-size, local/hosted or scale
  experiment was performed. No new native run was needed for this analysis.

This RCA records an observed problem and proposed remedies. It does not complete
WO-HAG-009 or WO-HAG-011, waive missing Claude cases, or verify the implementation.
WO-HAG-009 remains `in_progress`; the fresh released result selects
`PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK`. Qualification gaps must be resolved
before its handoff check can support completion. PR #543 remains draft.
