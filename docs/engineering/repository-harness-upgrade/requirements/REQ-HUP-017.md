+++
id = "REQ-HUP-017"
type = "requirement"
title = "Prove complete-graph operation under the 0.8.0 root"
status = "draft"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-08-28"
updated = "2026-08-28"
statement = "WHEN the standard root has moved to exact public 0.8.0, THE SYSTEM SHALL validate the complete governance graph with 0 errors, pass doctor and released-root qualification, keep every repository suite green, and derive a predecessor pair for the candidate."
verification_method = ["test"]
priority = "must"
source = "REL-SEH-019 post-release observation window; WO-HUP-007 evidence of what a root move touches; rehearsal of 2026-08-28 on a throwaway export of main 2628627"
measure = "0.8.0 validate 0 errors; doctor 0 FAIL; qualify released-root passed; suites OK; evaluator_facts derive yields the 0.8.0 to 0.9.0 pair with no legacy acceptance digest"
[relations]
derives_from = ["CAP-HUP-002"]
+++

# Requirement: Prove complete-graph operation under the 0.8.0 root

## Statement

WHEN the standard root has moved to exact public 0.8.0, THE SYSTEM SHALL
validate the complete governance graph with 0 errors, pass `doctor` and
released-root qualification, keep every repository suite green, and derive a
predecessor pair for the candidate.

## Rationale

A root move changes the evaluator every gate runs under and the managed
copies the tests pin. This move has two effects `WO-HUP-007` did not have.
First, the root copies and the candidate templates become byte-identical
(0.8.0 is the candidate that was released), so every test that declared the
released-0.7.1-versus-candidate divergence — the validator's retired names,
the quality-gates transition binding index, the `.gitattributes` migration
rules in the managed block — must read the root identity instead of assuming
the divergence. Second, 0.8.0 carries the `qualify` namespace, so no legacy
`accept-candidate` contract digest exists for it and `evaluator_facts derive`
yields none; the candidate-package job takes the typed branch. With root and
candidate both at `0.8.0`, `derive` raises `PRE008` (measured 2026-08-28), so
the candidate moves to `0.9.0` in the same change; since `WO-ECP-010` no
scenario accompanies a bump.

## Acceptance

- Exact 0.8.0 outside the checkout: `validate .` 0 errors; `doctor .` 0 FAIL;
  `qualify released-root` passed with the archive pair recorded.
- `python scripts/run_tests.py --scale full` OK; the tests that pinned the
  0.7.1 root or the 0.8.0 candidate assert the released-root identity and
  the package version instead, each named in the evidence with the
  assumption it carried.
- `evaluator_facts derive` yields version 0.8.0, wheel
  `se_harness-0.8.0-py3-none-any.whl` with its digest from the lock,
  candidate 0.9.0 and an empty acceptance-contract digest.
