+++
id = "VER-RSK-001"
type = "verification"
title = "Independent evidence for the risk artifact"
status = "approved"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
verifies = ["REQ-RSK-001", "REQ-RSK-002", "REQ-RSK-003", "REQ-RSK-004", "REQ-RSK-005", "REQ-RSK-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T13:25:29Z"
decided_by = "assurance-owner"
+++

# Verification Contract: Independent evidence for the risk artifact

## Independence

Expected values derive from the six requirements and `SPEC-RSK-001`;
fixtures are written from the specification, not from candidate output.
Reviewers judge the disposition rationale and residual-risk wording in a
blinded corpus.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-RSK-001` artifact | validator tests | valid risk; score mismatch; stage/type mismatch; missing field; residual required when mitigated | exact error codes on the named planes; valid risk passes |
| `REQ-RSK-002` raising | `raise-risk` and validator tests | levels 1, 6, 25; unconfigured; score edit crossing the level | status computed correctly; event `decided_by = "harnessctl"`; level copied; stale status is a governance error |
| `REQ-RSK-003` disposition | transition tests | every permitted and forbidden edge; wrong-role actor; missing reason; missing relation; `mitigated` without verified coverage; residual above level without "accepted" | refusals before write; permitted transitions change only the risk |
| `REQ-RSK-004` gates | check/transition/prepare tests | raised at each stage; mitigating at G4 vs G5; empty register; malformed risk | correct predicate outcome per gate; corrective escalation rendered; empty register passes |
| `REQ-RSK-005` traceability | validator and prepare-release tests | relation pairs; `lists_risks` derivation; mitigating blocks preparation | pairs accepted or rejected per table; record lists exactly the qualifying risks |
| `REQ-RSK-006` identification | scope and procedure tests | raise from a narrow-scope WO; disposed risk path in changed set; every stage procedure resolves a `RISKS` step; skills' contracts | exception admits only undisposed risk files; steps present; no skill disposes |

## Acceptance scenarios

1. Fresh install: no `[risk]` section, no risks; every gate passes as before.
2. Agent raises a risk mid-implementation; handoff blocked by `QGP-G4I-RISK`;
   engineering owner disposes `mitigating`; handoff passes; release
   preparation refuses; mitigation WO verified; risk `mitigated` with
   residual; release prepared listing it.
3. Below-level risk stays `identified`, never blocks, appears in `inspect`,
   is accepted by the stage owner at a later decision.
4. Wrong-role and missing-reason transitions refused with the accountable
   role named.
5. Level lowered in policy after a risk was raised: the risk keeps its copied
   level and status.
6. Blinded review of five disposition rationales: reviewers identify the
   disposer role and the residual correctly.

## Pass criteria

All deterministic tests pass on Windows and Linux; Scenario 6 has zero
misclassifications; released-evaluator validation reports 0 errors; the
handoff check completes.
