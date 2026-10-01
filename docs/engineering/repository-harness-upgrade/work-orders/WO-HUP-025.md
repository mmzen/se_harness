+++
id = "WO-HUP-025"
type = "work_order"
title = "Adopt public 0.20.1 in the repository and CI"
status = "in_progress"
owners = ["mmzen"]
created = "2026-10-01"
updated = "2026-10-01"

[assurance]
commit_bound_verification = "required"
rationale = "Human mmzen approved the reviewed adoption package and required commit-bound verification. Later governance and candidate qualification rely on the evaluator selection, lock, CI configuration and retained transaction."
decided_by = "mmzen"

[execution_scope]
paths = [
  ".engineering-harness.toml",
  ".engineering-harness.lock",
  "ENGINEERING_HARNESS.md",
  ".github/workflows/engineering-harness.yml",
  "docs/notes/developing-se-harness.md",
  "docs/notes/harness-installation-and-upgrades.md",
  "docs/engineering/repository-harness-upgrade/README.md",
  "docs/engineering/instruction-architecture/README.md",
  "tests/test_progressive_documentation.py",
  "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-025.md",
  "docs/engineering/repository-harness-upgrade/verification/VER-HUP-023.md",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-025/",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-025-evaluator-upgrade.json",
  "docs/engineering/repository-harness-upgrade/verification-records/VREC-HUP-024.md",
  "docs/engineering/repository-harness-upgrade/evidence/VREC-HUP-024-evaluator.json",
]

