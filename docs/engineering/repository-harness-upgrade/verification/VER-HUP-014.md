+++
id = "VER-HUP-014"
type = "verification"
title = "Verify standard-root adoption of exact public 0.13.0"
status = "approved"
owners = ["assurance-owner", "security-owner"]
created = "2026-09-02"
updated = "2026-09-02"

[relations]
verifies = ["REQ-HUP-027", "REQ-HUP-028"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-02T08:31:12Z"
decided_by = "assurance-owner"
reason = "Approved on 2026-09-02 by the accountable owner by selecting the presented option 'Approve, start, complete on green' for WO-HUP-014: the adoption of exact public 0.13.0 (RLS-SEH-022, released and published 2026-09-02) as the standard root the simple way, from the 0.12.0 lock 4d8f9d37, rehearsed the same day on a throwaway clone of main 09aa69f. The transaction and complete-graph rows with the rehearsal-measured pass conditions."
+++

# Verification: Verify standard-root adoption of exact public 0.13.0

## Method

Automated tests and command readings, all retained in the work order's
evidence with the evaluator that produced each.

| Requirement | Method | Pass condition |
| --- | --- | --- |
| `REQ-HUP-027` | wheel-file SHA-256 before install; `upgrade .`, `upgrade . --apply --evidence-output ...`, `upgrade .` replay from the isolated 0.13.0 environment | wheel digest equals `RLS-SEH-022`'s; plan 46 files with 5 `update` and no `customized`/`conflict`/`remove`; lock `tool_version 0.13.0`, `archive_sha256` equal to the wheel, payload recorded; replay 46 unchanged |
| `REQ-HUP-028` | exact 0.13.0 `validate`, `doctor`, `qualify released-root`, `inspect`, `dashboard` twice, review preflight; `evaluator_facts derive`; `run_tests.py --scale full` on the moved root and on a same-commit control | validate 0 errors, 0 advisories; doctor 0 FAIL; released-root PASS 113/113; dashboard content digest identical across two runs and no remote origin in the page; derive yields 0.13.0 to 0.14.0; suite failure set equal to the control's beyond the identity-aware edits the evidence names; managed lane green at the implemented head and at the record heads |

## Independence

The readings under the 0.13.0 root are produced by the released evaluator
outside the checkout, not by candidate source; the suite runs candidate
source against the moved root. The assurance decision on the verification
record is the assurance owner's and is not part of this contract.

## Evidence

`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-014/` (the
keyed packet the root writes) and `WO-HUP-014-evaluator-upgrade.json`.
