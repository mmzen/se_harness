# WO-KIS-010 implementation review

Status: local implementation checks passed; verification has not been accepted.
The human approved WO-KIS-011 and required commit-bound verification. The selected
evaluator recorded that approval and start. The combined handoff passed from the original main baseline. The released
evaluator applied completion for both work orders; both are implemented.
Their current next procedure is commit-bound verification preparation.

## Outcome and design

The candidate adds optional check --planned-path input. It reports coverage
of an explicitly supplied file list under one selected work order.
The normal lifecycle projection and its exit meaning remain unchanged.
Coverage is not approval, a gate result or proof of complete impact analysis.

One small read-only helper reuses declared_change_set, execution_scope,
path_is_admitted, own_record_paths, safe_destination and the existing packet
destination. It consumes the validated catalog already built by projection;
a test asserts one repository validation. No new command family, artifact,
persistent inventory, gate, lifecycle edge or dependency was introduced.
The helper is separate because proposed-path reporting is not actual-change
evidence. Existing admission behavior and owner content remain unchanged.

## Approved scope and baseline

The human approved REQ-KIS-010, SPEC-KIS-004, VER-KIS-004 and WO-KIS-010
after reviewing PR #523. The selected released 0.21.0 evaluator applied that
decision under mmzen and started WO-KIS-010 under Codex agent.
The retained approval and start results identify the exact reviewed inputs.

The implementation branch is work/complete-scope-implementation, based on
ccbfbdec811d722974336924125b070d91f111f4. PR #523 remains the separate proposal
snapshot. Its review Markdown is not part of this implementation diff.

The approved paths cover the CLI, projection, renderer, new helper and tests,
six documentation/template files, this package and this evidence directory.
No edits to existing test modules, workflow_change_set, CI or packaging were
needed. A generated diagnostic index dependency was missed during planning:
docs/notes/diagnostic-codes.md needs two updated message counts. WO-KIS-011
authorizes that exact correction. Regeneration changed only the two reviewed
counts, and the generator check now passes.

## Requirement-to-result assessment

| VER-KIS-004 case | Observed evidence | Current assessment |
| --- | --- | --- |
| A: planned paths | tests.test_scope_preparation covers exact files, missing future files, component children, prefix lookalikes, omitted files and reasons. | Focused cases pass. |
| B: automatic outputs | Tests cover the selected WO, linked VREC/RLS and evaluator paths, packet directory, unrelated record and neighboring evidence. | Focused cases pass. Automatic paths reuse existing rules. |
| C: refusal and invariants | Tests cover invalid paths, case duplicates, incompatible flags, missing/non-WO selections, no writes and invalid scope. | Cases pass locally except the explicit Windows symlink privilege skip. Linux CI remains required at integration. |
| D: compatibility and integrity | Projection fields match the ordinary result after removing only preparation and its digest; changed planning data changes the digest. Existing workflow suites and one-validation test run. | Focused cases and the final full suite pass. |
| E: instructions and request | Reviewed the authoring checklist link, preparation procedure, shared generated-output reference, WO template, approval decision card and CLI reference. | Meets the accepted content; this is inspection, not a measured usability score. |
| F: complete outcomes | Both temporary repositories detect an omitted planned test before approval, reject an unrelated later path, retain one unchanged approved scope through handoff and ready VREC capture. | Both corrected demonstrations pass. Fixture decisions do not establish human or live-host evidence. |

For E, the decision card names the outcome, why, supporting changes, success
checks, material limits and permission before the technical review links.
Guidance uses existing procedure entry points; startup instructions are not
expanded. The shared reference distinguishes exact linked-record admission
from the selected WO's existing evidence-directory admission. Unknown future
record IDs stay unresolved until the actual generated paths can be checked.

The demonstrations now execute the new regression assertion against old
behavior first, then verify the corrected result. This is stronger than a
fixture that only passes after setup. Two demonstrations do not prove that
an agent will always discover the complete impact or quantify interruption
reduction across real projects. This actual change missed the diagnostic
index, which is retained as a preparation finding rather than hidden.

