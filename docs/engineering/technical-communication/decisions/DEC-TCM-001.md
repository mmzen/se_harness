+++
id = "DEC-TCM-001"
type = "decision"
title = "The rule identity of a specification"
status = "open"
owners = ["product-owner"]
created = "2026-09-06"
updated = "2026-09-06"
kind = "question"
question = "Does every rule of a new specification carry a stable identifier, or are numbered rules an accepted form?"
raised_by = "engineering-owner"
recommendation = "identifiers"

[[options]]
id = "identifiers"
label = "Every rule of a new draft leads with a stable identifier; a numbered rule draws an advisory; the deviation reference accepts identifiers only."

[[options]]
id = "numbers-tolerated"
label = "Identifiers are the template's form, but a numbered list draws no advisory and the deviation reference accepts any fragment."

[relations]
concerns = ["REQ-TCM-014", "REQ-TCM-016", "SPEC-TCM-006"]
blocks = ["REQ-TCM-014", "REQ-TCM-016"]
+++

# Decision: The rule identity of a specification

## Question

The template says "number rules"; the checklist says "stable identifier".
Of 135 specifications, 71 number their rules and 41 lead each with an
identifier. A rule is cited by number in 29 work orders and 33 evidence
packets, and a number moves when a rule is inserted, so amended
specifications only append. Ten of the eleven specifications drafted in
September lead with identifiers.

## Options

**identifiers.** Every rule of a new draft opens with `<PREFIX>-<AREA>-NNN`
in bold; a paragraph without one draws `W-AUT-020` on the draft; the
deviation reference must name an identifier. Approved numbered files are
untouched and their citations stay true. It costs one token per rule.

**numbers-tolerated.** The template shows identifiers but the validator is
silent about numbers, and a deviation may point at `rule-7`. Two identities
persist, the Explorer cannot anchor a number, and a typo in a fragment is
not caught.

## Recommendation

`identifiers`. It is what the checklist already asks, what the September
drafts already do, and the only form the deviation anchor and the coverage
table can be checked against.

## Disposition

Written by `harnessctl decide`; do not edit by hand.
