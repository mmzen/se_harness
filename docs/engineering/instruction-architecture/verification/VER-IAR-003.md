+++
id = "VER-IAR-003"
type = "verification"
title = "Verify review procedure responsibility separation"
status = "approved"
owners = ["quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
verifies = ["REQ-IAR-011"]
+++

# Verification Contract: Verify review procedure responsibility separation

## Independence

Tests assess the requirement's responsibility and authority meanings across both managed files, while human inspection checks that concise routing has not removed a review obligation.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-IAR-011` | content tests | fresh router and workflow | Router owns routing/invariant; workflow owns both exact commands and inspection activity. |
| `REQ-IAR-011` | migration tests | exact-prior and customized installations | Exact content upgrades transactionally and idempotently; customization blocks all writes. |
| `REQ-IAR-011` | parity and regression | self-hosting plus full suites | Root/distribution/lock agree and no behavior regresses. |

## Property and invariant tests

- Assert the router contains the approved evidence boundary and no exact `--phase review` or `harnessctl dashboard .` invocation in its review section.
- Assert workflow step 6 contains both commands, evidence retention, and consistency/anomaly inspection.
- Assert preflight and Explorer are never described as approval or verification transitions.
- Assert exact prior router/workflow content upgrades together, a second apply is a no-op, and customization prevents every write.

## Static and architecture checks

Run doctor, start/review preflight, formal validation, CLI help, deterministic dashboard generation, canonical/root/lock parity, changed-path inspection, and diff hygiene.

## Performance and resilience checks

Run focused instruction and artifact-authoring suites plus the full suite on Python 3.11 and the local supported runtime.

## Manual assessments

Confirm no review, evidence, visualization, quality-gate, lifecycle, or authority obligation is lost and no unrelated policy body or historical governance fact changes.

## Evidence retention

Retain commands, runtimes, test counts, upgrade outcomes, parity, graph diagnostics, Explorer snapshots, changed paths, deviations, and residual risk under `WO-IAR-003`.

## Residual uncertainty

No structural check proves an actor performs meaningful candidate inspection. Accountable review remains necessary.