## Retained check results

| Evidence | Result |
| --- | --- |
| focused-tests.log | 161 tests, OK, 2 skips; before final demonstration additions. |
| focused-final.log | Final coded-error implementation and corrected demonstrations: 163 tests, OK, 2 skips (161 passed). |
| instruction-tests.log | 75 tests, OK, 1 skip. |
| demonstrations-third.log | 2 demonstrations passed before adding explicit before-fix execution. |
| full-suite.log | 1,233 tests, 4 failures, 22 skips. Three failures are diagnostic-index drift; one was a demonstration fixture error corrected afterward. |
| full-suite-final.log | 1,233 tests, OK, 22 skips: 1,211 passed. Includes both corrected demonstrations and all diagnostic-index checks. |
| correction-tests.log | 29 tests, 3 failures, 1 skip. Both corrected demonstrations passed. Remaining failures are diagnostic-index drift. |
| released-validation.json.gz | Selected evaluator validation passed before correction drafting. Subsequent draft validation also returned exit 0. |
| released-doctor.json | Selected installation-integrity check passed. |
| distribution-check.log | 21 distribution-bearing records passed. |
| cli-help.log | Help includes the new optional flag. |

The exact final focused invocation and runtime are retained in
focused-final-command.json. The final suite passed. Source, test and instruction bytes were unchanged after
the final suite started. Only retained evidence and evaluator-applied completion
history were added before the clean candidate commit. The generated record
identifies that exact commit.

The generated correction preview is retained in diagnostic-index-proposed.patch.
WO-KIS-011 validated with zero errors. Its reviewed SHA-256 is
63456285024da8f9ddfe8a715f13a929718b72bde32ed062ff5248ec8e46eacd.

## Failures and resolutions

1. The first linked-output fixture repeated evaluator_evidence_path, making
   its TOML invalid. The fixture now replaces the existing field.
2. The first demonstration named a not-yet-created review file in the WO
   before transition. It now uses the supported evidence command after checks.
3. The second demonstration used a legacy WO identifier rejected by public
   preflight. It now uses the canonical fixture WO-PRD-001 and its links.
4. The full-suite bug demonstration read the old unprefixed fixture during
   before-fix execution, so the test passed unexpectedly. Its new assertion
   explicitly exercises the required prefixed input before reading the fixture.
5. Additional coded diagnostics require regenerating two counts in the index.
   A temporary experiment using generic errors reduced index drift but was
   reverted: the candidate retains the normal coded diagnostics. The right
   correction is the generated reference update proposed in WO-KIS-011.
   No test was relaxed and no generated index change was applied without scope.

Original failures remain in the logs and task transcript. The final focused
rerun assesses the retained coded-error implementation.

## Remaining limits

- The new symlink-escape case is skipped on this Windows host because link
  creation lacks the required privilege. It must run on Linux CI.
- Hosted Linux/Windows CI has not run for this implementation branch.
- Local required checks, combined handoff and completion passed. The generated
  verification record binds the exact subsequent clean candidate commit. No VREC has been accepted, implementation pushed, or release
  performed.
- The repository and installed plugin continue to use released evaluator
  0.21.0. New behavior reaches users only through later release and adoption.


## Final local handoff

The selected evaluator passed the combined scope and handoff check for both
work orders. The complete Git diff used baseline
ccbfbdec811d722974336924125b070d91f111f4. A local event file selected both
work orders; no remote PR was created by this check. The initial Windows
long-path refusal and the successful process-local correction are retained
in handoff-environment.md and combined-handoff-longpaths.json. Completion
preview and apply outputs retain both exact selected IDs and the actual actor.

Large successful validation outputs are retained losslessly as .json.gz;
validation-output-encoding.json records their original and compressed hashes.
Failed test outputs remain directly readable. The final assessment records
no unresolved local functional failure. The Windows symlink skip and hosted
CI remain visible integration limitations, not passing test claims.
