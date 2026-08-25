+++
id = "INT-RSK-001"
type = "intent"
title = "Make risk a first-class governed fact with one accountable disposer"
status = "draft"
owners = ["product-owner", "domain-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
+++

# Intent: Make risk a first-class governed fact with one accountable disposer

## Problem

The formal chain records why a change exists, what was approved, how it was
checked, and who decided; it records nothing about what could go wrong, how
badly, or who chose to live with it. Deviations are captured in verification
transition reasons; risks live in prose or nowhere. In the week of 2026-08-25
this repository recorded eleven accepted deviations and no risk, although a
ready record orphaned by a rebase and a governor upgrade re-governing every
repository were both foreseeable. An attestation that "risks were identified
and mitigated or accepted" cannot be made on that basis.

## Outcome

Anyone, including a coding agent mid-implementation, can identify a risk
where it arises. Repository policy decides whether it must be raised. When
raised, exactly one accountable role — the owner of the stage the risk
threatens — accepts, avoids, or mitigates it, and the stage it threatens is
blocked until then. Mitigation is ordinary governed work, and a release names
every risk it ships with.

## Scope boundary

In scope: one artifact type, one lifecycle family, one decision right, one
gate predicate applied to existing gates, two commands, one scope exception,
one configuration section, validator and template support. Out of scope:
quantitative risk models, per-category levels, a dedicated risk-owner role,
independence between raiser and disposer.

## Accountable product owner

The `product-owner` role decides this intent; the `domain-owner` decides the
capability and requirements derived from it.

## Success measure

- A risk raised during implementation blocks the handoff check until disposed.
- A release record lists every accepted or mitigated risk threatening its work.
- A repository with no risk artifact behaves exactly as before.
