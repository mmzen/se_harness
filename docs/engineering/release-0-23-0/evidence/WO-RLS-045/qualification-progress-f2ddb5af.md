# Corrected 0.23.0 candidate: results and remaining blocker

**Not ready for verification, merge or release.** Candidate `f2ddb5afe42d40cc7c4a426b5c9cb985156a28a3` contains the
exact instruction correction approved under WO-RLS-049. Its first required
Claude EFF-04A2 diagnostic failed independent content review. The work orders
remain in progress. No completion or human verification is inferred.

## What changed

The reviewed `hosted-drafts.md` bytes were applied, packaged and delivered.
SHA-256: `cdd3d9f13a7998a36ff5f2c293dff8dad6f61c54997f69f41edd48c6b096c23e`.
The exact linked REL-SEH-036 membership amendment was also applied with prior
accepted bytes/history preserved. Existing tasks, models, permissions and
criteria were unchanged. The earlier candidate and its failure remain recorded.

## Observed checks

| Check | Result |
| --- | --- |
| Windows full source suite | Pass; 1,339 tests, 24 reported skips, 330.49 seconds. |
| Linux full source suite | Pass; 1,339 tests, 2 skips. CI run 38333230109 tested merge commit 78635a102c6486d69fa11e72b2cb5a8f963f7c76. Its complete tree exactly equals this candidate; raw result and comparison are retained. |
| Release recipe | Two pinned builds produced identical wheel/sdist bytes. |
| Windows/Linux archives | Released verifier, installed wheel, index-selected sdist, CLI surface, init and doctor passed. |
| Plugin packages | Both exact 0.2.7 archives staged; 47 portable tests passed with 2 skips. |
| Upgrade | Two real Windows 0.22.1 → 0.23.0 rehearsals passed with matching semantic digests. |
| Private service | New exact combination built; packaged walkthrough, compatibility/refusal/concurrency/transaction/HTTP-MCP checks and restart/consistent restore passed. |
| Claude diagnostic | **Fail.** 311.368 seconds, 12 native calls, 13 model turns, 30,042 initial and 60,269 peak input-context tokens. |

The diagnostic is a failed missing-input case, not successful complete artifact
authoring. Positive-case performance goals do not grade it. All executed CI
checks at the candidate passed; ready-RLS and complete-delivery legs were skipped.
The later evidence-only review head has its own CI status.

## Why Claude failed

Claude saved one draft, `INT-P3-001`, and called its content **complete**. Its
document still said that the audience and observation point were unknown. It
did not ask for the missing user problem, agreed improvement or success measure.
It supplied a problem based on a missing software capability and added scope
limits that the request had not established. Its report then denied unsupported
claims. These are R23-NATIVE-003 and R23-NATIVE-004 in the independent assessment.

The service correctly returned `content_review: not_assessed`. Zero structural
errors and incomplete fields do not prove semantic completeness. The failure
is in the agent's content judgment/report, not evidence that draft admission
should reject every incomplete draft. The contract explicitly permits retaining
an incomplete draft; it forbids claiming this missing-input result complete.

No native call failed or was denied in this run. The previous failed-Read omission
did not recur, but this failure-free run cannot prove reliable reporting after
errors. The saved report also counted three accepted mutations while listing
four receipts: import, draft-open, create-artifact and revise-artifact.

Separate service reads confirm the exact authored revision and all seven imported
records' original bytes. The project is version 4; the new intent remains draft.
Staged files and inspected host-setting hashes are unchanged. The complete
visible transcript, saved draft/report and readbacks are retained; private
reasoning and credentials are excluded with digests and omission method.

## Preserved setup and assessment errors

The initial diagnostic database connectivity probe ran before Memgraph was ready.
It failed before initialization; the later read-only probe passed and initialization
ran once. The assessor initially read a nonexistent `result.baseline_id` field;
it retained the successful draft read, corrected the field to `view.baseline_id`
and completed the remaining independent reads. These are test-setup/assessor
errors, not hidden native failures. Earlier focused-test permission/import errors
remain in WO-RLS-049's retained correction checks.

## Next work

VER-HAG-008 requires stopping native repetitions on a candidate whose first
diagnostic fails. No Codex or positive drafting attempt was run on this candidate.
The exact reviewed instruction edit is exhausted; another product correction
needs a new bounded review before a new candidate is qualified.

The next correction should address the distinction between unknown required
inputs, saved draft status and content readiness. Reordering the existing text
alone did not establish the required behavior. Preserve the content criterion,
agent-selected operations and independent assessment. Do not repeat trials to obtain
a pass, supply the expected answer, or add a script that authors the draft.

Remaining release work includes native diagnostics/positive/full-lifecycle cases,
native instruction-delivery cases, separate Codex Windows desktop evidence,
marketplace review staging, aggregate verification and ready-record rehearsals.
No prior desktop omission applies. No public release, tag, marketplace, host
plugin, adoption or provider setting changed.

Evidence: [index](candidate-f2ddb5af-evidence-index.json),
[independent assessment](../WO-RLS-046/candidate-f2ddb5af-claude-assessment.json).
The [previous candidate report](qualification-progress.md) remains unchanged.
