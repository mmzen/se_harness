# Published evaluator 0.23.0 and plugin 0.2.7

Current status: **RLS-SEH-034 is released. VREC-SEH-034 and VREC-RLS-005 are verified
by mmzen. All five public delivery surfaces are complete.**

Binary candidate `48e851bbc94d7fb0c06e9b80666c3860cb5f8c15` covers 20 implemented
work orders and 11 verification contracts. The [candidate assessment](evidence/WO-RLS-045/verification-assessment-48e851bb.md)
and [VREC-SEH-034](verification-records/VREC-SEH-034.md) retain its qualification,
including 19 passing CI checks and accepted limits. PR #544 merged that verification.
[RLS-SEH-034](releases/RLS-SEH-034.md) binds the same candidate and archives.

[VREC-RLS-005](verification-records/VREC-RLS-005.md), merged through PR #548,
verifies the later public observations under WO-RLS-047. The
[closeout assessment](evidence/WO-RLS-047/closeout-assessment.md) and
[delivery result](evidence/WO-RLS-047/delivery-result.json) cover GitHub/PyPI,
marketplace, documentation, Pages, maintenance line and latest/last. Windows
Codex and Claude CLI fresh/update routes passed. Codex required native marketplace
registration recovery; its ordinary upgrade timeouts remain recorded.

The [frozen plan and review](evidence/WO-RLS-045/complete-release-review.md)
retain the release inputs and decision boundary. Published package README snapshots
remain unchanged; current source guidance reports the later delivery result.

Historical preparation: read the [earlier qualification report](evidence/WO-RLS-045/qualification-progress-6fa4d1a6.md),
[open instruction/desktop items](evidence/WO-RLS-054/open-items.md), and
[historical-rehearsal correction proposal](evidence/WO-RLS-055/preparation-review.md).
That earlier candidate was `6fa4d1a645660cd8022dfc5c3ee7ba35bda3d162`.
Its package, source and hosted checks passed; the separate historical-release
rehearsal failed at that point. WO-RLS-055 corrected that defect; the final
assessment above records the subsequent passing qualification and human verification.

R23-NATIVE-010/011 remain open under DEC-RLS-010 / RISK-RLS-008.
Codex Windows desktop remains deferred and unverified under DEC-RLS-011 / RISK-RLS-009.
These release-only decisions do not mark failed or unrun checks as passed.

Earlier candidate reports and correction reviews remain historical evidence.
Their original failures and blockers are preserved; use the current report above
for continuation.

Read the [preparation review](evidence/WO-RLS-045/preparation-review.md) for the
requested decision, concrete changes, evidence and limits.

The release makes the merged hosted client and plugin guidance available through
the normal distribution routes. The service remains a private sandbox built from
the tagged source. Git remains authoritative; no public service is proposed.

| Artifact | Purpose |
| --- | --- |
| [REL-SEH-036](release/REL-SEH-036.md) | Exact release membership, versions and the complete-release decision. |
| [WO-RLS-045](work-orders/WO-RLS-045.md), [VER-RLS-039](verification/VER-RLS-039.md) | Candidate versions, bounded build-helper correction, current docs and aggregate assurance. |
| [WO-RLS-046](work-orders/WO-RLS-046.md), [VER-RLS-040](verification/VER-RLS-040.md) | Exact plugin and hosted combination qualification, with marketplace review staging. |
| [WO-RLS-048](work-orders/WO-RLS-048.md) | Approved exact client-admission and instruction-map correction; linked release membership amendment. |
| [WO-RLS-049](work-orders/WO-RLS-049.md) | Implemented. One-file clarification/reporting correction. Earlier failures are retained; see current qualification report. |
| [WO-RLS-050](work-orders/WO-RLS-050.md) | Implemented. Content-readiness correction. Earlier failures are retained; see current qualification report. |
| [WO-RLS-051](work-orders/WO-RLS-051.md) | Implemented. Input-assessment correction. Earlier failures are retained; see current qualification report. |
| [WO-RLS-052](work-orders/WO-RLS-052.md) | Implemented. Source-support correction. Earlier failures are retained; see current qualification report. |
| [WO-RLS-053](work-orders/WO-RLS-053.md) | Implemented. Two-guide input-size correction. Earlier failures are retained; see current qualification report. |
| [WO-RLS-054](work-orders/WO-RLS-054.md) | Implemented. Early communication pointer and exact linked membership amendment. Earlier failures are retained; see current qualification report. |
| [WO-RLS-055](work-orders/WO-RLS-055.md) | Implemented historical-rehearsal correction, included in verified VREC-SEH-034. |
| [WO-RLS-047](work-orders/WO-RLS-047.md), [VER-RLS-041](verification/VER-RLS-041.md) | Public delivery and independently observed closeout after complete-release approval. |

Base: merged main `4fb5dbc29ffd7a2ccdc9a081c9c9b9f82b99d999`.
Historical preparation branch: `codex/release-0-23-0`, integrated into `main`.
Released 0.22.1 governed preparation and remains the private service evaluator.
Repository adoption under WO-HUP-031 selects 0.23.0; development source is 0.23.1.
Published plugin 0.2.7 bundles evaluator/client 0.23.0.

Use existing product and delivery definitions, build recipe, staging and
publisher. Retain the existing hosted combination manifest as a release-bundle
companion. No new artifact type, release pipeline or container registry is needed.

mmzen approved preparation, required commit-bound verification and bounded
review publication. The work-order lifecycle entries retain that exact decision.
The preparation review and its byte-bound checks preserve the original proposal.
Human verification, integration and the complete-release decision were followed
by the retained public delivery and closeout verification.

Codex desktop qualification remains unverified under the current release-only
DEC-RLS-011 disposition; follow-up is still required. Authentication/DB ACL work and broad performance
improvements remain deferred. RISK-HAG-001/002 remain raised. Repository adoption
and updates to the user's installed host plugins remain separate.
