+++
id = "DEC-TCM-003"
type = "decision"
title = "Mechanical coverage of requirements by rules"
status = "open"
owners = ["product-owner"]
created = "2026-09-06"
updated = "2026-09-06"
kind = "question"
question = "Is the coverage table read by the validator and rendered by the Explorer on both sides, or is coverage left to the specifies relation alone?"
raised_by = "engineering-owner"
recommendation = "mechanical-table"

[[options]]
id = "mechanical-table"
label = "The Coverage table is the authoritative map from requirement to rules; the validator reads it on drafts and the Explorer shows it on the specification and on each requirement."

[[options]]
id = "relation-only"
label = "The specifies relation remains the only coverage statement; a coverage table is optional prose nothing reads."

[relations]
concerns = ["REQ-TCM-015", "SPEC-TCM-006"]
blocks = ["REQ-TCM-015"]
+++

# Decision: Mechanical coverage of requirements by rules

## Question

The checklist asks that every specified requirement be covered by at least
one rule. The validator checks that a requirement has some active
specification, not that a rule covers it. Twenty-six specifications carry
a hand-written coverage table and all twenty-six are complete; 83 bodies
never name a requirement they specify.

## Options

**mechanical-table.** The `Coverage` table maps each specified requirement
to the rule identifiers that meet it. The validator reports on a draft a
missing table, a requirement without a row, or a row naming an undefined
rule. The Explorer shows the table on the specification and, on each
requirement, the rules that cover it, from the same source. It depends on
`DEC-TCM-001` choosing identifiers.

**relation-only.** Nothing changes: a requirement is covered by a relation
to a file, and the reader finds the covering rule by reading the file.

## Recommendation

`mechanical-table`. Twenty-six authors have shown the form works and stays
complete; making it read gives the requirement's reader the one thing the
relation cannot, the rule.

## Disposition

Written by `harnessctl decide`; do not edit by hand.
