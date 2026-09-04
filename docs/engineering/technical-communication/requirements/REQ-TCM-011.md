+++
id = "REQ-TCM-011"
type = "requirement"
title = "The Explorer shows an intent's outcome"
status = "draft"
owners = ["product-owner", "quality-owner"]
created = "2026-09-04"
updated = "2026-09-04"
statement = "WHEN an intent carries an outcome, THE EXPLORER SHALL show the outcome and the plain words beneath the intent's title wherever the intent is shown."
verification_method = ["test"]
priority = "should"
source = "docs/notes/assessment-intent-readability-2026-09-04.md: the Explorer renders nothing intent-specific and its G0 intent-quality condition is fixed at not_assessable"

[relations]
derives_from = ["CAP-TCM-001"]
+++

# Requirement: The Explorer shows an intent's outcome

## In plain words

Whoever opens an intent in the Explorer, or reaches it from a work order's
first gate, sees the outcome sentence and the plain words before anything
else. An intent without them shows what it shows today.

## Why

Every work order's first gate asks whether an approved intent is reachable,
and the Explorer answers with a title. The record panel renders a
requirement's statement and plain words first; an intent has had no
equivalent because no field held its outcome. The G0 condition on intent
quality has been a constant, `not_assessable`, since it was written. With
an outcome field it can become a derived observation.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| The bundle is generated from an intent carrying `outcome` and `In plain words` | The intent's record projects both; the record panel renders the outcome, then the plain words, before the lifecycle events; the lineage board shows the outcome under the title | Not applicable |
| A work order's reachable intent carries an outcome and at least one success-measure row | The G0 `intent_quality` condition reads `satisfied`, as a derived observation | The condition reads `not_assessable`, as today |
| An intent carries neither field | The record renders as today | Not applicable |

## Examples

### Normal

**Given** a bundle generated from a fixture intent with a 22-word outcome
and two plain-words sentences,

**When** the record panel opens on it,

**Then** the outcome is the first text under the title, the plain words
follow, and the lifecycle events come after.

### Failure

**Given** a bundle generated from a legacy intent without `outcome`,

**When** a work order reaching it is inspected on the Readiness view,

**Then** the G0 intent-quality condition reads `not_assessable` and the
record panel shows the title, status, owners and body as today.
