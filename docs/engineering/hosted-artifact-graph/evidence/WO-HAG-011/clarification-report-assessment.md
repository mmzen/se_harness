# Clarification-report qualification assessment

**Result: the missing-input content now passes; the trial still fails one report
requirement.** Claude asks what should change for the user and how the owner will
know it helped. It stops before any mutation. Its final reply omits the required
statement that no hosted change was attempted. No later native case was run.

Candidate: `7949619680cfb6801716770fa04b69032eb0fb8f`. Selected work: `WO-HAG-011`.
Case: `VER-HAG-008 EFF-04A2`, trial `claude-171`.

## Applied amendment

mmzen approved the [exact proposal](clarification-contract-20261010/review.md)
with “I approve.” The [activation record](clarification-contract-20261010/activation.json)
binds all five reviewed file digests to that decision. The three formal records
retain their states and lifecycle history. Accepted versions remain preserved.

The captured final reply now serves as the report for a clarification-only stop
before any hosted mutation attempt. A refused mutation still requires the saved
report. The guide and task implement that branch. The guide makes the existing
user-outcome and success-measure questions explicit. No command, helper option,
dependency, permission or service behavior changed. Earlier verdicts are unchanged.

## Independent result

| Assessed condition | Result |
| --- | --- |
| Recognize existing definitions and missing agreed user outcome/measure | Pass. The reply names the -900 definitions, asks both missing questions and labels its proposed outcome incomplete. |
| Avoid inventing audience, benefit, measure or missing prior work | Pass. No unsupported completed definition or complete-content claim. |
| Eligibility for the captured-reply report | Pass. Complete captured calls and final reply; only one setup-file read and one service-status call. No mutation attempted. |
| Required no-attempt statement in the report | **Fail.** The reply does not state that no hosted change was attempted. |
| Source preservation and actual service state | Pass. Inputs unchanged; independent final project version is 0; no imports, draft context or new artifact. |
| Failed/denied calls and uncertain effects | None observed. No false zero-failure claim. |

Saying clarification is needed before drafting does not report whether an import
or draft-context mutation was attempted. The independent no-mutation evidence is
retained, but it does not supply the missing user-facing report statement. The
absence of `native-report.md` is **not** a failure under this amended contract.
No exact phrase is required; an unambiguous statement of the actual effects is.

Two further usability observations are recorded without creating new pass criteria:
question 5 reopens the immutable-record and fixture constraints already stated by
the task, and question 3 introduces implementation alternatives before the user
outcome is confirmed. Neither observation means that a prohibited write occurred.

The [assessment](claude-171-assessment.json), [visible transcript](claude-171-visible.md),
[native evidence](claude-171-evidence.zip) and [inventory](claude-171-inventory.json)
retain the actual result. The capture contains both tool requests and matching
successful results. Independent status confirms version 0. All 12 staged source
files and seven formal source records match exact Git blobs; none was imported.
A saved-revision read is not applicable because no document was saved.

## Cost and checks

| Observation | Previous A2: claude-161 | Current A2: claude-171 |
| --- | ---: | ---: |
| Native wall time | 106.925 s | 85.993 s |
| Tool calls | 4 | 2 |
| Model turns | 3 | 2 |
| Initial input context | 28,900 tokens | 29,081 tokens |
| Peak input context | 37,770 tokens | 32,737 tokens |
| Delivered task | 45,982 bytes | 46,787 bytes |

Both use Claude Code 2.1.273, claude-opus-4-6, the same A2 requested outcome,
original fixture, five initial canonical sections and permission configuration.
Guidance, reporting obligation and candidate differ. This is one observation per
candidate, not a reliability benchmark or equivalent successful-authoring comparison.
All three numeric thresholds are met for this negative case; EFF-04B remains pending.

The guide grows from 986 to 1,057 words and the task from 383 to 390 words.
Initial canonical content remains 4,989 bytes. Total selected references are
19,779 bytes, fixture 5,490, selection/provenance 12,324 and remaining task 4,205.
The initial entry grew; lower peak context came with fewer observed reads/calls.
Captured client execution took 0.526 s; remaining provider time is unclassified.

Exact build, package preparation and client installation took **439.217 s**
(7 min 19 s), separately from native execution. Source tests ran during preparation;
all finished before native timing began. Editing, review and reporting time is not
included in either measure. End-to-end work still costs more than the native run.

- 31 focused native-support tests pass.
- Source suite: 1,336 tests, 24 skips, exit 0. Distribution and CLI smoke checks pass.
- Released validation: 1,991 artifacts, zero errors, 63 warnings. Scope and review
  preflight pass; these do not establish native qualification.
- Two pinned builds produce identical archives. Both packaged guidance variants
  match the candidate. All delivered canonical sections and fixture bytes match.
- All 127 runtime wheel member payloads match candidate15. Server/runtime source,
  dependencies and build inputs match. Reused EFF-02/03 evidence covers unchanged
  runtime behavior only; it does not qualify the new instruction route.

Wheel SHA-256: `cab120f3789a85d7f670aeb5ebe185bb810183a6b412c42cd065b236af784562`.
Sdist SHA-256: `7bad529747006119b626561a7521bb2c21c21e31beb4bac5060dfeaecbab492b`.
Candidate client: 0.22.2; packaged plugin: 0.2.7; released governor: 0.22.1.
No host installation changed. [Check records](candidate23-checks.zip) and their
[inventory](candidate23-checks-inventory.json) retain commands, results and identities.

## Remaining work

The approved first-Claude stop rule applies. Codex A2 and all positive cases on
this candidate remain unperformed. The two owned trial containers are stopped;
their volumes remain available. No work completion or verification is claimed.

The next correction should make the clarification reply itself easy to complete:
show the fixed constraints, ask only unanswered questions, and report actual change
attempts. This can replace the current report paragraph with a shorter reply
structure. It needs no new criterion, report file or automatic grader. Review the
exact wording before another variation; no such correction is applied here.

WO-HAG-011 remains `in_progress`. The released next step is
`PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK`, with bound command
`harnessctl check REPO --artifact WO-HAG-011 --checkpoint handoff`.
The reporting failure remains unresolved. Full WO-HAG-009/010 qualification is
separate and unfinished; draft PR #543 keeps its main target and disclosed blockers.
