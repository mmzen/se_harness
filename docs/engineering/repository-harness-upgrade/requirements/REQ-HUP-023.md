+++
id = "REQ-HUP-023"
type = "requirement"
title = "Prove complete-graph operation under the 0.11.0 root"
status = "draft"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-08-29"
updated = "2026-08-29"
statement = "WHEN the standard root has moved to exact public 0.11.0, THE SYSTEM SHALL validate the complete governance graph with 0 errors, pass doctor and released-root qualification, keep the repository suite at its measured baseline, derive a predecessor pair for the candidate, and pass its own pull request's managed lane through completion and the record heads without a scoped records directory."
verification_method = ["test"]
priority = "must"
source = "WO-HUP-010 evidence of what a root move touches; rehearsal of 2026-08-29 on a throwaway clone of main 896f8fa; VER-ECP-012's hosted demonstration"
measure = "0.11.0 validate 0 errors; doctor 0 FAIL; qualify released-root passed; suite failure set equal to the same-commit control on the 0.10.0 root; evaluator_facts derive yields the 0.11.0 to 0.12.0 pair with no legacy acceptance digest; the managed lane green at the implemented head and at the verification-record head with the work order's scope naming no verification-records directory"
[relations]
derives_from = ["CAP-HUP-002"]
+++

# Requirement: Prove complete-graph operation under the 0.11.0 root

## Rationale

A root move is proven by what the new evaluator reads over the whole
graph and by the suite staying where it was, not by the transaction alone.
This adoption also closes the interim rule every packet since 0.10.0
carried — listing `verification-records/` so the released gate would admit
the work order's own record — because the 0.11.0 gate admits it by
construction (`WO-ECP-016`, `ECP-ADM-001`); this work order's own scope
therefore names no records directory, and its record head is
`VER-ECP-012`'s hosted demonstration.

## Acceptance examples

**Given** the moved root, **when** exact 0.11.0 runs `validate`, `doctor`,
`qualify released-root`, `inspect`, `dashboard` twice and this work
order's review preflight, **then** every reading passes and the dashboard
content is identical across the two runs.

**Given** the moved root with the candidate at 0.12.0, **when**
`repository_tools.evaluator_facts derive` runs, **then** it yields the
0.11.0 to 0.12.0 pair and no legacy acceptance digest.

**Given** this work order's pull request, **when** its verification record
is pushed, **then** the managed lane is green with the scope naming no
`verification-records/` directory.
