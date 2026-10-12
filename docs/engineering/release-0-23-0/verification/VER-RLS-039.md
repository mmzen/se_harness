+++
id = "VER-RLS-039"
type = "verification"
title = "Verify the integrated 0.23.0 release inputs"
status = "approved"
owners = ["mmzen"]
created = "2026-10-12"
updated = "2026-10-12"

[relations]
verifies = ["REQ-DST-006", "REQ-PLG-002", "REQ-HAG-008", "REQ-RLO-018", "REQ-RLO-021", "REQ-RLO-022", "REQ-RLO-023"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-12T14:05:21Z"
decided_by = "mmzen"
reason = "Human mmzen answered \"Approve preparation, verification and review publication\" to the exact evaluator/client 0.23.0 and plugin 0.2.7 package: REL-SEH-036, WO-RLS-045/046/047 and VER-RLS-039/040/041, with required commit-bound verification. This approves the bounded build-helper/setup-guide correction, current documentation, qualification, review pushes and a draft PR from codex/release-0-23-0 to mmzen/se_harness:main, later verification-decision pushes, read-only CI rehearsals and codex/plugin-0-2-7-staging review staging. The hosted service remains a private source-built sandbox and Git remains authoritative. Human verification, merge and the exact complete-release approval remain separate; adoption and host updates are excluded. Reviewed byte digests matched; only confirmed assurance fields were added before preview. Reviewed SHA-256 9e6e03016fee36b14e0d0129627985970782b0efb51bfc061c8e206d9168a0cb."
+++

# Verify the integrated 0.23.0 release inputs

## Independence and candidate

Use accepted distribution, HAG and delivery specifications as expected behavior.
Released 0.22.1 governs from outside the checkout. Candidate 0.23.0 is test input.
Keep VREC-HAG-003/004/005/006/007, VREC-HUP-028 and VREC-IPK-002 unchanged.

## Requirement-to-evidence matrix

| Requirement | Method and evidence | Pass condition |
| --- | --- | --- |
| REQ-DST-006 | Windows/Linux full-scale source suites, installed wheel/sdist, CLI, distribution/resource checks, real upgrade rehearsals and pinned build replay | Required checks pass at C; two recipe builds produce byte-identical archives; core remains dependency-free. |
| REQ-PLG-002 | Inspect both manifests and staged inventories | Both packages use 0.2.7, matching shared source and the exact 0.23.0 bundle; detailed qualification is VER-RLS-040. |
| REQ-HAG-008 | Helper boundary tests and actual coordinated build | Client version matches wheel/source/replay; supplied staged plugins match the retained bundle and source. Wrong version/hash/source, an incomplete pair or a dirty source is refused. The original development route remains usable. Hosted evaluator stays exact public 0.22.1. |
| REQ-RLO-018 | Release census, membership and five-surface review | Every new included outcome has governing work and final verification; every public surface has an owner, destination and observation. |
| REQ-RLO-021 | Inspect the ready RLS and frozen v2 plan | Candidate, payloads, staged ref, documentation, combination companion, prior refs and permitted integrations are concrete before the one approval request. |
| REQ-RLO-022 | Compare build/staging/review inputs and replay the bound record | Final exact archives and plugin inputs have required assurance before public approval. No pending input is relabelled ready. |
| REQ-RLO-023 | Read-only provider readiness and existing recovery rehearsal | Required controls, credentials and actual invocation boundaries are evidenced; no provider change or bypass is made. |

## Final aggregate verification

At final clean C, capture one VREC covering exactly REL-SEH-036.gates and all
their verification contracts. Assess final integration, including HAG, adoption
compatibility and integration-package behavior. Preserve historical records.
Reuse an earlier result only with explicit source/package/input identity and
applicability evidence; version-sensitive or changed inputs require new tests.
Do not report reused evidence as a fresh run. Missing required cases remain pending.

Run both existing publication rehearsal legs and complete-delivery/recovery
rehearsal. A PR merge commit is not the candidate build identity. Use the pinned
recipe, create the schema-2 bundle, bind and replay the ready RLS after human
verification. Keep the actual hosted combination and deployment conditions in
the referenced companion manifest without changing the evaluator bundle schema.

Retain commands, results, failures, skips, byte comparisons and independent
assessments under evidence/WO-RLS-045/. No build or public availability is
established by this contract's preparation.
