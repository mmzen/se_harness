# Hosted draft content review and procedure simplification

WO-HAG-011 remains **in_progress**. Candidate `4ce7ffd09d0b991d29311a1164b1fa029a64a83e` has a Claude
missing-input result of **fail** and **3/3** passing Claude verification
contracts. Required Codex content cases remain pending because its normal Windows
sandbox cannot launch shell commands. This report grants no verification or merge.

| Original issue | Current result |
| --- | --- |
| Unsupported gap and success claims in the intent | **Unresolved**: the latest run acknowledges missing inputs but still makes an unsupported completion claim. |
| Vague verification evidence destination | **Pass in 3/3 fresh Claude trials**: each names a work order and a concrete filename. |
| Additional assertion inconsistency found during this correction | **Pass in 3/3 fresh Claude trials**: each check matches its stated pass condition. |

## Changes

The product change is confined to `plugins/verity-plane/common/skills/change/references/hosted-drafts.md`. The procedure now has three sections:
read selected instructions once, prepare and review one draft, and retain the result.
It replaces overlapping checks with one input table and one finished-content review.
The report is also the progress note; no second inventory or model-written metrics
report is needed.

- Check existing definitions before claiming a gap. A source file or same-type record
  cannot show that no requirement or verification contract exists.
- Ask for missing purpose or success measures before dependent writing. A requested
  artifact type supplies neither missing content nor a checklist waiver. Report
  unresolved required content as incomplete even when service admission succeeds.
- A verification plan names its check, pass condition and complete proposed evidence
  path, including filename. Review each assertion against its stated pass condition
  and remove duplicate checks or unsupported constraints.

The guide changed from 938 to 888 words
(5.3% shorter), and from
6,605 to 6,253 bytes. This modest source reduction is not a
claim of equivalent context or latency savings. Task text, canonical instructions,
fixtures, model, permissions and runtime behavior remain unchanged in this correction.

## Native results

Each attempt uses Claude Code 2.1.273 / claude-opus-4-6 on Windows, a fresh
private project, installed client and packaged plugin.
The original missing-input task remains unchanged. The alternative verification task
is the exact approved EFF-04B request. No finished answer or operation sequence was
inserted. A different candidate starts a new comparison; earlier passes are not
combined with the latest repetitions.

| Trial | Candidate | Case | Content review | Seconds | Calls | Peak input tokens |
| --- | --- | --- | --- | ---: | ---: | ---: |
| claude-41 | 602c92b8 | EFF-04A | **fail** | 249.818 | 18 | 54,871 |
| claude-51 | 28002f31 | EFF-04A | **pass** | 256.692 | 17 | 54,485 |
| claude-52 | 28002f31 | EFF-04B | **pass** | 242.678 | 21 | 57,704 |
| claude-53 | 28002f31 | EFF-04B | **pass** | 210.583 | 21 | 55,149 |
| claude-54 | 28002f31 | EFF-04B | **fail** | 205.054 | 21 | 53,936 |
| claude-61 | 2fe17dae | EFF-04A | **fail** | 262.508 | 20 | 55,581 |
| claude-71 | 4ce7ffd0 | EFF-04A | **fail** | 257.193 | 20 | 60,483 |
| claude-72 | 4ce7ffd0 | EFF-04B | **pass** | 252.101 | 24 | 60,090 |
| claude-73 | 4ce7ffd0 | EFF-04B | **pass** | 240.323 | 21 | 56,782 |
| claude-74 | 4ce7ffd0 | EFF-04B | **pass** | 258.318 | 23 | 58,055 |

The initial shortened procedure still allowed invented coverage in claude-41.
Moving the review before creation improved the two original findings in trials
51–53, but trial 54 added an incorrect type assertion. Trial 61 then acknowledged
a purpose/measure gap while calling the draft complete. All failures remain visible.
The final revision explicitly requires unresolved content to remain incomplete
and retains the assertion review. The latest negative run still failed that rule. Service admission is never used as the content verdict.

The assertion counterexample and a correction to its original illustrative label
are retained in [candidate 12 checks](candidate12-checks.zip). Historical evidence
was preserved; the mislabeled expression was not silently rewritten.

## Duration and context

Latest comparable EFF-04B measurements:

| Measurement | Full range | Median | Goal |
| --- | ---: | ---: | --- |
| Duration (seconds) | 240.323–258.318 | 252.101 | < 180 |
| Tool calls | 21–24 | 23 | <= 15 |
| Peak input tokens | 56782–60090 | 58055 | < 40,000 |

