+++
id = "VER-HUP-007"
type = "verification"
title = "Verify standard-root adoption of exact public 0.7.1"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-27"
updated = "2026-08-27"
[relations]
verifies = ["REQ-HUP-014", "REQ-HUP-015"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-27T17:43:24Z"
decided_by = "quality-owner"
reason = "Approved on 2026-08-27 by the accountable owner, 'Approve and start', for the adoption of exact public 0.7.1 as the standard root the simple way (REQ-REB-027, REQ-REB-028 shipped by RLS-SEH-016): one command from an isolated index install outside the checkout, no packet, candidate moved to 0.8.0 with its scenario in the same change. Successor to the rejected WO-HUP-006. Measured before this transition over branch state 12e9e36 carrying unmoved main 23d5781: validate PASS at 986 artifacts, 0 errors under both the governing 0.6.0 root and public 0.7.1; doctor 0 FAIL; upgrade plan 61 files, 43 add or update, 18 unchanged."
+++

# Verification: Verify standard-root adoption of exact public 0.7.1

## Method

Automated tests and command readings, all retained in the work order's
evidence with the evaluator that produced each.

| Requirement | Method | Pass condition |
| --- | --- | --- |
| `REQ-HUP-014` | `identity`, `upgrade .`, `upgrade . --apply --evidence-output …`, `upgrade .` replay from the isolated 0.7.1 environment | identity by version and payload, archive pair `null`; plan inside the managed set with no `customized` or `conflict`; apply succeeds without a packet; lock schema 3 names 0.7.1; replay reads every file unchanged; the evidence document is retained |
| `REQ-HUP-015` | exact 0.7.1 `validate`, `doctor`, `qualify released-root`, `inspect`, `dashboard` twice, review preflight; `predecessor_facts derive`; `run_tests.py --scale full` on CPython 3.14 and 3.11; the pull request's lanes | 0 errors, 0 FAIL, released-root passed, deterministic dashboard, preflight PASS; derive yields 0.7.1 to 0.8.0; suites OK; every lane success with the candidate-package job on the typed branch |

## Independence

The readings under the 0.7.1 root are produced by the released evaluator
outside the checkout, not by candidate source; the suites run candidate
source against the moved root. The assurance decision on the verification
record is the assurance owner's and is not part of this contract.

## Evidence

`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-007-verification.md`
and `WO-HUP-007-evaluator-upgrade.json`.
