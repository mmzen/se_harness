+++
id = "REQ-HUP-015"
type = "requirement"
title = "Prove complete-graph operation under the 0.7.1 root"
status = "draft"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-08-27"
updated = "2026-08-27"
statement = "WHEN the standard root has moved to exact public 0.7.1, THE SYSTEM SHALL validate the complete governance graph with 0 errors, pass doctor and released-root qualification, keep every repository suite green, and derive a predecessor pair for the candidate."
verification_method = "automated-test"
priority = "must"
source = "REL-SEH-018 post-release observation window; WO-HUP-006 evidence of what a root move touches"
measure = "0.7.1 validate 0 errors; doctor 0 FAIL; qualify released-root passed; suites OK on CPython 3.14 and 3.11; predecessor_facts derive yields the 0.7.1 to 0.8.0 pair"
[relations]
derives_from = ["CAP-HUP-002"]
+++

# Requirement: Prove complete-graph operation under the 0.7.1 root

## Statement

WHEN the standard root has moved to exact public 0.7.1, THE SYSTEM SHALL
validate the complete governance graph with 0 errors, pass `doctor` and
released-root qualification, keep every repository suite green, and derive a
predecessor pair for the candidate.

## Rationale

A root move changes the evaluator every gate runs under and the managed
copies the tests pin. With root and candidate both at 0.7.1,
`predecessor_facts derive` raises `PRE008` (no predecessor pair) and every
pull request's candidate-evidence lane goes red, so the candidate must move to
the next development version with its scenario in the same change
(measured under `WO-HUP-006`).

## Acceptance

- Exact 0.7.1 outside the checkout: `validate .` 0 errors; `doctor .` 0 FAIL;
  `qualify released-root` passed with a `null` archive pair.
- `python scripts/run_tests.py --scale full` OK on CPython 3.14 and 3.11; the
  tests that pinned 0.6.0 root assumptions assert the released-root identity
  instead, each named in the evidence.
- `predecessor_facts derive` yields version 0.7.1, candidate 0.8.0 and the
  scenario `candidate-0.7.1-to-0.8.0.json` written by the canonical writer.
