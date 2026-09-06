+++
id = "REQ-TCM-014"
type = "requirement"
title = "A specification rule the reader can cite and test"
status = "draft"
owners = ["product-owner", "quality-owner"]
created = "2026-09-06"
updated = "2026-09-06"
statement = "WHEN a specification draft departs from the reader-first shape, its contract sentence, its rule identity or its rule shape, THE VALIDATOR SHALL report each departure on the draft."
verification_method = ["test", "inspection"]
priority = "must"
source = "docs/notes/assessment-specification-readability-2026-09-06.md: 135 specifications, median body 760 words at reading grade 18.4, 79 heading shapes; 71 files number their rules and 41 use stable identifiers because the template and the checklist disagree; 737 of 1,431 rules carry a normative verb; the owner accepted the proposal on 2026-09-06."

[relations]
derives_from = ["CAP-TCM-001"]
+++

# Requirement: A specification rule the reader can cite and test

## In plain words

A specification is a list of rules that a test can cite, a work order can
execute and a deviation can name. Each rule gets a stable name and one
sentence, and the validator tells the author while the file is a draft.

## Why

The assessment of 2026-09-06 found two rule identities: the template says
"number rules", the checklist says "stable identifier". A number moves when
a rule is inserted, so amended specifications only append. Half the rules
carry no word that makes them an obligation. Nothing mechanical checks any
of it.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| A specification draft is validated | The validator reports a missing or long contract, a rule without an identifier, keyword or single sentence, a duplicate identifier, prose over budget, a legacy heading | Each departure is an advisory; validation still passes |
| An approved specification is validated | No shape, identity or budget advisory fires | Not applicable |
| The contract field is present but empty or not a string | The validator reports the structural error it reports for `source` | The graph is invalid until the field is fixed |

## Examples

### Normal

**Given** a draft with a 20-word contract and nine one-sentence rules led
by identifiers,

**When** the validator runs,

**Then** no advisory names the file.

### Failure

**Given** a draft whose rules are a numbered list of 60-word descriptions,

**When** the validator runs,

**Then** advisories name the identity and the shape, and validation passes.
