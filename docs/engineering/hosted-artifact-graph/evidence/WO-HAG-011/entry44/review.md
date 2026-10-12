# Review: distinguish the outcome from its implementation

The C43 full native lifecycle passes for both hosts. The separate first focused
Claude diagnostic still fails; both results and all failures are retained:
[full qualification](../../WO-HAG-009/final43-result/assessment.md) and
[focused diagnostic](../focused43-result/assessment.md).

Replace one paragraph in hosted-drafts.md. It clarifies the existing requirement
to establish the user's problem, intended improvement and way to observe success.
A channel, message or function is a solution choice. An unmeasured baseline does
not replace the required success measure. Reuse confirmed inputs.

This is explanatory guidance under WO-HAG-011. No task answer, qualification
criterion, canonical instruction, endpoint, lifecycle policy, host setting,
dependency or test-driver behavior changes. Replacing the existing paragraph
avoids a second rule source or another tool. The diff adds 174 bytes.

Focused resource/native/plugin checks, full source tests, distribution and CLI
checks pass. Released validation and both review preflights pass. Exact results
and the failed prior diagnostic are retained. Both previous disposable service
pairs were stopped with volumes preserved before modifying this checkout.

The new packaged candidate must first pass a fresh Claude EFF-04A2 diagnostic.
Only then may the remaining focused sequence proceed. Required full NQ evidence
must be assessed against final guidance. Keep the PR draft; no actual assurance,
merge, release or authority switch is inferred. CI's separate 512 MiB archive
limit failure remains disclosed and needs new bounded correction authority.
