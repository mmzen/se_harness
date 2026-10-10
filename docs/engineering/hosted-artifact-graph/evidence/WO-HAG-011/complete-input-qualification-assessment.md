# Complete-input qualification assessment

The approved complete-input change is implemented at candidate
`db7f2d241dfe680a48328014e584909d10335835`. The amendment preserves the previous
accepted files and their lifecycle history. [Activation](input-delivery-20261010/activation.json)
records mmzen's actual approval of the proposal published at
`08a3ad39ee3e349a2fefe24502575f5f082b7e26`.

WO-HAG-011 remains **in progress**. This assessment records content results,
performance and a Codex delivery defect separately. It grants no verification,
merge, release, adoption or broader host qualification.

## What changed

An explicit driver option assembles the complete selected fixture and exact
applicable instruction sections into one entry. It includes every one of the
12 source files, all seven existing formal records, nine canonical sections,
four selected references and the existing selection. It adds no completed draft,
expected missing answer or workflow sequence. Native agents still choose and
execute the operations and author their own documents.

The driver checks containment, inventory/manifest identities, exact UTF-8 bytes,
duplicates and the complete 64 KiB task limit. Invalid input refuses before host
execution. Source files and the original pointer route remain available.

Independent comparison confirms the included source bytes match their original
Git blobs and the instruction/reference bytes match the identified release and
candidate packages. This explicit test route does not prove automatic startup
or compaction delivery.

## Native results

EFF-04A tests truthful handling of missing input. Its correct result is an
explicitly incomplete draft or a precise stop. EFF-04B tests a complete new
verification-contract draft. All times include the native session, its reads,
imports, mutations and final report. Preparation is separate.

| Trial | Case | Content verdict | Seconds | Calls | Peak input tokens |
| --- | --- | --- | ---: | --- | ---: |
| [claude-111](claude-111-assessment.json) | EFF-04A | pass | 400.396 | 13 | 68,461 |
| [codex-111](codex-111-assessment.json) | EFF-04A | pass | 148.438 | 12 visible items; exact total unavailable | Unavailable |
| [claude-112](claude-112-assessment.json) | EFF-04B | pass | 252.974 | 13 | 59,655 |
| [claude-113](claude-113-assessment.json) | EFF-04B | fail | 302.182 | 13 | 62,427 |
| [claude-114](claude-114-assessment.json) | EFF-04B | fail | 296.550 | 15 | 63,663 |
| [codex-112](codex-112-assessment.json) | EFF-04B | pass | 241.615 | 20 visible items; exact total unavailable | Unavailable |

Claude111 acknowledges the existing definitions and leaves one intent draft
explicitly incomplete. Its confirmation language and before-reliance explanation
are disclosed limitations, not an accepted new product outcome. Codex111 names
the missing operational benefit and measure and stops before import or mutation;
the independent final service status is version zero.

Each positive case is assessed through an independent saved-document read,
comparison with its submitted bytes, the governing requirement and the native
report. The per-trial assessments retain the exact content findings and failures.
The imported records are separately read and compared with their original bytes.
No trial result is inferred from admission or process exit alone.

Claude113's saved draft and detailed report correctly distinguish planned checks
from executed tests. Its final reply nevertheless says the contract was
"verified in the hosted sandbox." The task expressly prohibits that claim.
The trial therefore fails reporting, despite passing draft-content inspection.
This is no evidence of a real verification transition; the draft state did not
change. Both the correct detailed report and the contradictory final reply remain.

Claude114 also produces a usable draft and accurately reports a recovered HTTP404
create refusal. It used a project ID as a draft-context ID, then opened the context
and corrected the request. Its report incorrectly labels the result incomplete
solely because the evaluator's `content_review` is `not_assessed`, although its
own review finds no missing content. The evaluator does not perform that agent
review. This fails readiness reporting, not saved-document content or a service
gate. The three Claude draft documents pass inspection, but only Claude112 passes
the complete content-and-reporting assessment.

Codex112 passes both draft-content and reporting inspection. It reports both
refused reads, distinguishes structural validation from its own content review,
and states that no behavior test ran. Its 241.615 seconds and at least 20 observed
tool items miss the time and call goals. Peak context is unavailable. The correct
content result does not close the initial-delivery and recovery findings.

## Efficiency and comparison

The three positive Claude attempts use the same candidate, model
`claude-opus-4-6`, fixture, permissions and fresh-project task. Their results are:

- wall_seconds: 252.974–302.182; median 296.55.
- native_calls: 13–15; median 13.
- peak_input_context: 59655–63663; median 62427.

Goals remain less than 180 seconds, at most 15 calls and less than 40,000 peak
input tokens. The [comparison](candidate17-comparison.json) reports each outcome.
All three Claude positive attempts meet the call goal and miss both the time
and context goals. The 296.550-second, 13-call and 62,427-token medians describe
the attempts, including failures; they do not establish successful qualification.
Missing Codex call/token totals are unavailable, not zero or passes. Negative
diagnostic timings are not positive authoring measurements.

The previous pointer-route positive Claude median was 249.398 seconds, 21 calls
and 57,952 peak tokens on candidate15. The new range/median includes all scheduled
completed attempts, including reporting failures; it is not a success-only
benchmark or evidence of three correct drafts. This is a descriptive comparison across
different input presentation and trial times, not an isolated causal benchmark.
The original Opus10 task is different; its 112,326-token result is historical
evidence and is not a same-task baseline for EFF-04B.

