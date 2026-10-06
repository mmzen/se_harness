+++
id = "REL-SEH-035"
type = "release_contract"
title = "Release evaluator 0.22.1 and plugin 0.2.6"
status = "approved"
owners = ["mmzen"]
created = "2026-10-04"
updated = "2026-10-04"

previous_release_tag = "v0.22.0"

[delivery]
route = "complete-release"

[relations]
gates = ["WO-HAG-002", "WO-HAG-003", "WO-DST-028", "WO-RLS-040", "WO-RLS-041", "WO-RLS-043"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-04T18:24:52Z"
decided_by = "mmzen"
reason = "mmzen answered \"Approve preparation and review publication\" to the exact seven-artifact evaluator 0.22.1 / plugin 0.2.6 proposal: REL-SEH-035, WO-RLS-040/041/042 and VER-RLS-036/037/038, with required commit-bound verification. This approves bounded preparation and qualification of the two HAG fixes and main already-approved dashboard correction, ordinary review pushes/draft PRs from codex/release-0-22-1 to mmzen/se_harness:main, later verification-decision updates, read-only CI rehearsals and the codex/plugin-0-2-6-staging review ref. Human verification, merge, the exact complete-release decision, adoption and provider-setting changes remain separate. Reviewed draft hashes matched; only the human-confirmed assurance fields were added before preview. Reviewed SHA-256 f989e5d3e82a3fd285cede989bad3cf81a791053fc341b49703a6f65e7960da1."
+++

# Release evaluator 0.22.1 and plugin 0.2.6

## Outcome and release unit

Publish evaluator 0.22.1 and plugin 0.2.6 so the hosted project can later adopt
released standalone draft validation and accurate decision-owner attribution.
The release also includes main's already-approved 4 MiB dashboard correction
under WO-DST-028; it is already present in the proposed main baseline and has
not previously shipped in an evaluator archive.

Use isolated preparation from main 82f5a0ed7438a73da8f03aee23ad02a9b8cc09e1.
Extract only the two HAG corrections and transport their governing records and
historical evidence. Exclude the unfinished hosted service and WO-HAG-001 from
the release unit. Preserve PR #535 and its inputs-branch target. No comparison
base change, silent ownership change or live decision disposition is permitted.

The gates array is the exact proposed release membership. One final verified
VREC at clean candidate C must cover all six work orders and VER-HAG-002,
VER-HAG-003, VER-DST-030, VER-RLS-036, VER-RLS-037, VER-RLS-004 and VER-IAR-021. Earlier
VREC-HAG-001/002 and VREC-RLO-015 retain their original candidates/evidence.
WO-RLS-042 owns post-publication observations and is excluded from this set.

## Complete-release route

Select the existing complete-release route in SPEC-RLO-007. Released 0.22.0
governs. Prepare and verify all immutable deliverables before the one final
release/publication request. Package approval permits bounded preparation only;
it does not approve the later exact RLS, public actions, adoption or changed
provider settings. Verify actual controls before claiming the route is executable.

| Surface | Destination and completion evidence |
| --- | --- |
| Evaluator | PyPI se-harness 0.22.1, GitHub v0.22.1, release/0.22; exact bound archives and clean public install. |
| Marketplace | mmzen/se_harness:plugin-marketplace, both plugin 0.2.6 packages; staged-to-public identity and required fresh/0.2.5-update observations. |
| Documentation | Reviewed current files on main and assembled package instructions; matching versions and readable routes. |
| Demonstration | https://mmzen.github.io/se_harness/; existing release-governance provenance and readback. |
| Markers | GitHub latest=v0.22.1 and last=the exact RLS candidate, after required public observations. |

Use the existing v2 delivery plan, schema-2 bundle, deterministic staging,
publisher and frozen-plan decision/receipt integration. Candidate, archive,
staging tree and previous ref identities are filled from observations during
preparation; no invented values and no executable plan with unresolved inputs.
All paths permitted for later integration must be fixed before final approval.

## Checks, recovery and exclusions

Meet the listed verification contracts on the final candidate. Missing required
native/desktop evidence stays pending; prior release omissions do not carry
forward. No service scenario is claimed by evaluator or plugin verification.
Inspect provider readiness and do not alter settings under this package.

Before publication, changed inputs require fresh qualification and a matching
review. After publication, preserve immutable version tags/archives. Inspect
uncertain effects; reuse exact completed outputs and resume only missing work.
Conflicting refs, content or missing controls stop the affected action. The
observation window ends only after all required public checks pass; publish
latest/last afterward under the same matching complete-release grant.

Repository/host adoption, linked preserved revisions of SPEC-HAG-003 and
VER-HAG-001, and applying the already-selected DEC-HAG-001 option remain a
separate bounded package after release. No historical decision is repeated.

## Linked revision for the native qualification defect

This revision adds only WO-RLS-043 and VER-RLS-004 to the release unit and final
aggregate verification. It corrects transition snapshots of absent draft
evidence under existing REQ-WEX-002 and SPEC-WEX-001. Versions, delivery route,
provider controls, public destinations and all remaining acceptance criteria
are unchanged. The prior accepted version is preserved byte-for-byte at
../evidence/WO-RLS-043/REL-SEH-035-accepted-before.txt, SHA-256 `7249aa639db1cc412849fa2a54e8fe6135a8813fb4e9031295f1d1cebaa0ea4f`.

Activation requires mmzen's explicit authorization of this exact manual linked
amendment because released 0.22.0 has no supported revision command. Retain the
actual human decision in the amendment evidence; preserve existing lifecycle
history and prior evidence. This proposal alone does not activate the revision.
