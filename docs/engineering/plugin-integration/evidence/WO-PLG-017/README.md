# Windows checkout repair proposal

PR445 and PR446 fail during Windows checkout, before the upgrade test runs.
Their Linux/source/validate passes do not cancel this failure. The root cause is
the depth of retained WO011 native products, introduced during evidence retention.

The proposed work order shortens 55 paths and retains all bytes through an exact
path/hash map. This directory contains the proposal and original failure logs;
no relocation or successful repair is claimed. The later explicit owner approval
is retained under approval; the work order is approved but has not started.

- [Proposed work order](../../work-orders/WO-PLG-017.md)
- [Exact proposed relocation map](path-plan.json)
- [PR445 failure log](pr445-windows-checkout.log)
- [PR446 failure log](pr446-windows-checkout.log)

The early WO011 completion used the live validate gate and successful source
checks before the failed Windows result was accounted for. That was insufficient
verification of the full CI outcome. The historical completion and ready record
are preserved; they are not evidence that this newly identified gate passed.
