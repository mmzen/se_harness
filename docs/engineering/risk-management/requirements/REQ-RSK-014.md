+++
id = "REQ-RSK-014"
type = "requirement"
title = "Mitigated is claimed only under verified coverage and a recorded residual"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-07"
updated = "2026-09-07"
statement = "IF a risk claims mitigated without a verified record covering its mitigating work order, THEN THE VALIDATOR SHALL reject it."
verification_method = ["test", "analysis"]
priority = "must"
source = "PR #156 REQ-RSK-005, retired with its branch; TRC-009 and TRC-012, which already make a verified record the only proof that changed state was assessed"
measure = "a risk in mitigated names at least one work order; every named work order is covered by a verified or released record; the residual is present and non-empty"

[relations]
derives_from = ["CAP-RSK-010"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-07T20:49:30Z"
decided_by = "assurance-owner"
reason = "Approved by the accountable owner on 2026-09-07, by selecting the presented option in the ratified decision channel. A mitigation claim rests on a verified record and a written residual, or it is refused."
+++

# Requirement: Mitigated is claimed only under verified coverage and a recorded residual

## In plain words

Saying a threat is handled is a claim about work that was checked. The claim
holds only when a verified record covers the work, and the leftover is written
down.

## Why

"Mitigated" is the sentence a reader trusts most and the one easiest to type
without grounds. Binding it to a verified record makes the claim rest on the
same proof every other completion claim rests on. Requiring the residual keeps
the reader from reading "mitigated" as "gone".

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| a risk asks to become mitigated | a verified record must cover every mitigating work order | the move is refused, naming the uncovered work order |
| a risk asks to become mitigated | the residual must be present | the move is refused, naming the missing residual |
| the mitigating work order is later superseded | the risk keeps its recorded facts unchanged | none |

## Examples

### Normal

**Given** a mitigating risk whose work order a verified record covers,

**When** the assurance owner closes it,

**Then** the risk reads mitigated and states what remains.

### Failure

**Given** a mitigating risk whose work order is only implemented,

**When** the assurance owner tries to close it,

**Then** the move is refused and the risk stays mitigating.
