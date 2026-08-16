# WO-VSP-005 aggregate publication-envelope evidence

Date: 2026-08-16

## Scope and authority

The repository owner instructed completion of the restored supersession transaction. This evidence covers the bounded integration and publication envelope for `WO-VSP-003` and `WO-VSP-004`. It authorizes a candidate commit, normal push, one PR declaring `WO-VSP-005`, and preparation of an aggregate ready VREC. It does not grant assurance, merge, release, publication, deployment, or another lifecycle decision.

## Aggregate scope

| Work order | Authorized decision | Retained evidence |
| --- | --- | --- |
| `WO-VSP-003` | `VREC-DST-006 -> VREC-SEH-005` | `docs/engineering/verification-supersession/evidence/WO-VSP-003-verification.md` |
| `WO-VSP-004` | `VREC-AGR-001 -> VREC-PMI-001` | `docs/engineering/verification-supersession/evidence/WO-VSP-004-verification.md` |
| `WO-VSP-005` | publish both decisions as one bounded candidate | this document |

Both sources are retained as `superseded`; both successors remain verified, coverage-preserving, and unchanged. No active release record references either source. Captured source commits, object formats, worktree assertions, timestamps, snapshots, evidence paths, original work-order relations, and original verification-contract relations remain unchanged.

## Verification

- Formal validation passes with 344 artifacts, zero errors, and the existing 40 maintenance warnings.
- Review preflight passes for `WO-VSP-003`, `WO-VSP-004`, and `WO-VSP-005` with the complete VSP governing chain.
- Managed-integrity doctor passes and retains only the known canonical-location advisories.
- Python 3.11.9 and Python 3.14.6 each pass 188 tests with 3 expected Windows symlink skips.
- The focused revision-provenance, dashboard, and inspection suite passes 48 tests with 1 expected skip.
- Repeated JSON inspection output is byte-identical at SHA-256 `a3a124a4ab8372c103db3a494f09d0d28d2dc2390796f3d392b0d09c195a65eb`; each report contains 344 artifacts, 1,241 relations, 72 findings, 15 suggestions, and no finding referencing either superseded source.
- Repeated Explorer generation reports snapshot SHA-256 `d87ef48dd72b146c3f71f00cf43cb1ed29b52c2464ac709c1ad42c685cb84f07` and rendered HTML SHA-256 `cde34935dcd9888cc08201170f30df87b827caca3fa4a176cded9dffebd1a6b9`.
- Diff hygiene passes, and the change surface is limited to both source transitions, the three work orders and evidence, and the VSP index.

## Candidate and assurance boundary

The clean candidate will be created after this evidence enters the tree. `harnessctl capture-verification` may then prepare one aggregate record covering all three work orders, the shared `VER-VSP-001` contract, and all three evidence paths. The record must remain `ready` until an accountable assurance owner explicitly reviews and approves it.
