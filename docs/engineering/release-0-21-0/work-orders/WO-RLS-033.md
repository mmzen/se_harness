+++
id = "WO-RLS-033"
type = "work_order"
title = "Confirm public 0.21.0 delivery and reconcile current guidance"
status = "approved"
owners = ["mmzen"]
created = "2026-10-01"
updated = "2026-10-01"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen approved the reviewed v0.21.0 release package and required commit-bound verification. Later release, publication and availability decisions depend on this work."
decided_by = "mmzen"

[execution_scope]
paths = [
  "docs/engineering/release-0-21-0/",
  "README.md",
  "release/plugin-marketplace/README.md",
  "plugins/verity-plane/codex/README.md",
  "plugins/verity-plane/claude-code/README.md",
  "docs/notes/plugin-installation-guide.md",
  "docs/notes/plugin-marketplace-publication.md",
  "docs/notes/developing-se-harness.md",
  "docs/notes/release-delivery-completion.md",
  "docs/notes/harness-installation-and-upgrades.md",
  "docs/engineering/plugin-integration/README.md",
  "docs/engineering/instruction-architecture/README.md",
  "docs/engineering/README.md",
  "tests/test_progressive_documentation.py",
  "tests/plugin_integration/package_assembly/test_refresh_guidance.py",
]

[relations]
implements = ["REQ-RLO-019", "REQ-RLO-020"]
specifications = ["SPEC-RLO-006"]
verification = ["VER-RLS-032"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-01T19:53:49Z"
decided_by = "engineering-owner"
reason = "Human mmzen: Approve package and required verification. Approves REL-SEH-033, WO-RLS-031/032/033 and VER-RLS-030/031/032, required commit-bound verification, plugin 0.2.4, ordinary release-review branch push/draft PR and read-only CI rehearsals. Existing v0.21.0 publication authorization is retained. Final-candidate verification, exact RLS decision and unresolved desktop evidence remain separate. Reviewed SHA256 1e465a19bbafe7554631099df970d37e02b10eaa5c01108f8147f49d7227c8ce; transition-input SHA256 5e935e115fc06e6e5170aeaca7694a69cfd3ae91a36a3b17c9dc5e7af96f8938. Only confirmed work-order assurance metadata was added. Codex applies the human decision using the selected evaluator role-label encoding; mmzen is the decision-maker."
scope_paths = ["docs/engineering/release-0-21-0/", "README.md", "release/plugin-marketplace/README.md", "plugins/verity-plane/codex/README.md", "plugins/verity-plane/claude-code/README.md", "docs/notes/plugin-installation-guide.md", "docs/notes/plugin-marketplace-publication.md", "docs/notes/developing-se-harness.md", "docs/notes/release-delivery-completion.md", "docs/notes/harness-installation-and-upgrades.md", "docs/engineering/plugin-integration/README.md", "docs/engineering/instruction-architecture/README.md", "docs/engineering/README.md", "tests/test_progressive_documentation.py", "tests/plugin_integration/package_assembly/test_refresh_guidance.py"]
+++

# Confirm public 0.21.0 delivery and reconcile current guidance

## Objective

Verify what users can obtain and report complete delivery only when all five release surfaces have matching evidence.

## In scope

1. Observe the public evaluator and qualified marketplace package independently.
2. Test public fresh installation and update from 0.2.3 to 0.2.4 for Codex and
   Claude Code in disposable profiles. Record the exact package and host identities.
3. Update only the listed current availability, installation and publication
   guidance to observed facts. Preserve historical receipts and native limits.
4. Check source and assembled links, Pages provenance and separately authorized
   latest/last markers. Report missing observations rather than inferring success.
5. Capture verification for the owner-documentation changes. After human acceptance
   and authorized integration, read back public documents and run final closeout.

## Proposed assurance

Required commit-bound verification is proposed. Later release, publication and
availability decisions rely on this work. Human confirmation is still needed
for this new bounded package. No assurance decided_by or lifecycle approval is
invented. The work remains draft until its approval is recorded.

## Decision envelope

Approval authorizes read-only public observations, disposable native acceptance,
bounded documentation edits, local commits, checks and VREC preparation. Any source
PR/push, merge or marker mutation requires matching external authority. Reuse valid
existing decisions only when their actual targets still match.

Human mmzen requested "Publish v0.21.0". Preserve that publication authorization
for the matching release once the required immutable inputs and controls exist.
Do not ask again for the same publication action. This request does not supply a
verification verdict on an unprepared candidate or release record. Apply any
later exact human decisions through the selected evaluator; its legacy role
encoding must retain mmzen and the actual decision in the reason.

## Constraints

Use released 0.20.1 outside the checkout as the governing evaluator. Candidate
0.21.0 is only the system under test until separate adoption. Preserve the root
selection, installed instructions, owner files, accepted definitions and earlier
evidence. Reuse existing build, qualification, marketplace and delivery tools.
No new framework, policy edition or automation is needed.

## Required verification

Meet VER-RLS-032. Public-route qualification must use the actual public ref,
not local assembly. Current claims must match real support and pending criteria.
The delivery checker reports incomplete until all surfaces pass.

Codex Windows desktop remains unverified. VER-IAR-021 explicitly requires it;
CLI or app-server traces do not satisfy it. Keep the criterion pending until
matching native evidence exists or a separately authorized formal resolution
changes its applicability. This draft grants no deferral or waiver.

## Evidence and expected change surface

The release domain, listed current documentation and two existing documentation
test expectations only. Retain observations under evidence/WO-RLS-033/ and generated
verification files in the canonical directories in this domain.

The execution_scope lists the permitted files. Directory entries admit only this
work's declared release artifacts and evidence, not unrelated changes. Retain
actual commands, full commits, versions, exit codes, failed attempts and digests.
Keep bulky raw logs and disposable profiles outside the repository; keep complete
native traces when the verification contract requires them.

## Out of scope

Runtime, installer, workflow or builder changes; publication of unverified
packages; real-profile changes; credentials; release-marker movement without its
own exact authorization; repository adoption and historical evidence rewriting.

## Stop conditions

Stop the affected step for changed or occupied identities, missing verification,
an unassessed required criterion, unsafe or customized input, failed checks,
out-of-scope edits, unavailable independent controls, or an advanced destination
ref. Preserve original failures. Inspect uncertain external effects before retry.

## Completion report

Report the exact candidate/package identity, actual checks and limitations,
formal record state, completed external effects and remaining delivery surfaces.
No missing or pending result may be reported as passed or complete.
