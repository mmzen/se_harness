+++
id = "VER-HUP-008"
type = "verification"
title = "Verify standard-root adoption of exact public 0.8.0"
status = "draft"
owners = ["assurance-owner", "security-owner"]
created = "2026-08-28"
updated = "2026-08-28"
[relations]
verifies = ["REQ-HUP-016", "REQ-HUP-017"]
+++

# Verification: Verify standard-root adoption of exact public 0.8.0

## Method

Automated tests and command readings, all retained in the work order's
evidence with the evaluator that produced each.

| Requirement | Method | Pass condition |
| --- | --- | --- |
| `REQ-HUP-016` | wheel-file SHA-256 before install; `upgrade .`, `upgrade . --apply --evidence-output …`, `upgrade .` replay from the isolated 0.8.0 environment | wheel digest equals `RLS-SEH-017`'s bound wheel; plan inside the managed set with no `customized` or `conflict`; apply succeeds without a packet; lock schema 3 names 0.8.0 by version, payload and the same archive pair; replay reads every file unchanged; the evidence document is retained |
| `REQ-HUP-017` | exact 0.8.0 `validate`, `doctor`, `qualify released-root`, `inspect`, `dashboard` twice, review preflight; `evaluator_facts derive`; `run_tests.py --scale full`; the pull request's lanes | 0 errors, 0 FAIL, released-root passed, dashboard content identical, preflight PASS; derive yields 0.8.0 to 0.9.0 with an empty acceptance digest; suite OK; every lane success including the governor-transition assessment of the real transition |

## Independence

The readings under the 0.8.0 root are produced by the released evaluator
outside the checkout, not by candidate source; the suite runs candidate
source against the moved root. The assurance decision on the verification
record is the assurance owner's and is not part of this contract.

## Evidence

`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-008-verification.md`
and `WO-HUP-008-evaluator-upgrade.json`.
