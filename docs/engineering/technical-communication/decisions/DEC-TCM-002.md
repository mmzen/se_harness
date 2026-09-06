+++
id = "DEC-TCM-002"
type = "decision"
title = "The shape of the specification template"
status = "decided"
owners = ["product-owner"]
created = "2026-09-06"
updated = "2026-09-06"
kind = "question"
question = "Does the specification template become eight reader-first sections with a contract field, or keep its fourteen sections with only the identifier and coverage changes?"
raised_by = "engineering-owner"
recommendation = "eight-sections"

[[options]]
id = "eight-sections"
label = "A contract field and eight sections: In plain words, Scope, Terms, Rules, Failure behaviour, Examples, Coverage, Not decided here; nine former sections become optional guidance."

[[options]]
id = "fourteen-kept"
label = "The fourteen sections stay; only the rule identifier and the coverage table are added."

[relations]
concerns = ["REQ-TCM-014", "SPEC-TCM-006"]
blocks = ["REQ-TCM-014"]

[disposition]
option = "eight-sections"
label = "A contract field and eight sections: In plain words, Scope, Terms, Rules, Failure behaviour, Examples, Coverage, Not decided here; nine former sections become optional guidance."
decided_by = "product-owner"
decided_at = "2026-09-06T10:56:28Z"
reason = "Disposed by the accountable product owner on 2026-09-06 with the instruction 'approve as recommended' on PR #358, taking the option the assessment docs/notes/assessment-specification-readability-2026-09-06.md recommends."

[[lifecycle_events]]
from = "open"
to = "decided"
decided_at = "2026-09-06T10:56:28Z"
decided_by = "product-owner"
reason = "Disposed by the accountable product owner on 2026-09-06 with the instruction 'approve as recommended' on PR #358, taking the option the assessment docs/notes/assessment-specification-readability-2026-09-06.md recommends."
+++

# Decision: The shape of the specification template

## Question

Four of the fourteen template sections are present in more than two thirds
of the 135 files; the other ten are present in between 38 and 50 percent
and are often one sentence saying they do not apply. Authors add sections
the template lacks: `Terms` in 27 files, `Failure behaviour` in 32,
`Coverage` in 26. The median body is 760 words at reading grade 18.4, and
91 files carry more than 300 words outside their rules and examples.

## Options

**eight-sections.** The template carries a `contract` field and the eight
sections the corpus actually uses, in the order a reader needs them. The
nine rarely-used sections move to the authoring guide as optional, each
with one sentence on when it earns its place. New drafts are shorter and
one shape; approved files are untouched.

**fourteen-kept.** The template keeps its fourteen questions and gains the
identifier and the coverage table. Authors keep writing sections they have
nothing to say in, and the 79 shapes persist because the template does not
match what authors need.

## Recommendation

`eight-sections`. The corpus has already voted with the sections it adds
and the sections it skips; the template should say what authors do.

## Disposition

Written by `harnessctl decide`; do not edit by hand.
