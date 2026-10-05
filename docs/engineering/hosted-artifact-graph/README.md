# Hosted Artifact Graph Engineering Domain

> Repository-owned index. Formal artifact authority comes from TOML metadata, typed relations, and lifecycle state—not this directory or index.

This package covers the first complete hosted context and draft-authoring sandbox. mmzen approved WO-HAG-001 with required commit-bound verification on 2026-10-04. mmzen subsequently approved all 16 governing definitions in the reviewed Phase 0 artifact package. This index grants no authority.

## Definitions and work

- [INT-HAG-001](intent/INT-HAG-001.md) and [CAP-HAG-001](capabilities/CAP-HAG-001.md): intended outcome and operator ability.
- [REQ-HAG-001](requirements/REQ-HAG-001.md) through [REQ-HAG-008](requirements/REQ-HAG-008.md): import fidelity, immutable baselines, context, draft authoring, atomic operations, reads, evaluator reuse and packaged qualification.
- [SPEC-HAG-001](specifications/SPEC-HAG-001.md): canonical representation, reference dataset, baselines and historical digests.
- [SPEC-HAG-002](specifications/SPEC-HAG-002.md): commands, validation, transactions, reads and Cypher.
- [SPEC-HAG-003](specifications/SPEC-HAG-003.md): development/release contract, Phase 0 completion rules HAG-OPS-007 through HAG-OPS-011, and the later Docker walkthrough.
- [ARCH-HAG-001](architecture/ARCH-HAG-001.md) and [ADR-HAG-001](architecture/adr/ADR-HAG-001.md): one Python service, one Memgraph store and the released evaluator adapter.
- [VER-HAG-001](verification/VER-HAG-001.md): independent acceptance and failure scenarios.
- [WO-HAG-001](work-orders/WO-HAG-001.md): complete first implementation outcome, scoped paths and required commit-bound verification.
- [RISK-HAG-001](risks/RISK-HAG-001.md): database-side read-only enforcement remains open while Cypher is retained in the sandbox.

The 16 definitions above are approved; WO-HAG-001 is in_progress. The risk is raised, not accepted or closed. Phases 3 and 4 require later work for authenticated human decisions, authority cutover, operational qualification and release/deployment. No release or operating claim is made by this package.

## Phase 0 observations

- [Contract preparation result](evidence/WO-HAG-001/phase0-contract-result.json): actual approval, start-preflight findings and the bounded Phase 0 result.
- [Docker and registry observations](evidence/WO-HAG-001/phase0-environment.json): available Linux engine and selected immutable image manifests; no application qualification claim.

## Package approval

- [Approval and current work state](evidence/WO-HAG-001/package-approval-result.json): recorded definition decisions by mmzen, start preflight, and current evaluator next step. Earlier Phase 0 observations retain their historical results.

## Phase 1 contract and feasibility

- [Protocol guide](../../notes/hosted-artifact-graph.md): concrete identities,
  selectors, hash rules and storage representation.
- [Phase 1 result](evidence/WO-HAG-001/phase1-contract.json): fixture checks,
  Git-blob bindings and remaining qualification.
- [Phase 1 continuation](evidence/WO-HAG-001/phase1-continuation.json): completed
  independent read/result contracts, explicit outcomes for all twelve scenarios,
  final schema/regression observations and the remaining Phase 2 admission dependency.
- [Evaluator observations](evidence/WO-HAG-001/phase1-evaluator-feasibility.json):
  successful reference projection and the reproduced standalone admission gap.
- [DEC-HAG-001](decisions/DEC-HAG-001.md): the existing `extend-evaluator` choice
  is now recorded by released 0.22.1 under actual human `mmzen`, with
  `engineering-owner` retained separately as the authority owner. WO-HAG-001
  remains in_progress. RISK-HAG-001 remains raised.

## Evaluator correction

mmzen accepted the `extend-evaluator` correction path in conversation. The
original 0.22.0 decision preview refused the actual identity with WEX201.
That historical recording defect is now resolved through released 0.22.1;
the previously selected answer has not changed.
The exact observation is retained in
[the decision attempt](evidence/WO-HAG-001/correction-decision-attempt.json).

mmzen approved the correction package for local implementation with required
commit-bound verification on 2026-10-04:
[REQ-HAG-009](requirements/REQ-HAG-009.md),
[SPEC-HAG-004](specifications/SPEC-HAG-004.md),
[VER-HAG-002](verification/VER-HAG-002.md), and
[WO-HAG-002](work-orders/WO-HAG-002.md).
It adds standalone draft validation and shared relationship checks to the
evaluator. WO-HAG-002 is implemented. The
[criterion assessment](evidence/WO-HAG-002/verification-results.json) records
the full-suite result, installed-wheel qualification, identical independent
package builds, retained failures and limitations.
[VREC-HAG-001](verification-records/VREC-HAG-001.md) is verified by mmzen and binds
candidate `169430fe25d28972a9b86fef2d00eccde2baa5db`. The recorded acceptance is
retained in [the verification result](evidence/WO-HAG-002/phase0-correction-verification-apply.json).
Release/adoption and resolution of the separate decision identity mismatch
remain outside this work order.

## Released evaluator reconciliation

[WO-HAG-005](work-orders/WO-HAG-005.md) integrates the approved main commit
`d7eeb2ae785928925669695074be7bdd6ccb1e0a` while preserving the HAG branch.
[DEC-HAG-002](decisions/DEC-HAG-002.md) records the explicit bounded manual
revision authority. SPEC-HAG-003 and VER-HAG-001 now select public evaluator
0.22.1; their prior complete bytes and lifecycle events are preserved.
Development source remains separately identified as 0.22.2, unpublished.

[VER-HAG-004](verification/VER-HAG-004.md) assesses only this reconciliation.
The [integration manifest](evidence/WO-HAG-005/integration-manifest.json) proves
134 earlier HAG files are unchanged and 180 transported paths match the
reviewed merge. VREC-HAG-001 and VREC-HAG-002 retain their exact candidates
and evidence. The full source suite passed (1,311 tests, 23 skips), as did
seven independent released draft-admission probes. Reconciliation verification
is pending; these observations do not verify the hosted service.

WO-HAG-001 still requires Phase 2 service implementation, all twelve hosted
scenarios, the walkthrough and restart/restore qualification. Zero hosted
scenarios have run. PR #535 stays draft and keeps its original target
`codex/hosted-artifact-graph-inputs`.
