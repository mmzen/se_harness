+++
id = "INT-KIS-001"
type = "intent"
title = "Make the harness practical for one early-stage user"
status = "approved"
owners = ["product-owner"]
created = "2026-09-13"
updated = "2026-09-13"

outcome = "The owner can develop the project with fewer needless interruptions while retaining clear evidence for meaningful decisions."

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-13T16:40:43Z"
decided_by = "product-owner"
reason = "The owner accepted all 38 candidates in the retained 2026-09-13 codebase KISS review and requested the work orders: \"OK ! Let's create the work orders to implement all candidates\". Record the product-owner approval of INT-KIS-001 within that accepted scope and the established delegated route. SPEC-KIS-001 makes the replacement contracts and seven retained protections explicit; the coverage map assigns all candidates. This records definition approval or bounded execution delegation only, not implementation start, completion, verification, release, merge, publication, live adoption or historical evidence deletion."
+++

# Make the harness practical for one early-stage user

## In plain words

The owner can change the project without repeatedly fixing paperwork and checks for problems they do not have.

## Problem

The project has exactly one user and is still young. Small changes encounter formatting rules, repeated identity checks and release rehearsals.
The accepted codebase review records the observed examples. These costs slow the same owner who must maintain the extra machinery.

## Success measures

| Measure | Today | When reached | Observed |
| --- | --- | --- | --- |
| Work interrupted only by formatting or unavailable GitHub | Observed in the accepted review | No such interruption in the owner's next three tasks | Owner's normal task sessions |
| Release rehearsal on an ordinary change | Runs on ordinary PRs | Absent when build and publication inputs are unchanged | Owner's next three ordinary PRs |
| New copied repositories in evidence | Large retained historical trees | None added by new ordinary runs | Owner's monthly checkout review |

## Not this

- A new enterprise assurance framework or threat model.
- Removal of safeguards for user files, released packages or accountable decisions.
