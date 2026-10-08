# Hosted drafting efficiency: changes and observed limits

The client and instruction changes reduce avoidable work. Native qualification
is still incomplete. None of the three Claude diagnostics passed content review,
and none met the three efficiency goals. WO-HAG-011 remains in progress; no
verification decision or successful efficiency claim is requested.

## What changed

| Problem | Implemented change | Observed limit |
| --- | --- | --- |
| Instruction length | Four skill entries fell from 34,825 to 3,504 bytes. Task references select hosted or repository work. Complete selected released sections can be read together. | Startup reduction is not total-context reduction. The required sections and native host context still cost tokens. |
| Duplicate content | Shared repository setup has one reference. Typed inputs use one command reference. Complete responses stay in evidence files, with exact document text or a file pointer. | Native agents still produce overlapping prose/JSON reports and sometimes reread results. |
| Tool calls | Typed import/open/create/revise/read remove manual envelope, base64 and wheel-digest work. Create can return its exact template in the same call. | Agents still choose every mutation. Fresh-project setup, instruction discovery and reporting require several turns. |
| Discovery failures | Resource IDs now match the public client; the earlier inventory prefix remains compatible. Windows Unicode survives the console/child-process boundary. | An agent can still supply an inapplicable typed field; the client must refuse it. |
| Truthful reporting | The native test helper exposes the existing mechanical observation summary, including recovered errors. | It cannot establish content quality. Codex's captured stream does not expose every orchestrated tool call or peak context. |
| Host portability | Codex can read bounded inventoried text through the same approved helper prefix when native Read is absent. The prefix is available before reading selection. | This is test-driver adaptation, not a new permission grant, installed-host update or automatic-delivery claim. |

Service endpoints, schemas, persistence, lifecycle policy and decision rights
are unchanged. The released 0.22.1 evaluator remains the real governor. Candidate
client 0.22.2 and plugin 0.2.7 are disposable test inputs.

## Native observations

These rows are development iterations, not three repetitions of one final
candidate. Claude used the same `claude-opus-4-6` model, task, fixture and normal
permissions. Import and draft creation are inside the measured session.

| Run | Seconds | Native calls | Peak input context | Independent result |
| --- | ---: | ---: | ---: | --- |
| Retained Opus10 reference | 673.180 | 56 | 112,326 | Content and failure-reporting failures |
| Claude 01 / `4905b0ae` | 418.181 | 42 | 70,537 | Content failure; four failed calls not fully reported |
| Claude 02 / `ebea7148` | 314.444 | 25 | 56,733 | Content failure; one failed instruction call omitted |
| Claude 03 / `e5f3a221` | 361.282 | 26 | 61,512 | Content failure; recovered read error correctly reported |
| Codex 01 / `e5f3a221` | 80.093 | Unavailable | Unavailable | Correct stop before authoring: test required unavailable native Read |
| Codex 02 / `456c84a7` | 443.352 | At least 32 observed tool items; exact total unavailable | Unavailable | Truthful incomplete draft; two recovered discovery failures reported |

Goals remain **under 180 seconds**, **at most 15 calls**, and **under 40,000 peak
input-context tokens**. All Claude runs missed all three. The shorter Codex stop
is not an efficiency success: it performed no hosted work. Codex 02 missed the
wall and call goals; its context goal is unavailable. No general model or
host ranking follows from these observations. Provider latency is unclassified.

In Claude 02, the six retained client/fixture command durations sum to 6.95
seconds of the 314.44-second session. This excludes instruction helpers, native
file tools and provider time; it does not establish where every remaining second
went. Model turns and reports remain material costs. Package preparation is
outside the native clock: candidate 03's build/capture intervals were about
348 seconds for reproducible client builds, 36 for service/plugin preparation,
9 for the disposable environment and 3 for installation. Exact command records
state the timestamp method and its limits.

## Content failure and task fit

Every Claude draft claimed that no formal definition records the greeting.
Imported `INT-P3-900` and `REQ-P3-900` already describe it. Source inspection of
`greeting.py` proves its source behavior, not the absence of engineering records.
The unsupported claim remains a failure even if the service admits the draft.

Each draft also turned a fixture assertion or verification activity into an
operational success measure. The released intent template explicitly places
those checks in a verification contract. The task requests confirmation of a
function return but insists on a new intent. This is a poor positive case for
that template. Missing inputs should be reported honestly; the mismatch does
not excuse fabricated content or false completion claims.

The later guidance moved these existing claim checks before submission and
shortened the drafting reference. The third Claude run still failed them.
Adding more repetitions of the same warning has not demonstrated a solution.

Codex 02 independently read the existing intent, avoided the false absence claim,
and left the missing operational measure unresolved. Its final report accurately
distinguishes mechanical admission from content completeness. The independent
service read matches the submitted bytes. This is useful evidence of truthful
handling, not a completed positive authoring case or general host qualification.

