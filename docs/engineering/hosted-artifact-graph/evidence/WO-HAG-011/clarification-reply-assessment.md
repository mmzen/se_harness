# Clarification reply and draft-creation assessment

The clarification correction works for Claude. All three Claude draft-creation
attempts also pass independent content review. The context target remains missed.
Codex's clarification content is correct, but its report cannot be qualified from
incomplete call capture. Its positive-case result is **pass**;
the separate assessment records the evidence and limits.

Candidate: `89946ef270cd75c26478a166cd56377eeafb3791`. Work: `WO-HAG-011`.
Contract: `VER-HAG-008`, with the already approved
[clarification-report amendment](clarification-contract-20261010/activation.json).

## Change and scope

The [one-file correction](clarification-reply-review.md) moves the existing
clarification report duty next to the stop instruction. It proposes three short
parts: Actions, Known inputs and Questions. These are writing aids, not literal
pass criteria. The later report section points back instead of repeating the rule.
The guide grows from 1,057 to 1,075 words. No task, acceptance criterion, permission,
dependency, formal definition or service behavior changed. Earlier results remain
unchanged, including the failed candidate23 trial.

## Observed results

| Trial | Case | Independent result | Native duration | Tool calls | Peak input tokens |
| --- | --- | --- | ---: | ---: | ---: |
| `claude-181` | Clarification | pass | 120.315 s | 4 | 34,919 |
| `codex-181` | Clarification | not_qualified | 43.395 s | at least 5 | unavailable |
| `claude-182` | Draft creation | pass | 205.812 s | 14 | 62,154 |
| `claude-183` | Draft creation | pass | 172.979 s | 9 | 52,416 |
| `claude-184` | Draft creation | pass | 161.600 s | 13 | 60,763 |
| `codex-182` | Draft creation | pass | 172.958 s | at least 14 | unavailable |

Claude used Code 2.1.273 and claude-opus-4-6. The three positive attempts used the
same candidate, request, model, input bytes and permissions, each with a fresh
project. Codex's exact CLI invocation is retained in its evidence archive.
Its visible item counts are lower bounds; complete counts, model turns and peak
input context remain unavailable. Cumulative provider usage is not substituted
for peak context. Preparation and assessment are outside native timing.

Claude positive ranges: **161.600–205.812 seconds**, **9–14 calls**, and
**52,416–62,154 peak input tokens**. Medians: **172.979 seconds**,
**13 calls**, **60,763 tokens**.
Two of three meet the under-180-second goal; all three meet the at-most-15-call
goal; none meets the under-40,000-token goal. Correct clarification is reported
separately from successful draft creation.

## Content and reporting

The Claude clarification reply asks for the new audience, its problem, the desired
improvement and how the owner will know it helped. It explicitly reports that no
hosted change was attempted. Complete call capture and independent service state
support this statement. No duplicate report file is required for that eligible
branch. No artifact was created or imported; project version stays zero.

The three Claude verification drafts link to REQ-P3-900 and derive the expected
`Hello rehearsal` string from the governing definitions. Each supplies a usable
exact-equality check, a pass condition, platform/evaluator and a concrete proposed
evidence destination. Each remains draft. Native reports and final replies say
that the checks are planned and no tests ran. Service admission and authoring
review are reported separately. No observed native failures were concealed.
Independent readbacks match the submitted bytes. All seven imported historical
records match their original Git blobs in each positive trial.

Codex's clarification reply asks the right questions and states no mutation was
attempted. Its recorded commands succeed and the independent project version is
zero. However, CLI JSON omits some orchestrated calls. The final-reply-only branch
requires complete attempted-call evidence, including refusals. The unchanged
project and the agent's statement cannot supply that evidence. The required
fallback saved report is absent, so this case is **not qualified**. No hidden
mutation or denial is asserted. Codex host diagnostics, including an after-agent
notification failure from Windows path length, are retained separately in its
assessment. No global setting or permission was changed to suppress them.

## Context and duration costs

Each Claude positive task contains 63,550 bytes before host overhead: 20,069 bytes
of selected canonical instructions, 19,916 of references, 5,490 of fixture content,
13,481 of selection/provenance/labels, and 4,594 of remaining task text. This is
still a large entry for one small artifact.

