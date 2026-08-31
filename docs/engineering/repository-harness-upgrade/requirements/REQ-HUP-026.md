+++
id = "REQ-HUP-026"
type = "requirement"
title = "Prove complete-graph operation under the 0.12.0 root"
status = "approved"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-08-31"
updated = "2026-08-31"
statement = "WHEN the standard root has moved to exact public 0.12.0, THE SYSTEM SHALL validate the complete governance graph with 0 errors and 0 advisories in the default count, pass doctor and released-root qualification, keep the repository suite at its measured baseline, derive a predecessor pair for the candidate, and pass its own pull request's managed lane through completion and the record heads."
verification_method = ["test"]
priority = "must"
source = "WO-HUP-011 evidence of what a root move touches; rehearsal of 2026-08-31 on a throwaway clone of main 63889f7"
measure = "0.12.0 validate 0 errors, 65 warnings, 0 advisories; doctor 0 FAIL; qualify released-root passed 113/113; suite failure set equal to the same-commit control on the 0.11.0 root beyond the identity-aware edits the evidence names; evaluator_facts derive yields the 0.12.0 to 0.13.0 pair; the managed lane green at the implemented head and at the record heads"
[relations]
derives_from = ["CAP-HUP-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-31T13:13:31Z"
decided_by = "repository-owner"
reason = "Approved on 2026-08-31 by the accountable owner by selecting the presented option 'Approve, start, complete on green' for WO-HUP-013: complete-graph operation under the 0.12.0 root, with the gate's own numbers moving to 0 errors, 65 warnings, 0 advisories over the same artifacts."
+++

# Requirement: Prove complete-graph operation under the 0.12.0 root

## Rationale

A root move is proven by what the new evaluator reads over the whole graph
and by the suite staying where it was, not by the transaction alone. The
0.12.0 gate's headline changes are visible in its own numbers: the
authoring advisories leave the warning count (`WO-AUT-004`) and the six
retired `W024` debt warnings are gone (`WO-LRE-002`), so the rehearsed
reading drops from 486 warnings under the 0.11.0 root to 65 warnings and 0
advisories under 0.12.0 — over the same artifacts, with 0 errors both
ways.

## Acceptance examples

**Given** the moved root, **when** exact 0.12.0 runs `validate`, `doctor`,
`qualify released-root`, `inspect`, `dashboard` twice and this work
order's review preflight, **then** every reading passes, the summary
carries four numbers with 0 advisories, and the dashboard content is
identical across the two runs.

**Given** the moved root with the candidate at 0.13.0, **when**
`repository_tools.evaluator_facts derive` runs, **then** it yields the
0.12.0 to 0.13.0 pair.

**Given** this work order's pull request, **when** its verification record
is pushed, **then** the managed lane is green at that head.
