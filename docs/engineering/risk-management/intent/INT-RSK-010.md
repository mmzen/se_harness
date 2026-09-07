+++
id = "INT-RSK-010"
type = "intent"
title = "Make a threat to governed work a measured fact with a recorded answer"
status = "approved"
owners = ["product-owner"]
created = "2026-09-07"
updated = "2026-09-07"
outcome = "An owner can see every known threat to governed work, its size, and the answer given to it, at the moment a stage asks to move."

[relations]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-07T20:49:30Z"
decided_by = "product-owner"
reason = "Approved by the accountable owner on 2026-09-07, by selecting the presented option in the ratified decision channel. The threat a governed repository carries has nowhere to go today; this intent makes it a measured fact with a recorded answer."
+++

# Intent: Make a threat to governed work a measured fact with a recorded answer

## In plain words

A threat to work in flight is written down today in prose, or not at all. This
initiative makes it a governed file with a size and an answer.

## Problem

A threat noticed during work has nowhere to go. It lands in a pull-request
comment or a reviewer's memory, and the stage moves on without an answer. Two
threats of very different size read the same, because nothing records how likely
or how damaging either is. When one arrives, no record says who accepted it. The
authoring policy already sends a threat to its own artifact, and that artifact
does not exist.

## Success measures

| Measure | Today | When reached | Observed |
| --- | --- | --- | --- |
| Releases whose notes state the threats carried | none | every release | the release notes |
| Threats that arrived unwritten | not measured | none over two releases | the incident notes |
| Days a threat waits for an answer | not measured | under seven, median | the Explorer's in-flight tile |

## Not this

- Threat modelling or an external register.
- Alerting, monitoring, or incident response.
- Any change to how a pending question is answered.
- Probability arithmetic beyond one judgement.
