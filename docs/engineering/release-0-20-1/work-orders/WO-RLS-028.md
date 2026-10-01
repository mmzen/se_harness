+++
id = "WO-RLS-028"
type = "work_order"
title = "Prepare and qualify plugin 0.2.3 for evaluator 0.20.1"
status = "in_progress"
owners = ["mmzen"]
created = "2026-09-30"
updated = "2026-10-01"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen approved the reviewed work-order and verification-contract pair with required commit-bound verification; later package and delivery decisions depend on the changed manifests, instructions and retained evidence."
decided_by = "mmzen"

[execution_scope]
paths = [
  "plugins/verity-plane/codex/.codex-plugin/plugin.json",
  "plugins/verity-plane/claude-code/.claude-plugin/plugin.json",
  "plugins/verity-plane/codex/README.md",
  "plugins/verity-plane/claude-code/README.md",
  "release/plugin-marketplace/README.md",
  "release/plugin-marketplace/submissions/README.md",
  "release/plugin-marketplace/submissions/reviewer-test-cases.md",
  "tests/plugin_integration/package_assembly/test_refresh_guidance.py",
  "docs/engineering/release-0-20-1/",
]

[relations]
implements = ["REQ-PLG-002", "REQ-RLO-018"]
specifications = ["SPEC-PLG-001", "SPEC-RLO-006"]
verification = ["VER-RLS-028"]
architecture = ["ARCH-PLG-001", "ADR-PLG-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-01T05:48:10Z"
decided_by = "engineering-owner"
reason = "Human mmzen approved the reviewed package and confirmed: Yes\u2014approve both 028 and 029 pairs. Approves WO-RLS-028, VER-RLS-028, WO-RLS-029 and VER-RLS-029, required commit-bound verification, the stated ordinary review-branch pushes/draft PRs and read-only CI rehearsals, and the existing 0.19.0 engineering-owner encoding retaining mmzen as the human decision-maker. Reviewed SHA256 cce8b7ae0c8e47f6b081f793cbbbcac07003d3acd1cbe302734f3e07a2cb3dbc; transition input SHA256 9cd48d6c1b071f17ffd3a0c5f9efecbae8368a44b858f320517074f4254333da. Only confirmed assurance metadata was added to work orders. Codex applies the matching decision. Human verification, merges, release, publication, release markers and adoption remain separate."
scope_paths = ["plugins/verity-plane/codex/.codex-plugin/plugin.json", "plugins/verity-plane/claude-code/.claude-plugin/plugin.json", "plugins/verity-plane/codex/README.md", "plugins/verity-plane/claude-code/README.md", "release/plugin-marketplace/README.md", "release/plugin-marketplace/submissions/README.md", "release/plugin-marketplace/submissions/reviewer-test-cases.md", "tests/plugin_integration/package_assembly/test_refresh_guidance.py", "docs/engineering/release-0-20-1/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-01T05:49:09Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed."
+++

# Prepare and qualify plugin 0.2.3 for evaluator 0.20.1

## Objective

Prepare one immutable Verity Plane 0.2.3 marketplace package from the public
0.2.2 plugin behavior and the independently published 0.20.1 evaluator.
REL-SEH-032 requires this downstream work. It is not a member of the 0.20.1
wheel release or VREC-SEH-030.

## Source and execution boundaries

The plugin source baseline is 7253d13b212ad6f7df670021290fea32e81d66de,
the source recorded by the public 0.2.2 marketplace. Use the maintenance
checkout, whose plugin inputs still match that baseline, and its exact
released 0.19.0 evaluator. Record a new full source commit after the allowed
metadata and guidance changes. Check that 0.2.3 remains unused first.

Current main contains later instruction work. Do not merge maintenance source
into main or use main's plugin source for this package. Transport only the
selected release-0-20-1 domain to a separate checkout of current main when
needed for the publisher. Confirm main's own released evaluator there; compare
all transported records and evidence with their reviewed source. Preserve
existing main files and stop on a conflicting domain or governing graph.

## In scope

1. Set only the version field in both host manifests to 0.2.3. Update the five
   listed packaged guidance files for 0.2.3/0.20.1, the selected work and honest
   availability. Keep immutable source links and observed support limits.
   In test_refresh_guidance.py, update only the candidate version constants
   and their contract reference. Preserve its public receipt, identity,
   refusal and link checks. Do not manufacture a new public observation.
2. Bind the release delivery plan to RLS-SEH-030 and both downstream work orders.
   Keep its earlier version and evidence unchanged. Source and package hashes
   remain pending until the relevant commits and outputs exist.
3. Prepare release-governance transport to main and the exact bound-record
   replay inputs. Copy the selected domain's definitions, histories, VREC,
   RLS and evidence without rewriting their meaning or candidate bindings.
   A release decision is applied only after the human supplies it.
4. After RLS-SEH-030 is released and the matching wheel is public, independently
   download it, compare its digest and assemble both host packages with the
   existing builder. Use fresh output outside the repository; run check mode.
5. Perform VER-RLS-028 in disposable profiles. Retain the selected source,
   governance commit, wheel, inventories, host observations and failed attempts.
6. Prepare a distribution commit on the then-current plugin-marketplace parent.
   Check the complete tree against the qualified output. Complete the work and
   capture a VREC for human verification before requesting publication.

## Proposed assurance and decision envelope

Commit-bound verification is proposed as required: users and later publication
decisions rely on the changed manifests, instructions and qualified package.
The human must confirm this classification before approval; no assurance
metadata asserts that decision yet.

Approval would authorize the bounded local work, checks, disposable profiles,
local commits, evidence, completion and VREC preparation. It also proposes
ordinary pushes and draft PRs in mmzen/se_harness for these review branches:
work/release-0-20-1-preparation and work/plugin-0-2-3 to release/0.20;
work/release-0-20-1-governance to main. Read-only candidate and bound-record
rehearsals on those review refs are included in the proposed review envelope.
No force push is included. Human verification, merges, evaluator publication,
marketplace publication and latest/last changes need separate exact decisions.

For maintenance lifecycle decisions, the approval proposal includes the existing
0.19.0 role-label encoding, retaining mmzen and the actual decision in the reason.
Use a checkout's actual identity contract; an actor label supplies no authority.

## Constraints and exclusions

Reuse SPEC-PLG-001, SPEC-RLO-006, ARCH-PLG-001 and ADR-PLG-001 unchanged. No new
runtime, lifecycle, assembly, installer, hook, skill or workflow behavior is
needed. The whole domain path permits required governance transport and evidence;
it does not permit edits to accepted definitions or frozen candidate evidence.
Do not change the verified 0.20.1 source, real user profiles, installed repository
selection, credentials, provider listings or existing published versions.

The work stays in progress across evaluator publication. Source preparation is
not package acceptance. It completes after local package qualification; public
route checks and documentation closeout follow under WO-RLS-029. This boundary
allows verification before marketplace publication without claiming its result.

## Required verification, evidence and stops

Follow VER-RLS-028. Retain evidence under this domain's evidence/WO-RLS-028/,
release preparation under evidence/RLS-SEH-030/, and generated records under
verification-records/ with their evaluator companions in evidence/.
Stop the affected action on an occupied version, changed baseline, failed
check, evidence mismatch, missing native access, incompatible governance
transport, moved marketplace parent or an edit outside the listed paths.
Propose the bounded correction; preserve all original observations.

## Completion report

Report exact source/release/package identities, actual checks, limitations,
publication candidate, pending public observations and the evaluator's next
accountable step. Do not report overall delivery complete.
