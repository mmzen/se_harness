+++
id = "WO-DOC-016"
type = "work_order"
title = "Refresh the public README for published plugin onboarding"
status = "implemented"
owners = ["engineering-owner", "documentation-owner"]
created = "2026-09-15"
updated = "2026-09-16"

[assurance]
commit_bound_verification = "required"
rationale = "Users will rely on the rewritten public installation and setup guidance; this changes trusted engineering guidance rather than solely transporting an existing decision."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "README.md",
  "docs/engineering/harness-distribution/README.md",
  "docs/engineering/harness-distribution/work-orders/WO-DOC-016.md",
  "docs/engineering/harness-distribution/verification/VER-DST-029.md",
  "docs/engineering/harness-distribution/evidence/WO-DOC-016/",
  "docs/engineering/harness-distribution/verification-records/VREC-DOC-008.md",
  "docs/engineering/harness-distribution/evidence/VREC-DOC-008-evaluator.json",
]

[relations]
implements = ["REQ-DST-069"]
specifications = ["SPEC-DST-024"]
verification = ["VER-DST-029"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-16T05:51:30Z"
decided_by = "engineering-owner"
reason = "The owner approved the reviewed README and both named artifacts by replying i approve to the exact approval package; all three reviewed SHA-256 inputs still match."
scope_paths = ["README.md", "docs/engineering/harness-distribution/README.md", "docs/engineering/harness-distribution/work-orders/WO-DOC-016.md", "docs/engineering/harness-distribution/verification/VER-DST-029.md", "docs/engineering/harness-distribution/evidence/WO-DOC-016/", "docs/engineering/harness-distribution/verification-records/VREC-DOC-008.md", "docs/engineering/harness-distribution/evidence/VREC-DOC-008-evaluator.json"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-16T05:55:31Z"
decided_by = "codex-executor"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed. Start the approved README implementation after the released evaluator start preflight passed."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-16T06:10:05Z"
decided_by = "codex-executor"
reason = "Execution of DR-WO-COMPLETE under recorded engineering-owner approval; relevant local gates passed. Completed the exact owner-reviewed README and index update; 1068 source tests passed with 15 skips, 30 documentation checks passed, distribution and released-governor checks passed, and the Git-derived handoff passed with retained evidence."
+++

# Work order: Refresh the public README for published plugin onboarding

## Objective and review input

After the plugin publication merged, the repository owner requested a rewrite of
the main README. Make the published Codex and Claude Code installation paths easy
to find, explain the relationship between SE Harness and the Verity Plane plugin,
and accurately describe how setup installs the bundled checker.

The complete proposed README is supplied for review as `README-proposed.md`,
SHA-256 `d9cb469ccda4438134ee23b46852a58ecc91595dd2ce87437f4967a4ea1a7c8b`.
It is 593 whitespace-separated source words, 108 lines and six level-two headings.
The proposal remains outside the source checkout until this work is approved.
Approval of this work order selects that concrete content for implementation.

## In scope

Replace README.md with the reviewed proposal, add this packet to the domain index,
retain the approved input and verification evidence, and prepare the exact
candidate's ready VREC-DOC-008. The README puts installation before the workflow
and vision, presents both native host commands and the PyPI CLI route, describes
offline setup of the bundled released 0.18.0 checker, and keeps the logo, screenshots,
required deeper links and human decision boundaries.

## Existing contracts and simplicity

Reuse approved REQ-DST-069 and SPEC-DST-024 without amendment. The proposal meets
their existing budgets and all 30 existing public-onboarding and progressive-
documentation checks without changing tests. VER-DST-029 supplies the new review
inputs, plugin factual checks and evidence destination; VER-DST-024 remains the
historical publication contract. No active architecture addresses REQ-DST-069,
and this presentation change needs no new architecture or ADR.

## Out of scope

Product code, tests, plugin packages and catalogs, managed files, package metadata,
other documentation rewrites, historical definitions and evidence, provider portal
submissions, releases, tags, deployment and branch deletion. Preserve both
`plugin-marketplace` and `work/plugin-marketplace-publication`.

## Authorized decision envelope

Once approved, the executor may perform the scoped local edits and commits,
required checks, evidence retention, completion recording and VREC preparation
under DR-015. Use the reviewed README bytes; return material content changes for
review. Record only observed results. The executor may choose ordinary evidence
file names inside the scoped directory and reuse unchanged native acceptance
inputs with an explicit comparison. This work order does not authorize a push,
PR creation, merge, new publication, assurance decision or release decision.

## Required verification and evidence

Apply VER-DST-029 and the repository's required checks. Retain the reviewed input,
its hash, commands and outcomes, content/render review and complete path review
under `docs/engineering/harness-distribution/evidence/WO-DOC-016/`. Prepare the
ready record only after implementation and its required evidence are complete.
The full implementation checks are not claimed by the proposal's 30 passing
read-only documentation checks.

## Stop conditions

Stop the affected action for changed reviewed input, overlapping owner work,
invalid managed integrity, invalid governing chain, an ID collision, a required
check failure, unsupported installation or capability claims, or effects outside
this scope. Do not edit or reinterpret historical approval or verification facts.

## Completion report

Report the README and candidate identity, checks and material limitations, the
actual work-order state and ready verification record, and the next accountable
decision returned by the released evaluator. Claim no publication before its
separately authorized action and observed readback.
