+++
id = "VER-RLS-030"
type = "verification"
title = "Verify the 0.21.0 release candidate and delivery handoff"
status = "approved"
owners = ["mmzen"]
created = "2026-10-01"
updated = "2026-10-01"

[relations]
verifies = ["REQ-DST-006", "REQ-PLG-002", "REQ-IAR-031", "REQ-RLO-018", "REQ-RLO-020"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-01T19:53:49Z"
decided_by = "engineering-owner"
reason = "Human mmzen: Approve package and required verification. Approves REL-SEH-033, WO-RLS-031/032/033 and VER-RLS-030/031/032, required commit-bound verification, plugin 0.2.4, ordinary release-review branch push/draft PR and read-only CI rehearsals. Existing v0.21.0 publication authorization is retained. Final-candidate verification, exact RLS decision and unresolved desktop evidence remain separate. Reviewed SHA256 56589749ed8db0fcec6013eb396e033e2041acf1d61532fc13946af67f47ce51; transition-input SHA256 56589749ed8db0fcec6013eb396e033e2041acf1d61532fc13946af67f47ce51. Only confirmed work-order assurance metadata was added. Codex applies the human decision using the selected evaluator role-label encoding; mmzen is the decision-maker."
+++

# Verify the 0.21.0 release candidate and delivery handoff

## Independence

Expected behavior comes from SPEC-DST-001's distribution requirement,
SPEC-PLG-001, SPEC-IAR-016 and SPEC-RLO-006. DEC-IAR-003 supplies the accepted
successor-layout boundary; historical copied-installation examples do not
override it. Released 0.20.1 governs; 0.21.0 is tested outside its source checkout.

## Requirement-to-evidence matrix

| Requirement | Method | Evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-DST-006 | test, inspection | Final Windows/Linux source and installed-package checks; pinned replay and bundle | Exact candidate C passes existing suites and public-0.20.1 independent candidate qualification. Two digest-pinned Linux/amd64 builds yield identical 0.21.0 wheel and sdist. |
| REQ-PLG-002 | test, inspection | Both manifests, shared assembly inventory and assembly tests | Both proposed host inputs select unused plugin 0.2.4 and include the accepted bootstrap, activation and resource adapter. No candidate wheel is claimed as a public wheel. |
| REQ-IAR-031 | test, inspection, demonstration | Final resource/migration scenarios and VER-IAR-020/021/022 assessment | The two-file default, explicit integrations, direct authoring, native delivery, safe retirement, refusal and recovery criteria pass. Original desktop uncertainty stays pending; earlier acceptance does not waive it. |
| REQ-RLO-018 | inspection | Five-surface plan with downstream WO-RLS-032/033 | Evaluator, marketplace, current documentation, demonstration and markers each name an owner, destination, disposition and next action. Future digests remain pending until produced. |
| REQ-RLO-020 | test, inspection | Existing closeout tests and pending-marketplace check | Missing or pending surfaces return incomplete, even when evaluator publication succeeds. |

## Final candidate and record

Capture one aggregate VREC covering every REL-SEH-033 member at the same clean
candidate C, with VER-IAR-020, VER-IAR-021, VER-IAR-022 and this contract.
Run the complete source suite with full scale, distribution checks, installed
wheel/sdist checks, resource acceptance, predecessor upgrade rehearsals and both
manual publication rehearsal legs. Retain their exact commits and runtime roles.
Read-only hosted rehearsal may provide the pinned build when no local engine is
available. Pull-request merge-commit results are not candidate-head build evidence.

Compare old native evidence against the final input identities before reuse.
Changed hook, plugin, resource or host inputs require matching observations.
Use genuine startup, manual and automatic compaction, resume and session-selection
traces required by VER-IAR-021. Its Windows desktop criterion remains required.
No new release exception or platform waiver is supplied by this contract.

After the human verifies the aggregate VREC, prepare the RLS with tag v0.21.0,
bind the schema-2 bundle and run bound-record replay before the release decision.
This later replay is not retroactively added to the already bound VREC.

## Evidence retention

Retain concise observations, permanent build manifests and required native traces
under evidence/WO-RLS-031/ in this domain. Capture creates the VREC and companion
at the same domain's canonical paths. Preserve original failures and prior VRECs.

## Residual uncertainty

No final candidate, aggregate VREC, distribution digest or RLS exists yet.
Public plugin qualification follows evaluator publication under VER-RLS-031 and
VER-RLS-032. Neither evaluator publication nor this contract establishes desktop
support or repository adoption.
