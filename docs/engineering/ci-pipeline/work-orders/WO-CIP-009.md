+++
id = "WO-CIP-009"
type = "work_order"
title = "Measure Windows and Linux upgrade rehearsal stages"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-09-11"
updated = "2026-09-11"

[assurance]
commit_bound_verification = "required"
rationale = "Timing instrumentation changes executable CI observations on which a later performance repair may rely. Measurement does not qualify for the governance-only exception."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "repository_tools/upgrade_rehearsal.py",
  ".github/workflows/candidate-evidence.yml",
  "tests/test_upgrade_rehearsal.py",
  "tests/test_ci_pipeline.py",
  "docs/engineering/ci-pipeline/work-orders/WO-CIP-009.md",
  "docs/engineering/ci-pipeline/verification/VER-CIP-005.md",
]

[relations]
implements = ["REQ-ECP-012"]
specifications = ["SPEC-ECP-007"]
verification = ["VER-CIP-005"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-11T17:09:29Z"
decided_by = "engineering-owner"
reason = "The accountable operator approved VER-CIP-005 and WO-CIP-009 and authorized diagnostic implementation and hosted runs on 2026-09-11: i approve both."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-11T17:10:20Z"
decided_by = "engineering-owner"
reason = "The operator authorized diagnostic implementation and hosted runs by approving both named artifacts on 2026-09-11 in response to the explicit start authorization question."
+++

# Work Order: Measure Windows and Linux upgrade rehearsal stages

## Lifecycle

The operator approved this WO and VER-CIP-005 and authorized diagnostic
implementation and hosted runs on 2026-09-11: "i approve both". The released
evaluator applied approval and start after passing the gates. No execution
delegation is proposed. Completion and assurance remain separate decisions.

## Objective

Identify where the real upgrade rehearsal spends time on hosted Windows and
Linux, while preserving the handover checks required by SPEC-ECP-007 ECP-PRD-008.
This is a diagnostic branch, not a performance optimisation or release.

## In scope

Baseline: main `6b30ed3d07f61f9d3a994392ce9564b2f46e1a4a`.
The motivating [run](https://github.com/mmzen/se_harness/actions/runs/34620678755)
spent 336 seconds in two Windows replays and 22 seconds in two Linux replays.
Its tested merge was `816e1231fab5d620a32469714b2058228c995971`.

1. Add opt-in timing to the existing rehearsal module. Measure Git archive,
   extraction, Git initialization/configuration, staging, commit creation,
   each evaluator invocation, scratch cleanup, and the complete replay.
2. Emit flushed start/end progress and a separate machine-readable timing
   file outside the checkout. Keep timing out of the semantic digest and
   original result schema. Identify nested timings so totals are not added twice.
3. Enable timing for both existing replays in each platform job. Retain the
   timing files beside the existing result files in GitHub Actions artifacts.
4. Read Windows Defender's runtime state and exclusions using Get commands
   only. Record runner image, OS, Python and Git versions with the run identity.
   Report unavailable diagnostics explicitly; do not invent an enabled state.
5. Add focused tests in the two existing test files. Run the normal PR pipeline,
   inspect each replay and platform, and download the raw diagnostic evidence.
   Repeat the complete diagnostic run once on the same commit if needed to
   distinguish a reproducible bottleneck from first-run or runner variability.

## Out of scope

No faster exporter, cache, parallel replay, removed check, reduced fixture,
Python upgrade, Defender setting change, permission change, or broader logging.
No product package change, managed-file edit, release, merge, historical evidence
rewrite, archive-limit increase, or verification-record preparation.

## Authorized decision envelope

After approval and start, choose internal timing helpers, progress wording and
an optional timing-output argument. Use monotonic elapsed time and fixed stage
names. Do not execute an extra rehearsal inside a pipeline run or duplicate
its full suite. Manual repeat runs remain separately identified observations.

The existing workflow controls acquisition, wheel hashes and both replays.
Preserve its triggers, dependencies, timeouts, trust boundaries and verdicts.
No new architecture or product rule is introduced by observing these steps.

## Constraints

Measurement is not a speed target. Missing measurements remain missing. Report
actual errors and retain partial timings on failure without hiding the original
failure. Optional diagnostic errors must not turn failed handover checks green.
No secrets, broad environment dumps or unredacted subprocess output are logged.

The baseline archive has 9,998 entries against a 10,000-entry limit. This packet
adds exactly two files in existing directories. Executable instrumentation and
tests modify existing files only; runner output stays outside the checkout.
Download GitHub artifacts before expiry and record their hashes in the report.
Do not add tracked evidence or later VREC files within this bounded measurement.
A durable evidence/VREC delivery needs a separately reviewed archive-capacity
plan before completion or assurance is claimed; this packet grants no waiver.

## Expected change surface

Two new draft artifacts, followed after approval by modifications to the four
existing executable/test files. No diagnostic data is a tracked source input.

## Required verification

Pass VER-CIP-005. Use the isolated released 0.17.0 evaluator for governing
checks. Match the actual CI head and tested merge, not a local checkout label.
Keep the two replay digests and Windows/Linux agreement checks unchanged.

## Evidence to record

Retain raw job logs, timing/result files, runtime diagnostics, workflow/run/job
identities, file counts, exact commands and hashes outside the repository.
Provide a compact stage comparison and distinguish hosted facts from local
measurements and hypotheses. Link it from the PR report when requested.

## Stop and escalate conditions

Stop on a changed handover verdict or digest, changed isolation, credential
exposure, missing authority, failed required checks, scope expansion, new
tracked files beyond the packet, or archive overflow. Do not optimise while
measuring or present a local profile as the hosted result.

## Completion report format

Report per-replay and per-platform timings, the confirmed largest stages,
Defender's observed state, missing data, and measurement limitations. Preserve
WO state and the boundary between an observation and formal completion,
verification or integration. Propose a repair only after the measurements.
