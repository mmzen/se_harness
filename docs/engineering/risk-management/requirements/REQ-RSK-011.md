+++
id = "REQ-RSK-011"
type = "requirement"
title = "Every recorded risk is raised for an answer"
status = "draft"
owners = ["product-owner"]
created = "2026-09-07"
updated = "2026-09-07"
statement = "WHEN a risk is recorded, THE HARNESS SHALL move it to raised carrying the score computed from its likelihood and impact."
verification_method = ["test"]
priority = "must"
source = "PR #156 REQ-RSK-002, retired with its branch; the acceptance level it read from configuration is removed here, so no recorded risk is exempt"
measure = "the raise command writes status raised and the computed score in one act; no recorded risk stays in identified after the command returns"

[relations]
derives_from = ["CAP-RSK-010"]
+++

# Requirement: Every recorded risk is raised for an answer

## In plain words

Writing a risk down is the same act as putting it in front of its owner. There
is no threshold below which a risk is filed and forgotten.

## Why

A threshold is a number nobody can defend, and any value above one creates a
register of threats that no one ever answers. Raising everything keeps the cost
proportionate instead: a small risk costs the owner one sentence, a large one
costs attention. The size then informs the answer rather than gating whether an
answer is owed.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| a risk is recorded by the command | the risk is raised with its computed score | the command writes nothing and refuses |
| a risk file is added by hand in identified | the graph reports it as not yet raised | the threatened stage is not stopped by it |

## Examples

### Normal

**Given** a domain with no risks,

**When** a threat is recorded with likelihood two and impact five,

**Then** the new risk is raised and carries score ten.

### Failure

**Given** a threat recorded with likelihood seven,

**When** the risk would be raised,

**Then** the command refuses and no file is written.
