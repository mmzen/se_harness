+++
id = "REQ-TCM-008"
type = "requirement"
title = "Pending decisions are read from the graph, not from a section"
status = "draft"
owners = ["product-owner", "quality-owner"]
created = "2026-09-04"
updated = "2026-09-04"
statement = "WHEN a definition is checked for approval, THE AUTHORING GATE SHALL read its pending decisions from the decision artifacts that block it and require no Open decisions section."
verification_method = ["test"]
priority = "must"
source = "SPEC-DCM-001 rule 11 and the owner's decision of 2026-09-04: with the decision artifact in place the section is a second source of truth"

[relations]
derives_from = ["CAP-TCM-001"]
+++

# Requirement: Pending decisions are read from the graph, not from a section

## In plain words

Since `WO-DCM-001`, a pending question is a decision artifact that names the
artifacts it blocks. The `Open decisions` paragraph at the end of every
definition then only repeats what the graph already knows, or contradicts
it. New definitions do not carry the section; old ones keep theirs until
amended for another reason.

## Why

The section once held a question inline and blocked approval by reading
anything but `None`. Both jobs moved: prose there is refused, and the
`QGP-G1-DECISION` and `QGP-G2-DECISION` predicates block approval from the
decision's `blocks` relation. What remains is a line that can say `None`
while a decision is open, and nothing checks the two against each other.
Removing the section leaves one source of truth.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| A definition without an `Open decisions` section is checked for approval | The authoring gate passes on that point; the decision predicate of the gate decides from the graph | An open decision blocking the definition fails the decision predicate, naming the decision and the `decide` command |
| A definition that still carries the section is checked | The section reads `None` or lists `DEC-` identifiers; prose is `E-DCM-004`, unchanged | The refusal is unchanged from `SPEC-DCM-001` |
| A definition is created from the managed template | The template has no `Open decisions` section | Not applicable |

## Examples

### Normal

**Given** a requirement draft in the reader-first shape with no
`Open decisions` section and no decision blocking it,

**When** its approval is checked,

**Then** `QGP-G1-AUTHORING` and `QGP-G1-DECISION` both pass.

### Failure

**Given** the same draft and an open `DEC-` naming it in `blocks`,

**When** its approval is checked,

**Then** `QGP-G1-DECISION` fails naming the decision; the absence of the
section is not mentioned.

## Open decisions

None.
