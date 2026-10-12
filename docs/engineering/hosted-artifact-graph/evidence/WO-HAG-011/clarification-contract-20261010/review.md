# Review: one report for a clarification-only stop

**Decision requested:** Approve the linked SPEC-HAG-008, VER-HAG-008 and
WO-HAG-011 revision, including bounded manual activation and continued required
commit-bound verification. The exact proposed implementation is included below.
Nothing in this proposal is active yet.

## What changes

1. When the agent stops for missing requester input before attempting any hosted
   mutation, use its retained final reply as the report. Remove the duplicate file.
2. Keep the saved report and recovery duties after any mutation command is invoked,
   including a command refused locally or denied by host permissions.
3. Clarification asks what should change for the user and how the owner will know
   it helped. Reuse supplied answers. This makes the existing content rule explicit;
   it does not accept a replacement output string as the missing operational outcome.

The [last assessment](../clarification-route-assessment.md) records a 107-second,
four-call Claude run that correctly stopped before writing. It still failed:
the required separate report was absent, and the questions did not clearly identify
the missing agreed user outcome and measure. That failure remains recorded.

## Exact scope

| File | Proposed change |
| --- | --- |
| SPEC-HAG-008 | Define the conditional report form and capture requirements; measure through the required final output. |
| VER-HAG-008 | Independently assess eligibility and retain existing content criteria; no retrospective pass. |
| WO-HAG-011 | Apply this bounded change and retain the existing qualification sequence. |
| plugins/verity-plane/common/skills/change/references/hosted-drafts.md | Select the reporting branch and clarify the existing intent questions. |
| tests/hosted_artifact_graph/native-drafting-task.md | Follow that guide; require native-report.md only on its saved-report branch. |

Read the [five-file diff](proposal.patch), [exact file identities](proposal.json),
[specification](SPEC-HAG-008.proposed.txt), [verification contract](VER-HAG-008.proposed.txt),
[work order](WO-HAG-011.proposed.txt), [guide](hosted-drafts.proposed.txt), and
[native task](native-drafting-task.proposed.txt).

## Boundary examples

| Observed situation | Required report |
| --- | --- |
| Missing requester input; only reads; full reply and calls retained | Captured final reply with missing inputs/questions, no-attempt statement and observed failures. |
| Import/create/revise command invoked, even if refused before sending | Existing native-report.md and actual command evidence. |
| A mutation reply is uncertain | Existing report and operation-key reconciliation; no unsupported no-change claim. |
| Reply or calls are missing | Evidence remains incomplete; absence of a changed project version proves no exemption. |

The assessor checks actual calls and fresh service state. The final reply cannot
certify its own eligibility. Read failures still belong in the reply and independent
assessment. A correct report form does not compensate for unsupported content.

## KIS review

The normal clarification result already lives in the conversation. Its capture
already exists. Requiring another file duplicates the same unanswered questions
without adding a changed artifact or recovery identity. Removing that requirement
is simpler than a new report generator or an extra tool call to save the reply.

The alternative of removing all reports would lose the useful recovery summary
after an attempted change. Keep that existing report. This proposal adds one
explicit condition, but no command, driver option, dependency or automatic content
grader. The task points to the guide rather than copying its branch rules.

No shorter duration or reduced context is claimed before a new trial. A correct
clarification stop is not evidence of successful artifact creation. The existing
positive authoring sequence and its timing goals remain required.

## Activation and validation

Released 0.22.1 has no supported linked-definition revision command. The proposed
bounded manual activation would copy only the three reviewed formal files after
checking their accepted and proposed full-file digests, preserve the accepted
copies and original lifecycle events, and record mmzen's actual decision and
before/after identities at this evidence location. It changes no artifact state.
Earlier work retains its original definition references. Approval of the exact
proposal is needed before these revised obligations govern work.

All five paths already fit WO-HAG-011's approved path scope. Its behavior requires
this explicit amendment; existing approval alone does not activate it. The actual
approval would permit the two reviewed instruction edits, relevant checks, exact
candidate builds and the existing native sequence. Required commit-bound verification
remains separate. Git remains authoritative; no permission changes are proposed.

Before publishing this review, validate the active repository and the proposed
definitions in a disposable copy, compare metadata/history and unaffected task
text, check scope and review preflight, and retain the results. These checks inspect
the proposal; they do not qualify the future implementation or clear the existing
WO-HAG-009 handoff-evidence finding in draft PR #543.

After approval and activation: run one fresh Claude EFF-04A2 and stop if it fails.
If it passes, run Codex EFF-04A2 with the existing boundary probes, then EFF-04B:
a correct initial Claude attempt, two fresh repeats on the same candidate, and
one Codex attempt. Preserve every result. Keep full WO-HAG-009/010 qualification
separate and incomplete until its own contract passes.

## Observed proposal checks

Released validation of the disposable proposed graph: 1,991 artifacts, zero errors,
63 existing warnings. Proposed review preflight, five-path scope and diff checks pass.
Metadata, lifecycle history, requested outcomes and native task entry are unchanged.
All five active files still match their accepted digests. These are proposal checks;
no new native test or implementation result is claimed.

The guide grows from 986 to 1,057 words and the task from 383 to 390 words.
That is a real instruction cost, accepted here as a proposal tradeoff for one explicit
reporting branch. Avoid adding a second reporting mechanism or copying the branch
criteria into the task. Actual context and duration still require measurement.

The disposable clone initially failed on sandbox process startup, then on Windows
path length. Recovery used the approved execution route and long-path support in
that clone only. The first scope check covered the five proposed active paths;
the final check includes all 16 changed paths, including the review copies, with
no unreadable inventory paths. Failed commands and corrected checks are retained
in publication-checks.zip. The active checkout was not repaired or reset.
