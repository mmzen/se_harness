+++
id = "VER-CIP-005"
type = "verification"
title = "Check upgrade rehearsal timing preserves the real handover"
status = "draft"
owners = ["assurance-owner"]
created = "2026-09-11"
updated = "2026-09-11"

[relations]
verifies = ["REQ-ECP-012"]
+++

# Verification Contract: Check upgrade rehearsal timing preserves the real handover

## Independence

The existing handover sequence and verdicts come from SPEC-ECP-007 ECP-PRD-008,
VER-ECP-007 and the baseline rehearsal. Timing expectations use an independently
controlled clock in focused tests. Real durations are observations, not expected
values copied from candidate output. No performance acceptance threshold is set.

## Requirement-to-evidence matrix

| Requirement and rule | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-ECP-012; SPEC-ECP-007 ECP-PRD-008 | test, inspection, demonstration | TIM01-TIM06 | Instrumentation preserves the real handover, both replays and cross-platform agreement, while exposing their actual stage costs. |

## Acceptance scenarios

| Case | Action | Observable pass condition |
| --- | --- | --- |
| TIM01 - Unchanged handover | Exercise existing success and failure fixtures with timing disabled and enabled. | Same commands, order, timeout bounds, exit decisions, original result fields and semantic digest. Expected predecessor refusal and permitted E012 diagnostics retain their meaning. |
| TIM02 - Timing accuracy | Supply a controlled monotonic clock; time stages, child stages and the complete replay. | Correct elapsed intervals, fixed identifiers, explicit parent relationships or non-overlapping categories; no double-counted total or timing in the semantic digest. |
| TIM03 - Failure reporting | Inject an evaluator failure, export failure and cleanup failure; test interrupted or unwritable timing output. | Partial observations identify the failed or unfinished stage. Original failure is not suppressed, and incomplete measurement never counts as complete evidence. Existing behavior without timing remains intact. |
| TIM04 - Boundaries | Inspect diagnostic paths and test an output path inside the operational repository. Inspect workflow commands and allowed diagnostic fields. | Timing output is outside the checkout. No new credential, broad environment dump, Defender mutation, original checkout write, archive-limit change, or secret-bearing output. |
| TIM05 - Hosted comparison | Run the normal PR workflow on Windows and Linux with two independent replays per platform. Read actual image and runtime facts. | Four timing files and their original result files identify the exact run and tested commit. All existing handover gates pass, replay digests agree and Windows/Linux semantic digests agree. Defender state is observed or explicitly unavailable. |
| TIM06 - Candidate checks | Run focused tests, normal required checks, released doctor/validate, Git scope checks and actual archive counting. | Existing test verdicts and CI controls remain intact; only WO-CIP-009 paths differ; archive has at most 10,000 entries. Report any failed check without a waiver. |

## Property and invariant tests

Progress output is flushed at stage boundaries. Monotonic durations remain
non-negative; nested and unaccounted time are labelled. Different durations
cannot change the resulting lock digest. No output path is followed outside
the explicitly selected diagnostic destination. Test failure paths without
executing dangerous actions on the real checkout.

## Static and architecture checks

Review the complete diff against the pinned baseline. Keep the two Python
rehearsal invocations, existing artifact hashes, caller isolation, exported
committed tree, clean-checkout check, job dependencies and both platforms.
No full-suite or qualification duplication is introduced by instrumentation.

## Security and privacy checks

Only read Defender state/preferences. Do not add exclusions, disable a service,
change permissions or print the environment. Measurement cannot waive any gate.

## Performance and resilience checks

Compare Git export, extraction, staging, commit creation, each evaluator and
cleanup separately. Report each replay, not only the sum or fastest result.
A second workflow run, if needed, must use the same candidate and be labelled
separately. Claim a dominant stage only from hosted measurements; local Python
3.14 results do not substitute for hosted Python 3.11 observations.

## Manual assessments

Explain the measured Windows/Linux gap in plain English. Distinguish observed
cost, inferred explanation and any remaining uncertainty. Do not promise a
speedup or choose an optimisation before the measurement supports it.

## Evidence retention

Keep raw timing JSON, original result JSON, logs and runtime facts as Actions
artifacts and downloaded copies with SHA-256 hashes outside the checkout.
Bind the report to the PR head, tested merge and run/job identifiers.
This measurement packet does not authorize later VREC preparation. A separately
reviewed capacity plan is needed for durable verification delivery under the
unchanged 10,000-entry archive limit.

## Residual uncertainty

Hosted VMs vary. Timing itself adds overhead. Two replays show within-job
variation but do not establish a broad benchmark. Image configuration is not
proof of runtime Defender state, and an unavailable query cannot settle it.