[relations]
implements = ["REQ-REB-027"]
specifications = ["SPEC-REB-012"]
verification = ["VER-HUP-023"]
architecture = ["ARCH-REB-011", "ADR-REB-011"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-01T13:48:14Z"
decided_by = "engineering-owner"
reason = "Human mmzen: I approve. Approves the reviewed WO-HUP-025 and VER-HUP-023 adoption package, required commit-bound verification, exact public 0.20.1 adoption, private evaluator switch and bounded ordinary branch-push/draft-PR envelope. Reviewed SHA256 3e7a843376a9ef15f4c3877016599e6028f0f3a481dfa6a4ac254ac9ae02e922; transition input SHA256 c97acfaa2f8c3545bbc1094841075830ed9cf164a25748111d510e33a924f673. Only the confirmed work-order assurance fields were added. Codex applies the human decision using the selected released evaluator engineering-owner encoding. Verification acceptance and merge remain separate."
scope_paths = [".engineering-harness.toml", ".engineering-harness.lock", "ENGINEERING_HARNESS.md", ".github/workflows/engineering-harness.yml", "docs/notes/developing-se-harness.md", "docs/notes/harness-installation-and-upgrades.md", "docs/engineering/repository-harness-upgrade/README.md", "docs/engineering/instruction-architecture/README.md", "tests/test_progressive_documentation.py", "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-025.md", "docs/engineering/repository-harness-upgrade/verification/VER-HUP-023.md", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-025/", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-025-evaluator-upgrade.json", "docs/engineering/repository-harness-upgrade/verification-records/VREC-HUP-024.md", "docs/engineering/repository-harness-upgrade/evidence/VREC-HUP-024-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-01T13:50:05Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."
+++

# Adopt public 0.20.1 in the repository and CI

## Objective

Select released SE Harness 0.20.1 as the evaluator for mmzen/se_harness and
its CI. This is the separate adoption required by REL-SEH-032 after the release
and plugin delivery. It enables later independent qualification of the
minimal-layout candidate; that qualification remains separate work.

Reuse the accepted simple-upgrade contract, architecture and decision.
One work order and one verification contract are enough. No new product
requirement, upgrade framework, architecture decision or release is needed.

## In scope

1. Use RLS-SEH-030's public wheel, `se_harness-0.20.1-py3-none-any.whl`,
   SHA-256 `300923b4ea800487a7b96822768ff5fbd5c428305ac670948aef404282349764`.
   Its installed payload must match
   `70d70f9912a3f40865e1bd50ffb1b377f2fb4c29f87575444cf3ae175be0896a`.
   Install those bytes offline in the existing private evaluator environment
   after execution approval. Do not substitute a checkout build.
2. Recheck the target preview and apply the matching released installer plan.
   The reviewed preview updates `.engineering-harness.toml` and
   `ENGINEERING_HARNESS.md`; the installer also writes its lock. It changes no
   conditional guide or template and requires no entry-retirement evidence.
   Select no `--replace-file` option. Retain one upgrade transaction at the
   exact evidence path listed above. Never edit the lock by hand.
3. Change only the owner-maintained CI evaluator pin from 0.20.0 to 0.20.1.
4. Update current adoption facts in the four named guides/indexes. Preserve
   historical release and adoption accounts. Make the existing installation
   example test expect 0.20.1 while retaining its ordering and safety checks.
5. Run VER-HUP-023. Retain the results, record implementation completion and
   prepare the exact-candidate VREC-HUP-024 through the released procedure.

## Out of scope

Product code, source templates, lifecycle rules, new tests, source-version
changes, the minimal-resource implementation and its qualification, plugin or
host updates, credential changes, accepted-definition amendments, unrelated
documentation corrections, deletion of owner files, release or marketplace
publication, tag changes and merges. Development source remains 0.21.0.

## Proposed assurance and decision envelope

Required commit-bound verification is proposed: later governance and candidate
qualification depend on the evaluator selection, lock, CI and adoption evidence.
The human must confirm that classification when approving this work order.
No assurance decision or lifecycle approval is recorded by this draft.

Approval authorizes the bounded local implementation, private evaluator switch,
checks, commits, evidence, work completion and VREC preparation. It also covers
ordinary pushes of `work/adopt-0-20-1` and a draft PR to `main` in
`mmzen/se_harness` for this exact package, including read-only hosted CI and
receipt updates within scope. No force push is included. Human verification,
each merge, later successor qualification and external release actions remain
separate decisions.

If the selected 0.20.0 evaluator requires its legacy `engineering-owner` label
for approval, use that encoding only to apply the human's actual decision.
Retain mmzen and the exact decision in the transition reason. The label is
not a separate person and does not grant authority to an agent.

## Constraints

Start from main `aeebcabf8e3ed958e0166dfe2754a2af2681a59d`. Use public 0.20.0
for authoring, approval and work start. Use exact public 0.20.1 for upgrade
preview/apply. After successful apply, use 0.20.1 for repository governance.
Keep the target evaluator outside the checkout and invoke it with `-I`.

The target's pre-upgrade doctor reports three expected differences: the root
version text, evaluator payload and selected version. Current 0.20.0 doctor
passes. Preserve this observation; any other failure must be assessed before
apply. An unchanged plugin or manually read root does not prove automatic
instruction delivery in the chat's parent directory.

Preserve AGENTS.md, absent CLAUDE.md, removed legacy pointers, templates,
machine policy and prior formal/evidence records. Preserve all owner settings
except the specifically selected version and CI pin. Prior release and
verification records keep their original meaning and bytes.

## Expected change surface

Three installation files, one CI pin, four current documentation files, one
existing test expectation, and this work's exact formal/evidence paths. The
evidence directory admits only this adoption's observations and review material.
No product source or broad test directory is authorized.

## Required verification and evidence

Meet A0201-01 through A0201-05 in VER-HUP-023. Require target identity, doctor,
complete validation, released-root qualification, no-op upgrade replay,
predecessor transition assessment, owner-file preservation, documentation and
full source tests, distribution and CLI checks, complete scope/handoff checks,
and applicable hosted Linux/Windows checks before integration. Bind assurance
to the exact clean candidate; do not reuse the release VREC as adoption evidence.

Retain actual commands, identities, previews, the transaction, file comparisons,
check summaries, failures and candidate identity. Preserve all earlier evidence.
Keep new raw test logs outside the repository and retain concise summaries.

## Stop and escalate conditions

Stop the affected action for a different public identity, customized or unsafe
input, an unexpected installer path, an unapproved owner replacement, a changed
integration base, a failed required check, or an implementation edit outside
scope. If the planned VREC ID is occupied, review the new destination before
preparation. Do not expand scope or weaken checks to complete adoption.

## Completion report

Report the adopted evaluator, unchanged development version, actual file delta,
preservation checks, transaction, candidate commit and VREC. State platform
limits and remaining human decisions. Adoption is not applied while this work
remains draft; the new layout is not qualified by this adoption alone.
