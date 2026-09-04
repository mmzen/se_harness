+++
id = "REQ-TCM-009"
type = "requirement"
title = "An intent the reader understands on first reading"
status = "draft"
owners = ["product-owner", "quality-owner"]
created = "2026-09-04"
updated = "2026-09-04"
statement = "WHEN an intent draft departs from the reader-first shape, its outcome sentence or its word budgets, THE VALIDATOR SHALL report each departure on the draft before approval is requested."
verification_method = ["test", "inspection"]
priority = "must"
source = "docs/notes/assessment-intent-readability-2026-09-04.md: 33 intents, median body 312 words at reading grade about 16, three template generations and nine ad hoc shapes, a checklist of four paragraphs against a template of seven sections, no advisory on an intent"

[relations]
derives_from = ["CAP-TCM-001"]
+++

# Requirement: An intent the reader understands on first reading

## In plain words

An intent says what outcome an owner wants and how anyone will know it was
reached. The reader should find that outcome in one sentence, on first
reading. When a draft has no outcome sentence, is too long, or is shaped
differently from the template, the validator says so while it is a draft.

## Why

The assessment of 2026-09-04 found the intent template asking for seven
sections while the authoring checklist asks for four paragraphs, so
nobody could follow both. Three of the seven sections repeat what the
capability, the specification and the work order say, and carry two thirds
of the median body. No field holds the outcome, so the Explorer shows the
title and three hundred words of college-level prose. Advisories on drafts
change the next intent without rewriting the thirty-three approved ones.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| An intent draft is validated with no `outcome`, an outcome over 30 words, or one containing a code span | One advisory names the file, the budget and the measured value | Not applicable; an advisory never fails validation |
| An intent draft exceeds a body, Problem, sentence, code-identifier or plain-words budget, or cites a file path or line range | One advisory per budget, naming file, budget and value | Not applicable |
| An approved intent, or a legacy one without `outcome`, is validated | No advisory; `validate` passes as before | Not applicable |

## Examples

### Normal

**Given** an intent draft in the reader-first shape, with a 22-word
`outcome`, a 54-word Problem and three success-measure rows,

**When** the repository is validated,

**Then** no `W-AUT` advisory names it and validation passes.

### Failure

**Given** an intent draft with no `outcome`, a 473-word Problem and
sixteen source line ranges,

**When** the repository is validated,

**Then** three advisories name the missing outcome, the Problem budget
and the citations, and validation still passes.
