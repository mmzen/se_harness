+++
id = "ADR-CIP-002"
type = "adr"
title = "Freeze a release unit by candidate commit and measure its census"
status = "draft"
owners = ["release-owner"]
created = "2026-08-26"
updated = "2026-08-26"

[relations]
decides = ["ARCH-CIP-001"]
+++

# ADR: Freeze a release unit by candidate commit and measure its census

## Status

Proposed; decided by the release owner with the packet approval.

## Context

A release contract freezes `gates`, an allow-list of implemented work
orders, and forbids amendment. Development continues on `main` during and
after the freeze, so any work order reaching `implemented` invalidates the
contract. The 0.7.0 unit consumed five contracts and three release work
orders in a day; the rejections were correct under the rule, and the rule is
the problem. The tag, when it is created, already selects a commit.

## Decision drivers

A frozen thing must not be changed by unrelated events; the census must
remain exact and reviewable; late fixes must have a route; existing
released records must not be re-shaped.

## Considered options

1. Allow in-place amendment of `gates` — loses the property that an approval
   describes one fixed unit.
2. Freeze `main` while a contract is open — blocks every other work order
   for the release's duration.
3. Name a candidate commit in the contract and derive `gates` from the
   trailers between the previous release tag and that commit; cut a
   `candidate/X.Y.Z` branch when a late fix is needed — the ordinary
   release-branch model.

## Decision

Option 3. `gates` stays as the measured census so existing readers and
validators keep working; the derivation is a command, and the candidate
validator checks the two agree at approval.

## Consequences

A merge to `main` after the cut is not a stop condition. A late fix means a
new candidate commit and a new contract, as before, but only for fixes to
the release itself. Trailer-less commits on the first-parent path become
visible and must be exempted explicitly. The contract template changes;
approved and released contracts are untouched.
