# Integrated lifecycle and migration assessment

The candidate is not ready for VREC-IAR-020. Installed-package testing reproduced
the same verification-evidence defect on Windows and Linux. WO-IAR-030 remains
in_progress. WO-IAR-039 proposes the bounded correction; it grants no authority
while draft.

## Candidate and method

The tested wheel was independently built from
c1bcbfb8e053ee8099e98b1dc34fcf547adc46eb. Its SHA-256 is
66467146b32853ce87d7a782a9452aca8e20ead4ba4cb07837ec16c518aa784d.
Relevant package inputs are unchanged at repository HEAD
c316a371037379ef1c5e87fa8f0be66bfc3804a9. The selected repository stays governed
by released 0.20.1. The candidate runs only in disposable fixtures.

Full arguments, working directories, runtimes, exit statuses, outputs and driver
revisions are retained in integrated-lifecycle-and-migration.json. Windows uses
Python 3.14.6; Linux uses the retained WSL Ubuntu environment. The CLI runner
blocks network socket operations after installation. Synthetic fixture decisions
exercise the actual evaluator; they are not decisions about this product.

## Findings

| Criterion | Observed result |
| --- | --- |
| Minimal footprint and explicit Git integration | Passed on Windows and Linux: exactly two initial files; Git preview writes nothing; explicit apply adds only .gitattributes. |
| Governed lifecycle | Draft validation, definition/work approval, start, byte assertion, review, complete Git handoff, completion and committed-candidate capture succeeded on both platforms. The generated VREC is ready. |
| Usable verification evidence | **Failed on both platforms.** The next checkpoint-free check rejects VREC-QAL-001 with E012: standard evaluator lock identity is invalid. Do not treat the successful capture as an end-to-end pass. |
| Native replacement entry | Real Claude 2.1.273 startup and manual-compaction traces each contain the full exact rendered entry, independently compared with the wheel. Entry SHA-256: 9c581e0e80d3e1851eb5ce46bffd06945264aa366b64b7360232c5bee4319990. The selected fixture is unchanged. |
| Legacy migration | Passed on Windows and Linux from released 0.20.1. Reviewed managed copies and the selected stock authoring seed retire. Binary owner instructions, an owner note, historical intent and unselected templates retain their bytes. |
| Migration refusals | Missing native receipt refuses. A customized selected seed refuses with written=false. Every file remains unchanged in each final run. |
| Interruption and retry | An injected lock-write failure rolls back every byte on both platforms. Actual migration then passes, doctor passes, and repeat upgrade changes nothing. The native receipt uses the documented disposable rehearsal bound to each actual legacy target. |

The lifecycle record is unusable because validation_evidence.py restricts the
lock formats used for evidence comparison to schemas 3 and 4. Minimal installation
correctly writes schema 5. This is a product defect, not missing human approval.
The correction must validate that format using the existing lock validator and
preserve all evaluator-evidence checks and legacy refusals. It needs a newly
approved work order because the implementation file is outside the active scopes.

## Earlier driver failures

All attempts remain retained. Attempt 1 omitted the required candidate-commit
argument when supplying a test command; capture refused without writes. Attempt 2
read revision.commit instead of the actual top-level commit after successful
capture. Those driver errors were corrected before the final lifecycle runs.
Migration attempt 4 expected exit 2 for a customized seed; the CLI correctly
returned exit 1 and written=false. Attempt 5 checks that documented result and
byte preservation. None of these driver corrections changes product behavior or
removes the final E012 failure.

## Remaining work and limits

Approve and implement the bounded validator correction, rebuild the candidate,
rerun the failing installed-wheel lifecycle on both platforms, and reassess
affected evidence before handoff and aggregate capture. The final hash comparison
of bound evidence across platforms remains pending with the lifecycle correction.
Current native automatic compaction already passed and remains retained in
claude-fresh-recovery.json; these migration traces are a separate manual rehearsal.
Codex desktop remains unverified under the human's existing instruction.

No affected work order was completed and no VREC-IAR-020 was created. No source
implementation, accepted definition, installed harness, credentials, release,
remote branch or PR was changed in this assessment.
