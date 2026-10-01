+++
id = "WO-RLS-031"
type = "work_order"
title = "Prepare and qualify the integrated 0.21.0 release"
status = "in_progress"
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
  "release/plugin-assembly.json",
  "plugins/verity-plane/codex/.codex-plugin/plugin.json",
  "plugins/verity-plane/claude-code/.claude-plugin/plugin.json",
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
implements = ["REQ-DST-006", "REQ-PLG-002", "REQ-IAR-031", "REQ-RLO-018", "REQ-RLO-020"]
specifications = ["SPEC-DST-001", "SPEC-PLG-001", "SPEC-IAR-016", "SPEC-RLO-006"]
verification = ["VER-RLS-030"]
architecture = ["ARCH-DST-001", "ADR-DST-001", "ARCH-PLG-001", "ADR-PLG-001", "ARCH-IAR-012", "ADR-IAR-012"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-01T19:53:49Z"
decided_by = "engineering-owner"
reason = "Human mmzen: Approve package and required verification. Approves REL-SEH-033, WO-RLS-031/032/033 and VER-RLS-030/031/032, required commit-bound verification, plugin 0.2.4, ordinary release-review branch push/draft PR and read-only CI rehearsals. Existing v0.21.0 publication authorization is retained. Final-candidate verification, exact RLS decision and unresolved desktop evidence remain separate. Reviewed SHA256 4beb4a466ad2a5f76d55007e58799fa57669878755ad5c78a83530829babc6d3; transition-input SHA256 b1cfba497c61d3f8ce46238843843d979766ff1676652ce772475ae7bd283128. Only confirmed work-order assurance metadata was added. Codex applies the human decision using the selected evaluator role-label encoding; mmzen is the decision-maker."
scope_paths = ["docs/engineering/release-0-21-0/", "release/plugin-assembly.json", "plugins/verity-plane/codex/.codex-plugin/plugin.json", "plugins/verity-plane/claude-code/.claude-plugin/plugin.json", "README.md", "release/plugin-marketplace/README.md", "plugins/verity-plane/codex/README.md", "plugins/verity-plane/claude-code/README.md", "docs/notes/plugin-installation-guide.md", "docs/notes/plugin-marketplace-publication.md", "docs/notes/developing-se-harness.md", "docs/notes/release-delivery-completion.md", "docs/notes/harness-installation-and-upgrades.md", "docs/engineering/plugin-integration/README.md", "docs/engineering/instruction-architecture/README.md", "docs/engineering/README.md", "tests/test_progressive_documentation.py", "tests/plugin_integration/package_assembly/test_refresh_guidance.py"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-01T19:55:14Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."
+++

# Prepare and qualify the integrated 0.21.0 release

## Objective

Prepare one integrated evaluator 0.21.0 candidate for human verification and release. Prepare the plugin 0.2.4 source and explicit downstream delivery handoff.

## In scope

1. Start from main f5f7c77c6eadfd7d6f1c68e136f1f7cc29cfc0a5. Keep the approved
   external-resource implementation and record REL-SEH-033's complete membership.
2. Set both host manifest versions from 0.2.2 to the proposed unused 0.2.4.
   Public 0.2.3 was a maintenance package; do not overwrite either prior identity.
   Preserve shared bootstrap, activation, setup, hooks and resource resolution.
3. Reconcile only current release/install claims in the named documents and their
   existing tests. Distinguish proposed 0.21.0/0.2.4 from currently public
   0.20.1/0.2.3. No runtime, workflow or new test behavior is included.
4. Prepare the five-surface plan with WO-RLS-032 for marketplace assembly and
   publication, and WO-RLS-033 for public qualification and current documentation.
5. Run final integration qualification and two pinned recipe builds for clean C.
   Assess every required release-member contract, including pending desktop proof.
6. Complete implementation and capture the aggregate VREC for every REL member
   and its required VERs at C. Present actual evidence for human verification.
7. After that decision, prepare the tagged RLS, bind the immutable bundle, run
   bound-record replay and present the exact release record for the human decision.
8. After released-record integration, resolve publication readiness and execute
   the requested v0.21.0 publication through the protected existing publisher.
   Observe public bytes and hand off the exact wheel to WO-RLS-032.

## Proposed assurance

Required commit-bound verification is proposed. Later release, publication and
availability decisions rely on this work. Human confirmation is still needed
for this new bounded package. No assurance decided_by or lifecycle approval is
invented. The work remains draft until its approval is recorded.

## Decision envelope

Approval authorizes local preparation, checks, commits, evidence capture and
record preparation within scope. The proposed review envelope also includes
ordinary pushes of work/release-0-21-0, a draft PR to main in mmzen/se_harness,
and existing read-only publication-rehearsal/release-candidate-replay dispatches.
Final-candidate verification, the exact RLS decision, merge and protected provider
approval remain separate. The existing publication request is retained.

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

Meet VER-RLS-030 plus VER-IAR-020/021/022 for the complete release. Preserve the
unchanged 0.20.1 repository selection. Do not replay completed implementation or
attribute old verification acceptance to the new final candidate.

Codex Windows desktop remains unverified. VER-IAR-021 explicitly requires it;
CLI or app-server traces do not satisfy it. Keep the criterion pending until
matching native evidence exists or a separately authorized formal resolution
changes its applicability. This draft grants no deferral or waiver.

## Evidence and expected change surface

Release-domain artifacts and evidence, two host version fields, the existing
assembly plan if its accepted inventory needs correction, listed current documents
and two existing documentation tests only. All generated VREC/RLS companions,
manifests and subsequent decision transport belong under this release domain.

The execution_scope lists the permitted files. Directory entries admit only this
work's declared release artifacts and evidence, not unrelated changes. Retain
actual commands, full commits, versions, exit codes, failed attempts and digests.
Keep bulky raw logs and disposable profiles outside the repository; keep complete
native traces when the verification contract requires them.

## Out of scope

Product implementation corrections, new build/workflow logic, repository
adoption, real profile changes, credentials, force pushes, marker movement and
marketplace publication. Downstream work owns the latter.

## Stop conditions

Stop the affected step for changed or occupied identities, missing verification,
an unassessed required criterion, unsafe or customized input, failed checks,
out-of-scope edits, unavailable independent controls, or an advanced destination
ref. Preserve original failures. Inspect uncertain external effects before retry.

## Completion report

Report the exact candidate/package identity, actual checks and limitations,
formal record state, completed external effects and remaining delivery surfaces.
No missing or pending result may be reported as passed or complete.
