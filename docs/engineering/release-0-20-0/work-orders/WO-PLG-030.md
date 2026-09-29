+++
id = "WO-PLG-030"
type = "work_order"
title = "Assemble and qualify plugin 0.2.2 from public evaluator 0.20.0"
status = "approved"
owners = ["mmzen"]
created = "2026-09-29"
updated = "2026-09-29"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen confirmed required commit-bound verification by approving the reviewed 0.20.0/0.2.2 release package; later release, publication and availability decisions rely on this work."
decided_by = "mmzen"

[execution_scope]
paths = [
  "docs/engineering/release-0-20-0/work-orders/WO-PLG-030.md",
  "docs/engineering/release-0-20-0/evidence/WO-PLG-030/",
  "docs/engineering/release-0-20-0/verification-records/"
]

[relations]
implements = ["REQ-PLG-002", "REQ-RLO-018"]
specifications = ["SPEC-PLG-001", "SPEC-RLO-006"]
verification = ["VER-PLG-028"]
architecture = ["ARCH-PLG-001", "ADR-PLG-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-29T17:32:13Z"
decided_by = "engineering-owner"
reason = "Human repository owner mmzen: \"I approve\", responding to the reviewed seven-artifact 0.20.0/0.2.2 release package, required commit-bound verification, stated ordinary review-branch pushes/draft PRs and read-only CI rehearsals, and existing 0.19.0 role encoding. Reviewed SHA-256 50ecd19f44ad8a9d2fbf874a19cc960cc757cb07d05bf2ba4c389f064af32336; approval input SHA-256 e6b5e09f54b93985b878963f48c720099f328d233476de09461ee6a033eb601e. Only the confirmed assurance classification was added to work orders. Legacy label engineering-owner transports the human decision; Codex applies it. Exact candidate verification, RLS release, merge, publication, markers and adoption remain separate."
scope_paths = ["docs/engineering/release-0-20-0/work-orders/WO-PLG-030.md", "docs/engineering/release-0-20-0/evidence/WO-PLG-030/", "docs/engineering/release-0-20-0/verification-records/"]
+++

# Assemble and qualify plugin 0.2.2

## Confirmed assurance

Commit-bound verification is `required`. Human mmzen confirmed the proposed
classification with "I approve" in response to the seven-artifact release
package review. The assurance metadata records that decision; Codex applies it.

## Objective and prerequisites

Produce one reviewed marketplace distribution carrying public evaluator 0.20.0.
Begin only after the REL-SEH-031 evaluator is released and its public wheel
matches the RLS binding. Use the committed 0.2.2 manifests prepared by WO-RLS-026.
This work is downstream of the evaluator release, not a pre-publication member
of its aggregate VREC.

## In scope

1. Inspect current public release and marketplace state before any retry.
2. Independently obtain the published wheel, compare its SHA-256 with the RLS,
   and retain exact source/release commits and builder inputs.
3. Assemble both host packages in a fresh directory outside the source checkout
   with scripts/build_plugin_marketplace.py. Run its independent check mode.
4. Qualify the actual outputs on both Windows CLIs in disposable profiles under
   VER-PLG-028. Retain package identities and native instruction-delivery proof.
5. Prepare a history-preserving distribution commit whose parent is the current
   public plugin-marketplace head. Compare the complete tree with the qualified
   output. A moved or conflicting remote head requires inspection and review.
6. Retain the exact candidate and handoff, complete this WO, and prepare its
   commit-bound VREC for human verification. Present the distribution commit,
   destination and current pre-action checks for exact publication authority.

## Decision envelope and publication boundary

Approval authorizes the bounded local work, disposable profiles, required
checks, local commits, evidence and VREC preparation. Proposed review delivery
includes ordinary pushes of work/plugin-0-2-2 to mmzen/se_harness and a draft PR
to main for retained qualification evidence. It grants no force push.

Human verification acceptance and permission to publish the exact distribution
commit to refs/heads/plugin-marketplace remain separate decisions. When supplied,
apply that authorization under the existing external-action procedure and
independent provider controls. Inspect actual effects before retrying. Publication
changes only the reviewed generated distribution; it changes no formal state.
WO-PLG-031 then assesses the actual public result and current documentation.

The proposed required assurance and legacy 0.19.0 decision encoding must be
confirmed by the human, retaining mmzen and the actual decision in the reason.

## Constraints and verification

Use the external released 0.19.0 governor. Keep SPEC-PLG-001's public-wheel
boundary. Use existing assembly and publication tools; change no builder, hook,
runtime, skill or workflow implementation. Follow VER-PLG-028 and retain commands,
outputs, hashes, failures and host limitations under evidence/WO-PLG-030/.
No new architecture is needed; ARCH-PLG-001 and ADR-PLG-001 remain applicable.

## Out of scope and stops

No real profile adoption, repository upgrade, stock guide deletion, source
correction, release decision or marker change. Stop on mismatched wheel/package
identity, failed native qualification, insufficient external authority, conflicting
remote work or a required source edit. Present a bounded correction if needed.
Do not publish a local development wheel or overwrite the existing 0.2.1 identity.

## Completion report

Report the qualified source and package identities, actual checks, documented
limits, exact publication candidate and the evaluator's next accountable step.
Publication readback and availability corrections are owned by WO-PLG-031;
completion here must not claim overall delivery.
