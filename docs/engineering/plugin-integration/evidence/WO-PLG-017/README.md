# Windows checkout repair

PR445 and PR446 fail during Windows checkout, before the upgrade test runs.
Their Linux/source/validate passes do not cancel this failure. The root cause is
the depth of retained WO011 native products, introduced during evidence retention.

The approved work order shortens 55 paths and retains all bytes through an exact
path/hash map. This directory contains the original failure logs, owner approval,
delegated start and repair checks. Implementation is in progress.

- [Proposed work order](../../work-orders/WO-PLG-017.md)
- [Exact proposed relocation map](path-plan.json)
- [PR445 failure log](pr445-windows-checkout.log)
- [PR446 failure log](pr446-windows-checkout.log)

The early WO011 completion used the live validate gate and successful source
checks before the failed Windows result was accounted for. That was insufficient
verification of the full CI outcome. The historical completion and ready record
are preserved; they are not evidence that this newly identified gate passed.

## Implementation underway

The actual released evaluator enabled and applied delegated start at ed19676,
check-run 103052409603. The already-merged definition carries the execution class
at the base; the explicit approval is recorded on this branch. The earlier
statement that approval PR448 must merge before any start was too strict.
No external PR merge was performed by this agent.

All 55 planned captures have moved to shallow paths with identical SHA-256.
Original records and source manifests remain preserved. The path reconciliation
check passes; fresh Windows checkout, independent tamper detection, Linux replay
input reconciliation and the full CI outcomes remain pending. WO-PLG-017 stays
in_progress until these checks pass.
