+++
id = "REQ-TCM-017"
type = "requirement"
title = "A draft that still draws an authoring advisory is not approved"
status = "draft"
owners = ["product-owner", "quality-owner"]
created = "2026-09-06"
updated = "2026-09-06"
statement = "WHEN a draft intent, capability, requirement or specification that still draws an authoring advisory is transitioned to approved, THE GATE SHALL refuse the transition and name each advisory."
verification_method = ["test", "inspection"]
priority = "must"
source = "DEC-TCM-004 (disposed 2026-09-06, advisory-then-blocking) and the same choice recorded for the requirement, intent and capability families in SPEC-TCM-003, SPEC-TCM-004 and SPEC-TCM-005; the reading of 2026-09-06 that six of the nine definitions drafted under the 0.15.0 root would have been refused."

[relations]
derives_from = ["CAP-TCM-001"]
+++

# Requirement: A draft that still draws an authoring advisory is not approved

## In plain words

The writing advisories stay advice while a file is drafted and reviewed.
At the one moment an owner approves the draft, any advisory left on it
stops the approval until the draft is fixed.

## Why

The owner decided the same regime four times: advisory for one release,
then blocking at approval. Advice alone does not hold the shape. Of the
nine definitions drafted since the 0.15.0 root, six were approved with
advisories on them. The approval step already refuses a draft for an open
decision; it can refuse one for its writing the same way.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| An owner approves a draft of one of the four definition kinds | The approval gate reads the draft's advisories; with none, the approval proceeds as today | With one or more, the transition is refused and each advisory is named |
| `validate` runs with advisories present | Advisories stay listed apart from errors and warnings; validation passes | Not applicable |
| An approved artifact is transitioned further | No advisory is read | Not applicable |

## Examples

### Normal

**Given** a requirement draft within every budget,

**When** the product owner approves it,

**Then** the approval completes as it does today.

### Failure

**Given** a specification draft whose rule `X-Y-004` is 40 words,

**When** the technical owner approves it,

**Then** the gate refuses, names the rule and its budget, and the draft is
approved only after the rule is shortened or split.
