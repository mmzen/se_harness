# SE Harness 0.20.1 compatibility release

Status: the package is approved and WO-RLS-027 is in progress. Release,
publication and adoption decisions remain separate.

[DEC-IAR-004](../instruction-architecture/decisions/DEC-IAR-004.md) records
mmzen's selected sequence: compatibility maintenance release, separate adoption,
then independent qualification of the minimal-layout successor.

| Artifact | Purpose |
| --- | --- |
| [SPEC-RLS-001](specifications/SPEC-RLS-001.md) | Assess both candidate layouts while preserving the 0.20 installer and independent verification. |
| [VER-RLS-027](verification/VER-RLS-027.md) | Windows/Linux checks, exact minimal wheel input, legacy compatibility, independent qualification and release evidence. |
| [WO-RLS-027](work-orders/WO-RLS-027.md) | Bounded implementation, version metadata, listed documentation, local checks and verification preparation. |
| [REL-SEH-032](release/REL-SEH-032.md) | Release membership, evidence, five-surface delivery and separate adoption. |

The proposed version is 0.20.1. The public release/0.20 baseline is
7253d13b212ad6f7df670021290fea32e81d66de. Its installed root selects 0.19.0;
its own matching released evaluator must govern that maintenance checkout.
The current successor checkout stays on 0.20.0. This package changes neither.

Human mmzen approved the four artifacts and required commit-bound assurance.
The recorded decisions retain mmzen's identity through the maintenance evaluator's
0.19.0 role labels. Push/PR, hosted workflow dispatch, verification acceptance,
release, publication, markers and adoption remain separate decisions.

This repository-owned index provides navigation. Formal authority comes from the
linked artifacts, their typed relations and recorded lifecycle decisions.
