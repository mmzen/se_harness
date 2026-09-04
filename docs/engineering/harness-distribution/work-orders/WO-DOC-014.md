+++
id = "WO-DOC-014"
type = "work_order"
title = "Publish the owner-reviewed Verity Plane README"
status = "in_progress"
owners = ["engineering-owner", "documentation-owner"]
created = "2026-09-04"
updated = "2026-09-04"

[assurance]
commit_bound_verification = "required"
rationale = "Public guidance and its regression contract are trusted engineering state; technical evidence does not itself create a formal assurance decision."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "README.md",
  "docs/images/harness-explorer-virtual-twin.png",
  "tests/test_public_onboarding.py",
  "tests/test_progressive_documentation.py",
  "tests/test_integration_package.py",
  "docs/engineering/harness-distribution/README.md",
  "docs/engineering/harness-distribution/requirements/REQ-DST-069.md",
  "docs/engineering/harness-distribution/specifications/SPEC-DST-024.md",
  "docs/engineering/harness-distribution/verification/VER-DST-024.md",
  "docs/engineering/harness-distribution/work-orders/WO-DOC-014.md",
  "docs/engineering/harness-distribution/evidence/WO-DOC-014/",
]

[relations]
implements = ["REQ-DST-069"]
specifications = ["SPEC-DST-024"]
verification = ["VER-DST-024"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-04T20:43:53Z"
decided_by = "engineering-owner"
reason = "Execute the owner request to apply and publish the reviewed README, with the scoped contract and regression reconciliation required for that change."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-04T20:44:45Z"
decided_by = "engineering-owner"
reason = "Begin the owner-approved README publication after passing released-evaluator start preflight."
+++

# Work order: Publish the owner-reviewed Verity Plane README

## Authority and objective

On 2026-09-04, after reviewing the complete README proposal and its successive
content, image, and typography revisions, the repository owner instructed:
"good, can you make the change to the SE Harness repository and publish this README.md file".
This work order records that concrete approval and the requested repository
publication. Supporting contract/test updates preserve the reviewed result and
its installation, evidence, and human-authority safeguards. No separate package
release, tag, deployment, or formal assurance decision is inferred.

## In scope

Apply the reviewed Markdown and supplied Virtual Twin screenshot, reconcile the
public presentation checks under the new contract, retain evidence, and publish
through a branch and pull request. Keep the approved wording and image bytes.

## Out of scope

Runtime behavior, managed files, CI definitions, package metadata, old artifacts
and evidence, other documentation rewrites, release records, and product deployment.
No active architecture addresses REQ-DST-069; this presentation remains within the
existing root-to-notes layering and requires no new architecture relation.

## Authorized implementation choices

Choose test assertions for the specified behavior, preserve existing note coverage,
and use a normal fast-forward/merge workflow without rewriting published history.

The full regression run identified one additional root-presentation assertion in
tests/test_integration_package.py. Under the owner's instruction to publish the
reviewed README and reconcile its supporting checks, this scope includes replacing
that retired wording assertion with the root-to-notes link. All integration-package
installation and authority-boundary assertions remain unchanged.

## Required verification and evidence

Apply VER-DST-024 and retain results under evidence/WO-DOC-014/. Record the approved
input hashes and exact publishing commit. Agent-run evidence does not claim an
independent human assurance decision.

## Stop conditions

Stop for overlapping user work, invalid managed integrity, unsupported claims,
failed required checks, or effects outside the selected paths and publication.

## Completion report

Report the published README/PR link, technical check results, actual work-order
state, and any remaining formal assurance requirement without claiming a release.
