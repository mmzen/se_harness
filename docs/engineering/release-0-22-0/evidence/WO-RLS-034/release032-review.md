# Release 0.22.0 decision review

VREC-SEH-032 is verified by mmzen. RLS-SEH-032 is ready for the separate
release-owner decision reserved in the approved package. The record binds the
same tested candidate and the exact reproducible distribution archives.

## Decision requested

Authorize [RLS-SEH-032](../../releases/RLS-SEH-032.md) for evaluator 0.22.0,
tag `v0.22.0`, and candidate `abbec12ac5524c8adfb28693f846dd59de88f759`.
Reviewed record SHA-256: `49ad1f26ea9cc90d1325e75904684454f29a83a75f954548870e15a79bccaaae`.
The release record includes the ten work orders in
[REL-SEH-034](../../release/REL-SEH-034.md), covered by the verified
[VREC-SEH-032](../../verification-records/VREC-SEH-032.md).

Suggested response: **I authorize release record RLS-SEH-032.**

## Evidence

- Human verification was recorded in decision commit
  `57cdf5ea70abb9a940ca603c8efb93ee72f65723` and pushed to PR #528.
- [Bound-record replay](https://github.com/mmzen/se_harness/actions/runs/37090350595) passed at review commit
  `bd3a165b9a2e89e84ba8b41dda9351b1f4d95710`. Both pinned builds reproduced the complete recorded bundle.
- The [retained replay](release032-build-replay.json),
  [release gate result](release032-gates.json), and
  [structured review](release032-review.json) identify the exact inputs.
- The earlier [verification review](verification-review.md) retains full-scale
  Windows/Linux tests, installed-package and upgrade checks, original failures,
  platform skips and their limits. No source changed after that verification.
- Released-evaluator validation reports zero errors and 60 warnings: 58
  historical warnings, plus two valid domain-location notices for this VREC
  and RLS. Distribution validation passes for all 22 distribution-bearing records.

| Archive | SHA-256 |
| --- | --- |
| `se_harness-0.22.0-py3-none-any.whl` | `44543f242ed19bb30cfd65da415372a87508a6e439204d7f3e37f9f45aefe4e4` |
| `se_harness-0.22.0.tar.gz` | `3bc9ddb9b1d046dc111c5582b7d857cc815c8e2fb9f8255ec07bda56315ef52a` |

## Delivery after the decision

After the record decision and the separately controlled merge, the retained
release-execution grant supports publication through the existing protected
publisher. It creates the immutable evaluator distribution, version tag,
maintenance line and Pages deployment. The PyPI environment still requires
its configured human reviewer action.

WO-RLS-035 then owns plugin 0.2.5 assembly from the public wheel, current native
qualification and marketplace delivery. WO-RLS-036 owns public route checks,
current documentation, Pages readback and latest/last promotion after the
observation window. Required downstream human verification remains separate.
No prior release's accepted host-test omissions are reused.

The repository continues to use evaluator 0.21.0. Adoption and activation of
the new complete-release route require their separately reviewed follow-up.
This review claims no publication, marketplace update, marker change or adoption.

## Limits and recovery

The previously disclosed direct-file sdist initialization restriction remains:
named/index-selected source installation and wheel installation pass. The
accepted verification review describes the unchanged provenance limitation.

A changed candidate requires new build and verification evidence before release.
After publication, preserve the version archives and tag; corrections need a new
version. Inspect remote state before retrying a partial publication. Do not force
marketplace history or replace a conflicting maintenance ref. Latest/last moves
require the contract's completed observations and the exact expected old ref.
Delivery stays incomplete while a required surface or test remains outstanding.