## What still costs time and context

The positive Claude entry is 61,682 bytes: 20,069 canonical instruction bytes,
18,032 reference bytes, 5,490 fixture bytes, 13,379 bytes of selection/provenance/
labels/fences, and 4,712 task/host bytes. These are bytes, not token estimates.
The 7,139-byte full artifact-type catalog is much larger than the 588-byte
verification checklist. The complete fixture itself is a small part of the load.

Claude112 read the entry, read the already-included selection again, invoked the
setup skill, then performed its operations. The retained locator still requests
the selection read. Its observed client commands total only 8.351129 seconds of
252.974 native seconds. The remaining time is unclassified; these captures cannot
identify it all as provider, model or tool overhead. No private reasoning is
exposed or used as a measured timing explanation.

Bundling inputs reduces discovery calls but does not make all content necessary
or eliminate duplicate rendered results. The per-trial cost files in the check
archive retain visible result sizes, repeated reads and observed command timings.

## Codex delivery defect

Codex111 reports that its initial host read of the 63,272-byte entry was truncated.
The original command capture retains the full output; it does not prove that the
model received that full output. The attempted recovery through `read-text task.md`
failed because the helper permits inventoried inputs and work files, while this
entry is a root file. The agent disclosed the refusal and recovered applicable
instructions through permitted input files. No helper permission was broadened.

This is an entry transport/recovery defect. The approved session-only network
boundary probes passed. It is not evidence of a Node lock or a service network
failure. The prefer_mxc development warning is recorded separately from failed
calls. A correct final content result does not erase this delivery problem.

## KIS review and next correction

The change reuses the existing reader and client and removes per-file discovery
work. It also concentrates more content into a large entry and retains redundant
selection metadata. This is not an overall efficiency success merely because
the call count falls.

1. Make initial delivery and recovery use the same permitted, bounded source.
   Ensure the host receives every required byte without a truncated tool display.
   Remove the forced duplicate selection read while retaining exact identities.
2. Render common provenance once and use explicit relative paths from one known
   root. Keep exact source text and a complete identity index. Reduce duplicate
   result presentation without hiding findings or weakening evidence retention.
3. Make result reporting distinguish saved draft, template validation, agent
   content review and unperformed verification. Replace ambiguous readiness
   prose at its source; do not add a second review process or call every saved
   draft verified. Preserve actual refused calls and their recovery.
4. Split the canonical catalog and drafting procedure into addressable shared
   rules and type-specific sections. Select only applicable complete sections.
   Changes to released canonical instruction meaning or paths outside this work
   order require a separate bounded proposal; no such change is applied here.

Keep the two content cases and independent review. Do not add another warning
layer, orchestration framework or repeated variations without a concrete defect.
A changed candidate needs fresh comparisons; do not mix these repetitions into it.

## Technical checks and retained evidence

The focused native-support tests pass: 29. The complete source run reports 1,336
tests, 24 skips, exit zero. Distribution validation, CLI smoke, exact reproducible
builds, candidate installation and independent input/package comparisons pass.
Released validation reports 1,991 artifacts, zero errors and 63 existing warnings.
Scope and review preflight pass. Skips are retained as skips.

Candidate wheel SHA-256:
`6c924429203cb4976badcdbe6ca841cd3aa83ddac2a624a109091d97d5a786da`.
All 127 wheel member payloads match candidate15, while archive identities and
timestamps differ. Reuse of its EFF-02/03 results is bounded to those identical
runtime contents; it does not qualify this changed native delivery. The governor
remains public 0.22.1 outside the checkout. No candidate governs its own work.

Source-suite wall time was 175.202 seconds. Entry assembly takes about one third
of a second. Build/package commands and their actual logs are retained, but a
complete preparation elapsed total was not captured and is unavailable. It is
not counted as zero or hidden within a faster native-only claim.

The [check archive](candidate17-checks.zip) and [inventory](candidate17-checks-inventory.json)
retain actual commands, results, component identities, permission probes,
independent reads, failure records and cost measurements. Each trial has its own
evidence archive, visible transcript and inventory. Raw host events, credentials
and private reasoning are excluded; exact known test tokens were checked absent.
Original private capture digests remain in the inventories. Only owned test
containers were stopped after observation; their volumes remain available.

## Delivery and lifecycle

PR #543 stays draft against main. The complete comparison base remains
`55caaada508495bea7d97effd27644d1ce8373da`; WO-HAG-009/010/011 remain declared.
At prior remote head `08a3ad39ee3e349a2fefe24502575f5f082b7e26`, validate failed;
all other completed applicable checks passed, with release rehearsal legs skipped.
The known full-base blocker is WO-HAG-009 / QGP-G4I-EVIDENCE. The publication check
is retained separately and must preserve the actual new formal snapshot; no
evidence is fabricated or rebound to imply complete native qualification.
Read publication-head CI separately after the push.

Full VER-HAG-007 NQ-01 through NQ-05 remains incomplete. This report does not
qualify desktop, startup/compaction, real graph authority or production use.
The released evaluator selects PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK.
Continue the bounded delivery correction and required evidence before completion
or verification preparation. No verification record is prepared by this report.
