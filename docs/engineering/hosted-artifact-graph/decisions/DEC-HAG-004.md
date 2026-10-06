+++
id = "DEC-HAG-004"
type = "decision"
title = "Phase 3 pilot authority while authentication and database ACLs are deferred"
status = "open"
owners = ["mmzen"]
created = "2026-10-06"
updated = "2026-10-06"
kind = "question"
question = "Should Phase 3 exercise the engineering lifecycle on a test copy while Git remains authoritative, or make the graph authoritative for a real pilot project while authentication and database ACL work are deferred?"
raised_by = "Codex"
recommendation = "test-copy"

[[options]]
id = "test-copy"
label = "Implement and exercise the lifecycle on a private test copy; Git remains authoritative for real engineering decisions."

[[options]]
id = "authoritative-pilot"
label = "Propose a bounded real pilot using graph authority, with explicit treatment of the deferred controls and the accepted cutover prerequisites."

[relations]
concerns = ["SPEC-HAG-003"]
blocks = ["SPEC-HAG-003"]
+++

# Phase 3 pilot authority

## Confirmed direction

Phase 2 is verified and integrated into main through PR #541, commit
`5fa2d41cd701248605a22cb15d393d6b620f31ed`. The requester has asked to define
Phase 3, put authentication and graph database ACL work aside for now, and
publish the proposed artifacts early in a branch and PR.

This request authorizes proposal preparation and review publication. The new
implementation, verification acceptance, merge, release and deployment remain
separate actions. No accepted Phase 2 artifact or evidence is changed here.

## Question

The original Phase 3 roadmap combines functional lifecycle support with a
change of artifact authority. Deferring authentication and database ACL work
leaves two materially different outcomes to choose from.

`SPEC-HAG-003#HAG-OPS-006` requires authenticated decision enforcement and a
resolved database query boundary before the planned authority cutover.
`RISK-HAG-001` remains raised. Putting those implementation topics aside does
not by itself amend that accepted rule or accept the risk.

## Options

### Test copy

Develop the missing lifecycle operations, verification/release record handling,
and export behavior against one private, non-sensitive project copy. Compare
results with the selected released evaluator. Record supplied test actor labels
as test inputs, not authenticated identities or real human decisions. Keep Git
as the authority for real engineering work. Do not implement authentication,
database ACLs, public exposure or an authority switch in this package.

This allows functional work to proceed while the deferred controls remain a
separate prerequisite for later authoritative use.

### Authoritative pilot

Define a real non-production project whose engineering records would become
authoritative in the graph. Before approving that switch, specify its users,
operating boundary, accountable decision path, recovery/export conditions, and
the exact accepted-contract changes and risk decisions needed with the controls
deferred. Caller-supplied names alone do not prove a human decision.

This option requires further decisions and a reviewed linked revision of the
existing cutover contract. It does not silently waive the current prerequisites.

## Recommendation

Choose the test-copy outcome for this package. It delivers the functional
lifecycle path without mixing it with an unresolved authority switch. The
service remains one synchronous Python process, one Memgraph store and one
released evaluator; no new identity platform, workflow engine or release system
is proposed.

## Effect on the proposal

Keep this question open until the requester chooses. The initial link blocks a
transition of the existing cutover contract while its proposed treatment is
unresolved; it does not change that contract's accepted content or state. Reassess
the links when the new Phase 3 artifacts exist. RISK-HAG-001 is a contextual
reference, not a paired risk decision. Do not insert a disposition manually.
The selected option will determine the new intent, requirements, verification
contract and work-order boundaries. Draft preparation supplies no implementation
approval. Authentication and database ACL implementation remain excluded under
either proposal unless the requester later changes that direction.
