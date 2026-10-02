+++
id = "WO-RLS-034"
type = "work_order"
title = "Prepare and publish evaluator 0.22.0"
status = "in_progress"
owners = ["mmzen"]
created = "2026-10-03"
updated = "2026-10-02"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen confirmed required commit-bound verification; subsequent release, marketplace publication and public-delivery decisions depend on this work."
decided_by = "mmzen"

[execution_scope]
paths = [
  "docs/engineering/release-0-22-0/",
  "pyproject.toml",
  "se_harness/__init__.py",
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
  "docs/notes/release-publication-rehearsal.md",
  "docs/notes/harness-installation-and-upgrades.md",
  "docs/notes/harnessctl-reference.md",
  "docs/engineering/plugin-integration/README.md",
  "docs/engineering/README.md",
  "tests/test_progressive_documentation.py",
  "tests/plugin_integration/package_assembly/test_refresh_guidance.py"
]

[relations]
implements = ["REQ-DST-006", "REQ-PLG-002", "REQ-RLO-018", "REQ-RLO-020"]
specifications = ["SPEC-DST-001", "SPEC-PLG-001", "SPEC-RLO-006"]
verification = ["VER-RLS-033"]
architecture = ["ARCH-DST-001", "ADR-DST-001", "ARCH-PLG-001", "ADR-PLG-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T22:07:58Z"
decided_by = "mmzen"
reason = "Human repository owner mmzen answered \"Approve package and required verification\" to the reviewed evaluator 0.22.0 / plugin 0.2.5 package: REL-SEH-034, WO-RLS-034/035/036 and VER-RLS-033/034/035. This confirms required commit-bound verification and authorizes bounded preparation, qualification, review pushes/PRs and listed delivery work under the retained request \"Merged. Next: prepare and execute the release\". Human verification of exact results, the exact release-record decision and merge remain separate. Repository adoption and provider-setting changes are excluded. Selected released 0.21.0 governs; Codex applies the recorded human decision. Reviewed SHA-256 f707db09c095ed580106502f77ce6b6aa9fdab7a76f2a12d50efb42919f03812; transition-input SHA-256 a4d8c5ab57608ecb954299beb0df12f69cde92ab39c9522a5a2a369944b23964. Only confirmed assurance fields were added."
scope_paths = ["docs/engineering/release-0-22-0/", "pyproject.toml", "se_harness/__init__.py", "plugins/verity-plane/codex/.codex-plugin/plugin.json", "plugins/verity-plane/claude-code/.claude-plugin/plugin.json", "README.md", "release/plugin-marketplace/README.md", "plugins/verity-plane/codex/README.md", "plugins/verity-plane/claude-code/README.md", "docs/notes/plugin-installation-guide.md", "docs/notes/plugin-marketplace-publication.md", "docs/notes/developing-se-harness.md", "docs/notes/release-delivery-completion.md", "docs/notes/release-publication-rehearsal.md", "docs/notes/harness-installation-and-upgrades.md", "docs/notes/harnessctl-reference.md", "docs/engineering/plugin-integration/README.md", "docs/engineering/README.md", "tests/test_progressive_documentation.py", "tests/plugin_integration/package_assembly/test_refresh_guidance.py"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-02T22:09:33Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."
+++

# Prepare and publish evaluator 0.22.0

## Objective

Release the merged approval simplification and complete-delivery implementation
as evaluator 0.22.0. Prepare plugin 0.2.5 source for the following delivery work.

## In scope

1. Start from merged main de1d102b5f70b49ca1d2572e005d5daf7a570621. Set the
   two evaluator version fields to 0.22.0 and both host manifests to 0.2.5.
2. Update current release and installation statements in the named documents.
   Keep proposed, published, adopted and activated states distinct. Adjust only
   version/current-release expectations in the two named documentation tests.
3. Confirm release membership and the five-surface delivery plan in REL-SEH-034.
4. Qualify the final clean candidate on Windows and Linux. Run the existing
   installed-package, upgrade, distribution and publication rehearsal checks.
5. Produce the immutable wheel/sdist with two pinned builds. Capture one final
   aggregate VREC for every release member and all their verification contracts.
6. Publish the review and present its evidence for human verification. After
   verification, prepare the tagged RLS, bind the bundle, replay the bound record
   and present that exact release record for the release-owner decision.
7. After authorized record integration, pass publisher resolution and execute
   the requested publication through the existing protected main workflow.
   Observe public archives and hand the exact public wheel to WO-RLS-035.

## Expected change surface

The execution_scope is the complete proposed file set. It covers this domain's
artifacts, VREC-SEH-032 and RLS-SEH-032 with their fixed evaluator companions,
bundle manifest, reviews, handoffs and later decision/publication receipts.
Record IDs are proposed; check all refs again before capture or preparation.

## Required verification

VER-RLS-033 plus the existing contracts on every REL-SEH-034 member. Earlier
verified records support the assessment but do not verify the final candidate.

## Out of scope

New product fixes or feature work, test weakening, build/CI policy changes,
repository adoption and live provider configuration. Marketplace publication
and public closeout belong to WO-RLS-035/036.

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
