+++
id = "VER-RLS-033"
type = "verification"
title = "Verify the integrated 0.22.0 release"
status = "approved"
owners = ["mmzen"]
created = "2026-10-03"
updated = "2026-10-02"

[relations]
verifies = ["REQ-DST-006", "REQ-PLG-002", "REQ-RLO-018", "REQ-RLO-020"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T22:07:58Z"
decided_by = "mmzen"
reason = "Human repository owner mmzen answered \"Approve package and required verification\" to the reviewed evaluator 0.22.0 / plugin 0.2.5 package: REL-SEH-034, WO-RLS-034/035/036 and VER-RLS-033/034/035. This confirms required commit-bound verification and authorizes bounded preparation, qualification, review pushes/PRs and listed delivery work under the retained request \"Merged. Next: prepare and execute the release\". Human verification of exact results, the exact release-record decision and merge remain separate. Repository adoption and provider-setting changes are excluded. Selected released 0.21.0 governs; Codex applies the recorded human decision. Reviewed SHA-256 6c3244490e617cb4b6cbe44b1363a792821823db7b5f1d15d2cdee2493b57adb; transition-input SHA-256 6c3244490e617cb4b6cbe44b1363a792821823db7b5f1d15d2cdee2493b57adb. Only confirmed assurance fields were added."
+++

# Verify the integrated 0.22.0 release

## Independence

Expected results come from SPEC-DST-001, SPEC-PLG-001, SPEC-RLO-006 and the
accepted contracts of REL-SEH-034's implementation members. Selected public
0.21.0 governs real artifacts; installed candidate 0.22.0 is tested separately.

## Requirement-to-evidence matrix

| Requirement | Method | Evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-DST-006 | test, inspection | Final Windows/Linux source suites, installed wheel/sdist checks, upgrade rehearsal and pinned bundle | Full-scale suites and applicable required CI pass at the identified candidate; two recipe builds yield identical 0.22.0 archives with complete resources. |
| REQ-PLG-002 | test, inspection | Manifests, shared inventory, existing package tests | Both host manifests select unused 0.2.5; shared assets remain one source and the post-publication assembly is explicitly owned. |
| REQ-RLO-018 | inspection | Release membership and five-surface plan | Every surface has an owner, destination, disposition, work order and required observation; future hashes remain pending until produced. |
| REQ-RLO-020 | test, inspection | Existing delivery/recovery fixtures and status review | Failed, missing or deferred surfaces keep closeout incomplete; future complete-route activation is not claimed. |

## Final integration checks

Run the full source suite with full scale on Windows and Linux, the existing
distribution and installed-package checks, upgrade rehearsals from selected
0.21.0, and both publication rehearsal legs. Retain exact runtimes and skips.
Use the existing pinned recipe and toolchain. Without a local Docker engine,
dispatch the existing read-only candidate rehearsal at the release branch head
and confirm that its build manifest names that head, not a PR merge commit.

Assess VER-KIS-004/005/006 and VER-RLO-011 at the final integration. Reuse earlier
inspection evidence only after checking input equivalence. Run current tests
for modified behavior. Keep the live provider inventory's unobserved fields
visible; no provider setting is changed by qualification.

Capture one VREC covering exactly REL-SEH-034's ten work orders and all their
contracts. Human verification concerns its exact clean commit and evidence.
After verification, prepare the RLS with tag v0.22.0, bind the schema-2 bundle
and pass bound-record replay before the release-owner decision.

## Evidence retention and limits

Retain source identities, membership assessment, checks, original failures,
manifests and public build-artifact references in evidence/WO-RLS-034/.
Canonical VREC/RLS companions remain directly under this domain's evidence/.
Preserve every earlier record. Package source qualification is not public
plugin qualification; WO-RLS-035/036 own those downstream observations.
