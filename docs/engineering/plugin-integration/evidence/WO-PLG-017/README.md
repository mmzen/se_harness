# Windows evidence-path repair

The operator approved WO-PLG-017 and the released evaluator applied its delegated
start. The 55-file native-product relocation preserves every original byte and
passes ordinary Windows checkout and independent corruption checks. The checker
is pinned to the exact approved plan; existing VREC008 and its sidecar remain
unchanged. Original C/G commits remain ancestors.

**The repair is not complete.** The previous PR449 candidate passed checkout
but failed Git staging of one additional JSON in the deeper upgrade rehearsal.
The operator approved the exact one-file extension on 2026-09-11; it is now
implemented, with a supplemental map and two path profiles. Acceptance and CI
at the corrected candidate remain pending. The previous downstream jobs were
skipped. See the
[full CI observation](checks/ci-rehearsal-failed/result.json).

- [Original approved plan](path-plan.json), [approval](approval/) and [start](start/).
- [Original PR445 failure](pr445-windows-checkout.log) and [PR446 failure](pr446-windows-checkout.log).
- [Independent Windows/Linux results](acceptance/independent/REPORT.md) and [exact retention inventory](acceptance/independent/inventory.json).
- [Independent review and correction](checks/independent-review/followup-ed31a520.json).
- [Proposed one-file scope extension](scope-extension.md), approved with its [decision receipt](approval/scope-extension.json).

The local Windows source suite separately failed in unchanged fixture cleanup
with WinError5 on a Git object (1 error,23 skips). Its original output is retained
under checks/windows-source-failed. Candidate source CI at ed31a520 passed
1,134 tests with four skipped. These are separate observations; the local run is
not relabeled successful. Candidate doctor retains the six known candidate/root
template differences; the governing released doctor and graph validation pass.

The early WO011 completion used validate/source passes before its full Windows
outcome was accounted for. That was insufficient. Its historical completion and
ready record are preserved; they do not establish a successful Windows result.
WO-PLG-017 remains in_progress, and WO-PLG-012 remains paused at this failure.
The one additional path was explicitly authorized. Historical decisions,
aggregate VREC preparation and PR merge remain outside that approval.

The released scope check passes against the declared repair paths and the live
validate job is successful. This does not make the failed Windows rehearsal a
pass. Completion remains stopped under ENGINEERING_HARNESS.md's required-check
rule and the work order's explicit scope boundary. No completion transition was
applied in response to the narrower delegation gate.
