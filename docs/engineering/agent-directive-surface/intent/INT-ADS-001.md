+++
id = "INT-ADS-001"
type = "intent"
title = "Make agent directives enforced, bounded, and consistent"
status = "draft"
owners = ["product-owner", "domain-owner"]
created = "2026-08-25"
updated = "2026-08-25"

[relations]
+++

# Intent: Make agent directives enforced, bounded, and consistent

## Problem

The managed harness asks a coding agent to read about 65 KB of policy prose and
41 KB of machine contracts before acting, to return restitution verbatim, to
read every file in a manifest, and to report only effects that occurred. The
evaluator enforces integrity, gates, and provenance; it does not enforce any of
those behavioural obligations. At `0276dd7` a blocked handoff checkpoint named
its own command as the retry, `focus` and `check` disagreed on the next step
for the same state, the owner instructions routed to a document the harness had
withdrawn, and a dozen recurring failure modes lived only in operator memory.

## Outcome

An agent that opens a governed repository receives one bounded reading set for
its phase, one canonical next step per selected state in one dialect, a
corrective command whenever it is blocked, a warning before the traps that
recur, and a restitution block whose provenance can be recomputed. Every
obligation that remains in prose states where it applies.

## Scope boundary

In scope: the managed router, workflow contract, result rendering, preflight
manifest, repository-integrity diagnostics, and CI verification of the
restitution digest. Out of scope: lifecycle states, decision rights, gate
predicates, traceability relations, artifact schemas, and any change to
accountable human authority.

## Accountable product owner

The `product-owner` role decides this intent. The `domain-owner` role decides
the capability and requirements derived from it.

## Success measure

- No conformance-tested restitution names the evaluated command as its own retry.
- `focus --result-schema 2` and `check` resolve the same step for the same state.
- The mandatory reading set for a phase is the preflight manifest plus one card of at most 3072 bytes.
- At least two recurring traps are evaluator diagnostics.
- CI recomputes a declared restitution digest.
