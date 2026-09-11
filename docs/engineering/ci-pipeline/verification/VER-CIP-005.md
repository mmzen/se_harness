+++
id = "VER-CIP-005"
type = "verification"
title = "Check upgrade rehearsal timing preserves the real handover"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-11"
updated = "2026-09-11"

[relations]
verifies = ["REQ-ECP-012", "REQ-IPK-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-11T17:09:29Z"
decided_by = "assurance-owner"
reason = "The accountable operator approved VER-CIP-005 and WO-CIP-009 on 2026-09-11: i approve both, in response to the named packet and diagnostic implementation authorization question."
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
| REQ-IPK-001; SPEC-IPK-001 identity and security rules | test, inspection, demonstration | CAP01-CAP03 | The bounded capacity increase accepts up to 20,000 entries and preserves safe exact-commit extraction. |

## Acceptance scenarios

| Case | Action | Observable pass condition |
| --- | --- | --- |
| TIM01 - Unchanged handover | Exercise existing success and failure fixtures with timing disabled and enabled. | Same commands, order, timeout bounds, exit decisions, original result fields and semantic digest. Expected predecessor refusal and permitted E012 diagnostics retain their meaning. |
| TIM02 - Timing accuracy | Supply a controlled monotonic clock; time stages, child stages and the complete replay. | Correct elapsed intervals, fixed identifiers, explicit parent relationships or non-overlapping categories; no double-counted total or timing in the semantic digest. |
| TIM03 - Failure reporting | Inject an evaluator failure, export failure and cleanup failure; test interrupted or unwritable timing output. | Partial observations identify the failed or unfinished stage. Original failure is not suppressed, and incomplete measurement never counts as complete evidence. Existing behavior without timing remains intact. |
| TIM04 - Boundaries | Inspect diagnostic paths and test an output path inside the operational repository. Inspect workflow commands and allowed diagnostic fields. | Timing output is outside the checkout. No new credential, broad environment dump, Defender mutation, original checkout write, or secret-bearing output. Only the separately authorized CAP01 capacity change is admitted. |
| TIM05 - Hosted comparison | Run the normal PR workflow on Windows and Linux with two independent replays per platform. Read actual image and runtime facts. | Four timing files and their original result files identify the exact run and tested commit. All existing handover gates pass, replay digests agree and Windows/Linux semantic digests agree. Defender state is observed or explicitly unavailable. |
| TIM06 - Candidate checks | Run focused tests, normal required checks, released doctor/validate, Git scope checks and actual archive counting. | Existing test verdicts and CI controls remain intact; only WO-CIP-009 paths differ; final archive has at most 20,000 entries under the authorized amendment. Report any failed check without a waiver. |
| CAP01 - Entry boundary | Test 19,999, 20,000 and 20,001 archive entries; exercise successful extraction and rejection with a small boundary fixture. | The configured limit is 20,000, inclusive. Directories count as entries. Above-limit and empty archives are refused before member extraction. |
| CAP02 - Other protections | Exercise oversized-member and expanded-total failures, plus the existing hostile-path, link and duplicate tests. | The 128 MiB per-member and 512 MiB archive/expanded-total caps and existing path/type checks remain enforced. Small byte-limit fixtures may be used to avoid large allocations. |
| CAP03 - Real candidate | Count the committed Git archive, retain this WO's handoff evidence, and run the normal candidate pipeline. | The candidate has more than 10,000 and no more than 20,000 entries; exact-commit builds and Windows/Linux integration verification pass. Released handoff and scope checks pass with retained evidence. |

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

Keep raw logs and wheels as Actions artifacts and downloaded copies with SHA-256
hashes outside the checkout. Retain compact timing/result JSON, runtime facts,
test summaries and the generated handoff packet under WO-CIP-009's evidence
directory. Bind reports to the actual PR head, tested merge and run/job IDs;
label the original measurement separately from later capacity checks.
The authorized 20,000-entry amendment permits this durable handoff evidence.
It does not authorize VREC preparation, completion or an assurance decision.

## Residual uncertainty

Hosted VMs vary. Timing itself adds overhead. Two replays show within-job
variation but do not establish a broad benchmark. Image configuration is not
proof of runtime Defender state, and an unavailable query cannot settle it.

## Capacity amendment — 2026-09-11

The operator's "you can raise the limit" extends the previously approved
verification coverage with CAP01-CAP03. Expected limits come from the bounded
WO-CIP-009 amendment, not from candidate output. Existing timing and safety
criteria remain. The verification contract stays approved; no observed result
is treated as a human verification decision.