Two discovery failures remained. The agent guessed `#int` instead of `#intent`.
The returned `CONTINUE.md#continue-selected-work` matched both a title and a
nested heading, so the section reader correctly refused ambiguity. Full-file
fallbacks added context. Communication guidance arrived after first commentary;
the run reports that limitation. The current scope does not permit editing the
released resource's headings or silently choosing an ambiguous section.

## Checks and evidence

- Last full source suite: 1,334 tests reported, 24 skips, exit 0. The final
  candidate changes only test support relative to candidate 04; exact product,
  service and plugin bytes match. This is disclosed reuse, not a new full run.
- Latest focused native-helper boundary suite: 19 tests, exit 0.
- Distribution checks and CLI smoke passed. Exact reproducible candidate builds
  and installed disposable packages are retained.
- Real installed-client tests compare typed requests with independent raw
  requests for all five operations. Exact UTF-8/CRLF bytes survive create,
  revise and independent readback.
- Stale versions and changed bytes under a reused key were refused. Deliberate
  lost replies and post-commit local capture failures stayed unknown until their
  original receipts were recovered. Exact retries did not duplicate mutations.
- Real Windows multi-section reads preserve the canonical released text and
  provenance under a forced legacy console encoding.
- Every Claude saved document and the Codex 02 document match independent service reads. Staged inputs
  remained unchanged. These facts do not establish writing quality.

Historical results are preserved. Visible transcripts exclude private reasoning
and host/system messages. Archive inventories describe those omissions and
credential checks. Raw private event streams remain outside the repository.
Original incorrect native reports are retained alongside independent assessments.

## KIS assessment and proposed next decision

The useful simplification is to move mechanical representation into the existing
client and keep one owner for each instruction. The additional code addresses
real input, byte-fidelity, discovery and uncertain-write failures. It adds no
service, workflow engine, dependency, lifecycle gate or approval framework.

The whole task is still too expensive, and successful transport still allows bad
prose. A smaller startup file is therefore insufficient evidence of success.

Proposed next change, **not applied or approved by this report**:

1. Use a verification artifact for the positive greeting-confirmation case,
   matching the actual request and reusing the imported requirement. Supply no
   completed artifact or hidden workflow to the agent.
2. Retain the original intent request as a negative/ambiguity case. Expected
   behavior is to disclose the task/template gap, preserve existing records and
   avoid invented outcomes or absence claims.
3. Keep correctness checks, normal permissions and the three efficiency goals.
   Establish comparable observations for the revised positive task; do not treat
   its timing as the same-task Opus10 comparison.
4. Amend the approved SPEC-HAG-008 / VER-HAG-008 test definition explicitly,
   preserving and linking their accepted versions. Only then run the amended
   qualification and its required repetitions. This proposal accepts no failed
   result and changes no product artifact template or lifecycle rule.

Further reductions should remove required reading/report duplication and
unnecessary round trips at their actual owner, with measured results. They should
not be pursued by quietly omitting required instructions or calling an incomplete
run a pass. WO-HAG-009/010's full NQ qualification remains separate and incomplete.

## Review status and evidence links

Tested/package candidate: `456c84a7dcb3a11cd564899da01848f39dc53575`.
Selected released governor: 0.22.1. Fresh validation reports 1,991 artifacts,
zero errors and 63 existing warnings. Review preflight and the WO-HAG-011
implementation-delta scope check pass. Neither completes handoff or verification.
The complete PR comparison retains base `55caaada508495bea7d97effd27644d1ce8373da`
and all three work orders. The draft PR discloses the remaining evidence gate.

- [Claude 01 visible transcript](claude-01-visible.md), [archive inventory](claude-01-inventory.json).
- [Claude 02 visible transcript](claude-02-visible.md), [archive inventory](claude-02-inventory.json).
- [Claude 03 visible transcript](claude-03-visible.md), [archive inventory](claude-03-inventory.json).
- [Codex 01 visible transcript](codex-01-visible.md), [archive inventory](codex-01-inventory.json).
- [Codex 02 visible transcript](codex-02-visible.md), [archive inventory](codex-02-inventory.json).
- [Final build, focused checks and independent readback inventory](candidate05-checks-inventory.json).
- [Candidate 04 installed-client checks](installed-candidate04-inventory.json).
- [Earlier installed-client checks](installed-client-inventory.json).

Each native archive contains its independent assessment, exact command records,
metrics and original native report. The report can be wrong; the independent
assessment records the discrepancy. No verification record has been prepared.
WO-HAG-009, WO-HAG-010 and WO-HAG-011 remain in progress. No approval of an
amendment, release, host update, risk acceptance or merge is inferred.
