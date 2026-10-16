# Proposed evaluator 0.23.0 and plugin 0.2.7 release

Status: **Package approved by mmzen. WO-RLS-045/046/048/049/050/051/052/053 are in progress; qualification and final verification remain pending. WO-RLS-047 is approved and unstarted.**

The [current qualification report](evidence/WO-RLS-045/qualification-progress-a98a1571.md)
records passing focused drafting, packages, hosted functionality and CLI delivery. Communication timing, local handoff and desktop evidence remain incomplete.
The [WO-RLS-049 correction](evidence/WO-RLS-049/implementation-review.md) is approved and implemented in source; its fresh Claude diagnostic failed content review; native repetitions are stopped and qualification remains incomplete.

The [WO-RLS-050 correction](evidence/WO-RLS-050/implementation-review.md) is approved and applied. Its fresh Claude diagnostic failed independent content review; native repetitions are stopped and qualification remains incomplete.

The [WO-RLS-051 correction](evidence/WO-RLS-051/implementation-review.md) is approved and applied. Its fresh Claude diagnostic failed; further native tests on this candidate are stopped.

The [WO-RLS-052 correction](evidence/WO-RLS-052/implementation-review.md) is approved and applied. Both missing-input diagnostics pass; the positive case is blocked before provider invocation by the 64 KiB input limit.

The [WO-RLS-053 correction](evidence/WO-RLS-053/implementation-review.md) is approved and applied. Both complete positive inputs fit and all focused cases pass. Full instruction timing and remaining delivery qualification are incomplete.

The [WO-RLS-054 proposal](evidence/WO-RLS-054/preparation-review.md) adds an early pointer to the existing communication section. It is draft and unapplied; validation reports zero errors and planned paths are covered.

Read the [preparation review](evidence/WO-RLS-045/preparation-review.md) for the
requested decision, concrete changes, evidence and limits.

The release makes the merged hosted client and plugin guidance available through
the normal distribution routes. The service remains a private sandbox built from
the tagged source. Git remains authoritative; no public service is proposed.

| Artifact | Purpose |
| --- | --- |
| [REL-SEH-036](release/REL-SEH-036.md) | Exact release membership, proposed versions and one complete-release decision. |
| [WO-RLS-045](work-orders/WO-RLS-045.md), [VER-RLS-039](verification/VER-RLS-039.md) | Candidate versions, bounded build-helper correction, current docs and aggregate assurance. |
| [WO-RLS-046](work-orders/WO-RLS-046.md), [VER-RLS-040](verification/VER-RLS-040.md) | Exact plugin and hosted combination qualification, with marketplace review staging. |
| [WO-RLS-048](work-orders/WO-RLS-048.md) | Approved exact client-admission and instruction-map correction; linked release membership amendment. |
| [WO-RLS-049](work-orders/WO-RLS-049.md) | Approved one-file clarification/reporting correction; qualification pending. |
| [WO-RLS-050](work-orders/WO-RLS-050.md) | Approved content-readiness correction; first new-candidate diagnostic failed. Qualification remains incomplete. |
| [WO-RLS-051](work-orders/WO-RLS-051.md) | Approved input-assessment correction; first Claude diagnostic failed and is retained. |
| [WO-RLS-052](work-orders/WO-RLS-052.md) | Approved source-support correction; both diagnostics pass; positive input assembly remains blocked. |
| [WO-RLS-053](work-orders/WO-RLS-053.md) | Approved two-guide correction; focused cases pass, full release readiness remains pending. |
| [WO-RLS-054](work-orders/WO-RLS-054.md) | Unapproved one-file early communication pointer; linked membership amendment is proposed only. |
| [WO-RLS-047](work-orders/WO-RLS-047.md), [VER-RLS-041](verification/VER-RLS-041.md) | Public delivery and independently observed closeout after complete-release approval. |

Base: merged main `4fb5dbc29ffd7a2ccdc9a081c9c9b9f82b99d999`.
Review branch: `codex/release-0-23-0`, proposed target `main`.
Released 0.22.1 continues to govern preparation and the private service.
The proposed plugin bundles the new 0.23.0 evaluator/client; these distinct
identities must be explicit in the actual combination and current instructions.

Use existing product and delivery definitions, build recipe, staging and
publisher. Retain the existing hosted combination manifest as a release-bundle
companion. No new artifact type, release pipeline or container registry is needed.

mmzen approved preparation, required commit-bound verification and bounded
review publication. The work-order lifecycle entries retain that exact decision.
The preparation review and its byte-bound checks preserve the original proposal. Human verification and merge precede the later frozen-plan
approval, which can cover all listed public outputs together.

Codex desktop qualification must be revisited; the previous release-specific
omission is not renewed here. Authentication/DB ACL work and broad performance
improvements remain deferred. RISK-HAG-001/002 remain raised. Repository adoption
and updates to the user's installed host plugins remain separate.
