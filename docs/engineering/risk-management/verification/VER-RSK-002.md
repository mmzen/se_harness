+++
id = "VER-RSK-002"
type = "verification"
title = "Independent evidence for closing the risk artifact's accepted deviations"
status = "approved"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
verifies = ["REQ-RSK-007"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T17:15:22Z"
decided_by = "assurance-owner"
+++

# Verification Contract: Independent evidence for closing the risk artifact's accepted deviations

## Requirement-to-evidence matrix

| Rule | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `RSK2-GRD-001` | guard tests | `raise-risk` with and without authority; operation name in the guard's audit | refused without authority; audit names `raise-risk` |
| `RSK2-DOC-001` | doctor tests | valid, absent, and invalid `[risk]` sections | `C-RSK-001` only for the invalid section; preflight `I001` mirrors it |
| `RSK2-SKL-001/002` | skill contract and helper entry-point tests | a new risk path inside the execute and draft helpers' own effect plans; a `risk-raise` effect class offered to each; all three contracts | the risk path is admitted under `implementation-write` and `draft-create` and reaches the evaluator; a `risk-raise` effect class is refused with `AEXEXE005` and `AEXDRF003` before the evaluator is called; no contract permits a `risk-raise` effect or any lifecycle transition; `harness-prepare-assurance` requires `risks` |
| `RSK2-SKL-003` | vector tests | regenerated manifests | `build_skill_manifest` digests equal the vectors; adapters unchanged |
| `RSK2-AMD-001..003` | validator and contract tests | existing `test_risk_management` scenarios | unchanged behaviour, now specified |

## Acceptance scenarios

1. Fresh install; `doctor` PASS; corrupt `[risk]`; `doctor` FAIL `C-RSK-001`.
2. The execute skill's change plan names a new risk path mid-procedure; the plan is admitted with no scope decision; the evaluator writes it and the receipt names it; handoff blocked by `QGP-G4I-RISK`.
3. Prepare-assurance packet for a work order with an accepted risk lists it.

## Pass criteria

All deterministic tests pass on Windows and Linux; released-evaluator validation 0 errors; handoff check completes.

## Amendment record

**The `RSK2-SKL-001/002` matrix row and acceptance scenario 2, amended
2026-08-27 by the engineering owner under `WO-RSK-003`, in the same act that
amended `SPEC-RSK-002` rules RSK2-SKL-001 and RSK2-SKL-003 and `REQ-RSK-007`'s
required response.** Both statements described a skill that raises a risk
itself. Under the schema-v3 closed contracts of the delegated execution model
the evaluator owns every governed-target write, and `_parse_v3_contract` refuses
the alternative: `SKC036` requires `client.target_writer` `"evaluator"` and
`SKC038` requires `effects.permitted` to equal the closed profile. There is no
`raise-risk` operation and no `risk-raise` effect class to exercise, so the
approved method named tests that cannot be written and a pass condition that
cannot be observed.

The amended row and scenario verify the route the write actually takes, and they
strengthen the obligation rather than relax it. Where the approved row asked for
"raise admitted for new risk files only", the amended row requires both
directions to be measured at the helpers' real entry points: that a risk path is
admitted under the existing effect classes and reaches the evaluator, and that a
`risk-raise` effect class is refused by identifier, `AEXEXE005` and `AEXDRF003`,
before the evaluator is called. It adds two checks the approved row did not
ask for: that no contract permits a `risk-raise` effect, and that no contract
permits any lifecycle transition. The amended scenario adds that the plan is
admitted with no scope decision, which is the substance of `REQ-RSK-007` that
the mechanism change had to preserve, and keeps the `QGP-G4I-RISK` handoff block
unchanged.

Every other statement in this contract stands verbatim. The `RSK2-GRD-001`,
`RSK2-DOC-001`, `RSK2-SKL-003` and `RSK2-AMD-001..003` matrix rows, acceptance
scenarios 1 and 3, and the pass criteria are unchanged; in particular the
`RSK2-SKL-003` row still verifies that the regenerated digests equal
`build_skill_manifest` and that the adapters are unchanged, which holds of
whichever fixture file carries them. No pass condition is weakened, no evidence
obligation is removed, and no refusal is downgraded.
