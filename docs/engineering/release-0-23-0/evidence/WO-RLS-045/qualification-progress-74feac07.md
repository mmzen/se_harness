# Content-readiness correction: qualification result

**Claude still fails the required content review. The release is not ready for
verification or merge.** Candidate `74feac0767f33658b31fb9e9ad2b6a13a188c13c` contains the exact WO-RLS-050 edit and
approved REL-SEH-036 membership amendment. Both are applied; all work orders
remain in progress. Prior failed candidates and accepted versions are preserved.

## What happened

The guide now uses one readiness table and removes repeated wording. Its exact
reviewed bytes were packaged and delivered: SHA-256
`669c9f141f4d219aab1ad2b90f29c610e1e1a91280be87e6d7f34f9c1f7071cf`.

Claude created one intent, saved it as a draft, and then called its content
**complete**. It did not ask for the missing agreed operational problem,
improvement or success measure. Its report treats `not measured`, a baseline,
as the measure and says the audience details can be defined downstream.
The document restates the requested software output rather than establishing
the agreed improvement in the user's situation. The accepted EFF-04A2 criterion
explicitly rejects a complete-content claim for this task.

It also states that only the original operator audience uses the greeting and
that no adapted greeting exists. The fixture defines a fixed rehearsal greeting;
it does not establish those usage or absence facts. The report nevertheless
claims that no content was invented. It calls scope limits proposed, while the
saved draft does not qualify them that way. These findings are R23-NATIVE-005/006.

Separate service reads confirm the exact saved document, its draft state and
all seven imported records' original bytes. The project reached version 4 after
four accepted mutations. No native tool call failed or was denied. Inputs and
inspected host settings are unchanged. The client correctly reports
`content_review: not_assessed`; admitting an incomplete draft is permitted.
This is a content-judgment failure, not a demonstrated storage defect.

## Actual checks

| Check | Result |
| --- | --- |
| Focused resource/package and native-input tests | Pass: 58 tests with 2 skips; 52 tests with 1 skip. |
| Windows source suite | Pass: 1,339 tests, 24 skips, 328.27 seconds including wrapper. |
| Linux source suite | Pass: 1,339 tests, 2 skips, 70.511 seconds; CI run 38355644972, merge commit df971e6b324128d3d325d8e8a3dff25e15e3ad86. Its complete tree equals C; distinct identities and raw evidence are retained. |
| Release archives | Two pinned builds, 434.99 seconds; byte-identical wheel/sdist outputs. |
| Windows/Linux package checks | Released verifier's 10 scenarios, installed wheel, index-selected sdist, CLI surface, init and doctor passed. |
| Plugin staging | Both exact 0.2.7 packages assembled; 47 portable tests passed with 2 skips. |
| Distribution and source CLI checks | Pass. |
| Private service | Exact combination built; fresh diagnostic project initialized and ready. Native import, draft-open, create, revise and independent reads succeeded. Full new-combination walkthrough/recovery qualification is not claimed. |
| Claude EFF-04A2 | **Fail**: 502.774 seconds (8 min 23 s), 10 calls, 9 model turns, 30,027 initial and 71,591 peak input-context tokens. |
| Candidate CI | All 17 executed checks passed; ready-release and complete-delivery legs skipped. This does not override the native failure. |

This negative diagnostic is not successful complete artifact authoring.
Positive-case performance goals do not grade it. The preceding candidate's
311.368-second/12-call result is historical, with different instruction bytes;
do not combine it with this run into a same-candidate benchmark.

## Execution limits and recovery

Automatic review initially blocked the Claude invocation over possible export
of sensitive repository context. Read-only checks confirmed a public repository,
39 exact public fixture/resource files, and no credential matches in the staged
payload. The same invocation was approved with that evidence. No earlier native
trial started, and no execution route or permission changed. Actual local path,
loopback and generated project metadata were part of the test inputs.

The assessor first hit the enclosing tool sandbox's loopback socket restriction,
then resumed the read-only observation with permitted access. An initial guessed
document filename was corrected after inspecting the captured files. These are
assessment/setup events, separate from the failure-free native tool capture.
They are retained alongside the assessment. Credentials and private reasoning
are excluded from public evidence; original/published digests and omission method
are retained.

## Remaining work

VER-HAG-008 requires stopping further native repetitions on this candidate.
No Codex, positive drafting or full native lifecycle/delivery case was run on C.
The reviewed exact edit has been tested and does not establish the required
behavior. Another correction needs a reviewed scope and new candidate; do not
retry until a pass, supply the expected answers or weaken the content criterion.

The failure persists after consolidating the rule, so another wording-only fix
is not yet justified by evidence. The next investigation should examine why the
intent checklist is being treated as permission to defer required inputs and
why template completion is still called complete content. Preserve the distinction
between an allowed saved incomplete draft and a verified authoring outcome.

Remaining release qualification includes current-combination coverage where
required, local upgrade evidence or contract-permitted CI reuse, native diagnostic,
positive/lifecycle/delivery cases, separate Codex Windows desktop evidence,
marketplace review staging, aggregate verification and ready-record rehearsals.
No historical desktop omission applies. No public release, tag, marketplace
promotion, provider setting, adoption or host plugin changed.

The lifecycle context still selects `PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK`
for WO-RLS-050: `harnessctl check REPO --artifact WO-RLS-050 --checkpoint handoff`.
That context does not erase the failed required diagnostic or justify completion.

Evidence: [index](candidate-74feac07-evidence-index.json),
[independent assessment](../WO-RLS-046/candidate-74feac07-claude-assessment.json),
[visible transcript and saved files](../WO-RLS-046/candidate-74feac07-claude-diagnostic.zip).
The [preceding report](qualification-progress-f2ddb5af.md) remains unchanged.
