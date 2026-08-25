+++
id = "CAP-AUT-001"
type = "capability"
title = "Author any formal artifact under one managed policy with mechanical checks"
status = "approved"
owners = ["product-owner", "domain-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
derives_from = ["INT-AUT-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T18:44:01Z"
decided_by = "product-owner"
+++

# Capability: Author any formal artifact under one managed policy with mechanical checks

## Description

A coding agent or engineer drafting a formal artifact receives the
type-specific authoring rules at the moment of creation, writes against a
template whose shapes match the rules, and is stopped by the validator or the
approval gate when a mechanical rule is broken. The rules have one owner, the
managed authoring policy, and are consumed — never restated — by skills,
templates, and commands.

## Users

Coding agents drafting artifacts; requirements stewards and technical owners
approving them; assurance owners reading verification methods.

## Boundaries

The policy grants no authority and decides nothing. Mechanical rules fail
closed in the validator or a gate; judgement rules stay in the policy as
review guidance.

## Derived requirements

`REQ-AUT-001` through `REQ-AUT-006`.
