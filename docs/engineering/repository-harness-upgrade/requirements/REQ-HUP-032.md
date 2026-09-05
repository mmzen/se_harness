+++
id = "REQ-HUP-032"
type = "requirement"
title = "Prove complete-graph operation under the 0.15.0 root"
status = "draft"
owners = ["repository-owner", "engineering-owner"]
created = "2026-09-05"
updated = "2026-09-05"
statement = "WHEN the standard root has moved to exact public 0.15.0, THE SYSTEM SHALL pass validate with 0 errors and 0 advisories, doctor, released-root qualification, two identical Explorer generations, the suite at its baseline, the candidate derivation, and its own managed lane."
verification_method = ["test", "inspection"]
priority = "must"
source = "REQ-HUP-030's proof pattern for the previous adoption; the rehearsal of 2026-09-05 on the moved root"

[relations]
derives_from = ["CAP-HUP-002"]
+++

# Requirement: Prove complete-graph operation under the 0.15.0 root

## In plain words

A root move is proven by what the new evaluator reads over the whole
graph and by the test suite staying where it was. This time the evaluator
does change behaviour, so the readings are re-measured rather than
expected unchanged.

## Why

0.15.0 reads this graph with new rules: the decision family, the
per-type authoring advisories on drafts, the glossary seed. The rehearsal
read 0 errors, 71 warnings and 0 advisories over 1,310 artifacts, 116
managed checks, a passing released-root qualification and an identical
Explorer twice. The candidate must move to 0.16.0, or the derivation
reports `PRE008`.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| The moved root | Exact 0.15.0 `validate`, `doctor`, `qualify released-root`, `inspect`, `dashboard` twice and the work order's review preflight pass; `evaluator_facts derive` yields the 0.15.0 to 0.16.0 pair; the suite's failure set equals the control's beyond the edits the evidence names | The work order stops; the branch is amended or abandoned under the owner's decision |

## Examples

### Normal

**Given** the moved root with the candidate at 0.16.0,

**When** exact 0.15.0 runs the readings above,

**Then** every reading passes and the Explorer's resource digests are
identical across the two runs.

### Failure

**Given** the moved root with the candidate still at 0.15.0,

**When** `repository_tools.evaluator_facts derive` runs,

**Then** it fails closed with `PRE008`, and the work order moves the
candidate to 0.16.0 before continuing.

## Open decisions

None.
