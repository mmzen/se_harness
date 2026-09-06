+++
id = "DEC-TCM-004"
type = "decision"
title = "The regime of the specification budgets"
status = "decided"
owners = ["product-owner"]
created = "2026-09-06"
updated = "2026-09-06"
kind = "question"
question = "Do the specification advisories stay advisory, or become blocking at approval after one release, in step with the requirement, intent and capability families?"
raised_by = "engineering-owner"
recommendation = "advisory-then-blocking"

[[options]]
id = "advisory-then-blocking"
label = "Advisory for one release, then blocking at approval through the existing authoring predicate, executed by a later work order together with the three earlier families."

[[options]]
id = "advisory-only"
label = "The advisories inform and never block; the shape is a convention the reviewer enforces."

[relations]
concerns = ["REQ-TCM-014", "REQ-TCM-015"]
blocks = ["REQ-TCM-014", "REQ-TCM-015"]

[disposition]
option = "advisory-then-blocking"
label = "Advisory for one release, then blocking at approval through the existing authoring predicate, executed by a later work order together with the three earlier families."
decided_by = "product-owner"
decided_at = "2026-09-06T10:56:43Z"
reason = "Disposed by the accountable product owner on 2026-09-06 with the instruction 'approve as recommended' on PR #358, taking the option the assessment docs/notes/assessment-specification-readability-2026-09-06.md recommends."

[[lifecycle_events]]
from = "open"
to = "decided"
decided_at = "2026-09-06T10:56:43Z"
decided_by = "product-owner"
reason = "Disposed by the accountable product owner on 2026-09-06 with the instruction 'approve as recommended' on PR #358, taking the option the assessment docs/notes/assessment-specification-readability-2026-09-06.md recommends."
+++

# Decision: The regime of the specification budgets

## Question

The requirement, intent and capability families were each decided as
"advisory for one release, then blocking at approval". The specification
family is the fourth; its advisories are `W-AUT-019` to `W-AUT-023` and
the shared budgets with specification constants.

## Options

**advisory-then-blocking.** The same regime as the three earlier
families: one release of advisories to learn the shape, then the
`QGP-G1-AUTHORING` predicate refuses approval of a draft that still draws
one. The blocking step is a later work order that turns all four families
at once.

**advisory-only.** The validator informs and the reviewer decides. The
shape depends on review attention, and the four families would run under
two regimes.

## Recommendation

`advisory-then-blocking`, so the four definition types share one regime
and one later work order turns them together.

## Disposition

Written by `harnessctl decide`; do not edit by hand.
