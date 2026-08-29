+++
id = "REQ-HUP-019"
type = "requirement"
title = "Prove complete-graph operation under the 0.9.0 root"
status = "draft"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-08-29"
updated = "2026-08-29"
statement = "WHEN the standard root has moved to exact public 0.9.0, THE SYSTEM SHALL validate the complete governance graph with 0 errors, pass doctor and released-root qualification, keep the repository suite at its measured baseline, and derive a predecessor pair for the candidate."
verification_method = ["test"]
priority = "must"
source = "WO-HUP-008 evidence of what a root move touches; rehearsal of 2026-08-29 on a throwaway clone of main 7291602"
measure = "0.9.0 validate 0 errors; doctor 0 FAIL; qualify released-root passed; suite failure set equal to the same-commit control on the 0.8.0 root; evaluator_facts derive yields the 0.9.0 to 0.10.0 pair with no legacy acceptance digest"
[relations]
derives_from = ["CAP-HUP-002"]
+++

# Requirement: Prove complete-graph operation under the 0.9.0 root

## Statement

WHEN the standard root has moved to exact public 0.9.0, THE SYSTEM SHALL
validate the complete governance graph with 0 errors, pass `doctor` and
released-root qualification, keep the repository suite at its measured
baseline, and derive a predecessor pair for the candidate.

## Rationale

A root move changes the evaluator every gate runs under and the managed
copies the tests pin. Since `WO-HUP-008` the tests read the lock's evaluator
version instead of pinning a root, so this move surfaces fewer assumptions
than the last: the rehearsal on a throwaway clone of `main` at `7291602`
compared the full suite on the moved root against a control on the unmoved
root at the same commit and found exactly four tests that move, all
resolved by owner content and the candidate version. Three
`PredecessorDerivationTests` fail because `evaluator_facts derive` raises
`PRE008` when the candidate version equals the root version, so the
candidate moves to `0.10.0` in the same change; since `WO-ECP-010` no
scenario accompanies a bump. The fourth, the owner-region test, requires
`AGENTS.md` to direct the evaluator at the lock's version. The baseline
itself is the workstation's: the control reads 65 failing tests in
`test_workflow_compliance`, `test_workflow_execution`,
`test_delegated_workflow`, `test_artifact_authoring` and the owner-region
size bound, none touched by the root and all passing hosted; the pass
condition is therefore equality of the failure set with the control, and
the hosted lanes.

## Acceptance

- Exact 0.9.0 outside the checkout: `validate .` 0 errors; `doctor .` 0 FAIL;
  `qualify released-root` passed with the archive pair recorded.
- `python scripts/run_tests.py --scale full` on the moved root: the set of
  failing test names equals the control's on the unmoved root at the same
  commit, each divergence during the rehearsal named in the evidence with
  the assumption it carried; every pull-request lane passes hosted.
- `evaluator_facts derive` yields version 0.9.0, wheel
  `se_harness-0.9.0-py3-none-any.whl` with its digest from the lock,
  candidate 0.10.0 and an empty acceptance-contract digest.
