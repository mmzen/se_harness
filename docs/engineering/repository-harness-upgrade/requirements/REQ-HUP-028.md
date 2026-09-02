+++
id = "REQ-HUP-028"
type = "requirement"
title = "Prove complete-graph operation under the 0.13.0 root"
status = "draft"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-09-02"
updated = "2026-09-02"
statement = "WHEN the standard root has moved to exact public 0.13.0, THE SYSTEM SHALL pass validate with 0 errors and 0 advisories, doctor, released-root qualification, two identical Explorer generations, the suite at its baseline, the candidate derivation, and its own managed lane."
verification_method = ["test"]
priority = "must"
source = "WO-HUP-013 evidence of what a root move touches; rehearsal of 2026-09-02 on a throwaway clone of main 09aa69f"
measure = "0.13.0 validate 0 errors, 67 warnings, 0 advisories over main 09aa69f; doctor 0 FAIL; qualify released-root passed 113/113; dashboard content digest identical across two runs with no remote origin in the page; suite failure set equal to the same-commit control on the 0.12.0 root beyond the identity-aware edits the evidence names; evaluator_facts derive yields the 0.13.0 to 0.14.0 pair; the managed lane green at the implemented head and at the record heads"

[relations]
derives_from = ["CAP-HUP-002"]
+++

# Requirement: Prove complete-graph operation under the 0.13.0 root

## Rationale

A root move is proven by what the new evaluator reads over the whole graph
and by the suite staying where it was, not by the transaction alone. The
0.13.0 root's visible change is its own generated Explorer: the designed
self-contained page, 431,388 bytes at the rehearsal with no remote origin,
in place of the 0.12.0 page that loaded its graph library from a CDN. The
gate's numbers do not move: 0 errors, 67 warnings, 0 advisories over the
same artifacts under both roots.

## Behavior

- Trigger: the moved root.
- Response: exact 0.13.0 `validate`, `doctor`, `qualify released-root`,
  `inspect`, `dashboard` twice and the work order's review preflight all
  pass; the dashboard content is identical across the two runs and names
  no remote origin; `evaluator_facts derive` yields the 0.13.0 to 0.14.0
  pair; the suite's failure set equals the control's beyond the edits the
  evidence names.
- On failure: the work order stops; the branch is amended or abandoned
  under the owner's decision.

## Assumptions and dependencies

The candidate version has moved to 0.14.0, without which the derivation
reports `PRE008` (root and candidate equal), as the rehearsal measured.

## Acceptance examples

### Example: normal behavior

**Given** the moved root,

**When** exact 0.13.0 runs `validate`, `doctor`, `qualify released-root`,
`inspect`, `dashboard` twice and this work order's review preflight,

**Then** every reading passes, the summary carries four numbers with 0
advisories, and the dashboard content digest is identical across the two
runs.

### Example: failure behavior

**Given** the moved root with the candidate still at 0.13.0,

**When** `repository_tools.evaluator_facts derive` runs,

**Then** it fails closed with `PRE008`, and the work order moves the
candidate to 0.14.0 before continuing.
