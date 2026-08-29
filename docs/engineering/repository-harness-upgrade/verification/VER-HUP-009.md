+++
id = "VER-HUP-009"
type = "verification"
title = "Verify standard-root adoption of exact public 0.9.0"
status = "approved"
owners = ["assurance-owner", "security-owner"]
created = "2026-08-29"
updated = "2026-08-29"
[relations]
verifies = ["REQ-HUP-018", "REQ-HUP-019"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T06:37:01Z"
decided_by = "assurance-owner"
reason = "Approved on 2026-08-29 by the accountable owner, 'i approve the artifact packet', for the adoption of exact public 0.9.0 (RLS-SEH-018, released and published 2026-08-28) as the standard root the simple way: one command from an isolated wheel-file install outside the checkout whose digest equals the record's bound wheel, no packet, candidate moved to 0.10.0 in the same change. Measured before this transition over branch state 7b6f3e1 carrying unmoved main 7291602: validate PASS at 0 errors under the governing 0.8.0 root and under public 0.9.0; rehearsal on a throwaway clone: plan 61 files, 5 update, 56 unchanged, no customization or conflict; 0.9.0 doctor 0 FAIL and released-root 143/143 after apply; the full suite on the moved root differs from the same-commit control by four tests, all resolved by owner content, the candidate version and two test edits."
+++

# Verification: Verify standard-root adoption of exact public 0.9.0

## Method

Automated tests and command readings, all retained in the work order's
evidence with the evaluator that produced each.

| Requirement | Method | Pass condition |
| --- | --- | --- |
| `REQ-HUP-018` | wheel-file SHA-256 before install; `upgrade .`, `upgrade . --apply --evidence-output …`, `upgrade .` replay from the isolated 0.9.0 environment | wheel digest equals `RLS-SEH-018`'s bound wheel; plan inside the managed set with no `customized` or `conflict`; apply succeeds without a packet; lock schema 3 names 0.9.0 by version, payload and the same archive pair; replay reads every file unchanged; the evidence document is retained |
| `REQ-HUP-019` | exact 0.9.0 `validate`, `doctor`, `qualify released-root`, `inspect`, `dashboard` twice, review preflight; `evaluator_facts derive`; `run_tests.py --scale full` on the moved root and on a same-commit control; the pull request's lanes | 0 errors, 0 FAIL, released-root passed, dashboard content identical, preflight PASS; derive yields 0.9.0 to 0.10.0 with an empty acceptance digest; the moved root's failing-test set equals the control's; every lane success including the governor-transition assessment of the real transition |

## Independence

The readings under the 0.9.0 root are produced by the released evaluator
outside the checkout, not by candidate source; the suite runs candidate
source against the moved root. The assurance decision on the verification
record is the assurance owner's and is not part of this contract.

## Evidence

`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-009-verification.md`
and `WO-HUP-009-evaluator-upgrade.json`.