Compared with the [previous concise procedure](concise-qualification-assessment.md),
the positive medians increased from 209.797 to 252.101 seconds, from 22 to 23 calls,
and from 56,820 to 58,055 tokens. The measured correction has no efficiency win.
The small samples and varying provider latency do not establish which change caused
the increase. All three latest trials missed every efficiency goal.

See each goal outcome and exact capture in `content-native-metrics.json` inside
[candidate 13 checks](candidate13-checks.zip). Report missed goals separately from
content quality. Missing-input refusal costs are not successful-authoring speed.
These three observations are not a general benchmark; provider latency varies.

The existing file-pointer delivery avoids repeating the complete task at startup.
The selected canonical sections and file identities remain exact. A pointer does
not establish reading. Initial host context, calls, read paths, command timings and
provider peak context are retained. Source bytes and provider tokens are different
measurements. Do not infer token savings from a shorter guide.

## Checks and evidence limits

The latest source suite completed 1,335 tests with 24 skips (exit 0). The 23 driver
checks, distribution validation and CLI smoke check passed. Released validation
reported 1,991 artifacts, zero errors and 63 existing warnings.

The check archives retain exact commands, working directories, exits and timings,
source and driver tests, distribution checks, CLI smoke, released validation,
review preflight, scope checks, reproducible builds, package installs, component
identities and independent service reads. The latest package has client 0.22.2
and plugin 0.2.7. The governor remains released 0.22.1 in its separate environment.

[Candidate 10 checks](candidate10-checks.zip), [candidate 11 checks](candidate11-checks.zip),
[candidate 12 checks](candidate12-checks.zip), [candidate 13 checks](candidate13-checks.zip).
Each archive has a matching `candidateNN-checks-inventory.json` with file digests.

Imported records were separately read and compared; staged inputs were unchanged.
Owned qualification containers were stopped after inspection, with volumes preserved.
Prior service and EFF-02/03 evidence is reused only for the exact unchanged runtime
and dependencies identified in the component review. New native behavior is assessed
separately. Source tests do not establish native content quality.

Private reasoning, raw provider streams, credentials and package binaries are omitted
from published transcripts. Inventories record omissions and hashes. Actual visible
failures and rejected calls remain in the evidence. No fixture test is claimed to
have run merely because a native agent wrote a verification plan.

## Simplicity assessment and remaining work

One procedure and one report remove duplicate review instructions and bookkeeping.
The native agent still makes separate selection, instruction, fixture and component
reads before service operations. Shorter prose alone does not establish acceptable
latency or reduce the required discovery calls. Further consolidation should reuse
existing read-only discovery and mechanical capture, preserve source identities and
leave semantic drafting and decisions with the actor. It needs its own measured
comparison, not another untested claim of savings.

Codex authentication was live, but its normal shell failed before file access with
`helper_unknown_error`. Four previously authorized stale Node workers were stopped;
the active Codex app, backend, remote connection and protected helper were preserved.
No sandbox bypass or further process termination was used for qualification.

Full NQ-01 through NQ-05 for WO-HAG-009/010 remain incomplete. The focused tests do
not qualify desktop, automatic compaction, production access controls, release or
adoption. No ready VREC, completion transition or verification request is made here.

The fresh selected result keeps WO-HAG-011 at `PROC-WO-IMPLEMENT` /
`STEP-WO-IMPLEMENT-CHECK`: run the handoff checkpoint with the required actual evidence.
It is not permission to report failed or pending qualification as complete.
PR #543 stays draft, source `codex/hosted-agent-qualification`, target `main`.
Its known full-PR blocker is WO-HAG-009 / `QGP-G4I-EVIDENCE`; the publication checks
retain the fresh result and the trusted complete comparison base.

## Bounded follow-up proposal

The unresolved intent case needs a change to the way authoring results are
presented. The observed failure is specific: the report uses zero incomplete
fields as a completion claim, even beside an acknowledged content gap.

1. Make the compact client result label the evaluator observation as template/shape
   validation, with content review explicitly unassessed. Preserve the full original
   response and every mapped field; add no machine claim of semantic approval.
2. Use one report with separate saved-draft and content-review outcomes. Unresolved
   required content must remain visible in the final result. No second review
   artifact or extra approval is proposed.
3. Rerun the unchanged missing-input case before spending another full positive
   repetition set. Keep existing failed runs and the accepted criterion unchanged.

