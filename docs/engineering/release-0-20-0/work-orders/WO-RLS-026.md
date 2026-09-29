+++
id = "WO-RLS-026"
type = "work_order"
title = "Prepare evaluator 0.20.0 and plugin 0.2.2 release inputs"
status = "implemented"
owners = ["mmzen"]
created = "2026-09-29"
updated = "2026-09-29"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen confirmed required commit-bound verification by approving the reviewed 0.20.0/0.2.2 release package; later release, publication and availability decisions rely on this work."
decided_by = "mmzen"

[execution_scope]
paths = [
  "docs/engineering/release-0-20-0/",
  "docs/engineering/README.md",
  "docs/engineering/instruction-architecture/README.md",
  "docs/engineering/instruction-architecture/proposals/instruction-cleanup/README.md",
  "release/plugin-assembly.json",
  "release/plugin-marketplace/README.md",
  "plugins/verity-plane/codex/.codex-plugin/plugin.json",
  "plugins/verity-plane/claude-code/.claude-plugin/plugin.json",
  "plugins/verity-plane/codex/README.md",
  "plugins/verity-plane/claude-code/README.md",
  "README.md",
  "docs/notes/plugin-installation-guide.md",
  "docs/notes/plugin-marketplace-publication.md",
  "docs/notes/developing-se-harness.md",
  "docs/notes/release-delivery-completion.md",
  "docs/engineering/plugin-integration/README.md",
  "tests/test_progressive_documentation.py",
  "tests/plugin_integration/package_assembly/test_refresh_guidance.py"
]

