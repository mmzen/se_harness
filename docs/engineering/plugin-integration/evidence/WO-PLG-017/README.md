# Windows evidence-path repair

The operator approved WO-PLG-017 and the released evaluator applied its delegated
start. The 55-file native-product relocation preserves every original byte and
passes ordinary Windows checkout and independent corruption checks. The checker
is pinned to the exact approved plan; existing VREC008 and its sidecar remain
unchanged. Original C/G commits remain ancestors.

**The repair is not complete.** PR449 now passes checkout but fails inside the
deeper upgrade rehearsal during Git staging of one additional retained JSON.
Its downstream integration jobs are skipped. See the
[full CI observation](checks/ci-rehearsal-failed/result.json).

- [Original approved plan](path-plan.json), [approval](approval/) and [start](start/).
- [Original PR445 failure](pr445-windows-checkout.log) and [PR446 failure](pr446-windows-checkout.log).
- [Independent review and correction](checks/independent-review/followup-ed31a520.json).
- [Proposed one-file scope extension](scope-extension.md), awaiting owner approval.

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
No additional evidence path, historical decision, aggregate VREC or PR merge has
been authorized by the current repair approval.