This is a proposal for review, not an implemented fix or a changed verification
contract. The present prose-only corrections have not reliably solved the defect.

For duration, first measure the remaining discovery and reporting calls, then
consolidate only independent read-only inputs through existing capabilities. Also
review whether plugin-only guidance changes can reuse an already qualified client
runtime while rebuilding the plugin. The current exact-build contract was followed;
any change to its candidate/component binding needs explicit review before use.
The latest client replay alone took about 6 minutes 38 seconds between retained
start timestamps; package preparation took another 35 seconds. These preparation
costs are separate from native drafting measurements.

## Independent content findings

### claude-41

- The draft claims that no formal record establishes the expected greeting value or a way to confirm it. Existing REQ-P3-900 and VER-P3-900 contradict that claim; reading source code and INT-P3-900 does not establish their absence.
- The success measure is exact return-value agreement, an implementation acceptance check. The report identifies no missing operational measure and calls the draft complete.
- All admitted document bytes match a separate service read. All seven imported records and staged inputs are unchanged. No failed or denied native calls were observed.

Saved document SHA-256: `d7ed59cc4fc7e758f1fa5ea9e04e8da4c7f059cf18372ba3fba7106eb4c8e2a9`.

[Visible calls and replies](claude-41-visible.md), [evidence](claude-41-evidence.zip), [inventory](claude-41-inventory.json).

### claude-51

- The final report identifies the outcome as verification, not an operational benefit, and states that the measure does not identify an operational benefit. These remain unresolved content findings despite admission.
- The report acknowledges existing INT-P3-900 and possible overlapping coverage. The draft no longer claims that a behavior definition or verification contract is absent.
- The native result reports a prepared draft and content findings, not completed positive authoring. EFF-04A permits retention of one semantically incomplete draft. No operational benefit or accepted operational success measure is claimed.
- Independent service readback matches the submitted bytes. All seven imported records and staged inputs are unchanged. No failed or denied calls were observed.

Saved document SHA-256: `5a874eaa7df9e23bc5e542f5d3a4262406eb1bc161d84721d507582f3221ec89`.

[Visible calls and replies](claude-51-visible.md), [evidence](claude-51-evidence.zip), [inventory](claude-51-inventory.json).

### claude-52

- Draft VER-P3-901 verifies REQ-P3-900 and derives the exact expected string from the requirement and specification. Its matrix, import/call/equality steps and pass condition form a usable check.
- The concrete planned file is docs/engineering/lifecycle-pilot/evidence/WO-P3-900/ver-p3-901-result.json, retaining actual/expected values, comparison, Python version and timestamp.
- No empty optional template headings remain. The report explicitly states no tests ran and no lifecycle decisions occurred.
- Independent readback matches the submitted bytes; all seven imported records and staged inputs are unchanged. No native failed or denied calls were observed.

Saved document SHA-256: `e9f8ab87ac6c88fefc9e193fb034810a95aa36818f59afd80ecf5b66b4ebad84`.

[Visible calls and replies](claude-52-visible.md), [evidence](claude-52-evidence.zip), [inventory](claude-52-inventory.json).

### claude-53

- Draft VER-P3-901 links REQ-P3-900, derives the expected string independently, and defines a matrix plus import/call/equality scenario with platform and evaluator named.
- The exact proposed destination docs/engineering/lifecycle-pilot/evidence/WO-P3-900/ver-p3-901-assertion.json includes a selected directory and filename, with actual/expected values, pass/fail and timestamp.
- Optional empty headings are omitted. The report explicitly identifies a planned check, no executed test and no verification record or lifecycle decision.
- Independent service readback matches submitted bytes; all seven imported records and staged inputs are unchanged; no native failures or denials were observed.

Saved document SHA-256: `5475ee92a18f6f105051b23f6d0b6628d9b4c42a0c4614bccfe179e3886fc429`.

[Visible calls and replies](claude-53-visible.md), [evidence](claude-53-evidence.zip), [inventory](claude-53-inventory.json).

### claude-54

- The draft correctly links REQ-P3-900, derives an expected value independently, names a complete evidence path and reports planned checks without claiming execution.
- Acceptance scenario 2 says isinstance(greeting(), str) establishes str but not a subclass. That expression accepts str subclasses; the proposed assertion and stated pass condition disagree. Excluding subclasses also introduces a restriction absent from the governing requirement.
- The mismatch fails the usable-check/pass-condition content review. Zero admission errors do not establish this semantic correctness.
- Independent readback matches submitted bytes; all seven imported records and staged inputs are unchanged. No native failures or denials were observed.

