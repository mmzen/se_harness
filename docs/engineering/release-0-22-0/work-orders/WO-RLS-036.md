+++
id = "WO-RLS-036"
type = "work_order"
title = "Complete public 0.22.0 delivery"
status = "implemented"
owners = ["mmzen"]
created = "2026-10-03"
updated = "2026-10-03"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen confirmed required commit-bound verification; subsequent release, marketplace publication and public-delivery decisions depend on this work."
decided_by = "mmzen"

[execution_scope]
paths = [
  "docs/engineering/release-0-22-0/",
  "README.md",
  "release/plugin-marketplace/README.md",
  "plugins/verity-plane/codex/README.md",
  "plugins/verity-plane/claude-code/README.md",
  "docs/notes/plugin-installation-guide.md",
  "docs/notes/plugin-marketplace-publication.md",
  "docs/notes/developing-se-harness.md",
  "docs/notes/release-delivery-completion.md",
  "docs/notes/release-publication-rehearsal.md",
  "docs/notes/harness-installation-and-upgrades.md",
  "docs/notes/harnessctl-reference.md",
  "docs/engineering/plugin-integration/README.md",
  "docs/engineering/README.md",
  "tests/test_progressive_documentation.py",
  "tests/plugin_integration/package_assembly/test_refresh_guidance.py"
]

[relations]
implements = ["REQ-RLO-019", "REQ-RLO-020"]
specifications = ["SPEC-RLO-006"]
verification = ["VER-RLS-035"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T22:07:58Z"
decided_by = "mmzen"
reason = "Human repository owner mmzen answered \"Approve package and required verification\" to the reviewed evaluator 0.22.0 / plugin 0.2.5 package: REL-SEH-034, WO-RLS-034/035/036 and VER-RLS-033/034/035. This confirms required commit-bound verification and authorizes bounded preparation, qualification, review pushes/PRs and listed delivery work under the retained request \"Merged. Next: prepare and execute the release\". Human verification of exact results, the exact release-record decision and merge remain separate. Repository adoption and provider-setting changes are excluded. Selected released 0.21.0 governs; Codex applies the recorded human decision. Reviewed SHA-256 58736e0bf133ccbe4f97689ba4093ff96c1df43720d8d063964952e622d809c7; transition-input SHA-256 387419f7f5ae5585603b69c757361c5c72182f0074e12a5e6f19160dbf43a3ec. Only confirmed assurance fields were added."
scope_paths = ["docs/engineering/release-0-22-0/", "README.md", "release/plugin-marketplace/README.md", "plugins/verity-plane/codex/README.md", "plugins/verity-plane/claude-code/README.md", "docs/notes/plugin-installation-guide.md", "docs/notes/plugin-marketplace-publication.md", "docs/notes/developing-se-harness.md", "docs/notes/release-delivery-completion.md", "docs/notes/release-publication-rehearsal.md", "docs/notes/harness-installation-and-upgrades.md", "docs/notes/harnessctl-reference.md", "docs/engineering/plugin-integration/README.md", "docs/engineering/README.md", "tests/test_progressive_documentation.py", "tests/plugin_integration/package_assembly/test_refresh_guidance.py"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-03T05:37:29Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-10-03T05:47:59Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded work-order approval; relevant local gates passed."
+++

# Complete public 0.22.0 delivery

## Objective

Confirm public delivery of evaluator 0.22.0 and plugin 0.2.5 on every declared
surface, then align current guidance and the latest/last markers.

## In scope

1. Verify public evaluator files and clean installation against RLS-SEH-032.
2. Run fresh installation and 0.2.4-to-0.2.5 update from the actual public
   marketplace on both claimed hosts. Record installed bytes and native inputs.
3. Reconcile current version, availability and support statements in the named
   documentation. Adjust only matching assertions in the two named tests.
4. Retain Pages URL and deployment provenance for the selected governance input.
5. Capture VREC-PLG-033 for documentation/evidence work and publish its review
   before asking for verification. Push the recorded decision as the final
   verification commit; retain subsequent public readbacks separately.
6. After required observations, set GitHub v0.22.0 as latest and move last to the
   exact RLS candidate under the matching execution grant. Use an exact expected
   old-ref lease for last, inspect any conflict, and read both markers back.
7. Run the existing delivery checker with the exact plan and observation binding.
   Read merged guidance back. Report complete only when all surfaces qualify.

## Expected change surface

The named current documents, their two existing assertion files, and this release
domain only. This includes evidence/WO-RLS-036/, VREC-PLG-033 and its canonical
evaluator JSON, plan revisions, public receipts and final completion report.
Historical receipts and source package bytes remain unchanged.

## Required verification

VER-RLS-035 applies. Retain missing platform evidence as missing, not passed.
Do not copy an old accepted risk into a new delivery assessment.

## Out of scope

Runtime, installer, tests other than the named current-documentation assertions,
provider configuration, artifact-policy changes and repository/host adoption.

## Authority and assurance

Propose required commit-bound verification. Later release and availability
decisions rely on these changes. The human must confirm this classification
with package approval; no assurance decision or lifecycle event is invented.

Human mmzen requested: "Merged. Next: prepare and execute the release".
Retain this release-execution request. Package approval makes its versions,
destinations and permitted work concrete. Reuse matching grants as required
checks pass; do not ask again for an unchanged external action.

The review grant proposed here covers ordinary pushes and draft PRs from
work/release-0-22-0 to mmzen/se_harness:main, later decision/receipt updates,
and existing read-only publication rehearsals. Publish the review before asking
for verification. Human verification and the exact release-record decision
remain separate from work approval. No merge is inferred.

Released 0.21.0 governs formal artifacts and gates outside the checkout.
Candidate 0.22.0 is the system under test. Do not adopt it, activate the new
complete-release route, change provider settings, or overwrite old evidence.
Preserve credentials and normal user profiles; use disposable test profiles.

## Evidence and completion

Retain actual commands, runtimes, commits, results, failures and digests in this
release domain. Include canonical VREC/RLS files and fixed evaluator JSON
destinations under evidence/, plus handoff records and decision transport.
Keep temporary builds and profiles outside the repository. Retain concise
durable evidence with raw outputs only where required by the selected contract.

Stop the affected action for failed or missing required evidence, changed
identities or destinations, uncovered paths, unavailable independent controls,
or a conflicting remote ref. Inspect uncertain writes before retrying.
Report the actual formal state, completed surfaces, outstanding work and next
decision. A publication or a version label alone cannot establish completion.
