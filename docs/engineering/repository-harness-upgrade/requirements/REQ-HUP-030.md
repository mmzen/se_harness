+++
id = "REQ-HUP-030"
type = "requirement"
title = "Prove complete-graph operation under the 0.14.0 root"
status = "approved"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-09-02"
updated = "2026-09-02"
statement = "WHEN the standard root has moved to exact public 0.14.0, THE SYSTEM SHALL pass validate with 0 errors and 0 advisories, doctor, released-root qualification, two identical Explorer generations, the suite at its baseline, the candidate derivation, and its own managed lane."
verification_method = ["test"]
priority = "must"
source = "WO-HUP-014 evidence of what a root move touches; rehearsal of 2026-09-02 on a throwaway clone of main 25c0ef9"
measure = "0.14.0 validate 0 errors, 69 warnings, 0 advisories over main 25c0ef9; doctor 0 FAIL; qualify released-root passed; dashboard content digest identical across two runs; suite failure set equal to the same-commit control on the 0.13.0 root beyond the identity-aware edits the evidence names; evaluator_facts derive yields the 0.14.0 to 0.15.0 pair; the managed lane green at the implemented head and at the record heads"

[relations]
derives_from = ["CAP-HUP-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-02T11:42:30Z"
decided_by = "repository-owner"
reason = "Approved on 2026-09-02 by the accountable owner by selecting the presented option 'Approve, start, complete on green, prepare and verify the VREC' for WO-HUP-015: the adoption of exact public 0.14.0 (RLS-SEH-023, released and published 2026-09-02) as the standard root the simple way, from the 0.13.0 lock 9dfec5b4, rehearsed the same day on a throwaway clone of main 25c0ef9. Complete-graph operation under the 0.14.0 root with every number unchanged."
+++

# Requirement: Prove complete-graph operation under the 0.14.0 root

## Rationale

A root move is proven by what the new evaluator reads over the whole graph
and by the suite staying where it was. The 0.14.0 evaluator behaves as
0.13.0 does, so every number is expected unchanged: 0 errors, 69 warnings,
0 advisories over the same artifacts, the same designed Explorer generated
identically twice.

## Behavior

- Trigger: the moved root.
- Response: exact 0.14.0 `validate`, `doctor`, `qualify released-root`,
  `inspect`, `dashboard` twice and the work order's review preflight all
  pass; `evaluator_facts derive` yields the 0.14.0 to 0.15.0 pair; the
  suite's failure set equals the control's beyond the edits the evidence
  names.
- On failure: the work order stops; the branch is amended or abandoned
  under the owner's decision.

## Assumptions and dependencies

The candidate version has moved to 0.15.0, without which the derivation
reports `PRE008`, as the rehearsal measured.

## Acceptance examples

### Example: normal behavior

**Given** the moved root,

**When** exact 0.14.0 runs `validate`, `doctor`, `qualify released-root`,
`inspect`, `dashboard` twice and this work order's review preflight,

**Then** every reading passes and the dashboard content digest is identical
across the two runs.

### Example: failure behavior

**Given** the moved root with the candidate still at 0.14.0,

**When** `repository_tools.evaluator_facts derive` runs,

**Then** it fails closed with `PRE008`, and the work order moves the
candidate to 0.15.0 before continuing.
