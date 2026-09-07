+++
id = "REQ-RSK-013"
type = "requirement"
title = "The answer is given once, on the decision, and copied to the risk"
status = "approved"
owners = ["product-owner"]
created = "2026-09-07"
updated = "2026-09-07"
statement = "WHEN the decision concerning a raised risk is disposed, THE HARNESS SHALL move the risk to the state the chosen option names."
verification_method = ["test"]
priority = "must"
source = "PR #156 REQ-RSK-003, retired with its branch; DR-DECISION-DISPOSE, which already names the accountable role and records the answer verbatim"
measure = "one command disposes the decision and moves the risk; no second decision right is exercised; the risk's disposition names the option, the role, the time and the verbatim reason"

[relations]
derives_from = ["CAP-RSK-010"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-07T20:49:30Z"
decided_by = "product-owner"
reason = "Approved by the accountable owner on 2026-09-07, by selecting the presented option in the ratified decision channel. The answer is given once, on the decision, and copied to the risk in the same act."
+++

# Requirement: The answer is given once, on the decision, and copied to the risk

## In plain words

The owner answers the decision, and the same act moves the risk. Nobody answers
a risk twice, and nobody edits the answer by hand.

## Why

Two records of one answer drift apart, and the reader cannot tell which is
authoritative. Recording the answer where the harness already records answers
keeps the role, the time and the verbatim words in one place. Copying it onto
the risk keeps the risk readable on its own, without a second act to forget.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| the decision is disposed with accept | the risk becomes accepted and carries the revisit trigger | the disposition is refused and nothing moves |
| the decision is disposed with avoid | the risk becomes avoided and names what avoided it | the disposition is refused and nothing moves |
| the decision is disposed with mitigate | the risk becomes mitigating and names the work order | the disposition is refused and nothing moves |
| a disposition is written into a risk by hand | the risk is rejected | the graph reports the hand-written answer |

## Examples

### Normal

**Given** a raised risk and its pending decision,

**When** the owner disposes the decision choosing to accept,

**Then** the risk reads accepted with the owner's words and revisit trigger.

### Failure

**Given** a risk whose answer was typed into the file,

**When** the graph is read,

**Then** the risk is rejected because no disposing act recorded it.
