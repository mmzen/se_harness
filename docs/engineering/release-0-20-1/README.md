# SE Harness 0.20.1 compatibility release

Status: WO-RLS-027 is implemented and VREC-SEH-030 is verified. RLS-SEH-030
is ready with the exact 0.20.1 build binding. The downstream work below is
draft. Bound-record replay, release, publication and adoption remain pending.

[DEC-IAR-004](../instruction-architecture/decisions/DEC-IAR-004.md) records
mmzen's selected sequence: compatibility maintenance release, separate adoption,
then independent qualification of the minimal-layout successor.

| Artifact | Purpose |
| --- | --- |
| [SPEC-RLS-001](specifications/SPEC-RLS-001.md) | Assess both candidate layouts while preserving the 0.20 installer and independent verification. |
| [VER-RLS-027](verification/VER-RLS-027.md) | Windows/Linux checks, exact minimal wheel input, legacy compatibility, independent qualification and release evidence. |
| [WO-RLS-027](work-orders/WO-RLS-027.md) | Bounded implementation, version metadata, listed documentation, local checks and verification preparation. |
| [REL-SEH-032](release/REL-SEH-032.md) | Release membership, evidence, five-surface delivery and separate adoption. |
| [VREC-SEH-030](verification-records/VREC-SEH-030.md) | Human-verified candidate b9af631b850c495eace9807361ed3ec3e36a10b2. |
| [RLS-SEH-030](releases/RLS-SEH-030.md) | Ready 0.20.1 release record; no release decision applied. |
| [WO-RLS-028](work-orders/WO-RLS-028.md) / [VER-RLS-028](verification/VER-RLS-028.md) | Draft: released-baseline plugin 0.2.3 source, governance transport and package qualification. |
| [WO-RLS-029](work-orders/WO-RLS-029.md) / [VER-RLS-029](verification/VER-RLS-029.md) | Draft: public fresh/update checks, current documentation and delivery closeout. |

The proposed version is 0.20.1. The public release/0.20 baseline is
7253d13b212ad6f7df670021290fea32e81d66de. Its installed root selects 0.19.0;
its own matching released evaluator must govern that maintenance checkout.
The current successor checkout stays on 0.20.0. This package changes neither.

Human mmzen approved the original four-artifact package and its required
commit-bound assurance, later verified VREC-SEH-030, and authorized release-record
preparation. The four downstream drafts still require their own approval.
The recorded decisions retain mmzen's identity through the maintenance evaluator's
0.19.0 role labels. New review-branch pushes and read-only bound-record replay are proposed in
WO-RLS-028. Downstream verification, release, publication, markers and adoption
remain separate decisions.

This repository-owned index provides navigation. Formal authority comes from the
linked artifacts, their typed relations and recorded lifecycle decisions.

The [updated delivery plan](evidence/RLS-SEH-030/delivery-plan.json) binds the
known release identities and proposed downstream assignments. It awaits human
review; unknown package/source/public identities remain pending. The earlier
plan and all VREC-bound evidence remain unchanged.
