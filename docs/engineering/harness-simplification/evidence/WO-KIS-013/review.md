# Review of WO-KIS-013

## Result under review

PR-based work now has an explicit path to publish the candidate, evidence and
ready verification record before asking the owner to verify it. The original
work-approval request explicitly includes the bounded publication grant.
The later verification decision is recorded and pushed as the final commit.
Merge remains the owner's choice.

This is source implementation for a future release. The selected 0.21.0
evaluator continues to govern this work. No installed evaluator or plugin has
been changed.

## Requirement assessment

| Criterion from REQ-KIS-012 | Evidence and assessment |
| --- | --- |
| Explicit initial publication grant | AUTHORITY.md owns its bounds. AUTHORIZE_WORK.md requests it explicitly; DRAFT_WORK_ORDERS.md includes the destination and selected work. The plugin reference defers to the selected released policy and preserves provider controls. |
| Remote review before the request | PULL_REQUEST.md requires the draft PR, exact remote identities and readable record/evidence. VERIFY_OUTCOME.md and EXECUTE_WORK.md route PR-based work there first. Local-only work keeps its existing route. |
| Legal review-publication route | PROC-REVIEW-PUBLISH is declared only as an alternative for a ready VREC. It uses existing assurance prerequisites without borrowing the verified integration gate. Runtime and packaged workflow JSON remain identical. |
| Final decision commit | The procedure limits the commit to selected VREC state/history changes. The local Git regression demonstrates separate candidate, preparation and decision heads while captured identity and evidence references stay unchanged. |
| Optional merge | The PR stays draft until the recorded verification is confirmed remotely. Final-head CI and protections remain required; marking ready does not authorize the agent to merge. |
| Corrections and failures | The procedure keeps corrections pending, requires reassessment of changed inputs, and checks remote state before retrying uncertain writes. A failed final push is reported separately from a successful local decision. |

## Focused test results

- focused-first: 153 tests, 152 passed, one expected scale skip; exit 0.
- instructions-first: 55 tests, 53 passed, one failure and one error. Both
  identify the two missing CONTINUE.md index rows. The required edit is outside
  WO-KIS-013 and is proposed in WO-KIS-014; the index was not changed without
  approval. The failing output is retained.
- full-first: 1,238 tests, 1,214 passed, 22 skipped, one failure and one error;
  exit 1. The only failures are the same two missing CONTINUE.md index entries.
  The full output and exact invocation are retained.
- instructions-final: all 55 tests passed after the approved WO-KIS-014 index
  correction; exit 0, 38.489 seconds including runner overhead.
- full-final: 1,238 tests, 1,216 passed and 22 skipped; exit 0, 155.402 seconds
  including runner overhead. The complete command, runtime and output are
  retained beside this review. No required failing test remains.

The focused tests exercise the ready-record route without modifying the VREC,
refusal of integration before verification, refusal of the review route for
non-ready records, conditional discovery, and candidate preservation across
the final decision commit. The local Git fixture uses simulated human authority,
not a real production verification decision.

## Instruction examples inspected

These examples are illustrative; no hosting operation or human decision occurs.

| Situation | Expected instruction-driven behavior |
| --- | --- |
| Approved work and matching publication grant | Push the reviewed head, open or update its draft PR, check remote identities, then request verification with the PR and immutable evidence links. |
| Missing grant or failed publication | Explain the missing right or operation. Do not replace the remote package with a local path and request acceptance anyway. |
| Existing matching PR | Reuse it; a retry must not create another PR. |
| Wrong branch, head or destination | Stop the affected publication/request and resolve the mismatch. Existing authority does not extend to that new target. |
| Human verifies unchanged inputs | Apply the real transition, commit only the selected record update, and push under the earlier grant. The candidate stays the captured implementation commit. |
| Human requests corrections | Keep the PR draft and the decision pending. Confirm eligible correction work and prepare the revised verification package. |
| Final push fails | Report recorded locally but not delivered. Inspect the remote and retry only missing effects; do not reapply the lifecycle transition. |
| Required evidence is unavailable or final-head CI fails | Keep the actual failure visible. Do not infer verification or merge readiness from another successful check. |
| Local-only work or no new VREC required | Use the existing selected procedure; no PR is added by this rule. |

## Design and limits

One declared workflow alternative and its discovery prerequisites reuse the
existing rights, gates, CLI, record states and hosting tools. No new service,
state, command, network dependency in the evaluator, or permanent publication
receipt is introduced. The source root/startup router is unchanged.

The evaluator's local checks do not prove remote access or authenticate a
human. Agents must perform the prescribed provider readback and authority
checks. Draft PR controls are the normal hosting barrier, not a claim that a
privileged owner cannot bypass provider controls.

## Index correction and completion assessment

mmzen approved WO-KIS-014 and its required verification. The correction adds
only the two missing CONTINUE.md rows. Both index assertions now pass without
weakening a test. The combined candidate covers WO-KIS-013 and WO-KIS-014.

The six requirement criteria above pass the prescribed local tests and
inspection. The local Git demonstration passes in both the focused and full
suites. Its authority and provider observations remain simulated. No live
Codex or Claude test is required by VER-KIS-006.

Released-evaluator validation reports zero errors and zero advisories.
Integrity checks pass. The 58 unrelated historical warnings are unchanged.
Human verification, hosted CI, publication, release and installed adoption
are separate outcomes; this assessment does not claim them.

