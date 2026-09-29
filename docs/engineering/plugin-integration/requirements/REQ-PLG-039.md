+++
id = "REQ-PLG-039"
type = "requirement"
title = "Prepare the 0.2.1 marketplace delivery with evaluator 0.19.0"
status = "approved"
owners = ["mmzen"]
created = "2026-09-28"
updated = "2026-09-28"
statement = "Users receive a qualified complete plugin 0.2.1 candidate for Codex and Claude Code with the unchanged released 0.19.0 evaluator, accurate identity checks and bounded installation guidance."
verification_method = ["test", "inspection", "demonstration"]
priority = "must"
source = "Owner-approved marketplace and documentation correction plan, followed by the request to prepare its artifact package on 2026-09-28."

[relations]
derives_from = ["CAP-DST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-28T20:39:06Z"
decided_by = "product-owner"
reason = "Human repository owner mmzen: \"I approve\", responding to the nine-artifact marketplace refresh package and required commit-bound verification for WO-PLG-026, WO-PLG-027 and WO-PLG-028. The selected pairing is plugin 0.2.1 with the unchanged released evaluator 0.19.0. Reviewed SHA-256 3ed678ce5c13d8117c817e2a0deccbd2708be88333d5944c871c092ff1524725; transition input SHA-256 3ed678ce5c13d8117c817e2a0deccbd2708be88333d5944c871c092ff1524725. Legacy 0.19.0 role product-owner encodes the right; mmzen is the human decision-maker and Codex applies it. Only confirmed assurance fields and confirmation prose were added to the three draft WOs. WO-PLG-026 and WO-PLG-027 may start after required checks. WO-PLG-028 waits for human-verified preparation coverage and separately authorized, observed publication. No external mutation is authorized."
+++

# Prepare the 0.2.1 marketplace delivery with evaluator 0.19.0

## Need and applicability

Users of Codex and Claude Code need the delivered instruction architecture through
the public Git marketplace. The observed public package remains 0.1.0/0.18.0 at
`ed68b30c88043773be929540b7b10ae537957c2d`.

This requirement defines preparation of a distinct 0.2.1 delivery. It does not
replace the accepted initial-publication definition or change its evidence.

## Required outcome

Prepare complete Codex and Claude Code marketplaces for plugin 0.2.1, containing
the unchanged published SE Harness 0.19.0 wheel selected by RLS-SEH-028. Use the
merged instruction corrections from source baseline `c4d9036fdaab378f08fe2db68978126f66ab961e` or a later
reviewed descendant containing only authorized changes.

## Acceptance

- Both manifests, inventories, native archives and PACKAGE-IDENTITY.json agree
  with the exact committed source and wheel SHA-256 `43419a0c5e7711e7888ed69c207d5599dcd39a4aeb706c8827e7bb33c46573d8`.
- Existing skills and native startup/compaction hooks are present. The existing
  assembly builder checks the generated tree without hand-written overlays.
- Fresh installs, upgrades from the public 0.1.0 package, and replacement of the
  known local 0.2.0 selection are demonstrated in disposable Windows profiles
  on both hosts. Installed and actively loaded sources are identified.
- Startup and compaction deliver the complete selected repository root. Missing
  or mismatched roots report a gap. Detailed qualification limits are retained.
- Source and assembled documentation distinguish a prepared candidate from a
  public delivery. No local success is described as a successful public update.
- Automated checks fail when documentation agrees with itself but disagrees
  with the selected manifests, released wheel or retained publication identity.

Publication and post-publication acceptance belong to the separate public-route
requirement. Preparation approval grants neither action.
