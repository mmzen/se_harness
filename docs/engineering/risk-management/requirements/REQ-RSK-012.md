+++
id = "REQ-RSK-012"
type = "requirement"
title = "A raised risk stops the threatened stage through a decision"
status = "approved"
owners = ["product-owner"]
created = "2026-09-07"
updated = "2026-09-07"
statement = "WHILE a risk is raised, THE VALIDATOR SHALL require a pending decision whose blocked artifacts are exactly the artifacts the risk threatens."
verification_method = ["test", "analysis"]
priority = "must"
source = "PR #156 REQ-RSK-004, retired with its branch; SPEC-DCM-001 rule 5, which already stops every transition of a blocked artifact while a decision is pending"
measure = "no new gate predicate is added; a raised risk without a matching pending decision is a graph error; the transition refusal names the decision, not the risk"

[relations]
derives_from = ["CAP-RSK-010"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-07T20:49:30Z"
decided_by = "product-owner"
reason = "Approved by the accountable owner on 2026-09-07, by selecting the presented option in the ratified decision channel. The stop is the decision family's existing stop, not a second gate."
+++

# Requirement: A raised risk stops the threatened stage through a decision

## In plain words

A raised risk does not stop anything by itself. It must name a pending decision,
and that decision is what holds the threatened artifacts still.

## Why

The harness already stops a stage while a decision is pending, and that
mechanism is delivered and covered. A second way to stop a stage would mean two
things an owner must learn and two places a stop can hide. Tying the risk to a
decision keeps one stopping rule and puts the accountable answer where the tool
already records answers.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| a risk is raised | a pending decision blocks exactly the threatened artifacts | a missing or unequal decision is a graph error |
| a threatened artifact asks to move | the existing decision check refuses the move | none new |
| the decision is disposed | the threatened artifacts may move again | none new |

## Examples

### Normal

**Given** a raised risk threatening one work order,

**When** that work order asks to become implemented,

**Then** the refusal names the pending decision and its options.

### Failure

**Given** a raised risk naming no pending decision,

**When** the graph is read,

**Then** the risk is reported as raised without a decision.
