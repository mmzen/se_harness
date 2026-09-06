+++
id = "REQ-TCM-016"
type = "requirement"
title = "A deviation names a rule that exists"
status = "approved"
owners = ["product-owner", "quality-owner"]
created = "2026-09-06"
updated = "2026-09-06"
statement = "WHEN a deviation's departed rule reference names no rule identifier of the named specification, THE VALIDATOR SHALL reject the deviation."
verification_method = ["test"]
priority = "must"
source = "docs/notes/assessment-specification-readability-2026-09-06.md: the deviation reference accepts any fragment after the specification id, its example is a rule number no specification renders, and nothing checks that the fragment exists."

[relations]
derives_from = ["CAP-TCM-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-06T10:57:11Z"
decided_by = "product-owner"
reason = "Approved by the accountable repository owner on 2026-09-06 with the instruction 'approve as recommended' on PR #358 (REQ-TCM-014, REQ-TCM-015, REQ-TCM-016, SPEC-TCM-006, VER-TCM-006, WO-TCM-009), after the product owner disposed DEC-TCM-001 to DEC-TCM-004 with the options the assessment recommends: identifiers, eight-sections, mechanical-table, advisory-then-blocking."
+++

# Requirement: A deviation names a rule that exists

## In plain words

A deviation says which rule an implementation cannot meet. That rule must
be a real one, named by its identifier, so the link resolves and a typo is
caught before anyone decides on it.

## Why

Since the 0.15.0 root a deviation carries a reference of the form
specification id, hash, fragment. The fragment is free text today. With
rule identifiers as the only rule identity, the fragment is the identifier,
the validator can check it and the Explorer can anchor it. No deviation
exists yet, so the check can be an error from the start.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| A deviation is validated | Its `against` fragment equals a rule identifier defined in the named specification's rules section | The validator reports a decision-management error; the graph is invalid until the reference is corrected |
| The Explorer renders a specification | Each rule carries an anchor equal to its identifier, and a deviation's reference links to it | Not applicable |

## Examples

### Normal

**Given** a deviation against `SPEC-TCM-006#TCM-RFS-003` and a specification
defining that rule,

**When** the validator runs,

**Then** the deviation validates and the Explorer link opens the rule.

### Failure

**Given** a deviation against a fragment reading `rule-7`,

**When** the validator runs,

**Then** the validator reports the error naming the specification and the
fragment, and validation fails.
