+++
id = "WO-DOC-015"
type = "work_order"
title = "Add the supplied Verity Plane logo to the published README"
status = "implemented"
owners = ["engineering-owner", "documentation-owner"]
created = "2026-09-04"
updated = "2026-09-04"

[assurance]
commit_bound_verification = "not_required"
rationale = "Transport the owner's supplied logo and authorized README publication update only; the guidance, executable behavior, managed policy, and existing definitions are unchanged."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "README.md",
  "docs/images/verity-plane-logo.png",
  "docs/engineering/harness-distribution/README.md",
  "docs/engineering/harness-distribution/work-orders/WO-DOC-015.md",
  "docs/engineering/harness-distribution/evidence/WO-DOC-015/",
]

[relations]
implements = ["REQ-DST-069"]
specifications = ["SPEC-DST-024"]
verification = ["VER-DST-024"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-04T21:06:34Z"
decided_by = "engineering-owner"
reason = "Record the owner request to add the supplied logo as a last-minute update to the authorized README publication."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-04T21:06:41Z"
decided_by = "engineering-owner"
reason = "Begin the requested supplied-logo publication update after start preflight passes."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-04T21:09:16Z"
decided_by = "engineering-owner"
reason = "Complete the owner-authorized logo publication edit after unchanged-image and unchanged-body verification, visual review, documentation tests, and released-evaluator checks; publish only after hosted checks pass."
+++

# Add the supplied Verity Plane logo to the published README

## Authority and objective

After publication through PR #344, the repository owner supplied
lockup-white-on-red.png and requested: "last minute update: can we add the logo
in the README page ?" This continues the authorized README publication task.
Copy the supplied image unchanged and display it above the title at a compact
width with descriptive alternative text and a repository-relative source.

## Scope and implementation choices

Use GitHub-compatible image markup, 360 pixels wide with its natural aspect ratio.
Keep the title left aligned and retain the approved prose, tagline, and both
Explorer screenshots. The logo is branding, not a third Explorer screenshot.
No architecture addresses REQ-DST-069; no new architecture decision is needed.
Runtime, tests, managed files, existing definitions, historical evidence, package
releases, and deployment are outside this work order.

## Verification and evidence

Compare the copied image with the supplied bytes. Confirm that removing the new
logo markup reproduces the previously published README. Inspect the local render,
image sizing and alternative text; run existing documentation tests, released
doctor, graph validation, review/scope checks, distribution validation and CLI
help. Require the hosted full regression and PR checks before publication.
Retain the results, hashes, and publication PR reference under evidence/WO-DOC-015/.

## Completion

Record implementation after the bounded change and its evidence are complete;
publish through a normal PR merge after hosted checks pass. Report the README link.
No separate assurance, release, or deployment decision is claimed.

## Stop conditions

Stop for a conflicting edit, changed logo bytes, broken rendering, invalid managed
integrity, failed required checks, or effects outside the selected publication.

## Open decisions

None.
