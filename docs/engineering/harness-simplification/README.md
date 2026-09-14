# Harness simplification

The owner accepted all 38 candidates from the 2026-09-13 codebase KISS review and requested seven bounded work orders through the established delegated route.
The packet includes one shared replacement specification, an architecture decision, and a verification contract. It retains seven useful protections.

| Order | Work order | Outcome | KISS candidates |
| --- | --- | --- | --- |
| 1 | [WO-KIS-001](work-orders/WO-KIS-001.md) | Remove everyday input and writing blockers | 01, 02, 03, 07, 11, 35, 36, 37 |
| 2 | [WO-KIS-002](work-orders/WO-KIS-002.md) | Let local work progress on its own evidence | 04, 05, 06, 08, 09, 10, 12 |
| 3 | [WO-KIS-003](work-orders/WO-KIS-003.md) | Cut repeated identity proofs and locked guidance | 13, 14, 15, 16, 17, 18, 19, 20, 21, 22 |
| 4 | [WO-KIS-004](work-orders/WO-KIS-004.md) | Simplify verification and release records | 23, 24, 30, 38 |
| 5 | [WO-KIS-005](work-orders/WO-KIS-005.md) | Shorten CI and resume interrupted publication | 25, 26, 27, 28, 29 |
| 6 | [WO-KIS-006](work-orders/WO-KIS-006.md) | Keep new evidence small and assess historical archives | 31 |
| 7 | [WO-KIS-007](work-orders/WO-KIS-007.md) | Delete tests for the restrictions we removed | 32, 33, 34 |

- [Exact coverage](coverage.md), [replacement rules and compatibility](specifications/SPEC-KIS-001.md), [verification plan](verification/VER-KIS-001.md).
- [Recorded request](evidence/WO-KIS-001/governance/owner-request.md) and [accepted review](evidence/WO-KIS-001/governance/accepted-review.md).

The owner started WO-KIS-001 after merging the approved packet. It is implemented, owner-verified and merged. WO-KIS-002 is implemented, owner-verified and merged. WO-KIS-003 is implemented, owner-verified and merged. WO-KIS-004 is implemented; WO-KIS-005 through WO-KIS-007 remain approved and have not started.

[WO-KIS-001 implementation evidence](evidence/WO-KIS-001/implementation/README.md) records the first eight cuts, passing local checks and passing hosted CI. [VREC-KIS-001](verification-records/VREC-KIS-001.md) was verified by the owner and merged in PR #467; it binds the completion commit whose hosted checks all passed.

The intended order is sequential because several slices share code. Each work order remains separately selected and assessed.
This definition packet starts none of them. Current root governance remains released 0.17.0; the proposed local-delegation rule is future candidate behavior.
Historical archive work assesses existing bundles and shrinks new evidence; it does not silently delete old bound evidence.

[WO-KIS-002 implementation evidence](evidence/WO-KIS-002/implementation/README.md) records seven cuts and passing local source/package checks. Hosted CI passed. [VREC-KIS-002](verification-records/VREC-KIS-002.md) is verified by the owner. Integrated in PR #468.

[WO-KIS-003 implementation evidence](evidence/WO-KIS-003/implementation/README.md) records ten cuts and passing local source/package checks. Hosted checks passed; [VREC-KIS-003](verification-records/VREC-KIS-003.md) is verified by the owner. Integrated in PR #469.

[WO-KIS-004 implementation evidence](evidence/WO-KIS-004/implementation/README.md) records four cuts and passing local source/package checks. Hosted checks passed; [VREC-KIS-004](verification-records/VREC-KIS-004.md) is ready for owner verification.