Two positive runs reread the supplied hosted guide (8,151 visible result characters)
and procedure sections (about 6,900–7,300 characters). Even the run without these
rereads receives about 7,450 characters from draft-open and 7,190 from create.
These are measured output sizes, not token estimates. The command-cost records
retain each result size. Client execution totals about seven seconds per Claude
positive run; the remaining provider time is unclassified, not measured model time.

The exact build, package preparation and disposable client installation took
**496.206 seconds** (about 8 min 16 s).
Source checks ran during preparation. Native runs were sequential; the idle Codex
sandbox was prepared during the final Claude repeat. These costs are separate
from native duration and do not include editing, assessment or publication.

## Supporting checks

- 31 native-support tests pass. The source suite ran 1,336 tests with 24 skips,
  exit 0. Distribution checks and CLI smoke pass.
- Released validation: 1,991 artifacts, zero errors, 63 warnings. Selected scope
  and review preflight pass. These do not prove native qualification.
- Two pinned builds produce identical archives. Both packaged guidance variants,
  selected released sections and all 12 fixture files match exact source bytes.
- All 127 runtime wheel member payloads match candidate15. Server/runtime source,
  dependencies and build inputs are unchanged. Reused runtime evidence does not
  qualify this new instruction route.
- Both Codex session-only boundary probes pass: workspace write and selected
  service access succeed; outside write and external access fail as expected.
  The approved MXC boundary may expose other localhost services; it is not
  port-level isolation. Live no-tools authentication probes pass.

Wheel SHA-256: `d5c25f758a5f2ead36dff9063ef5ded56a96717fed0bca30fdf45ea3a06834e2`.
Sdist SHA-256: `d97a635fad1b944f769d597165cf08959651f23e15959c3cf42d7e0c2f4f9ad2`.
Candidate client 0.22.2; packaged plugin 0.2.7; released governor 0.22.1.
No actual host installation was changed. Owned trial containers are stopped and
their volumes preserved. Exact commands/results, component identities and
independent baseline reads are in [check records](candidate24-checks.zip) and the
[inventory](candidate24-checks-inventory.json).

## Evidence

- `claude-181`: [assessment](claude-181-assessment.json), [visible transcript](claude-181-visible.md), [evidence](claude-181-evidence.zip), [inventory](claude-181-inventory.json).
- `codex-181`: [assessment](codex-181-assessment.json), [visible transcript](codex-181-visible.md), [evidence](codex-181-evidence.zip), [inventory](codex-181-inventory.json).
- `claude-182`: [assessment](claude-182-assessment.json), [visible transcript](claude-182-visible.md), [evidence](claude-182-evidence.zip), [inventory](claude-182-inventory.json).
- `claude-183`: [assessment](claude-183-assessment.json), [visible transcript](claude-183-visible.md), [evidence](claude-183-evidence.zip), [inventory](claude-183-inventory.json).
- `claude-184`: [assessment](claude-184-assessment.json), [visible transcript](claude-184-visible.md), [evidence](claude-184-evidence.zip), [inventory](claude-184-inventory.json).
- `codex-182`: [assessment](codex-182-assessment.json), [visible transcript](codex-182-visible.md), [evidence](codex-182-evidence.zip), [inventory](codex-182-inventory.json).

Published transcripts omit private reasoning, credentials and raw host/system
events. Original local captures remain unchanged; their digests identify them.
Visible calls, saved reports, exact input snapshots and independent assessments
remain inspectable. An assessor script initially missed extensionless command
records; it was corrected to inspect all bounded work files before the positive
verdicts. Original native results were not changed.

## Next bounded focus

1. Make the existing fallback explicit when a host reports incomplete call
   capture: retain the normal saved report. Do not relax the no-attempt proof rule.
2. Reduce repeated instruction loading and large routine result summaries while
   preserving full evidence files and precise pointers. Use the observed sizes to
   select changes; do not add another layer of prose or merge unrelated commands.
3. Requalify affected cases on one exact candidate. Keep this run's successful
   content results and missed efficiency goals unchanged.

WO-HAG-011 remains `in_progress`. The released next step is
`PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK`, bound to
`harnessctl check REPO --artifact WO-HAG-011 --checkpoint handoff`.
This report does not complete or verify the work. Full WO-HAG-009/010 qualification
is also unfinished. Draft PR #543 retains target `main` and its disclosed
WO-HAG-009 handoff-evidence blocker; no evidence is rebound to hide that gap.