[relations]
implements = ["REQ-DST-006", "REQ-PLG-002", "REQ-IAR-027", "REQ-IAR-028", "REQ-RLO-018", "REQ-RLO-020"]
specifications = ["SPEC-DST-001", "SPEC-PLG-001", "SPEC-IAR-014", "SPEC-IAR-015", "SPEC-RLO-006"]
verification = ["VER-RLS-026"]
architecture = ["ARCH-DST-001", "ADR-DST-001", "ARCH-PLG-001", "ADR-PLG-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-29T17:32:13Z"
decided_by = "engineering-owner"
reason = "Human repository owner mmzen: \"I approve\", responding to the reviewed seven-artifact 0.20.0/0.2.2 release package, required commit-bound verification, stated ordinary review-branch pushes/draft PRs and read-only CI rehearsals, and existing 0.19.0 role encoding. Reviewed SHA-256 c35ec9cdf80e2070d51d7a9d551f5d8ce4ca01b772d5ae841b6b0ec777602d33; approval input SHA-256 3b8d7452d90d16fcd0dba479af38a3d7c821ff3b5bbe10621eb7a703391add1b. Only the confirmed assurance classification was added to work orders. Legacy label engineering-owner transports the human decision; Codex applies it. Exact candidate verification, RLS release, merge, publication, markers and adoption remain separate."
scope_paths = ["docs/engineering/release-0-20-0/", "docs/engineering/README.md", "docs/engineering/instruction-architecture/README.md", "docs/engineering/instruction-architecture/proposals/instruction-cleanup/README.md", "release/plugin-assembly.json", "release/plugin-marketplace/README.md", "plugins/verity-plane/codex/.codex-plugin/plugin.json", "plugins/verity-plane/claude-code/.claude-plugin/plugin.json", "plugins/verity-plane/codex/README.md", "plugins/verity-plane/claude-code/README.md", "README.md", "docs/notes/plugin-installation-guide.md", "docs/notes/plugin-marketplace-publication.md", "docs/notes/developing-se-harness.md", "docs/notes/release-delivery-completion.md", "docs/engineering/plugin-integration/README.md", "tests/test_progressive_documentation.py", "tests/plugin_integration/package_assembly/test_refresh_guidance.py"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-29T17:33:21Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed. Codex starts the unchanged mmzen-approved release preparation after passing start preflight; downstream WO-PLG-030 and WO-PLG-031 remain approved until their public-release prerequisites exist."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-29T17:53:07Z"
decided_by = "Codex"
reason = "Execution of DR-WO-COMPLETE under recorded engineering-owner approval; relevant local gates passed. Codex records completion under mmzen-approved scope after local full/focused checks, hosted candidate qualification, Windows/Linux upgrade rehearsals, both manual publication legs, two identical pinned builds, documentation review and the complete Git-derived handoff passed. Exact final-candidate CI, build and aggregate VREC preparation continue under the same scope; human verification and release remain separate."
+++

# Prepare evaluator 0.20.0 and plugin 0.2.2 release inputs

## Confirmed assurance

Commit-bound verification is `required`. Human mmzen confirmed the proposed
classification with "I approve" in response to the seven-artifact release
package review. The assurance metadata records that decision; Codex applies it.

## Objective

Prepare the exact integrated 0.20.0 evaluator for human verification and release.
Make the subsequent marketplace delivery explicit and reviewable. The source
already declares evaluator 0.20.0. Plugin 0.2.2 is proposed as a new identity;
do not replace the published 0.2.1 package under its existing version.

## In scope

1. Start from merged commit ff2b5694f5f74743cfc305ed563f01d165f2fe91.
   Retain the explicit release membership and final candidate in this domain.
2. Set both host manifests to plugin 0.2.2. Inspect the assembly plan and keep
   its complete shared assets and native hooks. Change the plan only if needed
   for the already accepted files; do not add a new capability.
3. Correct the current instruction-architecture index and cleanup status summary.
   Distinguish completed implementation, public release and later adoption.
   Preserve formal artifact histories and evidence-bound review files.
4. Update the listed current release/install/package documentation in two clearly
   distinguished phases: proposed 0.20.0/0.2.2 inputs now, observed availability
   under WO-PLG-030 later. Keep the current public 0.19.0/0.2.1 route identified
   until its replacement is actually published. Never claim publication early.
5. Adjust only version/status expectations in the two named documentation tests
   when those expectations conflict with the corrected claims. Preserve checks
   of actual public receipts, link validity and truthfulness; do not weaken them.
6. Retain the five-surface delivery plan under evidence/WO-RLS-026/. Select all
   five surfaces for update. Name WO-PLG-030 for package qualification/publication and
   WO-PLG-031 for public observations and current documentation. Unknown RLS IDs, hashes and future commits stay
   explicitly pending until the supported commands allocate or produce them.
7. Run the final integration checks and two pinned recipe builds. Complete this
   work order's implementation, then capture one aggregate VREC for every
   REL-SEH-031 member at the same clean candidate C and all their required VERs.
8. After the human verifies that exact VREC, prepare the RLS, bind the retained
   schema-2 manifest and run the bound-record replay. Present the exact RLS and
   hashes for the human release decision. Keep the marketplace handoff pending.

## Authorized decision envelope

This is a draft. Approval confirms required commit-bound assurance and authorizes
Codex to execute the bounded preparation, make local commits, retain observations,
record implementation completion and prepare the required records. The proposed
external review envelope includes ordinary pushes of work/release-0-20-0 to
mmzen/se_harness, a draft PR to main, and dispatch of the existing read-only
publication-rehearsal.yml and release-candidate-replay.yml workflows on that
branch. No force push is included. Required provider controls still apply.

Verification acceptance, an exact RLS release decision, merge, publication and
latest/last promotion remain human decisions on their actual immutable inputs.
A request to begin preparation is not a decision on a future candidate or RLS.
The selected 0.19.0 evaluator's legacy role encoding may transport a supplied
human decision only with mmzen and the exact decision retained in its reason.
The human must confirm that encoding and the assurance classification at approval.

## Constraints and design assessment

Use the external released 0.19.0 evaluator. Do not change this repository's
installed root, lock or owner guide files. Use the existing build recipe,
workflows, marketplace builder and delivery checker. Existing ARCH-DST-001 and
ARCH-PLG-001 plus their deciding ADRs apply; no new component, trust boundary,
automation framework or architecture decision is proposed.

The downstream work orders prevent a circular dependency: public plugin assembly
requires the newly published evaluator wheel. It therefore cannot be a completed
member of the evaluator's pre-publication aggregate VREC. Their scope and handoffs
are reviewed now, and their actual results are assessed separately later.

## Required verification and evidence

Apply VER-RLS-026 and all release-member contracts. Run final Windows/Ubuntu
source and installed-package CI, supported predecessor upgrades, distribution
checks, complete instruction reading traces and the manual publication rehearsals.
Preserve failed attempts and reported skips. Retain tested commits, actual
commands, runtimes, workflow identities and permanent build/bundle manifests.

Retain evidence under evidence/WO-RLS-026/ and use the repository's evidence
policy. Do not infer native/public success from a test fixture. Do not rewrite
historical VRECs or reuse their acceptance for changed candidates.

## Out of scope and stop conditions

No runtime, builder, workflow or lifecycle implementation correction is included.
Stop and propose a bounded correction if required checks reveal such a need.
No repository adoption, real user-profile installation, legacy guide deletion,
credential transfer, immutable publication or marker movement is included.
Public marketplace delivery is WO-PLG-030 followed by WO-PLG-031. Publication remains separately gated.
A changed release member set or candidate invalidates dependent identity bindings;
reassess them instead of relabelling earlier evidence.

## Completion report

Report changed inputs, actual checks and limits, exact candidate and membership,
pending marketplace work, and the evaluator's next accountable decision.
Approved preparation continues to cover record binding and decision transport
following implementation completion, without reopening the completed work order.
