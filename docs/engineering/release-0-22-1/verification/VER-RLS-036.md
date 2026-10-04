+++
id = "VER-RLS-036"
type = "verification"
title = "Verify the integrated 0.22.1 release"
status = "approved"
owners = ["mmzen"]
created = "2026-10-04"
updated = "2026-10-04"

[relations]
verifies = ["REQ-DST-006", "REQ-PLG-002", "REQ-RLO-018", "REQ-RLO-021", "REQ-RLO-023"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-04T18:24:52Z"
decided_by = "mmzen"
reason = "mmzen answered \"Approve preparation and review publication\" to the exact seven-artifact evaluator 0.22.1 / plugin 0.2.6 proposal: REL-SEH-035, WO-RLS-040/041/042 and VER-RLS-036/037/038, with required commit-bound verification. This approves bounded preparation and qualification of the two HAG fixes and main already-approved dashboard correction, ordinary review pushes/draft PRs from codex/release-0-22-1 to mmzen/se_harness:main, later verification-decision updates, read-only CI rehearsals and the codex/plugin-0-2-6-staging review ref. Human verification, merge, the exact complete-release decision, adoption and provider-setting changes remain separate. Reviewed draft hashes matched; only the human-confirmed assurance fields were added before preview. Reviewed SHA-256 325ccab00f5d894f376f63507454c2990b5281a2e9343c45cf69f76e1ebdfe21."
+++

# Verify the integrated 0.22.1 release

## Independence and inputs

Derive expectations from SPEC-DST-001, SPEC-RLO-006/007, SPEC-HAG-004/005 and
SPEC-DST-020. Use released 0.22.0 as governor and exact candidate 0.22.1 as the
system under test. Historical VREC-HAG-001/002 and VREC-RLO-015 remain intact;
their separate candidates do not establish final integration assurance.

## Requirement-to-evidence matrix

| Requirement | Method and retained evidence | Pass condition |
| --- | --- | --- |
| REQ-DST-006 | Windows/Linux full-scale source suites, installed wheel/sdist checks, upgrade rehearsals, CLI and distribution checks; pinned build replay | Applicable checks pass at exact candidate C; two independent pinned recipe builds produce identical archives with complete resources. |
| REQ-PLG-002 | Inspect both manifests and shared package inputs | Both select proposed plugin 0.2.6; no host-specific policy copy or bundled runtime; exact staged package qualification is owned by WO-RLS-041. |
| REQ-RLO-018 | Inspect release membership and all five surface inputs | Each surface has an exact destination, responsible work and required observation; no unfinished hosted implementation enters the release unit. |
| REQ-RLO-021 | Inspect complete plan, decision and action boundaries | Frozen v2 plan identifies candidate, payloads, destinations, recovery and exact permitted later governance changes before approval. |
| REQ-RLO-023 | Read-only current provider inventory and readiness assessment | Required controls and credentials are evidenced; unavailable inputs prevent executable-ready claims. No settings are changed. |

## Final candidate checks

Assess all cases in VER-HAG-002, VER-HAG-003 and VER-DST-030 at C. Run current
normal/refusal tests, actual installed Windows/Linux CLI probes and the real
0.22.0-to-0.22.1 upgrade rehearsal. Retain original failures and skips. Run both
publication rehearsal legs and the complete-delivery rehearsal. A PR merge
commit is not interchangeable with C for build qualification.

Run the pinned recipe in release/build-recipe.json and hash-locked toolchain.
Bind the resulting schema-2 bundle and replay the bound RLS before release.
Capture one final aggregate VREC covering exactly REL-SEH-035's gates at C,
including staged plugin evidence under VER-RLS-037 and VER-IAR-021. Obtain
human verification of that record before requesting the final release decision.

## Evidence retention

Retain commands, runtimes, raw failures/results, extraction/source comparisons,
membership, immutable manifests, checks and review under this release domain.
Keep builds and disposable profiles outside the repository. Package qualification
does not establish public availability; VER-RLS-038 covers that later observation.
