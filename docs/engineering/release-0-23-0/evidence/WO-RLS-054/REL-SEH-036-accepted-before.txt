+++
id = "REL-SEH-036"
type = "release_contract"
title = "Release evaluator 0.23.0 and plugin 0.2.7 with the private hosted sandbox"
status = "approved"
owners = ["mmzen"]
created = "2026-10-12"
updated = "2026-10-12"

previous_release_tag = "v0.22.1"

[delivery]
route = "complete-release"

[relations]
gates = ["WO-HAG-001", "WO-HAG-005", "WO-HAG-006", "WO-HAG-007", "WO-HAG-008", "WO-HAG-009", "WO-HAG-010", "WO-HAG-011", "WO-HUP-030", "WO-IPK-002", "WO-RLS-045", "WO-RLS-046", "WO-RLS-048", "WO-RLS-049", "WO-RLS-050", "WO-RLS-051", "WO-RLS-052", "WO-RLS-053"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-12T14:05:21Z"
decided_by = "mmzen"
reason = "Human mmzen answered \"Approve preparation, verification and review publication\" to the exact evaluator/client 0.23.0 and plugin 0.2.7 package: REL-SEH-036, WO-RLS-045/046/047 and VER-RLS-039/040/041, with required commit-bound verification. This approves the bounded build-helper/setup-guide correction, current documentation, qualification, review pushes and a draft PR from codex/release-0-23-0 to mmzen/se_harness:main, later verification-decision pushes, read-only CI rehearsals and codex/plugin-0-2-7-staging review staging. The hosted service remains a private source-built sandbox and Git remains authoritative. Human verification, merge and the exact complete-release approval remain separate; adoption and host updates are excluded. Reviewed byte digests matched; only confirmed assurance fields were added before preview. Reviewed SHA-256 d3c43d948767a103d03c67a40bc05842a3436a55e0a1fdcb329d0371f13d1135."
+++

# Release evaluator 0.23.0 and plugin 0.2.7 with the private hosted sandbox

## Outcome and release unit

Distribute the merged hosted client and shared plugin guidance through evaluator
0.23.0 and plugin 0.2.7. Keep the hosted service a private sandbox built from the
tagged source. Git remains authoritative. This is a proposed release contract.

Start from main `4fb5dbc29ffd7a2ccdc9a081c9c9b9f82b99d999`. The proposed minor
version reflects the new remote interface. The previous public release is
v0.22.1 / plugin 0.2.6. Recheck that both new public identities are unused.

The gates array defines exact membership: the first hosted implementation and
reconciliation (WO-HAG-001/005/006/007), private lifecycle pilot (008), native
qualification/instruction correction (009/010), authoring simplification (011),
root-compatibility baseline (WO-HUP-030), integration-package correction
(WO-IPK-002), new release preparation/qualification (WO-RLS-045/046), and the bounded client-admission and instruction-packaging correction (WO-RLS-048).
WO-RLS-047 owns later public observations and is excluded to avoid circularity.

The advisory census also finds prior-release WO-RLS-042 and untraced merge
`e0d50ec6255576e4b5517294c9c8bfc747b2a429` (PR #536). These record prior 0.22.1
release delivery/integration, not a new product outcome. The merge differs from
the released candidate in only three inspected packaging paths: the two host
README files and release/plugin-marketplace/README.md. These are the previously
verified WO-RLS-044 documentation correction; new current-release wording is
covered by WO-RLS-045. Retain this membership assessment and recheck it at C;
do not invent an exemption or omit new product changes discovered there.

## Coordinated component boundary

| Component | Proposed delivery and evidence |
| --- | --- |
| Core evaluator and remote client | se-harness 0.23.0 wheel/sdist; exact two-build schema-2 bundle. Zero runtime dependencies remain. |
| Plugin | Both Verity Plane 0.2.7 host packages from C, bundling the exact 0.23.0 wheel; staged inventories and native qualification. |
| Hosted service | Source-built 0.1.0.dev1 from the same tagged C; no registry publication. Retain the built image identity and existing combination manifest with the bundle. |
| Hosted evaluator | Unchanged public 0.22.1, wheel cb35c3c4eb51fe0fca575a9340b1cba6cd63b5f7133a0ebeb3fd32b4ed863053 and payload 0e7b7c2bc10b06150c6c1ebe88d796d047f5d906bdfb5ef4e00914a56c79e7ff. |
| Runtime/database | Existing immutable images, dependency locks, schema/protocol and loopback/private-network deployment conditions, recorded in the combination companion. |

This extends the new release bundle with the existing combination manifest as a
referenced evidence companion, including actual service image and deployment
conditions required by HAG-OPS-003. It does not change historical bundles, the
core archive-manifest schema or the existing five-surface publisher. The built
image is a qualification input; users build the private service from tagged source.

## Verification and authority

One final human-verified VREC must bind clean candidate C, exactly all gated work
orders, their governing verification contracts, VER-RLS-039/040 and VER-IAR-021.
Historical VRECs keep their candidates and bound bytes. New identities require
current integration and applicable native checks. Missing results stay pending;
prior release-specific deferrals do not carry forward.

Released 0.22.1 governs this repository throughout preparation. Neither the
0.23.0 candidate nor publication adopts it for this checkout or the hosted service.
Keep DEC-HAG-004, SPEC-HAG-003 and the accepted HAG definitions unchanged.
RISK-HAG-001/002 remain raised. Include their limits in current guidance and the
final review; approving this package does not accept those risks.

## One complete-release decision

Select the existing complete-release route in SPEC-RLO-007. Before requesting
its one approval, prepare qualified immutable payloads, exact documentation,
demonstration inputs, staged marketplace commit and provider readiness. Freeze
the complete v2 plan and companion digests. No unresolved identity is executable.

| Surface | Destination and required completion |
| --- | --- |
| Evaluator | PyPI se-harness 0.23.0; mmzen/se_harness GitHub v0.23.0 and release/0.23; exact downloads and clean public install. |
| Marketplace | mmzen/se_harness:plugin-marketplace; exact staged 0.2.7 tree and both public fresh/0.2.6-update routes. |
| Documentation | Reviewed main/tagged source and assembled instructions; truthful versions, qualification and private-sandbox boundaries. |
| Demonstration | https://mmzen.github.io/se_harness/ with existing release-governance provenance. |
| Markers | GitHub latest=v0.23.0; last=the RLS candidate, after required public observations. |

The eventual exact approval can cover all listed delivery actions, maintenance
line, release-only integrations and permitted receipts together. Preparation
approval alone supplies none of those public permissions. Reuse the matching
final grant across providers and retries without duplicate permission requests.

## Recovery and exclusions

Before publication, changed candidate or payloads require reassessment. After
publication, preserve immutable tags/archives; inspect remote effects and resume
only missing work. Conflicting refs, missing controls or failed required checks
stop the affected action. Complete delivery requires all five surface observations.

No public service, registry image, production operation, authority cutover,
authentication/DB ACL implementation, broad performance work, provider-setting
change, repository adoption or host-plugin update is included. A separately
requested source-to-graph authority transition needs its own future package.
