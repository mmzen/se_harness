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
| `RSK2-SKL-001/002` | skill contract, trigger, and sentinel tests | raise inside the execute skill; attempted dispose; prepare-assurance packet | raise admitted for new risk files only; dispose stopped; packet carries the register |
| `RSK2-SKL-003` | vector tests | regenerated manifests | `build_skill_manifest` digests equal the vectors; adapters unchanged |
| `RSK2-AMD-001..003` | validator and contract tests | existing `test_risk_management` scenarios | unchanged behaviour, now specified |

## Acceptance scenarios

1. Fresh install; `doctor` PASS; corrupt `[risk]`; `doctor` FAIL `C-RSK-001`.
2. Execute skill raises a risk mid-procedure; receipt names it; handoff blocked by `QGP-G4I-RISK`.
3. Prepare-assurance packet for a work order with an accepted risk lists it.

## Pass criteria

All deterministic tests pass on Windows and Linux; released-evaluator validation 0 errors; handoff check completes.
