# Verification request: one approval for a complete release

**Decision requested:** Verify VREC-RLO-014 as assurance owner.

The implementation prepares all release deliverables before one complete-release
approval. It reuses that recorded approval for the listed publication and recovery
actions. Failed checks, changed inputs and incomplete public observations still stop
the affected action.

## Exact scope

- Candidate: `7e7071d80eb22f43436807479972fee85905de43`.
- Record: [VREC-RLO-014](../../verification-records/VREC-RLO-014.md), currently `ready`.
- Work: WO-RLO-014, WO-RLO-015, WO-RLO-016 and WO-RLO-017, all `implemented`.
- Contract: [VER-RLO-011](../../verification/VER-RLO-011.md).
- Preparation and gates: the selected released evaluator 0.21.0.

## What the result demonstrates

| Expected result | Observed evidence |
| --- | --- |
| One approval covers the exact complete plan, including valid retries. | Workflow tests and real Git plan-binding tests pass; legacy grants are not expanded. |
| Both host plugin payloads can be prepared before the evaluator is public. | Windows and Linux staging and legacy package suites pass, 34 tests on each platform. |
| Publication checks approved bytes and resumes partial delivery safely. | Marketplace, marker, unknown-provider-state and complete/incomplete delivery cases pass. |
| Required checks remain meaningful. | Windows final capture: 1,255 tests, 22 skips, exit 0. Linux source suite: 1,255 tests, 2 skips. The final record retains the exact Windows candidate test result. |
| The one-time configuration change is reviewable. | Sanitized live snapshots, exact reviewer-only proposal, preservation checks and recovery are retained. No live setting was changed. |

The [implementation review](implementation-review.md) maps ONE01 through ONE08 to
the retained tests. [Capture recovery](capture-recovery.md) explains both failed
attempts and the evaluator-only Git setting that affected a fixture. The final run
uses normal workstation Git settings for tests; no product or assertion was weakened.
The raw suite output includes stderr from an intentional invalid-worker argument
test. Its final verdict is `OK (skipped=22)` with exit 0.

## Limits that remain

This verifies implementation and activation preparation. Operation requires a later
product release/adoption and the separately reviewed one-time provider change.
The live PyPI account-side Trusted Publisher binding remains unobserved and blocks
activation. Native public-host qualification remains a future release obligation.

GitHub latest-release updates have no compare-and-swap endpoint. The workflow
serializes its own writers and checks/readbacks the expected value; other writers
must not move markers concurrently. The `last` ref uses an exact Git lease.

## Evidence and next decision

The generated record binds 35 retained evidence files and the exact candidate.
Its verification-transition check passes. The later `final-capture-results.zip`
preserves complete capture output and that gate result as a supplemental review
attachment; it is not represented as one of the earlier candidate's bound files.
Archive SHA-256: `e1e1375a9717e924fde0933d42cbad2af77742f2bde9ed5ce1100d31dfe616cb`.

Human verification remains pending. To accept this implementation, reply:

> I verify VREC-RLO-014 as assurance owner.

That decision will be recorded and pushed as the final governance update under
the existing review-PR authorization. Merge remains the owner's decision.
