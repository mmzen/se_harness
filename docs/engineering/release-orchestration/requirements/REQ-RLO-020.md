+++
id = "REQ-RLO-020"
type = "requirement"
title = "Report delivery completion without granting authority"
status = "draft"
owners = ["mmzen"]
created = "2026-09-28"
updated = "2026-09-28"
statement = "The repository SHALL report formal release authorization, evaluator publication and overall delivery completion separately; overall delivery remains incomplete while a declared surface is pending, failed, unobserved or deferred."
verification_method = ["test", "inspection"]
priority = "must"
source = "2026-09-28 marketplace audit and approved release-procedure correction plan"

[relations]
derives_from = ["CAP-RLO-004"]
+++

# Requirement: Report delivery completion without granting authority

## In plain words

An authorized release may still have delivery work left. A successful evaluator
publication is one result within that delivery, not its final completion claim.

## Why

The existing completion sentence covers the evaluator, demonstration and
markers but can hide an old marketplace and stale current instructions.

## Behavior

| Trigger | Response | On failure |
| --- | --- | --- |
| Any delivery stage finishes or stops | Report each surface and its evidence, unresolved items, owners and next actions. | Missing or invalid input yields a visible non-complete result. |
| Every surface has matching evidence, including justified unchanged surfaces | Report overall delivery complete as an operational observation. | Any unresolved or deferred surface keeps overall delivery incomplete. |
| A report is generated | Keep formal release state, publication status and delivery status distinct. | Do not infer lifecycle transitions, permission to publish or human acceptance. |
| A deferral is recorded | Show its human decision reference, reason, owner and revisit trigger. | Deferral does not satisfy an obligation or waive a required harness gate. |

## Examples

### Normal

**Given** all declared updates and justified unchanged surfaces have matching
retained evidence, **when** closeout runs, **then** it reports complete delivery
without changing any formal record or public state.

### Failure

**Given** a released RLS and successful evaluator publication but pending plugin
publication, **when** closeout runs, **then** it reports the evaluator success
and overall delivery incomplete with the plugin owner and next action.
