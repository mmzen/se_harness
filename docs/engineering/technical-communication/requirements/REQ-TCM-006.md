+++
id = "REQ-TCM-006"
type = "requirement"
title = "A requirement the reader understands on first reading"
status = "draft"
owners = ["product-owner", "quality-owner"]
created = "2026-09-04"
updated = "2026-09-04"
statement = "WHEN a requirement draft departs from the reader-first shape or its word budgets, THE VALIDATOR SHALL report each departure on the draft before approval is requested."
verification_method = ["test", "inspection"]
priority = "must"
source = "docs/notes/assessment-requirement-readability-2026-09-04.md: 328 requirements, median body about 400 words at reading grade 14, one statement in four over the authoring rule, two template shapes in use"

[relations]
derives_from = ["CAP-TCM-001"]
+++

# Requirement: A requirement the reader understands on first reading

## In plain words

A requirement is one obligation. The reader should find it, understand it,
and know how to check it, on first reading. When a draft is too long, too
dense, or shaped differently from the template, the validator says so while
the draft is still a draft.

## Why

The assessment of 2026-09-04 measured the corpus: one obligation per file,
surrounded by four hundred words of college-level prose in one of two
template shapes. Nothing mechanical pushed back, so the length was paid by
every author, reviewer and approving owner and bought the everyday reader
nothing. The Explorer shows only the statement, and one statement in four
was longer than the authoring rule allows. Advisories on drafts change the
next requirement without rewriting the approved ones.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| A requirement draft is validated | The reader-first shape is the template: statement, `In plain words`, `Why`, a `Behavior` table, two `Examples`; the validator reports a statement over 30 words, more than one obligation, a body over 250 words, a `Why` over five sentences, a sentence over 25 words, a missing or long plain-words summary, or a body that cites more than three code identifiers | An advisory names the file and the budget it exceeds; validation still passes |
| An approved requirement is validated | No shape or budget advisory fires; approved artifacts are read as history | Not applicable |
| The statement names a concrete component in place of `THE SYSTEM` | The opener is accepted as one of the five EARS shapes | Not applicable |

## Examples

### Normal

**Given** a new requirement draft written in the reader-first shape with a
28-word statement and a 220-word body,

**When** the validator runs,

**Then** no `W-AUT` advisory names the file.

### Failure

**Given** a draft whose statement carries three `SHALL` clauses and whose
body runs to 420 words,

**When** the validator runs,

**Then** advisories name the file for the multiple obligations, the
statement length and the body length, and `validate` still reports PASS.

## Open decisions

None.
