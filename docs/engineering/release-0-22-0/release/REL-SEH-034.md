+++
id = "REL-SEH-034"
type = "release_contract"
title = "Release 0.22.0 and deliver plugin 0.2.5"
status = "approved"
owners = ["mmzen"]
created = "2026-10-03"
updated = "2026-10-02"

previous_release_tag = "v0.21.0"

[relations]
gates = ["WO-KIS-010", "WO-KIS-011", "WO-KIS-012", "WO-KIS-013", "WO-KIS-014", "WO-RLO-014", "WO-RLO-015", "WO-RLO-016", "WO-RLO-017", "WO-RLS-034"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T22:07:58Z"
decided_by = "mmzen"
reason = "Human repository owner mmzen answered \"Approve package and required verification\" to the reviewed evaluator 0.22.0 / plugin 0.2.5 package: REL-SEH-034, WO-RLS-034/035/036 and VER-RLS-033/034/035. This confirms required commit-bound verification and authorizes bounded preparation, qualification, review pushes/PRs and listed delivery work under the retained request \"Merged. Next: prepare and execute the release\". Human verification of exact results, the exact release-record decision and merge remain separate. Repository adoption and provider-setting changes are excluded. Selected released 0.21.0 governs; Codex applies the recorded human decision. Reviewed SHA-256 a214fdab7c991d6a8900c8c1db1d196fc2db361edf3982f34da6f1fe8542305d; transition-input SHA-256 a214fdab7c991d6a8900c8c1db1d196fc2db361edf3982f34da6f1fe8542305d. Only confirmed assurance fields were added."
+++

# Release 0.22.0 and deliver plugin 0.2.5

## Release unit

Prepare the successor to public v0.21.0 from merged main
de1d102b5f70b49ca1d2572e005d5daf7a570621. Propose evaluator 0.22.0 for the new
workflow capabilities and plugin 0.2.5 for their shared instructions. Recheck
unused public and local identities before building or publishing.

The gates array contains five approval/review simplification work orders,
four complete-release work orders, and WO-RLS-034 release preparation.
One final verified VREC must cover that exact set at clean candidate C under
VER-KIS-004, VER-KIS-005, VER-KIS-006, VER-RLO-011 and VER-RLS-033.

The v0.21.0 release/publication records and repository-only adoption/CI
maintenance remain historical supporting inputs. WO-RLS-035/036 are owned
downstream delivery work, excluded from the pre-publication VREC to avoid a
dependency cycle. Missing first-parent trailers in the advisory census do not
add scope or require invented exemptions. Do not replay completed work orders.

## Rollout boundary

Use selected released evaluator 0.21.0 for this release. SPEC-RLO-007 requires
the supporting product to be released and adopted before activating its new
complete-release route. This rollout therefore uses the existing release and
marketplace procedures and does not declare delivery.route = complete-release.

Package approval covers preparation and the proposed delivery scope; preserve
mmzen's request to prepare and execute the release as continuing external
intent. Apply matching exact grants once their reviewable inputs exist. Work
approval does not invent an assurance verdict or the exact RLS release decision.
The protected PyPI environment still requires its configured reviewer action.
Changing that control or adopting the release requires its own reviewed work.

## Required sequence

1. Approve WO-RLS-034/035/036, VER-RLS-033/034/035 and this contract, including
   required commit-bound assurance and bounded review pushes/PRs/rehearsals.
2. Implement version/current-guidance updates and complete final integration
   qualification. Produce wheel/sdist through two exact pinned recipe builds.
3. Publish the review before requesting human verification of the final VREC.
4. Prepare tagged RLS-SEH-032, bind the schema-2 manifest, pass bound-record
   replay and obtain the release-owner decision on that exact record.
5. Integrate through the reviewed PR route. Resolve publication against main,
   run the protected publisher and verify independent public distribution bytes.
6. Execute WO-RLS-035: assemble from the public wheel, verify exact packages,
   then publish the marketplace through an ordinary descendant commit.
7. Execute WO-RLS-036: verify public routes, current documentation and Pages;
   promote latest/last after the required observation window; retain closeout.

## Delivery surfaces

| Surface | Target | Work and completion evidence |
| --- | --- | --- |
| Evaluator | PyPI se-harness 0.22.0; GitHub v0.22.0; maintenance line release/0.22 | WO-RLS-034: publisher, exact archive digests and clean public install. |
| Marketplace | mmzen/se_harness:plugin-marketplace; both host packages 0.2.5 | WO-RLS-035/036: qualified shared inputs, descendant public commit, fresh and 0.2.4 update observations. |
| Documentation | Current main and assembled install/release instructions | WO-RLS-034/036: truthful proposal/publication/activation statements, link checks and merged readback. |
| Demonstration | https://mmzen.github.io/se_harness/ | Existing publisher and WO-RLS-036: deployed governance provenance. |
| Release markers | GitHub latest = v0.22.0; last = exact RLS candidate | WO-RLS-036: match the retained execution grant, expected old refs and final readbacks. |

Retain the existing v1 delivery-plan format under evidence/WO-RLS-034/.
Final candidate, archive digests, RLS and marketplace commits remain pending
until generated and reviewed. No new authority format or service is introduced.

## Compatibility, evidence and security

Keep this repository pinned to 0.21.0. Test real predecessor upgrades in isolated
repositories. Preserve owner content, existing records and published identities.
Candidate code must not execute with publication credentials. Use the existing
OIDC workflow, protected refs, recipe and marketplace builder.

Required host criteria stay required. Assess current native evidence explicitly;
0.21.0-specific accepted omissions do not waive them. A missing required result
blocks its affected action and completion claim until formally resolved.

## Recovery and observation

Before publication, a changed candidate needs refreshed builds and verification.
Correct out-of-scope product defects through bounded work. After publication,
preserve immutable archives and version tags; fixes require a new version.
Inspect remote state before retries. Do not force a marketplace branch or move
a conflicting maintenance line. Move last only with its exact observed old-ref
lease; unknown or changed state stops that action.

The observation window ends after publisher success, independent matching
archives, a clean public evaluator install and required marketplace public
routes. Check Pages and current guidance, then update/read back latest and last.
Overall delivery remains incomplete while a declared surface is pending, failed,
unobserved or deferred. Subsequent repository adoption and provider activation
are follow-up work, not completion claims of this release.
