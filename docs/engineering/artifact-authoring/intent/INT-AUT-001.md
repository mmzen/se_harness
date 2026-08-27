+++
id = "INT-AUT-001"
type = "intent"
title = "Make artifact quality a policy the tool can check, not advice in a skill"
status = "approved"
owners = ["product-owner", "domain-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T18:44:01Z"
decided_by = "product-owner"
+++

# Intent: Make artifact quality a policy the tool can check, not advice in a skill

## Problem

The requirement template offers one statement shape and one free-text
attribute, and the validator enforces one thing about a statement: it
contains `SHALL`. Measured on this repository's 255 requirements on
2026-08-25: 252 use the single `WHEN` shape, including invariants; 64 carry
two or more `SHALL`s (median length 271 characters, longest 584);
`verification_method` has 110 distinct values; 13 approved requirements still
contain template placeholders; the body headings are present in 60-80% of
files and are never checked. The harness's strength is that rules are
predicates; for authoring quality they are prose.

## Outcome

One managed authoring policy states, per artifact type, how a good artifact
is written. The drafting skill applies it; `create-artifact` prints the
type's checklist; the validator carries every rule that can be mechanical;
the requirement template offers the five EARS shapes and a slimmer body
linked to executable acceptance scenarios.

## Scope boundary

In scope: one managed policy, the requirement template and its validator
rules, a closed verification-method vocabulary, three optional attributes,
two approval predicates, and the `create-artifact` checklist. Out of scope:
new skills, elicitation procedures, changes to other templates beyond the
policy's guidance, and any lifecycle or decision-right change.

## Accountable product owner

The `product-owner` decides this intent; the `domain-owner` decides the
capability and requirements derived from it.

## Success measure

- A new requirement written under the policy fails validation on a second
  `SHALL` warning, an unrecognised opener, or a leftover placeholder at approval.
- `verification_method` is queryable: at most four values, as an array.
- The policy is one managed file every agent route can find, and no skill
  restates it.