Saved document SHA-256: `f9dde5cd247d0a75ad7372cfa3cd7befa95543c075d350b137769fc467fe900b`.

[Visible calls and replies](claude-54-visible.md), [evidence](claude-54-evidence.zip), [inventory](claude-54-inventory.json).

### claude-61

- Reads the existing INT, REQ, SPEC and VER, and reports overlap rather than inventing missing definitions.
- Still submits verification of the greeting output as an intent success measure without an agreed operational benefit or measure.
- The native report explicitly acknowledges the purpose-and-measure problem, but treats the requested artifact as sufficient reason to proceed.
- Both native report and final response call the intent complete. The approved negative case expressly fails that claim.

Saved document SHA-256: `3e116af211b9395dd5af4f88ce737fdd8c95cbf44a4ea80383c32d4b6a8749ba`.

[Visible calls and replies](claude-61-visible.md), [evidence](claude-61-evidence.zip), [inventory](claude-61-inventory.json).

### claude-71

- The report acknowledges INT-P3-900 and identifies the lack of a supplied operational benefit and measure.
- The saved Problem nevertheless says there is no recorded agreement without an explicit intent, despite the imported intent and governing definitions. This repeats the unsupported absence claim.
- The success measure substitutes agreement recorded in this intent for an agreed operational measure.
- The final reply and report explicitly call the draft complete while listing two unresolved required content findings. This fails EFF-04A despite successful service admission and the new explicit instruction.

Saved document SHA-256: `f54288a3a211aba1c6435d18a3c325449413ab8b0b0181b139bd476db52aa763`.

[Visible calls and replies](claude-71-visible.md), [evidence](claude-71-evidence.zip), [inventory](claude-71-inventory.json).

### claude-72

- VER-P3-901 remains draft, links REQ-P3-900 and derives the fixed expected string from the requirement, independently of candidate output.
- The matrix and scenario specify import, call and exact equality. No erroneous subclass assertion or empty optional headings remain.
- The proposed path docs/engineering/lifecycle-pilot/evidence/WO-P3-900/ver-p3-901-assertion.json includes work order and filename; required recorded values are named.
- The report clearly distinguishes source inspection and planned verification from executed tests.
- One create call failed HAG_REMOTE_UNKNOWN_IDENTITY because a project identity was supplied as the context before draft-open. The agent retained the failure and recovered through a real draft context; this did not change the content verdict.

Saved document SHA-256: `24bc9ea3b698a11329683c221531bfa693a540c87c197f2384cb6af7f56f92c3`.

[Visible calls and replies](claude-72-visible.md), [evidence](claude-72-evidence.zip), [inventory](claude-72-inventory.json).

### claude-73

- VER-P3-901 remains draft and links REQ-P3-900; the expected string comes from its acceptance criterion.
- One import/call/exact-equality check and a complete matrix cover the requested behavior, with no unsupported subclass condition or empty optional headings.
- The concrete proposed file is docs/engineering/lifecycle-pilot/evidence/WO-P3-900/ver-p3-901-result.json, with actual/expected value, outcome and timestamp.
- The report acknowledges the existing alternative verification contract, identifies the retention file as unpopulated and explicitly says no tests ran.
- No native failed or denied calls were observed.

Saved document SHA-256: `d1a4708d98bfeb87ad4e894fd7d3309ca89326df9ba5f4dea39a1d7c14dd66c5`.

[Visible calls and replies](claude-73-visible.md), [evidence](claude-73-evidence.zip), [inventory](claude-73-inventory.json).

### claude-74

- VER-P3-901 remains draft, verifies REQ-P3-900 and derives the fixed expected string from the governing definitions.
- Matrix and acceptance scenario define import, call and exact equality; wrong value, exception and missing function are meaningful failures of that check.
- The concrete proposed evidence file is docs/engineering/lifecycle-pilot/evidence/WO-P3-900/alternative-greeting-assertion.json, with actual/expected value, outcome and timestamp.
- There are no empty optional headings. Residual uncertainty and the report explicitly distinguish the planned check from future execution; no test execution or verification acceptance is claimed.
- No native failed or denied calls were observed.

Saved document SHA-256: `509f5d11dfb14779676dd31d323f7a9b01c0bfb4fadfe204afca3802dc7876f7`.

[Visible calls and replies](claude-74-visible.md), [evidence](claude-74-evidence.zip), [inventory](claude-74-inventory.json).
