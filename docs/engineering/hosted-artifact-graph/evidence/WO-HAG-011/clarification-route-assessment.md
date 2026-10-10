# Clarification-route qualification assessment

**Result: improved behavior, qualification still fails.** Claude now asks for
clarification before creating anything. Its required saved report is missing,
and its questions do not clearly identify the missing agreed operational outcome
and measure. Further native tests stopped under the approved first-Claude rule.

Candidate: `c374a960b16a2e64cd0d39da3888ea19ab1842a7`.
Selected work: `WO-HAG-011`; contract: unchanged `VER-HAG-008 EFF-04A2`.

## Applied correction

The [routing review](routing-review-20261010/review.md) identified that the previous
entry delivered drafting instructions whose confirmed-outcome and scope inputs
were missing. The existing clarification procedure had not been supplied.

Applied the exact reviewed edit to
`plugins/verity-plane/common/skills/change/references/hosted-drafts.md`.
It routes missing-input work to released DEFINE_CHANGE.md and retains the existing
drafting route for confirmed inputs. All text from **Check the inputs before
writing** onward remains unchanged. The actual edit is bound in
[implementation evidence](routing-review-20261010/implementation.json).

The test uses the existing section-selection option to deliver the current
clarification step first. It retains all 12 original fixture files, the exact A2
request, model, host permissions, content criteria and independent checks. No
assessor classification, expected answer or operation sequence was supplied.
No accepted formal artifact, lifecycle rule, command or decision right changed.

## Independent result

Claude read the setup route, checked service readiness and loaded drafting
sections. Its final response then selected clarification. It acknowledged
INT-P3-900, proposed an outcome for confirmation, and asked who the new audience
is and what greeting it should receive. It did not claim a completed artifact.

The service stayed at project version **0**. There was no import, draft context,
new artifact or lifecycle action. Staged inputs remained unchanged. No saved
document exists, so a saved-revision read is not applicable. The seven source
records still match their Git-blob bytes; none was imported or modified.

Two findings prevent a pass:

1. **The required report is absent.** `work/native-report.md` was not written.
   A final conversational reply and operator-captured transcript do not satisfy
   the task's required native report with readiness, saved state and review.
2. **Clarification remains incomplete.** The response asks for an audience and
   expected output text, treating those as determining the outcome and measure.
   It does not clearly identify the missing agreed change in the user's situation
   and how the owner would observe that the change helped, required by A2.
   Its outcome is explicitly proposed for confirmation, so it is not assessed as
   a falsely accepted or saved definition. This is progress, not complete coverage.

There were no failed or denied native calls and no false zero-failure claim.
The [independent assessment](claude-161-assessment.json),
[visible transcript](claude-161-visible.md), [evidence archive](claude-161-evidence.zip)
and [inventory](claude-161-inventory.json) retain the actual inputs, calls, response
and state checks. Private reasoning and credentials are omitted from publication.

## Cost comparison

| Observation | Previous A2, candidate21 | Current A2, candidate22 |
| --- | ---: | ---: |
| Wall time | 226.201 s | 106.925 s |
| Native calls | 13 | 4 |
| Model turns | 11 | 3 |
| Initial input context | 32,677 tokens | 28,900 tokens |
| Peak input context | 58,356 tokens | 37,770 tokens |
| Delivered task | 62,179 bytes | 45,982 bytes |
| New artifacts | 1 unsupported draft | 0; clarification requested |

Both observations use Claude Code 2.1.273, `claude-opus-4-6`, the same A2 request,
original fixture and bounded permission mode. They differ in candidate guidance
and initial section selection. One observation per candidate is not a reliability
or performance benchmark. Avoided incorrect drafting is part of the difference.
Historical EFF-04A is a different task and is not included in this comparison.

All three numeric thresholds are met in this negative trial. That does not
establish successful positive authoring or satisfy EFF-04B. Its positive cases
remain unperformed on this candidate.

Initial canonical instruction text falls from 21,262 to **4,989 bytes**. The full
guide grows by 161 words, from 825 to 986, which remains a maintenance cost. Later
drafting content stays available and Claude did load it; the lower initial load
does not mean those sections were permanently removed. Selected references are
19,310 bytes, fixture 5,490, selection/provenance 12,079 and other task text 4,114.

Captured client execution took 0.522 seconds; tool results added 18,868 visible
characters. Provider time is unclassified. Exact build, package preparation and
client installation took **485.836 seconds**, separately from the native run.
The source suite ran alongside preparation; native measurement began after both
finished. Preparation remains costly and is not hidden in the native comparison.

## Checks and boundaries

- Source suite: 1,336 tests, 24 skips, exit 0. Focused native checks: 31 pass.
- Distribution validation and CLI smoke pass. Released validation: 1,991 artifacts,
  zero errors, 63 existing warnings; review preflight and scoped edit checks pass.
- Two pinned builds produce matching archives. Both plugin packages contain the
  exact committed guidance; all five delivered canonical sections match their sources.
- Client/runtime member payloads, server source, dependencies and build inputs
  match candidate15. Prior EFF-02/03 runtime evidence is reused only for those
  unchanged bytes, not the changed instruction route or new native behavior.

Wheel SHA-256: `411306ca518c14b4fae20a6532344fc637e2bb5f06142bcbc34b805b9d3f9522`.
Sdist SHA-256: `2d5767e0184696676f240e91e2a84c3a173eaf802b87b1265880337727d8533d`.
The separate candidate client is 0.22.2 and packaged plugin is 0.2.7; released
0.22.1 remains the repository governor. No host installation changed. Exact
commands, component identities and review records are in
[candidate22-checks.zip](candidate22-checks.zip).

## Review and remaining work

The route change reaches an existing earlier procedure without adding a new
gate, framework or command. It avoids premature service writes in this sample.
It also exposes a branch-completion gap: the clarification reply bypassed the
required saved report. The questions still frame success as a returned string.

Before another variation, review whether a separate report file is needed for a
clarification-only stop. The released clarification procedure permits conversational
working material, and the runner already retains the final reply and observed calls.
Requiring the agent to duplicate that reply in a file may add work without useful
state to recover.

A bounded proposal would accept the retained final reply for a clarification stop
with **no attempted mutation**, while keeping the existing report/recovery duties
after a mutation attempt or uncertain effect. The exact missing inputs and actual
failures would still be retained and independently assessed. That changes a test
obligation and needs a reviewed amendment before use; it is not applied here and
would not retrospectively pass this trial.

Separately, the questions still need to identify the missing agreed user outcome
and measure, rather than assume that specifying a new string establishes both.
These findings do not justify silently weakening A2 or claiming reliable authoring.
No additional variation has been applied in response to these findings.

Codex A2 and all positive cases remain unperformed on candidate22. Full
WO-HAG-009/010 qualification remains incomplete. The owned trial containers are
stopped and their volumes are retained. No work completion, verification or merge
is claimed. The local complete-PR check still identifies WO-HAG-009's missing
handoff evidence; the draft publication grant does not resolve that finding.

WO-HAG-011 stays `in_progress`. The released next step remains
`PROC-WO-IMPLEMENT / STEP-WO-IMPLEMENT-CHECK`:
`harnessctl check REPO --artifact WO-HAG-011 --checkpoint handoff`.
The current content/report failures remain unresolved at that step.
