+++
id = "VER-DST-024"
type = "verification"
title = "Verify the reviewed Verity Plane README publication"
status = "approved"
owners = ["quality-owner", "documentation-owner"]
created = "2026-09-04"
updated = "2026-09-04"

[relations]
verifies = ["REQ-DST-069"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-04T20:43:53Z"
decided_by = "quality-owner"
reason = "Record the technical acceptance checks needed to publish the exact owner-reviewed documentation safely; no VREC decision is made."
+++

# Verification: Verify the reviewed Verity Plane README publication

## Method and independence

Compare the repository README and new PNG byte-for-byte with the owner-reviewed
deliverables. Derive static checks from SPEC-DST-024, command checks from the
current parser, and factual claims from existing implementation and managed policy.
The owner's prior visual/content review is distinct from agent-run test evidence;
neither is reported as a new formal assurance or package-release decision.

## Checks

- Inspect the reviewed opening, workflow, prospective Twin claim, and title/tagline.
- Count source words, lines, headings, and code fences.
- Resolve local routes and inspect both PNG signatures and dimensions.
- Parse the README's init, adopt, and doctor command forms against the CLI.
- Preserve the detailed-note checks for command coverage, authority, and safe upgrades.
- Run focused onboarding/progressive-documentation tests and the full unit suite.
- Run the released evaluator's doctor, graph validation, start/review preflight,
  and scoped checkpoint; run release-distribution validation and candidate CLI help.
- Review the final diff, protected paths, and git diff --check.
- Verify the published GitHub README and image match the approved local bytes.

## Evidence and pass criteria

Retain commands, results, reviewer input, file hashes, scope, and any unrelated
baseline failures under evidence/WO-DOC-014/. Required checks must pass; any
external limitation is reported explicitly. No old evidence or lifecycle record
is rewritten. The publication does not create a package release.

## Open decisions

None.
