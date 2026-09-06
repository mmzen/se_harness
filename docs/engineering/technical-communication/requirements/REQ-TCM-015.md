+++
id = "REQ-TCM-015"
type = "requirement"
title = "Coverage of a requirement by named rules"
status = "draft"
owners = ["product-owner", "quality-owner"]
created = "2026-09-06"
updated = "2026-09-06"
statement = "WHEN a specification's coverage table omits a requirement it specifies or names a rule it does not define, THE VALIDATOR SHALL report the gap on the draft."
verification_method = ["test", "inspection"]
priority = "must"
source = "docs/notes/assessment-specification-readability-2026-09-06.md: 26 specifications carry a hand-written coverage table and all 26 are complete; 83 bodies never name a requirement they specify; the validator checks that a requirement has a specification, not that a rule covers it."

[relations]
derives_from = ["CAP-TCM-001"]
+++

# Requirement: Coverage of a requirement by named rules

## In plain words

A specification promises that each requirement it specifies is met by at
least one of its rules. The promise is a small table, and the validator
reads it so the reader does not have to.

## Why

The checklist asks that every specified requirement be covered by a rule,
and nothing checks it. Twenty-six authors wrote the table by hand and all
twenty-six kept it complete. The other 109 files leave the reader to find
the covering rule in the whole body.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| A specification draft is validated | Every requirement in `specifies` has a row and every rule the table names exists | A missing table, requirement or rule is an advisory; validation still passes |
| The Explorer is generated | A specification record shows its table; a requirement record lists the rules that cover it, from the same table | A requirement covered by no rule shows an empty list |

## Examples

### Normal

**Given** a draft specifying two requirements with a table mapping each to
two existing rule identifiers,

**When** the validator runs and the Explorer is generated,

**Then** no advisory fires and each requirement's record lists its rules.

### Failure

**Given** a draft specifying three requirements whose table names two of
them and one rule identifier that is not in the rules section,

**When** the validator runs,

**Then** one advisory names the missing requirement and one names the
unknown rule, and validation passes.
