+++
id = "REQ-TCM-012"
type = "requirement"
title = "A capability the reader understands on first reading"
status = "approved"
owners = ["product-owner", "quality-owner"]
created = "2026-09-04"
updated = "2026-09-04"
statement = "WHEN a capability draft departs from the reader-first shape, its ability sentence or its word budgets, THE VALIDATOR SHALL report each departure on the draft before approval is requested."
verification_method = ["test", "inspection"]
priority = "must"
source = "docs/notes/assessment-capability-readability-2026-09-04.md: 36 capabilities, median body 157 words at reading grade 15.7, seven template shapes, the ability sentence present in 29 files and in the template's form in six; the owner's decision of 2026-09-04"

[relations]
derives_from = ["CAP-TCM-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-04T19:45:21Z"
decided_by = "product-owner"
reason = "Approved by the accountable repository owner on 2026-09-04 with the instruction 'i apprive' (approve), after reviewing PR #342 (REQ-TCM-012, REQ-TCM-013, SPEC-TCM-005, VER-TCM-005, WO-TCM-008), carrying the owner's four decisions on the capability assessment of the same day."
+++

# Requirement: A capability the reader understands on first reading

## In plain words

A capability says who can do what, under which conditions, and what it
leaves to others. That one sentence becomes a field the reader and the
Explorer can find. When a draft is longer, denser or shaped differently
from the template, the validator says so while it is still a draft.

## Why

The assessment of 2026-09-04 found the ability sentence buried in a body
that restates the intent above and the requirements below, in one of seven
shapes, with nothing mechanical checking any of it. The template's form,
an actor, `can`, an achievement, `under` conditions, is the right sentence
and six files use it. Making it a field and budgeting the body gives the
next capability a shape its reader can learn once, without rewriting the
36 approved ones.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| A capability draft is validated | The reader-first shape is the template: an `ability` field, `In plain words`, `Actor and need`, `Not decided here`; the validator reports a missing or malformed ability, a body over its budget, a long `Actor and need`, a long sentence, too many code identifiers, a missing or long plain-words summary, or a legacy requirement list | An advisory names the file, the budget and the measured value; validation still passes |
| An approved capability is validated | No shape or budget advisory fires | Not applicable |
| An `ability` field is present but empty or not a string | The validator reports `E-AUT-002`, as it does for `source` | The graph is invalid until the field is fixed or removed |

## Examples

### Normal

**Given** a new capability draft with a 22-word ability naming an actor, a
`can` and an `under`, and a 120-word body in the three sections,

**When** the validator runs,

**Then** no `W-AUT` advisory names the file.

### Failure

**Given** a draft whose ability runs to 60 words without `under` and whose
body ends with a `Candidate requirements` list,

**When** the validator runs,

**Then** advisories name the ability and the legacy list, and `validate`
still reports PASS.

## Open decisions

None.
