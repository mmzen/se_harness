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
  ".github/scripts/build_integration_package.py",
  "tests/test_integration_package.py",
  "docs/engineering/ci-pipeline/work-orders/WO-CIP-009.md",
  "docs/engineering/ci-pipeline/verification/VER-CIP-005.md",
  "docs/engineering/ci-pipeline/evidence/WO-CIP-009/",
]

[relations]
implements = ["REQ-ECP-012", "REQ-IPK-001"]
specifications = ["SPEC-ECP-007", "SPEC-IPK-001"]
architecture = ["ARCH-IPK-001", "ADR-IPK-001"]
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
The authorized scratch-placement amendment also tests explicit storage location.
No release is authorized.

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
6. Under the capacity amendment below, raise the integration-package archive
   member limit from 10,000 to 20,000, test the boundary and retain the bounded
   handoff evidence needed by this WO. This does not optimize the rehearsal.
7. Under the scratch-placement amendment below, expose the temporary and Git
   storage paths and place both disposable replays under RUNNER_TEMP. Compare
   their observed durations with the retained default-location baseline.

## Out of scope

No faster exporter, cache, parallel replay, removed check, reduced fixture,
Python upgrade, Defender setting change, permission change, RAM disk, or broader logging.
No product package change, managed-file edit, release, merge, historical evidence
rewrite, or verification-record preparation. The only archive-limit change
is the 20,000-entry capacity amendment below.

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

The original measurement candidate has exactly 10,000 archive entries. The
authorized amendment raises the integration-package extraction limit to 20,000
entries, counting both files and directories. Keep the 128 MiB member limit,
512 MiB archive/expanded-total limits, and every path and member-type check.
No automatic limit growth, bypass, CLI override or evidence deletion is allowed.
Retain compact handoff evidence under this WO's evidence directory. Large raw
logs and wheel files remain downloaded outside the checkout; record hashes and
run links. Verification-record preparation still requires separate authority.

## Expected change surface

Two formal artifacts, six existing executable/test files, and this WO's bounded
handoff evidence directory. Diagnostic data is not an input to package behavior.

## Required verification

Pass VER-CIP-005. Use the isolated released 0.17.0 evaluator for governing
checks. Match the actual CI head and tested merge, not a local checkout label.
Keep the two replay digests and Windows/Linux agreement checks unchanged.

## Evidence to record

Retain raw job logs and wheel files outside the repository. Keep compact timing,
runtime, test and handoff evidence under this WO, naming exact workflow/run/job
identities, file counts, commands and hashes.
Provide a compact stage comparison and distinguish hosted facts from local
measurements and hypotheses. Link it from the PR report when requested.

## Stop and escalate conditions

Stop on a changed handover verdict or digest, changed isolation, credential
exposure, missing authority, failed required checks, scope expansion, new
tracked files outside the declared scope, or archive overflow. Do not introduce
optimisations beyond the authorized scratch placement or present a local profile
as the hosted result.

## Completion report format

Report per-replay and per-platform timings, the confirmed largest stages,
Defender's observed state, missing data, and measurement limitations. Preserve
WO state and the boundary between an observation and formal completion,
verification or integration. Propose a repair only after the measurements.

## Authorized capacity amendment — 2026-09-11

The accountable operator authorized the repair with "you can raise the limit"
after the implementation limit and the evidence blockage were explained.
This is authority to extend WO-CIP-009 and its verification coverage for that
repair and necessary handoff evidence. Lifecycle states remain unchanged.

The bounded choice is 20,000 entries: twice the exhausted limit, while keeping
all byte budgets and safe-extraction checks. Add only the packaging script,
its existing test file, and this WO's evidence directory to execution scope.
REQ-IPK-001 and SPEC-IPK-001 govern the exact-commit export and safety boundary.
Re-run the affected tests and normal CI, including Windows/Linux integration
verification. Do not reinterpret historical WO-PLG-018 evidence or its 10,000
entry constraint: it describes the earlier accepted integration candidate.

## Authorized scratch-placement amendment — 2026-09-11

The operator's "ok go" authorizes the proposed first step: make the scratch
location explicit and observable. The retained baseline run 34630231918 used
Python's default temporary directory, whose resolved path was not recorded.
Record that default, the selected workspace, actual disposable repository and
Git-resolved index/object locations. Limit environment observations to TMPDIR,
TEMP, TMP and RUNNER_TEMP. Paths are diagnostics, not semantic-digest inputs.

Expose the existing workspace argument as an optional CLI option. An explicit
workspace must be an existing directory outside the operational checkout; reject
invalid, missing and checkout-contained paths before writing. Preserve unique
temporary subdirectories and cleanup. Without the option, preserve Python's
default selection, subject to the same checkout boundary.

Set the two existing platform replays to RUNNER_TEMP, resolved by the runner
rather than a hard-coded drive. Keep their wheel, sequence and verdict checks.
Git-path queries are bounded read-only diagnostics, timed separately; failure
must remain visible and must not create a false complete measurement.
Test default/explicit placement, invalid paths, cleanup, diagnostics and unchanged
results. Re-run normal CI and retain exact-head evidence. Cross-run differences
are observations, not proof of drive performance; the older run did not capture
its scratch path. No RAM disk, extra replay, security setting or lifecycle
transition is authorized by this amendment. Execution paths remain unchanged.
