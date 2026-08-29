+++
id = "VER-HUP-011"
type = "verification"
title = "Verify standard-root adoption of exact public 0.11.0"
status = "draft"
owners = ["assurance-owner", "security-owner"]
created = "2026-08-29"
updated = "2026-08-29"
[relations]
verifies = ["REQ-HUP-022", "REQ-HUP-023"]
+++

# Verification: Verify standard-root adoption of exact public 0.11.0

## Method

Automated tests and command readings, all retained in the work order's
evidence with the evaluator that produced each.

| Requirement | Method | Pass condition |
| --- | --- | --- |
| `REQ-HUP-022` | wheel-file SHA-256 before install; `upgrade .`, `upgrade . --apply --evidence-output ...`, `upgrade .` replay from the isolated 0.11.0 environment; the tree listed after the explicit removal | wheel digest equals `RLS-SEH-020`'s; plan 46 files with 9 `update` and no `customized`/`conflict`; lock `tool_version 0.11.0`, `archive_sha256` equal to the wheel, payload recorded; replay 46 unchanged; `.agents/skills` holds exactly `harness-operator-brief` and `harness-orient`, `.claude/skills` exactly `harness-orient` |
| `REQ-HUP-023` | exact 0.11.0 `validate`, `doctor`, `qualify released-root`, `inspect`, `dashboard` twice, review preflight; `evaluator_facts derive`; `run_tests.py --scale full` on the moved root and on a same-commit control; the pull request's lanes at the implemented head and at the record head | validate 0 errors; doctor 0 FAIL; released-root PASS; dashboard content identical; derive yields 0.11.0 to 0.12.0 with no legacy digest; suite failure set equal to the control's; managed lane green at both heads with no `verification-records/` in scope |

## Independence

The readings under the 0.11.0 root are produced by the released evaluator
outside the checkout, not by candidate source; the suite runs candidate
source against the moved root. The assurance decision on the verification
record is the assurance owner's and is not part of this contract.

## Evidence

`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-011/` (the
keyed packet the root writes) and `WO-HUP-011-evaluator-upgrade.json`.
