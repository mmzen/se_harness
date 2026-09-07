+++
id = "REQ-RSK-010"
type = "requirement"
title = "A risk carries one cause, one effect, and a measured size"
status = "approved"
owners = ["product-owner"]
created = "2026-09-07"
updated = "2026-09-07"
statement = "THE VALIDATOR SHALL reject a risk whose likelihood or impact is outside one to five, or whose recorded score is not their product."
verification_method = ["test", "inspection"]
priority = "must"
source = "PR #156 REQ-RSK-001, retired with its branch; ARTIFACT_AUTHORING.md, whose risk checklist already requires one cause, one effect, one threatened stage and the five-by-five scale"
measure = "likelihood and impact are integers 1 to 5; score equals their product, 1 to 25; a risk with a hand-written score that disagrees is rejected"

[relations]
derives_from = ["CAP-RSK-010"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-07T20:49:30Z"
decided_by = "product-owner"
reason = "Approved by the accountable owner on 2026-09-07, by selecting the presented option in the ratified decision channel. One cause, one effect, and a five-by-five measurement whose product is checked."
+++

# Requirement: A risk carries one cause, one effect, and a measured size

## In plain words

A risk file says what could go wrong, what it would cost, and how big it is on
a five-by-five scale. The size is arithmetic, not opinion.

## Why

Two threats of very different size read the same in prose, so an owner cannot
tell which one deserves attention. A number that anyone may type is a number
anyone may soften. Making the score the product of two declared judgements
keeps the judgement visible and the arithmetic beyond argument.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| always | likelihood and impact are integers from one to five | a value outside the range is rejected with a code |
| a risk records a score | the score equals likelihood times impact | a disagreeing score is rejected with a code |
| a risk omits its cause, effect, or threatened stage | the omission is rejected | the risk cannot be recorded |

## Examples

### Normal

**Given** a risk with likelihood three and impact four,

**When** the graph is read,

**Then** the risk carries score twelve and no finding.

### Failure

**Given** a risk with likelihood three, impact four, and score four,

**When** the graph is read,

**Then** the risk is rejected because the score is not the product.
