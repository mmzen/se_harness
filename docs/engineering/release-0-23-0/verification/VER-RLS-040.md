+++
id = "VER-RLS-040"
type = "verification"
title = "Qualify the exact 0.2.7 plugin and private hosted combination"
status = "approved"
owners = ["mmzen"]
created = "2026-10-12"
updated = "2026-10-12"

[relations]
verifies = ["REQ-PLG-002", "REQ-IAR-030", "REQ-HAG-008", "REQ-RLO-018", "REQ-RLO-022"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-12T14:05:21Z"
decided_by = "mmzen"
reason = "Human mmzen answered \"Approve preparation, verification and review publication\" to the exact evaluator/client 0.23.0 and plugin 0.2.7 package: REL-SEH-036, WO-RLS-045/046/047 and VER-RLS-039/040/041, with required commit-bound verification. This approves the bounded build-helper/setup-guide correction, current documentation, qualification, review pushes and a draft PR from codex/release-0-23-0 to mmzen/se_harness:main, later verification-decision pushes, read-only CI rehearsals and codex/plugin-0-2-7-staging review staging. The hosted service remains a private source-built sandbox and Git remains authoritative. Human verification, merge and the exact complete-release approval remain separate; adoption and host updates are excluded. Reviewed byte digests matched; only confirmed assurance fields were added before preview. Reviewed SHA-256 da00e0ae895809506a851885be657279460c810562b3d9be86d33bed3167ee6c."
+++

# Qualify the exact 0.2.7 plugin and private hosted combination

## Independence and inputs

Derive expected behavior from SPEC-PLG-001, SPEC-IAR-016, SPEC-HAG-003/007/008
and SPEC-RLO-006/007. Select exact candidate C and its schema-2 0.23.0 archives,
plugin 0.2.7 staging, private service 0.1.0.dev1 and pinned evaluator 0.22.1.
Do not substitute development archives for the staged public plugin payloads.

## Requirement-to-evidence matrix

| Requirement | Method and evidence | Pass condition |
| --- | --- | --- |
| REQ-PLG-002 | Existing staging/check commands and Windows/Linux archive tests | Both host outputs have matching shared bytes, exact bundled wheel, source revision and complete inventories; no runtime is bundled. |
| REQ-IAR-030 | Native delivery traces under VER-IAR-021 | Required startup, activation after clone, resume, compaction, isolation and delivery-gap cases pass for their exact host/package inputs. Desktop evidence remains separate from CLI evidence. |
| REQ-HAG-008 | Packaged sandbox, actual HTTP/MCP checks, independent replay and restart/restore | The exact new tuple satisfies applicable VER-HAG-001/006/007/008 cases and preserves Git authority, imported bytes, receipts, refusals and exported evidence. |
| REQ-RLO-018 | Staging parent/tree and coordinated manifest review | Complete staged tree is one ordinary child of the observed public tip; component/image/deployment identities are retained before approval. |
| REQ-RLO-022 | Candidate-to-staged-to-plan comparison | The qualified payloads are the frozen release inputs; later governance receipts neither rebuild nor replace them. |

## Native and hosted qualification

Use real Codex and Claude CLIs with disposable profiles, public fixture data and
the approved private service boundary. Reapply no prior host-global permissions.
Keep the service's evaluator 0.22.1 separate from the plugin's bundled 0.23.0.
Record host/model versions and the actual instruction-delivery route.

For the changed release tuple, run the required five native lifecycle cases on
both hosts and the focused drafting cases: both missing-input diagnostics,
three Claude positive drafts and one Codex positive draft. Assess content and
replay independently. Keep time/context/call observations separate from correctness;
the existing missed goals remain visible and no new performance threshold is added.

Assess unchanged service cases through exact dependency/runtime/source/input
comparisons where the governing contract permits reuse. Rerun all affected or
version-sensitive scenarios, and the final packaged walkthrough and restart/restore.
Retain each reused or new result distinctly; an unavailable result is not a pass.

The previous DEC-RLS-009/RISK-RLS-007 desktop omission applies only to 0.22.1.
Missing desktop or CLI evidence prevents the corresponding readiness claim;
a new bounded deferral would require its own reviewed human decision. Do not
infer risk acceptance from package approval or from the private-sandbox scope.

Retain native observations, failures, inventory digests, staged ref and independent
assessment under evidence/WO-RLS-046/. No container image is publicly published.
